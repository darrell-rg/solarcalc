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
        "Qty": 4,
        "Price": 150,
        "Total": 600
    },
    {
        "Desc": "Ground Rod",
        "Qty": 1,
        "Price": 40,
        "Total": 40
    },
    {
        "Desc": "Ground Wire",
        "Qty": 10,
        "Price": 2,
        "Total": 20
    },
    {
        "Desc": "Ground - to - Rack lug",
        "Qty": 1,
        "Price": 8,
        "Total": 8
    },
    {
        "Desc": "Ground - ground rod lug",
        "Qty": 1,
        "Price": 8,
        "Total": 8
    },
    {
        "Desc": "Solar Shutoff Switch",
        "Qty": 1,
        "Price": 200,
        "Total": 200
    },
    {
        "Desc": "Metal Conduit",
        "Qty": 3,
        "Price": 20,
        "Total": 60
    },
    {
        "Desc": "Plastic Conduit",
        "Qty": 5,
        "Price": 20,
        "Total": 100
    },
    {
        "Desc": "Roof mounts for rack",
        "Qty": 8,
        "Price": 12,
        "Total": 96
    },
    {
        "Desc": "Mid-solar rack bolts",
        "Qty": 8,
        "Price": 2,
        "Total": 16
    },
    {
        "Desc": "End solar rack mounts ",
        "Qty": 4,
        "Price": 6,
        "Total": 24
    },
    {
        "Desc": "Lag bolts for roof mounts",
        "Qty": 8,
        "Price": 2,
        "Total": 16
    },
    {
        "Desc": "600v solar wire",
        "Qty": 100,
        "Price": 1.5,
        "Total": 150
    },
    {
        "Desc": "MC4 connectors",
        "Qty": 4,
        "Price": 4,
        "Total": 16
    },
    {
        "Desc": "Hot Water Mixing Valve",
        "Qty": 1,
        "Price": 125,
        "Total": 125
    },
    {
        "Desc": "Water Heater element",
        "Qty": 1,
        "Price": 33,
        "Total": 33
    },
    {
        "Desc": "Solar Rack Rails",
        "Qty": 2,
        "Price": 55,
        "Total": 110
    },
    {
        "Desc": "DC Breaker",
        "Qty": 1,
        "Price": 44,
        "Total": 44
    }
];

