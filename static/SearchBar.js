$(document).ready(function(){
    // funkce se spustí, pokud je stránka načtená
    let searchBar = $('#searchBar');
    // na stráce hledá elementy s id = searchBar (input)

    let searchBarList = $('#searchBarList');
    // na stránce najde element id = searchBarList (ul)
    searchBarList.hide();
    // schová se

    searchBar.on('input', ev => {
        // funkce se spustí, když něco napíšeme do searchBaru
        if (searchBar.val() === ''){
            // pokud je searchBar prázdný, tak list chceme vyprázdnit a schovat
            searchBarList.empty();
            searchBarList.hide();
            return;
            // ukončíme funkci, protože nic nechceme posílat na server
        }
        $.ajax({
            // pro komunikaci se serverem
            type: 'POST',
            // http metoda
            url: '/searchBarProcess',
            // kam post posíláme
            contentType: 'application/json',
            // formát posílaných dat (JSON, plain text)
            data: JSON.stringify({val: searchBar.val()}),
            // data, která posíláme na server (val je hodnota v searchBaru)
            success: function(response){
                // funkce se spustí, pokud server správně pošle zprávu zpátky
                console.log(response.data);
                // Vypíše do konzole data přijatá ze serveru
                dataToList(response.data);
                // Zavolá funkci dataToList a předá jí data přijatá ze serveru pro další zpracování
            },
            error: function(error){
                console.log(error);
            }
        });
    })
    function dataToList(data){
        searchBarList.empty();
        // Vyprázdní vyhledávací panel
    for (i = 0; i < data.length; i++) {
        // Pro každou položku v poli `data` provede následující operace
        let film = data[i]
        // Uloží aktuální z pole `data` do proměnné `film`

        let li = document.createElement('li');
        // Vytvoří nový element <li> (položka seznamu)
        let a = document.createElement('a');
        // Vytvoří nový element <a> (odkaz)

        a.textContent = film['title'];
        // Nastaví text odkazu <a> na hodnotu atributu 'title' z aktuálního objektu `film`
        a.setAttribute('href', '/film/' + film['imdbId']);
        // Nastaví atribut `href` odkazu na cílovou URL filmu pomocí ID filmu
        li.appendChild(a);
        // Přidá vytvořený odkaz <a> do položky seznamu <li>

        searchBarList.append(li)
        // Přidá vytvořenou položku seznamu <li> do seznamu `searchBarList`
        searchBarList.show();
        // Zobrazí seznam `searchBarList`
    }
}
});
