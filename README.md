
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

HUOM. Repossa myös muita projektin kannalta tärkeitä brancheja, käytännön syistä ei liitetty mainiin. Kannattaa tsekata.




