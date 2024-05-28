<script>
	import { onMount } from 'svelte';
	import { bomData , headers, makeBomRow} from '$lib/components/bom.js';
	import { round, tokWh, clamp } from '$lib/components/util';
	import Table from '$lib/components/Table.svelte';
	
	import { defaultGridConfig} from '$lib/components/bom.js';
	
	

	function getSourceUrl(itm) {
		if (itm.link) return itm.link;

		let url = 'https://www.ebay.com/itm/' + itm.ebayid;
		return url;
	}

	function getSourceName(itm) {
		if (itm.link) {
			if (itm.link.includes('ebay')) return 'eBay';

			if (itm.link.includes('santansolar')) return 'SanTan Solar';
		}
		return 'link';
	}
	/* Fetch and update the state once */
	// onMount(async () => {
	// 	const f = await (await fetch('SolarHotWaterBOM.xlsx')).arrayBuffer();
	// 	const wb = read(f); // parse the array buffer
	// 	const data = utils.sheet_to_json(wb.Sheets[wb.SheetNames[0]]);
	// 	console.log(data);
	// 	const ws = wb.Sheets[wb.SheetNames[0]]; // get the first worksheet
	// 	html = utils.sheet_to_html(ws); // generate HTML and update state
	// });

	let tbl = {};

	/* get state data and export to XLSX */
	async function exportFile() {
		// const elt = tbl.getElementsByTagName('TABLE')[0];
		const xlsx = (await import('xlsx')).default;
		const wb = xlsx.utils.table_to_book(tbl);
		xlsx.writeFileXLSX(wb, 'SolarHotWaterBOM.xlsx');
	}

	// const ws = _bomSheet; // get the first worksheet
	// html = utils.sheet_to_html(ws); // generate HTML and update state

	let dataOld = bomData.map((r) => {
		return {
			PN: '',
			Desc: r.Desc,
			Qty: r.Qty,
			Price: r.Price,
			Source: '',
			ebayid: r.ebayid,
			link: r.link,
			Total: r.Price * r.Qty
		};
	});

	$: totalPrice = dataOld.reduce((accumulator, currentValue) => accumulator + currentValue.Total, 0);
	// console.log(data);
  
	const tableIdentifier = "bom";

	let config = JSON.parse(JSON.stringify(defaultGridConfig));

	//	The array of cells needs to be in sync with the rows/columns configuration
	let data = {};
	
	onMount(() => {
		if (typeof window !== 'undefined') {
			let localStorageData = window.localStorage.getItem(tableIdentifier);
			localStorageData = null;
			if (localStorageData) {
				data = JSON.parse(localStorageData);
				console.log('data', data);
			} else {
				data[0] = headers;
				for (let i = 0; i < bomData.length ; i++) {
  					data[i+1]=makeBomRow(bomData[i]);
				} 
			}
		}
	});

	
	
	let uid='Tbl-'+((Math.random()*999999999)|0);
	
	let currCell;
	
	function startEdit(e) {
		console.log('startEdit',e.detail);
	}
	function onEdit(e) {
		console.log('onEdit',e.detail);
	}
	function onSelectionChange(e) {
		console.log('onSelectionChange',e.detail);
		currCell=e.detail;
	}
</script>

<svelte:head>
	<title>PVH2O BOM</title>
	<meta name="description" content="Bill Of Materials" />
</svelte:head>

<div class="text-column">
	<h1>Bill Of Materials Spreadsheet</h1>

	<p>You can use this sheet to estimate your costs.</p>
	<table class="bomTable" id="bomTable" bind:this={tbl}>
		<tr>
			<th>PN</th>
			<th>DESC</th>
			<th style="min-width:5em">Qty Req</th>
			<th style="min-width:5em">Price EA</th>
			<th style="min-width:5em">Total</th>
			<th style="min-width:15em">Source</th>
		</tr>
		{#each dataOld as r}
			<tr>
				<td>{r.PN}</td>
				<td>{r.Desc}</td>
				<td>{r.Qty}</td>
				<td>{r.Price}</td>
				<td>{round(r.Total)}</td>
				<td>
					{#if r.link}
						<a target="_blank" href={getSourceUrl(r)}>{getSourceName(r)}</a>
					{/if}
				</td>
			</tr>
		{/each}

		<tfoot>
			<tr>
				<th scope="row" colspan="4">Total Cost</th>
				<th colspan="2">${round(totalPrice)}</th>
			</tr>
		</tfoot>
	</table>

	<!-- <button on:click={exportFile}>Export XLSX</button> -->

	<p>
		This website may receive a small commission if you use the links in the "Source" column to
		purchase parts.
	</p>

	<Table tableIdentifier="BOM" {data} {config} {uid} on:startedit={startEdit} on:endedit={onEdit} on:selChange={onSelectionChange}/>
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
