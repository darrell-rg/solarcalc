# DIY solar calculator for PV hot water

A design aid for DC solar hot water systems.

## Developing

First start the flask backend app in /python-flask-app.  See the readme.

Once you've created a project and installed dependencies with `npm install` (or `pnpm install` or `yarn`), start a development server:

```bash
set PUBLIC_API_URL="http://localhost:5173/"
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
