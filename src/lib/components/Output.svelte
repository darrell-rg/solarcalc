<script lang="ts">
	export let val: any;
	export let label: string;
	export let units: string;
	export let readonly = true;
</script>

<label>
	<input {readonly} bind:value={val} />
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
