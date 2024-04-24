import { supabase } from "$lib/supabaseClient";

export async function load() {
    const { data: courseData }  = await supabase.from("courses").select();
    const { data: specializationData }  = await supabase.from("specializations").select();

    // console.log("Course codes", await supabase.from("courses").select("code"));
    // console.log("Specialization codes", await supabase.from("specializations").select("code"));

    console.table(courseData)
    console.table(specializationData)

    return {
        courses: courseData ?? [],
        specializations: specializationData ?? [],
    };
}