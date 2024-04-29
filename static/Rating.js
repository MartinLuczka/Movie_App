$(document).ready(function(){

    var defaultVal = 0;
    var hvezdy = $("#ratingDiv").children("img");

    const fullStarSrc = "imgs/full.png"
    const emptyStarSrc = "imgs/empty.png"

    hvezdy.hover(function(event){
        for (var i = 0; i < hvezdy.length; i++) {
            if (event.target.getAttribute("val") >= i + 1) {
                hvezdy[i].src = fullStarSrc;
            } else {
                hvezdy[i].src = emptyStarSrc;
            }
        }
    });

    hvezdy.mouseleave(function(event){
        for (var i = 0; i < hvezdy.length; i++) {
            if (defaultVal >= i + 1) {
                hvezdy[i].src = fullStarSrc;
            } else {
                hvezdy[i].src = emptyStarSrc;
            }
        }
    });

    hvezdy.click(function(event){
        sendToServer(event.target.getAttribute("val"));
    });

    function sendToServer(hvezdaVal) {
        $.ajax({
            type: 'POST',
            url: '/hodnoceniFilmu',
            contentType: 'application/json',
            data: JSON.stringify({
                rating: hvezdaVal,
                filmId: $("main").attr("filmId")
            }),
            success: function(data){
                console.log(data);
                if (data === "notlogedin") {
                    if (confirm("Nejste prihlaseny\nChcete se prihlasit?")) {
                        window.location.href = "/login";
                    }
                }
                else if (data === "success") {
                    defaultVal = hvezdaVal;
                }
            },
            error: function(error){
                console.log(error);
            }
        });
    }

});