<script>
	import HousePic from '$lib/components/HousePic.svelte';
</script>

<svelte:head>
	<title>PVH2O Instructions</title>
	<meta name="description" content="Building Solar Photo Voltaic Hot Water System" />
</svelte:head>

<div class="text-column">
	<h1>Instructions</h1>
	<figure class="floatRightBig">
		<HousePic style="" />
		<figcaption>Mouseover schematic to show labels</figcaption>
	</figure>
	<ol type="i">
		<li>
			Calculate/Design
			<ol>
				<li>Design your system using the simulator.</li>
				<li>Fill in what you know, leave the rest on defaults.</li>
				<li>Simulate your design to figure out the minium number of panels required.</li>
				<li>The sim will estimate the yearly cost of power used for water heating</li>
				<li>
					Look at your water heater and figure out what kind of fittings you will need to install
					mixing valve.
				</li>
				<li>
					Divide the BOM total by "Estimated Value Of Generated Solar Power" to calculate your
					payback
				</li>
			</ol>
		</li>
		<li>Order Materials</li>
		<ol>
			<li>Check out the example parts listed on the BOM page</li>
			<li>
				Try to find a local panel supplier to avoid freight charges. Used panels are fine if they
				all match.
			</li>
			<li>
				The panels are tough on the glass side, but easily damaged on the plastic covered side. A
				damaged panel will limit the current of the entire array, so you may want to buy a spare.
				Make sure to wear clothes with no buttons when you lift the panels so they do not get
				scratched.
			</li>
			<li>
				Special Tools you may need:
				<ol type="a">
					<li>DC clamp meter</li>
					<li>Water Heater Element Wrench</li>
					<li>MC4 Crimper set</li>
					<li>Pipe Soldering Tools</li>
				</ol>
			</li>
		</ol>
		<li>
			Install Panels
			<ol>
				<li>Replace the shingles first if they are in bad shape.</li>
				<li>Install Roof anchors.</li>
				<li>Attach Rails to anchors. Use anti-seize on stainless hardware.</li>
				<li>Attach Panels to rails.</li>
				<li>Attach grounding system.</li>
				<li>Trench in plastic conduit from panels to house.</li>
				<li>Pull wire through conduit and connect it to the outdoor disconnect switch</li>
				<li>Turn off disconnect switch, lock it out and/or finish wiring at night</li>
				<li>Solar wiring is safe at night, just don't fall off the roof in the dark</li>
			</ol>
		</li>
		<li>Indoor Work</li>
		<ol>
			<li>
				Drill hole in wall near water heater and mount a Type-LB Conduit Body on each side as
				passthrough.
			</li>
			<li>Install indoor conduit as required. (just use flex, so easy)</li>
			<li>Install indoor shutoff switch.</li>
			<li>Turn off power and cold water supply to water heater</li>
			<li>Drain water heater</li>
			<li>Install Mixing valve</li>
			<li>Remove bottom element cover, take picture of wires for future reference.</li>
			<li>
				Disconnect bottom element from city power and secure wires so they will not short out on
				anything.
			</li>
			<li>Install new bottom element (if needed).</li>
			<li>Measure resistance of element and write it on water heater for future reference</li>
			<li>Refill water heater.</li>
			<li>
				Connect bottom element to indoor shutoff. (make sure there is water in there or you will
				burn out the elements)
			</li>
			<li>Finish wiring and button up what you can</li>
			<li>Wait for daytime to Turn solar power switches on, Check for smoke.</li>
			<li>
				You can safely measure current with a DC clamp Meter. Only clamp one wire or else they will
				cancel out.
			</li>
			<li>P = I<sup>2</sup>R</li>
			<li>Turn city power back on to top element.</li>
		</ol>
	</ol>

	<figure>
		<img alt="Stack Of Solar Panels" src="solarShed/PanelShipment.jpg" />
		<figcaption>Freight shipment of panels laying in street</figcaption>
	</figure>

	<figure>
		<img alt="BrokenPanel" src="solarShed/BrokenPanel.jpg" />
		<figcaption>Check for broken Cells, Don't use panel if it has broken cells.</figcaption>
	</figure>

	<figure>
		<img alt="Wood Shingles" src="solarShed/BeforeWithWoodShingles.jpg" />
		<figcaption>Old leaky wood shingles not good for solar</figcaption>
	</figure>

	<figure>
		<img alt="Remove Old Roof" src="solarShed/RemoveOldRoof.jpg" />
		<figcaption>Stripping off old shingles</figcaption>
	</figure>

	<figure>
		<img alt="Put on new Roof" src="solarShed/PutOnNewRoof.jpg" />
		<figcaption>Panels will hide shingles, so slap em on as crooked as you like</figcaption>
	</figure>

	<figure>
		<img alt="Put on new rails" src="solarShed/PutOnRails.jpg" />
		<figcaption>Lay out the rails, bolt them to rafters</figcaption>
	</figure>

	<figure>
		<img alt="Loose lag screw" src="solarShed/mounting1.jpg" />
		<figcaption>
			These lag bolts can loosen up over time. Make sure they are tight so the wind does not thrash
			the panels around.
		</figcaption>
	</figure>

	<figure>
		<img alt="Middle Holddown" src="solarShed/middleHolddown.jpg" />
		<figcaption>This is a middle-type holddown bolt, holds down two panels.</figcaption>
	</figure>

	<figure>
		<img alt="End Holddown" src="solarShed/endHoldown1.jpg" />
		<figcaption>This is cheap-o end holddown type that is not quite the right size.</figcaption>
	</figure>

	<figure>
		<img alt="Middle Holddown" src="solarShed/fancyEndHolddown.jpg" />
		<figcaption>
			This is a fancy no-show end holddown so the neighbors know you are classy.
		</figcaption>
	</figure>

	<figure>
		<img alt="Solar Optimizers" src="solarShed/tigos.jpg" />
		<figcaption>You can install solar optimizers if you have partial shade issues.</figcaption>
	</figure>

	<figure>
		<img alt="Ground wire and lug" src="solarShed/railGroundLug.jpg" />
		<figcaption>Don't forget to install your lightning protection.</figcaption>
	</figure>

	<figure>
		<img alt="DigDitch" src="solarShed/digDitch.jpg" />
		<figcaption>Always utilize child labor when digging ditches for conduit</figcaption>
	</figure>

	<figure>
		<img alt="Switch" src="solarShed/switch2.jpg" />
		<figcaption>
			Make sure you keep that switch turned off while you are messing with the wires!
		</figcaption>
	</figure>

	<figure>
		<img alt="Panels in the sun" src="solarShed/PanelsInSun.jpg" />
		<figcaption>Collecting Photons? Yes. Cleaning yard before taking picture? No.</figcaption>
	</figure>

	<figure>
		<img alt="Mixing Valve" src="solarShed/mixValve1.jpg" />
		<figcaption>Install a thermostatic mixing valve near the water heater</figcaption>
	</figure>

	<figure>
		<img alt="First Power" src="solarShed/firstPower.jpg" />
		<figcaption>Look at that Sweet Sweet HVDC power. (No Touching!)</figcaption>
	</figure>
</div>

<style>
	img {
		max-width: 75%;
	}

	.floatRightBig {
		width: 500px;
		float: right;
		clear: both;
	}

	@media (max-width: 481px) {
		.floatRightBig {
			width: 310px;
		}
	}
</style>
