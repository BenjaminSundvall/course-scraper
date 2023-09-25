import type { PageLoad } from "./$types"
import type { ApiCurriculum } from "./curriculumTypes"
// import type { Course } from "./courses"

// export type Curriculum = ApiCurriculum & {
//     semesterKeys: string[],
//     specializationKeys: string[],
// }

export const load = (async ({fetch}) => {
    const curriculumURL = "https://raw.githubusercontent.com/BenjaminSundvall/course-scraper/main/curriculum_v0.json"
    console.log(`Loading curriculum from ${curriculumURL}`)
    const response = await fetch(curriculumURL)
    const json = await response.json()
    const apiCurriculum: ApiCurriculum = json
    console.log("Finished loading curriculum.")

    // let semesterKeys: string[] = []
    // let specializationKeys: string[] = []

    // const curriculum: Curriculum = {
    //     version: apiCurriculum.version,
    //     date: apiCurriculum.date,
    //     semesters: apiCurriculum.semesters,
    //     semesterKeys,
    //     specializationKeys,
    // }

    // let curriculum = dummyCurriculum;
    return {
        // curriculum
        curriculum: apiCurriculum
    }
}) satisfies PageLoad

// export const load = (async) => {
//     let curriculum = dummyCurriculum;
//     return {
//         curriculum
//     };
// }