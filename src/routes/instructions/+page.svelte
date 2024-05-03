<script>
</script>

<svelte:head>
	<title>Instructions</title>
	<meta name="description" content="About this app" />
</svelte:head>

<div class="text-column">
	<h1>Instructions</h1>
	<ol>
		<li>
			Calculate/Design
			<ol>
				<li>Determine existing cost of power used for water heating</li>
				<li>Design your system using the simulator.</li>
				<li>Price out the BOM and calculate payback.</li>
			</ol>
		</li>
		<li>Order Materials</li>
		<ol>
			<li>Used panels are great for this, and can be had for very cheap.</li>
			<li>Big solar panels will ship via freight so you may have to be home to receive them</li>
			<li>
				The panels are easily damaged on the back/plastic covered side. A damaged panel will limit
				the current of the entire array, so you may want to order a spare.
			</li>
			<li>Most of the stuff I got from ebay/craigslist/amazon</li>
		</ol>
		<li>
			Install Panels
			<ol>
				<li>Replace the shingles first if they are in bad shape.</li>
				<li>Install Roof anchors.</li>
				<li>Attach Rails to anchors.</li>
				<li>Attach Panels to rails.</li>
				<li>Attach grounding system.</li>
				<li>
					Run plastic conduit from panels to house, and metal conduit inside the house going to the
					water heater.
				</li>
				<li>Pull wire through conduit and connect it to the shutoff switch</li>
				<li>Lockout/Tagout shutoff switch before working inside</li>
			</ol>
		</li>
		<li>Electrical</li>
		<ol>
			<li>Turn off power to water heater</li>
			<li>Drain water heater</li>
			<li>Install Mixing valve</li>
			<li>Remove bottom element cover, take picture of wires for future reference.</li>
			<li>
				Disconnect bottom element from city power and secure wires so they will not short out on
				anything.
			</li>
			<li>Install new bottom element.</li>
			<li>Refill water heater.</li>
			<li>
				Connect bottom element to panels. (make sure there is water in there or you will burn out
				the elements)
			</li>
			<li>Turn power back on to top element.</li>
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
		<img alt="DigDitch" src="solarShed/switch2.jpg" />
		<figcaption>
			Make sure you keep that switch turned off while you are messing with the wires!
		</figcaption>
	</figure>

	<figure>
		<img alt="DigDitch" src="solarShed/PanelsInSun.jpg" />
		<figcaption>Collecting Photons? Yes. Cleaning yard before taking picture? No.</figcaption>
	</figure>

	<figure>
		<img alt="DigDitch" src="solarShed/firstPower.jpg" />
		<figcaption>Look at that Sweet Sweet HVDC power. (No Touching!)</figcaption>
	</figure>
</div>

<style>
	img {
		max-width: 75%;
	}

	/* figure {
		float: right;
		clear: both;
	} */
</style>
