# %% Imports

import requests
from bs4 import BeautifulSoup
from datetime import date
import json

def get_examinations(url):
    # Load page from url
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    status = page.status_code

    examinations = []

    examinations_table = soup.select("table.table.table-striped.examinations-codes-table")[0]
    for exam in examinations_table.select("tr")[1:]:
        code = exam.select("td")[0].text.strip()
        name = exam.select("td")[1].text.strip()
        scope = exam.select("td")[2].text.strip()
        scale = exam.select("td")[3].text.strip()

        examination = {"code" : code,
                       "name" : name,
                       "scope" : scope,
                       "scale" : scale}

        examinations.append(examination)

    return examinations, status


def it_courses(prd_soup):
    for crs_soup in prd_soup.select("tr.main-row"):
        crs_code = crs_soup.select("td")[0].text.strip()
        crs_name = crs_soup.select("td")[1].text.strip()
        crs_credits = crs_soup.select("td")[2].text.strip()
        crs_level = crs_soup.select("td")[3].text.strip()
        crs_tt_module = crs_soup.select("td")[4].text.strip()
        crs_ecv = crs_soup.select("td")[5].text.strip()

        href = crs_soup.select("a")[0].get("href")
        crs_url = "https://studieinfo.liu.se/" + href

        crs = {"code" : crs_code,
                  "name" : crs_name,
                  "credits" : crs_credits,
                  "level" : crs_level,
                  "tt_module" : crs_tt_module,
                  "ecv" : crs_ecv,
                  "url" : crs_url,
                  "examinations" : []}

        yield crs_soup, crs


def it_periods(spec_soup):
    for prd_soup in spec_soup.select("tbody.period"):
        prd_title = prd_soup.select("th")[0].text.strip()
        prd_number = int(prd_title.split()[1])
        prd = {"title" : prd_title,
               "number" : prd_number,
               "courses" : []}

        yield prd_soup, prd


def it_specializations(sem_soup):
    for spec_soup in sem_soup.select("div.specialization"):
        try:
            spec_title = spec_soup.select("caption > span")[0].text
            spec_code = spec_soup.get("data-specialization").strip()
        except:
            spec_title = "[No Specialization]"
            spec_code = "none"
        spec= {"title" : spec_title,
               "code" : spec_code,
               "periods" : []}

        yield spec_soup, spec


def it_semesters(curr_soup):
    for sem_soup in curr_soup.select("section.accordion.semester"):
        sem_title = sem_soup.select("h3")[0].text.strip()
        sem_number = int(sem_title.split()[1])
        sem= {"title" : sem_title,
              "number" : sem_number,
              "specializations" : []}
        yield sem_soup, sem


def get_course_data(url, get_exam):
    # Load page from url
    print(f"Reading course data from {url}")
    page = requests.get(url)
    status = page.status_code
    print(f"Status: {status}")

    curr_soup = BeautifulSoup(page.content, 'html.parser')

    today = date.today()
    program = curr_soup.select("h1")[0].text.strip()

    i = 0

    lang = "swe"
    if "/en/" in url:
        lang = "eng"

    course_data = {
        "version" : 1,
        "date" : today.strftime("%Y-%m-%d"),
        "url" : url,
        "language" : lang,
        "program": program,
        "courses" : {},
        "specializations" : {},
        "specialization_titles" : [],
        "semester_titles" : [],
    }

    for sem_soup, sem in it_semesters(curr_soup):
        course_data["semester_titles"].append(sem["title"])
        for spec_soup, spec in it_specializations(sem_soup):
            course_data["specialization_titles"].append(spec["title"])
            spec_elective_courses = []
            spec_compulsory_courses = []
            spec_voluntary_courses = []
            for prd_soup, prd in it_periods(spec_soup):
                for crs_soup, crs in it_courses(prd_soup):
                    # Add examinations to the course if that option is selected
                    if get_exam:
                        crs["examinations"], status = get_examinations(crs["url"])
                        i += 1
                        print(f"  {i}: Status {status}")

                    # Add course to course list if not already added
                    if crs["code"] not in course_data["courses"]:
                        course = {"code" : crs["code"],
                                         "name" : crs["name"],
                                         "credits" : crs["credits"],
                                         "level" : crs["level"],
                                         "tt_module" : crs["tt_module"],
                                         # "ecv" : crs["ecv"],
                                         "url" : crs["url"],
                                         "examinations" : crs["examinations"],
                                         "semester_titles" : [],
                                         "specialization_titles" : [],
                                         "period_titles" : []}
                        course_data["courses"][crs["code"]] = course
                    # else:
                    #     course = all_courses[crs["code"]]

                    # Add specialization to list of specializations that take the course
                    if spec["title"] not in course_data["courses"][crs["code"]]["specialization_titles"]:
                        course_data["courses"][crs["code"]]["specialization_titles"].append(spec["title"])

                    # Add semester to list of semesters that the course is given in
                    if sem["title"] not in course_data["courses"][crs["code"]]["semester_titles"]:
                        course_data["courses"][crs["code"]]["semester_titles"].append(sem["title"])

                    # Add period to list of periods that the course is given in
                    if prd["title"] not in course_data["courses"][crs["code"]]["period_titles"]:
                        course_data["courses"][crs["code"]]["period_titles"].append(prd["title"])

                    # Add course to specialization courses if elective or compulsory
                    if ("C" in crs["ecv"] and lang == "eng") or ("O" in crs["ecv"] and lang == "swe"):
                        spec_compulsory_courses.append(course_data["courses"][crs["code"]])
                    if ("E" in crs["ecv"] and lang == "eng") or ("V" in crs["ecv"] and lang == "swe"):
                        spec_elective_courses.append(course_data["courses"][crs["code"]])
                    if ("V" in crs["ecv"] and lang == "eng") or ("F" in crs["ecv"] and lang == "swe"):
                        spec_voluntary_courses.append(course_data["courses"][crs["code"]])

            # Add specialization to program specializations if not already added
            if spec["title"] not in course_data["specializations"]:
                course_data["specializations"][spec["title"]] = {"title" : spec["title"],
                                                                        "elective_courses" : [],
                                                                        "compulsory_courses" : [],
                                                                        "voluntary_courses" : []}

            # Add data about compulsory/elective courses for each specialization
            course_data["specializations"][spec["title"]]["elective_courses"] += spec_elective_courses
            course_data["specializations"][spec["title"]]["compulsory_courses"] += spec_compulsory_courses
            course_data["specializations"][spec["title"]]["voluntary_courses"] += spec_voluntary_courses

            # specialization_data = {"title" : spec["title"],
            #                        "obligatory_courses" : spec_compulsory_courses,
            #                        "elective_courses" : spec_elective_courses,
            #                        "voluntary_courses" : spec_voluntary_courses}
            # course_data["specializations"].append(specialization_data)

    print("Performing le ugli hack...")

    # TODO: Ugly hack below, fix later?
    course_data["courses"] = list(course_data["courses"].values())

    # TODO: Ugly hack below, fix later?
    course_data["specialization_titles"] = list(course_data["specializations"].keys())
    course_data["specializations"] = list(course_data["specializations"].values())



    # # Add data about compulsory/elective courses for each specialization
    # for crs_code, crs in course_data["courses"]:

    #     for spec_title in crs["specializations"]:
    #         course_data["specializations"][spec["title"]]["elective_courses"].append(spec_elective_courses)
    #         course_data["specializations"][spec["title"]]["compulsory_courses"].append(spec_compulsory_courses)
    #         course_data["specializations"][spec["title"]]["voluntary_courses"].append(spec_voluntary_courses)

    print(f"Finished reading course data for {len(course_data['courses'])} courses from {url}")

    return course_data


def save_to_json(data, save_file):
    with open(save_file, "w", encoding="utf8") as f:
        json.dump(data, f)


def load_from_json(save_file):
    with open(save_file, "r", encoding="utf8") as f:
        data = json.load(f)
    return data

# %%

course_data = get_course_data("https://studieinfo.liu.se/en/program/6CDDD/4617#curriculum", get_exam=True)
save_to_json(course_data, "course_data_v2.json")

# %%
print(int("hello 7 world"))