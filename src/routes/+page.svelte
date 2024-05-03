<script>
	import Box from '$lib/components/Box.svelte';
	import Input from '$lib/components/Input.svelte';
	import HousePic from '$lib/components/HousePic.svelte';
	import Output from '$lib/components/Output.svelte';
	import { Vmp, Voc, Imp, Isc, lat, lng } from '$lib/components/stores.js';
	import { round, tokWh, clamp, vpToR } from '$lib/components/util';
	import Map from '$lib/components/Map.svelte';
	import { PUBLIC_API_URL } from '$env/static/public';

	let jsonUrlBase = '/json?';
	let graphUrlBase = '/graph?';

	const formatter = new Intl.DateTimeFormat('en', {
		hour12: true,
		hour: 'numeric',
		minute: '2-digit',
		second: '2-digit'
	});

	// Month in JavaScript is 0-indexed (January is 0, February is 1, etc),
	// but by using 0 as the day it will give us the last day of the prior
	// month. So passing in 1 as the month number will return the last day
	// of January, not February
	function daysInMonth(year, month) {
		return new Date(year, month + 1, 0).getDate();
	}

	let wireGuages = [
		{ id: 1, r: 2.1, text: `8AWG, 2.1 Ω/km` },
		{ id: 2, r: 3.35, text: `10AWG, 3.35 Ω/km` },
		{ id: 3, r: 5.31, text: `12AWG,  5.31  Ω/km` },
		{ id: 4, r: 8.46, text: `14AWG,  8.46  Ω/km` }
	];

	let moduleTypes = [
		{ id: 0, text: `Standard, 19% eff` },
		{ id: 1, text: `Premium, 21% eff` },
		{ id: 2, text: `Thin Film,  18% eff` }
	];

	let selectedWire = wireGuages[1];

	let selectedModuleType = moduleTypes[1];

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
	let panelsPerString = 3;
	let parallelStrings = 1;
	let azimuth = 180;
	let elevation = 40;
	let wireLength = 60;
	let peakPrice = 0.285;
	let offPeakPrice = 0.0792;

	let useMixingValve = 1;
	let mixingValveConstant = 1.5;

	let losses = 12;
	let wireResistance = 2.1;

	let elementR = 0;
	let elementV = 120;
	let elementP = 2000;

	let tankSize = 189; //50 gal
	//heat capacity Cp of water is 4.186kJ/kg-K
	let heatCapOfWater = 4186; // j/l/k
	let hotWaterOutTemp = 40;
	let hotWaterPerPersonDay = 64; // l/person/day
	let personsInHoushold = 4;
	let groundTemp = 5;
	let energyFactor = 0.91;
	let powerPerPanel = $Vmp * $Imp;
	let nominalPower = powerPerPanel * panelsPerString * parallelStrings;
	let energyToHeatOneTank = heatCapOfWater * tankSize * (hotWaterOutTemp - groundTemp);
	let tanksUsedPerDay = round((hotWaterPerPersonDay * personsInHoushold) / tankSize);
	let dailyDemand = round((tanksUsedPerDay * energyToHeatOneTank) / 3600e3);

	let mismatch = 10;
	let Rsource = 1;
	let Rmp = 1;
	let stringVoc = $Voc * panelsPerString;
	let peakHours = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0];
	let peakHourCount = peakHours.reduce((accumulator, currentValue) => {
		return accumulator + currentValue;
	}, 0);
	let avgPowerPrice =
		(0.0 + peakHourCount / 24.0) * peakPrice + ((24.0 - peakHourCount) / 24.0) * offPeakPrice;

	let year = new Date().getFullYear();

	let monthData = [];

	let yearlySavings = 0;
	let dailyEnergyDemand = 0;

	months.forEach((month, index) => {
		let m = {
			month: months[index],
			days: daysInMonth(year, index),
			insolation: 0,
			Edemand: 0,
			Esolar: 0,
			Ecity: 0,
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
	$: powerPerPanel = $Vmp * $Imp;
	$: nominalPower = powerPerPanel * panelsPerString * parallelStrings;
	$: stringVoc = $Voc * panelsPerString;
	$: elementR = vpToR(elementV, elementP);
	$: dailyDemand = round((tanksUsedPerDay * energyToHeatOneTank) / 3600e3);
	$: Rmp = ($Vmp * panelsPerString) / $Imp / parallelStrings;
	$: Rsource = Rmp;
	$: mismatch = Math.abs(100 - ((elementR + wireResistance) / Rsource) * 100.0);
	$: dailyEnergyDemand = (tanksUsedPerDay * energyToHeatOneTank) / 3600e3;

	function makeGraphUrl(startDay = 45, event) {
		//pick a random day in the season
		let day = Math.floor(Math.random() * 90) + startDay;
		let url = PUBLIC_API_URL + graphUrlBase;

		let reEnable = function () {
			// console.log('reEnableing ', event.srcElement);
			event.srcElement.removeAttribute('disabled');
		};
		event.srcElement.setAttribute('disabled', true);

		//pwr should be in kW
		let pwr = nominalPower / 1000.0;
		url =
			url +
			`day=${day}&lat=${$lat}&lng=${$lng}&tilt=${elevation}&azimuth=${azimuth}&pwr=${nominalPower}&losses=${losses}&module_type=${selectedModuleType.id}&liters=${tankSize}&uef=${energyFactor}&startingTemp=${hotWaterOutTemp}`;

		const elem = document.getElementById('solarGraph');
		if (elem) {
			elem.onload = reEnable;
			elem?.setAttribute('src', url);
		}
		return url;
	}

	function updateMonthlyTable(runMonthlySimButton) {
		let url = PUBLIC_API_URL + jsonUrlBase;

		//pwr should be in W
		let pwr = nominalPower / 1000.0;
		url =
			url +
			`lat=${$lat}&lng=${$lng}&tilt=${elevation}&azimuth=${azimuth}&pwr=${nominalPower}&losses=${losses}&module_type=${selectedModuleType.id}`;

		let newYearlySavings = 0;
		let newMonthData = [];

		// console.log(runMonthlySimButton)
		runMonthlySimButton.srcElement.setAttribute('disabled', true);

		fetch(url)
			.then((response) => response.json())
			.then((data) => {
				runMonthlySimButton.srcElement.removeAttribute('disabled');
				months.forEach((month, index) => {
					let m = {
						month: months[index],
						days: daysInMonth(year, index),
						insolation: data.outputs.solrad_monthly[index],
						Edemand: dailyDemand * daysInMonth(year, index),
						Esolar: data.outputs.dc_monthly[index] / 1000.0,
						savings: (data.outputs.dc_monthly[index] / 1000.0) * avgPowerPrice
					};

					m.Epercent = clamp((m.Esolar / m.Edemand) * 100.0, 0, 200);
					m.Ecity = clamp(100 - m.Epercent, 0, 100);
					newYearlySavings = newYearlySavings + m.savings;

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
	<li style="">
		<figure>
			<HousePic style="max-width: 300px;" />
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
		Fill in what you know about your Location and power price.<br /><br /> If you do not know your
		exact power price,
		<a href="https://www.bls.gov/regions/midwest/data/averageenergyprices_selectedareas_table.htm"
			>get an estimate here.</a
		>
		<br /><br /> You can measure your ground water temperature, or estimate it from
		<a href="https://www3.epa.gov/ceampubl/learn2model/part-two/onsite/tempmap.html"
			>this Ground Water Temperature Map.</a
		>
	</span>
	<span>
		<Box>
			<h2>Location Specs</h2>
			<!-- 
				<button on:click="{getCurrentPosition()}">Get Current Position</button>
				<br> 
			-->
			<Input val={round($lat)} label="Latitude" units="°North" readonly />
			<Input val={round($lng)} label="Longitude" units="°East" readonly />
			<Input bind:val={groundTemp} label="GroundTemp" units="°C" />
			<Input bind:val={offPeakPrice} label="Off Peak Price" units="$/kWh" />
			<Input bind:val={peakPrice} label="Peak Price" units="$/kWh" />

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

		<br /> <br />

		The important numbers are <b>Tank Size</b> and <b>Persons In Household</b>

		
		<br /> <br /> If you want to plug in the exact numbers from your water heater, look at the yellow energy star sticker or <a href="https://www.ahridirectory.org/NewSearch?programId=24&searchTypeId=3 ">search here.</a>
		
	</span>
	<span>
		<Box>
			<h2>Water Heater Specs</h2>
			<Input bind:val={personsInHoushold} label="Persons In Houshold" units="" />
			<Input bind:val={hotWaterPerPersonDay} label="Hot Water/Person/Day" units="l" />
			<br />
			<Input bind:val={tankSize} label="Tank Size" units="liter" />
			<Input bind:val={energyFactor} label="Energy Factor" units="UEF" />
			<Input bind:val={hotWaterOutTemp} label="Desired Output Temp" units="°C" />
			<!-- <Input val={50} label="ThermostatSetting" units="°C" /> -->
			<Input bind:val={elementP} label="Element Power Rating" units="W" />
			<Input bind:val={elementV} label="Element Voltage Rating" units="V" />
			<!-- <label>
				<input type="checkbox" bind:checked={useMixingValve} />
				Use Thermostatic mixing valve
			</label> -->
			<hr />
			<Output val={elementR} label="Element Resistance" units="Ω" />
			<Output val={round(energyToHeatOneTank / 3600e3)} label="Energy to heat 1 tank" units="kWh" />
			<Output val={costToHeatOneTank} label="Cost to heat one tank" units="$" />
			<Output val={tanksUsedPerDay} label="Tanks used per day" units="" />
			<Output val={round(dailyEnergyDemand)} label="Daily Energy Demand" units="kWh" />
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

			<p>
				<b> Element Resistance</b> Often water heater elements are rated by Volts and Watts instead
				of Ohms. You can put in <b>Element Power Rating</b> and <b>Element Voltage Rating</b> to calculate
				the Ohms.
			</p>
		</Box>
	</span>
</div>

<div class="smol-sidebar">
	<span data-text>
		<h2>Step 3</h2>
		Impedance matching calculator. Use this to figure out the optimal resistance for your water heater
		element.
		<br /> <br />
		Set <b>Azimuth </b> and <b>Elevation</b> to match the roof where you plan to install the panels.
		The ideal elevation is equal to your Latitude.
	</span>
	<span>
		<Box>
			<h2>Solar Panel Specs</h2>
			<Input bind:val={azimuth} label="Azimuth  180=South" units="°" />
			<Input bind:val={elevation} label="Elevation 0=Flat" units="°" />
			<Input bind:val={panelsPerString} label="Panels per string" units="" />
			<Input bind:val={parallelStrings} label="Parallel strings" units="" />
			<br />
			<label>
				<select bind:value={selectedModuleType}>
					{#each moduleTypes as mt}
						<option value={mt}>
							{mt.text}
						</option>
					{/each}
				</select>
				Module Type
			</label>
			<br />
			<Input bind:val={$Voc} label="Voc" units="V" />
			<Input bind:val={$Vmp} label="Vmp" units="V" />
			<Input bind:val={$Imp} label="Imp" units="A" />
			<Input bind:val={$Isc} label="Isc" units="A" />
			<br />
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
			<Output val={round(stringVoc)} label="Voc of full string" units="V" />
			<Output val={round($Vmp * panelsPerString)} label="Vmp of full string" units="V" />
			<Output val={round($Isc * parallelStrings)} label="Isc of parallel strings" units="A" />
			<Output val={wireResistance} label="Resistance of wire" units="Ω" />
			<Output val={round(nominalPower)} label="Nominal power of string" units="W" />
			<Output val={round($Imp * $Imp * wireResistance)} label="Wire Losses at Mpp" units="W" />
			<Output val={round(Rsource)} label="Source Impedance" units="Ω" />
			<Output val={round(mismatch)} label="Mismatch" units="%" />
		</Box>
	</span>
	<span>
		<Box>
			<p>
				<b>Vmp, Imp</b>, find these in the spec sheet of your solar panels (<a
					href="CS-Datasheet-BiHiKu7_CS7N-MB-AG_v2.4_EN.pdf">example</a
				>) , use the STC values. These are the volts and amps your panel will make with a Solar
				irradiance of 1,000 W/m2, cell temperature of 25°C (77°F).
			</p>

			<p>
				<b>Isc of parallel strings</b> All your wires/connectors/switches/breakers must be rated to at
				least this.
			</p>

			<p>
				<b>Voc</b> this is max voltage your panels can make. Everything in your system needs to be
				rated to at least <b>Voc of full string</b>. Common solar wire and connectors are rated to
				600V.
			</p>

			<p>
				<b>Panels per string, Parallel Strings</b> If possible, use a single series string. If you are
				using small panels it is possible to parallel more then one string but the strings should be
				well matched.
			</p>

			<p>
				<b>Source Impedance</b> is the resistance value you want to match with your lower heating
				element. I suggest a <b>Mismatch</b> below 20% is good enough; the heater elements are not made
				to a very precise resistance anyway.
			</p>
		</Box>
	</span>
</div>

<div class="sim-sidebar">
	<span data-text>
		<h2>Step 4</h2>
		<p>
			Click <b>Simulate Monthly Generation For TMY</b> This will feed the simulator with the solar panel
			data you entered above and Typical Meteorological Year Data (TMY) for your lat/lng. This calls
			a NREL PVwatts API rate limited to 1000 req/day so you may have to try again tomorrow if it is
			not working.
		</p>

		<hr />

		<button on:click={(e) => updateMonthlyTable(e)}>Simulate Monthly Generation For TMY</button>
		<Input
			bind:val={losses}
			label="Losses (dirt, snow, aging, etc.) If your panels are shaded 1/3 of the day, then add 33% to losses."
			units="%"
		/>
		<br />
		<br />
		<div>
			<!-- <TestSvg/> -->
			<table class="monthTable">
				<tr>
					<th>Month</th>
					<th>Days</th>
					<th>Insolation (kWh/m2/day) </th>
					<th>Energy Demand (kWh)</th>
					<th>Solar Generation (kWh<sub>dc</sub>)</th>
					<th>Solar Power Used (%)</th>
					<th>City Power Used (%)</th>
					<th>Solar Power Value ($)</th>
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
				<tfoot>
					<tr>
						<th scope="row" colspan="7">Estimated Value Of Generated Solar Power:</th>
						<th colspan="1">${round(yearlySavings)}</th>
					</tr>
				</tfoot>
			</table>
			<br />
		</div>
		<hr />
		<p>
			This graph uses the TMY simulation data to help you size your array. <span class="blue"
				><b>Mean Tank Temperature</b></span
			> assumes fully mixed water. On most days, your tank will not get as hot as the graph shows because
			you will be using hot water.
		</p>
		<p>
			Click a <b>Graph random day</b> button a few times until you find a nice sunny day (lots of
			<b>Solar Radiation</b>).
		</p>
		<p>
			If your <b>Net Thermal Energy Gain</b> is more than
			<b>Daily Energy Demand ({round(dailyEnergyDemand)}kWh)</b>
			on a sunny day, then your solar array is oversized. If the
			<span class="blue"><b>Tank Temperature</b></span>
			is going over the
			<span class="red"><b>Mixing Valve Limit</b></span>
			and you still are making less then 2/3 of your <b>Daily Energy Demand</b>, then your tank is
			undersized.
		</p>
		<div class="smol-css-grid">
			<button on:click={(e) => makeGraphUrl(0, e)}> Graph random day in Q1</button>
			<button on:click={(e) => makeGraphUrl(90, e)}> Graph random day in Q2</button>
			<button on:click={(e) => makeGraphUrl(180, e)}> Graph random day in Q3</button>
			<button on:click={(e) => makeGraphUrl(270, e)}> Graph random day in Q4</button>
		</div>
	</span>
	<span>
		<figure>
			<img alt="SolarSimGraph" src="sampleGraph.png" id="solarGraph" />
		</figure>
	</span>
	<p>Graph Assumptions:</p>

	<ul>
		<li>No hot water withdraws (aka nobody is home)</li>
		<li>
			On most days, the water will not get as hot as the graph shows because you will be using hot
			water.
		</li>
		<li>The tank water starts at your <b>Desired Output Temp</b> ({hotWaterOutTemp}℃)</li>
		<li><span class="blue"><b>Mean Tank Temperature</b></span> assumes fully mixed water.</li>
		<li>
			In the real world the hottest water moves to the top of the tank and the coldest to the
			bottom.
		</li>
		<li>
			The <span class="green"><b>Net Water Heating Power</b></span> will be negative when there is
			no sun. These are the standby losses estimated from your UEF ({energyFactor})
		</li>
		<li>The top element is disconnected (no city power)</li>
		<li>No thermostat is installed on the bottom element.</li>
		<li>
			If there was a thermostat the <span class="blue"><b>Mean Tank Temperature</b></span> would not
			exceed the <span class="red"><b>Mixing Valve Limit</b> </span>
		</li>
	</ul>
</div>

<!-- <h5>The time is ss {formatter.format($time)}</h5>

<p>
	This page has been open for
	{$elapsed}
	{$elapsed === 1 ? "second" : "seconds"}
</p>

</div> -->

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
	th {
		border-bottom: 1px solid #000;
		min-width: 8em;
	}
	tr:nth-child(even) {
		background-color: #d6eeee;
	}

	.smol-css-grid li {
		list-style: none;
		margin: 0;
	}

	.blue {
		color: blue;
	}

	.red {
		color: red;
	}

	.green {
		color: green;
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
