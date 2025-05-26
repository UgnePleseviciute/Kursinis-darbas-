# Kursinis-darbas-

1. Vektorizavimas.py programa skirta vektorzituoti stulpelius su tekstinėmis įvestimis. Vektorizuojami šie stulepliai: name_t, breadcrumbs_t, description_t, definition.
2. Industrycode.py programa skirta duomenų suskirstymui į 14 pramonės grupių (Gaunama 14 atskirų failų).

   Darbe buvo bandomi 3 algoritmai, todėl čia numeriu 3 aprašyti metodai bei funkcijos, skirtos "Primam iškirčių identifikavimo būdui". Numeriu 4 aprašyti metodai bei funkcijos, skirtos "Antram išskirčių identifikavimo būdui". Numeriu 5 aprašyti metodai bei funkcijos, skirtos "Trečiam išskirčių identifikavimo būdui".
   3, 4, 5 numeriais pažymėtos išskirčių identifikavimo funkcijos veikia nepriklausomai viena nuo kitos. T.y. norint įvyktdyti 4 numeriu pažymėtą kodą "Antro išskirčių identifikavimo metodas", užtenka prasileisti šiuos failus: 1. Vektorizavimas.py ir 2.Industrycode.py.

   Pirmas išskirčių identifikavimo metodas

3.  Skaičiuojamas kosinusų panašumas tarp produktų trijų tekstinių laukų vektorių [name_t, breadcrumbs_t, description_t (jei turi)] ir kategorijos oficialaus aprašymo vektorių.
   
      3.1.  By_Definition.py algoritmas apskaičiuoja visų trijų tekstinių stuleplių kosinusų panašumus su oficialiu kategorijos aprašymu ir stebima ar gautos reikšmės patenka į pirmąjį decilį. 
   Funkcija def process_industry_code(code): įkelia produktų duomenis kievienam pramonės kodui atskirai. Sugrupuoja duomenis pagal kategoriją (label), kadangi kiekvina pramonės grupė gali turėti daug kategorijų.
                                                Apskaičiuoja kosinuso panašumus tarp: name_t, breadcrumbs_t, description_t (jei turi) ir kategorijs oficialaus apibūdinimo.
                                                Kiekvienam stulpeliui nustato 10% slenkstinę reikšmę
                                                Jei visi trijų produkto stuleplių kosinusų panašumų reikšmės patenka į 10 proc. žemiasių, šie produktai žymimi kaip ALL3.
                                                Jei produktas neturi apibūdinimo, bet jo name_t ir breadcrumbs_t savo stulepliuose patenka į pirmąjį decilį šie produktai žymimi kaip NB_ONLY.
                                                Išveda rezultatus į du atskirus failus.

      3.2.  By_definition_manual.py algoritmas apskaičiuoja visų trijų/dviejų tekstinių stuleplių kosinusų panašumus su oficialiu kategorijos aprašymu ir sukuria kombinuotą bendrą panašumą ir pateikia fiksuotą       produktų skaičių: t.y. 355 produktų su apibūdinimu (description) ir 514 be apibūdinimo.

      3.3.  By_definition_2_proc.py algoritmas apskaičiuoja visų trijų/dviejų tekstinių stuleplių kosinusų panašumus su oficialiu kategorijos aprašymu ir sukuria kombinuotą bendrą panašumą. Stebima ar tas panašumas yra tarp 2% žemiausių reikšmių.
    Funkcija cosine_sim(a, b): Apskaičiuoja kosinuso panašumą tarp dviejų vektorių. Grąžina reikšmę tarp -1 ir 1, apibūdinančią panašumą (kuo arčiau 1 – tuo panašesni).
    Funkcija process_industry_code(code) Analizuoja vieną pramonės šaką (industrycode) ir apskaičiuoja panašumo balus kiekvienam produktui. Sugrupuoja pagal kategorija (label)/
                                            Skaičiuoja kosinuso panašumus tarp produkto vektorių (name_t_vec, breadcrumbs_t_vec, description_t_vec) ir oficialaus kategorijos apibrėžimo (definition_vec).
                                            Gražina DataFrame su papildomais skaičiavimo stulpeliais (name_score, breadcrumb_score, desc_score).                         
  
   Norint gauti darbe nagrinėjamą 2-4% prasčiausius rezultatus turinčius produktus, reikia įvykdyti 3.3. failą pakeitus slenkstinę reikšmę į 0.04 ir išfiltruoti iš gautų produktų tuos produktus, kurie buvo fiksuoti su slenkstine reikšme 0.02.

  Antras iškirčių identifikavimo metodas
  
4.  Centroid.py: skaičiuojami produkto name_t bei breadcrumbs_t kosinuso panašumai iki savo kategorijos centroido. Analizuojant kiekvieną pramonės kodo kategoriją duomenys sugrupuojami pagal (label) ir paskaičiuojamas kiekvieno produkto kosinuso panašumas iki label medianos centroido atskirai name ir breadcrumbs vektoriams. Produktai žymimi kaip “outliers”, jei jų name ir breadcrumbs reikšmės yra nutolusios per daugiau nei nustatyta slenkstinė reikšmė iki kategorijos centroido. Papildomai pridedama proceso veikimo vizualizacija. 

 

   Norint gauti darbe nagrinėjamus produktus tarp slenkstinės reikšmės 0.5 – 0.5, reikia įvykdyti 2. failą pakeitus slenkstinę reikšmę į 0.55 ir išfiltruoti iš gautų produktų tuos produktus, kurie buvo fiksuoti su slenkstine reikšme 0.5. 

   Trečias išskirčių identifikavimo metodas
   
5. Šiame metode identifikuojami produktai, kurie galimai netinkamai priskirti savo kategorijoms, remiantis jų pavadinimo (name_t_vec) ir kelio nuorodos (breadcrumbs_t_vec) vektorių kosinuso panašumu iki kategorijos centroido.Produktai laikomi išskirtimis, jei jų kombinuotas panašumas (name + breadcrumbs) yra reikšmingai žemas – pagal z-score žemiau -3.

   5.1. z-Score.py programoje
                              Duomenys sugrupuojami pagal kategorijas (label).
                              Kiekvienai kategorijai apskaičiuojamas centroidas:
                                          name_centroid – medianinis vektorius iš name_t_vec.
                                          breadcrumbs_centroid – medianinis vektorius iš breadcrumbs_t_vec.
                              Skaičiuojami kosinuso panašumai tarp kiekvieno produkto vektoriaus ir centroido.
                              Apskaičiuojamas kombinuotas panašumas
                              Apskaičiuojamas z-score, ir produktai, kurių z < -3.0, laikomi išskirtimis.

   5.2. TextCleaning.py programoje identifikuojamos blogos teksto įvestis naudojant 6 funkcijas:
                              def flag_noisy_symbols - pritaikyta patikrinti ar produktų pavaidinimai neturi įvairių netikslingų simbolių, kurie arba nesuteikia prasmės. Ši funkcija ieško šių simbolių @, #, ^, ~
                              def flag_only_digits - tikrina, ar pavadinimas nėra sudarytas vien iš skaičių.
                              def flag_non_latin - tikrina, ar produkto pavadinimas nėra tik vienas žodis.
                              def flag_name_is_single_word - tikrina ar produkto pavadinimas yra sudarytas tik iš lotyniškų raidžių.
                              def flag_generic_breadcrumbs -tikrina, ar kelio nuoroda iki produkto nėra sudaryta vien tik iš prasmės neturinčių žodžių ar jų junginių.
                              def flag_single_breadcrumb_word - tikrina, ar kelio nuoroda nėra sudaryta tik iš vieno žodžio, pašalinus perteklinius žodžius.

   5.3. Describtion_vs_centroid.py  programa skirta patikrinti ar įtartini produktai yra galimai neteisingai priskirti kategorijoms, naudojant kosinuso panašumą tarp produkto aprašymo vektoriaus (description_t_vec) ir atitinkamos kategorijos centroido, apskaičiuoto iš visų tos kategorijos produktų aprašymų.
                              Kiekvienam produktui iš df_suspicious paskaičiuojamas kosinuso panašumas tarp jo description_t_vec ir savo kategorijos centroido.
                              Produktas laikomas blogai priskirtu jei desc_vs_centroid_cosine < 0.5
                              
   Norint gauti darbe nagrinėjamą -3 <= z <-2.5 z įverčių aibe, reikia įvykdyti 5.1 failą pakeitus [ outlier_mask = z_scores < -Z_THRESHOLD ] į [outlier_mask = (z_scores >= -3.0) & (z_scores <= -2.5)].

   



 












