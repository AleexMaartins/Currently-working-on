var im1;
var im2;

function updatePhoto(event) {
    alert("1");

    var reader = new FileReader();
    reader = iml1(event);


    alert("777");
    im1 = event.target.files[0];
    //Libertar recursos da imagem selecionada


}

function iml1(event) {
    alert("ola");
    //Criar uma imagem
    var img = new Image();
    img = im1(img);

}

function im1(img) {
    canvas = document.getElementById("photo1");
    ctx = canvas.getContext("2d");
    ctx.drawImage(img, 0, 0, img.width, img.height, 0, 0, 530, 400);
    alert("1");

}

function updatePhoto2(event) {
    alert("1");

    var reader = new FileReader();
    reader = iml2(event);


    alert("777");
    im2 = event.target.files[0];
    //Libertar recursos da imagem selecionada

}

function iml2(event) {
    alert("ola");
    //Criar uma imagem
    var img = new Image();
    img = im2(img);

}

function im2(img) {
    canvas = document.getElementById("photo2");
    ctx = canvas.getContext("2d");
    ctx.drawImage(img, 0, 0, img.width, img.height, 0, 0, 530, 400);
    alert("1");

}




function sendFile() {
    alert("3");
    var data = new FormData();
    data.append("i1", im1);
    data.append("i2", im2);
    alert("3");
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "done");
    xhr.upload.addEventListener("progress", updateProgress, false);
    xhr.send(data);
}



function updateProgress(evt) {
    if (evt.loaded == evt.total) alert("Okay");
}