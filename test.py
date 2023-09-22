# %%
from curriculum_scraper_v1 import get_curriculum, save_to_json, load_from_json

# %% Scrape
curriculum = get_curriculum("https://studieinfo.liu.se/en/program/6CDDD/4617#curriculum", get_exam=True)
save_to_json(curriculum, "curriculum_v1.json")


# %%
print(curriculum['semesters']['Semester 1 Autumn 2020']['[No Specialization]']['Period 0']['TATA65'])


all_courses = {}
spec_courses = {}
specializations = curriculum['semesters']['Semester 7 Autumn 2023']
for spc_key in specializations:
    specialization = specializations[spc_key]
    for prd_key in specialization:
        period = specialization[prd_key]
        for crs_key in period:
            course = period[crs_key]
            if spc_key == "[No Specialization]":
                all_courses[crs_key] = course
            else:
                spec_courses[crs_key] = course

print("All:", len(all_courses))
print("Spec:", len(spec_courses))

print("\nAll, but not spec:")
for course in all_courses:
    if course not in spec_courses:
        print(course)

print("\nSpec, but not all:")
for course in spec_courses:
    if course not in all_courses:
        print(course)
# %%
