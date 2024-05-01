<script>
	import { onMount } from "svelte";
	export let style;
	let time = new Date();

	let houseWidth = 80;
	let roofHeight = 80;
	let wallHeight = 67;

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

<svg viewBox="-50 -50 100 100" style="{style}">
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

	<circle
		class="sun"
		r="8"
		fill="url('#sunGradient')"
		transform="translate(-36 -45.5) "
	/>

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
			x="-30"
			y="-12"
			width="20"
			height="50"
			rx="2"
			fill="url(#waterHeaterGradient)"
		/>

		<rect class="conduit" x="-34" y="30" width="5" height="4" rx="0.2" />
	</g>

	<g id="waterPipes">
		<polyline class="coldWater" points="50,46 -23,46 -23,37 " />

		<polyline class="coldWater" points="2,46 2,-10" />
		<polyline class="hotWater" points="-12,-10 0,-10" />

		<polyline class="pipe" points="0,-10 22,-10 22,-8" fill="none" />
		<ellipse class="shower" cx="22" cy="-8" rx="6" ry="3" />
		<rect class="valve" x="0" y="-12" width="4" height="4" rx="0.2" />

		{#each Array(10) as _, i}
			<path
				class="waterDrops"
				d="M {i}, {(i % 2) / 2} v 18 "
				transform="translate(18 -8) scale(0.9)"
			/>
		{/each}
	</g>

	<!-- <polyline class='conduit' points ='-33,30 -33,-30  ' /> -->
	<polyline
		class="redWire"
		points="-33,31 -33,-31"
		transform="translate(-0.3 0) "
	/>
	<polyline
		class="blackWire"
		points="-33,31 -33,-31"
		transform="translate(0.3 0) "
	/>

	<path
		class="heatingElement"
		d="
	M -18, 2 h 18
	M -18,-2 h 18
	q 2,2  0,4
	"
		transform="translate(-16 32) scale(0.7)"
	/>

	<line class="panel" x1="-5" y1="-41" x2="-43" y2="-28" />

	<!-- second hand 
	<g transform='rotate({6 * seconds})'>
		<line class='second' y1='10' y2='-38'/>
		<line class='second-counterweight' y1='10' y2='2'/>
	</g>
    -->
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
		animation: dash 15s linear;
	}
	@keyframes dash {
		to {
			stroke-dashoffset: -100;
		}
	}
	.sun {
		stroke: none;
	}

	.waterheater {
		stroke: #666;
		stroke-width: 1.2;
		/* fill: lightblue; */
	}

	.panel {
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
		stroke-width: 1;
	}

	.valve {
		stroke: #999;
		fill: #999;
		stroke-width: 2;
	}

	.hotWater {
		stroke: red;
		fill: none;
		stroke-width: 1;
	}

	.coldWater {
		stroke: blue;
		fill: none;
		stroke-width: 1;
	}

	.redWire {
		stroke: red;
		fill: none;
		stroke-width: 0.3;
	}

	.blackWire {
		stroke: black;
		fill: none;
		stroke-width: 0.3;
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
