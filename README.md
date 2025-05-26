# Kursinis-darbas-

1. Vektorizavimas.py programa skirta vektorizituoti stulpelius su tekstinėmis įvestimis. Vektorizuojami šie stulpeliai: name_t, breadcrumbs_t, description_t, definition.
2. Industrycode.py programa skirta duomenų suskirstymui į 14 pramonės grupių (Gaunama 14 atskirų failų).

Pirmas išskirčių identifikavimo metodas

3. Skaičiuojamas kosinusų panašumas tarp produktų trijų tekstinių laukų vektorių [name_t, breadcrumbs_t, description_t (jei turi)] ir kategorijos oficialaus aprašymo vektorių.

3.1. By_Definition.py algoritmas apskaičiuoja visų trijų tekstinių stulpelių kosinusų panašumus su oficialiu kategorijos aprašymu ir stebima ar gautos reikšmės patenka į pirmąjį decilį.
Funkcija def process_industry_code(code): įkelia produktų duomenis kiekvienam pramonės kodui atskirai. Sugrupuoja duomenis pagal kategoriją (label), kadangi kiekviena pramonės grupė gali turėti daug kategorijų.
Apskaičiuoja kosinuso panašumus tarp: name_t, breadcrumbs_t, description_t (jei turi) ir kategorijos oficialaus apibūdinimo.
Kiekvienam stulpeliui nustato 10% slenkstinę reikšmę
Jei visi trijų produkto stulpelių kosinusų panašumų reikšmės patenka į 10 proc. žemiausių, šie produktai žymimi kaip ALL3.
Jei produktas neturi apibūdinimo, bet jo name_t ir breadcrumbs_t savo stulpeliuose patenka į pirmąjį decilį šie produktai žymimi kaip NB_ONLY.
Išveda rezultatus į du atskirus failus.

3.2. By_definition_manual.py algoritmas apskaičiuoja visų trijų/dviejų tekstinių stulpelių kosinusų panašumus su oficialiu kategorijos aprašymu ir sukuria kombinuotą bendrą panašumą ir pateikia fiksuotą produktų skaičių: t.y. 355 produktų su apibūdinimu (description) ir 514 be apibūdinimo.

3.3. By_definition_2_proc.py algoritmas apskaičiuoja visų trijų/dviejų tekstinių stulpelių kosinusų panašumus su oficialiu kategorijos aprašymu ir sukuria kombinuotą bendrą panašumą. Stebima ar tas panašumas yra tarp 2% žemiausių reikšmių.
Funkcija cosine_sim(a, b): Apskaičiuoja kosinuso panašumą tarp dviejų vektorių. Grąžina reikšmę tarp -1 ir 1, apibūdinančią panašumą (kuo arčiau 1 – tuo panašesni).
Funkcija process_industry_code(code) Analizuoja vieną pramonės šaką (industrycode) ir apskaičiuoja panašumo balus kiekvienam produktui. Sugrupuoja pagal kategorija (label)/
Skaičiuoja kosinuso panašumus tarp produkto vektorių (name_t_vec, breadcrumbs_t_vec, description_t_vec) ir oficialaus kategorijos apibrėžimo (definition_vec).
Grąžina DataFrame su papildomais skaičiavimo stulpeliais (name_score, breadcrumb_score, desc_score).

Norint gauti darbe nagrinėjamą 2-4% prasčiausius rezultatus turinčius produktus, reikia įvykdyti 3.3. failą pakeitus slenkstinę reikšmę į 0.04 ir išfiltruoti iš gautų produktų tuos produktus, kurie buvo fiksuoti su slenkstine reikšme 0.02.



















