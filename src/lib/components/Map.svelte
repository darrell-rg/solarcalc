<script>
    import { MapLibre, Marker } from 'svelte-maplibre';

    
    let boundPos = { lng: -105.07, lat: 40.57 };

  </script>
  <ul>
    <li>Position from <code>bind:latLng</code>: {JSON.stringify(boundPos)}</li>
  </ul>
  <MapLibre 
    center={[boundPos.lng,boundPos.lat]}
    zoom={7}
    class="map"
    standardControls
    on:moveend={(event) => (console.log(event))}
    style="https://basemaps.cartocdn.com/gl/positron-gl-style/style.json" >

    <Marker
    bind:lngLat={boundPos}
    draggable

    class="solarMarker"
  >
  <img alt="PanelLocation" src="solarIcon.png" class="solarMarker" />
  </Marker>
</MapLibre>
  
  <style>
    :global(.map) {
      height: 500px;
    }
    .solarMarker{
      height: 50px;
    }
  </style>