# ieps_3
Tretja seminarska naloga pri predmetu IEPS

# Navodila za generacijo podatkov za bazo
1.) Program potrebuje python knjižnice bs4, nltk, os in pickle  
2.) Program potrebuje tudi dodano datoteko s slovenskimi stopwordsi v pravilni direktorij inštalacije knjižnice nltk  
3.) Prenesite repozitorj  
4.) Razpakirajte datoteke.zip znotraj prenesenega repozitorija  
5.) V konzoli se premaknite v repozitorij  
6.) Poženite ukaz python test2.py  
7.) Programi ustvari datoteko "final_take2.pickle", ki se uporabi za generacijo baze  


# Navodila za zagon
1.) Pred zagonom potrebujemo še (če nimamo) naslednje knjižnice: sqlite3, bs4, os, time, sys, pickle.

2.) Vsebino "indexer" direktorija je treba razpakirati v nek direktorij, kjer se nahaja direktorij s html datotekami imenovan "data_websites" in podatkovna baza imenovana "inverted-index.db". To je pomembno, saj so nekatere lokacije fiksirane.

3.) Ko je to urejeno, lahko zaženemo program: python Query.py ind sistem SPOT za iskanje v bazi ali python Query.py seq sistem SPOT za sekvenčno iskanje. V osnovi se kliče tako: python Query.py način_iskanja naštej_iskane_besede.
