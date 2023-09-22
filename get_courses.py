# %% Imports

import requests
from bs4 import BeautifulSoup
from datetime import date
import json

from curriculum_scraper_v0 import get_curriculum, save_to_json, load_from_json

# %% Scrape
curriculum = get_curriculum("https://studieinfo.liu.se/en/program/6CDDD/4617#curriculum", get_exam=True)
save_to_json(curriculum, "curriculum_2023_09_22.json")

# %%
curriculum = load_from_json("curriculum_2023_09_19.json")
print(curriculum)

# %%
def get_full_course_list(curriculum):
    courses = []

    for semster in curriculum['semesters']:
        for specialization in semster['specializations']:
            for period in specialization['periods']:
                for course in period['courses']:
                    if course in courses:
                        continue
                    courses.append(course)
    return courses

# %%
course_list = get_full_course_list(curriculum)
ten_count = 0

for course in course_list:
    for examination in course['examinations']:
        if examination['code'][:3] == "TEN":
            ten_count += 1
            break


print("Antal kurser med tenta:", ten_count)
# %%
