<script lang="ts">
	import Box from '$lib/components/Box.svelte';
	import Input from '$lib/components/Input.svelte';
	import HousePic from '$lib/components/HousePic.svelte';
	import Output from '$lib/components/Output.svelte';
	import InputInt from '$lib/components/InputInt.svelte';
	import LeafletMap from '$lib/components/LeafletMap.svelte';
	import AutoComplete from 'simple-svelte-autocomplete';
	import { read, utils, writeFileXLSX } from 'xlsx';
	import { Vmp, Voc, Imp, Isc, lat, lng } from '$lib/components/stores.js';
	import {
		round,
		clamp,
		months,
		indexToTime,
		daysInMonth,
		toGal,
		heatCapOfWater,
		wireGuages,
		moduleTypes,
		elements,
		getMonthData,
		year
	} from '$lib/components/util';
	import { PUBLIC_API_URL } from '$env/static/public';
	import { onMount } from 'svelte';
	let jsonUrlBase = '/json?';
	let graphUrlBase = '/graph?';


	function makeGraphUrl(startDay = 45, event:any) {
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

	/**
	 * @param {any} runMonthlySimButton
	 */
	function updateMonthlyTable(runMonthlySimButton:any) {
		let url = PUBLIC_API_URL + jsonUrlBase;

		//pwr should be in W
		let pwr = nominalPower / 1000.0;
		url =
			url +
			`lat=${$lat}&lng=${$lng}&tilt=${elevation}&azimuth=${azimuth}&pwr=${nominalPower}&losses=${losses}&module_type=${selectedModuleType.id}`;

		let newYearlySavings = 0;

		let newMonthData: {
			month: string;
			days: number;
			insolation: any;
			Edemand: number;
			Esolar: number;
			savings: number;
			Epercent: number;
			Ecity: number;
		}[] = [];

		// console.log(runMonthlySimButton)
		runMonthlySimButton.srcElement.setAttribute('disabled', true);

		document.getElementById('apiWarn')?.setAttribute('style', '');

		fetch(url)
			.then((response) => response.json())
			.then((data) => {
				runMonthlySimButton.srcElement.removeAttribute('disabled');
				document.getElementById('apiWarn')?.setAttribute('style', 'display:none;');
				months.forEach((month, index) => {
					let m = {
						month: months[index],
						days: daysInMonth(year, index),
						insolation: data.outputs.solrad_monthly[index],
						Edemand: dailyDemand * daysInMonth(year, index),
						Esolar: data.outputs.dc_monthly[index] / 1000.0,
						savings: (data.outputs.dc_monthly[index] / 1000.0) * avgPowerPrice,
						Epercent: 0,
						Ecity: 0
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

	let modules: any = [];
	let selectedModule: any = null;

	/* Fetch and update the list of modules once */
	async function loadModules() {
		const f = await (await fetch('CECModules2023-11-17combined.csv')).arrayBuffer();
		const wb = read(f); // parse the array buffer
		modules = utils.sheet_to_json(wb.Sheets[wb.SheetNames[0]]);
		console.log('loaded modules ', modules.length);
		// return modules;
	}

	function onModuleChange(newModule: any) {
		if(newModule)
		{
			$Vmp = newModule.V_mp_ref;
			$Imp = newModule.I_mp_ref;
			$Voc = newModule.V_oc_ref;
			$Isc = newModule.I_sc_ref;
			console.log('moduleChanged!', newModule);
		}
	}

	async function searchModule(keyword:string, nb_items_max:number) {
		if(modules.length < 1)
			await loadModules();
		let query = keyword.toLowerCase();
		return modules.filter((el:any) => el['Name'].toLowerCase().includes(query)).slice(0, nb_items_max);
	}

	let selectedWire = wireGuages[1];
	let selectedModuleType = moduleTypes[1];
	let panelsPerString = 3;
	let parallelStrings = 1;
	let azimuth = 180;
	let elevation = 40;
	let wireLength = 60;
	let wireResistance = 2.1;
	let peakPrice = 0.285;
	let offPeakPrice = 0.0792;
	let useMPPT = 1;
	let losses = 12;

	let selectedElement = elements[0];
	let elementR = 0;
	// $: elementR = vpToR(elementV, elementP);
	// let elementV = 120;
	// let elementP = 2000;

	let tankSize = 189; //50 gal
	let hotWaterOutTemp = 40;
	let hotWaterPerPersonDay = 64; // l/person/day
	let personsInHoushold = 4;
	let groundTemp = 5;
	let energyFactor = 0.91;
	let powerPerPanel = 0;
	let nominalPower = 0;
	let 	energyToHeatOneTank = 0;
	let tanksUsedPerDay = 0;
	let dailyDemand = 0;

	let mismatch = 10;
	let Rsource = 1;
	let Rmp = 1;
	let stringVoc = $Voc * panelsPerString;
	let peakHours = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0];
	let peakHourCount = 0;
	let avgPowerPrice = 0;

	let yearlySavings = 0;
	let dailyEnergyDemand = 0;

	let monthData = getMonthData();

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
	$: dailyDemand = round((tanksUsedPerDay * energyToHeatOneTank) / 3600e3);
	$: Rmp = ($Vmp * panelsPerString) / $Imp / parallelStrings;
	$: Rsource = Rmp;
	$: mismatch = Math.abs(100 - ((elementR + wireResistance) / Rsource) * 100.0);
	$: dailyEnergyDemand = (tanksUsedPerDay * energyToHeatOneTank) / 3600e3;
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
			<HousePic style="max-width: 350px;" />
			<figcaption>Simple DC only heating (mouseover for labels)</figcaption>
		</figure>
	</li>

	<li style="max-width: 300px;">
		<figure>
			<img alt="SolarShed" src="solarShed/firstPower.jpg" />
			<figcaption>Free power!</figcaption>
		</figure>
	</li>
</ul>
<p>
	At 85°C, you can cram around 10kWh of solar energy into an average sized water heater. At PG&E
	power prices, thats worth about $5/day. A thermostatic mixing valve is used to bring the water
	down to a safe temperature before use. Because this is a DC system, not connected to the grid, few
	or no permits are required. You can do the install in a weekend and have free hot water monday
	afternoon. This tool will help you design an optimal system for your home.
</p>

<div class="smol-sidebar">
	<span data-text>
		<h2>Step 1</h2>
		Fill in what you know about your Location and power price.<br /><br /> If you do not know your
		exact power price,
		<a
			target="_blank"
			href="https://www.bls.gov/regions/midwest/data/averageenergyprices_selectedareas_table.htm"
			>get an estimate here.</a
		>
		<br /><br /> You can measure your ground water temperature, or estimate it from
		<a target="_blank" href="https://www3.epa.gov/ceampubl/learn2model/part-two/onsite/tempmap.html"
			>this Ground Water Temperature Map.</a
		>
	</span>
	<span>
		<Box>
			<h2>Location Specs</h2>
			<Input val={round($lat)} label="Latitude" units="°North" readonly />
			<Input val={round($lng)} label="Longitude" units="°East" readonly />
			<InputInt bind:val={groundTemp} label="GroundTemp" units="°C" min="1" max="30" />
			<Input bind:val={offPeakPrice} label="Off Peak Price" units="$/kWh" />
			<Input bind:val={peakPrice} label="Peak Price" units="$/kWh" />

			<label>
				PeakHours: <br />
				{#each Array(12) as _, i}
					<input type="checkbox" bind:checked={peakHours[i]} title={indexToTime(i)} />
				{/each}
				<br />
				{#each Array(12) as _, i}
					<input type="checkbox" bind:checked={peakHours[i + 12]} title={indexToTime(i + 12)} />
				{/each}
			</label>
			<hr />
			<Output val={peakHourCount} label="Peak Hour Count" units="H" />
			<Output val={avgPowerPrice} label="Average power price" units="$" />
		</Box>
	</span>
	<span>
		<span>
			<LeafletMap />
		</span>
	</span>
</div>

<div class="smol-sidebar">
	<span data-text>
		<h2>Step 2</h2>
		Hot water Usage calculator, use this to estimate how much you are paying to heat water.

		<br /> <br />

		The important numbers are <b>Tank Size</b> and <b>Persons In Household</b>

		<br /> <br /> If you want to plug in the exact numbers from your water heater, look at the
		yellow energy star sticker or
		<a target="_blank" href="https://www.ahridirectory.org/NewSearch?programId=24&searchTypeId=3 "
			>search here.</a
		>
	</span>
	<span>
		<Box>
			<h2>Water Heater Specs</h2>
			<InputInt
				bind:val={personsInHoushold}
				label="Persons In Houshold"
				units=""
				min="1"
				max="20"
			/>
			<InputInt
				bind:val={hotWaterPerPersonDay}
				label="Hot Water/Person/Day"
				units="l"
				min="10"
				max="100"
			/>
			<br />
			<InputInt
				bind:val={tankSize}
				label="Tank Size ≈ {toGal(tankSize)}gal"
				units="l"
				min="50"
				max="500"
			/>
			<Input bind:val={energyFactor} label="Energy Factor" units="UEF" />
			<InputInt
				bind:val={hotWaterOutTemp}
				label="Desired Output Temp"
				units="°C"
				min="35"
				max="55"
			/>
			<!-- <Input val={50} label="ThermostatSetting" units="°C" /> -->
			<br />

			<AutoComplete
				items={elements}
				bind:selectedItem={selectedElement}
				bind:value={elementR}
				labelFieldName="label"
				valueFieldName="resistance"
				noInputStyles={false}
				hideArrow={false}
				create={false}
				readonly={true}
				className="elementInput"
			/>
			Element
			<!-- <InputInt bind:val={elementP} label="Element Power Rating" units="W" min="100" max="10000" />
			<InputInt bind:val={elementV} label="Element Voltage Rating" units="V" min="12" max="600" /> -->
			<br />
			<label>
				<input type="checkbox" bind:checked={useMPPT} />
				Use MPPT Thermostat
			</label>
			<hr />
			<Output val={round(energyToHeatOneTank / 3600e3)} label="Energy to heat 1 tank" units="kWh" />
			<Output val={costToHeatOneTank} label="Cost to heat one tank" units="$" />
			<Output val={tanksUsedPerDay} label="Tanks used per day" units="" />
			<Output val={round(dailyEnergyDemand)} label="Daily Energy Demand" units="kWh" />
			<Output
				val={round(tanksUsedPerDay * costToHeatOneTank)}
				label="Hot water cost per day"
				units="$"
			/>
			<br />
			<Output val={elementR} label="Element Resistance" units="Ω" />
		</Box>
	</span>
	<span>
		<Box>
			<p>
				<b>TankSize</b> Most water heaters are 30-80 gallons (113-226 liters) in size. A bigger water
				heater can store more energy to bridge cloudy days.
			</p>
			<p>
				<b>Desired Output Temp</b> 40°C(104°F) is good enough for showers, but for washing dishes it
				helps to have it at 50°C(122°F). The thermostatic mixing valve and the top element (city power)
				thermostat should be set to this temperature.
			</p>
			<p>
				<b>Energy Factor (UEF)</b> this is rating of how efficient your water heater is. Most
				electric heaters have an <b>UEF</b> of about 0.9, which means they waste about 10% of the energy
				used. The main losses are standby losses, where heat leaks through the insulation.
			</p>

			<p>
				<b> Daily Energy Demand</b> this is how much power your solar panels will need to make each
				day to completely replace city power. Every day you meet this target you will save the
				amount in <b>Hot water cost per day</b>
			</p>

			<p>
				<b> Element</b>  power rating must exceed <b>Nominal Array Power</b>.  The voltage rating is more flexible, you can go over this a bit.
			</p>
		</Box>
	</span>
</div>
<div class="smol-sidebar">
	<span data-text>
		<h2>Step 3</h2>
		Set<b>Azimuth </b> and <b>Elevation</b> to match the roof where you plan to install the panels.
		The ideal elevation is equal to your Latitude.
		<br /> <br />
		Put in the rest of the specs for the solar panels you want to Simulate, or use <b>Search for Panel by PN</b>
		<br /> <br />
		The bottom of this section will show you the source impedance you want to match with your water heater
		element.
	</span>
	<span>
		<Box>
			<h2>Solar Panel Specs</h2>
			<InputInt bind:val={azimuth} label="Azimuth  180=South" units="°" min="0" max="359" />
			<InputInt bind:val={elevation} label="Elevation 0=Flat" units="°" min="0" max="90" />
			<InputInt bind:val={panelsPerString} label="Panels per string" units="" min="1" max="100" />
			<InputInt bind:val={parallelStrings} label="Parallel strings" units="" min="1" max="10" />
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
			<Input bind:val={$Isc} label="Isc" units="A" />
			<Input bind:val={$Vmp} label="Vmp" units="V" />
			<Input bind:val={$Imp} label="Imp" units="A" />
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

			<InputInt bind:val={wireLength} label="Total wire length" units="m" min="3" max="300" />

			<hr />
			<Output val={round(stringVoc)} label="Voc of full string" units="V" />
			<Output val={round($Vmp * panelsPerString)} label="Vmp of full string" units="V" />
			<Output val={round($Isc * parallelStrings)} label="Isc of parallel strings" units="A" />
			<Output val={round(nominalPower)} label="Nominal Array Power" units="W" />
			<br />
			<Output val={round(Rsource)} label="Source Impedance" units="Ω" />
			<Output val={round(mismatch)} label="Mismatch" units="%" />
			<br />
			<Output val={wireResistance} label="Resistance of wire" units="Ω" />
			<Output val={round($Imp * $Imp * wireResistance)} label="Wire Losses at Mpp" units="W" />
		</Box>
	</span>
	<span>
		<Box>
			<p>
			<b>Search for Panel by PN:</b><br>
			<AutoComplete
			searchFunction={searchModule}
			bind:selectedItem={selectedModule}
			onChange={onModuleChange}
			maxItemsToShowInList={15}
			minCharactersToSearch={3}
			delay={200}
			localFiltering={false}
			localSorting={true}
			labelFieldName="Name"
			valueFieldName="__rowNum__"
			create={false}
		/>
	</p>
			<p>
				<b>Vmp, Imp</b>, find these in the spec sheet of your solar panels (<a
					target="_blank"
					href="CS-Datasheet-BiHiKu7_CS7N-MB-AG_v2.4_EN.pdf">example</a
				>) , use the STC values. These are the volts and amps your panel will make with a Solar
				irradiance of 1,000 W/m<sup>2</sup>, cell temperature of 25°C (77°F).
			</p>

			<p>
				<b>Isc of parallel strings</b> This is the max current your panels can make when shorted. All
				your wires/connectors/switches/breakers must be rated to at least this.
			</p>

			<p>
				<b>Voc</b> this is max open circuit voltage your panels can make. Everything in your system
				needs to be rated to at least <b>Voc of full string</b>. Common solar wire and connectors
				are rated to 600V.
			</p>

			<p>
				<b>Panels per string, Parallel Strings</b> If possible, use a single series string. If you are
				using small panels you can parallel more then one string but the strings should be well matched.
			</p>

			<p>
				<b>Source Impedance</b> is the resistance value you want to match with your lower heating
				element. I suggest a <b>Mismatch</b> below 20% is good enough; the heater elements are not made
				to a very precise resistance anyway.
			</p>

			<p>
				<b>Wire Gauge</b> most solar installs use 10AWG 600V wire. You can reduce your losses a bit if
				you use 8AWG wire.
			</p>
		</Box>
	</span>
</div>

<div class="sim-sidebar">
	<span data-text>
		<h2>Step 4</h2>
		<p>
			Click <b>Simulate Monthly Generation</b> This will feed the simulator with the solar panel data
			you entered above and Typical Meteorological Year Data (TMY) 2020 for your lat/lng.
		</p>
		<p>
			If you are going much over 100% for <b>Solar Power Used</b> your array is bigger then it needs
			to be.
		</p>
		<hr />
		<button on:click={(e) => updateMonthlyTable(e)}>Simulate Monthly Generation</button> with
		<InputInt
			bind:val={losses}
			label="Losses (dirt, snow, aging, etc.) If your panels are shaded 1/3 of the day, then add 33% to losses."
			units="%"
			min="1"
			max="99"
		/>
		<br />
		<p id="apiWarn" style="display: none;">
			This calls a NREL PVwatts API rate limited to 1000 req/day so you may have to try again
			tomorrow if it is not working.
		</p>
		<div>
			<!-- <TestSvg/> -->
			<table class="monthTable">
				<tr>
					<th>Month</th>
					<th>Days</th>
					<th>Insolation (kWh/m<sup>2</sup>/day) </th>
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
			> assumes fully mixed water. On most days, the tank will not get as hot as the graph shows because
			you will be withdrawing hot water from the top, which adds cold water to the bottom.
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
	<br />
	<span>
		<figure>
			<img alt="SolarSimGraph" src="sampleGraph.png" id="solarGraph" style="padding-top:10px;" />
		</figure>
	</span>
	<p>Graph Assumptions:</p>

	<ul>
		<li>No hot water withdraws (aka nobody is home)</li>
		<li>The tank water starts at your <b>Desired Output Temp</b> ({hotWaterOutTemp}℃)</li>
		<li>
			<span class="blue"><b>Mean Tank Temperature</b></span> assumes fully mixed water. In the real world
			the hottest water moves to the top of the tank and the coldest to the bottom.
		</li>
		<li>
			The <span class="green"><b>Net Water Heating Power</b></span> will be negative when there is
			no sun. These are the standby losses estimated from your UEF ({energyFactor})
		</li>
		<li>The top element is disconnected (no city power).</li>
		<li>
			No thermostat is installed on the bottom element. If there was a thermostat the <span
				class="blue"><b>Mean Tank Temperature</b></span
			>
			would not exceed the <span class="red"><b>Mixing Valve Limit</b> </span>
		</li>
	</ul>
</div>

<style>
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
	input:read-only {
		background-color: grey;
	}

	input .elementInput {
		padding-top: 2px;
		padding-bottom: 2px;
	}
</style>
