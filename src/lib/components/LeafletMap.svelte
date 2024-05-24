<script lang="ts">
	import { LatLng, type LatLngExpression } from 'leaflet';
	import Leaflet from '$lib/Leaflet.svelte';
	import Marker from '$lib/Marker.svelte';
	import Popup from '$lib/Popup.svelte';
	import { pv } from '$lib/components/stores.ts';
	import { round } from './util';
	import SolarIcon from './SolarIcon.svelte';
	import Box from './Box.svelte';

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

<Box style="padding: 0em;">
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
</Box>
