%pylab inline
import time #lubab kasutada time lisamoodulit millega saab programmis määrata pause
from __future__ import print_function #kuna tegemist on python2 programmiga, siis see lubab võtta python3-st print käsu
from pypot.creatures import PoppyErgoJr #võimaldab robotile spetsiifilise käske anda
from pypot.primitive.move import MoveRecorder, MovePlayer, Move #võimaldab liigutusi salvestada

poppy = PoppyErgoJr() #defineerime roboti
motors=[poppy.m1, poppy.m2, poppy.m3, poppy.m4, poppy.m5, poppy.m6] #defineerime kõik kuus mootorit
recorder = MoveRecorder(poppy, 50, motors) #defineerime liigutuste salvesti

options = [] #algne tühi nimekirja kuhu laetakse sisse teada olevad liigutused
thingsIknow = open("/home/poppy/notebooks/memory/thingsIknow.txt", "r") #lae sisse fail kus on teada olevate liigutuste nimed
for tik in thingsIknow: #tsükkel mis käib läbi sisse laetud faili thingsIknow.txt
    tik = tik.strip() #eemaldab sisse loetud nimest mitte vajalikud sümbolid
    options.append(tik) #lisab liigutuse nime nimekirja
thingsIknow.close() #sulgeb sisse laetud faili

def addToMemory(name): #funktsioon liigutuse mällu lisamiseks
    thingsIknow = open("/home/poppy/notebooks/memory/thingsIknow.txt", "a") #ava fail kus on liigutuste nimed
    thingsIknow.write(str(name)+"\n") #kirjuta faili uue liigutuse nimi
    thingsIknow.close() #sulge fail
def show(choice): #ette näitamise funktsioon
    presentation = "/home/poppy/notebooks/memory/" + choice + ".move" #otsi üles liigutuse andmed
    for m in poppy.motors: #käi läbi kõik mootorid
        m.led='blue' #muuda led lambid siniseks
    with open(presentation, 'r') as fromMemory: #ava fail kus on liikumis andmed
        imported = Move.load(fromMemory) #loe andmed sisse nii et programm nendest aru saaks
    player = MovePlayer(poppy, imported) #lae need andmed muutujasse
    player.start() #alusta liigutuse presenteerimist
def learn(): #õppimis funktsioon
    while True: #tsükkli algus, tsükkel kestab kuni midagi selle lõpetab
        for m in motors: #käi läbi küik mootorid
            m.compliant=True #vabasta mootorid et inimesne saaks neid liigutada
        for m in poppy.motors: #käi läbi kõik mootorid
            m.led='green' #muuda led lambid roheliseks
        recorder.start() #alusta liigutuse salvestamist
        time.sleep(5) #oota 5 sekundit
        recorder.stop() #lõpeta liigutuse salvestamine
        player = MovePlayer(poppy, recorder.move) #lisa salvestatud andmed muutujasse
        player.start() #presenteeri liigutus
        acceptable = raw_input("should I save this performance if not then we'll try again(y/n)") #küsi kas kasutajale meeldis liigutus, anna teada et vastata kas y või n
        if acceptable == "y" or acceptable == "Y": #kui vastus on kas y või Y, siis liigu edasi
            return recorder #saada salvestatud info tagasi põhi programmi
        else: #kui vastati midagi mis ei ole y või Y
            continue #korda tsükklit

while True: #tsükkli algus, tsükkel kestab kuni midagi selle lõpetab
    activity = raw_input("do you want to teach me or do you want me to show you somthing?(answer either learn or show)") #küsi kasutajalt kas learn või show
    if activity == "learn" or activity == "show": #kui vastati kas learn või show
        break #lõpeta tsükkel
    else: #kui vastati midagi muud
        print("palun jälgi juhiseid") #anna kasutajale teada et ta sisestaks õige termini

if activity == "show": #kui kasutaja kirjutas show
    while True: #tsükkli algus, tsükkel kestab kuni midagi selle lõpetab
        print("Here are my options:", options, "please select one") #n'ita kasutajale võimalike valikuid
        presenting = raw_input() #laseb kasutajal valida mida ta näha soovib
        if presenting in options: #kui sisestatud nimi eksisteerib nimekirjas siis liigu edasi
            show(presenting) #liigu edasi ette näitamis funktsiooni koos ette antud liigutuse nimega
            break #kui liigutus on presenteeritud, siis program tuleb siia ja lõpetab tsükli
        break #lõpeta tsükkel ja programm kui ei leitud nime, soovi korral võib siia panna sõna continue sõna break asemele, siis program jätkab tööd kuni saab sobiva nime
if activity == "learn": #kui kasutaja kirjutas learn
    recorder = learn() #käivita õpetamis funktsioon
    print("what shall we name this program?") #anna kasutajale teada et ta saab sisestada uuele liigutusele nime
    while True: #tsükkli algus, tsükkel kestab kuni midagi selle lõpetab
        teaching = raw_input() #siin saab sisestada kasutaja nime
        if teaching in options: #kui see nimi juba eksisteerib
            print("that name is already taken") #see nimi on juba võetud
        else: #kui seda nime pole olemas
            break #lõpeta tsükkel
    addToMemory(teaching) #liigu mällu lisamis funktsiooni
    teaching = "/home/poppy/notebooks/memory/" + teaching + ".move" #lisa muutujasse vastave liigutuse jaoks asukoht
    with open(teaching, "w") as memory: #ava just lisatud asukoht
        recorder.move.save(memory) #kirjuta sinna uus fail koos andmetega

