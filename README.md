# ElectionScraper

Tento program slouží ke stažení výsledků voleb do Poslanecké sněmovny ČR z roku 2017.  
Respektive výsledky pro jednotlivé obce ze zvoleného okresu z odkazu: [volby.cz](https://volby.cz/pls/ps2017nss/ps3?xjazyk=CZ)  
Stažené výsledky se uloží do csv souboru ve složce programu.

## Instalace knihoven

Použité knihovny jsou uloženy v souboru `requirements.txt`. Pro instalaci je vhodné vytvořit nové virtuální prostředí a naistalovat takto:
```
$ pip3 install -r requirements.txt
```

## Spuštění programu

Program se spouští z příkazové řádky a vyžaduje dva vstupní argumenty.
```
python election_scraper.py <odkaz-na-okres> <vysledny-soubor>
```

## Ukázka programu

Výsledky hlasování pro okres Brno-venkov:
  1. argument `https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=11&xnumnuts=6203`
  2. argument `brno_venkov.csv`
  
Spuštění programu:
`python election_scraper.py "https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=11&xnumnuts=6203" brno_venkov.csv`
  
Průběh stahování:
```
Stahuji volební výsledky pro okres: Brno-venkov
Nalezeno: 187 obcí.
Stahuji data do souboru 'brno_venkov.csv'.
|##################################################| 187 z 187
Stahování úspěšně dokončeno.
```

Částečný výstup programu:
```
Kód obce,Název obce,Voliči,Vydané obálky,Platné hlasy, ...
582794,Babice nad Svitavou,925,660,655,109,1,2,43,0,53,31,7,3,10,0,0,93,0,39,129,0,3,69,0,2,1,1,58,1,0
582808,Babice u Rosic,553,353,351,32,0,0,18,1,27,30,5,1,6,0,2,37,0,13,93,0,1,25,5,4,1,1,49,0,0
581321,Běleč,160,131,130,13,0,0,25,0,8,14,0,1,0,0,0,11,1,1,30,0,0,14,0,0,0,0,12,0,0
...
```
