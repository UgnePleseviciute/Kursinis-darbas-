# Kursinis-darbas-

1. Vektorizavimas.py programa skirta vektorzituoti stuleplius su tekstinėmis įvestimis. Vektorizuojami šie stulepliai: name_t, breadcrumbs_t, description_t, definition.
2. Industrycode.py programa skirta duomenų suskirtstymui į 14 pramonės grupių (Gaunama 14 atskirų failų).

   Darbe buvo bandomi 3 algoritmai, todėl čia numeriu 3 aprašyti metodai bei funkcijos, skirtos "Primam iškirčių identifikavimo būdui". Numeriu 4 aprašyti metodai bei funkcijos, skirtos "Antram išskirčių identifikavimo būdui". Numeriu 5 aprašyti metodai bei funkcijos, skirtos "Trečiam išskirčių identifikavimo būdui".
   3, 4, 5 numeriais pažymėtos išskirčių identifikavimo funkcijos veikia nepriklausomai viena nuo kitos. T.y. norint įvyktdyti 4 numeriu pažymėtą kodą "Antro išskirčių identifikavimo metodas", užtenka prasileisti šiuos failus: 1. Vektorizavimas.py ir 2.Industrycode.py.



  Antras iškirčių identifikavimo metodas
  
4.  Centroid.py: skaičiuojami produkto name_t bei breadcrumbs_t kosinuso panašumai iki savo kategorijos centroido. Analizuojant kiekvieną pramonės kodo kategoriją duomenys sugrupuojami pagal (label) ir paskaičiuojamas kiekvieno produkto kosinuso panašumas iki label medianos centroido atskirai name ir breadcrumbs vektoriams. Produktai žymimi kaip “outliers”, jei jų name ir breadcrumbs reikšmės yra nutolusios per daugiau nei nustatyta slenkstinė reikšmė iki kategorijos centroido. Papildomai pridedama proceso veikimo vizualizacija. 

 

   Norint gauti darbe nagrinėjamus produktus tarp slenkstinės reikšmės 0.5 – 0.5, reikia įvykdyti 2. failą pakeitus slenkstinę reikšmę į 0.55 ir išfiltruoti iš gautų produktų tuos produktus, kurie buvo fiksuoti su slenkstine reikšme 0.5. 



 












