function senduseD() {
    alert("1")
    var u = document.getElementById("username");
    u = u.value;
    var p = document.getElementById("password");
    p = p.value;
    var data = new FormData();
    data.append("user", u);
    data.append("pas", p);
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "cre");
    xhr.upload.addEventListener("progress", updateProgress, false);
    xhr.send(data);
}

function senduseDfL() {
    alert("1")
    var u = document.getElementById("username");
    u = u.value;
    var p = document.getElementById("password");
    p = p.value;
    var data = new FormData();
    data.append("user", u);
    data.append("pas", p);
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "log2");
    xhr.upload.addEventListener("progress", updateProgress, false);
    xhr.send(data);
    r(xhr);


}

function r() {
    alert("10")
    if (xhr.readyState == 4) {
        if (xhr.status == 200) {
            alert("success")
            var json_data = xhr.responseText;
            console.log(json_data);
        }
    }

}







function updateProgress(evt) {
    if (evt.loaded == evt.total) alert("Okay");

}


function error() {
    alert("Pass ou username errado ou não resgistrado!")
}