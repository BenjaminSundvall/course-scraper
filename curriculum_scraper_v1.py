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


def get_courses(prd_key, get_exam):
    courses = {}

    for crs_soup in prd_key.select("tr.main-row"):
        crs_code = crs_soup.select("td")[0].text.strip()
        crs_name = crs_soup.select("td")[1].text.strip()
        crs_credits = crs_soup.select("td")[2].text.strip()
        crs_level = crs_soup.select("td")[3].text.strip()
        crs_tt_module = crs_soup.select("td")[4].text.strip()
        crs_ecv = crs_soup.select("td")[5].text.strip()

        href = crs_soup.select("a")[0].get("href")
        crs_url = "https://studieinfo.liu.se/" + href

        crs_examinations = {}
        if get_exam:
            crs_examinations = get_examinations(crs_url)

        courses[crs_code] = {"name" : crs_name,
                             "credits" : crs_credits,
                             "level" : crs_level,
                             "block" : crs_tt_module,
                             "ecv" : crs_ecv,
                             "url" : crs_url,
                             "examinations" : crs_examinations}

    return(courses)


def get_periods(spec_soup, get_exam):
    periods = {}

    for prd_soup in spec_soup.select("tbody.period"):
        period_key = prd_soup.select("th")[0].text.strip()

        periods[period_key] = get_courses(prd_soup, get_exam)

    return periods


def get_specializations(sem_soup, get_exam):
    specializations = {}

    for spec_soup in sem_soup.select("div.specialization"):
        specialization_key = spec_soup.get("data-specialization").strip()

        if not specialization_key:
            specialization_key = "[No Specialization]"

        specializations[specialization_key] = get_periods(spec_soup, get_exam)

    return specializations


def get_semesters(soup, get_exam):
    semesters = {}

    for sem_soup in soup.select("section.accordion.semester"):
        semester_title = sem_soup.select("h3")[0].text.strip()

        semesters[semester_title] = get_specializations(sem_soup, get_exam)

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
        "semesters" : {}
    }

    curriculum["semesters"] = get_semesters(soup, get_exam)

    print(f"Finished reading curriculum from {url}")
    return curriculum


def get_course_list(curriculum, semesters=[], specializations=[], periods=[], blocks=[], examinations=[]):
    # TODO: Change to english?
    courses = {"HT1" : {},
               "HT2" : {},
               "VT1" : {},
               "VT2" : {}}

    sem_dict = curriculum['semesters']
    for sem_idx, sem_key in enumerate(sem_dict):
        if semesters and sem_idx+1 not in semesters:
            continue
        print("Semester:", sem_key)
        specs_dict = sem_dict[sem_key]

        for spec_key in specs_dict:
            if specializations and spec_key not in specializations:
                continue
            print("  Specialization:", spec_key)
            spec_dict = specs_dict[spec_key]

            for prd_key in spec_dict:
                period_number = int(prd_key[-1])
                if periods and period_number not in periods:
                    continue
                print("    Period:", prd_key)
                crs_dict = spec_dict[prd_key]

                for crs_key in crs_dict:
                    if blocks and crs_dict[crs_key]["block"] not in blocks:
                        continue

                    # TODO: Check examination types
                    given = f"HT{period_number}" if sem_idx % 2 == 0 else f"VT{period_number}"
                    courses[given][crs_key] = crs_dict[crs_key]

    return courses


def save_to_json(curriculum, save_file):
    with open(save_file, "w", encoding="utf8") as f:
        json.dump(curriculum, f)


def load_from_json(save_file):
    with open(save_file, "r", encoding="utf8") as f:
        curriculum = json.load(f)

    return curriculum

# %%

curriculum = get_curriculum("https://studieinfo.liu.se/en/program/6CDDD/4617#curriculum", get_exam=False)
# curriculum_sv = get_curriculum("https://studieinfo.liu.se/program/6CDDD/4617#curriculum", get_exam=False)
save_to_json(curriculum, "curriculum_v1.json")
# %%
