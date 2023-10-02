import { supabase } from "$lib/supabaseClient";

export async function load() {
    const { data } = await supabase.from("courses").select();

    console.log("Course codes", await supabase.from("courses").select("code"));

    return {
        courses: data ?? [],
    };
}