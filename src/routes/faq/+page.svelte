<script>


</script>

<svelte:head>
	<title>FAQ</title>
	<meta name="description" content="Frequently asked Questions" />
</svelte:head>

<div class="text-column">
	<h1>FAQ</h1>
  <article class="faq">
    <h2>What are we even doing here?</h2>
    <p>This site teaches you how to hook some solar panels to the bottom element of your water heater.  Cheap solar power with energy storage. I did this DIY and cut my household electric use in half.</p>
  </article>

  <article class="faq">
    <h2>Will this kill me?</h2>
    <p>The main dangers are falling off the roof while installing the panels, electrocution, and fire.  I did the wiring at night when there is no possibly of a shock.  I installed all the wires in conduit to reduce fire risk. I bonded the solar mounting rails and negative side of the array to a ground rod in case of lightning. </p>
  </article>

  <article class="faq">
    <h2>How much hot water do I use?</h2>
    <p> According  <a href="https://www.fsec.ucf.edu/en/publications/pdf/fsec-pf-464-15.pdf">Estimating Daily Domestic HotWater Use in North American Homes</a> people use about 64L/person/day on average in a four person household.   This seems high to me, our house with 2 adults and 2 kids uses about half that.  I have noticed that I am more aware of how much hot water I am using after installing this system.  On sunny days I use more and on cloudy days I use less. </p>
  </article>

	<article class="faq">
    <h2>What is impedance matching and why does it matter?</h2>
    <p>Maximum Power Transfer theorem says we want to match the load impedance to the source impedance.   To get the full capacity of the panels, it necessary to choose a water heater element that matches the source impedance(Vmpp/Immp) of the solar panel array.  You can also use DC solar optimizers for this, they do MPPT at the panel level.   If you have a lot of partial shading, the optimizers MIGHT be worth it.  In most cases, carefully selecting the resistance of your heater element is good enough.  There is a calculator on the simulator page to help you with this. </p>
  </article>

  <article class="faq">
    <h2>What DC solar optimizers did you try?</h2>
    <p>After the first year, I installed 5 TS4-A-O solar optimizers.  These cost about $40 each, and there is also a central controller setup you can get for $300 that will log the performance of each panel to the internet.  I did not not get the central controller.  After another year, I tested the panels with a DC clamp meter and found that two of the optimizers were producing zero amps.  I replaced these two bad ones.  I am not sure what is wrong with the two that failed, and it is not worth the money to buy the central controller to find out.  The manufacturer calls running without the central controller a "blind install" and does not officially support it, possibly because they want the monthly revenue from their cloud service.  On the whole, I am not sure the optimizers were worth it. <a href="https://www.sma-sunny.com/en/five-myths-about-dc-power-optimizers/">See also</a>  </p>
  </article>

  <article class="faq">
    <h2>What about permits?</h2>
    <p>Fewer or no permits are required since there is no connection to the grid.  This is a major benefit because in my county, the permits would cost more then all the materials!  Mounting the panels on a shed instead of your house roof can avoid the need for permits in some locales. </p>
  </article>

  <article class="faq">
    <h2>Is this better then solar thermal?</h2>
    <p>This system has no moving parts and is cheaper and easier to install.  It reuses your existing electric water heater.  It does require more panel area. If you want to heat the whole house solar thermal would be better.</p>
  </article>

  <article class="faq">
    <h2>Is this better then a heat pump water heater?</h2>
    <p>Heat pump water heaters are neat, but they have some downsides.  They make noise, and you have to clean the air filter regularly. Some of them beep when they need the filter cleaned (and they always manage to start beeping at 3am). They cost more and are less reliable then the old fashioned electric water heater. They steal heat from the indoor air and dump it to the water, which is great in summer but in winter this will add to your heating bill. </p>
  </article>

  <article class="faq">
    <h2>How much energy can I store in my water heater?</h2>
    <p> Heating 50 gallons of water from  5C to 70C stores about 14.3kWh of energy.  A Tesla Powerwall, stores about 13.5kWh of energy.  For both the water heater and the powerwall, you can expect an efficiency of about 90%.  The powerwall cost around $9,300,  and you should be able to DIY this system for well less then $2,000.  </p>
  </article>

  <article class="faq">
    <h2>What kind of shutoff switch do I need?</h2>
    <p>You want to mount an off switch in a outside in a readily accessible place, near the panels.  This is so firefighters/electricians/roofers/etc can turn your panels off while they are working.  Search for  "Solar Disconnect Switch" or "Solar Circuit Breaker Waterproof Isolator".   You can a combo unit that is both a switch and a circuit breaker.  If you are using parallel strings you can get a "Solar PV Combiner Box." </p>
  </article>

  <article class="faq">
    <h2>Why use the bottom element?</h2>
    <p>This way you can leave the top element hooked up to city power for when there is a long stretch of limited sunshine.  In my case, the top element is only used in winter. The thermal breaker on the upper heating element will trip if the water gets really hot in the summer.  You may have to take the cover off and reset the breaker come winter. </p>
  </article>

  <article class="faq">
    <h2>Do I need a thermostat?</h2>
    <p> The AC thermostat built into the water heater will not last long on DC power. DC arcs more since there is no zero-crossing to extinguish the arc. If your array is not too oversized you can make do with only a mixing valve and no thermostat. The standby losses of the water heater <a href="https://en.wikipedia.org/wiki/Newton%27s_law_of_cooling">increase proportionally</a> with the hot water temperature. This helps to bring the system into equilibrium so it will not activate your PTV valve.   In the summer, the water will get hotter then is safe so you need a hot/cold mixing valve to prevent scalds.   This extra hot water in the tank increases the amount of energy you can store.  I have made it through three cloudy days in a row before I need to use city power to heat the water.  </p>
  </article>

  <article class="faq">
    <h2>What is a thermostatic mixing valve?</h2>
    <p> A mixing valve mixes some cold water in with the hot to maintain a set output temperature.  You install it at the output from the water heater where the hot water is piped to the rest of the house. Adding this valve prevents excessively hot water from burning you, and allows you to store more energy.  An example is the <a href="https://www.nibco.com/nibco-products/system-management/temperature-control/thermostatic-mixing-valves/h-tmv-131">Webstone TMV</a> which costs $115 and handles hot water up to 85C.  </p>
  </article>

  <article class="faq">
    <h2>What is the best angle to mount the solar panels?</h2>
    <p>If possible, face the panels due south and angle them so they are a bit steeper then your latitude in degrees.   Steeper will collect more power in winter when the days are short and the sun is low. Steeper also sheds snow/leaves better. Flat mounted panels can be used but you will have to clean them frequently.  If getting to the ideal angle is going to cause a lot of mounting headaches, don't worry about it too much.  My system is about 15 degrees flatter then ideal.   </p>
  </article>

  <article class="faq">
    <h2>What kind of panels should I get?</h2>
    <p>I recommend getting some used panels from somewhere close to you on eBay, facebook marketplace, craigslist, etc.  You want the largest panels you can fit as this will result in less mounting hardware and connector losses. As an example currently on eBay you can get panels as big as 655w for $250, they are 2.4m x 1.3m, so about the size of a sheet of plywood.   </p>
  </article>

  <article class="faq">
    <h2>How big an array do I need?</h2>
    <p> I have 1.5kw on a standard 40 gallon water heater and it works great.  In the summer this is almost too much, the water gets very hot. In the winter I still need a bit of city power from time to time. </p>
  </article>

  <article class="faq">
    <h2>What about trees or other shading?</h2>
    <p>Deciduous trees are not that bad because they block light in the summer when there is too much, and allow more through in the winter when there is not enough.  If you have some evergreen trees that will block the sun for half the day, you can add more panels to compensate.  </p>
  </article>

  <article class="faq">
    <h2>What problems have you run into?</h2>
    <p>Squirrels chewed some of the wires and I had to replace them. An cheap ebay inline fuse holder melted.  2/5 DC solar optimizers failed.  I am not sure the optimizers were worth it, they only get you 20-30% more power. The panels are not quite steep enough to shed snow by themselves, sometime I have to clean them manually.  </p>
  </article>


</div>


<style>
	h2 {
		font-size: 1.2em;
		font-weight: 700;
	}
</style>