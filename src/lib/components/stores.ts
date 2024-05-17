import { readable, derived, writable } from 'svelte/store';
import { persisted } from 'svelte-persisted-store';
import { defaultPrefs } from '$lib/components/util';

// export const lat = writable(40.5);
// export const lng = writable(-104.7);

function onWriteError(error: any) {
	console.log(error);
}

function onParseError(raw: any, error: any) {
	console.log('error loading prefs, using defaults', error);
	pv.set(defaultPrefs);
}

// First param `solarPrefs` is the local storage key.
// if defaultPrefs changes, need to clear out local storage or we will have error
// also make sure you use a deep copy of the defaults or they might get changed
export const pv = persisted('solarPrefs', JSON.parse(JSON.stringify(defaultPrefs)), {
	serializer: JSON, // defaults to `JSON`
	storage: 'local', // 'session' for sessionStorage, defaults to 'local'
	syncTabs: false, // choose whether to sync localStorage across tabs, default is true
	onWriteError: (error) => onWriteError, // Defaults to console.error with the error object
	onParseError: (raw, error) => onParseError // Defaults to console.error with the error object
});
