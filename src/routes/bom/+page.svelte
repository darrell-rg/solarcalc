<script>
	import { onMount } from 'svelte';
	import { read, utils, writeFileXLSX } from 'xlsx';



	let html = "";
	let tbl;

	/* Fetch and update the state once */
	onMount(async() => {
	const f = await (await fetch("SolarHotWaterBOM.xlsx")).arrayBuffer();
	const wb = read(f); // parse the array buffer
	const ws = wb.Sheets[wb.SheetNames[0]]; // get the first worksheet
	html = utils.sheet_to_html(ws); // generate HTML and update state
	});

	/* get state data and export to XLSX */
	function exportFile() {
	const elt = tbl.getElementsByTagName("TABLE")[0];
	const wb = utils.table_to_book(elt);
	writeFileXLSX(wb, "SolarHotWaterBOM.xlsx");
	}

</script>

<svelte:head>
	<title>About</title>
	<meta name="description" content="About this app" />
</svelte:head>

<div class="text-column">

	<h1>Bill Of Materials Spreadsheet</h1>

	<p>
		You can use this sheet to help figure out what you need to buy and how much everything will cost.
	</p>

	<button on:click={exportFile}>Export XLSX</button>
	<div bind:this={tbl}>{@html html}</div>
</div>
