
import { writable, type Writable } from "svelte/store";
import type { Course } from "../routes/curriculumTypes";

export const selectedCourses: Writable<Course[]> = writable([]);