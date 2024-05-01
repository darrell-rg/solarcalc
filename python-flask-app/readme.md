# Flask Application for Solar PV hot water simulator

This is a simple Flask application developed to simulate solar PV with PVWAtts

## Deploying the application in Choreo
1. Fork this repository.
2. Get an API key for NRDS and PVWatts V8 from NREL
3. Create a `Service` component in Choreo.
4. Deploy the component.

## Testing the application

Invoke the following endpoints to test the application. Make sure to change the `<endpoint-url>` to the URL of the deployed component.

### Viewing all the available endpoints

```
set NRDSBAPIKEY = "your api key from NREL"

flask run dev

curl -X GET <endpoint-url>/

curl -X GET <endpoint-url>/graph

curl -X GET <endpoint-url>/csv

curl -X GET <endpoint-url>/json

```
