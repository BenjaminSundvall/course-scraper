export type Examination = {
    code: string,
    name: string,
    scope: string,
    scale: string,
}

export type Course = {
  code: string,
  name: string,
  credits: string,
  level: string,
  tt_module: string,
  ecv: string,
  url: string,
  examinations: Examination[],
//   period: string,
}

export type ApiPeriod = {
    title: string,
    courses: Course[],
}

export type ApiSpecialization = {
    title: string,
    periods: ApiPeriod[],
}

export type ApiSemester = {
    title: string,
    specializations: ApiSpecialization[],
}

export type ApiCurriculum = {
    version: number,
    date: string,
    semesters: ApiSemester[],
}

export const dummyCourses: Course[] = [
  {
    code: "TDDC17",
    name: "Artificial Intelligence",
    credits: "6",
    level: "G2X",
    tt_module: "3",
    ecv: "C",
    url: "https://studieinfo.liu.se//en/kurs/TDDC17/ht-2023",
    examinations: [],
  },
  {
    code: "TSBB08",
    name: "Digital Image Processing",
    credits: "6",
    level: "A1X",
    tt_module: "4",
    ecv: "C",
    url: "https://studieinfo.liu.se//en/kurs/TSBB08/ht-2023",
    examinations: [],
  },
]

export const dummyPeriods: ApiPeriod[] = [
    {
        title: "Dummy Period",
        courses: dummyCourses,
    }
]

export const dummySpecializations: ApiSpecialization[] = [
    {
        title: "Dummy Specialization",
        periods: dummyPeriods,
    }
]

export const dummySemesters: ApiSemester[] = [
    {
        title: "Dummy Semester",
        specializations: dummySpecializations,
    }
]

export const dummyCurriculum: ApiCurriculum = {
    version: -1,
    date: "1337-42-42",
    semesters: dummySemesters,
}