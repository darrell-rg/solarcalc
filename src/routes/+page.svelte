<script lang="ts">
	import Box from '$lib/components/Box.svelte';
	import Input from '$lib/components/Input.svelte';
	import HousePic from '$lib/components/HousePic.svelte';
	import Output from '$lib/components/Output.svelte';
	import InputInt from '$lib/components/InputInt.svelte';
	import LeafletMap from '$lib/components/LeafletMap.svelte';
	import AutoComplete from 'simple-svelte-autocomplete';
	import { pv } from '$lib/components/stores.ts';
	import {
		round,
		clamp,
		months,
		indexToTime,
		daysInMonth,
		toGal,
		heatCapOfWater,
		wireGauges,
		moduleTypes,
		elements,
		getMonthData,
		year,
		defaultPrefs,
		CToF,

		degreesToCompass,

		degreesToRoofPitch



	} from '$lib/components/util';
	import { PUBLIC_API_URL } from '$env/static/public';
	import Spinner from '$lib/components/Spinner.svelte';
	let jsonUrlBase = '/json?';
	let graphUrlBase = '/graph?';
	// cloudflare pages will compress .txt but not .csv, so we add a .txt to the file name
	let cecModuleUrl = 'CECModules201920202023.csv.txt';

	/* Fetch and update the list of modules once */
	async function loadModules() {
		// dynamic import for this large js lib
		const xlsx = (await import('xlsx')).default;
		const f = await (await fetch(cecModuleUrl)).arrayBuffer();

		const wb = xlsx.read(f); // parse the array buffer
		modules = xlsx.utils.sheet_to_json(wb.Sheets[wb.SheetNames[0]]);
		console.log('loaded modules ', modules.length);
		// return modules;
	}

	function makeGraphUrl(startDay = 45, event: any) {
		//pick a random day in the season
		let day = Math.floor(Math.random() * 90) + startDay;
		let url = PUBLIC_API_URL + graphUrlBase;
		graphLoading = true;

		let reEnable = function () {
			// console.log('reEnableing ', event.srcElement);
			graphLoading = false;
			event.srcElement.removeAttribute('disabled');
		};
		event.srcElement.setAttribute('disabled', true);

		let Re = elementR * -1;
		if ($pv.nonMpptGraph) Re = elementR;

		//pwr should be in kW
		let pwr = nominalPower / 1000.0;
		url =
			url +
			`day=${day}&lat=${$pv.lat}&lng=${$pv.lng}&tilt=${$pv.elevation}&azimuth=${$pv.azimuth}&pwr=${nominalPower}&losses=${$pv.losses}&module_type=${$pv.selectedModuleTypeId}&liters=${$pv.tankSize}&uef=${$pv.energyFactor}&startingTemp=${$pv.hotWaterOutTemp}&Rw=${wireResistance}&Re=${Re}&pps=${$pv.panelsPerString}&ps=${$pv.parallelStrings}&MN=${$pv.selectedModuleName}`;

		const elem = document.getElementById('solarGraph');
		if (elem) {
			elem.onload = reEnable;
			elem?.setAttribute('src', url);
		}
		return url;
	}

	function updateMonthlyTable(runMonthlySimButton: any) {
		let url = PUBLIC_API_URL + jsonUrlBase;

		let Re = elementR * -1;

		//pwr should be in W
		let pwr = nominalPower / 1000.0;
		url =
			url +
			`lat=${$pv.lat}&lng=${$pv.lng}&tilt=${$pv.elevation}&azimuth=${$pv.azimuth}&pwr=${nominalPower}&losses=${$pv.losses}&module_type=${$pv.selectedModuleTypeId}&liters=${$pv.tankSize}&uef=${$pv.energyFactor}&startingTemp=${$pv.hotWaterOutTemp}&Rw=${wireResistance}&Re=${Re}&pps=${$pv.panelsPerString}&ps=${$pv.parallelStrings}&MN=${$pv.selectedModuleName}`;

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
		monthTableLoading = true;

		document.getElementById('apiWarn')?.setAttribute('style', '');

		fetch(url)
			.then((response) => response.json())
			.then((data) => {
				runMonthlySimButton.srcElement.removeAttribute('disabled');
				document.getElementById('apiWarn')?.setAttribute('style', 'display:none;');
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
				monthTableLoading = false;
			});
	}

	function onModuleChange(newModule: any) {
		if (newModule) {
			$pv.Vmp = newModule.V_mp_ref;
			$pv.Imp = newModule.I_mp_ref;
			$pv.Voc = newModule.V_oc_ref;
			$pv.Isc = newModule.I_sc_ref;
			$pv.selectedModuleName = newModule.Name;
			$pv.allowNonMpptt = true;
			console.log('moduleChanged!', newModule);
		}
	}

	function resetToDefaults() {
		// console.log("resetting to",defaultPrefs);
		$pv = JSON.parse(JSON.stringify(defaultPrefs));
		window.location.reload();
		// const jsonState = JSON.stringify(defaultPrefs);
		// localStorage.setItem('solarPrefs', jsonState);
	}

	async function searchModule(keyword: string, nb_items_max: number) {
		if (modules.length < 1) await loadModules();
		// make searches like "Jinko 200" work
		let query = new RegExp(keyword.toLowerCase().replace(' ', '.*'));
		return modules.filter((el: any) => query.test(el['Name'].toLowerCase())).slice(0, nb_items_max);
	}

	// all user configurable values are stored in $pv, except these two objects
	// hack to fix https://stackoverflow.com/questions/70331078/svelte-pre-selecting-a-select-input-option-when-using-objects-as-values
	let selectedWire: any = wireGauges[$pv.selectedWireId];
	$: selectedWire = wireGauges.find((o: any) => o.id === $pv.selectedWireId);
	let selectedModuleType: any = moduleTypes[$pv.selectedModuleTypeId];
	$: selectedModuleType = moduleTypes.find((o: any) => o.id === $pv.selectedModuleTypeId);

	// these two are generated/downloaded
	let monthData = getMonthData();
	let modules: any = [];
	let graphLoading = false;
	let monthTableLoading = false;

	//all values below this line are calculated
	let powerPerPanel = 0;
	let nominalPower = 0;
	let energyToHeatOneTank = 0;
	let tanksUsedPerDay = 0;
	let dailyDemand = 0;
	let elementR = 0;
	let mismatch = 10;
	let Rsource = 1;
	let Rmp = 1;
	let peakHourCount = 0;
	let avgPowerPrice = 0;
	let wireResistance = 2.1;
	let yearlySavings = 0;
	let dailyEnergyDemand = 0;
	let stringVoc = 0;
	let wireLosses = 0;

	// the `$:` means 're-run whenever these values change'
	// does not listen to changes happening inside components
	$: peakHourCount = $pv.peakHours.reduce((accumulator: number, currentValue: number) => {
		return accumulator + currentValue;
	}, 0);
	$: avgPowerPrice =
		(peakHourCount / 24.0) * $pv.peakPrice + ((24 - peakHourCount) / 24.0) * $pv.offPeakPrice;
	$: wireResistance = (selectedWire.r * $pv.wireLength) / 1000;
	$: energyToHeatOneTank =
		(heatCapOfWater * $pv.tankSize * ($pv.hotWaterOutTemp - $pv.groundTemp) * 1) / $pv.energyFactor;
	$: costToHeatOneTank = round((avgPowerPrice * energyToHeatOneTank) / 3600e3);
	$: tanksUsedPerDay = round(($pv.hotWaterPerPersonDay * $pv.personsInHoushold) / $pv.tankSize);
	$: powerPerPanel = $pv.Vmp * $pv.Imp;
	$: nominalPower = powerPerPanel * $pv.panelsPerString * $pv.parallelStrings;
	$: stringVoc = $pv.Voc * $pv.panelsPerString;
	$: dailyDemand = round((tanksUsedPerDay * energyToHeatOneTank) / 3600e3);
	$: Rmp = ($pv.Vmp * $pv.panelsPerString) / $pv.Imp / $pv.parallelStrings;
	$: Rsource = Rmp;
	$: mismatch = Math.abs(100 - ((elementR + wireResistance) / Rsource) * 100.0);
	$: dailyEnergyDemand = (tanksUsedPerDay * energyToHeatOneTank) / 3600e3;
	$: wireLosses = $pv.Imp * $pv.parallelStrings * ($pv.Imp * $pv.parallelStrings) * wireResistance;
</script>

<svelte:head>
	<title>PVH2O</title>
</svelte:head>
<div class="container">
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
		down to a safe temperature before use. Because this is a DC system, not connected to the grid,
		few or no permits are required. You can do the install in a weekend and have free hot water
		monday afternoon. This tool will help you design an optimal system for your home.
	</p>

	<div class="smol-sidebar">
		<span data-text>
			<h2>Step 1: Location</h2>
			Fill in what you know about your location and power price.<br /><br /> If you do not know your
			exact power price,
			<a
				target="_blank"
				href="https://www.bls.gov/regions/midwest/data/averageenergyprices_selectedareas_table.htm"
				>get an estimate here.</a
			>
			<br /><br /> You can measure your ground water temperature with a thermometer, or estimate it from the red isotherm lines on the 
			<a
				target="_blank"
				href="https://www3.epa.gov/ceampubl/learn2model/part-two/onsite/tempmap.html"
				>map.</a
			>
			<br />
			<br />
			<button on:click={(e) => resetToDefaults()}> Reset All To Defaults</button>
		</span>
		<span>
			<Box>
				<Input val={round($pv.lat)} label="Latitude" units="°North" readonly />
				<Input val={round($pv.lng)} label="Longitude" units="°East" readonly />
				<InputInt bind:val={$pv.groundTemp} label="Ground Water Temp" units="°C" min="1" max="30" />
				<Input bind:val={$pv.offPeakPrice} label="Off Peak Price" units="$/kWh" />
				<Input bind:val={$pv.peakPrice} label="Peak Price" units="$/kWh" />

				<label>
					Peak Hours: <br />
					{#each Array(12) as _, i}
						<input type="checkbox" bind:checked={$pv.peakHours[i]} title={indexToTime(i)} />
					{/each}
					<br />
					{#each Array(12) as _, i}
						<input
							type="checkbox"
							bind:checked={$pv.peakHours[i + 12]}
							title={indexToTime(i + 12)}
						/>
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
			<h2>Step 2:Water Heater</h2>
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
				<!-- <h2>Water Heater Specs</h2> -->
				<InputInt
					bind:val={$pv.personsInHoushold}
					label="Persons in Household"
					units=""
					min="1"
					max="20"
				/>
				<InputInt
					bind:val={$pv.hotWaterPerPersonDay}
					label="Hot Water/Person/Day"
					units="l"
					min="10"
					max="100"
				/>
				<br />
				<InputInt
					bind:val={$pv.tankSize}
					label="Tank Size ≈ {toGal($pv.tankSize)}gal"
					units="l"
					min="50"
					max="500"
				/>
				<Input bind:val={$pv.energyFactor} label="Energy Factor" units="EF" />
				<InputInt
					bind:val={$pv.hotWaterOutTemp}
					label="Desired Output Temp  ≈ {CToF($pv.hotWaterOutTemp)}°F"
					units="°C"
					min="35"
					max="55"
				/>
				<!-- <Input val={50} label="ThermostatSetting" units="°C" /> -->
				<br />

				<AutoComplete
					items={elements}
					bind:selectedItem={$pv.selectedElement}
					bind:value={elementR}
					labelFieldName="label"
					valueFieldName="resistance"
					noInputStyles={false}
					hideArrow={true}
					create={false}
					readonly={false}
					inputClassName="elementInput"
					inputId="elementInput"
				/>

				<label for="elementInput" class="elementInputLabel">Element</label>
				<!-- <InputInt bind:val={elementP} label="Element Power Rating" units="W" min="100" max="10000" />
			<InputInt bind:val={elementV} label="Element Voltage Rating" units="V" min="12" max="600" /> -->
				<hr />
				<Output
					val={round(energyToHeatOneTank / 3600e3)}
					label="Energy to heat 1 tank"
					units="kWh"
				/>
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
			<Box style="padding-top:0px; padding-bottom:0px;">
				<p>
					<b>Tank Size</b> Most water heaters are 30-80 gallons (113-226 liters) in size. A bigger water
					heater can store more energy to bridge cloudy days.
				</p>
				<p>
					<b>Desired Output Temp</b> 40°C is good enough for showers, but for washing dishes it
					helps to have it at 50°C. The thermostatic mixing valve and the top element (city power)
					thermostat should be set to this temperature.
				</p>
				<p>
					<b>Energy Factor (EF/UEF)</b> this is rating of how efficient your water heater is. Most
					electric heaters have an <b>EF</b> of about 0.9, which means they waste about 10% of the energy
					used. The primary standby loss comes from heat leaking through the tank's insulation. 
					The second largest source of loss is pipe losses. 
				</p>

				<p>
					<b> Daily Energy Demand</b> this is how much power your solar panels will need to make
					each day to completely replace city power. Every day you meet this target you will save
					the amount in <b>Hot water cost per day</b>
				</p>

				<p>
					Select a bottom water heater <b>Element</b> to match <b>Source Impedance</b> and exceed <b>Nominal Array Power</b>. 
				</p>
			</Box>
		</span>
	</div>
	<div class="smol-sidebar">
		<span data-text>
			<h2>Step 3: Solar Panels</h2>
			Set <b>Azimuth</b> and <b>Elevation</b> to match the roof where you plan to install the panels.
			The ideal Elevation is equal to your Latitude.
			<br /> <br />
			Put in the rest of the specs for the solar panels you want to Simulate, or use
			<b>Search for Panel by PN</b>
			<br /> <br />
			The bottom of this section will show you the source impedance you want to match with your water
			heater element.
		</span>
		<span>
			<Box>
				<!-- <h2>Solar Panel Specs</h2> -->
				<InputInt bind:val={$pv.azimuth} label="Azimuth ≈ {degreesToCompass($pv.azimuth)}" units="°" min="0" max="359" />
				<InputInt bind:val={$pv.elevation} label="Elevation ≈ {degreesToRoofPitch($pv.elevation)} Pitch" units="°" min="0" max="90" />
				<InputInt
					bind:val={$pv.panelsPerString}
					label="Panels per string"
					units=""
					min="1"
					max="100"
				/>
				<InputInt
					bind:val={$pv.parallelStrings}
					label="Parallel strings"
					units=""
					min="1"
					max="10"
					readonly={false}
				/>
				<br />
				<label>
					<select bind:value={$pv.selectedModuleTypeId}>
						{#each moduleTypes as mt}
							<option value={mt.id}>
								{mt.text}
							</option>
						{/each}
					</select>
					Module Type
				</label>
				<br />
				<Input bind:val={$pv.Voc} label="Voc" units="V" />
				<Input bind:val={$pv.Isc} label="Isc" units="A" />
				<Input bind:val={$pv.Vmp} label="Vmp" units="V" />
				<Input bind:val={$pv.Imp} label="Imp" units="A" />
				<br />
				<label>
					<select bind:value={$pv.selectedWireId}>
						{#each wireGauges as g}
							<option value={g.id}>
								{g.text}
							</option>
						{/each}
					</select>
					Wire Gauge
				</label>
				<br />

				<InputInt bind:val={$pv.wireLength} label="Total wire length" units="m" min="3" max="300" />

				<hr />
				<Output val={round(stringVoc)} label="Voc of full string" units="V" />
				<Output val={round($pv.Vmp * $pv.panelsPerString)} label="Vmp of full string" units="V" />
				<Output
					val={round($pv.Isc * $pv.parallelStrings)}
					label="Isc of parallel strings"
					units="A"
				/>
				<Output val={round(nominalPower)} label="Nominal Array Power" units="W" />
				<br />
				<Output val={round(Rsource)} label="Source Impedance" units="Ω" />
				<Output val={round(mismatch)} label="Mismatch" units="%" />
				<br />
				<Output val={wireResistance} label="Resistance of wire" units="Ω" />
				<Output val={round(wireLosses)} label="Wire losses at Imp" units="W" />
			</Box>
		</span>
		<span>
			<Box style="padding-top:0px; padding-bottom:0px;">
				<p>
					<b>Search for Panel by PN:</b><br />
					<AutoComplete
						searchFunction={searchModule}
						bind:selectedItem={$pv.selectedModule}
						onChange={onModuleChange}
						maxItemsToShowInList={100}
						minCharactersToSearch={3}
						delay={200}
						localFiltering={false}
						localSorting={true}
						labelFieldName="Name"
						valueFieldName="__rowNum__"
						create={false}
						hideArrow={true}
					/>
				<p>
					<b>Vmp, Imp</b>, find these in the spec sheet of your solar panels (<a
						target="_blank"
						href="/pdf/CS-Datasheet-BiHiKu7_CS7N-MB-AG_v2.4_EN.pdf">example</a
					>) , use the STC values. These are the volts and amps your panel will make with a Solar
					irradiance of 1,000 W/m<sup>2</sup>, cell temperature of 25°C (77°F).
				</p>

				<p>
					<b>Isc of parallel strings</b> This is the max current your panels can make when shorted. All
					your wires/connectors/switches/breakers must be rated to at least this.
				</p>

				<p>
					<b>Voc</b> this is max open circuit voltage your panels can make. Everything in your
					system needs to be rated to at least <b>Voc of full string</b>. Common solar wire and
					connectors are rated to 600V.
				</p>

				<p>
					<b>Panels per string, Parallel Strings</b> If possible, use a single series string. If you
					are using small panels you can parallel more then one string but the strings should be well
					matched.
				</p>

				<p>
					<b>Source Impedance</b> is the resistance value you want to match with your lower heating
					element. I suggest a <b>Mismatch</b> below 15% is good enough. MPPT will correct the mismatch(within reason).
				</p>

				<p>
					<b>Wire Gauge</b> most solar installs use 10AWG 600V wire. You can reduce your <b>Wire Losses</b> a
					bit if you use thicker 8AWG wire.
				</p>
			</Box>
		</span>
	</div>

	<div class="sim-sidebar" id="step4">
		<span data-text>
			<h2>Step 4: Simulate 1 Year</h2>
			<p>
				Click <b>Simulate Monthly Generation</b> This will feed the simulator with the solar panel
				data you entered above and Typical Meteorological Year Data (TMY-{year}) for your lat/lng.
			</p>

			<button on:click={(e) => updateMonthlyTable(e)}>Simulate Monthly Generation</button> with
			<InputInt
				bind:val={$pv.losses}
				label="Losses (dirt, snow, aging, etc.) If your panels are shaded 1/3 of the day, then add 33%."
				units="%"
				min="1"
				max="99"
			/>
			<br />
			<p id="apiWarn" style="display: none;">
				This gets Weather data from an NREL API rate limited to 5000 req/day so you may have to try
				again tomorrow if it is not working.
			</p>
			<div>
				{#if monthTableLoading}
					<Spinner style="position: absolute; left:40%;" height="300px"></Spinner>
				{/if}

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
			</div>
			<p>
				If you are going much over 100% for <b>Solar Power Used</b> your array is bigger then it needs
				to be.
			</p>
			<hr>
		</span>
	</div>
<br>
<br>
	<div class="sim-sidebar" id="step4">
		<span data-text>
			<h2>Step 5: Simulate 1 Day</h2>
			<p>
				Click a <b>Graph random day</b> button a few times until you find a nice sunny day (lots of
				<b>Solar Radiation</b>). This graph uses the TMY-{year} weather data to run a daily PV simulation to help you size your
				array.  The important thing to look at here is <span class="blue"> <b>Tank Temperature</b></span>.

			</p>

			<div class="smol-css-grid">
				<button on:click={(e) => makeGraphUrl(0, e)}> Graph random day in Q1</button>
				<button on:click={(e) => makeGraphUrl(90, e)}> Graph random day in Q2</button>
				<button on:click={(e) => makeGraphUrl(180, e)}> Graph random day in Q3</button>
				<button on:click={(e) => makeGraphUrl(270, e)}> Graph random day in Q4</button>

				{#if $pv.allowNonMpptt}
					<label>
						<input type="checkbox" bind:checked={$pv.nonMpptGraph} />
						Estimate Non-MPPT Power
					</label>
				{/if}
			</div>
		</span>
		<br />
		{#if graphLoading}
			<Spinner style="position: absolute; left:700px; padding-top:100px;" height="400px"></Spinner>
		{/if}
		<span>
			<figure>
				<img alt="SolarSimGraph" src="sampleGraph.png" id="solarGraph" style="padding-top:10px;" />
			</figure>
		</span>
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

		<p>Graph Assumptions:</p>

		<ul>
			{#if $pv.allowNonMpptt}
				<li>
					Non-MPPT Power estimates are an experimental feature, do not expect high accuracy. This
					uses the <a href="https://pvlib-python.readthedocs.io/en/v0.6.0/singlediode.html"
						>lambertw single diode model</a
					> to estimate power into a fixed load (your heater element). Notice that MPPT is most useful
					when there are clouds. To use Non-MPPT you must select a panel by name/PN.
				</li>
			{/if}

			<li>No hot water withdraws (aka nobody is home). On most days you will be using hot water which will lower the <span class="blue"><b>Tank Temperature</b></span></li>
			<li>The tank water starts at your <b>Desired Output Temp</b> ({$pv.hotWaterOutTemp}℃)</li>
			<li>
				<span class="blue"><b>Tank Temperature</b></span> assumes fully mixed water. In the real
				world the hottest water moves to the top of the tank and the coldest to the bottom.
			</li>
			<li>
				The <span class="green"><b>Net Water Heating Power</b></span> will be negative when there is
				no sun. These are the standby $pv.losses estimated from your UEF ({$pv.energyFactor})
			</li>
			<li>The top element is disconnected (no city power).</li>
			<li>
				No thermostat is installed on the bottom element. If there was a thermostat the <span
					class="blue"><b>Tank Temperature</b></span
				>
				would not exceed the <span class="red"><b>Mixing Valve Limit</b> </span>
			</li>
		</ul>
	</div>
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

	container {
		min-width: 600px;
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
		/* grid-template-columns: fit-content(20ch) minmax(min(50vw, 30ch), 45ch) minmax(
				min(50vw, 30ch),
				1fr
			); */

		grid-template-columns: 1fr 2fr minmax(300px, 3fr);
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

	.elementInputLabel {
		line-height: 30px;
	}
	:global(.elementInput) {
		padding-top: 1px !important;

		padding-left: 4px !important;
		padding-bottom: 1px !important;
		font-size: 16px !important;
	}

	select {
		padding-top: 1px;
		padding-bottom: 1px;
		font-size: 16px;
	}
</style>
