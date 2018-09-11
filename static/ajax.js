let form = document.getElementById("form1");
let question = document.getElementById("user_input");

//  Flexbox for speech bubble
function createFlexBox(justify, color) {
    let flexElt = document.createElement('div');
    flexElt.className = 'd-flex ' + justify;

    let contentElt = document.createElement('div');
    contentElt.className = 'm-2 p-2 rounded bg-' + color;
    flexElt.appendChild(contentElt);
    return flexElt;
}
// Ajax callback function
function grandPy(data) {
    let chatbox = document.getElementById("chatlog");
    let answer = createFlexBox('justify-content-start', 'success');
    answer.firstElementChild.innerHTML = JSON.stringify(data);
    chatbox.appendChild(answer);
    // let gmap = createFlexBox('justify-content-start', 'secondary');
    // gmap.firstElementChild.id = 'map'
    // gmap.firstElementChild.innerHTML = data[1];
    chatbox.scrollTop = chatbox.scrollHeight;
//     createMarker(data[1]);
}
// Posts user input on the chatbox when submit event is evolked
form.addEventListener("submit", function (e) {
    e.preventDefault();
    let chatbox = document.getElementById("chatlog");
    let userInput = createFlexBox('justify-content-end', 'primary');
    userInput.firstElementChild.textContent = question.value;
    chatbox.appendChild(userInput);
    chatbox.scrollTop = chatbox.scrollHeight;

    //Ajax request
    let data = new FormData(form);
    let req = new XMLHttpRequest();
    req.open('POST', '/post');
    req.addEventListener("load", function () {
        if (req.status>=200 && req.status<=400) {
            let parsed = JSON.parse(req.responseText)
            setTimeout(grandPy.bind(null, parsed), 1000);
        }
    });
    req.send(data);
    // Clears text on the input element
    form.reset();

});

var map; 

function initMap() {

    map = new google.maps.Map(document.getElementById('map'), {
    center: {lat: 48.8584, lng: 2.2945},
    zoom: 15
    });



}

function createMarker(loc){
    map.setCenter(loc)
    var marker = new google.maps.Map({
        position: loc,
        map: map
    });
}


    

