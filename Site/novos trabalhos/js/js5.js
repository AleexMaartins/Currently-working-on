function pic() {
    alert('Please')
    $.get("../showim",
        function(response) {
            alert('d')
            console.log(response.pics)
            var text = '<div class="row text-center"><div class="col-lg-4"><a href="javascript:void(0)" class="card border-0 text-dark"><img class="card-img-top" src="img/' + response.pic + '" alt=><span class="card-body"><h4 class="' + response.u + '" id="us">Coleção de ' + response.u + ' </h4><input type="submit" value="Click here to see collection" onclick="showpic()"></span></a></div>';
            $("#dst").html(text);
        });
    alert('Please')
};

function showpic() {
    alert("10")
    var u = document.getElementById("us");
    u = u.className;
    alert(u);
    alert("10");
    var data = new FormData();
    data.append("user", u);
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "../us/show");
    xhr.upload.addEventListener("progress", updateProgress, false);
    alert("10")
    xhr.send(data);
    location.href = "../us/usepic";
    alert("10")
}

function updateProgress(evt) {
    if (evt.loaded == evt.total) alert("Okay");

}

function logO() {
    alert("10")
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "../log/logoff");
    xhr.upload.addEventListener("progress", updateProgress, false);
    xhr.send();
    location.href = "../"
}