%pylab inline
import time 
from __future__ import print_function 
from pypot.creatures import PoppyErgoJr 
from pypot.primitive.move import MoveRecorder, MovePlayer, Move 

poppy = PoppyErgoJr() 
motors=[poppy.m1, poppy.m2, poppy.m3, poppy.m4, poppy.m5, poppy.m6] 
recorder = MoveRecorder(poppy, 50, motors) 

options = [] 
thingsIknow = open("/home/poppy/notebooks/memory/thingsIknow.txt", "r") 
for tik in thingsIknow: 
    tik = tik.strip() 
    options.append(tik) 
thingsIknow.close() 

def addToMemory(name): 
    thingsIknow = open("/home/poppy/notebooks/memory/thingsIknow.txt", "a") 
    thingsIknow.write(str(name)+"\n") 
    thingsIknow.close() 
def show(choice): 
    presentation = "/home/poppy/notebooks/memory/" + choice + ".move" 
    for m in poppy.motors: 
        m.led='blue' 
    with open(presentation, 'r') as fromMemory: 
        imported = Move.load(fromMemory) 
    player = MovePlayer(poppy, imported) 
    player.start() 
def learn():
    while True: 
        for m in motors: 
            m.compliant=True 
        for m in poppy.motors: 
            m.led='green' 
        recorder.start() 
        time.sleep(5)
        recorder.stop(
        player = MovePlayer(poppy, recorder.move) 
        player.start()
        acceptable = raw_input("should I save this performance if not then we'll try again(y/n)") 
        if acceptable == "y" or acceptable == "Y": 
            return recorder 
        else:
            continue 

while True: 
    activity = raw_input("do you want to teach me or do you want me to show you somthing?(answer either learn or show)") 
    if activity == "learn" or activity == "show": 
        break
    else:
        print("palun jälgi juhiseid")

if activity == "show": 
    while True: 
        print("Here are my options:", options, "please select one") 
        presenting = raw_input() 
        if presenting in options: 
            show(presenting) 
            break 
        break 
if activity == "learn": 
    recorder = learn()
    print("what shall we name this program?")
    while True: 
        teaching = raw_input() 
        if teaching in options:
            print("that name is already taken")
        else: 
            break 
    addToMemory(teaching) 
    teaching = "/home/poppy/notebooks/memory/" + teaching + ".move" 
    with open(teaching, "w") as memory:
        recorder.move.save(memory) 
