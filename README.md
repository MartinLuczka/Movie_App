# MOVIE APP

## Jak vznikl tento projekt ?

Projekt byl vytvořen jako závěrečná práce do předmětu 
**Programování ve 3. ročníku** na 
<a href = "https://www.spseol.cz/">SPŠEOL</a>. 
Zadáním bylo si v libovolném programovacím jazyce zpracovat projekt. 
To, o čem projekt měl být, jsme si mohli vybrat sami. 
Měl jsem více nápadů, ale volba padla na **Webovou aplikaci vytvořenou pomocí webového frameworku Flask a databázovým systémem SQLite**.

<div style="display: flex; align-items: center;">
    <img style="margin-left: 30px" src="README_file_imgs/Flask_logo.png" alt="Logo Flasku" width="220"/>
    <img style="margin-left: 100px" src="README_file_imgs/SQLite_logo.png" alt="Logo SQLite" width="220"/>
</div>

## Proč zrovna webová aplikace zaměřená na hodnocení filmů ?

Již od malička jsem měl rád filmy a čím víc přibývalo těch, 
které jsem již viděl, tím víc se mi zamlouvala myšlenka, 
že by člověk všechny filmy, které viděl, měl na jednom místě. 
A ještě k tomu ohodnocené či okomentované ! 
Vždy se mi tím pádem líbily stránky jako 
<a href = "https://www.csfd.cz/">ČSFD</a> 
či zahraniční <a href = "https://www.imdb.com/">IMDb</a> a samozřejmě další. 
Tyto stránky na tomto projekty zanechaly také svůj otisk, 
ale snažil jsem se v několika věcech aspoň mírně odlišit. 
To, jak se mi to povedlo, zhodnotíte už Vy. 
Něco podobného jsem už řešil v rámci programu napsaného čistě v Pythonu (odkaz: <a href="https://github.com/MartinLuczka/MOVIE-APP">Stará Movie App</a>), 
ale tady je to samozřejmě posunuto na mnohem vyšší úroveň.

> [!TIP]
> Pokud by Vás mimochodem zajímalo něco na způsobem mé stránky, ale co se týče videoher, tak určitě můžu doporučit stránku <a href="https://www.backloggd.com/">Backloggd</a>, na které jsem si sám před nedávnem založil účet.

## Jak jsem projekt vytváře, jak jsem postupoval, v jakém vývojovém prostředí jsem pracoval ?

Projekt jsem si rozdělil na dvě části. 
**Funkční stránka projektu** představovala práci s Flaskem a vytváření metod pro práci s databází.
V této části jsem si také musel udělat HTML stránky, 
ale používal jsem pouze základní elementy a všechno jsem dával pod sebe.
Do této části také samozřejmě spadají také funkční JavaScript soubory, 
se kterými jsem ale popravdě bojoval až do dokončení projektu.

<br>**Stylování vytvořených HTML stránek**
byla řekněmě druhá část projektu. Ve spojitosti tady s tímto mě napadlo si
vyzkoušet nějaký framework, podle kterého bych své webové stránky nastyloval.
Po chvíli hledání mých možností padla volba na **CSS framework** 
<a href = "https://getbootstrap.com/">**Bootstrap**</a>, se kterým jsem se po
pár tutoriál videích seznámil dostatečně na to, abych s ním mohl pracovat.
V práci mi také pomohla velice názorná a příklady proložená 
<a href = "https://getbootstrap.com/docs/3.4/css/">Dokumentace</a> (starší verze, ale 
vše je pěkně pohromadě). Při stylování jsem si přidáváním některých
prvků rozházel funkčnost některých prvků, ale vše jsem nakonec vyřešil a opravil.

<br>Projekt jsem začal vytvářet ve vývojovém prostředí programu **Visual Studio Code**,
avšak s vidinou šikovnější práce s databází a jednotlivými tabulkami jsem
přešel na vývojové prostředí programu <a href = "https://www.jetbrains.com/pycharm/">**PyCharm**</a>,
se kterým jsem byl po dobu celé své práce naprosto spokojen.
Nejdřív jsem zaregistroval pouze program <a href="https://www.jetbrains.com/datagrip/?var=light">Datagrip<a/>,
ale ten je do PyCharmu v podstatě integrován. 
Oba programy totiž spadají pod (dokonce českou) softwarovou společenost
<a href = "https://www.jetbrains.com/">**JetBrains**</a>,
která podobných programů provozuje celou řadu.

<div style="display: flex; align-items: center; flex-wrap: wrap;">
    <img style="margin-left: 25px; margin-bottom: 15px" src="README_file_imgs/Bootstrap_logo.png" alt="Logo Bootstrapu" width="170"/>
    <img style="margin-left: 25px; margin-bottom: 15px" src="README_file_imgs/PyCharm-logo.png" alt="Logo PyCharmu" width="170"/>
    <img style="margin-left: 25px; margin-bottom: 15px" src="README_file_imgs/JetBrains_logo.png" alt="Logo JetBrains" width="190"/>
</div>

> [!TIP]
> Pokud jste studentem a máte **ISIC kartu**, tak si můžete v rámci produktů
> společnosti **JetBrains** aktivovat studentské license, které jsou tak pro
> vás přístupné **zadarmo**.

## Jak jsem si vytvořil databázi tolika filmů ?

Databáze je tvořena **TOP 250 filmy**, které jsem si pomocí Python skriptů
vytáhl ze stránek <a href = "https://www.imdb.com/">IMDb</a>. Tyto Python soubory se nachází ve složce
*insertovac*, kterou jsem skrze celý projekt necommitoval, ale
zahrnu ji v rámci posledních commitů k tomuto projektu.
Tímto jsme tedy získaly všechny důležitá data k filmu.

Byly tu ovšem určité problémy, které jsem vyřešil přidáním dalších 
Python souborů, v našem případě dvěma dalšími. Odkazy na
trailery fungovaly vždy jen chvíli, tak jsem si do databáze nechal
poslat odkazy na youtube videa (Python vyhledá název filmu + trailer
na stránce <a href = "https://www.youtube.com/">Youtube</a>) a Python
program již vezme a do databáze uloží adresu prvního výsledku).  

Dále byl problém s popisem filmu v angličtině. Ten jsem vyřešil tak, 
že si na stránkách <a href = "https://www.csfd.cz/">ČSFD</a> vyhledávám
jednotlivé filmy a vybírám si text z popisu filmu u prvního výsledku.
Jelikož jsou to většinou ty nejznámnější filmy, tak první výsledek je
ve všem případech s největší pravděpodobností dobře (nenarazil jsem na chybu).
Filmy, u kterých chyběl popisek (nebyl nebo se nevyhledal celý název filmu, ČSFD
má omezen počet znaků ve vyhledávání na 50 - vyhodilo chybu), tak
jsem popisky doplnit manuálně za pomoci internetu.

## Python souborů je v projektu strašně moc a některé jsou dost rozsáhlé, jak se v tom mám vyznat ?

Nebojte, myslel jsem na Vás (ale také trochu na sebe). Jelikož jsem nic
podobného nikdy nedělal, tak jsem si chtěl v kódu udržovat nějaký pořádek
a přehled. Protože jsem se chtěl koncepty **hlavně naučit**, tak v **Pythonu**
a **JavaScriptu** jsou (skoro) všechny řádky zakomentovány. Některé komentáře
se tam trochu zbytečně opakují několikrát, ale pokud by někdo přeskakoval,
tak jsem to tak raději nechal. V **HTML** jsem kód v podstatě moc nekomentoval,
nemyslím si, že by to přineslo moc užitku a já osobně se v tom lépe vyznám
spíše takto.

<div style="display: flex; align-items: center;">
    <img style="margin-left: 35px; margin-bottom: 20px" src="README_file_imgs/comment_PY_script.png" alt="Ukázka komentáře v Pythonu" width="250"/>
    <img style="margin-left: 35px;" src="README_file_imgs/comment_JS_script.png" alt="Ukázka komentáře v JavaScriptu" width="250"/>
</div>


