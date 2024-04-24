# %%
from supabase import create_client, Client

url = "https://xvfdqonvnrxgrkqlcriw.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inh2ZmRxb252bnJ4Z3JrcWxjcml3Iiwicm9sZSI6ImFub24iLCJpYXQiOjE2OTU3OTkxMDUsImV4cCI6MjAxMTM3NTEwNX0.NhtoK8tEeorPphhyQxVAPZVYNsmSBFH3M73L8rMdFFs"

supabase = create_client(url, key)

# %%
# response = supabase.table("courses").select("courses(*)").eq('courses.code', "TDDC17").execute()
response = supabase.table("specializations").select("*").execute()

print(response.data[0])

#%%
data, count = supabase.table('courses') \
  .insert({"code": "ABCD12", "name": "Test", "credits": 42, "level": "A2X", "tt_module": 2, "url": "my.url"}) \
  .execute()

#%%


# %%
courses = [
    {
        "code" : "TDDC17",
        "name" : "Artificial Intelligence",
        "credits" : 6
    },
    {
        "code" : "TSBB08",
        "name" : "Multidimensional Signal Analysis",
        "credits" : 6
    },
    {
        "code" : "TSFS12",
        "name" : "Autonomous Vehicles - Planning, Control, and Learning Systems",
        "credits" : 6
    },
]

specializations = [
    {
        "code" : "DAIM",
        "name" : "AI and Machine Learning"
    },
    {
        "code" : "DAUT",
        "name" : "Autonomous Systems"
    },
]

in_spec = [
    {
        "crs_code" : "TDDC17",
        "spec_code" : "DAIM",
        "ecv" : "C"
    },
    {
        "crs_code" : "TDDC17",
        "spec_code" : "DAUT",
        "ecv" : "C"
    },
    {
        "crs_code" : "TSBB08",
        "spec_code" : "DAUT",
        "ecv" : "C"
    },
    {
        "crs_code" : "TSFS12",
        "spec_code" : "DAUT",
        "ecv" : "C"
    },
]

periods = [
    {
        "code" : "HT1 2023",
        "period" : 1,
        "semester" : 0, # 0: fall, 1: spring
        "year" : 2023
    },
    {
        "code" : "HT2 2023",
        "period" : 2,
        "semester" : 0, # 0: fall, 1: spring
        "year" : 2023
    },
    {
        "code" : "VT1 2024",
        "period" : 1,
        "semester" : 1, # 0: fall, 1: spring
        "year" : 2023
    },
    {
        "code" : "VT2 2024",
        "period" : 2,
        "semester" : 1, # 0: fall, 1: spring
        "year" : 2024
    },
]

in_prd = [
    {
        "crs_code" : "TDDC17",
        "prd_code" : "HT1 2023"
    },
    {
        "crs_code" : "TSBB08",
        "prd_code" : "HT1 2023"
    },
    {
        "crs_code" : "TSFS12",
        "prd_code" : "HT1 2023"
    },
]

# %%
try:
    # data, count = supabase.table('specializations').insert(courses[0]).execute()
    data, count = supabase.table('specializations').insert({"code" : "ABCD12", "name": "Test Course", "credits": "42"}).execute()
    print(data)
    print(count)
except Exception as e:
    print('ded')
    print(e)

# %%
try:
    for spec in specializations:
        data, count = supabase.table('specializations').insert(spec).execute()
        print(data)
        print(count)
except Exception as e:
    print('ded')
    print(e)

# %%
