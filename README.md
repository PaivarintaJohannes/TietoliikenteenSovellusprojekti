
# TVT22SPL Tietoliikenteen sovellusprojekti.
## Johannes Päivärinta, Niko Kokko

![Posteri](https://github.com/PaivarintaJohannes/TietoliikenteenSovellusprojekti/blob/main/posteri.png)


# Selitykset ohjelmista:

## 1. Kiihtyvyysanturidatan mittaus ja lähetys

Datan mittaus toteutettiin Adxl335-kiihtyvyysanturilla joka kytkettiin Nordicin alustalle. Datan mittaus sekä valmius Bluetoothin yli lähettämiseen tapahtuu samassa ohjelmassa (datan vastaanottamien eri ohjelmassa).
Ohjelma vaatii nordicin oman ADC-kirjaston analogisen signaalin lukemiseen sekä Bluetooth-kirjastot. Ohjelma pyörittää for-loopilla anturidatan käsittelyä ja antaa yksitellen jokaisen akselin arvon. 
Ennen kuin kolme (x,y,z)-arvoa annetaan järjestyksessä, annetaan suunta-arvo (1-6). Suunta-arvoa muutetaan Nordicin painonapeilla.  
Alhaalla kuvassa näkyvä app_sensor_value siis lähetetään reaaliaikaisesti siihen laitteeseen (tässä tapauksessa Raspberry Pi), joka luo Bluetooth-yhteyden tähän systeemiin.

![forloop](https://github.com/PaivarintaJohannes/TietoliikenteenSovellusprojekti/blob/main/forlooppi.png)

## 2. Raspberry Pi:llä datan vastaanotto ja tietokantaan lähetys

Raspberrylle kirjoitettiin ohjelma joka luo Bt-yhteyhden ennalta määritetyillä osoitteilla nordicin alustaan, joka pyörittää ylempänä mainittua ohjelmaa. Ohjelman käynnistyessä se vastaanottaa tietyn määrän arvoja ja tallettaa ne taulukoihin.
Kun arvot on talletettu taulukoihin, ne lähetetään verkon yli mysql.connector-kirjaston avulla tietokantaan. Tietokantaan lähettäminen vaati tunnukset, salasanat sekä osoitteet. Nämä laitettiin dotenv-tiedostoon (jota ei sisällytetty tietenkään githubiin). Lähetettävä data koostuu ryhmäid:stä (jotta jokaisen ryhmän oma data erottuu joukosta) ja suunta- sekä x,y,z-arvoista.

![databasekoodi](https://github.com/PaivarintaJohannes/TietoliikenteenSovellusprojekti/blob/main/database.png)

## 3. Datan haku tietokannasta ja K-Means algoritmi

Data haettiin tietokannasta oman ryhmäid:n avulla yksinkertaisella soketti-skriptillä pythonilla. Data valmisteltiin haluttuun muotoon pandas-kirjaston avulla. Itse K-Means-ohjelma tuottikin enemmän työtä - paljolti debuggaamista. Ohjelman tarkoitus on lukea koko anturidata csv-tiedostosta ja ajaa ne algoritmin läpi. Algoritmi tuottaa datan keskipisteet jokaiselle klusterille. Näiden keskipisteiden avulla voidaan sitten jatkossa luokitella kaikki kiihtyvyysanturin arvot kuuteen eri klusteriin. 
Ohjelma koostuu siis datan ja muuttujien määrittelystä sekä eri funktioista. Itse Kmeans-funktio käy läpi jokaisen datapisteen ja laskee kunkin etäisyyden kuuteen eri generoituun alkukeskipisteeseen ja valitsee sen pisteen, johon oli lyhyin etäisyys. Jokaiselle tämmöiselle "voittajalle" annetaan yksi countti per datapiste. Myöhemmissä funktioissa keskipisteiden datapointit summataan yhteen ja jaetaan counttien määrällä. Jos jokin keskipiste ei saanut yhtään "voittoa", tälle arvotaan uudet koordinaatit. Tällä tavoin datalle löytyy oikeat keskipisteet. Lopuski tulosta visualisoidaan plottaamalla data, ja algoritmin tuottamat keskipisteet.



HUOM. Repossa myös muita projektin kannalta tärkeitä brancheja, käytännön syistä ei liitetty mainiin. Kannattaa tsekata.




