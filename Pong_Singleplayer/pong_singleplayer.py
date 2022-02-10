from microbit import *
#importerer alt som blir brukt i koden

wallBrightness = 9 #bestemmer hvor lys veggen (spilleren) er
wall = Image(5,1, bytearray([0,0,wallBrightness,0,0])) #spilleren selv

speed = 200

bBr = 3 #ball Brightness
xPos = 1 #x-Posisjonen til ballen
yPos = 5 #y-Posisjonen til ballen
deltaX = 1 #hvor mye ballen begever seg på x-aksen
deltaY = -1 #hvor mye ballen begever seg på y-aksen

def resetBall():
    global xPos
    global yPos
    global deltaX
    global deltaY
    #disse må være global, fordi de er del av en funksjon
    #som ikke har adgang til andre variabler 
    xPos = 1
    yPos = 5
    deltaX = 1
    deltaY = -1
    #setter ballen i sin opprinnelige posisjon

wins = 0
losses = 0
#teller hvor mange ganger spilleren har tapt (og vunnet)


while True:
    if button_a.was_pressed() and wall.get_pixel(0,0) == 0: #hvis a er trykket og spilleren ikke er rett ved en vegg
        wall = wall.shift_left(1) #beveger spilleren om en til venstre
    if button_b.was_pressed() and wall.get_pixel(4,0) == 0: #samme her med den andre veggen
        wall = wall.shift_right(1) #beveger spilleren om en til høyre
    display.show(wall)
    xPosTest = xPos + deltaX #regner ut hvor ballen kommer til å være (på x-aksen)
    yPosTest = yPos + deltaY #regner ut hvor ballen kommer til å være (på y-aksen)
    if yPos == 0: #hvis ballen er bak spilleren
        losses += 1 #har man tapt
        resetBall()
    else: #hvis den ikke er bak spilleren
        if xPosTest >= 5 or xPosTest <= -1: #hvis xPosTest hadde vært utenfor microbiten
            deltaX *= -1 #går ballen i den motsatte retningen
            xPosTest = xPos + deltaX
        if yPosTest >= 5: #hvis yPosTest hadde vært utenfor microbiten
            deltaY *= -1 #går den i den andre retningen
            yPosTest = yPos + deltaY
        if display.get_pixel(xPos, yPos - 1) == wallBrightness: #hvis pixelen over ballen er like lys som spilleren (treffer spilleren)
            deltaY *= -1 #går den i motsatt retning
        if display.get_pixel(xPosTest, yPosTest) == wallBrightness and not display.get_pixel(xPos, yPos - 1) == wallBrightness:
        #hvis den kommer til å treffe veggen i neste skritt og spilleren ikke er over ballen:
            deltaY *= -1 #blir deltaY og deltaX motsatt av det de var
            deltaX *= -1
            xPosTest = xPos + deltaX 
            if xPosTest >= 5 or xPosTest <= -1: #det samme som linje 42 og 43 for spesialfall
                deltaX *= -1
    xPos += deltaX #regner ut den neste posisjonen til ballen
    yPos += deltaY
    display.set_pixel(xPos,yPos,bBr) #viser ballen
    sleep(speed)
