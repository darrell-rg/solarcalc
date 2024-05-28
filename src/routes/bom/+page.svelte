<script lang="ts">
	import { onMount } from 'svelte';
	import { bomData, headers, makeBomRow, makeEmptyRow } from '$lib/components/bom.js';
	import { round, tokWh, clamp } from '$lib/components/util';
	import Table from '$lib/components/Table.svelte';
	import { defaultGridConfig } from '$lib/components/bom.js';
	import { pv } from '$lib/components/stores.ts';

	let tbl: any = {};
	/* get state data and export to XLSX */
	async function exportFile() {
		// const elt = tbl.getElementsByTagName('TABLE')[0];
		const xlsx = (await import('xlsx')).default;
		const wb = xlsx.utils.table_to_book(tbl);
		xlsx.writeFileXLSX(wb, 'SolarHotWaterBOM.xlsx');
	}

	// const ws = _bomSheet; // get the first worksheet
	// html = utils.sheet_to_html(ws); // generate HTML and update state

	const tableIdentifier = 'bom';
	const maxRows = 30;
	let config = defaultGridConfig(7, maxRows);
	config.columnSetting[1].width = 200;
	config.columnSetting[2].width = 300;
	config.columnSetting[3].width = 60;
	config.columnSetting[4].width = 60;
	config.columnSetting[5].width = 60;
	config.columnSetting[6].width = 300;
	//	The array of cells needs to be in sync with the rows/columns configuration
	let data: any = {};
	let uid = 'bom';
	let totalPrice = 0;
	let currCell;

	function isValidNumber(str) {
		return !isNaN(parseFloat(str)) && isFinite(str);
	}

	function calcTotals() {
		totalPrice = 0;
		for (let i = 1; i < maxRows; i++) {
			if (data[i] && data[i][3] && data[i][4]) {
				if (isValidNumber(data[i][3].value) && isValidNumber(data[i][4].value)) {
					data[i][5].result = data[i][4].value * data[i][3].value;
					data[i][5].value = '=D' + (i + 1) + '*E' + (i + 1);
					data[i][5].display = round(data[i][5].result);
					totalPrice += data[i][5].result;
				} else {
					data[i][5].result = 0;
					data[i][5].value = '=D' + (i + 1) + '*E' + (i + 1);
					data[i][5].display = '';
				}
			}

			if (data[i] && data[i][1]) {
				let re = /^https:\/\/(www\.)?([^.]+).*$/;
				let site = re.exec(data[i][1].value);
				if (site) {
					let r = data[i][1].value;
					data[i][1].display = '<a target="_blank" href="' + r + '">' + site[2] + '</a>';
				}
			}
		}
		$pv.bomTotal = totalPrice;
	}

	function startEdit(e) {
		// console.log('startEdit', e.detail);
	}
	function onEdit(e) {
		// console.log('onEdit', e.detail);
		calcTotals();
		saveData();
	}
	function saveData() {
		window.localStorage.setItem(uid, JSON.stringify(data));
	}
	function onSelectionChange(e) {
		// console.log('onSelectionChange', e.detail);
		currCell = e.detail;
	}

	onMount(() => {
		if (typeof window !== 'undefined') {
			let localStorageData = window.localStorage.getItem(tableIdentifier);
			// localStorageData = null;
			if (localStorageData) {
				data = JSON.parse(localStorageData);
				// console.log('data', data);
			} else {
				data[0] = headers;
				for (let i = 0; i < bomData.length; i++) {
					data[i + 1] = makeBomRow(bomData[i]);
				}
				for (let i = bomData.length; i < maxRows; i++) {
					data[i + 1] = makeEmptyRow();
				}
			}
		}
		calcTotals();
		saveData();
	});
</script>

<svelte:head>
	<title>PVH2O BOM</title>
	<meta name="description" content="Bill Of Materials" />
</svelte:head>

<div class="text-column">
	<h1>Bill Of Materials Spreadsheet</h1>
	<center><br />Estimated Total System Cost: ${round(totalPrice)}</center>

	<!-- <button on:click={exportFile}>Export XLSX</button> -->

	<!-- <p>
		This website may receive a small commission if you use the links in the "Source" column to
		purchase parts.
	</p> -->

	<Table
		{data}
		{config}
		{uid}
		on:startedit={startEdit}
		on:endedit={onEdit}
		on:selChange={onSelectionChange}
	/>

	<p>
		You can use this sheet to estimate your costs. Double click to edit cells, copy with ctrl+c,
		paste with ctrl+v. Your changes will be saved in your browser's local storage.
	</p>
</div>

<style>
	.bomTable {
		border-collapse: collapse;
		border: 1px solid #000;
		text-align: left;
		padding: 8 px;
	}
	tr {
		border-bottom: 1px solid #ddd;
	}

	th {
		border-bottom: 1px solid #000;
		min-width: 10em;
	}
	tr:nth-child(even) {
		background-color: #d6eeee;
	}
</style>
