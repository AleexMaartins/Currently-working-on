//cv

function updatePhoto(event) {
    alert("1");

    var reader = new FileReader();
    reader = iml(event);


    alert("777");
    sendFile(event.target.files[0]);
    //Libertar recursos da imagem selecionada
    windowURL.revokeObjectURL(picURL);

}

function iml(event) {
    alert("ola");
    //Criar uma imagem
    var img = new Image();
    img = im(img);

}

function im(img) {
    canvas = document.getElementById("photo");
    ctx = canvas.getContext("2d");
    ctx.drawImage(img, 0, 0, img.width, img.height, 0, 0, 530, 400);
    alert("1");

}




function sendFile(file) {
    alert("3");
    var data = new FormData();
    data.append("myFile", file);
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/image/done");
    xhr.upload.addEventListener("progress", updateProgress, false);
    xhr.send(data);
}

function updateProgress(evt) {
    if (evt.loaded == evt.total) alert("Okay");
}