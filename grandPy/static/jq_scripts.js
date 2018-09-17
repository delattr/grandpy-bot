$(document).ready(function () {
    var counter = 0;
    var logId;
    // loadSpinner();

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



    function loadSpinner() {

        var loading = '<div></div><div></div><div></div>'
        chatOutput('lds-ellipsis', loading);
    }
    // Append speechballoon inside of chatting box
    function chatOutput(clss, text) {
        counter++;
        logId = "log_" + counter;
        var justify;
        if (clss === 'grandpy' || clss === 'lds-ellipsis') {
            justify = 'justify-content-start'
        } else {
            justify = 'justify-content-end'
        };

        var flex = $("<div>").attr("class", `d-flex ${justify}`);
        var output = $("<div>").attr({
            class: `m-2 p-2 rounded shadow-sm ${clss}`,
            id: logId
        });
        output.html(text);

        $(flex).append(output)
        $("#chatlog").append(flex);
        $("#chatlog").scrollTop($('#chatlog')[0].scrollHeight);
    }

    // Display google maps object
    function createMap(location) {
        chatOutput('grandpy', "");
        $("#" + logId).css({
            width: '400px',
            height: '300px'
        });

        $("#chatlog").scrollTop($('#chatlog')[0].scrollHeight);

        var map = new google.maps.Map(document.getElementById(logId), {
            center: location,
            zoom: 12
        });
        var marker = new google.maps.Marker({
            position: location,
            map: map
        });

    }
    // Submit event
    $("form").submit(function (event) {
        event.preventDefault();

        var userInput = $("input").val();
        if (userInput != null) {
            chatOutput('user', userInput);
        };
        // post FormData to the server
        postAjax('/post', $("form").serialize(), callback);
        // Clear input field
        $("form input").val("");
    });
    // Ajax callback function
    function callback(response) {
        if (response.status == 'OK') {
            var promise = loader(chatOutput);
            promise.then(function () {
                chatOutput('grandpy', response.address)
                return loader()
            }).then(function () {
                createMap(response.location)
                return loader()
            }).then(function () {
                chatOutput('grandpy', response.wiki)
            });

        } else {
            loader().then(function () {
                chatOutput('grandpy', response.status);
            });
        }

        function loader() {
            return new Promise(function (resolve) {
                loadSpinner();
                setTimeout(() => {
                    $('.lds-ellipsis').hide()
                    resolve();
                }, 1000);
            });
        }
    }

});