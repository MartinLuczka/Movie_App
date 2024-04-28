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
                // funkce se spustí, pokud server správně pošle zpátky zprávu
                console.log(response.data);
                dataToList(response.data);
            },
            error: function(error){
                console.log(error);
            }
        });
    })
    function dataToList(data){
        searchBarList.empty();
    for (i = 0; i < data.length; i++) {
        let film = data[i]

        let li = document.createElement('li');
        let a = document.createElement('a');

        a.textContent = film['title'];
        a.setAttribute('href', '/film/' + film['imdbId']);
        li.appendChild(a);

        searchBarList.append(li)
        searchBarList.show();
    }
}
});
