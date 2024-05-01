<script>
	import HousePic from "$lib/components/HousePic.svelte";


</script>

<svelte:head>
	<title>FAQ</title>
	<meta name="description" content="Frequently asked Questions" />
</svelte:head>

<div class="text-column">
	<h1>FAQ</h1>
  <article class="faq">
    <figure>
      <HousePic style="float:right; width: 400px;"/>
      <figcaption>DC only, Note thermostatic mixing valve</figcaption>
    </figure>
    <h2>What are we even doing here?</h2>
    <p>This site teaches you how to hook some solar panels to the bottom element of your water heater.  Cheap solar power with energy storage. I did this DIY and cut my household electric use in half. </p>
 
  </article>

  <article class="faq">
    <h2>What is the payback period?</h2>
    <p>This depends a lot on how expensive your power is and how much hot water you use. In my case, it was costing me a bit over buck day to heat water.  I was able to build a PV system for less then $2000.   I calculated my payback at around 5 years.  There are some places with expensive power where your payback could be closer to 2 years.</p>
  </article>

  <article class="faq">
    <h2>Will this kill me?</h2>
    <p>The main dangers are falling off the roof while installing the panels, electrocution, and fire.  HVDC is hazardous, probably more so then AC.  If you do not have much electrical experience it would be good to find an experienced person to help with the wiring part.  That said, this is a very simple circuit we are building.  Be sure to install all the wires in conduit to reduce fire risk.  Bond the solar rails and negative side of the array to a ground rod in case of lightning. Turn the switch off and check for current with a DC clamp meter before messing with the wires (or work at night).</p>
  </article>

  <article class="faq">
    <h2>How much hot water do I use?</h2>
    <p> According  <a href="https://www.fsec.ucf.edu/en/publications/pdf/fsec-pf-464-15.pdf">Estimating Daily Domestic HotWater Use in North American Homes</a> people use about 64 liters/person/day on average in a four person household.   This seems high to me, our house with 2 adults and 2 kids uses about half that.  I have noticed that I am more aware of how much hot water I am using after installing this system.  On sunny days I use more and on cloudy days I use less. </p>
  </article>

	<article class="faq">
    <figure >
      <img alt="shutoff switch" src="Source_and_load_circuit.svg" style="max-width: 300px;"/>
      <figcaption>Rs = RL for MAX POWER </figcaption>
    </figure>
    <h2>What is impedance matching and why does it matter?</h2>
    <p> <a href="https://en.wikipedia.org/wiki/Maximum_power_transfer_theorem">Maximum Power Transfer theorem</a> says we want to match the load impedance to the source impedance.   To get the full capacity of the panels, it necessary to choose a water heater element that matches the source impedance(Vmp/Immp) of the solar panel array.  You can also use DC solar optimizers for this, they will match the impedance for you (within reason).   If you have a lot of partial shading, the optimizers MIGHT be worth it.  In most cases, carefully selecting the resistance of your heater element is good enough.  There is a calculator on the simulator page to help you with this. 
    </p>
  </article>

  <article class="faq">
    <figure >
      <img src="solarShed/deadTigos.jpg" style="max-width: 300px;"/>
      <figcaption>Dead  TS4-A-O solar optimizers</figcaption>
    </figure>
    <h2>What DC solar optimizers did you try?</h2>
    <p>After the first year, I installed 5 TS4-A-O solar optimizers.  These cost about $40 each, and there is also a central controller setup you can get for $300 that will log the performance of each panel to the internet.  I did not not get the central controller.  After another year, I tested the panels with a DC clamp meter and found that two of the optimizers were producing zero amps.  I replaced these two bad ones.  I am not sure what is wrong with the two that failed, and it is not worth the money to buy the central controller to find out.  The manufacturer calls running without the central controller a "blind install" and does not officially support it, possibly because they want the monthly revenue from their cloud service.  On the whole, I am not sure the optimizers were worth it. <a href="https://www.sma-sunny.com/en/five-myths-about-dc-power-optimizers/">See also</a>  </p>
  </article>

  <article class="faq">
    <h2>What about permits?</h2>
    <p>Few or no permits are required since there is no connection to the grid.  This is a major benefit! In my county, the permits would double the install cost. Off grid also means there are no delays waiting for approvals to turn on your system.  Mounting the panels on a shed instead of your house roof can avoid the need for permits, this was the case in my locale. </p>
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
    <p> Heating 50 gallons of water from  5C to 70C stores about 14kWh of energy.  A Tesla Powerwall, stores about 13.5kWh of energy.  For both the water heater and the Powerwall, you can expect an efficiency of about 90%.  The powerwall cost around $9,300,  and you should be able to DIY this system for around $2,000.  </p>
  </article>

  <article class="faq">
    <figure >
      <img alt="shutoff switch" src="solarShed/switch1.jpg" style="max-width: 300px;"/>
      <figcaption>Solar Shutoff Switch</figcaption>
    </figure>
    <h2>What kind of shutoff switch do I need?</h2>
    <p>You need to mount the solar disconnect switch outside in a readily accessible place near the panels.  This is so firefighters/electricians/roofers/etc can turn your panels off while they are working.  Search for  "Solar Disconnect Switch" or "Solar Circuit Breaker Waterproof Isolator".   You can get a combo unit that is both a switch and a circuit breaker. You can also mount a second shutoff switch near the water heater to make working on it safer if you like.  I kinda wish I had one.</p>
  </article>

  <article class="faq">
    <h2>Why use the bottom element?</h2>
    <p>This way you can leave the top element hooked up to city power for when there is a long stretch of limited sunshine.  If the bottom element is keeping the water hot enough, the top element will never turn on.  In my case, the top element is only used in winter. The thermal breaker on the upper heating element will trip if the water gets really hot in the summer.  You may have to take the cover off and reset the breaker come winter. </p>
  </article>

  <article class="faq">
    <h2>Do I need a thermostat?</h2>
    <p> The AC thermostat built into the water heater will not last long if you try to use it on DC power. DC arcs a lot worse then AC since there is no zero-crossing to extinguish the arc.  A 600V, DC rated thermostat is hard to find.  If your array is not too oversized you can make do with only a mixing valve and no thermostat. The standby losses of the water heater <a href="https://en.wikipedia.org/wiki/Newton%27s_law_of_cooling">increase proportionally</a> with the hot water temperature. This helps to bring the system into equilibrium so it will not activate your P&T valve.   In the summer, the water will get hotter then is safe so you definitely need a thermostatic mixing valve to prevent scalds.   The extra hot water in the tank increases the amount of energy you can store.  I have made it through three cloudy days in a row before I need to use city power to heat the water.  </p>
  </article>

  <article class="faq">
    <figure >
      <img alt="mixing valve" src="solarShed/pAndTValve.webp" style="max-width: 300px;"/>
      <figcaption>P&T Valve</figcaption>
    </figure>
    <h2>Really you don't need a thermostat?</h2>
    <p> My system has been running for three years with no thermostat. I am using solar DC power hooked directly to the bottom heater element. As long as you don't overdo it with the number of panels this works fine. If you do overheat, your P&T valve will open and let some hot water out.  You can hear this if it happens. Make sure you test your P&T valve yearly by pulling the lever and listening for water flow.  </p>
  </article>


  <article class="faq">
    <figure >
      <img alt="mixing valve" src="solarShed/mixValve1.jpg" style="max-width: 300px;"/>
      <figcaption>My Mixing Valve</figcaption>
    </figure>
    <h2>What is a thermostatic mixing valve?</h2>
    <p> A mixing valve mixes some cold water in with the hot to maintain a set output temperature.  You install it at the output from the water heater where the hot water is piped to the rest of the house. Adding this valve prevents excessively hot water from burning you, and allows you to store more energy.  An example is the <a href="https://www.nibco.com/nibco-products/system-management/temperature-control/thermostatic-mixing-valves/h-tmv-131">Webstone TMV</a> which costs $115 and handles hot water up to 85C.      
    </p>
  </article>

  <article class="faq">
    <h2>What is the best angle to mount the solar panels?</h2>
    <p>If possible, face the panels due south and angle them so they are a bit steeper then your latitude in degrees.   Steeper will collect more power in winter when the days are short and the sun is low. Steeper also sheds snow/leaves better. Flat mounted panels can be used but you will have to clean them frequently.  If getting to the ideal angle is going to cause a lot of mounting headaches, don't worry about it too much.  My system is about 15 degrees flatter then ideal.  You can use the simulator to look at the seasonal affect that mounting angle has. </p>
  </article>

  <article class="faq">
    <h2>What kind of panels should I get?</h2>
    <p>I recommend getting some used panels from somewhere close to you on eBay, facebook marketplace, craigslist, etc.  You want the largest panels you can fit as this will result in less mounting hardware and connector losses. As an example currently on eBay you can get panels as big as 655W for $250, they are 2.4m x 1.3m, so about the size of a sheet of plywood.  Just three of those 655W panels would do the job. </p>
  </article>

  <article class="faq">
    <h2>What is the difference between commercial and residential panels?</h2>
    <p>Commercial panels are bigger and often have shorter wires. Residential panels are small enough to be handled by one person and have longer wires to make the install a bit easier. Either one will work, I got some used commercial panels because they were the cheapest option. </p>
  </article>

  <article class="faq">
    <h2>How big an array do I need?</h2>
    <p> I have 1.7kW on a standard 40 gallon water heater and it works great.  In the summer this is almost too much, the water gets up to around 70C. In the winter I still need a bit of city power from time to time. I suggest you start with 1-2kW and if that does not meet your needs you can add more panels.</p>
  </article>

  <article class="faq">
    <h2>What about trees or other shading?</h2>
    <p>Deciduous trees are not that bad because they block light in the summer when there is too much, and allow more through in the winter when there is not enough.  If you have some evergreen trees that will block the sun for half the day, you can add more panels to compensate.  That said, the most important thing for solar to work, is of course sunshine.  If you do not have a spot you can mount the panels where they will be in direct sunlight for at least half the day,  then this system will not work work for you. </p>
  </article>

  <article class="faq">
    <h2>What problems have you run into?</h2>
    <p>Squirrels chewed some of the wires and I had to replace them. A cheap ebay inline fuse holder melted.  2/5 DC solar optimizers failed.  I am not sure the optimizers were worth it, they only get you 20-30% more power. The panels are not quite steep enough to shed snow by themselves, sometime I have to clean them manually. I noticed some of the lag screws holding the solar rails down loosened up. Might want to give the system a yearly once over for lose bolts and chewed wires.  </p>
  </article>

  
  <article class="faq">
    <h2>There is an error on this website!</h2>
    <p> Thats not really a question, but you can email: webmaster@hot-h20.us and I will try to fix it.</p>
  </article>


  <article class="faq">
    <h2>Can you install this for me?</h2>
    <p> Yes, possibly if you are willing to pay $1000 and don't live to far away.  email: sales@hot-h20.us</p>
  </article>

</div>


<style>
	h2 {
		font-size: 1.2em;
		font-weight: 700;
	}

  figure{
    float: right;
    clear: both;
  }

  /* article > p{
    max-width: 75%;
  } */


</style>