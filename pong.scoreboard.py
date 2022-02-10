from microbit import *
import radio

radio.on()

gameStart = False
p2Wins = 0
p1Wins = 0
#teller poengsummen til spillerne

while True:
    received = radio.receive()
    if gameStart:
        if received:
            if received == "P1 lost": #hvis p1 taper
                p2Wins += 1 #får p2 et poeng
                display.scroll(str(p1Wins) + "-" + str(p2Wins)) #og det viser poengene
                radio.send("ready") #sender klarsignal sånn at spillet ikke går videre når den fortsatt viser poeng
            elif received == "P2 lost": #hvis p2 taper
                p1Wins += 1 #får p1 et poeng
                display.scroll(str(p1Wins) + "-" + str(p2Wins)) 
                radio.send("ready")
        if button_a.was_pressed():
            radio.send("end game") #forteller andre at spillet slutter 
            p2Wins = 0
            p1Wins = 0 #setter poengene til 0
            display.scroll(str(p1Wins) + "-" + str(p2Wins)) #viser at begge har 0 poeng
            gameStart = False #spillet slutter
        if button_b.was_pressed():
            radio.send("end game")
            if p1Wins > p2Wins: #hvis p1 har vunnet mer enn p2
                display.scroll("P1") #viser hvem som vant (p1)
            elif p2Wins > p1Wins: #hvis p2 har vunnet mer enn p1
                display.scroll("P2") #viser hvem som vant (p2)
            else: #hvis ingen av dem har mer poeng enn den andre
                display.scroll("DRAW") #uavgjort
            p1Wins = 0
            p2Wins = 0
            gameStart = False #spillet slutter
    else:
        if button_a.was_pressed(): #starter spillet
            gameStart = True
            radio.send("ready")
    sleep(100)
