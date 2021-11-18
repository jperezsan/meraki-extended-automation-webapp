var platform = new H.service.Platform({
    'apikey': hereMapsApiKey
});

// Obtain the default map types from the platform object:
var defaultLayers = platform.createDefaultLayers();

// Instantiate (and display) a map object:
map = new H.Map(
    document.getElementById('mapContainer'),
    defaultLayers.vector.normal.map,
    {
        zoom: 5,
        center: { lat: 19.4326, lng: -99.1332 }
    });

// add a resize listener to make sure that the map occupies the whole container
window.addEventListener('resize', () => map.getViewPort().resize());
                                    
// MapEvents enables the event system
// Behavior implements default interactions for pan/zoom (also on mobile touch environments)
var behavior = new H.mapevents.Behavior(new H.mapevents.MapEvents(map));

// Create the default UI:
ui = H.ui.UI.createDefault(map, defaultLayers);