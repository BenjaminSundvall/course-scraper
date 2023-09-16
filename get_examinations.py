# %%
from load_curriculum import load_from_json, get_examinations
import json
from bs4 import BeautifulSoup
import requests
from datetime import date

# %%
curriculum = load_from_json("curriculum.json")

semester = 0
specialization = 0
period = 0
course_nr = 0

course = curriculum["semesters"][semester]["specializations"][specialization]["periods"][period]["courses"][course_nr]

url = course["url"]
print(url)

get_examinations(url)
