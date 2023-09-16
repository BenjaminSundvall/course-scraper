# %% Imports

import requests
from bs4 import BeautifulSoup
from datetime import date
import json

# %% Load the page
# page = requests.get("https://studieinfo.liu.se/program/6CDDD/4617#curriculum")
page = requests.get("https://studieinfo.liu.se/en/program/6CDDD/4617#curriculum")

soup = BeautifulSoup(page.content, 'html.parser')

status = page.status_code
print(status)

# %%
courses_file = open("course_list.txt", "w", encoding="utf8")

title = soup.title.text
header = soup.header.text
body = soup.body.text

first_h1 = soup.select('h1')[0].text

course_count = 0
# for elem in soup.select('section.accordion.semester.js-semester.show-focus.is-toggled'):
for i, elem in enumerate(soup.select('tr.main-row')):
    courses_file.write(f"Course number {i}:\n")
    # title = elem.select('td > a')[0].text.strip()
    # print('Title:', title)
    elem.get()
    for field in elem.select('td'):
        # print(e.text.strip())
        courses_file.write(field.text.strip() + "\n")
    course_count += 1

print(f"Done reading {course_count} courses!")


# %% Read AI/ML courses for semester 7
today = date.today()

curriculum = {
    "version" : 0,
    "date" : today.strftime("%Y-%m-%d"),
    "semesters" : []
}

# Get semesters
for sem in soup.select("section.accordion.semester"):
    semester_title = sem.select("h3")[0].text.strip()

    semester = {"title" : semester_title,
                "specializations" : []}

    # Get specializations
    for spec in sem.select("div.specialization"):
        try:
            specialization_title = spec.select("caption > span")[0].text
        except:
            specialization_title = "[No Specialization]"
        # print(specialization_title)

        specialization = {"title" : specialization_title,
                          "periods" : []}

        # Get periods
        for i, prd in enumerate(spec.select("tbody.period")):
            period_title = f"Period {i}"
            # print(f"  {period_title}")

            period = {"title" : period_title,
                      "courses" : []}

            # Get courses
            for crs in prd.select("tr.main-row"):
                crs_code = crs.select("td")[0].text.strip()
                crs_name = crs.select("td")[1].text.strip()
                crs_credits = crs.select("td")[2].text.strip()
                crs_level = crs.select("td")[3].text.strip()
                crs_tt_module = crs.select("td")[4].text.strip()
                crs_ecv = crs.select("td")[5].text.strip()

                # print(f"    {crs_code}")

                course = {"code" : crs_code,
                          "name" : crs_name,
                          "credits" : crs_credits,
                          "level" : crs_level,
                          "tt_module" : crs_tt_module,
                          "ecv" : crs_ecv,}

                period["courses"].append(course)

            specialization["periods"].append(period)

        semester["specializations"].append(specialization)

    curriculum["semesters"].append(semester)

print(curriculum)

with open("curriculum.json", "w", encoding="utf8") as f:
    json.dump(curriculum, f)
