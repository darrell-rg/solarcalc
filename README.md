# DIY solar calculator for PV hot water

A few years ago I hooked some some panels to the bottom element of my water heater. It has worked so well, I wanted to make it easier for more people to try it. So I made this tool for design of PV hot water systems. 

At 85C, you can store around 10kWh of thermal energy in an average sized water heater.  With PG&E power prices, thats about 5 bucks worth, and the system will pay for itself in under two years.   A thermostatic mixing valve is used to bring the water down to a safe temperature before it is used. 

The simulator uses Typical Meteorological Year Data (TMY2020) for your location and simulates your solar hot water system at 30 minute intervals.  

The best part is, since this system is not connected to the grid, there are few or no permits required. You can do the install in a weekend and have free hot water monday afternoon.

Try it out at [pvh2o.com](https://www.pvh2o.com/).

![Screenshot](/static/Screenshot.png)

## Developing

First start the flask backend app in /python-flask-app.  See /python-flask-app/README.md

Once you've created a project and installed dependencies with `npm install` (or `pnpm install` or `yarn`), start a development server:

```bash
set PUBLIC_API_URL="http://localhost:5000/"
npm run dev

# or start the server and open the app in a new browser tab
npm run dev -- --open
```

## Building

To create a production version of your app:

```bash
PUBLIC_API_URL="urlwhereyoudeployedtheflaskapp.com"
npm run build
```

You can preview the production build with `npm run preview`.

> To deploy your app, you may need to install an [adapter](https://kit.svelte.dev/docs/adapters) for your target environment.
