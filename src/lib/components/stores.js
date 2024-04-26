import { readable, derived, writable } from 'svelte/store';
//https://github.com/MacFJA/svelte-persistent-store
//import { persist, localStorage } from "@macfja/svelte-persistent-store"

export const Vmpp = writable(42.8);
export const Impp = writable(8.06);
export const Voc = writable(55.2);

export const lat = writable(40.5);
export const lng = writable(-104.7);



function round(num) {
	var m = Number((Math.abs(num) * 100).toPrecision(15));
	return (Math.round(m) / 100) * Math.sign(num);
}

export const time = readable(new Date(), function start(set) {
	const interval = setInterval(() => {
		set(new Date());
	}, 1000);

	return function stop() {
		clearInterval(interval);
	};
});

export const elapsed = derived(time, ($time) => Math.round(($time - start) / 1000));

export const Rmpp = derived([Vmpp, Impp], ([$Vmpp, $Impp]) => round($Vmpp / $Impp));

const start = new Date();
