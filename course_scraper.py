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
        prd = {"title" : prd_title,
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
        semester_title = sem_soup.select("h3")[0].text.strip()
        sem= {"title" : semester_title,
              "specializations" : []}

        yield sem_soup, sem


def get_course_data(url, get_exam):
    # Load page from url
    print(f"Reading course data from {url}")
    page = requests.get(url)
    status = page.status_code
    print(f"Status: {status}")

    today = date.today()
    program = curr_soup.select("h1")[0].text.strip()

    courses = {}
    i = 0

    course_data = {
        "version" : 0,
        "date" : today.strftime("%Y-%m-%d"),
        "url" : url,
        "program": program,
        "courses" : {},
        "specializations" : [],
        "semesters" : [],
        "periods" : [],
    }

    curr_soup = BeautifulSoup(page.content, 'html.parser')
    for sem_soup, sem in it_semesters(curr_soup):
        for spec_soup, spec in it_specializations(sem_soup):
            for prd_soup, prd in it_periods(spec_soup):
                for crs_soup, crs in it_courses(prd_soup):
                    if get_exam:
                        crs["examinations"], status = get_examinations(crs["url"])
                        i += 1
                        print(f"  {i}: Status {status}")


                    crs_code = crs["code"]
                    sem_title = sem["title"]
                    spec_title = spec["title"]
                    prd_title = prd["title"]

                    if crs_code in courses:
                        courses[crs_code]["specializations"].append(spec_title)
                        courses[crs_code]["semesters"].append(sem_title)    # TODO: Fix duplicates
                        courses[crs_code]["periods"].append(prd_title)      # TODO: Fix duplicates
                    else:
                        new_crs = {
                            "code" : crs["code"],
                            "name" : crs["name"],
                            "credits" : crs["credits"],
                            "level" : crs["level"],
                            "tt_module" : crs["tt_module"],
                            "ecv" : crs["ecv"],
                            "url" : crs["url"],
                            "examinations" : crs["examinations"],
                            "semesters" : [sem_title],
                            "specializations" : [spec_title],
                            "periods" : [prd_title],
                        }
                        courses[crs_code] = new_crs

    print(f"Finished reading course data for {len(courses)} courses from {url}")

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
save_to_json(course_data, "course_data_v1.json")

# %%
