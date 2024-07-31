<script lang="ts">

    
    import { onMount } from 'svelte';
    import { Calculator } from   '../lib/calculator'
    import { create_chart } from '../lib/charts'

    let result = new Calculator('asdf');
    onMount(() => {
        create_chart();
    });
    
</script>

<h1>Dave Ramsey Cool Sciencey</h1>
<p>This page is intending to create a financial calculator based on Dave's good ole advice.</p>
{result.get_user()}
{result.my_func(5)}
<svg></svg>

<style>
    svg {
        width: 100%;
        height: 500px;
    }
</style>
