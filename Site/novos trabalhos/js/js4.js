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
    xhr.open("POST", "../log/log2");
    xhr.upload.addEventListener("progress", updateProgress, false);
    xhr.send(data);


}

function r() {
    alert('Please');
    $.get("/log/log3",
        function(response) {
            alert("4");
            d(response);
        });
    alert('Please');

}

function d(r) {
    alert("10");
    if (r.r == "done") {
        alert("10");
        location.href = "../rot";
    } else {
        location.href = "../log/inerr";
    }

}







function updateProgress(evt) {
    if (evt.loaded == evt.total) alert("Okay");
    r();

}


function error() {
    alert("Pass ou username errado ou não resgistrado!")
}