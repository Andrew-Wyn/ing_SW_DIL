window.addEventListener("load", initPage);

function initPage(e) {
    video = document.getElementById("videoPreview");
    canvas = document.getElementById("canvas");
    imageList = document.getElementById("imageList");
    context = canvas.getContext('2d');

    window.navigator.mediaDevices.getUserMedia({video: true})
        .then(setCameraStream)
        .catch(getUserMediaError);
}

function setCameraStream(mediaStream) {
    video.addEventListener("canplay", videoReady)
    video.srcObject = mediaStream
}

function videoReady(e) {
    button.removeAttribute("disabled");
}

function takePicture() {
    button.setAttribute("disabled", "disabled");

    w = video.videoWidth
    h = video.videoHeight

    canvas.width = w
    canvas.height = h

    context.drawImage(video, 0, 0, w, h);
    var data = canvas.toDataURL('image/png');
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

function dataReady(data) {
    console.log(data)
    if (data.length != 0) {
        var i;
        for (i = 0; i < data.length; i++) {
            var elem = document.createElement("img");
            elem.setAttribute('src', "data:image/png;base64," + data[i].snapshot);
            imageList.appendChild(elem);
        }
    }

    window.setTimeout(takePicture, 200);
}

function fetchError(error) {
    console.error('Error:', error);
}

function responseJsonError(error) {
    console.error('Error:', error);
}

function getUserMediaError(error) {
    console.error('Error:', error);
}
