// remove existing markers
map.eachLayer(function(layer) {
    if (layer instanceof L.Marker) {
        map.removeLayer(layer);
    }
});

// a map of colors, can be hardcoded or build dynamically from data field
var colors = {
    "Type A": 'red',
    "Type B": 'blue',
    "Type C": 'yellow',
    "Type D": 'black'
};

// init config
var markers = L.DonutCluster({
    chunkedLoading: true
}, {
    key: 'groupingKey',
    sumField: 'valueKey',
    arcColorDict: colors
});

// iterate data, pull necessary keys and pass them into marker constructor
for (var i = 0; i < data.length; i++) {
    var marker = L.marker(L.latLng(data[i]['Latitude'], data[i]['Longitude']), {
        groupingKey: data[i]['Type'],
        valueKey: data[i]['Value']
    });

    // control what to display inside onclick popup
    var popupContent = Object.keys(data[i]).map(function(key) {
        return data[i][key];
    }).join("<br> ");
    marker.bindPopup(popupContent);

// add marker to markers layer    
markers.addLayer(marker);
};

// add marker layer to map
map.addLayer(markers);
