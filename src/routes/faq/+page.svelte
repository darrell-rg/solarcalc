<script>
	import HousePic from '$lib/components/HousePic.svelte';
</script>

<svelte:head>
	<title>PVH20 FAQ</title>
	<meta name="description" content="Frequently asked Questions" />
</svelte:head>

<div class="text-column">
	<h1>FAQ</h1>
	<figure class="floatRightBig">
		<HousePic style="" />
		<!-- <figcaption>Those lazy trees get plenty of free solar power. Why not you?</figcaption> -->
		<!-- <figcaption>Those lazy trees get plenty of free photons. Why not collect your share?</figcaption> -->
		<!-- <figcaption>Those lazy trees stand around all day, getting fed free photons. Why not wet your beak?</figcaption> -->
		<figcaption>
			Those lazy trees stand around all day, gorging themselves on free photons and farting out
			highly combustible gasses. If they can do it, so can you!
		</figcaption>
	</figure>
	<article class="faq">
		<h2>What are we even doing here?</h2>
		<p>
			This site teaches you how to hook some photo voltaic (PV) solar panels to the bottom element
			of your water heater. Cheap solar power with energy storage. I did this DIY and cut my
			household electric use in half.
		</p>
	</article>

	<article class="faq">
		<h2>What is the payback period?</h2>
		<p>
			This depends a lot on how expensive your power is and how much hot water you use. In my case,
			it was costing me a bit over buck day to heat water. I was able to build a PV system for less
			then $2000. Even with cheap power in Colorado my payback was around 5 years. If you are using
			expensive California power, your payback could be closer to 2 years.
		</p>
	</article>

	<article class="faq">
		<h2>Will this kill me?</h2>
		<p>
			The main dangers are falling off the roof while installing the panels, electrocution, and
			fire. HVDC is hazardous, probably more so then AC. If you do not have much electrical
			experience it would be good to find an experienced person to help with the wiring part. That
			said, this is a very simple circuit we are building. Be sure to install all the wires in
			conduit to reduce fire risk. Bond the solar rails and negative side of the array to a ground
			rod in case of lightning. Turn the switch off and check for current with a DC clamp meter
			before messing with the wires (or work at night).
		</p>
	</article>

	<article class="faq">
		<figure>
			<img alt="hot water use graph" src="medium_use_home.png" class="rightSideImg" />
			<figcaption>Medium Usage Home, Hot Water Draws</figcaption>
		</figure>
		<figure>
			<img alt="hot water pie chart" src="gpd_estimate.png" class="rightSideImg" />
			<figcaption>Hot Water Used vs. Household Size</figcaption>
		</figure>
		<h2>How much hot water do I use?</h2>
		<p>
			According <a href="https://www.fsec.ucf.edu/en/publications/pdf/fsec-pf-464-15.pdf"
				>Estimating Daily Domestic HotWater Use in North American Homes</a
			> people use about 64 liters/person/day on average in a four person household. This seems high
			to me, our house with 2 adults and 2 kids and we rarely use more then 150liters/day. I have noticed
			that I am more aware of how much hot water I am using after installing this system. On sunny days
			I use more and on cloudy days I use less.
		</p>
	</article>

	<article class="faq">
		<h2>How much energy can I store in my water heater?</h2>
		<p>
			If you assume the water starts off warm, heating from 40°C to 85°C, stores 9.89kWh. If you
			assume you are pulling water from the cold ground, heating 50 gallons from 5°C(ground temp) to
			85°C stores 17.5kWh. A Tesla Powerwall, stores about 13.5kWh. For both the water heater and
			the Powerwall, you can expect an efficiency of about 90%. The powerwall cost around $9,300,
			and you should be able to DIY this system for around $2,000.
		</p>
	</article>

	<article class="faq">
		<figure>
			<img alt="Source and Load Schematic" src="Source_and_load_circuit.svg" class="rightSideImg" />
			<figcaption>IF R<sub>S</sub>==R<sub>L</sub> THEN power='Maximum!'</figcaption>
		</figure>
		<h2>What is impedance matching and why does it matter?</h2>
		<p>
			<a href="https://en.wikipedia.org/wiki/Maximum_power_transfer_theorem"
				>Maximum Power Transfer theorem</a
			> says we want to match the load impedance to the source impedance. To get the full capacity of
			the panels, it necessary to choose a water heater element that matches the source impedance(Vmp/Immp)
			of the solar panel array. You can also use DC solar optimizers or a MPPT thermostat, they will
			match the impedance for you (within reason). If you have a lot of partial shading, the optimizers
			MIGHT be worth it. In many cases, carefully selecting the resistance of your heater element is
			good enough. There is a calculator on the simulator page to help you with this.
		</p>
	</article>

	<article class="faq">
		<figure>
			<img alt="dead tigos" src="solarShed/deadTigos.jpg" class="rightSideImg" />
			<figcaption>Dead TS4-A-O solar optimizers</figcaption>
		</figure>
		<h2>What DC solar optimizers did you try?</h2>
		<p>
			After the first year, I installed 5 TS4-A-O solar optimizers. These cost about $40 each, and
			there is also a central controller setup you can get for $300 that will log the performance of
			each panel to the internet. I did not not get the central controller. After another year, I
			tested the panels with a DC clamp meter and found that two of the optimizers were producing
			zero amps. I replaced these two bad ones. I am not sure what is wrong with the two that
			failed, and it is not worth the money to buy the central controller to find out. The
			manufacturer calls running without the central controller a "blind install" and does not
			officially support it, possibly because they want the monthly revenue from their cloud
			service. On the whole, I am not sure the optimizers were worth it. <a
				href="https://www.sma-sunny.com/en/five-myths-about-dc-power-optimizers/">See also</a
			>
		</p>
	</article>

	<article class="faq">
		<h2>What is MPPT?</h2>
		<p>
			MPPT is Maximum Power Point Tracking, a special case of impedance matching. To get the most
			out of your solar panels, you need MPPT. You can do the MPPT for the whole array in your
			thermostat or you can do it with DC solar optimizers at the panel level. The downside of using
			MPPT is that it adds a lot of cost and electronics that can fail. It is possible to run
			without using MPPT if you carefully match the source impedance of your panels to your heater
			element. Without MPPT you will only get around 2/3 of the power that MPPT can make. If your
			solar panels are really cheap and/or you live in an area with few cloudy days, not using MPPT
			can make sense. There is an "Estimate Non-MPPT Power" checkbox above the graph that will show
			if you select your panel by name/pn.
		</p>
	</article>

	<article class="faq">
		<h2>What about permits?</h2>
		<p>
			Few or no permits are required since there is no connection to the grid. This is a major
			benefit! In my county, the permits would double the install cost. Off grid also means there
			are no delays waiting for approvals to turn on your system. Mounting the panels on a shed
			instead of your house roof can avoid the need for permits, this was the case in my locale.
		</p>
	</article>

	<article class="faq">
		<h2>What about wind loads?</h2>
		<p>
			The <a href="https://www.omnicalculator.com/physics/wind-load"
				>100mph wind load on a 45deg tilted 4'x8' panel is 578lbf</a
			>. The <a href="lagPullout.png">pullout rating for a 3/8 lag screw into a 2x4 is 400lbf</a>.
			So use at least 4 lag screws per panel and make sure you are screwing into a rafter, not just
			the sheathing. If your panel is mounted close to the roof you will have less wind load. My
			panels stick out past the edges of the shed about a foot. The panels have survived winds that
			knocked over two back yard fences for what that is worth.
		</p>
	</article>

	<article class="faq">
		<h2>Is this better then solar thermal?</h2>
		<figure>
			<img alt="electric water heater" src="electricWaterHeater.png" class="rightSideImg" />
			<figcaption>A standard electric water heater</figcaption>
		</figure>
		<p>
			This system has no moving parts and is cheaper and easier to install. It reuses your existing
			electric water heater. PV panels gain efficiency on really cold days when thermal panels have
			trouble. PV does require more panel area to collect the same amount of heat as thermal. If you
			want to heat the whole house solar thermal would be better.
		</p>
	</article>

	<article class="faq">
		<h2>Is this better then a heat pump water heater?</h2>
		<p>
			Heat pump water heaters are neat, but they have some downsides. They make noise, and you have
			to clean the air filter regularly. Some of them beep when they need the filter cleaned (and
			they always manage to start beeping at 3am). They cost more and are less reliable then the old
			fashioned electric water heater. They steal heat from the indoor air and dump it to the water,
			which is great in summer but less great in winter. If you already have a heat pump water
			heater, you may be able to hook up the bottom element to solar, but I have not tried this
			myself.
		</p>
	</article>

	<article class="faq">
		<figure>
			<img alt="shutoff switch" src="solarShed/switch1.jpg" class="rightSideImg" />
			<figcaption>Solar Shutoff Switch</figcaption>
		</figure>
		<h2>What kind of shutoff switch do I need?</h2>
		<p>
			You need to mount the solar disconnect switch outside in a readily accessible place near the
			panels. This is so firefighters/electricians/plumbers/etc can turn your panels off while they
			are working. Search for "Solar Disconnect Switch" or "Solar Circuit Breaker Waterproof
			Isolator". You can get a combo unit that is both a switch and a circuit breaker. You should
			also mount a second shutoff switch near the water heater to make working on it safer.
		</p>
	</article>

	<article class="faq">
		<h2>Why use the bottom element?</h2>
		<p>
			This way you can leave the top element hooked up to city power for when there is a long
			stretch of limited sunshine. If the bottom element is keeping the water hot enough, the top
			element will never turn on. In my case, the top element is only used in winter. The thermal
			breaker on the upper heating element will trip if the water gets really hot in the summer. You
			may have to take the cover off and reset the breaker come winter.
		</p>
	</article>

	<article class="faq">
		<figure>
			<img alt="mixing valve" src="mixingValve.png" class="rightSideImg" />
			<figcaption>The Magical Mixing Valve</figcaption>
		</figure>
		<h2>What is a thermostatic mixing valve?</h2>
		<p>
			A mixing valve mixes some cold water in with the hot to maintain a set output temperature. In
			the summer,the water will get hotter then is safe so you definitely need a thermostatic mixing
			valve to prevent scalds. The extra hot water in the tank increases the amount of energy you
			can store. I have made it through three cloudy days in a row before I need to use city power
			to heat the water. You install it at the output from the water heater where the hot water is
			piped to the rest of the house. Adding this valve prevents excessively hot water from burning
			you, and allows you to store more energy. An example is the <a
				href="https://www.nibco.com/nibco-products/system-management/temperature-control/thermostatic-mixing-valves/h-tmv-131"
				>Webstone TMV</a
			> which costs $115 and handles hot water up to 85C.
		</p>
	</article>

	<article class="faq">
		<figure>
			<img alt="mppt thermostat" src="mppt_thermostat.jpg" class="rightSideImg" />
			<figcaption>MPPT thermostat</figcaption>
		</figure>
		<h2>Do I need a thermostat?</h2>
		<p>
			In most cases you will need a thermostat. If you want to use an array larger then 1kW or so,
			or you have a water heater with a high UEF (good insulation) you should use a thermostat. They
			make
			<a href="https://www.ebay.com/itm/263523458861"> thermostats with MPPT built in</a> so you do
			not have to worry much about impedance matching your heating element. The AC thermostat built
			into the water heater will not last long if you try to use it on DC power. DC arcs a lot worse
			then AC since there is no zero-crossing to extinguish the arc. If your array is pretty small
			you can make do with only a mixing valve and no thermostat. The standby losses of the water
			heater
			<a href="https://en.wikipedia.org/wiki/Newton%27s_law_of_cooling">increase proportionally</a>
			with the hot water temperature. This helps to bring the system into equilibrium.
		</p>
	</article>

	<article class="faq">
		<h2>What are standby losses?</h2>
		<p>
			The standby loss is how much heat energy leaks out through the water tank insulation and the
			attached pipes. It
			<a
				href="https://www.energytrust.org/wp-content/uploads/2017/11/Water_Heater_Energy_Storage_wStaffResponse.pdf"
				>varies widely</a
			>, from 20W for a new well-insulated tank to 200W for an old badly insulated tank. The higher
			your tank's UEF rating, the lower the standby losses. If your tank has a UEF rating above
			0.90, you will want to use a thermostat so your tank will not overheat when you go on summer
			vacation.
		</p>
	</article>

	<article class="faq">
		<h2>Really you don't use thermostat?</h2>
		<p>
			My system has been running for three years with no thermostat. BUT I have a crappy old water
			heater with bad insulation (high standby losses), and I have trees that shade the solar panels
			for about 1/2 of the day. So my 1.7kW becomes more like 0.8kW. If ever replace the water
			heater, or the trees fall down, I will get a thermostat.
		</p>
	</article>

	<article class="faq">
		<figure>
			<img alt="T&P valve" src="solarShed/pAndTValve.webp" class="rightSideImg" />
			<figcaption>T&P Valve</figcaption>
		</figure>
		<!-- <figure>
			<img alt="T&P valve popping" src="tempering-diagram.jpg" class="rightSideImg" />
			<figcaption>The T&P valve is popping</figcaption>
		</figure> -->
		<h2>What is a Temperature and Pressure (T&P) Relief valve?</h2>
		<p>
			The T&P valve is a safety device that will let some hot water out if your water heater gets
			too hot or has too high pressure. T&P valves used on residential water heaters are designed to
			open at 150 psi or 98C. When water is heated it expands. In a 50-gallon water heater, water
			being heated to the thermostat setting expands by approximately 1/2 gallon. In most houses the
			extra pressure will push back into the city water supply but if you have a really tight
			backflow preventer installed on the water main feeding the house there is nowhere for the
			pressure to go.
			<a href="https://www.watts.com/resources/references-tools/t-and-p-relief-valves"
				>If you find your T&P is popping you may need an expansion tank.</a
			>
			Make sure you test your T&P valve yearly by pulling the lever and listening for water flow.
		</p>
	</article>

	<article class="faq">
		<h2>What is the best angle to mount the solar panels?</h2>
		<p>
			If possible, face the panels due south and angle them so they are a bit steeper then your
			latitude in degrees. Steeper will collect more power in winter when the days are short and the
			sun is low. Steeper also sheds snow/leaves better. Flat mounted panels can be used but you
			will have to clean them frequently. If getting to the ideal angle is going to cause a lot of
			mounting headaches, don't worry about it too much. My system is about 15 degrees flatter then
			ideal. You can use the simulator to look at the seasonal affect that mounting angle has.
		</p>
	</article>

	<article class="faq">
		<h2>What kind of panels should I get?</h2>
		<p>
			I recommend getting some used panels from somewhere close to you on eBay, facebook
			marketplace, craigslist, etc. You want the largest panels you can fit as this will result in
			less mounting hardware and connector losses. As an example currently on eBay you can get
			panels as big as 655W for $250, they are 2.4m x 1.3m, so about the size of a sheet of plywood.
			Just three of those 655W panels would do the job.
		</p>
	</article>

	<article class="faq">
		<h2>What is the difference between commercial and residential panels?</h2>
		<p>
			Commercial panels are bigger and often have shorter wires. Residential panels are small enough
			to be handled by one person and have longer wires to make the install a bit easier. Either one
			will work, I got some used commercial panels because they were the cheapest option.
		</p>
	</article>

	<article class="faq">
		<h2>How big an array do I need?</h2>
		<p>
			I have 1.7kW on a standard 50 gallon water heater and it works great. In the summer this is
			almost too much, the water gets up to around 70C. In the winter I still need a bit of city
			power from time to time. I suggest you start with 1-2kW and if that does not meet your needs
			you can add more panels. If you plug your numbers into the simulator and you have multiple
			months with over 100% solar power generation then your array is probably too big.
		</p>
	</article>

	<article class="faq">
		<h2>What about trees or other shading?</h2>
		<p>
			Deciduous trees are not that bad because they block light in the summer when there is too
			much, and allow more through in the winter when there is not enough. If you have some
			evergreen trees that will block the sun for half the day, you can add more panels to
			compensate. That said, the most important thing for solar to work, is of course sunshine. If
			you do not have a spot you can mount the panels where they will be in direct sunlight for at
			least half the day, then this system will not work work for you.
		</p>
	</article>

	<article class="faq">
		<figure>
			<img alt="Melted Fuse Holder" src="meltedFuse1.jpg" class="rightSideImg" />
			<figcaption>Melted Inline Fuse Holder</figcaption>
		</figure>
		<h2>What problems have you run into?</h2>
		<p>
			Squirrels chewed some of the wires and I had to replace them. A cheap ebay inline fuse holder
			melted. 2/5 DC solar optimizers failed. I am not sure the optimizers were worth it, they only
			get you 20-30% more power. The panels are not quite steep enough to shed snow by themselves,
			sometimes I have to clean them manually. I noticed some of the lag screws holding the solar
			rails down loosened up. Might want to give the system a yearly once over to check for lose
			bolts and chewed wires.
		</p>
	</article>

	<article class="faq">
		<h2>There is an error/bug/falsehood on this website!</h2>
		<p>
			Please <a href="https://github.com/darrell-rg/solarcalc/issues">open a ticket on the github</a
			>.
		</p>
	</article>

	<article class="faq">
		<h2>Can you install this for me?</h2>
		<p>
			If you live on the front range and are want to pay me to install this for you, email:
			<a href="mailto:darrell@pvh2o.com"> darrell@pvh2o.com </a>
		</p>
	</article>

	<article class="faq">
		<h2>I have a question not answered here.</h2>
		<p>
			Please open a ticket on the <a href="https://github.com/darrell-rg/solarcalc">github</a> or
			email <a href="mailto:darrell@pvh2o.com"> darrell@pvh2o.com </a>
		</p>
	</article>

	<article class="faq">
		<h2>What element and panels did you use?</h2>
		<p>
			My heating element is Zoro #G1831724, 240V 2000W 28.8Ω. On the shed are SunPower
			SPR-P17-345-COM panels in 5S 1P.
		</p>
	</article>
</div>

<style>
	h2 {
		font-size: 1.2em;
		font-weight: 700;
	}

	figure {
		float: right;
		clear: both;
		/* width: 500px; */
	}

	.rightSideImg {
		max-width: 400px;
		min-width: 200px;
	}

	.floatRightBig {
		width: 500px;
	}

	@media (max-width: 481px) {
		.floatRightBig {
			width: 310px;
		}
		.rightSideImg {
			max-width: 300px;
			min-width: 200px;
		}
	}
</style>
