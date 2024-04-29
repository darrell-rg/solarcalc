<script>
	import Counter from '$lib/Counter.svelte';
	import Box from '$lib/components/Box.svelte';

	import Input from '$lib/components/Input.svelte';
	import HousePic from '$lib/components/HousePic.svelte';
	import TestSvg from '$lib/components/TestSvg.svelte';
	import Output from '$lib/components/Output.svelte';
	import { time, elapsed, Vmpp, Voc, Impp, Rmpp, lat, lng } from '$lib/components/stores.js';
	import { element } from 'svelte/internal';
	import Map from '$lib/components/Map.svelte';
	import { PUBLIC_API_URL } from '$env/static/public';

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
	let useMixingValve = 1;

	let mixingValveConstant = 1.5;

	let wireResistance = 2.1;

	let tankSize = 151; //40 gal
	//heat capacity Cp of water is 4.186kJ/kg-K
	let heatCapOfWater = 4186; // j/l/k
	let hotWaterOutTemp = 50;
	let hotWaterPerPersonDay = 64; // l/person/day
	let personsInHoushold = 4;
	let groundTemp = 5;
	let energyFactor = 0.91;
	let powerPerPanel = $Vmpp * $Impp;
	let nominalPower = powerPerPanel * panelsPerString * parallelStrings;
	let energyToHeatOneTank = heatCapOfWater * tankSize * (hotWaterOutTemp - groundTemp);
	let tanksUsedPerDay = round((hotWaterPerPersonDay * personsInHoushold) / tankSize);
	let dailyDemand = round((tanksUsedPerDay * energyToHeatOneTank) / 3600e3);

	let peakPrice = 0.2352;
	let stringVoc = $Voc * panelsPerString;
	let offPeakPrice = 0.0716;
	let peakHours = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0];
	let peakHourCount = peakHours.reduce((accumulator, currentValue) => {
		return accumulator + currentValue;
	}, 0);
	let avgPowerPrice =
		(0.0 + peakHourCount / 24.0) * peakPrice + ((24.0 - peakHourCount) / 24.0) * offPeakPrice;

	let year = new Date().getFullYear();

	let monthData = [];

	let yearlySavings = 0;

	months.forEach((month, index) => {
		let m = {
			month: months[index],
			days: daysInMonth(year, index),
			insolation: 0,
			Edemand: 0,
			Esolar: 0,
			Ecity:0,
			Epercent: 0,
			savings: 0
		};

		monthData.push(m);
	});

	// the `$:` means 're-run whenever these values change'
	// does not listen to changes happening inside components
	$: peakHourCount = peakHours.reduce((accumulator, currentValue) => {
		return accumulator + currentValue;
	}, 0);
	$: avgPowerPrice =
		(peakHourCount / 24.0) * peakPrice + ((24 - peakHourCount) / 24.0) * offPeakPrice;
	$: wireResistance = (selectedWire.r * wireLength) / 1000;
	$: energyToHeatOneTank =
		(heatCapOfWater * tankSize * (hotWaterOutTemp - groundTemp) * 1) / energyFactor;
	$: costToHeatOneTank = round((avgPowerPrice * energyToHeatOneTank) / 3600e3);
	$: tanksUsedPerDay = round((hotWaterPerPersonDay * personsInHoushold) / tankSize);
	$: nominalPower = powerPerPanel * panelsPerString * parallelStrings;
	$: stringVoc = $Voc * panelsPerString;

	$: dailyDemand = round((tanksUsedPerDay * energyToHeatOneTank) / 3600e3);

	let graphUrlBase = '/graph?';
	function makeGraphUrl(startDay = 45) {
		//pick a random day in the season
		let day = Math.floor(Math.random() * 90) + startDay;

		let url = PUBLIC_API_URL + graphUrlBase;

		//pwr should be in kW
		let pwr = nominalPower / 1000.0;
		url =
			url +
			`day=${day}&lat=${$lat}&lng=${$lng}&tilt=${elevation}&azimuth=${azimuth}&pwr=${nominalPower}`;

		const elem = document.getElementById('solarGraph');

		elem?.setAttribute('src', url);
		return url;
	}

	let jsonUrlBase = '/json?';
	function updateMonthlyTable() {
		let url = PUBLIC_API_URL + jsonUrlBase;

		//pwr should be in W
		let pwr = nominalPower / 1000.0;
		url = url + `lat=${$lat}&lng=${$lng}&tilt=${elevation}&azimuth=${azimuth}&pwr=${nominalPower}`;

		let newYearlySavings = 0;
		fetch(url)
			.then((response) => response.json())
			.then((data) => {
				let newMonthData = [];
				months.forEach((month, index) => {
					let m = {
						month: months[index],
						days: daysInMonth(year, index),
						insolation: data.outputs.solrad_monthly[index],
						Edemand: dailyDemand * daysInMonth(year, index),
						Esolar: data.outputs.dc_monthly[index] /1000.0,
						savings: data.outputs.dc_monthly[index]/1000.0 * avgPowerPrice
					};

					// m.Edemand = tokWh(
					// 	m.days * ((hotWaterPerPersonDay * personsInHoushold) / tankSize) * energyToHeatOneTank
					// );
					m.Epercent = clamp((m.Esolar/ m.Edemand)*100.0, 0, 200);

					m.Ecity = clamp(100-m.Epercent,0, 100);

					newYearlySavings = newYearlySavings + m.savings;

					// m.savings = (m.Edemand - m.Ecity) * avgPowerPrice;
					newMonthData.push(m);
				});
				monthData = newMonthData;
				yearlySavings = newYearlySavings;
			});
	}
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
			<figcaption>Simple DC only heating</figcaption>
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
			<Input val={round($lat)} label="Latitude" units="°North" readonly />
			<Input val={round($lng)} label="Longitude" units="°West" readonly />
			<Input bind:val={groundTemp} label="GroundTemp" units="°C" />
			<Input bind:val={offPeakPrice} label="Off Peak Price" units="$/kwh" />
			<Input bind:val={peakPrice} label="Peak Price" units="$/kwh" />

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
				<br />
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
			<Output val={peakHourCount} label="Peak Hour Count" units="H" />
			<Output val={avgPowerPrice} label="Average power price" units="$" />
		</Box>
	</span>
	<span>
		<span>
			<Map />
		</span>
	</span>
</div>

<div class="smol-sidebar">
	<span data-text>
		<h2>Step 2</h2>
		Hot water Usage calculator, use this to estimate how much you are paying to heat water.
	</span>
	<span>
		<Box>
			<h2>Water Heater Specs</h2>
			<Input bind:val={tankSize} label="TankSize" units="liter" />
			<Input bind:val={energyFactor} label="Energy Factor" units="ef" />
			<Input bind:val={hotWaterOutTemp} label="Desired Output Temp" units="°C" />
			<!-- <Input val={50} label="ThermostatSetting" units="°C" /> -->
			<Input bind:val={hotWaterPerPersonDay} label="Hot Water/Person/Day" units="l" />
			<Input bind:val={personsInHoushold} label="Persons In Houshold" units="" />
			<label>
				<input type="checkbox" bind:checked={useMixingValve} />
				Use Thermostatic mixing valve
			</label>
			<hr />
			<Output val={round(energyToHeatOneTank / 3600e3)} label="Energy to heat 1 tank" units="kWh" />
			<Output val={costToHeatOneTank} label="Cost to heat one tank" units="$" />
			<Output val={tanksUsedPerDay} label="Tanks used per day" units="" />
			<Output
				val={round((tanksUsedPerDay * energyToHeatOneTank) / 3600e3)}
				label="Daily Energy Demand"
				units="kWh"
			/>
			<Output
				val={round(tanksUsedPerDay * costToHeatOneTank)}
				label="Hot water cost per day"
				units="$"
			/>
		</Box>
	</span>
	<span>
		<Box>
			<p>
				<b>TankSize</b> Most water heaters are 30-60 gallons in size. A bigger water heater can store
				more energy to bridge cloudy days. For showers, you want water at around 40C, but for washing
				dishes it helps to have it at 50C. If you install a thermostatic mixing valve you can increase
				the effective size of the tank.
			</p>

			<p>
				<b>Energy Factor (ef)</b> this is rating of how efficient your water heater is. Most
				electric heaters have an <b>ef</b> of about 0.9, which means they waste about 10% of the energy
				used. The main losses are standby losses, where heat leaks through the insulation to the air.
			</p>

			<p>
				<b> Daily Energy Demand</b> this is how much power your solar panels will need to make each
				day to completely replace city power. Every day you meet this target you will save the
				amount in <b>Hot water cost per day</b>
			</p>
		</Box>
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
			<h2>Solar Panel Specs</h2>
			<Input bind:val={$Voc} label="Voc" units="V" />
			<Input bind:val={$Vmpp} label="Vmpp" units="V" />
			<Input bind:val={$Impp} label="Impp" units="A" />
			<Input bind:val={panelsPerString} label="Panels per string" units="" />
			<Input bind:val={parallelStrings} label="Parallel strings" units="" />
			<Input bind:val={azimuth} label="Azimuth  180=South" units="°" />
			<Input bind:val={elevation} label="Elevation 0=Flat" units="°" />
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

			<Input bind:val={wireLength} label="Total wire length" units="m" />
			<hr />
			<Output val={stringVoc} label="Voc of full string" units="V" />
			<Output val={$Vmpp * panelsPerString} label="Vmpp of full string" units="V" />
			<Output val={wireResistance} label="Resistance of wire" units="Ω" />
			<Output val={round(nominalPower)} label="Nominal power of string" units="W" />
			<Output val={round($Impp * $Impp * wireResistance)} label="Wire Losses at Mpp" units="W" />
			<Output
				val={round(($Vmpp * panelsPerString) / $Impp)}
				label="Rmpp of full string"
				units="Ω"
			/>
		</Box>
	</span>
	<span>
		<Box>
			<p>
				<b>Vmpp, Impp</b>, find these in the spec sheet of your solar panels. This is the volts and
				amps your panel will make, brand new, clean, in full sun.
			</p>

			<p>
				<b>Voc</b> this is max voltage your panels can make. Everything in your system needs to be
				rated to at least <b>Voc of full string</b> Common solar wire and connectors are rated to 600V.
			</p>

			<p>
				<b>Panels per string, Parallel Strings</b> I kept things simple using a single string of large
				size panels. If are using small panels you may need to run parallel strings to keep the voltage
				down.
			</p>

			<p>
				<b>Rmpp of full string</b> is the resistance value you want for your lower water heater element.
				This number is the ideal impedance for maximum power transfer in full sun.
			</p>
		</Box>
	</span>
</div>


<div class="sim-sidebar">
	<span data-text>
		<h2>Step 4</h2>
		Run simulator. This will feed the simulator with solar panel data you entered above and historical
		weather data for the year 2010.

		<hr />
		<button on:click={() => makeGraphUrl(0)}> Show random day in spring </button>
		<button on:click={() => makeGraphUrl(90)}> Show random day in summer</button>
		<button on:click={() => makeGraphUrl(180)}> Show random day in fall</button>
		<button on:click={() => makeGraphUrl(270)}> Show random day in winter</button>
	</span>
	<span>
		<figure>
			<img alt="SolarSimGraph" src="day67.png" id="solarGraph" />
		</figure>
	</span>
</div>

<!-- <h5>The time is ss {formatter.format($time)}</h5>

<p>
	This page has been open for
	{$elapsed}
	{$elapsed === 1 ? "second" : "seconds"}
</p>

</div> -->

<button on:click={() => updateMonthlyTable()}>Simulate Monthly Generation Totals</button>
<div>
	<!-- <TestSvg/> -->
	<table class="monthTable">
		<tr>
			<th>Month</th>
			<th>Days</th>
			<th>Insolation</th>
			<th>Energy Demand (kWh)</th>
			<th>Solar Energy (kWh)</th>
			<th>Solar Power Used (%)</th>
			<th>City Power Used (%)</th>
			<th>Savings ($)</th>
		</tr>
		{#each monthData as m}
			<tr>
				<td>{m.month}</td>
				<td>{round(m.days)}</td>
				<td>{round(m.insolation)}</td>
				<td>{round(m.Edemand)}</td>
				<td>{round(m.Esolar)}</td>
				<td>{round(m.Epercent)}</td>
				<td>{round(m.Ecity)}</td>
				<td>{round(m.savings)}</td>
			</tr>
		{/each}
	</table>
	<br>
	Total Yearly Power Bill Savings (estimated) = ${round(yearlySavings)}
</div>

<!-- </div> -->

<!-- <Counter /> -->

<style>
	.map {
		height: 300px;
	}
	h1,
	figure,
	p {
		/* text-align: center; */
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
		margin-top: 2rem;
		display: grid;
		grid-template-columns: fit-content(20ch) minmax(min(50vw, 30ch), 45ch) minmax(
				min(50vw, 30ch),
				1fr
			);
	}

	img {
		width: 100%;
		/* max-width: 400px; */
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
