<script lang="ts">
    import type { Course } from "./curriculumTypes";

    import { selectedCourses } from "$lib/stores"

    export let course: Course;

    let isSelected = false;

    $: isSelected = $selectedCourses.filter(selectedCourse => selectedCourse.name === course.name).length > 0

    const toggleCourse = () => {
        if(isSelected) {
            $selectedCourses = $selectedCourses.filter((selectedCourse) => selectedCourse.name != course.name)
            console.log(`Deselected course ${course.code}`)
            console.log($selectedCourses)
        } else {
            $selectedCourses = [...$selectedCourses, course]
            console.log(`Selected course ${course.code}`)
            console.log($selectedCourses)
        }
    }
</script>

<div class=course>
    <div class="course-info">
        {course.code}, {course.credits} hp, {course.level}, block {course.tt_module}, {course.ecv}
    </div>
    <a href={course.url}>{course.name}</a>
    <button class="select-button" class:active={isSelected} on:click={toggleCourse}>
        {#if isSelected}
            Remove
        {:else}
            Add
        {/if}
    </button>
</div>

<style>
.course {
    width: 300px;
    margin: 10px;
    padding: 10px;
    position: relative;
    background-color: #eee;
    border-radius: 5px;
    overflow: hidden;
}

.course:hover {
    background-color: #ddd;
}

.course-info {
    font-size: 0.8em;
    color: #333;
}

.select-button {
    background-color: #0a0;
    color: #eee;
    border: none;
    border-radius: 5px;
    height: 30px;
    float: right;
    padding: 5px 10px;
}

.select-button.active {
    background-color: #c00;
}
</style>