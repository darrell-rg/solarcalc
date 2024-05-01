import { dev } from '$app/environment';

// we don't need any JS on this page, though we'll load
// it in dev so that we get hot module replacement
export const csr = dev;

// since there's no dynamic data here, we can prerender
// it so that it gets served as a static asset in production
export const prerender = true;


export const _bomData = [
    {
        "Desc": "Solar Panel",
        "Qty": 5,
        "Price": 150,
    },
    {
        "Desc": "Ground Rod",
        "Qty": 1,
        "Price": 40,
    },
    {
        "Desc": "Ground rod wire clamp",
        "Qty": 1,
        "Price": 8,
    },
    {
        "Desc": "Ground Wire",
        "Qty": 10,
        "Price": 2,
    },
    {
        "Desc": "Ground to rack bonding lug",
        "Qty": 1,
        "Price": 8,
    },
    {
        "Desc": "Solar Shutoff Switch",
        "Qty": 1,
        "Price": 150,
    },
    {
        "Desc": "Flexible Metal Conduit",
        "Qty": 3,
        "Price": 20,
    },
    {
        "Desc": "Plastic Conduit",
        "Qty": 5,
        "Price": 20,
    },
    {
        "Desc": "Roof jacks for rack",
        "Qty": 8,
        "Price": 12,
    },
    {
        "Desc": "Middle solar clamp bolts",
        "Qty": 8,
        "Price": 2,
    },
    {
        "Desc": "End solar clamp bolts ",
        "Qty": 4,
        "Price": 6,
        "Total": 24
    },
    {
        "Desc": "Roof to Rail brackets",
        "Qty": 16,
        "Price": 2,
    },
    {
        "Desc": "Stainless Lag bolts for roof mounts",
        "Qty": 16,
        "Price": 2,
    },
    {
        "Desc": "600v solar wire",
        "Qty": 100,
        "Price": 1.5,
    },
    {
        "Desc": "MC4 connectors",
        "Qty": 4,
        "Price": 4,
    },
    {
        "Desc": "Thermostatic Mixing Valve",
        "Qty": 1,
        "Price": 125,
    },
    {
        "Desc": "Misc copper fittings/elbows",
        "Qty": 6,
        "Price": 4,
    },
    {
        "Desc": "Water Heater element",
        "Qty": 1,
        "Price": 33,
    },
    {
        "Desc": "Solar Mounting Rails",
        "Qty": 2,
        "Price": 55,
    },
    {
        "Desc": "MC4 Crimper Kit",
        "Qty": 1,
        "Price": 44,
    },
    {
        "Desc": "Heater Element Wrench",
        "Qty": 1,
        "Price": 24,
    }
];

