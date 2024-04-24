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
    <h2>What problems have you run into?</h2>
    <p>Squirrels chewed some of the wires and I had to replace them. An cheap ebay inline fuse holder melted.  2/5 DC solar optimizers failed.  I am no sure the optimizers were worth it, they only get you 20-30% more power. The panels are not quite steep enough to shed snow by themselves, sometime I have to clean them manually.  </p>
  </article>

	<article class="faq">
    <h2>What is impedance matching and why does it matter?</h2>
    <p>Maximum Power Transfer theorem says we want to match the load impedance to the source impedance.   To get the full capacity of the panels, it necessary to choose a water heater element that matches the source impedance(Vmpp/Immp) of the solar panel array.  You can also use DC solar optimizers for this, they do MPPT at the panel level.   If you have a lot of partial shading, the optimizers may be worth it.  In most cases, carefully selecting the resistance of your heater element is good enough.  There is a calculator on the simulator page to help you with this. </p>
  </article>

  <article class="faq">
    <h2>What about permits?</h2>
    <p>Fewer or no permits are required since there is no connection to the grid.  This is a major benefit because in my county, the permits would cost more then all the materials!  Mounting the panels on a shed instead of your  house roof can avoid the need for permits in some locales. </p>
  </article>

  <article class="faq">
    <h2>Is this better then solar thermal?</h2>
    <p>This system has no moving parts and is cheaper and easier to install.  It reuses your existing electric water heater.  It does require more panel area. If you want to heat the whole house solar thermal would be better.</p>
  </article>

  <article class="faq">
    <h2>Is this better then a heat pump water heater?</h2>
    <p>Heat pump water heaters have some downsides.  They make noise, and you have to clean the air filter regularly. Some of them beep when they need the filter cleaned and they always manage to start beeping at 3am. They cost more and are less reliable then the old fashioned electric water heater. They steal heat from the air, which is great in summer but in winter this will add to your heating bill. </p>
  </article>

  <article class="faq">
    <h2>Why use the bottom element?</h2>
    <p>This way you can leave the top element hooked up to city power for when there is a long stretch of limited sunshine.  In my case, the top element is only used in winter. The thermal breaker on the upper heating element will trip if the water gets really hot in the summer.  You may have to take the cover off and reset the breaker come winter. </p>
  </article>

  <article class="faq">
    <h2>Do I need a thermostat?</h2>
    <p> The AC thermostat built into the water heater will not last long on DC power. DC arcs more since there is no zero-crossing to extinguish the arc. If your array is not too oversized you can make do with only a mixing valve and no thermostat.  In the summer, the water will get hotter then is safe so you need a hot/cold mixing valve to prevent scalds.   This extra hot water in the tank increases the amount of energy you can store.  I have made it through three cloudy days in a row before I need to use city power to heat the water.  </p>
  </article>

  <article class="faq">
    <h2>What is the best angle to mount the solar panels?</h2>
    <p>If possible, face the panels due south and angle them so they are a bit steeper then your latitude in degrees.   Steeper will collect more power in winter when the days are short and the sun is low. Steeper also sheds snow/leaves better. Flat mounted panels can be used but you will have to clean them frequently.  If getting to this steep angle is going to cause a lot of mounting headaches, don't worry about it too much.  My system is about 15 degrees flatter then ideal.   </p>
  </article>

  <article class="faq">
    <h2>How big an array do I need?</h2>
    <p> I have 1.5kw on a standard 40 gallon water heater and it works great.  In the summer this is almost too much, the water gets very hot. In the winter I still need a bit of city power from time to time. </p>
  </article>

  <article class="faq">
    <h2>What about trees or other shading?</h2>
    <p>Deciduous trees are not that bad because they block light in the summer when there is too much, and allow more through in the winter when there is not enough.  If you have some evergreen trees that will block the sun for half the day, you can add more panels to compensate.  </p>
  </article>


</div>


<style>
	h2 {
		font-size: 1.2em;
		font-weight: 700;
	}
</style>