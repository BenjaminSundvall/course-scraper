  <script>
    export let data;
  </script>

  <ul>
    {#each data.courses as course}
      <li>{course.code}</li>
      <li>{course.name}</li>
      <li>{course.credits}</li>
    {/each}
  </ul>