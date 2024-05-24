<script lang="ts">
	export let val: number;
	export let label: string;
	export let units: string;
	export let min: any = 0;
	export let max: any = 100;
	export let step: any = 1;
	export let readonly: boolean = false;
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
	input {
		border: 1px solid black;
		box-shadow: none;
		margin: 1px;
		background-color: white;
	}
	input:read-only {
		border: 2px solid white;
		background-color: whitesmoke;
	}
</style>
