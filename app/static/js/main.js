var map = L.map('mapid').setView([21.07204051307818, 105.7739627412891], 20);
var osm = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

function iconTree(feature, latlng) {
    var iconCus = L.icon({
        iconUrl: "../static/images/tree.png",
        iconSize: [20, 20],
        iconAncho: [22, 94],
        popupAncho: [-3, -76]
    })
    return L.marker(latlng, { icon: iconCus })
}

//Feature building, tree
function buildingFeature(feature, layer) {
    feature.layer = layer;
    if (feature.properties) {

        layer.bindPopup("<b>Địa chỉ: </b>" + feature.properties.diaChi + "<br>" +
            "<b>Loại nhà: </b>" + feature.properties.loaiNha + "<br>" +
            "<b>Số tầng: </b>" + feature.properties.soTang + "<br>" +
            "<b>Diện tích: </b>" + feature.properties.dienTich + "m2<br>" +
            "<b>ID: </b>" + feature.properties.id + "<br>" +
            '<a href="building/' + feature.properties.id + '">Edit</a> | ' +
            '<a href="delBuilding/' + feature.properties.id + '">Delete</a>')
    }
}
function treeFeature(feature, layer) {
    feature.layer = layer;
    if (feature.properties) {

        layer.bindPopup("<b>Loại cây: </b>" + feature.properties.loaicay + "<br>" +
            "<b>Chiều cao: </b>" + feature.properties.chieucao + "m<br>" +
            "<b>ID: </b>" + feature.properties.id + "<br>" +
            '<a href="tree/' + feature.properties.id + '">Edit</a> | ' +
            '<a href="delTree/' + feature.properties.id + '">Delete</a>')
    }
}

//Layer Group
var markersLayer = new L.LayerGroup();

//Search
var searchTree = L.control.fuseSearch({
    position: 'topleft'
})
searchTree.addTo(map);

var searchBuilding = L.control.fuseSearch()
searchBuilding.addTo(map);

$("#btn").click(function (e) {

})


//
// Get API tree, building
function getAPI(link) {
    var overlay = null;
    $.ajax({
        type: "GET",
        datatype: "JSON",
        url: link,
        async: !1,
        success: function (response) {
            console.log(response)
            if (link == "api/v1/tree") {

                searchTree.indexFeatures(response.features, ['loaicay', 'chieucao', 'id']);

                overlay = L.geoJSON(response, {
                    pointToLayer: iconTree, onEachFeature: treeFeature
                })
                markersLayer.addLayer(overlay)
                // .addTo(map)
            }
            else {

                searchBuilding.indexFeatures(response.features, ['loaiNha', 'soTang', 'diaChi']);

                overlay = L.geoJSON(response, {
                    onEachFeature: buildingFeature
                })
                markersLayer.addLayer(overlay)
                // .addTo(map)
            }
        }
    })
    return overlay
}
//layer tree, building
var building = getAPI("localhost:5000/api/v1/building")
var tree = getAPI("localhost:5000/api/v1/tree")

console.log(tree)
//add layer to map
map.addLayer(markersLayer)

// Control layers
var baseLayers = {
    "Open Street Maps": osm
}
var overlays = {
    "Tree": tree,
    "Building": building,
}

L.control.layers(baseLayers, overlays).addTo(map)

//map legend
var legend = L.control({ position: 'bottomright' })
legend.onAdd = function (map) {
    var div = L.DomUtil.create('div', 'info')
    div.innerHTML += '<img style="width:30px;height:30px" src="static/images/building.png">: Building<br>'
    div.innerHTML += '<img style="width:30px;height:30px" src="static/images/tree.png">: Tree<br>'
    return div
}
legend.addTo(map)

//draw Item
drawnItems = L.featureGroup().addTo(map);
map.addControl(new L.Control.Draw({
    edit: {
        featureGroup: drawnItems,
        poly: {
            allowIntersection: false
        }
    },
    draw: {
        polygon: {
            allowIntersection: false,
            showArea: true
        }
    }
}));

map.on('draw:created', function (event) {
    var layer = event.layer;
    // layer.on('click', layerClick);
    drawnItems.addLayer(layer);
    var geoJSON = drawnItems.toGeoJSON();

    $.ajax({
        url: "/createNewItem",
        type: "POST",
        contentType: "application/json",
        data: JSON.stringify(geoJSON),
        success: function (data) { }
    });
});
// function layerClick(e) {
// }
