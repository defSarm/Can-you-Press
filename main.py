from gamelib import *
from time import sleep
from random import *

game = Game(1000,600,"   Can you press?")
bk = Image("./images/bk.jpg",game)
bk.resizeTo(game.width,game.height)

spawnx, spawny= 100, 390

doorSound = Sound("./sounds/dooropen.mp3",3)

# character
RightStance = Animation("./images/Character/CRightBlink.png",2,game,531/2,546,30)
RightStance.resizeBy(-60)
RightStance.moveTo(100,390)

RPick = Image("./images/Character/RightPickUp.png",game)
RPick.resizeBy(-60)

RightGun = Animation("./images/Character/CRightGun.png",2,game,599/2,294,30)
RightGun.resizeBy(-60)

LeftStance = Animation("./images/Character/CLeftBlink.png",2,game,531/2,546,30)
LeftStance.resizeBy(-60)
LeftStance.moveTo(100,390)

LPick = Image("./images/Character/LeftPickUp.png",game)
LPick.resizeBy(-60)

LeftGun = Animation("./images/Character/CLeftGun.png",2,game,616/2,292,30)
LeftGun.resizeBy(-60)


# buttons
Eb = Image("./images/Ebutton.png",game)
Eb.moveTo(800,447)
Eb.resizeBy(-30)
EbON = Image("./images/Ebutton.png",game)
EbON.resizeBy(-30)
EbON.moveTo(Eb.x,Eb.y)
EbOFF = Image("./images/EbuttonOFF.png",game)
EbOFF.moveTo(EbON.x,EbON.y)
EbOFF.resizeBy(-30)

# doors
door = Image("./images/doorC.jpg",game)
door.resizeBy(40)
door.moveTo(100,400)

doorC = Image("./images/doorC.jpg",game)
doorC.resizeBy(40)
doorC.moveTo(door.x,door.y)

doorO = Image("./images/doorO.jpg",game)
doorO.resizeBy(40)
doorO.moveTo(door.x,door.y)

# Floor
floor = Shape("rectangle",game,1000,200,"gray")
floor.moveTo(500,game.height-32)

# TEST BLOCK
block = Shape("rectangle",game,40,40,"black")

counter = 0
cooldown = True

# part of blockPhys
RPick.visible = False
LPick.visible = False

# mouse cursor
cursor = Image("./images/mouse.png",game)
cursor.resizeBy(-88)

# gun
RightGun.visible=False
LeftGun.visible=False

buttonClick=Sound("./sounds/buttonClick.mp3",2)
pickupSound = Sound("./sounds/pop.wav",1)

def cursorPhys():
    cursor.draw()
    cursor.moveTo(mouse.x,mouse.y)

# physics (PLAYER)
def PlayerMovement(move=True,gun=False):
    # Standard walking animation
    LeftStance.draw()
    RightStance.draw()
    RPick.draw()
    LPick.draw()
    RightGun.draw()
    LeftGun.draw()
    if keys.Pressed[K_d] or keys.Pressed[K_RIGHT]:
        if move:
            RightStance.visible = True
            LeftStance.visible = False
            LeftStance.x = RightStance.x
            RightStance.x+=8
            if pickUp:
                  RightStance.visible = False
                  LeftStance.visible = False
                  RPick.visible = True
                  LPick.visible = False
        if gun:
            RightStance.visible=False
            LeftStance.visible=False
            RightGun.visible=True
            LeftGun.visible=False
            LeftGun.x=RightGun.x
            RightGun.x+=8
        if gun==False:
          LeftGun.visible=False
          RightGun.visible=False
          
    elif keys.Pressed[K_a] or keys.Pressed[K_LEFT]:
        if move and not(gun):
            RightStance.visible = False
            LeftStance.visible = True
            RightStance.x = LeftStance.x
            LeftStance.x-=8
            if pickUp:
                RightStance.visible = False
                LeftStance.visible = False
                RPick.visible = False
                LPick.visible = True
        if gun:
            RightStance.visible=False
            LeftStance.visible=False
            RightGun.visible=False
            LeftGun.visible=True
            RightGun.x=LeftGun.x
            LeftGun.x-=8
        if gun==False:
          LeftGun.visible=False
          RightGun.visible=False
    global counter
    global cooldown

    # Gravity
    if RightStance.y < 390 and LeftStance.y < 390:
        RightStance.y+=20
        LeftStance.y+=20
  
    # Jumping
    if keys.Pressed[K_w] or keys.Pressed[K_UP]: 
        if move:     
            counter += 1
            if cooldown==True:
                RightStance.y -= 100
                LeftStance.y -= 100
                cooldown = False
            elif counter == 6:
                cooldown = True
                counter-=6

# physics (OBJECTS)
pickUp = False
def blockPhy(shape,collision,ht,flooring):
    global pickUp
    if not(shape.collidedWith(flooring,"rectangle") and pickUp != True):
      shape.y+=7
    if shape.x > game.width:
      shape.x-=40
    if shape.x <0:
      shape.x+=40
  
    if collision.collidedWith(shape,"rectangle"):
        if keys.Pressed[K_e]:
            pickupSound.play()
            pickUp = True
    if pickUp == True:
        # animation adjustments
        RPick.moveTo(RightStance.x,RightStance.y)
        LPick.moveTo(LeftStance.x,LeftStance.y)
        # actual pick up
        shape.x = collision.x
        shape.y = collision.y-ht
    if keys.Pressed[K_q] and pickUp == True:
        if RPick.visible == True:
          RightStance.visible = True
          RPick.visible = False
        elif LPick.visible == True:
          LeftStance.visible = True
          LPick.visible = False
        shape.rotateTo(0)
        pickUp = False
    elif keys.Pressed[K_SPACE] and pickUp == True:
      pickUp = False

      # throwing
      if RightStance.visible == True or RPick.visible == True:
        LeftStance.x = RightStance.x
        RightStance.visible = True
        LeftStance.visible = False
        RPick.visible = False
        LPick.visible = False
        shape.rotateTo(0)
        shape.x +=150
      elif RightStance.visible != True or RPick.visible != True:
        RightStance.x = LeftStance.x
        RightStance.visible = False
        LeftStance.visible = True
        RPick.visible = False
        LPick.visible = False
        shape.rotateTo(0)
        shape.x-=150
        

def wallBorder():
    # player
    if RightStance.x > game.width-40 and LeftStance.x > game.width-40:
        RightStance.moveTo(game.width-35, RightStance.y)
        LeftStance.moveTo(game.width-35, LeftStance.y)
        
    elif RightStance.x < 40 and LeftStance.x < 40:
        LeftStance.moveTo(35,LeftStance.y)
        RightStance.moveTo(35,RightStance.y)
        

# START BUTTONS

# quit 
leave = False

# Start screen

# logo
cup = Image("./images/Can you press.png",game)
cup.resizeBy(-20)
cup.moveTo(500,50)

# start menu buttons
play = Image("./images/startMenu/playON.gif",game)
play.moveTo(500,160)
play.resizeBy(80)
playO = Image("./images/startMenu/playON.gif",game)
playO.moveTo(play.x,play.y)
playO.resizeBy(80)
playOF = Image("./images/startMenu/playOFF.gif",game)
playOF.moveTo(play.x,play.y)
playOF.resizeBy(80)

# - - - - - - - 
quit = Image("./images/startMenu/quitON.gif",game)
quit.moveTo(500,410)
quit.resizeBy(80)
quitO = Image("./images/startMenu/quitON.gif",game)
quitO.moveTo(quit.x,quit.y)
quitO.resizeBy(80)
quitOF = Image("./images/startMenu/quitOFF.gif",game)
quitOF.moveTo(quit.x,quit.y)
quitOF.resizeBy(80)

# - - - - - - - 
help = Image("./images/startMenu/HelpO.gif",game)
help.moveTo(500,285)
help.resizeBy(80)
helpO = Image("./images/startMenu/HelpO.gif",game)
helpO.moveTo(help.x,help.y)
helpO.resizeBy(80)
helpOF = Image("./images/startMenu/HelpOF.gif",game)
helpOF.moveTo(help.x,help.y)
helpOF.resizeBy(80)

# help text
story = Image("./images/story line.png",game)
story.moveTo(500,400)
story.visible = False
story.resizeBy(-10)
story.moveTo(500,150)

arrow = Image("./images/arrow.gif",game)
arrow.moveTo(100,50)
arrow.visible = False
arrow.resizeBy(100)

# CONTROLS
controls = Image("./images/startMenu/CONTROLS.png",game)
controls.moveTo(200,260)
controls.resizeBy(-55)
controls.visible = False

wasd = Image("./images/startMenu/wasd.png",game)
wasd.moveTo(180,370)
wasd.resizeBy(-50)
wasd.visible = False

qkey = Image("./images/startMenu/QKEY.png",game)
qkey.moveTo(380,370)
qkey.resizeBy(-83)
qkey.visible = False

ekey = Image("./images/startMenu/EKEY.png",game)
ekey.moveTo(550,370)
ekey.resizeBy(-83)
ekey.visible = False

spaceKey = Image("./images/startMenu/spaceBAR.png",game)
spaceKey.moveTo(800,370)
spaceKey.resizeBy(20)
spaceKey.visible = False

book = Image("./images/startMenu/BOOK.png",game)
book.moveTo(900,530)
book.visible = False
book.resizeBy(-70)

mouseSHOOT = Image("./images/startMenu/mouse.png",game)
mouseSHOOT.moveTo(200,560)
mouseSHOOT.visible = False
mouseSHOOT.resizeBy(-70)

# clicking AUDIO
clickSOUND = Sound("./sounds/Click.mp3",0)

game.setMusic("./sounds/lobbyM.mp3")
game.setVolume(10)
game.playMusic()

# start menu ---------------------------------------------------------------------------------------------------
while not game.over:
    game.processInput()
    bk.draw()
    floor.draw()
    play.draw()
    quit.draw()
    cup.draw()
    help.draw()
    story.draw()
    arrow.draw()
    controls.draw()
    wasd.draw()
    qkey.draw()
    ekey.draw()
    spaceKey.draw()
    book.draw()
    mouseSHOOT.draw()

    play.setImage(playO.image)
    if mouse.collidedWith(play,"rectangle"):
        play.setImage(playOF.image)
        if mouse.LeftClick:
            clickSOUND.play()
            game.over = True

    quit.setImage(quitO.image)
    if mouse.collidedWith(quit,"rectangle"):
        quit.setImage(quitOF.image)
        if mouse.LeftClick:
            clickSOUND.play()
            leave = True
            game.over = True

    help.setImage(helpO.image)
    if mouse.collidedWith(help,"rectangle"):
        help.setImage(helpOF.image)
        if mouse.LeftClick:
            clickSOUND.play()
            arrow.visible = True
            story.visible = True
            help.visible = False
            play.visible = False
            quit.visible = False
            cup.visible = False
            controls.visible = True
            wasd.visible = True
            qkey.visible = True
            ekey.visible = True
            spaceKey.visible = True
            book.visible = True
            mouseSHOOT.visible = True
            
    # back arrow
    if mouse.collidedWith(arrow) and mouse.LeftClick:
        story.visible = False
        arrow.visible = False
        help.visible = True
        play.visible = True
        quit.visible = True
        cup.visible = True
        controls.visible = False
        qkey.visible = False
        wasd.visible = False
        ekey.visible = False
        spaceKey.visible = False
        book.visible = False
        mouseSHOOT.visible = False

    cursorPhys()
    game.update(30)

def spawn(regular=True,gun=False):
    if regular and not(gun):
      RightStance.visible = True
      RightStance.moveTo(spawnx, spawny)
      LeftStance.visible = False
      LeftStance.moveTo(spawnx, spawny)
    else:
      RightStance.visible=False
      LeftStance.visible=False

    if gun and not(regular):
      RightGun.visible=True
      RightGun.moveTo(spawnx,spawny-15)
      LeftGun.visible=False
      LeftGun.moveTo(spawnx,spawny-15)
    else:
      RightGun.visible=False
      LeftGun.visible=False

# level 1 ----------------------------------------------------------------------------------------------------
door.visible = False
game.over = False
game.stopMusic()

playSound = False

qkey.moveTo(Eb.x,Eb.y-150)
game.setMusic("./sounds/SneakySnitch.mp3")
game.playMusic()
while not game.over and not(leave):
    game.processInput()
    bk.draw()
    block.draw()
    floor.draw()
    Eb.draw()
    door.draw()
    ekey.draw()
    qkey.draw()

    blockPhy(block,RightStance,70,floor)
    blockPhy(block,LeftStance,70,floor)
    
    wallBorder()
    PlayerMovement()
    cursorPhys()


    Eb.setImage(EbON.image)
    if block.collidedWith(Eb):
        playSound=True
        ekey.visible = False
        qkey.visible = False
        block.y=Eb.y-40
        pressed = True
        Eb.setImage(EbOFF.image)
    else:
        ekey.moveTo(500,300)
        qkey.visible = True
        ekey.visible = True
        door.visible = False
        pressed=False
    
    if playSound:
        buttonClick.play()
        playSound=False

    if pressed:
        door.visible = True
        door.setImage(doorC.image)
        if RightStance.collidedWith(door,"rectangle") or LeftStance.collidedWith(door,"rectangle"):
            doorSound.play(False)
            ekey.visible = True
            ekey.moveTo(door.x,door.y-150)
            door.setImage(doorO.image)
            if keys.Pressed[K_e]:
                game.stopMusic()
                game.over = True

    game.update(30)

door.visible = False
game.over = False

levelANIMATION = Shape("rectangle",game,60,60,(0,0,0))
levelANIMATION.moveTo(1300,300)

lvl2 = Image("./images/levels/level2/level2.png",game)
lvl2.moveTo(-200,300)

def LEVEL(lvl):
    lvl.draw()
    if lvl.collidedWith(levelANIMATION):
        lvl.visible = False
    else:
        lvl.moveTowards(levelANIMATION,25)

# level 2 ---------------------------------------------------------------------------------------------------

gun = Image("./images/levels/level2/gun.png",game)
gun.resizeBy(-88)
gun.moveTo(500,430)
bll = Image("./images/levels/level2/bullet.png",game)
bll.visible = False
bll.resizeBy(-97)

# balloons
one = Image("./images/levels/level2/numberB/one.png",game)
one.resizeBy(-70)
one.moveTo(150,250)

two = Image("./images/levels/level2/numberB/two.png",game)
two.resizeBy(-75)
two.moveTo(250,120)

three = Image("./images/levels/level2/numberB/three.png",game)
three.resizeBy(-81)
three.moveTo(800,300)

four = Image("./images/levels/level2/numberB/four.png",game)
four.resizeBy(-69)
four.moveTo(500,100)

five = Image("./images/levels/level2/numberB/five.png",game)
five.resizeBy(-80)
five.moveTo(400,269)

six = Image("./images/levels/level2/numberB/six.png",game)
six.resizeBy(-70)
six.moveTo(700,80)

seven = Image("./images/levels/level2/numberB/seven.png",game)
seven.resizeBy(-83)
seven.moveTo(680,200)

bookIG = Image("./images/startMenu/bookIG.png",game)
bookIG.resizeBy(-80)
bookIG.moveTo(230,410)

bookHELP = Image("./images/levels/level2//bookINS.png",game)
bookHELP.resizeBy(-50)
bookHELP.visible = False

hitbox = Image("./images/bk.jpg",game)
hitbox.resizeTo(10,10)
hitbox.visible = False

BOUNCEWALL = Shape("rectangle",game,100,500,(128,128,128))
BOUNCEWALL.moveTo(-20,220)
BOUNCEWALL2 = Shape("rectangle",game,100,500,(128,128,128))
BOUNCEWALL2.moveTo(1020,220)

doorC.moveTo(500,400)
doorO.moveTo(doorC.x,doorC.y)

option = True
shoot = False
bounce = False

wallHit = Sound("./sounds/WallHit.mp3",1)

# gun physics - - - - - - - - - - - - - - - - - - - - 
def gunPhys(bullet,weapon,pointer,wall=None,wall2=None):
    global shoot
    global bounce
    weapon.rotateTowards(pointer)
    if mouse.LeftClick and not(shoot) and not(bounce):
        bullet.moveTo(weapon.x,weapon.y)
        bullet.visible = True
        hitbox.visible = True
        hitbox.moveTo(pointer.x,pointer.y)
        shoot = True
    if shoot:
        bullet.moveTowards(hitbox,6)
        if bullet.collidedWith(hitbox):
            hitbox.visible = False
            bullet.moveTo(weapon.x,weapon.y)
            bullet.visible = False
            shoot = False
        if bll.collidedWith(wall,"rectangle"):
            wallHit.play()
            hitbox.visible = False
            bounce = True
            shoot=False
    if bll.collidedWith(wall,"rectangle"):
        wallHit.play()
        bullet.setSpeed(7,-45)
        hitbox.visible = False
        bounce = True
        shoot=False
    if bll.collidedWith(wall2,"rectangle"):
        wallHit.play()
        bullet.setSpeed(7,45)
        hitbox.visible = False
        bounce = True
        shoot = False
    if bounce:
      bullet.move()
      if bullet.y<0:
        bounce = False
        bullet.visible = False
        bullet.moveTo(weapon.x,weapon.y)

gunFont = Font(black)

popS=Sound("./sounds/pop.wav",0)
pageFlip=Sound("./sounds/pageflip.mp3",2)

game.playMusic()
spawn()

balcount = 1
balLeft = 7

doorC.visible = False
doorO.visible = False
while not game.over and not(leave):
    game.processInput()
    bk.draw()
    floor.draw()
    door.draw()
    levelANIMATION.draw()
    hitbox.draw()
    doorC.draw()
    doorO.draw()

    # balloons
    one.draw()
    two.draw()
    three.draw()
    four.draw()
    five.draw()
    six.draw()
    seven.draw()

    bookIG.draw()
    bll.draw()
    gun.draw()
    bookHELP.draw()
    BOUNCEWALL.draw()
    BOUNCEWALL2.draw()

    # level features
    blockPhy(gun,RightStance,70,floor)
    blockPhy(gun,LeftStance,70,floor)

    wallBorder()
    PlayerMovement(option,False)
    cursorPhys()
    LEVEL(lvl2)

    if pickUp:
        gunPhys(bll,gun,cursor,BOUNCEWALL,BOUNCEWALL2) 
    else:
        bll.visible = False
        shoot = False

# balloon game
    if bll.collidedWith(one) and balcount == 1:
        popS.play()
        one.visible = False
        balLeft-=1
        balcount=2
        bll.visible = False
        shoot = False
    if bll.collidedWith(two) and balcount == 2:
        popS.play()
        two.visible = False
        balLeft-=1
        balcount=3
        bll.visible = False
        shoot = False
    if balcount !=2 and bll.collidedWith(two):
        popS.play()
        one.visible=True
        balLeft=7
        balcount=1
    if bll.collidedWith(three) and balcount == 3:
        popS.play()
        three.visible = False
        balLeft-=1
        balcount=4
        bll.visible = False
        shoot = False
    if balcount !=3 and bll.collidedWith(three):
        popS.play()
        one.visible=True
        two.visible = True
        balLeft=7
        balcount=1

    if bll.collidedWith(four) and balcount == 4:
        popS.play()
        four.visible = False
        balLeft-=1
        balcount=5
        bll.visible = False
        shoot = False
    if balcount !=4 and bll.collidedWith(four):
        popS.play()
        one.visible=True
        two.visible = True
        three.visible = True
        balLeft=7
        balcount=1
    if bll.collidedWith(five) and balcount == 5:
        popS.play()
        five.visible = False
        balLeft-=1
        balcount=6
        bll.visible = False
        shoot = False
    if balcount !=5 and bll.collidedWith(five):
        popS.play()
        one.visible=True
        two.visible = True
        three.visible = True
        four.visible = True
        balLeft=7
        balcount=1
    if bll.collidedWith(six) and balcount == 6:
        popS.play()
        six.visible = False
        balLeft-=1
        balcount=7
        bll.visible = False
        shoot = False
    if balcount !=6 and bll.collidedWith(six):
        popS.play()
        one.visible=True
        two.visible = True
        three.visible = True
        four.visible = True
        five.visible = True
        balLeft=7
        balcount=1
    if bll.collidedWith(seven) and balcount == 7:
        popS.play()
        seven.visible = False
        balLeft-=1
        balcount=8
        bll.visible = False
        shoot = False
    if balcount !=7 and bll.collidedWith(seven):
        popS.play()
        one.visible=True
        two.visible = True
        three.visible = True
        four.visible = True
        five.visible = True
        six.visible = True
        balLeft=7
        balcount=1
    
    # win
    if balLeft == 0 and balcount == 8:   
        bookIG.visible = True
        doorC.visible = True
        if not(RightStance.collidedWith(doorC) or LeftStance.collidedWith(doorC)):
            doorC.visible = True
            doorO.visible = False
    if RightStance.collidedWith(doorC) or LeftStance.collidedWith(doorC):
        doorSound.play(False)
        doorC.visible = False
        doorO.visible = True
        if keys.Pressed[K_e]:
            pickUp=False
            RPick.visible=False
            LPick.visible=False
            game.over=True

    if gun.collidedWith(doorC):
        game.drawText("Hey, no guns in the next room >:(",doorC.x-100,doorC.y-100,gunFont)

        
    # book
    if RightStance.collidedWith(bookIG,"rectangle") or LeftStance.collidedWith(bookIG,"rectangle"):
        bookHELP.moveTo(500,300)
        if keys.Pressed[K_e]:
            pageFlip.play()
            option = False
            bookHELP.visible = True
        if keys.Pressed[K_q]:
            bookHELP.visible = False
            option = True
            


    game.update(30)

# level 3 ---------------------------------------------------------------------------------------------------
lvl3 = Image("./images/levels/level3/level3.png",game)
lvl3.moveTo(-200,300)
spawn()

spikes = Image("./images/levels/level3/spikes.png",game)
spikes.moveTo(500,436)
spikes.resizeBy(-60)
spikes2 = Image("./images/levels/level3/spikes.png",game)
spikes2.moveTo(620,436)
spikes2.resizeBy(-60)

# blank spaces
blank1 = Image("./images/levels/level3/puzzlePieces/blank.jpg",game)
blank1.visible = False
blank1.moveTo(370,156)
blank1.resizeBy(-30)

blank2 = Image("./images/levels/level3/puzzlePieces/blank.jpg",game)
blank2.visible = False
blank2.resizeBy(-30)
blank2.moveTo(512,156)

blank3 = Image("./images/levels/level3/puzzlePieces/blank.jpg",game)
blank3.visible = False
blank3.resizeBy(-30)
blank3.moveTo(654,156)

blank4 = Image("./images/levels/level3/puzzlePieces/blank.jpg",game)
blank4.visible = False
blank4.resizeBy(-30)
blank4.moveTo(370,300)

blank5 = Image("./images/levels/level3/puzzlePieces/blank.jpg",game)
blank5.visible = False
blank5.resizeBy(-30)
blank5.moveTo(512,300)

blank6 = Image("./images/levels/level3/puzzlePieces/blank.jpg",game)
blank6.visible = False
blank6.resizeBy(-30)
blank6.moveTo(654,300)

blank7 = Image("./images/levels/level3/puzzlePieces/blank.jpg",game)
blank7.visible = False
blank7.resizeBy(-30)
blank7.moveTo(370,444)

blank8 = Image("./images/levels/level3/puzzlePieces/blank.jpg",game)
blank8.visible = False
blank8.resizeBy(-30)
blank8.moveTo(512,444)

blank9 = Image("./images/levels/level3/puzzlePieces/blank.jpg",game)
blank9.visible = False
blank9.resizeBy(-30)
blank9.moveTo(654,444)

# puzzle pieces
p1 = Image("./images/levels/level3/puzzlePieces/piece1.jpg",game)
p1.visible = False
p1.moveTo(130,200)
p1.resizeBy(-30)

p2 = Image("./images/levels/level3/puzzlePieces/piece2.jpg",game)
p2.visible = False
p2.moveTo(800,270)
p2.resizeBy(-30)

p3 = Image("./images/levels/level3/puzzlePieces/piece3.jpg",game)
p3.visible = False
p3.moveTo(140,350)
p3.resizeBy(-30)

p4 = Image("./images/levels/level3/puzzlePieces/piece4.jpg",game)
p4.visible = False
p4.resizeBy(-30)
p4.moveTo(850,400)

p5 = Image("./images/levels/level3/puzzlePieces/piece5.jpg",game)
p5.visible = False
p5.resizeBy(-30)
p5.moveTo(120,430)

p6 = Image("./images/levels/level3/puzzlePieces/piece6.jpg",game)
p6.visible = False
p6.resizeBy(-30)
p6.moveTo(880,170)

p7 = Image("./images/levels/level3/puzzlePieces/piece7.jpg",game)
p7.visible = False
p7.resizeBy(-30)
p7.moveTo(150,130)

p8 = Image("./images/levels/level3/puzzlePieces/piece8.jpg",game)
p8.visible = False
p8.resizeBy(-30)
p8.moveTo(865,470)

p9 = Image("./images/levels/level3/puzzlePieces/piece9.jpg",game)
p9.visible = False
p9.resizeBy(-30)
p9.moveTo(160,490)

puzzle = Image("./images/levels/level3/puzzle.png",game)
puzzle.resizeBy(-80)
puzzle.moveTo(230,390)

puzzleBK = Image("./images/levels/level3/puzzleBK.jpg",game)
puzzleBK.visible = False
puzzleBK.resizeTo(950,550)

# repetative lists
click1 = False
click2 = False
click3 = False
click4 = False
click5 = False
click6 = False
click7 = False
click8 = False
click9 = False

blankLIST = [blank1,blank2,blank3,blank4,blank5,blank6,blank7,blank8,blank9]
puzzleLIST = [p1,p2,p3,p4,p5,p6,p7,p8,p9]
clickLIST = [click1,click2,click3,click4,click5,click6,click7,click8,click9]

ekey.moveTo(puzzle.x,260)
ekey.visible = False

click = False
counterCLICK = 0

done1 = False
done2 = False
done3 = False
done4 = False
done5 = False
done6 = False
done7 = False
done8 = False
done9 = False
doneLIST = [done1,done2,done3,done4,done5,done6,done7,done8,done9,]

# making of the level
valid = True
def puzzlePICKUP(puzzleNUMBER,clickNUM,valid):
    global counterCLICK
    global clickLIST
    if valid:
      if cursor.collidedWith(puzzleNUMBER,"rectangle") and mouse.LeftButton:
        counterCLICK = clickNUM
      else:
          counterCLICK = 0

def puzzleLOCK(puzzleNUMBER,blankNUM):
  if puzzleNUMBER.collidedWith(blankNUM) and not(mouse.LeftButton) and cursor.collidedWith(blankNUM):
    puzzleNUMBER.moveTo(blankNUM.x,blankNUM.y)

def puzzleCHECK(puzzleNUMBER,blankNUM):
  if puzzleNUMBER.collidedWith(blankNUM) and not(mouse.LeftButton):
    return True

finish = Image("./images/levels/level3/done.png",game)
finish.visible = False

# button
bON = Image("./images/levels/level3/tallButton.png",game)
bON.resizeBy(-45)
bON.visible = False
bON.moveTo(370,405)
bOFF = Image("./images/levels/level3/pressedButton.png",game)
bOFF.visible = False
bOFF.resizeBy(-45)
bOFF.moveTo(bON.x,bON.y)

bON2 = Image("./images/levels/level3/tallButton.png",game)
bON2.resizeBy(-45)
bON2.moveTo(970,405)
bOFF2 = Image("./images/levels/level3/pressedButton.png",game)
bOFF2.visible = False
bOFF2.resizeBy(-45)
bOFF2.moveTo(bON2.x,bON2.y)

puzzleDONE = False

shiftBLOCK = Shape("rectangle",game,40,40,"black")
shiftBLOCK.moveTo(795,252)
option = True

platform1 = Shape("bar",game,100,30,(125,125,125))
platform1.moveTo(780,270)

platform2 = Shape("bar",game,100,30,(125,125,125))
platform2.moveTo(580,230)

platform3 = Shape("bar",game,100,30,(125,125,125))
platform3.moveTo(380,180)

platform4 = Shape("bar",game,250,30,(125,125,125))
platform4.moveTo(0,180)

shift = False

def shapeShifting(shape,floor1=None,floor2=None,floor3=None,floor4=None):
    global option
    option = False
    shape.draw()
    if shape.y>300:
        shape.moveTo(780,252)
    if shape.x>game.width:
      shape.x=995
    if shape.x<0:
      shape.x=5
    if not(shape.collidedWith(floor1,"rectangle") or shape.collidedWith(floor2,"rectangle") or shape.collidedWith(floor3,"rectangle") or shape.collidedWith(floor4,"rectangle")):
        shape.y+=6
    if keys.Pressed[K_w]:
        if shape.collidedWith(floor1,"rectangle") or shape.collidedWith(floor2,"rectangle") or shape.collidedWith(floor3,"rectangle" or shape.collidedWith(floor4,"rectangle")):
            shape.y-=120
    if keys.Pressed[K_a] or keys.Pressed[K_LEFT]:
        shape.x-=8
    if keys.Pressed[K_d] or keys.Pressed[K_RIGHT]:
        shape.x+=8

buttonClicker = Sound("./sounds/buttonClick.mp3",4)
# minigame buttons (r,g,b,p) -> (b,p,r,g)
gameCOUNTER = 0

blue = Font(blue)
b1 = Image("./images/levels/level3/tallButton.png",game)
b1.resizeBy(-60)
b1.moveTo(20,135)
b1OFF = Image("./images/levels/level3/pressedButton.png",game)
b1OFF.visible = False
b1OFF.resizeBy(-60)
b1OFF.moveTo(b1.x,b1.y)

pink = Font(pink)
b2 = Image("./images/levels/level3/tallButton.png",game)
b2.resizeBy(-60)
b2.moveTo(80,135)
b2OFF = Image("./images/levels/level3/pressedButton.png",game)
b2OFF.visible = False
b2OFF.resizeBy(-60)
b2OFF.moveTo(b2.x,b2.y)

red = Font(red)
b3 = Image("./images/levels/level3/tallButton.png",game)
b3.resizeBy(-60)
b3.moveTo(140,135)
b3OFF = Image("./images/levels/level3/pressedButton.png",game)
b3OFF.visible = False
b3OFF.resizeBy(-60)
b3OFF.moveTo(b3.x,b3.y)

green = Font(green)
b4 = Image("./images/levels/level3/tallButton.png",game)
b4.resizeBy(-60)
b4.moveTo(200,135)
b4OFF = Image("./images/levels/level3/pressedButton.png",game)
b4OFF.visible = False
b4OFF.resizeBy(-60)
b4OFF.moveTo(b4.x,b4.y)

rgbp = Font(black,40)

doorC.visible = False
doorO.visible = False

win = False

game.over = False
while not(game.over) and not(leave):
    game.processInput()
    bk.draw()
    floor.draw()
    levelANIMATION.draw()
    spikes.draw()
    spikes2.draw()
    puzzle.draw()
    ekey.draw()
    bON.draw()
    bOFF.draw()
    bON2.draw()
    bOFF2.draw()
    platform1.draw()
    platform2.draw()
    platform3.draw()
    platform4.draw()
    doorC.draw()
    doorO.draw()

    # buttons
    b1.draw()
    b1OFF.draw()
    b2.draw()
    b2OFF.draw()
    b3.draw()
    b3OFF.draw()
    b4.draw()
    b4OFF.draw()

    game.drawText("PINK",b2.x-20,b2.y,pink)
    game.drawText("BLUE",b1.x-20,b1.y,blue)
    game.drawText("RED",b3.x-20,b3.y,red)
    game.drawText("GREEN",b4.x-20,b4.y,green)

    game.drawText(f"'Colors' ({gameCOUNTER})",35,30,rgbp)

    # button game
    if shiftBLOCK.collidedWith(b1,"rectangle") and keys.Pressed[K_e]:
        buttonClicker.play()
        b1.visible = False
        b1OFF.visible = True
        if gameCOUNTER == 2:
            gameCOUNTER+=1
        else:
            gameCOUNTER = 0
    else:
        b1.visible = True
        b1OFF.visible = False
    
    if shiftBLOCK.collidedWith(b2,"rectangle") and keys.Pressed[K_e]:
        buttonClicker.play()
        b2.visible = False
        b2OFF.visible = True
        if gameCOUNTER == 3:
            gameCOUNTER+=1
        else:
            gameCOUNTER = 0
    else:
        b2.visible = True
        b2OFF.visible = False
    
    if shiftBLOCK.collidedWith(b3,"rectangle") and keys.Pressed[K_e]:
        buttonClicker.play()
        b3.visible = False
        b3OFF.visible = True
        if gameCOUNTER == 0:
            gameCOUNTER+=1
        else:
            gameCOUNTER = 0
    else:
        b3.visible = True
        b3OFF.visible = False

    if shiftBLOCK.collidedWith(b4,"rectangle") and keys.Pressed[K_e]:
        buttonClicker.play()
        b4.visible = False
        b4OFF.visible = True
        if gameCOUNTER == 1:
            gameCOUNTER+=1
        else:
            gameCOUNTER = 0
    else:
        b4.visible = True
        b4OFF.visible = False
    
    if gameCOUNTER == 4:
        gameCOUNTER = 4
        option = True
        shift = False
        win = True

    if win:
        doorC.moveTo(900,400)
        doorO.moveTo(doorC.x,doorC.y)
        bOFF2.visible = False
        bON2.visible = False
        doorC.visible = True
    
    if RightStance.collidedWith(doorC) or LeftStance.collidedWith(doorC):
        if win:
            doorSound.play(False)
            doorC.visible = False
            doorO.visible = True
            if keys.Pressed[K_e]:
                game.over=True
        else:
            doorC.visible = True
            doorO.visible = False

    LEVEL(lvl3)

    wallBorder()
    PlayerMovement(option)
    
    puzzleBK.draw()

    # blank squares
    for i in range(len(blankLIST)):
        blankLIST[i].draw()

    # puzzles
    for i in range(len(puzzleLIST)):
        puzzleLIST[i].draw()

    finish.draw()
  
    if RightStance.collidedWith(spikes,"rectangle") or LeftStance.collidedWith(spikes,"rectangle"):
      spawn()
      
    if RightStance.collidedWith(spikes2,"rectangle") or LeftStance.collidedWith(spikes2,"rectangle"):
      spawn()

    if RightStance.collidedWith(puzzle,"rectangle") or LeftStance.collidedWith(puzzle,"rectangle"):
        ekey.visible = True
        
        if keys.Pressed[K_e]:
            option = False
            puzzleBK.visible = True
            for i in range(len(blankLIST)):
                blankLIST[i].visible = True
            for i in range(len(puzzleLIST)):
                puzzleLIST[i].visible = True

        if keys.Pressed[K_q]:
            finish.visible = False
            option = True
            puzzleBK.visible = False
            for i in range(len(blankLIST)):
                blankLIST[i].visible = False
            for i in range(len(puzzleLIST)):
                puzzleLIST[i].visible = False
    else:
        ekey.visible = False
    
    # puzzle placement and physics
    if cursor.collidedWith(p1,"rectangle") :
        puzzlePICKUP(p1,1,valid)
    if cursor.collidedWith(p2,"rectangle") :
        puzzlePICKUP(p2,2,valid)
    if cursor.collidedWith(p3,"rectangle") :
        puzzlePICKUP(p3,3,valid)
    if cursor.collidedWith(p4,"rectangle") :
        puzzlePICKUP(p4,4,valid)
    if cursor.collidedWith(p5,"rectangle") :
        puzzlePICKUP(p5,5,valid)
    if cursor.collidedWith(p6,"rectangle") :
        puzzlePICKUP(p6,6,valid)
    if cursor.collidedWith(p7,"rectangle") :
        puzzlePICKUP(p7,7,valid)
    if cursor.collidedWith(p8,"rectangle") :
        puzzlePICKUP(p8,8,valid)
    if cursor.collidedWith(p9,"rectangle") :
        puzzlePICKUP(p9,9,valid)

    if counterCLICK == 1:
        p1.moveTo(mouse.x,mouse.y)
    if counterCLICK == 2:
        p2.moveTo(mouse.x,mouse.y)
    if counterCLICK == 3:
        p3.moveTo(mouse.x,mouse.y)
    if counterCLICK == 4:
        p4.moveTo(mouse.x,mouse.y)
    if counterCLICK == 5:
        p5.moveTo(mouse.x,mouse.y)
    if counterCLICK == 6:
        p6.moveTo(mouse.x,mouse.y)
    if counterCLICK == 7:
        p7.moveTo(mouse.x,mouse.y)
    if counterCLICK == 8:
        p8.moveTo(mouse.x,mouse.y)
    if counterCLICK == 9:
        p9.moveTo(mouse.x,mouse.y)
      
    puzzleLOCK(p1,blank1)
    puzzleLOCK(p2,blank2)
    puzzleLOCK(p3,blank3)
    puzzleLOCK(p4,blank4)
    puzzleLOCK(p5,blank5)
    puzzleLOCK(p6,blank6)
    puzzleLOCK(p7,blank7)
    puzzleLOCK(p8,blank8)
    puzzleLOCK(p9,blank9)


    # check for puzzle completion
    c1 = puzzleCHECK(p1,blank1)
    c2 = puzzleCHECK(p2,blank2)
    c3 = puzzleCHECK(p3,blank3)
    c4 = puzzleCHECK(p4,blank4)
    c5 = puzzleCHECK(p5,blank5)
    c6 = puzzleCHECK(p6,blank6)
    c7 = puzzleCHECK(p7,blank7)
    c8 = puzzleCHECK(p8,blank8)
    c9 = puzzleCHECK(p9,blank9)

    if c1 and c2 and c3 and c4 and c5 and c6 and c7 and c8 and c9:
      valid = False
      finish.visible = True
      puzzleDONE = True
      finish.moveTo(500,300)
      bON.visible = True

    if puzzleDONE:
        if RightStance.collidedWith(bON,"rectangle") or LeftStance.collidedWith(bON,"rectangle"):
            if not(RightStance.collidedWith(puzzle,"rectangle") or LeftStance.collidedWith(puzzle,"rectangle")):
                if keys.Pressed[K_e]:
                    buttonClicker.play()
                    bOFF.visible = True
                    bON.visible = False
                    RightStance.moveTo(750,390)
                    LeftStance.moveTo(750,390)
        else:
            bON.visible = True
            bOFF.visible = False
    
    if RightStance.collidedWith(bON2,"rectangle") or LeftStance.collidedWith(bON2,"rectangle"):
        if keys.Pressed[K_e]:
            buttonClicker.play()
            bOFF2.visible = True
            bON2.visible = False
            shift = True
    else:
        bON2.visible = True
        bOFF2.visible = False
    
    if shift:
        spawn()
        shapeShifting(shiftBLOCK,platform1,platform2,platform3,platform4)
  
    cursorPhys()
  
    game.update(30)

# level 4 -------------------------------------------------

logo4 = Image("./images/levels/level4/level4.png",game)
logo4.moveTo(-200,300)

# cups + marble
marbleBall = Image("./images/levels/level4/ball.png",game)
marbleBall.resizeBy(-80)
marbleBall.moveTo(500,420)

cup1 = Image("./images/levels/level4/cups.png",game)
cup1.resizeBy(-70)
cup1.moveTo(300,420)

cup2 = Image("./images/levels/level4/cups.png",game)
cup2.resizeBy(-70)
cup2.moveTo(500,200)

cup3 = Image("./images/levels/level4/cups.png",game)
cup3.resizeBy(-70)
cup3.moveTo(700,420)

cords = [300,500,700]

timer = 0
time = True
marbleWin = False 
cupTimer = False 
cupTime = 0

cup1.clicked = False
cup2.clicked = False
cup3.clicked = False

posx = choice(cords)

def correctCup(cup):
    global marbleWin
    global posx
    if marbleBall.collidedWith(cup):
        marbleWin = True
    if cup.clicked == True and not(marbleBall.collidedWith(cup)):
        posx = choice(cords)

def lift():
    global cupTimer
    global cupTime
    if cupTimer == False:
        cupTime = 0

blueBox = Shape("rectangle",game,50,50,(0,255,255))
blueBox.moveTo(500,80)
blueBox.visible = False

fireBox = Shape("rectangle",game,50,50,(255,165,0))
fireBox.visible = False

enter = Shape("rectangle",game,20,120,(255,255,255))
enter.moveTo(game.width,390)
enter.visible = False
next = False
nextbox = True

exit = Shape("rectangle",game,20,120,(255,255,255))
exit.moveTo(0,390)
exit.visible = False

text = True

# room 2 features ------------------------------------ **

portalON = Image("./images/levels/level4/portalButton1.png",game)
portalON.moveTo(200,423)
portalON.resizeBy(-60)
portalON.visible = False

portalOFF = Image("./images/levels/level4/portalButtonOFF.png",game)
portalOFF.moveTo(portalON.x,portalON.y)
portalOFF.resizeBy(-60)
portalOFF.visible = False

flooring = Image("./images/levels/level4/lava.png",game)
flooring.resizeTo(500,60)
flooring.moveTo(100,150)
flooring.visible = False

# portals
size = -80

blueP = Image("./images/levels/level4/blueP.png",game)
blueP.visible = False
blueP.resizeBy(size)
blueP.rotateTo(180)
blueP.moveTo(30,75)

redP = Image("./images/levels/level4/redP.png",game)
redP.visible=False
redP.resizeBy(size)
redP.rotateTo(-90)
redP.moveTo(400,465)

purpleP = Image("./images/levels/level4/purpleP.png",game)
purpleP.visible=False
purpleP.resizeBy(size)
purpleP.rotateTo(180)
purpleP.moveTo(485,75)

greenP = Image("./images/levels/level4/greenP.png",game)
greenP.visible=False
greenP.resizeBy(size)
greenP.rotateTo(-90)
greenP.moveTo(70,470)

# platform

platformWood = Shape("rectangle",game,100,30,(125,125,125))
platformWood.moveTo(550,250)
platformWood.visible=False

burnWood = Image("./images/levels/level4/wood.png",game)
burnWood.moveTo(550,200)
burnWood.resizeBy(-80)
burnWood.visible=False

cardCode = Image("./images/levels/level4/code.jpg",game)
cardCode.visible=False
cardCode.resizeTo(517,314)
cardCode.resizeBy(-80)
cardCode.moveTo(burnWood.x,burnWood.y)

padLock = Image("./images/levels/level4/padlock.png",game)
padLock.resizeBy(-50)
padLock.visible=False
padLock.moveTo(700,370)

# buttons -------------------------------------------------------

# set 1
pad0 = Image("./images/levels/level4/buttons/pad0.png",game)
pad1 = Image("./images/levels/level4/buttons/pad1.png",game)
pad2 = Image("./images/levels/level4/buttons/pad2.png",game)
pad3 = Image("./images/levels/level4/buttons/pad3.png",game)
pad4 = Image("./images/levels/level4/buttons/pad4.png",game)
pad5 = Image("./images/levels/level4/buttons/pad5.png",game)
pad6 = Image("./images/levels/level4/buttons/pad6.png",game)
pad7 = Image("./images/levels/level4/buttons/pad7.png",game)
pad8 = Image("./images/levels/level4/buttons/pad8.png",game)
pad9 = Image("./images/levels/level4/buttons/pad9.png",game)
padKeys = [pad0,pad1,pad2,pad3,pad4,pad5,pad6,pad7,pad8,pad9]

# set 2
s2pad0 = Image("./images/levels/level4/buttons/pad0.png",game)
s2pad1 = Image("./images/levels/level4/buttons/pad1.png",game)
s2pad2 = Image("./images/levels/level4/buttons/pad2.png",game)
s2pad3 = Image("./images/levels/level4/buttons/pad3.png",game)
s2pad4 = Image("./images/levels/level4/buttons/pad4.png",game)
s2pad5 = Image("./images/levels/level4/buttons/pad5.png",game)
s2pad6 = Image("./images/levels/level4/buttons/pad6.png",game)
s2pad7 = Image("./images/levels/level4/buttons/pad7.png",game)
s2pad8 = Image("./images/levels/level4/buttons/pad8.png",game)
s2pad9 = Image("./images/levels/level4/buttons/pad9.png",game)
s2padKeys = [s2pad0,s2pad1,s2pad2,s2pad3,s2pad4,s2pad5,s2pad6,s2pad7,s2pad8,s2pad9]

# set 3
s3pad0 = Image("./images/levels/level4/buttons/pad0.png",game)
s3pad1 = Image("./images/levels/level4/buttons/pad1.png",game)
s3pad2 = Image("./images/levels/level4/buttons/pad2.png",game)
s3pad3 = Image("./images/levels/level4/buttons/pad3.png",game)
s3pad4 = Image("./images/levels/level4/buttons/pad4.png",game)
s3pad5 = Image("./images/levels/level4/buttons/pad5.png",game)
s3pad6 = Image("./images/levels/level4/buttons/pad6.png",game)
s3pad7 = Image("./images/levels/level4/buttons/pad7.png",game)
s3pad8 = Image("./images/levels/level4/buttons/pad8.png",game)
s3pad9 = Image("./images/levels/level4/buttons/pad9.png",game)
s3padKeys = [s3pad0,s3pad1,s3pad2,s3pad3,s3pad4,s3pad5,s3pad6,s3pad7,s3pad8,s3pad9]
for i in range(len(padKeys)):
    padKeys[i].resizeBy(-45)
    padKeys[i].visible = False
    padKeys[i].moveTo(592,368)
    s2padKeys[i].resizeBy(-45)
    s2padKeys[i].visible = False
    s2padKeys[i].moveTo(700,368)
    s3padKeys[i].resizeBy(-45)
    s3padKeys[i].visible = False
    s3padKeys[i].moveTo(808,368)

code2 = Image("./images/levels/level4/code2.png",game)
code2.resizeBy(-85)
code2.visible=False

stick = Image("./images/levels/level4/stick.png",game)
stick.resizeBy(-93)
stick.moveTo(100,300)

paperstack=Image("./images/levels/level4/paperstack.png",game)
paperstack.resizeTo(100,50)
paperstack.moveTo(150,190)

paperPlatform=Shape("bar",game,100,30,(125,125,125))
paperPlatform.moveTo(100,200)

portalActivate = 1
switch = False
spawn()

pixelBubble = Image("./images/levels/level4/speech.png",game)
pixelBubble.visible = False

textSize = 10
textForBubble=Font(black,textSize)

# progress for text bubbles
def textBubble(msg,size):
    global textSize
    textSize=size
    pixelBubble.draw()
    pixelBubble.visible = True

burned = False
room1=False

padNumber1=0
padNumber2=0
padNumber3=0

doorO.visible=False
doorC.visible=False

portalOpen = Sound("./sounds/portalOpen.wav",5)

def door():
    if not(RightStance.collidedWith(doorC) or LeftStance.collidedWith(doorC)):
        doorC.visible=True
        doorO.visible=False
    if RightStance.collidedWith(doorC) or LeftStance.collidedWith(doorC):
        doorSound.play(False)
        doorC.visible = False
        doorO.visible = True
        if keys.Pressed[K_e]:
            game.over=True

doorC.moveTo(400,400)
doorO.moveTo(400,400)

game.over = False
while not(game.over) and not(leave):
    game.processInput()
    bk.draw()
    floor.draw()

    marbleBall.draw()
    cup1.draw()
    cup2.draw()
    cup3.draw()
    enter.draw()
    exit.draw()
    blueBox.draw()
    paperPlatform.draw()
    paperstack.draw()

    # room 2 aspects
    padLock.draw()
    cardCode.draw()
    burnWood.draw()
    portalON.draw()
    portalOFF.draw()
    blueP.draw()
    greenP.draw()
    redP.draw()
    purpleP.draw()
    fireBox.draw()
    platformWood.draw()
    flooring.draw()
    code2.draw()
    stick.draw()
    doorO.draw()
    doorC.draw()

    for i in range(len(padKeys)):
        padKeys[i].draw()
        s2padKeys[i].draw()
        s3padKeys[i].draw()

    LEVEL(logo4)

    if not(burned):
        stick.visible=False

    if marbleWin:
        if not(burned):
            blockPhy(blueBox,RightStance,50,floor)
            blockPhy(blueBox,LeftStance,50,floor)
        else:
            blockPhy(stick,RightStance,37,floor)
            blockPhy(stick,LeftStance,37,floor)
    
    wallBorder()
    PlayerMovement()
  # timer for reading
    if time:
        timer+=1
        marbleBall.x = cup2.x

        game.drawText("The marble of wisdom",350,80,rgbp)
  
  # stop the timer
    if timer == 40:
        timer = 40
        time = False

        # cup game
        cup2.y = 420
        marbleBall.x = posx
        timer = 0
    
    if cupTimer:
        cupTime +=1
        if cupTime == 40:
            marbleBall.x=posx
            cupTimer = False
      
    if not(marbleWin) and not(time):
        if cursor.collidedWith(cup1,"rectangle") and mouse.LeftClick and cup2.clicked == False and cup3.clicked == False:
            cupTimer = True
            cup1.clicked = True
            correctCup(cup1)
        lift()
        if cupTimer and cup1.clicked == True:
            cup1.visible = False
        if not(cupTimer) and cup1.clicked == True:
            cup1.visible = True
            cup1.clicked = False

        if cursor.collidedWith(cup2,"rectangle") and mouse.LeftClick and cup1.clicked == False and cup3.clicked == False:
            cupTimer = True
            cup2.clicked = True
            correctCup(cup2)
        lift()
        if cupTimer and cup2.clicked == True:
            cup2.visible = False
        if not(cupTimer) and cup2.clicked == True:
            cup2.visible = True
            cup2.clicked = False

        if cursor.collidedWith(cup3,"rectangle") and mouse.LeftClick and cup1.clicked == False and cup2.clicked == False:
            cupTimer = True
            cup3.clicked = True
            correctCup(cup3)
        lift()
        if cupTimer and cup3.clicked == True:
            cup3.visible = False
        if not(cupTimer) and cup3.clicked == True:
            cup3.visible = True
            cup3.clicked = False
    
    if marbleWin:
        cup1.clicked = True
        cup2.clicked = True
        cup3.clicked = True
        blueBox.visible = nextbox
        enter.visible = True
        exit.visible = False

        if text:
            game.drawText(" Throw the box in first >>>",550,270,rgbp)

        if RightStance.collidedWith(enter,"rectangle") or LeftStance.collidedWith(enter,"rectangle"):
            blueBox.moveTo(100,370)
            marbleBall.visible = False
            cup1.visible = False
            cup2.visible = False
            cup3.visible = False
            text = False
            next = True
            flooring.visible = True
            portalON.visible = True
            platformWood.visible=True
            burnWood.visible=True
            cardCode.visible=True
            code2.visible=False
            if burned:
                burnWood.visible=False
                padLock.visible=True
                padKeys[0].visible=True
                s2padKeys[0].visible=True
                s3padKeys[0].visible=True
                stick.moveTo(100,370)
            paperPlatform.visible=False
            paperstack.visible=False
            spawn()


        if blueBox.collidedWith(enter,"rectangle"):
            nextbox = False
            blueBox.moveTo(enter.x,enter.y)
            blueBox.visible = nextbox

        if next:
            nextbox = True
            blueBox.visible = nextbox
            enter.visible = False
            exit.visible = True
        
        if stick.collidedWith(exit,"rectangle") and not(pickUp):
            stick.visible=False
            room1=True

        if RightStance.collidedWith(exit,"rectangle") or LeftStance.collidedWith(exit,"rectangle"):
            nextbox = False
            marbleBall.visible = True
            blueBox.visible = nextbox
            cup1.visible = True
            cup2.visible = True
            cup3.visible = True
            text=True
            next = False
            RightStance.moveTo(900,390)
            LeftStance.moveTo(900,390)
            flooring.visible = False
            portalON.visible = False
            portalOFF.visible = False
            blueP.visible=False
            redP.visible=False
            greenP.visible=False
            purpleP.visible=False
            fireBox.visible = False
            platformWood.visible=False
            burnWood.visible=False
            cardCode.visible=False
            padLock.visible=False
            for i in range(len(padKeys)):
                padKeys[i].visible=False
                s2padKeys[i].visible=False
                s3padKeys[i].visible=False
            paperPlatform.visible=True
            paperstack.visible=True
            stick.moveTo(800,370)
            stick.visible=True
    
    if stick.visible and pickUp:
        if cursor.collidedWith(paperstack,"rectangle") and mouse.LeftClick:
            pageFlip.play()
            paperstack.visible=False
            code2.moveTo(300,430)
            code2.visible=True

    # room 2 puzzles


    if RightStance.collidedWith(portalON,"rectangle") or LeftStance.collidedWith(portalON,"rectangle"):
        if keys.Pressed[K_e]:
            buttonClicker.play()
            portalOFF.visible=True
            portalON.visible=False
            if portalActivate==2:
                portalActivate=1
            elif portalActivate==1:
                portalActivate=2
    else:
        if next:
          portalON.visible=True
          portalOFF.visible=False
      
    if portalActivate == 1 and next:
        blueP.visible=True
        redP.visible=True
        purpleP.visible=False
        greenP.visible=False
    if portalActivate==2 and next:
        blueP.visible = False
        redP.visible = False
        purpleP.visible=True
        greenP.visible=True
    
    if blueBox.collidedWith(flooring,"rectangle"):
        switch = True
        fireBox.moveTo(70,150)
    if switch and next:
        fireBox.visible=True
        blueBox.visible=False
    else:
        if next:
            fireBox.visible=False
            blueBox.visible=True
    
    if not(fireBox.collidedWith(floor,"rectangle") or fireBox.collidedWith(platformWood,"rectangle")):
        fireBox.y+=7
    if fireBox.x > game.width:
        fireBox.x-=40
    if fireBox.x <0:
        fireBox.x+=40

    if fireBox.collidedWith(burnWood,"rectangle"):
        padLock.visible=True
        fireBox.visible=False
        burnWood.visible=False
        burned=True
        
        padKeys[0].visible=True
        s2padKeys[0].visible=True
        s3padKeys[0].visible=True

    if burned:
        fireBox.visible=False
        stick.visible=True
    
    # number lock 1
    for i in range(len(padKeys)):
        if cursor.collidedWith(padKeys[i]) and mouse.LeftButton:
            clickSOUND.play()
            if padNumber1==9:
                padNumber1=0
            else:
                padNumber1+=.5

    if burned and next:
        if padNumber1==0:
            pad0.visible=True
            pad9.visible=False
        if padNumber1==1:
            pad0.visible=False
            pad1.visible=True
        if padNumber1==2:
            pad1.visible=False
            pad2.visible=True
        if padNumber1==3:
            pad2.visible=False
            pad3.visible=True
        if padNumber1==4:
            pad3.visible=False
            pad4.visible=True
        if padNumber1==5:
            pad4.visible=False
            pad5.visible=True
        if padNumber1==6:
            pad5.visible=False
            pad6.visible=True
        if padNumber1==7:
            pad6.visible=False
            pad7.visible=True
        if padNumber1==8:
            pad7.visible=False
            pad8.visible=True
        if padNumber1==9:
            pad8.visible=False
            pad9.visible=True
        
    # number lock 2
    for i in range(len(s2padKeys)):
        if cursor.collidedWith(s2padKeys[i]) and mouse.LeftButton:
            clickSOUND.play()
            if padNumber2==9:
                padNumber2=0
            else:
                padNumber2+=.5

    if burned and next:
        if padNumber2==0:
            s2pad0.visible=True
            s2pad9.visible=False
        if padNumber2==1:
            s2pad0.visible=False
            s2pad1.visible=True
        if padNumber2==2:
            s2pad1.visible=False
            s2pad2.visible=True
        if padNumber2==3:
            s2pad2.visible=False
            s2pad3.visible=True
        if padNumber2==4:
            s2pad3.visible=False
            s2pad4.visible=True
        if padNumber2==5:
            s2pad4.visible=False
            s2pad5.visible=True
        if padNumber2==6:
            s2pad5.visible=False
            s2pad6.visible=True
        if padNumber2==7:
            s2pad6.visible=False
            s2pad7.visible=True
        if padNumber2==8:
            s2pad7.visible=False
            s2pad8.visible=True
        if padNumber2==9:
            s2pad8.visible=False
            s2pad9.visible=True
    
    # number lock 3
    for i in range(len(s3padKeys)):
        if cursor.collidedWith(s3padKeys[i]) and mouse.LeftButton:
            clickSOUND.play()
            if padNumber3==9:
                padNumber3=0
            else:
                padNumber3+=.5

    if burned and next:
        if padNumber3==0:
            s3pad0.visible=True
            s3pad9.visible=False
        if padNumber3==1:
            s3pad0.visible=False
            s3pad1.visible=True
        if padNumber3==2:
            s3pad1.visible=False
            s3pad2.visible=True
        if padNumber3==3:
            s3pad2.visible=False
            s3pad3.visible=True
        if padNumber3==4:
            s3pad3.visible=False
            s3pad4.visible=True
        if padNumber3==5:
            s3pad4.visible=False
            s3pad5.visible=True
        if padNumber3==6:
            s3pad5.visible=False
            s3pad6.visible=True
        if padNumber3==7:
            s3pad6.visible=False
            s3pad7.visible=True
        if padNumber3==8:
            s3pad7.visible=False
            s3pad8.visible=True
        if padNumber3==9:
            s3pad8.visible=False
            s3pad9.visible=True
    
    # complete the lock
    if pad1.visible and s2pad3.visible and s3pad8.visible:
        door()
    else:
        doorC.visible=False
        doorO.visible=False

    # teleporting feature (BOX)
    if blueBox.collidedWith(redP) and pickUp==False:
        portalOpen.play()
        blueBox.moveTo(blueP.x+50,blueP.y)

    if fireBox.collidedWith(greenP):
        portalOpen.play()
        fireBox.moveTo(purpleP.x+40,purpleP.y-30)

    cursorPhys()
    game.update(30)

# level 5

level5 = Image("./images/levels/level5/level5.png",game)
level5.moveTo(-200,300)

# scrollpaper
colorPaper = Image("./images/levels/level5/scrollpaper.png",game)
colorPaper.resizeBy(-50)
colorPaper.visible=False

# scroll
scroll = Image("./images/levels/level5/scroll.png",game)
scroll.resizeBy(-90)
scroll.moveTo(270,440)

# numbers set 1
s1boxone = Image("./images/levels/level5/buttons/one.png",game)
s1boxtwo = Image("./images/levels/level5/buttons/two.png",game)
s1boxthree = Image("./images/levels/level5/buttons/three.png",game)
s1boxfour = Image("./images/levels/level5/buttons/four.png",game)
s1boxfive = Image("./images/levels/level5/buttons/five.png",game)
s1boxsix = Image("./images/levels/level5/buttons/six.png",game)
s1boxseven = Image("./images/levels/level5/buttons/seven.png",game)
s1boxeight = Image("./images/levels/level5/buttons/eight.png",game)
s1boxnine = Image("./images/levels/level5/buttons/nine.png",game)
s1boxzero = Image("./images/levels/level5/buttons/zero.png",game)

boxset1 = [s1boxzero,s1boxone,s1boxtwo,s1boxthree,s1boxfour,s1boxfive,s1boxsix,s1boxseven,s1boxeight,s1boxnine]

# numbers set 2
s2boxone = Image("./images/levels/level5/buttons/one.png",game)
s2boxtwo = Image("./images/levels/level5/buttons/two.png",game)
s2boxthree = Image("./images/levels/level5/buttons/three.png",game)
s2boxfour = Image("./images/levels/level5/buttons/four.png",game)
s2boxfive = Image("./images/levels/level5/buttons/five.png",game)
s2boxsix = Image("./images/levels/level5/buttons/six.png",game)
s2boxseven = Image("./images/levels/level5/buttons/seven.png",game)
s2boxeight = Image("./images/levels/level5/buttons/eight.png",game)
s2boxnine = Image("./images/levels/level5/buttons/nine.png",game)
s2boxzero = Image("./images/levels/level5/buttons/zero.png",game)

boxset2 = [s2boxzero,s2boxone,s2boxtwo,s2boxthree,s2boxfour,s2boxfive,s2boxsix,s2boxseven,s2boxeight,s2boxnine]

for i in range(len(boxset1)):
    boxset1[i].resizeBy(-55)
    boxset2[i].resizeBy(-55)
    boxset1[i].moveTo(611,273)
    boxset2[i].moveTo(783,271)
    boxset1[i].visible=False
    boxset2[i].visible=False

puzzle1 = Image("./images/levels/level5/puzzle1.png",game)
puzzle1.moveTo(700,200)
puzzle1.resizeBy(-55)

blueFlash = Image("./images/levels/level5/flashinglights/blueFlash.png",game)
greenFlash = Image("./images/levels/level5/flashinglights/greenFlash.png",game)
orangeFlash = Image("./images/levels/level5/flashinglights/orangeFlash.png",game)
purpleFlash = Image("./images/levels/level5/flashinglights/purpleFlash.png",game)
redFlash = Image("./images/levels/level5/flashinglights/redFlash.png",game)
yellowFlash = Image("./images/levels/level5/flashinglights/yellowFlash.png",game)

greenButton = Image("./images/levels/level5/green.png",game)
greenButton.moveTo(697,272)
greenButton.resizeBy(-56)
greenButton.visible=False
redButton = Image("./images/levels/level5/red.png",game)
redButton.moveTo(697,272)
redButton.resizeBy(-56)
redButton.visible=False

lights = [blueFlash,greenFlash,orangeFlash,purpleFlash,redFlash,yellowFlash]

for i in range(len(lights)):
  lights[i].moveTo(700,380)
  lights[i].resizeBy(-50)
  lights[i].visible=False
  
sheet = Image("./images/levels/level5/sheet.png",game)
sheet.moveTo(400,300)
sheet.resizeBy(-85)

Manual = Image("./images/levels/level5/Manual.png",game)
Manual.resizeBy(-35)
Manual.moveTo(500,300)
Manual.visible=False

# blobbles ------------------------------------------------- **

s10 = Image("./images/levels/level5/BLOBBLES/0.png",game)
s11 = Image("./images/levels/level5/BLOBBLES/1.png",game)
s12 = Image("./images/levels/level5/BLOBBLES/2.png",game)
s13 = Image("./images/levels/level5/BLOBBLES/3.png",game)
s14 = Image("./images/levels/level5/BLOBBLES/4.png",game)
s15 = Image("./images/levels/level5/BLOBBLES/5.png",game)
s16 = Image("./images/levels/level5/BLOBBLES/6.png",game)
s17 = Image("./images/levels/level5/BLOBBLES/7.png",game)
s18 = Image("./images/levels/level5/BLOBBLES/8.png",game)
s19 = Image("./images/levels/level5/BLOBBLES/9.png",game)
s1=[s10,s11,s12,s13,s14,s15,s16,s17,s18,s19]

# blobbles set 2 ------------------------------------------------- **

s20 = Image("./images/levels/level5/BLOBBLES/0.png",game)
s21 = Image("./images/levels/level5/BLOBBLES/1.png",game)
s22 = Image("./images/levels/level5/BLOBBLES/2.png",game)
s23 = Image("./images/levels/level5/BLOBBLES/3.png",game)
s24 = Image("./images/levels/level5/BLOBBLES/4.png",game)
s25 = Image("./images/levels/level5/BLOBBLES/5.png",game)
s26 = Image("./images/levels/level5/BLOBBLES/6.png",game)
s27 = Image("./images/levels/level5/BLOBBLES/7.png",game)
s28 = Image("./images/levels/level5/BLOBBLES/8.png",game)
s29 = Image("./images/levels/level5/BLOBBLES/9.png",game)
s2=[s20,s21,s22,s23,s24,s25,s26,s27,s28,s29]

# blobbles set 3 ------------------------------------------------- **
s30 = Image("./images/levels/level5/BLOBBLES/0.png",game) 
s31 = Image("./images/levels/level5/BLOBBLES/1.png",game) 
s32 = Image("./images/levels/level5/BLOBBLES/2.png",game) 
s33 = Image("./images/levels/level5/BLOBBLES/3.png",game) 
s34 = Image("./images/levels/level5/BLOBBLES/4.png",game) 
s35 = Image("./images/levels/level5/BLOBBLES/5.png",game) 
s36 = Image("./images/levels/level5/BLOBBLES/6.png",game) 
s37 = Image("./images/levels/level5/BLOBBLES/7.png",game) 
s38 = Image("./images/levels/level5/BLOBBLES/8.png",game) 
s39 = Image("./images/levels/level5/BLOBBLES/9.png",game) 
s3=[s30,s31,s32,s33,s34,s35,s36,s37,s38,s39]

# blobbles set 4 ------------------------------------------------- **
s40 = Image("./images/levels/level5/BLOBBLES/0.png",game)
s41 = Image("./images/levels/level5/BLOBBLES/1.png",game)
s42 = Image("./images/levels/level5/BLOBBLES/2.png",game)
s43 = Image("./images/levels/level5/BLOBBLES/3.png",game)
s44 = Image("./images/levels/level5/BLOBBLES/4.png",game)
s45 = Image("./images/levels/level5/BLOBBLES/5.png",game)
s46 = Image("./images/levels/level5/BLOBBLES/6.png",game)
s47 = Image("./images/levels/level5/BLOBBLES/7.png",game)
s48 = Image("./images/levels/level5/BLOBBLES/8.png",game)
s49 = Image("./images/levels/level5/BLOBBLES/9.png",game)
s4=[s40,s41,s42,s43,s44,s45,s46,s47,s48,s49]

# blobbles set 5 ------------------------------------------------- **
s50 = Image("./images/levels/level5/BLOBBLES/0.png",game)
s51 = Image("./images/levels/level5/BLOBBLES/1.png",game)
s52 = Image("./images/levels/level5/BLOBBLES/2.png",game)
s53 = Image("./images/levels/level5/BLOBBLES/3.png",game)
s54 = Image("./images/levels/level5/BLOBBLES/4.png",game)
s55 = Image("./images/levels/level5/BLOBBLES/5.png",game)
s56 = Image("./images/levels/level5/BLOBBLES/6.png",game)
s57 = Image("./images/levels/level5/BLOBBLES/7.png",game)
s58 = Image("./images/levels/level5/BLOBBLES/8.png",game)
s59 = Image("./images/levels/level5/BLOBBLES/9.png",game)
s5=[s50,s51,s52,s53,s54,s55,s56,s57,s58,s59]

# blobbles set 6 ------------------------------------------------- **
s60 = Image("./images/levels/level5/BLOBBLES/0.png",game)
s61 = Image("./images/levels/level5/BLOBBLES/1.png",game)
s62 = Image("./images/levels/level5/BLOBBLES/2.png",game)
s63 = Image("./images/levels/level5/BLOBBLES/3.png",game)
s64 = Image("./images/levels/level5/BLOBBLES/4.png",game)
s65 = Image("./images/levels/level5/BLOBBLES/5.png",game)
s66 = Image("./images/levels/level5/BLOBBLES/6.png",game)
s67 = Image("./images/levels/level5/BLOBBLES/7.png",game)
s68 = Image("./images/levels/level5/BLOBBLES/8.png",game)
s69 = Image("./images/levels/level5/BLOBBLES/9.png",game)
s6=[s60,s61,s62,s63,s64,s65,s66,s67,s68,s69]

# blobbles set 7 ------------------------------------------------- **
s70 = Image("./images/levels/level5/BLOBBLES/0.png",game)
s71 = Image("./images/levels/level5/BLOBBLES/1.png",game)
s72 = Image("./images/levels/level5/BLOBBLES/2.png",game)
s73 = Image("./images/levels/level5/BLOBBLES/3.png",game)
s74 = Image("./images/levels/level5/BLOBBLES/4.png",game)
s75 = Image("./images/levels/level5/BLOBBLES/5.png",game)
s76 = Image("./images/levels/level5/BLOBBLES/6.png",game)
s77 = Image("./images/levels/level5/BLOBBLES/7.png",game)
s78 = Image("./images/levels/level5/BLOBBLES/8.png",game)
s79 = Image("./images/levels/level5/BLOBBLES/9.png",game)
s7=[s70,s71,s72,s73,s74,s75,s76,s77,s78,s79]

# blobbles set 8 ------------------------------------------------- **
s80 = Image("./images/levels/level5/BLOBBLES/0.png",game)
s81 = Image("./images/levels/level5/BLOBBLES/1.png",game)
s82 = Image("./images/levels/level5/BLOBBLES/2.png",game)
s83 = Image("./images/levels/level5/BLOBBLES/3.png",game)
s84 = Image("./images/levels/level5/BLOBBLES/4.png",game)
s85 = Image("./images/levels/level5/BLOBBLES/5.png",game)
s86 = Image("./images/levels/level5/BLOBBLES/6.png",game)
s87 = Image("./images/levels/level5/BLOBBLES/7.png",game)
s88 = Image("./images/levels/level5/BLOBBLES/8.png",game)
s89 = Image("./images/levels/level5/BLOBBLES/9.png",game)

s8=[s80,s81,s82,s83,s84,s85,s86,s87,s88,s89]

# bobble settings --------------------------------------------- **
for i in range(len(s1)):
    s1[i].resizeBy(-60)
    s1[i].moveTo(45,200)
    s1[i].visible=False

    s2[i].resizeBy(-60)
    s2[i].moveTo(100,200)
    s2[i].visible=False

    s3[i].resizeBy(-60)
    s3[i].moveTo(155,200)
    s3[i].visible=False

    s4[i].resizeBy(-60)
    s4[i].moveTo(210,200)
    s4[i].visible=False

    s5[i].resizeBy(-60)
    s5[i].moveTo(265,200)
    s5[i].visible=False

    s6[i].resizeBy(-60)
    s6[i].moveTo(320,200)
    s6[i].visible=False

    s7[i].resizeBy(-60)
    s7[i].moveTo(375,200)
    s7[i].visible=False

    s8[i].resizeBy(-60)
    s8[i].moveTo(430,200)
    s8[i].visible=False

mobility = True
s1boxcounter=0
s2boxcounter=0
flashTimer = 0
boxCorrect = False
colorCorrect = False

s1blobbles = 0
s2blobbles = 0
s3blobbles = 0
s4blobbles = 0
s5blobbles = 0
s6blobbles = 0
s7blobbles = 0
s8blobbles = 0

def combinationLock(item1,item2,item3,item4,item5,item6,item7,item8,item9,item0,itemCounter):
    if itemCounter == 0:
      item0.visible=True
      item9.visible=False
    if itemCounter == 1:
      item1.visible=True
      item0.visible=False
    if itemCounter == 2:
      item2.visible=True
      item1.visible=False
    if itemCounter == 3:
      item3.visible=True
      item2.visible=False
    if itemCounter == 4:
      item4.visible=True
      item3.visible=False
    if itemCounter == 5:
      item5.visible=True
      item4.visible=False
    if itemCounter == 6:
      item6.visible=True
      item5.visible=False
    if itemCounter == 7:
      item7.visible=True
      item6.visible=False
    if itemCounter == 8:
      item8.visible=True
      item7.visible=False
    if itemCounter == 9:
      item9.visible=True
      item8.visible=False

blobblesWIN=False

doorO.visible=False
doorC.visible=False

spawn()
game.over=False
while not(game.over) and not(leave):
    game.processInput()
    bk.draw()
    floor.draw()
    level5.draw()

    scroll.draw()
    puzzle1.draw()
    greenButton.draw()
    redButton.draw()
    sheet.draw()
    doorO.draw()
    doorC.draw()

    # buttons
    for i in range(len(boxset1)):
        boxset2[i].draw()
        boxset1[i].draw()

    # flashing lights
    for i in range(len(lights)):
        lights[i].draw()
    
    # BLOBBLES
    for i in range(len(s1)):
        s1[i].draw()
        s2[i].draw()
        s3[i].draw()
        s4[i].draw()
        s5[i].draw()
        s6[i].draw()
        s7[i].draw()
        s8[i].draw()
  
    LEVEL(level5)
    wallBorder()
    PlayerMovement(mobility)
    colorPaper.draw()

    Manual.draw()
    
    if RightStance.collidedWith(scroll,"rectangle") or LeftStance.collidedWith(scroll,"rectangle"):
        if keys.Pressed[K_e]:
            pageFlip.play()
            colorPaper.visible=True
            mobility = False
        if keys.Pressed[K_q]:
            mobility=True
            colorPaper.visible=False

    for i in range(len(boxset1)):
      if cursor.collidedWith(boxset1[i],"rectangle"):
        if mouse.LeftButton:
          clickSOUND.play()
          if s1boxcounter == 9:
            s1boxcounter=0
          else:
            s1boxcounter+=1
      if cursor.collidedWith(boxset2[i],"rectangle"):
        if mouse.LeftButton:
          clickSOUND.play()
          if s2boxcounter == 9:
            s2boxcounter=0
          else:
            s2boxcounter+=1

  # number lock for set 1
    if s1boxcounter == 0:
      s1boxzero.visible=True
      s1boxnine.visible=False
    if s1boxcounter == 1:
      s1boxone.visible=True
      s1boxzero.visible=False
    if s1boxcounter == 2:
      s1boxtwo.visible=True
      s1boxone.visible=False
    if s1boxcounter == 3:
      s1boxthree.visible=True
      s1boxtwo.visible=False
    if s1boxcounter == 4:
      s1boxfour.visible=True
      s1boxthree.visible=False
    if s1boxcounter == 5:
      s1boxfive.visible=True
      s1boxfour.visible=False
    if s1boxcounter == 6:
      s1boxsix.visible=True
      s1boxfive.visible=False
    if s1boxcounter == 7:
      s1boxseven.visible=True
      s1boxsix.visible=False
    if s1boxcounter == 8:
      s1boxeight.visible=True
      s1boxseven.visible=False
    if s1boxcounter == 9:
      s1boxnine.visible=True
      s1boxeight.visible=False
            
  # number switching for set 2
    if s2boxcounter == 0:
      s2boxzero.visible=True
      s2boxnine.visible=False
    if s2boxcounter == 1:
      s2boxone.visible=True
      s2boxzero.visible=False
    if s2boxcounter == 2:
      s2boxtwo.visible=True
      s2boxone.visible=False
    if s2boxcounter == 3:
      s2boxthree.visible=True
      s2boxtwo.visible=False
    if s2boxcounter == 4:
      s2boxfour.visible=True
      s2boxthree.visible=False
    if s2boxcounter == 5:
      s2boxfive.visible=True
      s2boxfour.visible=False
    if s2boxcounter == 6:
      s2boxsix.visible=True
      s2boxfive.visible=False
    if s2boxcounter == 7:
      s2boxseven.visible=True
      s2boxsix.visible=False
    if s2boxcounter == 8:
      s2boxeight.visible=True
      s2boxseven.visible=False
    if s2boxcounter == 9:
      s2boxnine.visible=True
      s2boxeight.visible=False

    # flashing lights
    flashTimer += .5
    if flashTimer == 4:
      blueFlash.visible=True
      yellowFlash.visible=False
    if flashTimer == 8:
      blueFlash.visible=False
      greenFlash.visible=True
    if flashTimer == 12:
      greenFlash.visible=False
      orangeFlash.visible=True
    if flashTimer == 16:
      orangeFlash.visible=False
      purpleFlash.visible=True
    if flashTimer == 20:
      purpleFlash.visible=False
      redFlash.visible=True
    if flashTimer == 24:
      redFlash.visible=False
      yellowFlash.visible=True
    if flashTimer == 28:
      flashTimer = 0
    
    # correct code
    if s1boxthree.visible and s2boxone.visible:
        boxCorrect=True
    if cursor.collidedWith(redButton,"rectangle") and mouse.LeftButton and boxCorrect and blueFlash.visible:
        portalOpen.play()
        colorCorrect=True
        redButton.visible=False
    if colorCorrect and boxCorrect:
        redButton.visible=False
        greenButton.visible=True
    else:
        redButton.visible=True
        greenButton.visible=False
    
    # manual visibilty
    if cursor.collidedWith(sheet,"rectangle") and mouse.LeftButton:
        pageFlip.play()
        Manual.visible=True
    if keys.Pressed[K_q]:
        Manual.visible=False
    
    # Bobbles --------------------------------------------------------
    for i in range(len(s1)):
        if cursor.collidedWith(s1[i],"rectangle"):
            if mouse.LeftButton:
                buttonClick.play()
                if s1blobbles == 9:
                    s1blobbles=0
                else:
                    s1blobbles+=.5
        if cursor.collidedWith(s2[i],"rectangle"):
            if mouse.LeftButton:
                buttonClick.play()
                if s2blobbles == 9:
                    s2blobbles=0
                else:
                    s2blobbles+=.5
        if cursor.collidedWith(s3[i],"rectangle"):
            if mouse.LeftButton:
                buttonClick.play()
                if s3blobbles == 9:
                    s3blobbles=0
                else:
                    s3blobbles+=.5
        if cursor.collidedWith(s4[i],"rectangle"):
            if mouse.LeftButton:
                buttonClick.play()
                if s4blobbles == 9:
                    s4blobbles=0
                else:
                    s4blobbles+=.5
        if cursor.collidedWith(s5[i],"rectangle"):
            if mouse.LeftButton:
                buttonClick.play()
                if s5blobbles == 9:
                    s5blobbles=0
                else:
                    s5blobbles+=.5
        if cursor.collidedWith(s6[i],"rectangle"):
            if mouse.LeftButton:
                buttonClick.play()
                if s6blobbles == 9:
                    s6blobbles=0
                else:
                    s6blobbles+=.5
        if cursor.collidedWith(s7[i],"rectangle"):
            if mouse.LeftButton:
                buttonClick.play()
                if s7blobbles == 9:
                    s7blobbles=0
                else:
                    s7blobbles+=.5
        if cursor.collidedWith(s8[i],"rectangle"):
            if mouse.LeftButton:
                buttonClick.play()
                if s8blobbles == 9:
                    s8blobbles=0
                else:
                    s8blobbles+=.5
    # repeat of blobbles if statements --------------------------------------------------------------------------------------------------------
    combinationLock(s11,s12,s13,s14,s15,s16,s17,s18,s19,s10,s1blobbles)
    combinationLock(s21,s22,s23,s24,s25,s26,s27,s28,s29,s20,s2blobbles)
    combinationLock(s31,s32,s33,s34,s35,s36,s37,s38,s39,s30,s3blobbles)
    combinationLock(s41,s42,s43,s44,s45,s46,s47,s48,s49,s40,s4blobbles)
    combinationLock(s51,s52,s53,s54,s55,s56,s57,s58,s59,s50,s5blobbles)
    combinationLock(s61,s62,s63,s64,s65,s66,s67,s68,s69,s60,s6blobbles)
    combinationLock(s71,s72,s73,s74,s75,s76,s77,s78,s79,s70,s7blobbles)
    combinationLock(s81,s82,s83,s84,s85,s86,s87,s88,s89,s80,s8blobbles)

    if s15.visible and s23.visible and s37.visible and s48.visible and s58.visible and s60.visible and s77.visible and s88.visible:
        blobblesWIN = True
    
    if blobblesWIN and boxCorrect and colorCorrect:
        door()
    else:
        doorC.visible=False
        doorO.visible=False

    cursorPhys()
    game.update(30)

#level 6 ---------------------------------------------------------------------------------------

rifle = Image("./images/levels/bosslevel/rifle.png",game)
rifle.resizeBy(-90)
rifle.moveTo(850,100)

table = Image("./images/levels/bosslevel/table.png",game)
table.resizeBy(-80)
table.moveTo(250,435)

laptop = Image("./images/levels/bosslevel/laptop.png",game)
laptop.resizeBy(-80)
laptop.moveTo(table.x,table.y-50)

# platform for gun
gunslab = Shape("bar",game,200,30,(125,125,125))
gunslab.moveTo(760,120)

# computer
screen = Image("./images/levels/bosslevel/computerscreen.jpg",game)
screen.moveTo(500,300)
screen.visible=False

colorBLANK = Image("./images/levels/bosslevel/slippaper.png",game)
colorBLANK.moveTo(600,440)

colorScroll = Image("./images/levels/bosslevel/scroll.png",game)
colorScroll.moveTo(500,300)
colorScroll.resizeBy(-50)
colorScroll.visible=False

appleCode = Image("./images/levels/bosslevel/purpleapple.png",game)
appleCode.moveTo(260,100)

# combination set 1
combZero = Image("./images/levels/level5/BLOBBLES/0.png",game)
combOne = Image("./images/levels/level5/BLOBBLES/1.png",game)
combTwo = Image("./images/levels/level5/BLOBBLES/2.png",game)
combThree = Image("./images/levels/level5/BLOBBLES/3.png",game)
combFour = Image("./images/levels/level5/BLOBBLES/4.png",game)
combFive = Image("./images/levels/level5/BLOBBLES/5.png",game)
combSix = Image("./images/levels/level5/BLOBBLES/6.png",game)
combSeven = Image("./images/levels/level5/BLOBBLES/7.png",game)
combEight = Image("./images/levels/level5/BLOBBLES/8.png",game)
combNine = Image("./images/levels/level5/BLOBBLES/9.png",game)
combS1 = [combZero,combOne,combTwo,combThree,combFour,combFive,combSix,combSeven,combEight,combNine]
counterS1=0

# combination set 2
s2combZero = Image("./images/levels/level5/BLOBBLES/0.png",game)
s2combOne = Image("./images/levels/level5/BLOBBLES/1.png",game)
s2combTwo = Image("./images/levels/level5/BLOBBLES/2.png",game)
s2combThree = Image("./images/levels/level5/BLOBBLES/3.png",game)
s2combFour = Image("./images/levels/level5/BLOBBLES/4.png",game)
s2combFive = Image("./images/levels/level5/BLOBBLES/5.png",game)
s2combSix = Image("./images/levels/level5/BLOBBLES/6.png",game)
s2combSeven = Image("./images/levels/level5/BLOBBLES/7.png",game)
s2combEight = Image("./images/levels/level5/BLOBBLES/8.png",game)
s2combNine = Image("./images/levels/level5/BLOBBLES/9.png",game)
combS2 = [s2combZero,s2combOne,s2combTwo,s2combThree,s2combFour,s2combFive,s2combSix,s2combSeven,s2combEight,s2combNine]
counterS2=0

# combination set 3
s3combZero = Image("./images/levels/level5/BLOBBLES/0.png",game)
s3combOne = Image("./images/levels/level5/BLOBBLES/1.png",game)
s3combTwo = Image("./images/levels/level5/BLOBBLES/2.png",game)
s3combThree = Image("./images/levels/level5/BLOBBLES/3.png",game)
s3combFour = Image("./images/levels/level5/BLOBBLES/4.png",game)
s3combFive = Image("./images/levels/level5/BLOBBLES/5.png",game)
s3combSix = Image("./images/levels/level5/BLOBBLES/6.png",game)
s3combSeven = Image("./images/levels/level5/BLOBBLES/7.png",game)
s3combEight = Image("./images/levels/level5/BLOBBLES/8.png",game)
s3combNine = Image("./images/levels/level5/BLOBBLES/9.png",game)
combS3 = [s3combZero,s3combOne,s3combTwo,s3combThree,s3combFour,s3combFive,s3combSix,s3combSeven,s3combEight,s3combNine]
counterS3=0

# combination set 4
s4combZero = Image("./images/levels/level5/BLOBBLES/0.png",game)
s4combOne = Image("./images/levels/level5/BLOBBLES/1.png",game)
s4combTwo = Image("./images/levels/level5/BLOBBLES/2.png",game)
s4combThree = Image("./images/levels/level5/BLOBBLES/3.png",game)
s4combFour = Image("./images/levels/level5/BLOBBLES/4.png",game)
s4combFive = Image("./images/levels/level5/BLOBBLES/5.png",game)
s4combSix = Image("./images/levels/level5/BLOBBLES/6.png",game)
s4combSeven = Image("./images/levels/level5/BLOBBLES/7.png",game)
s4combEight = Image("./images/levels/level5/BLOBBLES/8.png",game)
s4combNine = Image("./images/levels/level5/BLOBBLES/9.png",game)
combS4 = [s4combZero,s4combOne,s4combTwo,s4combThree,s4combFour,s4combFive,s4combSix,s4combSeven,s4combEight,s4combNine]
counterS4=0

for i in range(len(combS1)):
    combS1[i].visible=False
    combS2[i].visible=False
    combS3[i].visible=False
    combS4[i].visible=False

    combS1[i].resizeBy(-40)
    combS2[i].resizeBy(-40)
    combS3[i].resizeBy(-40)
    combS4[i].resizeBy(-40)

    combS1[i].moveTo(600,300)
    combS2[i].moveTo(700,300)
    combS3[i].moveTo(800,300)


movementenable=True
getGun=False

level6 = Image("./images/levels/bosslevel/level6.png",game)
level6.moveTo(-200,300)

# sounds
keyboard = Sound("./sounds/Keyboard.mp3",6)

endTimer=0

spawn()
game.over = False
while not(game.over) and not(leave):
    game.processInput()
    bk.draw()
    floor.draw()
    gunslab.draw()
    table.draw()
    laptop.draw()
    colorBLANK.draw()
    appleCode.draw()
    
    for i in range(len(combS1)):
        combS1[i].draw()
        combS2[i].draw()
        combS3[i].draw()
        combS4[i].draw()

    rifle.draw()
    if getGun:
        blockPhy(rifle,LeftStance,51,floor)
        blockPhy(rifle,RightStance,51,floor)

    LEVEL(level6)
    wallBorder()
    PlayerMovement(movementenable)

    colorScroll.draw()
    screen.draw()

    if RightStance.collidedWith(laptop,"rectangle") or LeftStance.collidedWith(laptop,"rectangle"):
        if keys.Pressed[K_e]:
            keyboard.play()
            screen.visible=True
            movementenable=False
        if keys.Pressed[K_q]:
            screen.visible=False
            movementenable=True
    
    if cursor.collidedWith(colorBLANK,"rectangle") and mouse.LeftButton and not(screen.visible):
        pageFlip.play()
        colorScroll.visible=True
        movementable=False
    if keys.Pressed[K_q]:
        colorScroll.visible = False
        movementable=True

    # combination
    for i in range(len(combS1)):
        if cursor.collidedWith(combS1[i],"rectangle"):
            if mouse.LeftButton:
                buttonClick.play()
                if counterS1 == 9:
                    counterS1=0
                else:
                    counterS1+=.5
        if cursor.collidedWith(combS2[i],"rectangle"):
            if mouse.LeftButton:
                buttonClick.play()
                if counterS2 == 9:
                    counterS2=0
                else:
                    counterS2+=.5
        if cursor.collidedWith(combS3[i],"rectangle"):
            if mouse.LeftButton:
                buttonClick.play()
                if counterS3 == 9:
                    counterS3=0
                else:
                    counterS3+=.5
        if cursor.collidedWith(combS4[i],"rectangle"):
            if mouse.LeftButton:
                buttonClick.play()
                if counterS4 == 9:
                    counterS4=0
                else:
                    counterS4+=.5
    
    combinationLock(combOne,combTwo,combThree,combFour,combFive,combSix,combSeven,combEight,combNine,combZero,counterS1)
    combinationLock(s2combOne,s2combTwo,s2combThree,s2combFour,s2combFive,s2combSix,s2combSeven,s2combEight,s2combNine,s2combZero,counterS2)
    combinationLock(s3combOne,s3combTwo,s3combThree,s3combFour,s3combFive,s3combSix,s3combSeven,s3combEight,s3combNine,s3combZero,counterS3)
    combinationLock(s4combOne,s4combTwo,s4combThree,s4combFour,s4combFive,s4combSix,s4combSeven,s4combEight,s4combNine,s4combZero,counterS4)

    # 3 5 4 1
    if s4combThree.visible and combFive.visible and s2combFour.visible and s3combOne.visible:
        getGun=True
    if getGun:
        gunslab.visible=False
        endTimer +=1
    if endTimer==100:
        game.over=True


    cursorPhys()  
    game.update(30)

# BOSS LEVEL ----------------------------------------------

ammobox = Image("./images/levels/level___/ammobox.png",game)
ammobox.resizeBy(-90)
ammobox.visible=False
ammoCount = 10
shooting = False

ammoboxICON = Image("./images/levels/level___/ammobox.png",game)
ammoboxICON.resizeBy(-90)
ammoboxICON.moveTo(40,30)

gunBullet = Image("./images/levels/level___/ammo.png",game)
gunBullet.resizeBy(-95)
gunBullet.visible=False

# bullet spawn rate ---------
bulletSpawn = randint(1,30)
ammoX,ammoY = (randint(50,670),450)

# boss dodge rate -------
bossDodge = randint(1,3)

# boss shooting rate
bossShoot = randint(1,5)

rightSide = False
leftSide = False

givenAngle=0

# boss character ------ *****
bossHitbox = Image("./images/Character/hitbox.png",game)
bossHitbox.resizeBy(-60)

bossLeft = Animation("./images/Character/bossLeft.png",2,game,835/2,427,30)
bossLeft.resizeBy(-60)
bossLeft.moveTo(800,385)

bossRight = Animation("./images/Character/bossRight.png",2,game,854/2,425,30)
bossRight.resizeBy(-60)
bossRight.visible=False

bossHealth=100
bossHP = Shape("bar",game,bossHealth,20,(34,139,34))

# plasma ball ---------------- ******
plasmaball = Image("./images/levels/level___/plasma.png",game)
plasmaball.resizeBy(-95)
plasmaball.visible=False
plasmaball.moveTo(bossLeft.x,bossLeft.y+35)

# first aid
playerHp=100

firstAid = Image("./images/levels/level___/firstaid.png",game)
firstAid.moveTo(160,30)
firstAid.resizeBy(-90)

winGame = False
lostGame = False

# sounds
ammoCollection = Sound("./sounds/gunreload.mp3",1)
gunShot = Sound("./sounds/gunShot.mp3",2)
gunShot.setVolume(30)
plasma = Sound("./sounds/plasma.mp3",3)

spawn(False,True)
game.over=False
game.stopMusic()
game.setMusic("./sounds/intense.mp3")
game.playMusic()
while not(leave) and not(game.over):
    game.processInput()
    bk.draw()
    floor.draw()

    ammobox.draw()
    gunBullet.draw()
    ammoboxICON.draw()
    bossHitbox.draw()
    bossHitbox.moveTo(bossLeft.x-40,bossLeft.y)

    RPick.visible=False
    LPick.visible=False
  
    bossLeft.draw()
    bossRight.draw()
    bossHP.draw()

    firstAid.draw()

    wallBorder()
    PlayerMovement(True,True)

    plasmaball.draw()

    bossHP.moveTo(bossLeft.x-50,bossLeft.y-120)

  # gun guy physics ------
    if RightGun.collidedWith(floor,"rectangle") or LeftGun.collidedWith(floor,"rectangle"):
        if keys.Pressed[K_w]:
            RightGun.y-=170
            LeftGun.y-=170
    else:
        RightGun.y+=10
        LeftGun.y+=10

    if LeftGun.x<0:
      LeftGun.x=5
    if RightGun.x>bossLeft.x-10:
      RightGun.x=bossLeft.x-10
    if RightGun.collidedWith(bossLeft,"rectangle") or LeftGun.collidedWith(bossLeft,"rectangle"):
      playerHp-=5

    game.drawText(playerHp,210,20,rgbp)

  # ammo counter
    game.drawText(ammoCount,75,20,rgbp)

    # shooting
    if mouse.LeftClick and gunBullet.visible==False and ammoCount>0:
        gunShot.play()
        gunBullet.moveTo(RightGun.x,RightGun.y+18)
        gunBullet.visible=True
        ammoCount-=1
      
    if LeftGun.visible:
        leftSide=True
        rightSide=False
        if givenAngle == 0 and gunBullet.visible:
            givenAngle=0
            gunBullet.x+=15
        elif leftSide and not(rightSide):
            givenAngle=180
            gunBullet.rotateTo(givenAngle)
            gunBullet.x-=15
        
    if RightGun.visible:
        rightSide=True
        leftSide=False
        if givenAngle == 180 and gunBullet.visible:
            givenAngle = 180
            gunBullet.x-=15
        elif rightSide and not(leftSide):
            givenAngle=0
            gunBullet.rotateTo(givenAngle)
            gunBullet.x+=15

    if gunBullet.x<0 or gunBullet.x>game.width:
        gunBullet.visible=False
        leftSide=False
        rightSide=False

    if gunBullet.visible==False:
        bossDodge=randint(1,3)

    if RightGun.collidedWith(ammobox,"rectangle") or LeftGun.collidedWith(ammobox,"rectangle"):
        ammoCollection.play()
        ammobox.visible=False
        ammoCount = 24

    if ammobox.visible==False:
        bulletSpawn = randint(1,80)
        ammoX,ammoY = (randint(50,670),450)
    
    # gun bullet spawn rate
    if bulletSpawn == 20:
        ammobox.visible=True
        ammobox.moveTo(ammoX,ammoY)

    # boss physics -------------------------------------------- ***
    bossRight.moveTo(bossLeft.x,bossLeft.y)
    if gunBullet.collidedWith(bossHitbox,"rectangle"):
        if bossDodge == 3:
            bossLeft.y-=50
    if not(bossLeft.collidedWith(floor,"rectangle")):
        bossLeft.y+=8

    if gunBullet.collidedWith(bossLeft,"rectangle"):
        wallHit.play()
        bossHealth-=5
        gunBullet.visible=False
        bossHP.width=bossHealth

    # boss plasma shooting
    if plasmaball.visible==False:
        bossShoot=randint(1,10)
    if bossShoot == 3:
        plasma.play()
        plasmaball.visible=True
        plasmaball.x-=15
    if plasmaball.x<0 or plasmaball.x>game.width:
        plasmaball.visible=False
        plasmaball.moveTo(bossLeft.x,bossLeft.y+35)
    if plasmaball.collidedWith(RightGun,"rectangle") or plasmaball.collidedWith(LeftGun,"rectangle"):
        plasmaball.visible=False
        plasmaball.moveTo(bossLeft.x,bossLeft.y+35)
        playerHp-=5

    # win condition and lose conditions
    if playerHp<=0:
        lostGame=True
        game.over=True
    if bossHealth<=0:
        winGame=True
        game.over=True

    cursorPhys()
    game.update(30)

youwinFont = Font("green",50,None,"courier new")
youloseFont = Font("red",50,None,"courier new")

RightStance.moveTo(-10,390)
RightStance.visible=False

bossRight.moveTo(-200,385)
bossRight.visible=False

game.over=False
game.stopMusic()
if winGame:
    game.setMusic("./sounds/lobbyM.mp3")
if lostGame:
    game.setMusic("./sounds/intense.mp3")
game.playMusic()
while not(game.over) and not(leave):
    game.processInput()
    bk.draw()
    floor.draw()
    RightStance.draw()
    bossRight.draw()

    if winGame:
        game.drawText("YOU WIN!",390,100,youwinFont)
        RightStance.visible=True
        if not(RightStance.x>game.width+200):
            RightStance.x+=7
        if RightStance.x>game.width+200:
            RightStance.x = -150
    if lostGame:
        game.drawText("YOU LOSE.",390,100,youloseFont)
        RightStance.visible=True
        bossRight.visible=True

        if not(RightStance.x>game.width+200):
            RightStance.x+=7

        if not(bossRight.x>game.width+200):
            bossRight.x+=7
        if bossRight.x>game.width+200:
            bossRight.x = -200
            RightStance.x=-30

    game.update(30)

game.quit