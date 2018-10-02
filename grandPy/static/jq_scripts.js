$(document).ready(function () {
    var counter = 0;
    var logId;
    // Loading animation
    function loadSpinner() {

        var loading = '<div></div><div></div><div></div>'
        chatOutput('lds-ellipsis', loading);
    }

    // Ajax call
    function postAjax(url, data, callback) {
        loadSpinner();
        $.ajax({
            type: "POST",
            url: url,
            data: data,
            success: callback,
            error: (xhr) => {
                var msg = 'ERROR: ' + xhr.status + ' ' + xhr.statusText;
                chatOutput('grandpy', msg);
            },
            complete: function () {
                $('.lds-ellipsis').hide();
            }
        });
    }
    // Ajax callback function
    function callback(response) {
        if (response.status == 'OK') {
            var promise = loader();
            promise.then(function () {
                var answer = `Mon poussin ! as-tu demandé <b>${response.name}</b> ?`
                chatOutput('grandpy', answer + "<br>La voici : <i>" +
                    response.address + "</i>");
                return loader();
            }).then(function () {
                createMap(response);
                return loader();
            }).then(function () {
                var answer = "Mais t'ai-je déjà raconté l'histoire de ce quartier qui m'a vu en culottes courtes ?<br> "
                chatOutput('grandpy', answer + '<i>' + response.wiki + '</i>');
            });
        } else if (response.status === 'ZERO_RESULTS') {
            var promise = loader();
            promise.then(function () {
                chatOutput('grandpy', "Désolé, mon poussin. Je ne connais pas l'adresse");
            });
        } else {
            var promise = loader();
            promise.then(function () {
                chatOutput('grandpy', "Oh ! Mon pussin, il y avait une erreur.<br>ERROR: " + response.status);
            });
        }
    }

    // Display loading animation for 1 second before calling ajax callback function
    function loader() {
        return new Promise(function (resolve) {
            loadSpinner();
            setTimeout(() => {
                $('.lds-ellipsis').hide()
                resolve();
            }, 1000);
        });
    }
    // Create speechballoon inside of chatting box
    function chatOutput(clss, text) {
        counter++;
        logId = "log_" + counter;
        var justify;
        if (clss === 'grandpy' || clss === 'lds-ellipsis') {
            justify = 'justify-content-start'
        } else {
            justify = 'justify-content-end'
        };

        var flex = $("<div>").attr("class", `d-flex w-100 ${justify}`);
        var output = $("<div>").attr({
            class: `m-2 p-2 rounded shadow-sm ${clss}`,
            id: logId,
            style: "max-width: 75%;"
        });
        output.html(text);
        $(flex).append(output)
        $("#chatlog").append(flex);
        $("#chatlog").scrollTop($('#chatlog')[0].scrollHeight);
    }

    // Display google maps object
    function createMap(r) {
        chatOutput('grandpy', "");
        $("#" + logId).css({
            width: '400px',
            height: '300px'
        });
        $("#chatlog").scrollTop($('#chatlog')[0].scrollHeight);
        var map = new google.maps.Map(document.getElementById(logId), {
            center: r.location,
            zoom: 12
        });

        var marker = new google.maps.Marker({
            position: r.location,
            map: map
        });

        var infowindow = new google.maps.InfoWindow({
            content: `<b>${r.name}</b><br>${r.address}</div>`,
            maxWidth: 200
        });
        // Open InfoWindow when map object is loaded
        map.addListener("tilesloaded", () => {
            infowindow.open(map, marker);
        });
        // Open InfoWindow when marker is clicked
        marker.addListener("click", () => {
            infowindow.open(map, marker);
        });
    }

    // Submit event
    $("form").submit(function (event) {
        event.preventDefault();

        var userInput = $("input").val();
        question = userInput.trim();
        if (question != "") {
            chatOutput('user', userInput);

            // post FormData to the server
            postAjax('/post', $("form").serialize(), callback);

        } else {
            chatOutput('grandpy', "Demandes-moi ! l'adresse d'un lieu.");
        };
        // Clear input field
        $("input").val("");
    });
});