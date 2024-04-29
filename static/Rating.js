$(document).ready(function(){

    let defaultVal = ($("#ratingDiv").attr("defaultUserRating") === undefined) ? 0 : $("#ratingDiv").attr("defaultUserRating");
    // Získání výchozí hodnoty hodnocení uživatele, pokud existuje, jinak nastavení na 0
    let hvezdy = $("#ratingDiv").children("img");
    // Získáme všechny hvězdy

    const fullStarSrc = "/static/imgs/full.png"
    const emptyStarSrc = "/static/imgs/empty.png"
    // Cesty k obrázkům si zapíšeme do konstatních proměnných

    hvezdy.hover(function(event){
        // Když máme myš nad kteroukoliv hvězdou
        for (var i = 0; i < hvezdy.length; i++) {
            console.log(i)
            // Projdeme si všechny hvězdy
            if (event.target.getAttribute("order") >= i + 1) {
            // Rozsvítíme hvězdu na kterou ukazujeme a také všechny pod ní
                hvezdy[i].src = fullStarSrc;
                // Nastavení zdroje obrázku na plnou hvězdu
            } else {
                hvezdy[i].src = emptyStarSrc;
                // U ostatních nastaveníme zdroje obrázku na prázdnou hvězdu
            }
        }
    });

    hvezdy.mouseleave(function(event){
    // Při opuštění oblasti s hvězdami myší
        for (var i = 0; i < hvezdy.length; i++) {
            // Nastavení zdroje obrázku na plnou nebo prázdnou hvězdu podle defaultní hodnoty, ta je dána hodnocením v databázi
            if (defaultVal >= i + 1) {
                hvezdy[i].src = fullStarSrc;
            } else {
                hvezdy[i].src = emptyStarSrc;
            }
        }
    });
    // Tak hvězdy nastavíme podle defaultní hodnoty, ta se změní ohodnocením uživatele, chceme, aby viděl uživatel své hodnocení

    hvezdy.click(function(event){
        // Při kliknutí na hvězdu
        sendToServer(event.target.getAttribute("order"));
        // Když kliknu na nějakou z hvězd, tak pošlu hodnotu pořadí této hvězdy
    });

    function sendToServer(hvezdaVal) {
    // Funkce pro odeslání hodnocení na server
        $.ajax({
        // tvorba requestu na server
            type: 'POST',
            // Typ požadavku POST
            url: '/hodnoceniFilmu',
            // Cílová URL pro odeslání dat
            contentType: 'application/json',
            data: JSON.stringify({
                rating: hvezdaVal,
                filmId: $("main").attr("filmId")
            // Data k odeslání (hodnocení a id filmu)
            }),
            success: function(data){
            // Úspěšná odezva ze serveru
                if (data === "notlogedin") {
                    if (confirm("Nejste zde přihlášen!\nChcete se přihlásit?")) {
                        window.location.href = "/prihlaseni";
                    }
                }
                // Zobrazení okna pro přihlášení, pokud jsme zjistili, že uživatel není přihlášen, není v session
                else if (data === "success") {
                    // Pokud hodnocení bylo úspěšně uloženo
                    defaultVal = hvezdaVal;
                    // Aktualizace výchozí hodnoty na hodnotu hodnocení uživatele
                }
            },
            error: function(error){
                // Chyba při komunikaci se serverem
                console.log(error);
                // chybu si vypíšeme do konzole na webu
            }
        });
    }

});