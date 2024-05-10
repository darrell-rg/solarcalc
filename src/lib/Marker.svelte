<script lang="ts">
	import { onMount, onDestroy, getContext, setContext, createEventDispatcher } from 'svelte';
	import L from 'leaflet';
	import { writable } from 'svelte/store';

	export let width: number;
	export let height: number;
	export let lat: number;
	export let lng: number;

	let marker: L.Marker | undefined;
	let markerElement: HTMLElement;

	export function updateLatLng(newLat: number, newLng: number) {
		lat = newLat;
		lng = newLng;
		marker?.setLatLng([newLat, newLng]);

		map?.setView([newLat, newLng]);
	}

	const dispatch = createEventDispatcher();
	const { getMap }: { getMap: () => L.Map | undefined } = getContext('map');
	const map = getMap();

	setContext('layer', {
		// L.Marker inherits from L.Layer
		getLayer: () => marker
	});

	onMount(() => {
		if (map) {
			let icon = L.divIcon({
				html: markerElement,
				className: 'map-marker',
				iconSize: L.point(width, height)
			});
			let options = { draggable: true, icon: icon };
			marker = L.marker([lat, lng], options).addTo(map);
			marker.on('move', (e) => dispatch('move', e));
		}
	});

	onDestroy(() => {
		marker?.remove();
		marker = undefined;
	});
</script>

<div bind:this={markerElement}>
	{#if marker}
		<slot />
	{/if}
</div>
