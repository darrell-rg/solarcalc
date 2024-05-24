<script lang="ts">
	import { onMount, onDestroy, setContext, createEventDispatcher, tick } from 'svelte';
	import L from 'leaflet';
	import 'leaflet/dist/leaflet.css';
	import 'leaflet-textpath';
	import { isoTherms, isoThermsC } from './isoTherms';

	export let bounds: L.LatLngBoundsExpression | undefined = undefined;
	export let view: L.LatLngExpression | undefined = undefined;
	export let zoom: number | undefined = undefined;

	const dispatch = createEventDispatcher();

	let map: L.Map | undefined;
	let mapElement: HTMLElement;
	let showGroundTemps = true;

	function fToC(fahrenheit: number) {
		let celsius = ((fahrenheit - 32.0) * 5.0) / 9.0;

		return '' + Math.floor(celsius) + '°                                ';
	}

	function formatC(celsius: number) {
		return '' + Math.floor(celsius) + '°                            ';
	}

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

		var myStyle1 = {
			color: 'gray',
			weight: 1,
			opacity: 0.65
		};

		var myStyle2 = {
			color: 'red',
			weight: 1,
			opacity: 0.65
		};

		if (showGroundTemps) {
			// L.geoJSON(isoTherms.features, {
			// 	style: myStyle1,
			// 	onEachFeature: function (feature, layer) {
			// 		layer.setText(fToC(feature.properties.Temperature), { repeat: true });
			// 	}
			// }).addTo(map);

			L.geoJSON(isoThermsC.features, {
				style: myStyle2,
				onEachFeature: function (feature, layer) {
					layer.setText(formatC(feature.properties.tempC), { repeat: true });
				}
			}).addTo(map);

			// var imageUrl = 'groundTempMapClearWithNumbers.png';
			// var altText =
			// 	'Average shallow ground water Temperatures in the United States by Collins, 1925';
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
