<script lang="ts">

    import type { PageData } from "./$types";
    import { selectedCourses } from "$lib/stores";
    import CourseComponent from "./CourseComponent.svelte";
    import type { ApiCourse, ApiCourseData } from "./+page";

    export let data: PageData;

    let courseData: ApiCourseData = data.courseData;
    let courses: ApiCourse[] = courseData.courses;
    let semesterTitles: string[] = courseData.semester_titles;
    let specializationTitles: string[] = courseData.specialization_titles;

    let form = {
        searchString: "",
        semester: "none",
        specialization: "none",
    }

    $: selectedSemesters = [];
    $: selectedSpecializations = [];

    // let semester: Semester = curriculum.semesters[6];
    // let specialization: Specialization = semester.specializations[2];
    // let period: Period = specialization.periods[0];

    // let courses: Course[] = period.courses;

    // $: specCourses = curriculum.filter

    // let filteredCourses: Course[] = [];

    // $: curriculum.semesters.forEach(semester => {
    //     semester.specializations.forEach(specialization => {
    //         specialization.periods.forEach(period => {
    //             period.courses.forEach(course => {
    //                 filteredCourses = courses.filter((course) => {
    //                     let codeIncluded = course.code.toLowerCase().includes(form.searchString.toLowerCase());
    //                     let nameIncluded = course.name.toLowerCase().includes(form.searchString.toLowerCase());
    //                     return codeIncluded || nameIncluded;
    //                 });
    //             });
    //         });
    //     });
    // });


    $: filteredCourses = courses.filter((course) => {
        let codeIncluded = course.code.toLowerCase().includes(form.searchString.toLowerCase());
        let nameIncluded = course.name.toLowerCase().includes(form.searchString.toLowerCase());
        let correctSemester = (form.semester == "none") || course.semester_titles.includes(form.semester);
        let correctSpecialization = (form.specialization == "none") || course.specialization_titles.includes(form.specialization);
        return (codeIncluded || nameIncluded) && correctSemester && correctSpecialization;
    });

</script>

<div class="selected-courses">
    <h1>My Courses</h1>
    {#each $selectedCourses as course (course.code)}
        <CourseComponent course={course} />
    {/each}
</div>


<div class="course-list">
    <h1>All Courses</h1>

    <form class="search-form" on:submit>
        <input class="search-field" type="text" bind:value={form.searchString} placeholder="Course name or code" />

        <select bind:value={form.semester}>
            <option value="none">All Semesters</option>
            {#each semesterTitles as semesterTitle (semesterTitle)}
                <option value={semesterTitle}>{semesterTitle}</option>
            {/each}
        </select>

        <select bind:value={form.specialization}>
            <option value="none">All Specializations</option>
            {#each specializationTitles as specializationTitle (specializationTitle)}
                <option value={specializationTitle}>{specializationTitle}</option>
            {/each}
        </select>

        <!-- <select bind:value={form.specialization}>
            <option value="none">No specialization</option>
            <option value="DAIM">AI och maskininlärning</option>
            <option value="DAUT">Autonoma system</option>
        </select> -->

    </form>

    <p>{form.semester}</p>

    <p>{form.specialization}</p>

    <h1>Filtered Courses</h1>
    {#each filteredCourses as course (course.code)}
        <CourseComponent course={course} />
    {/each}

    <h1>All Courses:</h1>
    {#each courses as course (course.code)}
        <CourseComponent course={course} />
    {/each}

    <!-- {#each curriculum.semesters as semester (semester.title)}
        <h1>{semester.title}</h1>
        {#each semester.specializations as specialization (specialization.title)}
            <h2>{specialization.title}</h2>
            {#each specialization.periods as period (period.title)}
                <h3>{period.title}</h3>
                {#each period.courses as course (course.code)}
                    {#if course.code.toLowerCase().includes(form.searchString.toLowerCase())}
                        <CourseComponent course={course} />
                    {/if}
                {/each}
            {/each}
        {/each}
    {/each} -->

    <!-- {#each filteredCourses as course (course.code)}
        <CourseComponent course={course} />
    {/each} -->
</div>