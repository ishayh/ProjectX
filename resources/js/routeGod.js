GreenPath = {};
GreenPath.waypts = []

$('#submit').click(function() {
    GreenPath.calculateRoute();
});

GreenPath.calculateRoute = () => {
    let userSettings = {}
    userSettings.startLocation = $('#start').val()
    userSettings.endLocation = $('#end').val()
    userSettings.distance = $('#range').val()
    
    $.post("/newroute", { "userPreferences": JSON.stringify(userSettings) }, function (result) {
        if (result["STATUS"] != "SUCCESS") {
            alert(result["MSG"] + "Post request failed");
        } else {
            console.log(JSON.stringify(result["WAYPOINTS"]));
            GreenPath.updateRouteParameters(result["WAYPOINTS"]);
            directionArr = GreenPath.mapStarter();
            directionsService =  directionArr[0];
            directionsDisplay =  directionArr[1];
            GreenPath.displayRouteOnMap(directionsService, directionsDisplay);

        }
    }, "json");
    return false;
}

// **************** Map Route Display *******************

GreenPath.updateRouteParameters = (waypointArray) => {
    for (let i in waypointArray) {
        console.log(typeof waypointArray[i].latitude, waypointArray[i].longitude);
        GreenPath.waypts.push({
            location: new google.maps.LatLng(waypointArray[i].latitude, waypointArray[i].longitude),
            stopover: true
        });
    }
    console.log("this is waypoints: " + JSON.stringify(GreenPath.waypts));
    GreenPath.startPoint = document.getElementById('start').value;
    GreenPath.endPoint = document.getElementById('end').value;
}

initMap = () => {
    directionArr = GreenPath.mapStarter();
    directionsService =  directionArr[0];
    directionsDisplay =  directionArr[1];

    var onChangeHandler = function () {
        GreenPath.updateRouteParameters();
        GreenPath.displayRouteOnMap(directionsService, directionsDisplay);
    };
    document.getElementById('start').addEventListener('change', onChangeHandler);
    document.getElementById('end').addEventListener('change', onChangeHandler);
}

GreenPath.mapStarter = () =>{
    var directionsService = new google.maps.DirectionsService;
    var directionsDisplay = new google.maps.DirectionsRenderer;
    var map = new google.maps.Map(document.getElementById('map'), {
        zoom: 7,
        center: { lat: 41.85, lng: -87.65 }
    });
    directionsDisplay.setMap(map);
    return [directionsService, directionsDisplay];
}

GreenPath.displayRouteOnMap = (directionsService, directionsDisplay) => {
    console.log(GreenPath.startPoint, GreenPath.endPoint);
    directionsService.route({
        origin: GreenPath.startPoint,
        destination: GreenPath.endPoint,
        travelMode: 'WALKING',
        waypoints: GreenPath.waypts,
        //waypoints: [{location:{ lat: 41.85, lng: -87.65 }, stopover:true}],
        optimizeWaypoints: false
    }, function (response, status) {
        if (status === 'OK') {
            directionsDisplay.setDirections(response);
        } else {
            window.alert('Directions request failed due to ' + status);
        }
    });
}