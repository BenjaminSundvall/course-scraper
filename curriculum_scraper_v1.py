# %% Imports

import requests
from bs4 import BeautifulSoup
from datetime import date
import json
# import jq


# %% Define functions
def get_examinations(url):
    # Load page from url
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    status = page.status_code
    print(f"Loading examinations from: {url}")
    print(f"Status: {status}")

    examinations = {}

    examinations_table = soup.select("table.table.table-striped.examinations-codes-table")[0]
    for exam in examinations_table.select("tr")[1:]:
        code = exam.select("td")[0].text.strip()
        name = exam.select("td")[1].text.strip()
        scope = exam.select("td")[2].text.strip()
        scale = exam.select("td")[3].text.strip()

        examinations[code] = {"name" : name,
                              "scope" : scope,
                              "scale" : scale}

    return examinations


def get_courses(period, get_exam):
    courses = {}

    for crs in period.select("tr.main-row"):
        crs_code = crs.select("td")[0].text.strip()
        crs_name = crs.select("td")[1].text.strip()
        crs_credits = crs.select("td")[2].text.strip()
        crs_level = crs.select("td")[3].text.strip()
        crs_tt_module = crs.select("td")[4].text.strip()
        crs_ecv = crs.select("td")[5].text.strip()

        href = crs.select("a")[0].get("href")
        crs_url = "https://studieinfo.liu.se/" + href

        crs_examinations = {}
        if get_exam:
            crs_examinations = get_examinations(crs_url)

        courses[crs_code] = {"name" : crs_name,
                             "credits" : crs_credits,
                             "level" : crs_level,
                             "tt_module" : crs_tt_module,
                             "ecv" : crs_ecv,
                             "url" : crs_url,
                             "examinations" : crs_examinations}

    return(courses)


def get_periods(specialization, get_exam):
    periods = {}

    for i, prd in enumerate(specialization.select("tbody.period")):
        period_title = f"Period {i}"

        periods[period_title] = get_courses(prd, get_exam)

    return periods


def get_specializations(semester, get_exam):
    specializations = {}

    for spec in semester.select("div.specialization"):
        try:
            specialization_title = spec.select("caption > span")[0].text
        except:
            specialization_title = "[No Specialization]"

        specializations[specialization_title] = get_periods(spec, get_exam)

    return specializations


def get_semesters(soup, get_exam):
    semesters = {}

    for sem in soup.select("section.accordion.semester"):
        semester_title = sem.select("h3")[0].text.strip()

        semesters[semester_title] = get_specializations(sem, get_exam)

    return semesters


def get_curriculum(url, get_exam):
    # Load page from url
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    status = page.status_code
    print(f"Status: {status}")


    # Create curriculum
    today = date.today()

    curriculum = {
        "version" : 1,
        "date" : today.strftime("%Y-%m-%d"),
        "semesters" : []
    }

    curriculum["semesters"] = get_semesters(soup, get_exam)

    print(f"Finished reading curriculum from {url}")
    return curriculum


def save_to_json(curriculum, save_file):
    with open(save_file, "w", encoding="utf8") as f:
        json.dump(curriculum, f)


def load_from_json(save_file):
    with open(save_file, "r", encoding="utf8") as f:
        curriculum = json.load(f)

    return curriculum

# %%
