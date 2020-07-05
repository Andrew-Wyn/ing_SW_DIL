/* Page init */

window.addEventListener("load", initPage);

function initPage(e) {
    video = document.getElementById("video");
    button = document.getElementById("startButton");
    canvas = document.getElementById("canvas");
    listColumn = document.getElementById("listColumn");
    previewContainer = document.getElementById("previewContainer");
    context = canvas.getContext('2d');
}

/* Start stream */

function start() {
    button.setAttribute("disabled", "disabled");

    const constraints = {
        audio: false,
        video: {
            width: {
                ideal: 1920
            },
            height: {
                ideal: 1080
            }
        }
    };

    window.navigator.mediaDevices.getUserMedia(constraints)
        .then(setCameraStream)
        .catch(getUserMediaError);
}

function getUserMediaError(error) {
    console.error('Error:', error);
}

function setCameraStream(mediaStream) {
    video.addEventListener("canplay", hideStartButton);
    video.srcObject = mediaStream;
    video.play();
}

function hideStartButton(e) {
    button.setAttribute("hidden", "hidden");
}

/* Main logic */

function takePicture() {
    w = video.videoWidth;
    h = video.videoHeight;

    canvas.width = w;
    canvas.height = h;

    context.drawImage(video, 0, 0, w, h);
    var data = canvas.toDataURL('image/jpg', .8);
    data = data.replace(/^[^,]*,\s*/, "");

    makeRequest(data);
}

function makeRequest(imgData) {
    const data = { image: imgData };

    fetch('/recognize', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    })
    .then(responseReceived)
    .catch(fetchError);
}

function fetchError(error) {
    console.error('Error:', error);
}

function responseReceived(response) {
    if (response.status != 200) {
        console.log("Errore " + response.status);
        window.setTimeout(takePicture, 200);
        return;
    }

    data = response.json()
        .then(dataReady)
        .catch(responseJsonError);
}

function responseJsonError(error) {
    console.error('Error:', error);
}

function dataReady(data) {
    if (data.length != 0) {
        while (imageList.firstChild) {
            imageList.removeChild(imageList.lastChild);
        }
        var i;
        for (i = 0; i < data.length; i++) {
            var elem = document.createElement("img");
            elem.setAttribute('src', "data:image/png;base64," + data[i].snapshot);
            imageList.appendChild(elem);

            elem = document.createTextNode(
                JSON.stringify(data[i].attributes, null, 4));
            imageList.appendChild(elem);
        }
    }

    window.setTimeout(takePicture, 0);
}

/* Cards creation */

function test() {
    listColumn.appendChild(makeCard("dummy.png", "Test"));
}

function makeCard(image, text) {
    var card = document.createElement("div");
    card.setAttribute("class", "card");

    var img = document.createElement("img");
    img.setAttribute("src", image);
    card.appendChild(img);

    var textDiv = document.createElement("div");
    textDiv.setAttribute("class", "text");
    var textNode = document.createTextNode(text);
    textDiv.appendChild(textNode);
    card.appendChild(textDiv);

    return card;
}
