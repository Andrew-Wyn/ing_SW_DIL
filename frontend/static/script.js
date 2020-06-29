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

// async function Main() {
//    const file = document.querySelector('#myfile').files[0];
//    console.log(await toBase64(file));
// }

// Main();

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

/*
$("button").click(function(){
    $.ajax({url: "/recognize", success: function (result){
      // callback
      $("#;
    }});
  });
*/