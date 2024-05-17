<script lang="ts">
	import { onMount, onDestroy, setContext, createEventDispatcher, tick } from 'svelte';
	import L from 'leaflet';
	import 'leaflet/dist/leaflet.css';

	export let bounds: L.LatLngBoundsExpression | undefined = undefined;
	export let view: L.LatLngExpression | undefined = undefined;
	export let zoom: number | undefined = undefined;

	const dispatch = createEventDispatcher();

	let map: L.Map | undefined;
	let mapElement: HTMLElement;
	let showGroundTemps = false;

	onMount(() => {
		if (!bounds && (!view || !zoom)) {
			throw new Error('Must set either bounds, or view and zoom.');
		}

		map = L.map(mapElement)
			// example to expose map events to parent components:
			.on('zoom', (e) => dispatch('zoom', e))
			.on('popupopen', async (e) => {
				await tick();
				e.popup.update();
			});

		L.tileLayer('https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png', {
			attribution: `&copy;<a href="https://www.openstreetmap.org/copyright" target="_blank">OpenStreetMap</a>,&copy;<a href="https://carto.com/attributions" target="_blank">CARTO</a>`
		}).addTo(map);

		if (showGroundTemps) {
			var imageUrl = 'groundTempMapClearWithNumbers.png';
			var altText =
				'Average shallow ground water temperatures in the United States by Collins, 1925';

			var latLngBounds = L.latLngBounds([
				[50, -128.79],
				[26.12, -62.75]
			]);

			var imageOverlay = L.imageOverlay(imageUrl, latLngBounds, {
				opacity: 0.8,
				alt: altText,
				interactive: false
			}).addTo(map);
		}
		// console.log("map mounted")
	});

	onDestroy(() => {
		map?.remove();
		map = undefined;
	});

	setContext('map', {
		getMap: () => map
	});

	$: if (map) {
		if (bounds) {
			map.fitBounds(bounds);
		} else if (view && zoom) {
			map.setView(view, zoom);
		}
	}
</script>

<!-- w-full h-full -->
<div class="leafletDiv" bind:this={mapElement}>
	{#if map}
		<slot />
	{/if}
</div>

<style>
	.leafletDiv {
		height: 300px;
		/* width: 600px; */
	}
</style>
