<script>
	import Counter from '$lib/Counter.svelte';
	import Box from '$lib/components/Box.svelte';

	import Input from '$lib/components/Input.svelte';
	import HousePic from '$lib/components/HousePic.svelte';
	import TestSvg from '$lib/components/TestSvg.svelte';
	import Output from '$lib/components/Output.svelte';
	import { time, elapsed, Vmpp, Voc, Impp, Rmpp } from '$lib/components/stores.js';
	import { element } from 'svelte/internal';
	import Map from '$lib/components/Map.svelte';
	import LeafletMap from '$lib/components/LeafletMap.svelte';

	let lat = 40.5;
	let lng = -105.7;

	let useCityPower = false;

	function updateCalc(value) {
		f = +value;
		c = +((5 / 9) * (f - 32)).toFixed(1);
	}

	const formatter = new Intl.DateTimeFormat('en', {
		hour12: true,
		hour: 'numeric',
		minute: '2-digit',
		second: '2-digit'
	});

	function round(num) {
		// rounds to two digits
		var m = Number((Math.abs(num) * 100).toPrecision(15));
		return (Math.round(m) / 100) * Math.sign(num);
	}

	function getCurrentPosition() {
		navigator.geolocation.getCurrentPosition(function (position) {
			lat = round(position.coords.latitude);
			lng = round(position.coords.longitude);
		});
	}

	// Month in JavaScript is 0-indexed (January is 0, February is 1, etc),
	// but by using 0 as the day it will give us the last day of the prior
	// month. So passing in 1 as the month number will return the last day
	// of January, not February
	function daysInMonth(year, month) {
		return new Date(year, month, 0).getDate();
	}

	function tokWh(j) {
		//converts joules to kwh
		return j / 3600e3;
	}

	function clamp(value, min, max) {
		if (value < min) return min;

		if (value > max) return max;

		return value;
	}

	let wireGuages = [
		{ id: 1, r: 2.1, text: `8AWG, 2.1 Ω/km` },
		{ id: 2, r: 3.35, text: `10AWG, 3.35 Ω/km` },
		{ id: 3, r: 5.31, text: `12AWG,  5.31  Ω/km` },
		{ id: 4, r: 8.46, text: `14AWG,  8.46  Ω/km` }
	];

	let selectedWire = wireGuages[0];

	let months = [
		'January',
		'February',
		'March',
		'April',
		'May',
		'June',
		'July',
		'August',
		'September',
		'October',
		'November',
		'December'
	];
	let panelsPerString = 5;
	let parallelStrings = 1;
	let azimuth = 180;
	let elevation = 40;
	let wireLength = 100;

	let wireResistance = 2.1;

	let tankSize = 151; //40 gal
	//heat capacity Cp of water is 4.186kJ/kg-K
	let heatCapOfWater = 4186; // j/l/k
	let hotWaterOutTemp = 50;
	let hotWaterPerPersonDay = 50; // l/person/day
	let personsInHoushold = 4;
	let groundTemp = 5;
	let avgPowerPrice = 0.2;
	let energyToHeatOneTank = heatCapOfWater * tankSize * (hotWaterOutTemp - groundTemp);

	let year = new Date().getFullYear();

	let monthData = [];

	let peakHours = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0];

	months.forEach((month, index) => {
		let m = {
			month: months[index],
			days: daysInMonth(year, index),
			insolation: 0.5 + Math.random() * 0.5,
			Edemand: 0,
			Esolar: 456 * Math.random(),
			Ecity: -1,
			savings: -1
		};

		m.Edemand = tokWh(
			m.days * ((hotWaterPerPersonDay * personsInHoushold) / tankSize) * energyToHeatOneTank
		);
		m.Ecity = clamp(m.Edemand - m.Esolar, 0, 999999999);

		m.savings = (m.Edemand - m.Ecity) * avgPowerPrice;
		monthData.push(m);
	});

	// the `$:` means 're-run whenever these values change'
	// does not listen to changes happening inside components
	$: wireResistance = (selectedWire.r * wireLength) / 1000;
	$: energyToHeatOneTank = heatCapOfWater * tankSize * (hotWaterOutTemp - groundTemp);


</script>

<svelte:head>
	<title>PVH2O</title>
</svelte:head>

<h1>Free Hot Water!</h1>

<ul class="smol-css-grid">
	<li style="max-width: 300px;">
		<figure>
			<img alt="SolarShed" src="solarShed/PanelsInSun.jpg" />
			<figcaption>Make your shed pay!</figcaption>
		</figure>
	</li>
	<li style="max-width: 300px;">
		<figure>
			<HousePic />
			<figcaption>Simple</figcaption>
		</figure>
	</li>

	<li style="max-width: 300px;">
		<figure>
			<img alt="SolarShed" src="solarShed/firstPower.jpg" />
			<figcaption>Free power!</figcaption>
		</figure>
	</li>
</ul>

<!-- <div class="smol-flexbox-grid">
	<div> -->

<div class="smol-sidebar">
	<span data-text>
		<h2>Step 1</h2>
		Fill in what you know about your Location and power price
	</span>
	<span>
		<Box>
			<h2>Location Specs</h2>
			<!-- 
				<button on:click="{getCurrentPosition()}">Get Current Position</button>
				<br> 
			-->
			<Input val={lat} label="Lattitude" units="°North" />
			<Input val={groundTemp} label="GroundTemp" units="°C" />
			<Input val={50} label="Cloudy days per year" units="days" />
			<Input val={7.16} label="Off Peak Price" units="$/kwh" />
			<Input val={23.52} label="Peak Price" units="$/kwh" />

			<label>
				PeakHours <br />
				<input type="checkbox" bind:checked={peakHours[0]} />
				<input type="checkbox" bind:checked={peakHours[1]} />
				<input type="checkbox" bind:checked={peakHours[2]} />
				<input type="checkbox" bind:checked={peakHours[3]} />
				<input type="checkbox" bind:checked={peakHours[4]} />
				<input type="checkbox" bind:checked={peakHours[5]} />
				<input type="checkbox" bind:checked={peakHours[6]} />
				<input type="checkbox" bind:checked={peakHours[7]} />
				<input type="checkbox" bind:checked={peakHours[8]} />
				<input type="checkbox" bind:checked={peakHours[9]} />
				<input type="checkbox" bind:checked={peakHours[10]} />
				<input type="checkbox" bind:checked={peakHours[11]} />
				<input type="checkbox" bind:checked={peakHours[12]} />
				<input type="checkbox" bind:checked={peakHours[13]} />
				<input type="checkbox" bind:checked={peakHours[14]} />
				<input type="checkbox" bind:checked={peakHours[15]} />
				<input type="checkbox" bind:checked={peakHours[16]} />
				<input type="checkbox" bind:checked={peakHours[17]} />
				<input type="checkbox" bind:checked={peakHours[18]} />
				<input type="checkbox" bind:checked={peakHours[19]} />
				<input type="checkbox" bind:checked={peakHours[20]} />
				<input type="checkbox" bind:checked={peakHours[21]} />
				<input type="checkbox" bind:checked={peakHours[22]} />
				<input type="checkbox" bind:checked={peakHours[23]} />
			</label>
			<hr />
			<Output val={$Rmpp} label="City Power Price/day" units="$" />
		</Box>
	</span>
<span>
<span>
	<Map location=[40.57,-105.07]/>
</span>
</div>

<div class="smol-sidebar">
	<span data-text>
		<h2>Step 2</h2>
		Impedance matching calculator. Use this to figure out the optimal resistance for your water heater
		element.
	</span>
	<span>
		<Box>
			<h2>Solar Panel Specs</h2>
			<Input val={$Voc} label="Voc" units="v" />
			<Input val={$Rmpp} label="Vmpp" units="v" />
			<Input val={$Impp} label="Impp" units="a" />
			<Input val={panelsPerString} label="Panels per string" units="" />
			<Input val={parallelStrings} label="Parallel strings" units="" />
			<Input val={azimuth} label="Azimuth  180=South" units="°" />
			<Input val={elevation} label="Elevation 0=Flat" units="°" />
			<label>
				<select bind:value={selectedWire}>
					{#each wireGuages as g}
						<option value={g}>
							{g.text}
						</option>
					{/each}
				</select>
				Wire Gauge
			</label>
			<br />

			<Input val={wireLength} label="Total wire length" units="m" />
			<hr />
			<Output
				val={round(($Vmpp * panelsPerString) / $Impp)}
				label="Rmpp of full string"
				units="Ω"
			/>
			<Output val={$Vmpp * panelsPerString} label="Vmpp of full string" units="v" />
			<Output val={$Voc * panelsPerString} label="Voc of full string" units="v" />
			<Output val={wireResistance} label="Resistance of wire" units="Ω" />
			<Output
				val={round($Vmpp * panelsPerString * $Impp)}
				label="Nominal power of string"
				units="w"
			/>
			<Output val={round($Impp * $Impp * wireResistance)} label="Wire Losses at Mpp" units="w" />
		</Box>
	</span>
	<span>

		<div id="map" style="height: 250px;"></div>
	</span>
</div>

<div class="smol-sidebar">
	<span data-text>
		<h2>Step 3</h2>
		Impedance matching calculator. Use this to figure out the optimal resistance for your water heater
		element.
	</span>
	<span>
		<Box>
			<h2>Water Heater Specs</h2>
			<Input val={4} label="Heating Element Resistance" units="Ω" />
			<Input val={tankSize} label="TankSize" units="liter" />
			<Input val={4} label="StandbyLoss" units="W" />
			<Input val={hotWaterOutTemp} label="Desired Output Temp" units="°C" />
			<!-- <Input val={50} label="ThermostatSetting" units="°C" /> -->
			<Input val={hotWaterPerPersonDay} label="Hot Water/Person/Day" units="l" />
			<Input val={personsInHoushold} label="Persons In Houshold" units="" />
			<label>
				<input type="checkbox" bind:checked={useCityPower} />
				Use city power for top element
			</label>
			<hr />
			<Output val={round(energyToHeatOneTank / 3600e3)} label="Energy to heat 1 tank" units="kWh" />

			<Output
				val={round((avgPowerPrice * energyToHeatOneTank) / 3600e3)}
				label="Power Cost/day"
				units="$"
			/>
		</Box>
	</span>
</div>

<div class="smol-sidebar">
	<span data-text>
		<h2>Step 4</h2>
		Run simulator, view pretty graphs and numbers.

		<button> Run random week in spring</button>
		<button> Run random week in summer</button>
		<button> Run random week in fall</button>
		<button> Run random week in winter</button>
	</span>
	<span>
		<Box>
			<h2>Summer Sim results</h2>

			<figure>
				<img alt="SolarShed" src="day44.png" />
				<figcaption>Cheap and simple DIY solar hot water!</figcaption>
			</figure>
		</Box>
	</span>
</div>

<!-- 
<Box>
	<h2>Usage Specs</h2>
	<Input val={4} label="Persons In Houshold" units="" />
	<Input val={4} label="Shower GPM" units="" />
	<Input val={4} label="Shower Time/day" units="min" />

	<input type=radio bind:group={wireResistPerKm} value={2.1}>8AWG
	<input type=radio bind:group={wireResistPerKm} value={3.35}>10AWG
	<input type=radio bind:group={wireResistPerKm} value={5.31}>12AWG 
</Box>


<Box>
	<h2>Material Costs</h2>
	<Input val={110} label="Price per panel" units="$" />
	<Input val={600} label="Other expenses" units="$" />
	Racking, Conduit, Cutoffswitch, GroundRod, Brackets, Wire, Panel Clamps, MixingValue, CrimpTool, GroundWire, GroundClamp
  <br>
	<Input val={600} label="Total Material" units="$" />
</Box> -->

<!-- <h5>The time is ss {formatter.format($time)}</h5>

<p>
	This page has been open for
	{$elapsed}
	{$elapsed === 1 ? "second" : "seconds"}
</p>

</div> -->
<div>
	<!-- <TestSvg/> -->
	<table class="monthTable">
		<tr>
			<th>Month</th>
			<th>Days</th>
			<th>Insolation</th>
			<th>Energy Demand (kWh)</th>
			<th>Solar Energy (kWh)</th>
			<th>City Energy (kWh)</th>
			<th>Savings ($)</th>
		</tr>
		{#each monthData as m}
			<tr>
				<td>{m.month}</td>
				<td>{round(m.days)}</td>
				<td>{round(m.insolation)}</td>
				<td>{round(m.Edemand)}</td>
				<td>{round(m.Esolar)}</td>
				<td>{round(m.Ecity)}</td>
				<td>{round(m.savings)}</td>
			</tr>
		{/each}
	</table>
</div>
<!-- </div> -->

<!-- <Counter /> -->

<style>

	.map{
		height: 300px;
	}
	h1,
	figure,
	p {
		text-align: center;
		margin: 0 auto;
	}

	h1 {
		font-size: 2.8em;
		text-transform: uppercase;
		font-weight: 700;
		margin: 0 0 0.5em 0;
	}

	h2 {
		font-size: 1.5em;
		font-weight: 700;
		margin: 0 0 0.5em 0;
	}

	figure {
		margin: 0 0 1em 0;
	}

	.monthTable {
		border: 1px solid #dddddd;
		text-align: left;
		padding: 8 px;
	}
	tr {
		border-bottom: 1px solid #ddd;
	}
	tr:nth-child(even) {
		background-color: #d6eeee;
	}

	.smol-css-grid li {
		list-style: none;
		margin: 0;
	}

	.smol-css-grid {
		--min: 15ch;
		--gap: 1rem;

		display: grid;
		grid-gap: var(--gap);
		/* min() with 100% prevents overflow
		in extra narrow spaces */
		grid-template-columns: repeat(auto-fit, minmax(min(100%, var(--min)), 1fr));
	}

	.smol-flexbox-grid {
		--min: 10ch;
		--gap: 1rem;

		display: flex;
		flex-wrap: wrap;
		gap: var(--gap);
	}

	.smol-flexbox-grid > * {
		flex: 1 1 var(--min);
		/* border: 1px solid red; */
	}

	.smol-flexbox-grid > div:first-child {
		max-width: 350px;
		border-radius: 0.5rem 0.5rem 0 0;
	}

	.smol-sidebar {
		display: grid;
		grid-template-columns: fit-content(20ch) minmax(min(50vw, 30ch), 1fr) minmax(min(50vw, 30ch), 1fr);
	}

	img {
		width: 100%;
		max-width: 400px;
		margin: 0 0 1em 0;
	}

	p {
		margin: 1em auto;
	}

	@media (min-width: 480px) {
		h1 {
			font-size: 4em;
		}
	}
</style>
