<script>
	import { onMount } from 'svelte';
	import { read, utils, writeFileXLSX } from 'xlsx';
	import { _bomData } from './+page';
	import { round, tokWh, clamp } from '$lib/components/util';

	let ebayAffiliateCode = '';

	function getSourceUrl(itm) {
		let url = 'https://www.ebay.com/itm/' + itm.ebayid + ebayAffiliateCode;
		return url;
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
	function exportFile() {
		// const elt = tbl.getElementsByTagName('TABLE')[0];
		const wb = utils.table_to_book(tbl);
		writeFileXLSX(wb, 'SolarHotWaterBOM.xlsx');
	}

	// const ws = _bomSheet; // get the first worksheet
	// html = utils.sheet_to_html(ws); // generate HTML and update state

	let data = _bomData.map((r) => {
		return {
			PN: '',
			Desc: r.Desc,
			Qty: r.Qty,
			Price: r.Price,
			Source: '',
			ebayid: r.ebayid,
			Total: r.Price * r.Qty
		};
	});

	$: totalPrice = data.reduce((accumulator, currentValue) => accumulator + currentValue.Total, 0);
	// console.log(data);
</script>

<svelte:head>
	<title>About</title>
	<meta name="description" content="About this app" />
</svelte:head>

<div class="text-column">
	<h1>Bill Of Materials Spreadsheet</h1>

	<p>
		You can use this sheet to help figure out what you need to buy and how much everything will
		cost.
	</p>
	<p>I have filled it in with the approximate costs from my project in the year 2020.</p>
	<table class="bomTable" id="bomTable" bind:this={tbl}>
		<tr>
			<th>PN</th>
			<th>DESC</th>
			<th style="min-width:5em">Qty Req</th>
			<th style="min-width:5em">Price EA</th>
			<th style="min-width:5em">Total</th>
			<th style="min-width:15em">Source</th>
		</tr>
		{#each data as r}
			<tr>
				<td>{r.PN}</td>
				<td>{r.Desc}</td>
				<td>{r.Qty}</td>
				<td>{r.Price}</td>
				<td>{round(r.Total)}</td>
				<td>
					{#if r.ebayid}
						<a href={getSourceUrl(r)}>eBay</a>
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

	<p>You can support this website by using the links in the "Source" column to purchase parts.</p>
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
