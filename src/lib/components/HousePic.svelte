<script>
	import { onMount } from 'svelte';
	export let style;
	let time = new Date();

	let houseWidth = 80;
	let roofHeight = 80;
	let wallHeight = 67;

	let showShowerPerson = true;

	// these automatically update when `time`
	// changes, because of the `$:` prefix
	$: hours = time.getHours();
	$: minutes = time.getMinutes();
	$: seconds = time.getSeconds();

	onMount(() => {
		const interval = setInterval(() => {
			time = new Date();
		}, 1000);

		return () => {
			clearInterval(interval);
		};
	});
</script>

<svg viewBox="-50 -50 100 100" {style}>
	<mask id="myMask">
		<!-- Everything under a white pixel will be visible -->
		<rect x="0" y="0" width="100" height="100" fill="white" />

		<!-- Everything under a black pixel will be invisible -->
		<path
			d="M10,35 A20,20,0,0,1,50,35 A20,20,0,0,1,90,35 Q90,65,50,95 Q10,65,10,35 Z"
			fill="black"
		/>
	</mask>
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
		width="100"
		height="100"
		x="-50"
		y="-50"
		fill="url(#EarthAndSky)"
		transform="rotate(90)"
	/>

	<circle class="sun" r="8" fill="url('#sunGradient')" transform="translate(-36 -45.5) " />

	<polygon
		class="wall"
		points="0,0 {houseWidth},0 {houseWidth},{wallHeight} {houseWidth /
			2},{roofHeight} 0, {wallHeight}"
		transform="rotate(180) translate(-{houseWidth / 2} -40)"
	/>

	<polyline class="roof" points="-45,-25 0,-40  45,-25" />

	<g id="waterHeater">
		<rect
			class="waterheater"
			x="-25"
			y="-12"
			width="20"
			height="50"
			rx="2"
			fill="url(#waterHeaterGradient)"
		/>

		
		<path
			class="heatingElement"
			d="
		M -20, 2 h 18
		M -20,-2 h 18
		q 2,2  0,4
		"
			transform="translate(-9 31.5) scale(0.9)"
		/>

		{#each Array(10) as _, i}
			<path
				class="bubbles"
				d="M {i}, {(i % 2) / 2} v 18 "
				transform="translate(-20, 17) scale(0.9)"
			/>
		{/each}
	</g>

	<g id="waterPipes">
		<polyline class="coldWater" points="50,46 -15,46 -15,37 " />

		<polyline class="coldWater" points="4,46 4,-10" />
		<polyline class="hotWater" points="-12,-10 0,-10" />

		<polyline class="pipe" points="0,-10 22,-10 22,-8" fill="none" />
		<ellipse class="shower" cx="22" cy="-8" rx="6" ry="3" />
		<rect class="valve" x="0" y="-12" width="8" height="8" rx="0.2" />

		{#each Array(10) as _, i}
			<path
				class="waterDrops"
				d="M {i}, {(i % 2) / 2} v 18 "
				transform="translate(18 -8) scale(0.9)"
			/>
		{/each}
	</g>

	<g id="thermometer" transform="translate(-0.4 -12.5) scale(0.3)">
		<style type="text/css">
			.st0 {
				fill: none;
				stroke: #000000;
				stroke-width: 2;
				stroke-linecap: round;
				stroke-linejoin: round;
				stroke-miterlimit: 10;
			}
			.st1 {
				fill: none;
				stroke: #000000;
				stroke-width: 2;
				stroke-linejoin: round;
				stroke-miterlimit: 10;
			}
		</style>
		<path
			class="st0"
			d="M15,17.81V6c0-1.66-1.34-3-3-3S9,4.34,9,6v11.81C7.21,18.85,6,20.78,6,23c0,3.31,2.69,6,6,6s6-2.69,6-6
	C18,20.78,16.79,18.85,15,17.81z"
		/>
		<circle class="st0" cx="12" cy="23" r="3" />
		<line class="st0" x1="12" y1="13" x2="12" y2="20" />
		<line class="st0" x1="20" y1="6" x2="25" y2="6" />
		<line class="st0" x1="20" y1="10" x2="22" y2="10" />
		<line class="st0" x1="20" y1="14" x2="25" y2="14" />
		<line class="st0" x1="20" y1="18" x2="22" y2="18" />
	</g>

	<g class="electrical">
		<!-- <polyline class='conduit' points ='-33,30 -33,-30  ' /> -->

		<path
			class="blackWire"
			transform="translate(-32 -32) "
			d="
		M 0 0
		V 65 
		H 7 
	"
		/>

		<path
			class="redWire"
			transform="translate(-30 -33) "
			d="
	M 0 0
	V 63 
	H 7 
"
		/>


		<rect class="conduit" x="-28" y="29" width="5" height="5" rx="0.2" />
		<polyline class="greenWire" points="-35,73 -35,-31" transform="translate(-1, 0) " />

		<!-- the switch -->
		<rect class="conduit" x="-38" y="-11" width="10" height="9" rx="0.2" />
		<line class="onOff" x1="-33" y1="-5" x2="-33" y2="-10.5" />
		<circle class="onOff" r="3" transform="translate(-33, -6) "></circle>
		<line class="solarPanel" x1="-5" y1="-41" x2="-43" y2="-28" />
	</g>

	{#if showShowerPerson}
		<g id="showerUser" transform="translate(15 -0.5) scale(0.125)">
			<ellipse
				transform="matrix(0.3947 -0.9188 0.9188 0.3947 6.9937 106.2129)"
				style="fill-rule:evenodd;clip-rule:evenodd;fill:#FFDECC;"
				cx="84.107"
				cy="47.799"
				rx="7.317"
				ry="4.231"
			/>
			<path
				style="fill-rule:evenodd;clip-rule:evenodd;fill:#FF690F;"
				d="M15.989,84.083c-2.123-2.848-0.711-5.583,2.494-7.394
		c4.619-2.612,3.463-6.694-2.235-9.305c-5.698-2.61-6.774-10.451-0.769-14.774c6.006-4.323,7.543-7.793,3.306-13.67
		c-4.237-5.877-1.059-15.83,5.41-17.134c6.469-1.304,5.493-2.072,6.873-7.245c2.401-8.996,12.755-15.862,18.298-9.985
		c7.928-9.703,25.751-2.295,28.978,6.681c3.419,9.512,6.514,9.417,11.597,12.045c5.083,2.628,6.743,14.486,2.889,19.431
		c-5.1,6.541-2.293,9.457,3.944,12.558c6.236,3.101,4.71,7.677-0.256,10.246c-4.966,2.567-8.048,7.154-3.428,9.766
		c3.384,1.913,4.382,4.639,3.077,8.803C89.988,103.839,33.139,107.093,15.989,84.083z"
			/>
			<path
				style="fill-rule:evenodd;clip-rule:evenodd;fill:#FFDECC;"
				d="M66.808,73.832c-0.198,0.313-19.745,0.624-19.962,0.932
		c-6.139,8.759-19.404,12.596-29.95,14.954c-10.497,2.347-10.903,15.68-10.919,24.56h102.324c-0.016-8.88-0.211-22.165-10.919-24.56
		C86.674,87.323,72.632,82.989,66.808,73.832z"
			/>
			<path
				style="fill-rule:evenodd;clip-rule:evenodd;fill:#FFDECC;"
				d="M67.391,55.129v25.117c-5.639,7.412-14.865,7.155-20.504,0
		V55.129C46.887,41.566,67.391,41.566,67.391,55.129z"
			/>
			<path
				style="fill-rule:evenodd;clip-rule:evenodd;fill:#F7C5AA;"
				d="M67.391,55.129v16.816c-3.88,3.035-7.619,4.735-10.252,4.735
		s-6.373-1.701-10.252-4.735V55.129C46.887,41.566,67.391,41.566,67.391,55.129z"
			/>
			<path
				style="fill-rule:evenodd;clip-rule:evenodd;fill:#FFDECC;"
				d="M57.139,72.503c-6.674,0-20.775-10.494-25.135-25.524
		c-4.401-15.176,3.889-36.944,25.135-36.944c21.247,0,29.537,21.767,25.135,36.944C77.915,62.009,63.814,72.503,57.139,72.503z"
			/>
			<path
				style="fill-rule:evenodd;clip-rule:evenodd;fill:#FF386A;"
				d="M49.099,57.372c3.401-3.293,6.054-0.823,8.04-0.823
		c1.986,0,4.639-2.47,8.04,0.823C63.352,66.056,51.523,66.322,49.099,57.372z"
			/>
			<path
				style="fill-rule:evenodd;clip-rule:evenodd;fill:#FFFFFF;"
				d="M50.143,57.821c1.859-0.476,11.329-0.572,13.992-0.104
		C61.936,61.766,52.004,61.531,50.143,57.821z"
			/>
			<path
				style="fill-rule:evenodd;clip-rule:evenodd;fill:#FF386A;"
				d="M49.099,57.372c3.401-3.293,6.054-0.823,8.04-0.823
		c1.986,0,4.64-2.47,8.04,0.823C59.979,59.934,52.599,58.737,49.099,57.372z"
			/>
			<path
				style="fill-rule:evenodd;clip-rule:evenodd;fill:#86BCEB;"
				d="M19.817,114.279c10.919-12.724,26.538-2.11,36.693-2.11
		c10.156,0,25.614-12.221,36.693,2.11H19.817z"
			/>
			<path
				style="fill-rule:evenodd;clip-rule:evenodd;fill:#FF690F;"
				d="M78.786,61.817c-5.121,9.614,20.594-24.301-1.557-46.802
		C64.004,1.58,42.087,2.522,33.522,17.437c4.192,6.348,13.161,12.018,23.672,11.799c17.868-0.373-1.385,10.868,13.17,12.785
		c10.6,1.396,8.531,3.318,3.35,9.113C70.086,55.192,71.114,60.476,78.786,61.817z"
			/>

			<ellipse
				transform="matrix(-0.3947 -0.9188 0.9188 -0.3947 -1.1945 94.8102)"
				style="fill-rule:evenodd;clip-rule:evenodd;fill:#FFDECC;"
				cx="30.634"
				cy="47.799"
				rx="7.317"
				ry="4.231"
			/>
			<path
				style="fill-rule:evenodd;clip-rule:evenodd;fill:#FF690F;"
				d="M43.458,17.74c-1.993,8.191,1.319,14.569-5.437,15.37
		c-8.791,1.042-4.606,6.565-5.285,13.348C27.883,40.41,26.318,13.533,43.458,17.74z"
			/>
		</g>

		<g id="showerDoor" transform="translate(7 10) scale(1.25,1.34)">
			<path
				opacity=".75"
				d="M21 12.257c-1.87.487-1.812 1.78-1.737 3.381.068 1.492.153 3.349-2.225 3.644-2.683.333-3.125 1.119-3.295 1.718H21z"
			/><path
				opacity=".5"
				d="M21 8.853c-2.233-.476-3.917.348-5.581 1.317-1.638.955-1.183 1.737-.607 2.727.326.562.664 1.143.384 1.707-.228.459-.788.72-1.815.848-3.175.393-3.849 2.036-4.211 2.919a3.063 3.063 0 0 1-.233.488 8.424 8.424 0 0 0-.498.9A6.94 6.94 0 0 1 7.7 21h5.01l.014-.054c.26-1.066.82-2.239 4.19-2.656 1.398-.174 1.424-.969 1.349-2.606-.075-1.625-.168-3.82 2.736-4.448z"
			/><path
				opacity=".25"
				d="M21 3h-1.286a21.544 21.544 0 0 0-9.27 3.325l-.215.126c-.768.447-1.181.96-1.134 1.404.038.357.384.685.905.855a1.87 1.87 0 0 1 1.508 1.92 2.802 2.802 0 0 1-2.526 2.218C6.3 13.181 6.355 14.19 6.4 15.002a1.47 1.47 0 0 1-.141.935C5.472 17.117 4.326 17.385 3 17.69V21h2.961c.835-.213 1.169-.863 1.584-1.689a9.411 9.411 0 0 1 .56-1.006 2.101 2.101 0 0 0 .14-.314c.377-.918 1.258-3.066 5.013-3.532.915-.113 1.042-.3 1.043-.301a2.486 2.486 0 0 0-.354-.759c-.536-.921-1.532-2.636.968-4.093A8.461 8.461 0 0 1 21 7.85z"
			/><path
				d="M19.696 2H2v20h20V2zm-4.675 1A29.014 29.014 0 0 0 9.94 5.461l-.214.125C8.186 6.483 8.047 7.46 8.1 7.96a2.11 2.11 0 0 0 1.588 1.7c.402.131.87.39.823.875a1.83 1.83 0 0 1-1.653 1.321c-3.611.447-3.506 2.308-3.457 3.202.008.131.018.311.025.324A3.463 3.463 0 0 1 3 16.664V3zM21 21h-7.257c.17-.6.612-1.385 3.295-1.718 2.378-.295 2.293-2.152 2.225-3.644-.075-1.6-.133-2.894 1.737-3.381zm0-9.764c-2.904.628-2.81 2.823-2.736 4.448.075 1.637.049 2.432-1.349 2.606-3.37.417-3.93 1.59-4.19 2.656L12.71 21H7.7a6.94 6.94 0 0 0 .737-1.24 8.424 8.424 0 0 1 .498-.9 3.063 3.063 0 0 0 .234-.49c.362-.882 1.036-2.525 4.21-2.918 1.028-.128 1.588-.389 1.816-.849.28-.564-.058-1.144-.385-1.706-.575-.99-1.03-1.773.608-2.727C17.083 9.2 18.767 8.377 21 8.853zm0-3.387a8.461 8.461 0 0 0-6.085 1.457c-2.5 1.457-1.504 3.172-.968 4.093a2.486 2.486 0 0 1 .354.759c-.001.002-.128.188-1.043.301-3.755.466-4.636 2.614-5.013 3.532a2.101 2.101 0 0 1-.14.314 9.411 9.411 0 0 0-.56 1.006c-.415.826-.75 1.476-1.584 1.689H3v-3.31c1.326-.305 2.472-.573 3.259-1.753a1.47 1.47 0 0 0 .141-.935c-.045-.812-.101-1.821 2.582-2.154a2.802 2.802 0 0 0 2.526-2.218A1.87 1.87 0 0 0 10 8.71c-.52-.17-.867-.498-.905-.855-.047-.445.366-.957 1.134-1.404l.215-.126A21.544 21.544 0 0 1 19.714 3H21z"
			/><path fill="none" d="M0 0h24v24H0z" />
		</g>
	{/if}
</svg>

<style>
	svg {
		/* width: 100%;
		height: 100%; 
		border: 1px solid red;
		*/
	}

	.wall {
		stroke: burlywood;
		fill: white;
	}

	.roof {
		stroke: burlywood;
		stroke-width: 1.5;
		fill: none;
	}
	.waterDrops {
		stroke-dasharray: 1;
		stroke: darkblue;
		stroke-width: 0.25;
		animation: dash 30s linear infinite;
	}
	@keyframes dash {
		to {
			stroke-dashoffset: -100;
		}
	}
	.sun {
		stroke: none;
	}

	.bubbles {
		stroke-dasharray: 1;
		stroke: rgb(139, 0, 23);
		stroke-width: 0.5;
		animation: dashup 30s linear infinite;
	}

	@keyframes dashup {
		to {
			stroke-dashoffset: 100;
		}
	}
	.waterheater {
		stroke: #666;
		stroke-width: 1.2;
		/* fill: lightblue; */
	}

	.solarPanel {
		stroke-width: 1.2;
		stroke: blue;
		fill: lightblue;
	}

	.conduit {
		stroke: #999;
		fill: #999;
		stroke-width: 1;
	}

	.shower {
		stroke: #444;
		fill: #777;
		stroke-width: 0.7;
	}

	.pipe {
		stroke: #444;
		fill: none;
		stroke-width: 1.5;
	}

	.valve {
		stroke: #999;
		fill: #999;
		stroke-width: 2;
	}

	.hotWater {
		stroke: red;
		fill: none;
		stroke-width: 1.5;
	}

	.coldWater {
		stroke: blue;
		fill: none;
		stroke-width: 1.5;
	}

	.redWire {
		stroke: red;
		fill: none;
		stroke-width: 0.7;
	}

	.blackWire {
		stroke: black;
		fill: none;
		stroke-width: 0.7;
	}

	.greenWire {
		stroke: green;
		fill: none;
		stroke-width: 0.7;
	}

	.onOff {
		stroke: black;
		fill: none;
		stroke-width: 0.8;
	}

	.heatingElement {
		stroke: red;
		fill: none;
		stroke-width: 1;
	}
	/* 
	.second, .second-counterweight {
		stroke: rgb(180,0,0);
	}

	.second-counterweight {
		stroke-width: 3;
	} */
</style>
