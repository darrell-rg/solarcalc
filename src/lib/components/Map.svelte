<script>
	import { MapLibre, Marker } from 'svelte-maplibre';
	import { lat, lng } from '$lib/components/stores.js';

	let boundPos = { lng: $lng, lat: $lat };

	function updateMapPos(event) {
		// console.log(event);
	}

	function updatePos(event) {
		lng.set(boundPos.lng);
		lat.set(boundPos.lat);
	}
</script>

Move the solar panel icon to set location.
<MapLibre
	center={[boundPos.lng, boundPos.lat]}
	zoom={2}
	class="map"
	on:moveend={updateMapPos}
	style="https://basemaps.cartocdn.com/gl/positron-gl-style/style.json"
>
	<Marker bind:lngLat={boundPos} draggable on:dragend={updatePos} class="solarMarker">
		<img alt="PanelLocation" src="solarIcon.png" class="solarMarker" />
	</Marker>
</MapLibre>

<style>
	:global(.map) {
		height: 300px;
	}
	.solarMarker {
		height: 30px;
	}
</style>
