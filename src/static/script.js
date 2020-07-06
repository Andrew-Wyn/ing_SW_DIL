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
    video.addEventListener("canplay", startMain);
    video.srcObject = mediaStream;
    video.play();
}

function startMain(e) {
    button.setAttribute("hidden", "hidden");
    window.setTimeout(takePicture, 0);
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

function dataReady(dataArray) {
    window.setTimeout(takePicture, 0);

    if (data.length == 0) {
        return;
    }

    emptyContainer(previewContainer);

    dataArray.forEach(function (data, i, arr) {
        card = makeCard(PNGb64toURL(data.snapshot), [bold(data.type)]);
        previewContainer.appendChild(card);

        if (data.valid) {
            var id = data["type"] + data["primaryKey"];
            card = makeCard(PNGb64toURL(data.snapshot), attrToDOM(data.attributes));
            card.setAttribute("id", id);
            dropFromList(id);
            listColumn.appendChild(card);
        }
    });
}

/* Cards creation */

function emptyContainer(container) {
    while (container.firstChild) {
        container.removeChild(container.lastChild);
    }
}

function PNGb64toURL(s) {
    return "data:image/png;base64," + s;
}

function bold(text) {
    var b = document.createElement("b");
    var textNode = document.createTextNode(text);
    b.appendChild(textNode);
    return b;
}

function attrToDOM(attr) {
    var ret = [];

    var keys = [];
    for (var key in attr) {
        if (attr.hasOwnProperty(key)) {
            keys.push(key);
        }
    }

    keys.sort();

    keys.forEach(function(key, i, keys) {
        ret.push(bold(key + ": "));
        ret.push(document.createTextNode(attr[key].join(" ")));
        ret.push(document.createElement("br"));
    });

    return ret;
}

function dropFromList(key) {
    el = document.getElementById(key);
    if (el) {
        listColumn.removeChild(el);
    }
}

function makeCard(image, textElements, key) {
    var card = document.createElement("div");
    card.setAttribute("class", "card");

    var img = document.createElement("img");
    img.setAttribute("src", image);
    card.appendChild(img);

    var textDiv = document.createElement("div");
    textDiv.setAttribute("class", "text");

    textElements.forEach(function (textElement, i, arr) {
        textDiv.appendChild(textElement);
    });

    card.appendChild(textDiv);

    return card;
}
