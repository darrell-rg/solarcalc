<script>
	import { onMount } from 'svelte';
	import Row from './Row.svelte';
	import { headers,bomData, makeBomRow } from './bom';

	let cols = 7;
	let rows = 25;
	let data = {};

	export let tableIdentifier;

	const handleChangedCell = (col, row, value) => {
		if (!data[row]) data[row] = {};
		data[row][col] = value;

		if (window && window.localStorage) {
			window.localStorage.setItem(tableIdentifier, JSON.stringify(data));
		}
	};

	onMount(() => {
		if (typeof window !== 'undefined') {
			let localStorageData = window.localStorage.getItem(tableIdentifier);
			localStorageData = null;
			if (localStorageData) {
				data = JSON.parse(localStorageData);
				console.log('data', data);
			} else {
				data[1] = headers;
				for (let i = 0; i < bomData.length ; i++) {
  					data[i+2]=makeBomRow(bomData[i]);
				} 
			}
		}
	});
</script>

{#each Array(rows) as _, row}
	<Row {row} cols={cols + 1} rowData={data[row] || {}} {handleChangedCell} />
{/each}
