$(document).ready(function(){
    thumbsDivs = $('ul .thumbsDiv')

    thumbsDivs.each(function() {
        updateVisual($(this))
    })

    if ($("main").attr("user") !== null) { // jestlize zadny uzivatel neni prihlaseny
        thumbsDivs.children("img").click(function () { // on click
        thumbsDiv = $(this).parent() // ziskat parent div palce

        if (thumbsDiv.attr("thumbsRating") === $(this).attr("choiceVal")) { // pokud je stejný
            thumbsDiv.attr("thumbsRating", -1)
            $(this).prev("h5").text(parseInt($(this).prev("h5").text()) - 1)
        }
        else{
            if (thumbsDiv.attr("thumbsRating") === "-1") { // není hodnocení
                $(this).prev("h5").text(parseInt($(this).prev("h5").text()) + 1)
                // přidat 1 tam, kde jsme klikli
            }
            else {
                $(this).prev("h5").text(parseInt($(this).prev("h5").text()) + 1) // přidáváme + 1 tam, kde jsme klikli
                $(this).siblings("img").prev("h5").text(parseInt($(this).siblings("img").prev("h5").text()) - 1)
                // siblings - hledej elementy na stejné úrovni
            }
            thumbsDiv.attr("thumbsRating", $(this).attr("choiceVal"))
        }

        updateReviewRating(thumbsDiv.parent().parent("li").attr("reviewId"), thumbsDiv.attr("thumbsRating"))
            // poslani infomaci na server
        updateVisual(thumbsDiv) // aktualizace barevneho zobrazeni

    })
    }

    function updateVisual(div) {
        thumbsRating = parseInt(div.attr("thumbsRating"))
        div.children("img.thumbsup").attr("src", "/static/imgs/thumb_up" +((thumbsRating === 1)?"_full":"")+".png");
        div.children("img.thumbsdown").attr("src", "/static/imgs/thumb_down" +((thumbsRating === 0)?"_full":"")+".png");

    }

    function updateRatingsCount(h, val) {
        h.text(parseInt(h.text()) + val)
    }


    function updateReviewRating(reviewId, thumbsRating) {
        $.ajax({ // tvroba requestu
            type: "POST",
            url: "/setReviewRating", // url na kterou se ma poslat
            contentType: 'application/json',
            data: JSON.stringify({
                reviewId: reviewId,
                rating: thumbsRating
            }),
            success:  function(data){ // kdyz se vysledek vrati spravne
                console.log(data)
            },
            error: function(error){ // pokud nastala chyba, tak vypis chybu
                console.log(error)
            }
        });
    }

});