$(document).ready(function () {
    var counter = 0;
    var logId;

    function postAjax(url, data, callback) {
        $.ajax({
            type: "POST",
            url: url,
            data: data,
            success: callback,
            error: (xhr) => {
                var msg = 'ERROR: ' + xhr.status + ' ' + xhr.statusText
                chatOutput('justify-content-start', 'primary', msg)
            }
        });
    }

    function chatOutput(justify, color, text) {
        counter++;
        logId = "log_" + counter;
        var flex = $("<div>").attr("class", `d-flex ${justify}`);
        var output = $("<div>").attr({
            class: `m-2 p-2 rounded shadow text-white bg-${color}`,
            id: logId
        });
        output.html(text);

        $(flex).append(output)
        $("#chatlog").append(flex);
        $("#chatlog").scrollTop($('#chatlog')[0].scrollHeight);

    }


    function createMap(location) {
        chatOutput('justify-content-start', 'success', "");
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

    $("form").submit(function (event) {
        event.preventDefault();

        var userInput = $("input").val();
        if (userInput != null) {
            chatOutput('justify-content-end', 'success', userInput);
        };

        postAjax('/post', $("form").serialize(), function (response) {
            if (response.status == 'OK') {


                chatOutput('justify-content-start', 'primary', response.address);

                createMap(response.location);

                chatOutput('justify-content-start', 'primary', response.route + '<br>' + response.wiki.extract);



            } else {
                chatOutput('justify-content-start', 'primary', response.status);
            }
        });

        $("form input").val("");
    });


});