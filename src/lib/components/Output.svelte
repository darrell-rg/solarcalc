<script>
	export let val;
	export let label;
	export let units;
	export let min = 0;
	export let max = 1000;
	export let readonly = true;
</script>

<label>
	<input {readonly} bind:value={val} {min} {max} />
	{#if units}
		({units})
	{/if}

	{label}
</label>
<br />

<style>
	input:read-only {
		border: 2px solid white;
		box-shadow: none;
		background-color: whitesmoke;
		width: 5em;
	}
</style>
