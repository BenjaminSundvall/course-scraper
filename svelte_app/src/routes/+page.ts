import type { PageLoad } from "./$types"

export type ApiExamination = {
    code: string,
    name: string,
    scope: string,
    scale: string,
}

export type ApiCourse = {
    code: string,
    name: string,
    credits: string,
    level: string,
    tt_module: string,
    url: string,
    examinations: ApiExamination[],
    semester_titles: string[],
    specialization_titles: string[],
    period_titles: string[],
}

export type ApiSpecialization = {
    title: string,
    elective_courses: ApiCourse[],
    compulsory_courses: ApiCourse[],
    voluntary_courses: ApiCourse[],
}

export type ApiCourseData = {
    version: number,
    date: string,
    url: string,
    language: string,
    program: string,
    courses: ApiCourse[],
    specializations: ApiSpecialization[],
    specialization_titles: string[]
    semester_titles: string[]
}

export const load = (async ({fetch}) => {
    const courseDataURL = "https://raw.githubusercontent.com/BenjaminSundvall/course-scraper/main/course_data_v1.json"
    console.log(`Loading course data from ${courseDataURL}`)
    const response = await fetch(courseDataURL)
    const json = await response.json()
    const apiCourseData: ApiCourseData = json
    console.log("Finished loading course data.")

    return {
        courseData: apiCourseData
    }
}) satisfies PageLoad
