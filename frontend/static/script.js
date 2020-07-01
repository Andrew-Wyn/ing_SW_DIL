function submit() {
    const file = document.getElementById("fileInput").files[0];
    const reader = new FileReader();
    reader.onload = fileRead;
    reader.readAsBinaryString(file);
}

function fileRead(event) {
    const data = { image: btoa(event.target.result) };

    fetch('/recognize', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    })
    .then(update)
    .catch(error);
}

const toBase64 = file => new Promise((resolve, reject) => {
    reader.onload = () => resolve(reader.result);
    reader.onerror = error => reject(error);
});

function update(response) {
    if (response.status != 200) {
        alert("Errore " + response.status);
        return;
    }

    data = response.json().then(dataReady); // <-- TODO: ricorda .error()
}

function dataReady(data) {
    console.log('Success:', data);
    document.getElementById("canvas").setAttribute("src", "data:image/png;base64," + data[0].snapshot);
}

function error(error) {
    console.error('Error:', error);
}

function askCamera() {
    window.navigator.mediaDevices.getUserMedia({video: true}).then(setStream);
}

window.onload = askCamera

function setStream(mediaStream) {
    document.getElementById("videoPreview").srcObject = mediaStream
}

/*stream = mediaStream.getVideoTracks()[0]*/
