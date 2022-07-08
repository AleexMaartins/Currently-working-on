function pic() {
    alert('Please')
    $.get("../us/showpic",
        function(response) {
            alert('d')
            console.log(response.pics)
            var text = '<img src="../img/' + response.pics + '" width="500" height="600">';
            $("#dst").html(text);
        });
    alert('Please')
};

$(document).ready(function() {
    $("#refresh_dst").on("click", pic);
});