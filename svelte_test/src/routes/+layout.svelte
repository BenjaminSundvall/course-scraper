<script lang="ts">
    import { page } from "$app/stores";
    import { caughtMonsters } from "$lib/stores";
</script>

<div class="navbar">
    <a href="/" class:active={$page.url.pathname == "/"}>Home</a>
    <a href="/my-monsters" class:active={$page.url.pathname == "/my-monsters"}>
        My Monsters ({$caughtMonsters.length})
    </a>
</div>

<div class="container">
    <slot />
</div>


<style>
    .navbar {
        display: flex;
        justify-content: space-between;
        background-color: #333;
        color: #fff;
        padding: 10px;
    }

    .navbar a {
        color: #fff;
        text-decoration: none;
    }

    .navbar a:hover {
        color: #ccc;
    }

    .navbar a.active {
        border: 1px solid #ccc;
        border-radius: 4px;
    }

    :global(body) {
        margin: 0px;
    }

    .container {
        max-width: 90%;
        margin: auto;
        width: 1200px;
    }
</style>