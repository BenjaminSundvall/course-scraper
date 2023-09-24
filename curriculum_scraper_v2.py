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


# def get_courses(period, get_exam):
#     courses = {}

#     for crs in period.select("tr.main-row"):
#         crs_code = crs.select("td")[0].text.strip()
#         crs_name = crs.select("td")[1].text.strip()
#         crs_credits = crs.select("td")[2].text.strip()
#         crs_level = crs.select("td")[3].text.strip()
#         crs_tt_module = crs.select("td")[4].text.strip()
#         crs_ecv = crs.select("td")[5].text.strip()

#         href = crs.select("a")[0].get("href")
#         crs_url = "https://studieinfo.liu.se/" + href

#         crs_examinations = {}
#         if get_exam:
#             crs_examinations = get_examinations(crs_url)

#         courses[crs_code] = {"name" : crs_name,
#                              "credits" : crs_credits,
#                              "level" : crs_level,
#                              "tt_module" : crs_tt_module,
#                              "ecv" : crs_ecv,
#                              "url" : crs_url,
#                              "examinations" : crs_examinations}

#     return(courses)


def add_courses(prd_soup, courses, get_exam):
    for crs in prd_soup.select("tr.main-row"):
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



# def get_periods(specialization, get_exam):
#     periods = {}

#     for i, prd in enumerate(specialization.select("tbody.period")):
#         period_title = f"Period {i}"

#         periods[period_title] = get_courses(prd, get_exam)

#     return periods


def add_periods(spec_soup, periods, get_exam):
    for i, prd_soup in enumerate(spec_soup.select("tbody.period")):
        period_key = f"Period {i}"

        # periods[period_key] = get_courses(prd_soup, get_exam)
        periods[period_key] = {}
        add_courses[prd_soup, periods[period_key], get_exam]


# def get_specializations(semester, get_exam):
#     specializations = {}

#     for spec in semester.select("div.specialization"):
#         try:
#             specialization_title = spec.select("caption > span")[0].text
#         except:
#             specialization_title = "[No Specialization]"

#         specializations[specialization_title] = get_periods(spec, get_exam)

#     return specializations


def add_specializations(sem_soup, specializations, get_exam):
    for spec_soup in sem_soup.select("div.specialization"):
        try:
            specialization_key = spec_soup.select("caption > span")[0].text
        except:
            specialization_key = "[No Specialization]"

        # specializations[specialization_key] = get_periods(spec, get_exam)
        specializations[specialization_key] = {}
        add_periods(spec_soup, specializations[specialization_key], get_exam)


# def get_semesters(soup, get_exam):
#     semesters = {}

#     for sem in soup.select("section.accordion.semester"):
#         semester_title = sem.select("h3")[0].text.strip()

#         semesters[semester_title] = get_specializations(sem, get_exam)

#     return semesters


def add_semesters(soup, semesters, get_exam):
    for sem_soup in soup.select("section.accordion.semester"):
        semester_key = sem_soup.select("h3")[0].text.strip()

        # semesters[semester_key] = get_specializations(sem_soup, get_exam)
        semesters[semester_key] = {}
        add_specializations(sem_soup, semesters[semester_key], get_exam)


def get_curriculum(url, get_exam):
    # Load page from url
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    status = page.status_code
    print(f"Status: {status}")


    # Create curriculum
    today = date.today()

    curriculum = {
        "version" : 2,
        "date" : today.strftime("%Y-%m-%d"),
        "semesters" : []
    }

    # curriculum["semesters"] = get_semesters(soup, get_exam)
    curriculum["semesters"] = {}
    add_semesters(soup, curriculum["semesters"], get_exam)

    print(f"Finished reading curriculum from {url}")
    return curriculum


"""
def get_curriculum(url, get_exam):
    # Load page from url
    page = requests.get(url)    # TODO: Add exception handling
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

    # Get courses

    semesters = {}

    for sem_soup in soup.select("section.accordion.semester"):
        sem_key = sem_soup.select("h3")[0].text.strip()

        # curriculum['semesters'][semester_key] = get_specializations(semester, get_exam)
        for spc_soup in sem_soup.select("div.specialization"):
            try:
                spc_key = spc_soup.select("caption > span")[0].text
            except:
                spc_key = "[No Specialization]"

            # curriculum['semesters'][sem_key][spc_key] = get_periods(specialization, get_exam)
            for period_idx, prd_soup in enumerate(spc_soup.select("tbody.period")):
                prd_title = f"Period {period_idx}"

                # curriculum['semesters'][sem_key][spc_key][prd_title] = get_courses(prd_soup, get_exam)
                for crs_soup in prd_soup.select("tr.main-row"):
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

                    curriculum['semesters'][sem_key][spc_key][prd_title][crs_code] = {"name" : crs_name,
                                        "credits" : crs_credits,
                                        "level" : crs_level,
                                        "tt_module" : crs_tt_module,
                                        "ecv" : crs_ecv,
                                        "url" : crs_url,
                                        "examinations" : crs_examinations}



    print(f"Finished reading curriculum from {url}")
    return curriculum
"""

def save_to_json(curriculum, save_file):
    with open(save_file, "w", encoding="utf8") as f:
        json.dump(curriculum, f)


def load_from_json(save_file):
    with open(save_file, "r", encoding="utf8") as f:
        curriculum = json.load(f)

    return curriculum

# %%
