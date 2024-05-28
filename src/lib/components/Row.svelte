<script>
	import Cell from './Cell.svelte';
	export let cols;
	export let row;
	export let rowData;
	export let handleChangedCell;
</script>

<div class="row">
	{#each Array(cols) as _, col}
		<Cell {row} {col} value={rowData[col] || ''} onChangedValue={handleChangedCell} />
	{/each}
</div>

<style>
	.row {
		display: block;
	}
</style>
