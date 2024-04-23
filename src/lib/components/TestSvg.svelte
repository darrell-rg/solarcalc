<script>
    import { onMount } from "svelte";

    let time = new Date();

    let houseWidth = 80;
    let roofHeight = 80;
    let wallHeight = 67;

    let viewWidth = 400;
    let viewHeight = 300;
</script>

<svg
    width="{viewWidth}px"
    height="{viewHeight}px"
    viewBox="0 0 {viewWidth} {viewHeight}"
>
    <title>3D perspective on transformed shapes</title>
    <style type="text/css">
        rect {
            stroke-width: 3;
            stroke-linejoin: round;
        }
        .inside {
            fill: burlywood;
            stroke: saddleBrown;
        }
        .outside {
            fill: lightGray;
            stroke: gray;
        }
        .sun {
            stroke: none;
        }
    </style>

    <defs>
        <linearGradient id="waterHeaterGradient" x1="0" x2="0" y1="0" y2="1">
            <stop offset="0%" stop-color="red" />
            <stop offset="100%" stop-color="blue" />
        </linearGradient>

        <linearGradient id="EarthAndSky">
            <stop offset="0%" stop-color="lightblue" />
            <stop offset="80%" stop-color="white" stop-opacity="0" />
            <stop offset="100%" stop-color="green" />
        </linearGradient>

        <linearGradient id="sunGradient" gradientTransform="rotate(90)">
            <stop offset="50%" stop-color="gold" />
            <stop offset="85%" stop-color="orange" />
        </linearGradient>
    </defs>

    <rect
        class="background"
        width="{viewWidth}"
        height="{viewHeight}"
        x="{viewWidth/2}"
        y="{viewHeight/2}"
        fill="url(#EarthAndSky)"
    />

    <circle
        class="sun"
        r="8"
        fill="url('#sunGradient')"
        transform="translate(-36 -45.5) "
    />

    <g transform="translate(50,100)">
        <rect
            class="inside"
            width="250"
            height="150"
            transform="translate(50,-50)"
        />
        <rect
            class="inside"
            width="100"
            height="150"
            transform="skewY(-45) scale(0.5,1)"
        />

        <!-- <rect class="outside" width="250" height="150" /> -->
        <rect
            class="outside"
            width="100"
            height="150"
            transform="translate(250,0) skewY(-45) scale(0.5,1)"
        />
    </g>
</svg>

<style>
</style>
