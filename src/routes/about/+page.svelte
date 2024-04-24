<script>
	import { Sheet, Toolbar } from 'svelte-sheets';

	let style = {
		// A1: 'background-color: red'
	};
	let mergeCells = {
		//A1: [5, 0] // 5 horizontally merged cell (colspan), 0 vertically merged cells (rowspan)
	};
	let columns = [{ width: '50px' }];
	let data = [
	['Part Number', 'Desc', 'Qty Req', 'Price', 'Total', 'Link'],
	['', 'Solar Panel', '4', '150', '=D2*C2']];
	let sheetNames;
	let sheets;
	let active;
</script>

<svelte:head>
	<title>About</title>
	<meta name="description" content="About this app" />
</svelte:head>

<div class="text-column">
	<h1>About this app</h1>

	<p>
		This is a <a href="https://kit.svelte.dev">SvelteKit</a> app. You can make your own by typing the
		following into your command line and following the prompts:
	</p>

	<pre>npm create svelte@latest</pre>

	<p>
		The page you're looking at is purely static HTML, with no client-side interactivity needed.
		Because of that, we don't need to load any JavaScript. Try viewing the page's source, or opening
		the devtools network panel and reloading.
	</p>

	<h1>Bill Of Materials Spreadsheet</h1>

	<!-- <Toolbar bind:sheetNames bind:sheets bind:active />  -->
	<Sheet {style} {mergeCells} {columns} {data} />
</div>
