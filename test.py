# %%
from curriculum_scraper_v1 import get_curriculum, get_courses, save_to_json, load_from_json

# %load_ext autoreload
# %autoreload 2

# %% Scrape
curriculum = get_curriculum("https://studieinfo.liu.se/en/program/6CDDD/4617#curriculum", get_exam=False)
# curriculum_sv = get_curriculum("https://studieinfo.liu.se/program/6CDDD/4617#curriculum", get_exam=False)
save_to_json(curriculum, "curriculum_v1.json")

# %% Load
curriculum = load_from_json("curriculum_v1.json")

# %%
all_courses = get_courses(curriculum, semesters=[7, 8, 9], specializations=["DAIM", "DAUT"])

save_to_json(all_courses, "my_course_list.json")

# %%