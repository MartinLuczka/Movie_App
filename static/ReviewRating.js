$(document).ready(function(){
// Když je dokument připravený (plně načtený), spustí se tento kód
    thumbsDivs = $('ul .thumbsDiv')
     // Vybere všechny elementy, které jsou uvnitř <ul> a mají třídu "thumbsDiv"

    thumbsDivs.each(function() {
        updateVisual($(this))
        // Pro každý z těchto vybraných elementů zavolá funkci updateVisual
    })

    if (jePrihlaseny() === 1) {
    // Jestliže je uživatel přihlášen (funkce jePrihlaseny vrací 1)
        thumbsDivs.children("img").click(function () {
        // Nastaví click event handler na všechny <img> elementy uvnitř thumbsDivs
        thumbsDiv = $(this).parent()
        // Získá parent element palce

        if (thumbsDiv.attr("thumbsRating") === $(this).attr("choiceVal")) {
        // Pokud je hodnocení stejné jako aktuální
            thumbsDiv.attr("thumbsRating", -1)
            // Resetuje hodnocení do hodnoty -1
            $(this).prev("h5").text(parseInt($(this).prev("h5").text()) - 1)
            // Sníží hodnotu zobrazovaného textu o 1, grafická responsivita
        }
        else {
            if (thumbsDiv.attr("thumbsRating") === "-1") {
            // Pokud ještě není hodnocení, tento případ odpovídá hodnotě nastavené do čísla -1
                $(this).prev("h5").text(parseInt($(this).prev("h5").text()) + 1)
                // Zvýší hodnotu zobrazovaného textu o 1, grafická responsivita
             }
            else {
            // Změna hodnocení
                $(this).prev("h5").text(parseInt($(this).prev("h5").text()) + 1)
                // Přidá + 1 tam, kde jsme klikli
                $(this).siblings("img").prev("h5").text(parseInt($(this).siblings("img").prev("h5").text()) - 1)
                // siblings - hledej elementy na stejné úrovni, druhému elementu sníží hodnotu o 1 (změnili jsme hodnocení), zpětná vazba
            }
            thumbsDiv.attr("thumbsRating", $(this).attr("choiceVal"))
            // Nastaví nové hodnocení na hodnotu atributu choiceVal
        }

        updateReviewRating(thumbsDiv.parent().parent("li").attr("reviewId"), thumbsDiv.attr("thumbsRating"))
        // Odešle aktualizované hodnocení na server pomocí funkce updateReviewRating
        updateVisual(thumbsDiv)
        // Aktualizace barevného zobrazení palců

    })
    }
    else {
    // Pokud uživatel není přihlášen
        thumbsDivs.children("img").click(function () {
        // Nastaví click event handler, který se spustí při kliknutí
            if (confirm("Nejste zde přihlášen!\nChcete se přihlásit?")) {
            // Pokud uživatel není přihlášen, zobrazí se potvrzovací okno s dotazem, zda se chce uživatel přihlásit
                        window.location.href = "/prihlaseni";
                        // Možnost přesměrování
                    }
        })
    }

    function updateVisual(div) {
    // Funkce, která aktualizuje vizuální zobrazení palců
        thumbsRating = parseInt(div.attr("thumbsRating"))
        // Získá aktuální hodnocení (stav) z atributu thumbsRating
        div.children("img.thumbsup").attr("src", "/static/imgs/thumb_up" +((thumbsRating === 1)?"_full":"")+".png");
        // Pokud je thumbsRating nastaven do 1, tak se palec nahoru vybarví do zelena
        div.children("img.thumbsdown").attr("src", "/static/imgs/thumb_down" +((thumbsRating === 0)?"_full":"")+".png");
        // Pokud je thumbsRating nastaven do 0, tak se palec dolů vybarví do červena

    }

    function updateReviewRating(reviewId, thumbsRating) {
    // Funkce, která odesílá nové hodnocení na server
        $.ajax({
        // Tvorba HTTP requestu
            type: "POST",
            url: "/setReviewRating",
            // URL, na kterou se má request poslat
            contentType: 'application/json',
            data: JSON.stringify({
                reviewId: reviewId,
                rating: thumbsRating
                // V requestu se posílá: ID recenze a nové hodnocení
            }),
            success: function(data){
            // Když se request úspěšně provede
                console.log(data)
                // Vypíše data do konzole
            },
            error: function(error){
            // Pokud nastane chyba
                console.log(error)
                // Vypíše chybu do konzole
            }
        });
    }

    function jePrihlaseny(){
    // Funkce, která kontroluje, zda je uživatel přihlášen
        let prihlaseni = 0
        // Defaultní hodnota je 0 --> není přihlášen
        $.ajax({
            url: "/jePrihlaseny",
            // URL, na kterou se má request poslat
            type: 'GET',
            dataType: 'text',
            async: false,
            // požadavek má být synchroní, zde nastávala chyba daná tím, že se funkce nestihla udělat a funkce vracela vždy deklarovanou hodnotu prihlaseni
            success: function(data) {
                prihlaseni = parseInt(data)
                // Pokud je request úspěšný, nastaví hodnotu prihlaseni na vrácená data, chceme datový typ Integer
            },
            error: function(jqXHR, textStatus, errorThrown) {
                console.error('Error: ' + textStatus, errorThrown);
                // Pokud nastane chyba, vypíše chybu do konzole
            }
        });
        return prihlaseni
        // Vrátí hodnotu, která nám udává, zda je uživatel přihlášen
    }

});