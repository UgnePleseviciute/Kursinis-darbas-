# Kursinis-darbas-

1. Vektorizavimas.py programa skirta vektorzituoti stuleplius su tekstinėmis įvestimis. Vektorizuojami šie stulepliai: name_t, breadcrumbs_t, description_t, definition.
2. Industrycode.py programa skirta duomenų suskirtstymui į 14 pramonės grupių (Gaunama 14 atskirų failų).

Šiame metode identifikuojami produktai, kurie galimai netinkamai priskirti savo kategorijoms, remiantis jų pavadinimo (name_t_vec) ir kelio nuorodos (breadcrumbs_t_vec) vektorių kosinuso panašumu iki kategorijos centroido.Produktai laikomi išskirtimis, jei jų kombinuotas panašumas (name + breadcrumbs) yra reikšmingai žemas – pagal z-score žemiau -3.

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
                              Kiekvienam produktui iš df_suspicious paskaičiuojams kosinuso panašumas tarp jo description_t_vec ir savo kategorijos centroido.
                              Produktas laikomas blogai priskirtu jei desc_vs_centroid_cosine < 0.5
                              
   Norint gauti darbe nagrinėjamą -3 <= z <-2.5 z įverčių aibe, reikia įvykdyti 5.1 failą pakeitus [ outlier_mask = z_scores < -Z_THRESHOLD ] į [outlier_mask = (z_scores >= -3.0) & (z_scores <= -2.5)].

   



 












