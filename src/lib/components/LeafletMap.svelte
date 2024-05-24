<script lang="ts">
	import { LatLng, type LatLngExpression } from 'leaflet';
	import Leaflet from '$lib/Leaflet.svelte';
	import Marker from '$lib/Marker.svelte';
	import Popup from '$lib/Popup.svelte';
	import { pv } from '$lib/components/stores.ts';
	import { round } from './util';
	import SolarIcon from './SolarIcon.svelte';

	let marker: Marker;
	const initialView: LatLngExpression = [$pv.lat, $pv.lng];

	function updatePos(event: any) {
		// console.log("marker dragged!",event);
		$pv.lng = event.detail.latlng.lng;
		$pv.lat = event.detail.latlng.lat;
	}

	function getCurrentPosition() {
		// this set the lat,lng from the browser location api
		navigator.geolocation.getCurrentPosition(function (position) {
			$pv.lat = round(position.coords.latitude);
			$pv.lng = round(position.coords.longitude);
			//tell leaflet to move the marker
			marker.updateLatLng($pv.lat, $pv.lng);
		});
	}
</script>

<div class="leafletBox">
	&nbsp; &nbsp; Move the solar panel icon to set your lat/lng. Or:
	<button on:click={(e) => getCurrentPosition()}> Use Browser Location</button>
	<Leaflet view={initialView} zoom={4}>
		<Marker
			bind:this={marker}
			bind:lat={$pv.lat}
			bind:lng={$pv.lng}
			width={40}
			height={40}
			on:move={updatePos}
		>
			<SolarIcon></SolarIcon>
			<Popup>Move this marker to set your lat/lng.</Popup>
		</Marker>
	</Leaflet>
</div>

<style>
	/* :global(.map) {
		height: 300px;
	} */

	.leafletBox {
		border: 1px solid #aaa;
		border-radius: 2px;
		box-shadow: 2px 2px 8px rgba(0, 0, 0, 0.1);
		padding: 0em;
		margin: 1rem;
		margin-top: 0rem;
		margin-bottom: 0rem;
	}
</style>
