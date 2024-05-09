import { dev } from '$app/environment';

// we don't need any JS on this page, though we'll load
// it in dev so that we get hot module replacement
export const csr = dev;

// since there's no dynamic data here, we can prerender
// it so that it gets served as a static asset in production
export const prerender = true;

//fixes https://stackoverflow.com/questions/69414265/error-when-evaluating-ssr-module-even-when-ssr-is-disabled-svelte-kit
export const ssr = false;
