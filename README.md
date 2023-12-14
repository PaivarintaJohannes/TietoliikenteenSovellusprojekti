
# Tietoliikenteen sovellusprojekti. Päivärinta, Kokko

![Posteri](https://github.com/PaivarintaJohannes/TietoliikenteenSovellusprojekti/blob/main/posteri.png)

# Luettelo ja selitykset tehdyistä ohjelmista:

## 1. Kiihtyvyysdatan mittaus ja lähetys
Datan mittaus toteutettiin Adxl335-kiihtyvyysanturilla joka kytkettiin Nordicin alustalle. Datan mittaus sekä valmius Bluetoothin yli lähettämiseen tapahtuu samassa ohjelmassa (datan vastaanottamien eri ohjelmassa).
Ohjelma vaatii nordicin oman ADC-kirjaston analogisen signaalin lukemiseen sekä Bluetooth-kirjastot. Ohjelma pyörittää for-loopilla anturidatan käsittelyä ja antaa yksitellen jokaisen akselin arvon. 
Ennen kuin kolme (x,y,z)-arvoa annetaan järjestyksessä, annetaan suunta-arvo (1-6). Suunta-arvoa muutetaan Nordicin painonapeilla.  


HUOM. Repossa myös muita projektin kannalta tärkeitä brancheja, käytännön syistä ei liitetty mainiin. Kannattaa tsekata.




