# %% Imports

import requests
from bs4 import BeautifulSoup
from datetime import date
import json
from supabase import create_client, Client

# TODO: Move
url = "https://xvfdqonvnrxgrkqlcriw.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inh2ZmRxb252bnJ4Z3JrcWxjcml3Iiwicm9sZSI6ImFub24iLCJpYXQiOjE2OTU3OTkxMDUsImV4cCI6MjAxMTM3NTEwNX0.NhtoK8tEeorPphhyQxVAPZVYNsmSBFH3M73L8rMdFFs"
supabase = create_client(url, key)

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
            spec_name = spec_soup.select("caption > span")[0].text
            spec_code = spec_soup.get("data-specialization").strip()
        except:
            # spec_name = "[No Specialization]"
            # spec_code = "none"
            spec_name = ""
            spec_code = ""
        spec= {"name" : spec_name,
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

    # course_data = {
    #     "version" : 1,
    #     "date" : today.strftime("%Y-%m-%d"),
    #     "url" : url,
    #     "language" : lang,
    #     "program": program,
    #     "courses" : {},
    #     "specializations" : {},
    #     "specialization_titles" : [],
    #     "semester_titles" : [],
    # }

    courses_dict = {}
    specializations_dict = {}
    included_in = []

    for sem_soup, sem in it_semesters(curr_soup):
        for spec_soup, spec in it_specializations(sem_soup):
            spec_code = spec["code"]
            if spec_code and spec_code not in specializations_dict:
                specialization = {"code": spec["code"],
                                  "name": spec["name"]}
                specializations_dict[spec_code] = specialization
            for prd_soup, prd in it_periods(spec_soup):
                for crs_soup, crs in it_courses(prd_soup):
                    crs_code = crs["code"]
                    # Add examinations to the course if that option is selected
                    # if get_exam:
                    #     crs["examinations"], status = get_examinations(crs["url"])
                    #     i += 1
                    #     print(f"  {i}: Status {status}")

                    # Add course to course list if not already added
                    if crs_code not in courses_dict:
                        course = {"code" : crs["code"],
                                  "name" : crs["name"],
                                  "credits" : crs["credits"],
                                  "level" : crs["level"],
                                  "tt_module" : crs["tt_module"],
                                         # "ecv" : crs["ecv"],
                                  "url" : crs["url"],
                                        #  "examinations" : crs["examinations"],
                                        #  "semester_titles" : [],
                                        #  "specialization_titles" : [],
                                        #  "period_titles" : [],
                                 }
                        courses_dict[crs["code"]] = course


                    # Add course to specialization courses if elective or compulsory
                    if not spec_code:
                        continue    # Skip this step if we are not in a specialization
                    if ("C" in crs["ecv"] and lang == "eng") or ("O" in crs["ecv"] and lang == "swe"):
                        ecv = "C"
                    elif ("E" in crs["ecv"] and lang == "eng") or ("V" in crs["ecv"] and lang == "swe"):
                        ecv = "E"
                    elif ("V" in crs["ecv"] and lang == "eng") or ("F" in crs["ecv"] and lang == "swe"):
                        ecv = "V"
                    included_in.append({"crs_code": crs_code, "spec_code": spec_code, "ecv": ecv})

    print(f"Finished reading course data for {len(courses_dict)} courses from {url}")

    course_data = {
        "version" : 2,
        "date" : today.strftime("%Y-%m-%d"),
        "url" : url,
        "language" : lang,
        "program": program,
        "courses" : list(courses_dict.values()),
        "specializations" : list(specializations_dict.values()),
        "included_in" : included_in,
    }

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
supabase.table("courses").upsert(course_data["courses"], on_conflict=['code']).execute()
supabase.table("specializations").upsert(course_data["specializations"], on_conflict=['code']).execute()
# try:
# data, count = supabase.table("includedIn").upsert(course_data["included_in"], on_conflict=['crs_code', 'spec_code']).execute()

# except Exception as e:
#     print('ded')
#     print(e)
# data, count = supabase.table("courses").upsert(course_data["courses"]).execute()

# %%
