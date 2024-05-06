<script>
	/**
	 * @type {any}
	 */
	 export let val;
	export let label;
	export let units;
    /**
	 * @type {number}
	 */
	export let min = 0;
        /**
	 * @type {number}
	 */
	export let max = 100;
	export let step = 1;
	export let readonly = false;
	// export let type = "number";
</script>

<label>
	<input
		{readonly}
		type="number"
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
