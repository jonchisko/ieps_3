
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

stop_words_slovene = set(stopwords.words("slovenian")).union(set(
        ["ter","nov","novo", "nova","zato","ĹĄe", "zaradi", "a", "ali", "april", "avgust", "b", "bi", "bil", "bila", "bile", "bili", "bilo", "biti",
         "blizu", "bo", "bodo", "bojo", "bolj", "bom", "bomo", "boste", "bova", "boĹĄ", "brez", "c", "cel", "cela",
         "celi", "celo", "d", "da", "daleÄ", "dan", "danes", "datum", "december", "deset", "deseta", "deseti", "deseto",
         "devet", "deveta", "deveti", "deveto", "do", "dober", "dobra", "dobri", "dobro", "dokler", "dol", "dolg",
         "dolga", "dolgi", "dovolj", "drug", "druga", "drugi", "drugo", "dva", "dve", "e", "eden", "en", "ena", "ene",
         "eni", "enkrat", "eno", "etc.", "f", "februar", "g", "g.", "ga", "ga.", "gor", "gospa", "gospod", "h", "halo",
         "i", "idr.", "ii", "iii", "in", "iv", "ix", "iz", "j", "januar", "jaz", "je", "ji", "jih", "jim", "jo",
         "julij", "junij", "jutri", "k", "kadarkoli", "kaj", "kajti", "kako", "kakor", "kamor", "kamorkoli", "kar",
         "karkoli", "katerikoli", "kdaj", "kdo", "kdorkoli", "ker", "ki", "kje", "kjer", "kjerkoli", "ko", "koder",
         "koderkoli", "koga", "komu", "kot", "kratek", "kratka", "kratke", "kratki", "l", "lahka", "lahke", "lahki",
         "lahko", "le", "lep", "lepa", "lepe", "lepi", "lepo", "leto", "m", "maj", "majhen", "majhna", "majhni",
         "malce", "malo", "manj", "marec", "me", "med", "medtem", "mene", "mesec", "mi", "midva", "midve", "mnogo",
         "moj", "moja", "moje", "mora", "morajo", "moram", "moramo", "morate", "moraĹĄ", "morem", "mu", "n", "na", "nad",
         "naj", "najina", "najino", "najmanj", "naju", "najveÄ", "nam", "narobe", "nas", "nato", "nazaj", "naĹĄ", "naĹĄa",
         "naĹĄe", "ne", "nedavno", "nedelja", "nek", "neka", "nekaj", "nekatere", "nekateri", "nekatero", "nekdo",
         "neke", "nekega", "neki", "nekje", "neko", "nekoga", "nekoÄ", "ni", "nikamor", "nikdar", "nikjer", "nikoli",
         "niÄ", "nje", "njega", "njegov", "njegova", "njegovo", "njej", "njemu", "njen", "njena", "njeno", "nji",
         "njih", "njihov", "njihova", "njihovo", "njiju", "njim", "njo", "njun", "njuna", "njuno", "no", "nocoj",
         "november", "npr.", "o", "ob", "oba", "obe", "oboje", "od", "odprt", "odprta", "odprti", "okoli", "oktober",
         "on", "onadva", "one", "oni", "onidve", "osem", "osma", "osmi", "osmo", "oz.", "p", "pa", "pet", "peta",
         "petek", "peti", "peto", "po", "pod", "pogosto", "poleg", "poln", "polna", "polni", "polno", "ponavadi",
         "ponedeljek", "ponovno", "potem", "povsod", "pozdravljen", "pozdravljeni", "prav", "prava", "prave", "pravi",
         "pravo", "prazen", "prazna", "prazno", "prbl.", "precej", "pred", "prej", "preko", "pri", "pribl.",
         "pribliĹžno", "primer", "pripravljen", "pripravljena", "pripravljeni", "proti", "prva", "prvi", "prvo", "r",
         "ravno", "redko", "res", "reÄ", "s", "saj", "sam", "sama", "same", "sami", "samo", "se", "sebe", "sebi",
         "sedaj", "sedem", "sedma", "sedmi", "sedmo", "sem", "september", "seveda", "si", "sicer", "skoraj", "skozi",
         "slab", "smo", "so", "sobota", "spet", "sreda", "srednja", "srednji", "sta", "ste", "stran", "stvar", "sva",
         "t", "ta", "tak", "taka", "take", "taki", "tako", "takoj", "tam", "te", "tebe", "tebi", "tega", "teĹžak",
         "teĹžka", "teĹžki", "teĹžko", "ti", "tista", "tiste", "tisti", "tisto", "tj.", "tja", "to", "toda", "torek",
         "tretja", "tretje", "tretji", "tri", "tu", "tudi", "tukaj", "tvoj", "tvoja", "tvoje", "u", "v", "vaju", "vam",
         "vas", "vaĹĄ", "vaĹĄa", "vaĹĄe", "ve", "vedno", "velik", "velika", "veliki", "veliko", "vendar", "ves", "veÄ",
         "vi", "vidva", "vii", "viii", "visok", "visoka", "visoke", "visoki", "vsa", "vsaj", "vsak", "vsaka", "vsakdo",
         "vsake", "vsaki", "vsakomur", "vse", "vsega", "vsi", "vso", "vÄasih", "vÄeraj", "x", "z", "za", "zadaj",
         "zadnji", "zakaj", "zaprta", "zaprti", "zaprto", "zdaj", "zelo", "zunaj", "Ä", "Äe", "Äesto", "Äetrta",
         "Äetrtek", "Äetrti", "Äetrto", "Äez", "Äigav", "ĹĄ", "ĹĄest", "ĹĄesta", "ĹĄesti", "ĹĄesto", "ĹĄtiri", "Ĺž", "Ĺže",
         "svoj", "jesti", "imeti","\u0161e", "iti", "kak", "www", "km", "eur", "paÄ", "del", "kljub", "ĹĄele", "prek",
         "preko", "znova", "morda","kateri","katero","katera", "ampak", "lahek", "lahka", "lahko", "morati", "torej"]))


#this function tokanizes then removes stopwords

def process_string(s):

    #splits by new line
    razdeljen = s.split("\n")

    #removes all the lines that might be a comment, code or empty
    #add a space at the end of every line so that we can join later
    razdeljen = [x + " " for x in razdeljen if x and "/*" not in x and ";" not in x and "*/" not in x]

    #join all the lines to create a single string
    obdelan_tekst = "".join(razdeljen)

    #tokenize that string
    a = word_tokenize(obdelan_tekst)

    #remove all the punctuation
    a = [x for x in a if x != "," and x != ";" and x != "(" and x != ")" and x != "." and x != ":" and x != "!" and x != "?" and x != "<" and x != ">" and x != "#"]

    #remove the stopwords and turn everything to lower case
    vocab = [word.lower() for word in a if word.lower() not in stop_words_slovene]

    #return the final list of processed words
    return vocab


if __name__ == "__main__":
    print(process_string("Domen je največji kral vseh časov majkemi. Vsakič znova me preseneča. Morda sem jaz tisti, ki torej nekaj dela narobe"))