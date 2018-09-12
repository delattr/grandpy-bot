var form = document.getElementById("form1");
var question = document.getElementById("user_input");
var chatboxElt = document.getElementById("chatlog");
var count = 0;

//  Flexbox for speech bubble
function createFlexBox(align, color, msg = '') {
    // Create flexbox
    let flexElt = document.createElement('div');
    flexElt.className = 'd-flex flex-column ' + align;
    // Content container
    let contentElt = document.createElement('div');
    contentElt.className = 'p-1 m-2 rounded shadow bg-' + color;
    contentElt.innerHTML = msg
    // Append container into Flex
    flexElt.appendChild(contentElt);
    return flexElt;
}

// Create response from JSON retrieved
function grandPyResponse(data) {
    // Create id for google map
    var mapId = 'map' + count++;
    // Check contents of data
    if (data.status === 'OK') {
        let speechBallon = createFlexBox('align-items-start', 'secondary', msg = data.address + ' ' + data.route);
        // Create div for google maps
        let gMap = document.createElement('div');
        gMap.id = mapId;
        gMap.className = 'newMap p-1 m-2 rounded shadow'
        speechBallon.appendChild(gMap);

        chatboxElt.appendChild(speechBallon);
        createMap(data.location, mapId);

    } else { // if result = 0 print error
        let speechBalloon = createFlexBox('align-items-start', 'secondary', msg = data.status);
        chatboxElt.appendChild(speechBalloon);
    }
    chatboxElt.scrollTop = chatboxElt.scrollHeight;
}

//Ajax request
function postAjax() {
    var data = new FormData(form);
    var req = new XMLHttpRequest();
    req.open('POST', '/post');
    req.addEventListener("load", function () {
        if (req.status >= 200 && req.status <= 400) {
            let parsed = JSON.parse(req.responseText)
            setTimeout(grandPyResponse.bind(null, parsed), 1000);
        } else {
            setTimeout(grandPyResponse.bind(null, "Http Error: " + req.statusText))
        }
    });
    req.send(data);

}
// Posts user input on the chatbox when submit event is evolked
form.addEventListener("submit", function (e) {
    e.preventDefault();
    let userInput = createFlexBox('align-items-end', 'primary', msg = question.value);
    chatboxElt.appendChild(userInput);
    chatboxElt.scrollTop = chatboxElt.scrollHeight;
    postAjax();
    // Clears text on the input element
    form.reset();

});

function createMap(location, id) {
    var map = new google.maps.Map(document.getElementById(id), {
        center: location,
        zoom: 15
    });
    var marker = new google.maps.Marker({
        position: location,
        map: map
    });
}