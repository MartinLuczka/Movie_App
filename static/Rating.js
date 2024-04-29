$(document).ready(function(){

    let defaultVal = ($("#ratingDiv").attr("defaultUserRating") === undefined) ? 0 : $("#ratingDiv").attr("defaultUserRating");
    // pokud není myš nad kurzorem, tak svítí 0 hvězd
    let hvezdy = $("#ratingDiv").children("img");
    // získáme všechny hvězdy

    console.log(hvezdy)

    const fullStarSrc = "/static/imgs/full.png"
    const emptyStarSrc = "/static/imgs/empty.png"
    // cesty k obrázkům si zapíšeme do konstatních proměnných
    hvezdy.hover(function(event){
        // když máme myš nad kteroukoliv hvězdou
        for (var i = 0; i < hvezdy.length; i++) {
            console.log(i)
            // projdeme si všechny hvězdy
            if (event.target.getAttribute("order") >= i + 1) {
            // rozsvítíme hvězdu na kterou ukazuje a také všechny pod ní
                hvezdy[i].src = fullStarSrc;
                console.log(fullStarSrc)
                // změníme, zadáme zdroj obrázku
            } else {
                hvezdy[i].src = emptyStarSrc;
                console.log(emptyStarSrc)
                // ostatní nastavíme do "neaktivního" stavu
            }
        }
    });

    hvezdy.mouseleave(function(event){
    // pokud nemáme kurzor nad žádnou hvězdou
        for (var i = 0; i < hvezdy.length; i++) {
            if (defaultVal >= i + 1) {
                hvezdy[i].src = fullStarSrc;
            } else {
                hvezdy[i].src = emptyStarSrc;
            }
        }
    });
    // tak hvězdy nastavíme podle defaultní hodnoty, ta se změní ohodnocením uživatele, chceme, aby viděl uživatel své hodnocení

    hvezdy.click(function(event){
        sendToServer(event.target.getAttribute("order"));
    });
    // když kliknu na nějakou z hvězd, tak pošlu hodnotu pořadí této hvězdy

    function sendToServer(hvezdaVal) {
        $.ajax({
        // tvorba requestu na server
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
                    if (confirm("Nejste zde přihlášen!\nChcete se přihlásit?")) {
                        window.location.href = "/prihlaseni";
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