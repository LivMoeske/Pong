from microbit import *
import radio

radio.on()

wallBrightness = 9
wall = Image(5,1, bytearray([0,0,wallBrightness,0,0]))

speed = 200
#bestemmer hvor lenge det tar til while loopen blir gjennomført i millisekunder

bBr = 7
xPos = 1
yPos = 5
deltaX = 1
deltaY = -1
#egenskapene av ballen

isBallOwner = False
#om den har ballen
isNextBallOwner = False 
#om den kommer til å få ballen

def resetBall():
    global xPos
    global yPos
    global deltaX
    global deltaY
    #disse må være global fordi de blir definert utenfor funksjonen
    xPos = 1
    yPos = 5
    deltaX = 1
    deltaY = -1
    #setter alle egenskapene tilbake til sine opprinnelige verdier

wins = 0
losses = 0
#hvor mange ganger den har tapt / vunnet

while True:
    received = radio.receive()
    if received:
        if received == "end game":
            wins = 0
            losses = 0
            isBallOwner = False #tar vekk ballen
            isNextBallOwner = False  #kommer ikke til å ha ballen når det starter igjen
        elif received == "P1 lost": #hvis p1 har tapt
            display.show("W") #får p2 et poeng
            sleep(1000)
        elif received == "ready": #hvis scoreboard er klar
            if isNextBallOwner: #hvis den får ballen
                isBallOwner = True #har den ballen
                isNextBallOwner = False #får den ikke neste gang
        elif received != "P1 lost": #hvis den får egenskapene av ballen til den andre
            isBallOwner = True
            receivedValues = received.split(",")
            #split blir brukt til å lage en liste av egenskapene og sepererer dem hos ','
            xPos = 4 - int(receivedValues[0]) #4 - xPos av den andre fordi koordinatene er omvendt
            yPos = int(receivedValues[1])
            deltaX = 0 - int(receivedValues[2]) #0 - deltaX / deltaX * -1 fordi koordinatene er omvendt
            deltaY = 0 - int(receivedValues[3]) #0 - deltaY / deltaY * -1 fordi koordinatene er omvendt
    if button_a.was_pressed() and wall.get_pixel(0,0) == 0:
        #hvis man trykker a og pixelen ved kanten er 0 (spilleren er ikke ved veggen)
        wall = wall.shift_left(1) #blir bildet "wall" dyttet en til venstre
    if button_b.was_pressed() and wall.get_pixel(4,0) == 0:
        #hvis man trykker b og pixelen ved kanten er 0 (spilleren er ikke ved veggen)
        wall = wall.shift_right(1) #blir bildet "wall" dyttet en til høyre
    display.show(wall) #vis veggen / spilleren
    if isBallOwner: #hvis den har ballen
        xPosTest = xPos + deltaX
        yPosTest = yPos + deltaY
        if yPos == 0: #hvis ballen er bak spilleren
            losses += 1
            radio.send("P2 lost") #sender at den har tapt
            display.show("L")
            sleep(1000)
            resetBall()
            isBallOwner = False #har ikke ballen lenger
            isNextBallOwner = True #kommer til å ha den neste gang den får "ready"
        else: #hvis den ikke er bak spilleren
            if yPosTest >= 5: #hvis den kommer til å være utenfor veggen som er mellom spillerne
                radio.send(str(xPos) + "," + str(yPosTest) + "," + str(deltaX) + "," + str(deltaY)) #send verdiene til ballen
                isBallOwner = False #har ikke ballen lenger
            else:
                if xPosTest >= 5 or xPosTest <= -1:
                    deltaX *= -1
                    xPosTest = xPos + deltaX
                if display.get_pixel(xPos, yPos - 1) == wallBrightness:
                    deltaY *= -1
                if display.get_pixel(xPosTest, yPosTest) == wallBrightness and not display.get_pixel(xPos, yPos - 1) == wallBrightness:
                    deltaY *= -1
                    deltaX *= -1
                    xPosTest = xPos + deltaX
                    if xPosTest >= 5 or xPosTest <= -1:
                        deltaX *= -1
                xPos += deltaX
                yPos += deltaY
                display.set_pixel(xPos,yPos,bBr)
                #dette er det samme som hos singleplayer
    sleep(speed)
