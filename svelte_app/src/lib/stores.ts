
import { writable, type Writable } from "svelte/store";
import type { ApiCourse } from "../routes/+page";

export const allCourses: Writable<ApiCourse[]> = writable([]);
export const selectedCourses: Writable<ApiCourse[]> = writable([]);