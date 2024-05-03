<script>
	export let val;
	export let label;
	export let units;
	export let min = 0;
	export let max = 100;
	export let step = 'any';
	export let readonly = false;
	// export let type = "number";
</script>

<label>
	<input
		{readonly}
		type="text"
		inputmode="numeric"
		bind:value={val}
		{min}
		{max}
		{step}
		style="width: 5em;"
	/>
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
	}
</style>
