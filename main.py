from pypresence import Presence
import pygame as gui
import sys
from pygame.locals import QUIT
import random
import time
import math
import os
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

def encrypt_and_save_integer(number, password, filepath):
    # Generate a key from the password using PBKDF2
    salt = os.urandom(16)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        iterations=100000,
        length=32,
        salt=salt,
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(password))

    # Encrypt the integer using the key
    f = Fernet(key)
    encrypted_number = f.encrypt(str(number).encode())

    with open(filepath, 'wb') as f:
        f.write(encrypted_number + salt)

def retrieve_and_decrypt_integer(password, filepath):
    # Read the encrypted number and salt from the file
    with open(filepath, 'rb') as f:
        encrypted_number_and_salt = f.read()
    encrypted_number = encrypted_number_and_salt[:-16]
    salt = encrypted_number_and_salt[-16:]

    # Generate a key from the password and salt using PBKDF2
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        iterations=100000,
        length=32,
        salt=salt,
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(password))

    # Decrypt the number using the key
    f = Fernet(key)
    decrypted_number = int(f.decrypt(encrypted_number).decode())
    return decrypted_number

# Test your functions
#encrypt_and_save_integer(69692069, b'yo', 'encrypt/encrypt.bin')
#encrypt_and_save_integer(0, b'tooyo', 'encrypt/1.bin')

client_id = "1068013390758432798"
useDiscord = True

def connect_loop():
    global RPC, useDiscord
    try:
        RPC = Presence(client_id)
        RPC.connect()
        useDiscord = True
    except:
        useDiscord = False

connect_loop()

def takeClosest(num, collection):
    return min(collection, key=lambda x: abs(x - num))

prestime=int(time.time())

gui.init()
gui.font.init()
gui.mixer.init()
S_WIDTH = 720
S_HEIGHT = 400

score = 0
totalcoins = retrieve_and_decrypt_integer(b'tooyo', 'encrypt/1.bin')
prevscore = retrieve_and_decrypt_integer(b'yo', 'encrypt/encrypt.bin')
rrand = []
lrand = [0, 20]
loop = "False"
white = (255, 255, 255)
torq = (0, 255, 255)
gold = (255, 223, 0)
secret = 0
speed = 0.5
speedupamount = -2
calcscore = score
speedingup = False
flapamount2 = 0
ycalc = 2
with open("encrypt/workingdir.bin", "r") as f:
    var = f.read().strip()
cwd = os.getcwd()
#Insert change dir to saved
os.chdir(cwd+var)

flapping = False
flapamount = 0
bird = gui.image.load('Sprites/brrrrr1.png')
bird1 = gui.transform.scale(bird, (20, 20))
currentPlayer = bird1
bird3 = gui.image.load('Sprites/brrrrr1_.png')
bird2 = gui.transform.scale(bird3, (20, 20))
selectedPlayer = 1
font = gui.font.Font('Sprites/font.ttf', 50)
fontsm = gui.font.Font('Sprites/font.ttf', 30)
fontbig = gui.font.Font('Sprites/font.ttf', 120)

'''pausetext = font.render("Paused", True, (255, 255, 255))
text = font.render(f'Score: {score}', True, white)
text2 = font.render(f'High Score: {prevscore}', True, white)
text3 = fontsm.render('Press "b" to swap backgrounds.', True, white)
text4 = fontsm.render('Press number keys or click to swap players.', True, white)
text5 = fontsm.render('Press "c" to open cosmetics.', True, white)
text6 = fontbig.render('SPEED UP!', True, torq)
text8 = font.render('Wait before pausing again', True, (255, 0, 0))
text7exec = "text7 = font.render(f'Coins: {coin.amount}', True, gold)"
text9exec = "text9 = font.render(f'Total Coins: {totalcoins}', True, gold)"
text9exec2 = "text9 = font.render(f': {haw2}', True, gold)"
textexec = "text = font.render(f'Score: {score}', True, white)"
text2exec = "text2 = font.render(f'High Score: {haw}', True, white)"'''
with open("Sprites/texts.bin", "rb") as f:
    # Read the binary data from the file
    binary_data = f.read()

# Convert the binary data to a string variable
text_data = binary_data.decode("utf-8")

# Print the contents of the string variable
exec(text_data)
coinimg = gui.image.load('Sprites/coin.png')
coinimg = gui.transform.scale(coinimg, (50, 50))
#display = gui.display.set_mode((S_WIDTH, S_HEIGHT))
display = gui.display.set_mode((S_WIDTH, S_HEIGHT), gui.SCALED + gui.RESIZABLE)
avatar1 = gui.image.load('Sprites/brrrrr1_.png')
avatar2 = gui.image.load('Sprites/brrrrr2_.png')
avatar3 = gui.image.load('Sprites/brrrrr3_.png')
avatar1_ = gui.image.load('Sprites/brrrrr1.png')
avatar2_ = gui.image.load('Sprites/brrrrr2.png')
avatar3_ = gui.image.load('Sprites/brrrrr3.png')
avatar10 = gui.transform.scale(avatar1, (75, 75))
avatar20 = gui.transform.scale(avatar2, (75, 75))
avatar30 = gui.transform.scale(avatar3, (75, 75))
avatar1 = gui.transform.scale(avatar1, (20, 20))
avatar2 = gui.transform.scale(avatar2, (20, 20))
avatar3 = gui.transform.scale(avatar3, (20, 20))
avatar1_ = gui.transform.scale(avatar1_, (20, 20))
avatar2_ = gui.transform.scale(avatar2_, (20, 20))
avatar3_ = gui.transform.scale(avatar3_, (20, 20))

goldring = gui.image.load("Sprites/goldring.png")
goldring = gui.transform.scale(goldring, (125, 125))
clock = gui.time.Clock()
hi = False
gui.display.set_caption('Faithful Flight')
icon = gui.image.load('Sprites/Icon.png')
home = gui.image.load('Sprites/home.png')
home = gui.transform.scale(home, (720, 400))
spike_right = gui.image.load('Sprites/spike_right.png')
spike_left = gui.image.load('Sprites/spike_left.png')
spike_down_long = gui.image.load('Sprites/spike_down_long.png')
spike_up_long = gui.image.load('Sprites/spike_up_long.png')
gameover = gui.image.load('Sprites/L Image.png')
gameover = gui.transform.scale(gameover, (680, 75))
gameover1 = gui.image.load('Sprites/L Image2.png')
gameover1 = gui.transform.scale(gameover1, (680, 50))
sel = gui.image.load("Sprites/sel.png")
sel = gui.transform.scale(sel, (602, 48))
back = gui.image.load("Sprites/back.png")
back = gui.transform.scale(back, (300, 20))
spike_right = gui.transform.scale(spike_right, (16, 16))
spike_left = gui.transform.scale(spike_left, (16, 16))
spike_up_long = gui.transform.scale(spike_up_long, (864, 16))
spike_down_long = gui.transform.scale(spike_down_long, (864, 16))
muon = gui.image.load("Sprites/soundon.png")
muoff = gui.image.load("Sprites/soundoff.png")
muon = gui.transform.scale(muon, (50, 50))
muoff = gui.transform.scale(muoff, (50, 50))
death = 'Sprites/death.mp3'
death = gui.mixer.Sound(death)
flap = 'Sprites/flap.mp3'
flap = gui.mixer.Sound(flap)
coinsound = 'Sprites/coincollect.mp3'
coinsound = gui.mixer.Sound(coinsound)
gui.display.set_icon(icon)
background = gui.image.load('Sprites/Backforpython.png')
background = gui.transform.scale(background, (720, 400))
background2 = gui.image.load('Sprites/Backforpython2.jpg').convert()
background2 = gui.transform.scale(background2, (720, 400))
back_set = background
backy = 1
cooldown_time = 3000
last_button_press = 0
playing = True

def pause_game(display, clock):
    global font, pausetext
    paused = True
    while paused:
        for event in gui.event.get():
            if event.type == gui.QUIT:
                gui.quit()
                quit()
            if event.type == gui.KEYDOWN:
                if event.key == gui.K_p:
                    paused = False
        gui.transform.scale(background, (720, 400))
        display.blit(pausetext, [310, 175])
        gui.display.update()
        clock.tick(60)

#Insert Change Directory Back Here
os.chdir(cwd)

class coin:
    img = coinimg
    WIDTH = img.get_width()
    HEIGHT = img.get_height()
    showing = False
    locating = True
    #def __init__(self, x, y, locating, showing):
    def collect(self):
        global text7, gold, text7exec
        self.showing = False
        self.amount += 1
        exec(text7exec)
        gui.mixer.Sound.play(coinsound)
        
    def gen(self):
        if self.locating == True:
            noidea = 2
            if noidea == 2:
                self.showing = True
                if player.x < 360:
                    self.x = random.randint(360, 660)
                    self.y = random.randint(50, 320)
                elif player.x >= 360:
                    self.x = random.randint(60, 360)
                    self.y = random.randint(50, 320)
                self.locating = False
            else:
                self.locating = False
                self.showing = False

coin.x = 0
coin.y = 0
coin.amount = 0
exec(text7exec)
exec(text9exec)

class Player:
    # Class to store the Player
    img = currentPlayer
    WIDTH = img.get_width()
    HEIGHT = img.get_height()

    def __init__(self):
        # Constructor
        self.x = S_WIDTH / 2 - self.WIDTH / 2
        self.y = S_HEIGHT - self.HEIGHT * 1.5
        self.x_movement = 0
        self.y_movement = 0

    def move_up(self):
        self.y_movement = -2

    def move_down(self):
        self.y_movement = 2

    def update(self):
        global currentPlayer
        self.x += self.x_movement
        self.y += self.y_movement
        display.blit(self.img, (self.x, self.y))

    def check_bounce(self):
        global score, loop, lrand, rrand, prevscore, speed, calcscore, speedingup, coin, speedupamount
        if self.x < 10:
            if self.x < 1:
                self.img = bird2
                self.x_movement = speed
                display.blit(self.img, (self.x, self.y))
                score += 1
                calcscore += 1
                if calcscore > 15:
                    speedupamount += 1
                    y = 1.1 * math.pow(1/2, speedupamount)
                    speed += y
                    calcscore = 0
                    speedingup = True
                if calcscore == 2:
                    speedingup = False
                addSpikes("Right")
                coin.locating = True
            #^if you survive on the wall^
            #below: checking side spikes
            else:
                roundedy = takeClosest(self.y, lrand)
                if roundedy > self.y:
                    roundedy3 = roundedy - self.y
                else:
                    roundedy3 = self.y - roundedy
                if roundedy3 < 10.1:
                    if score > prevscore:
                        prevscore = score
                        encrypt_and_save_integer(prevscore, b'yo', 'encrypt/encrypt.bin')
                    loop = "over"
                    self.img = bird1

        elif self.x > 690:
            if self.x > 700:
                self.img = bird1
                self.x_movement = -speed
                display.blit(self.img, (self.x, self.y))
                score += 1
                calcscore += 1
                if calcscore > 15:
                    speedupamount += 1
                    y = 1.1 * math.pow(1/2, speedupamount)
                    speed += y
                    calcscore = 0
                    speedingup = True
                if calcscore == 2:
                    speedingup = False
                addSpikes("Left")
                coin.locating = True
            #^if you survive on the wall^
            #below: checking side spikes
            else:
                roundedy = takeClosest(self.y, rrand)
                if roundedy > self.y:
                    roundedy3 = roundedy - self.y
                else:
                    roundedy3 = self.y - roundedy
                if roundedy3 < 10.1:
                    if score > prevscore:
                        prevscore = score
                        encrypt_and_save_integer(prevscore, b'yo', 'encrypt/encrypt.bin')
                    loop = "over"
                    self.img = bird1

    def check_collision(self):
        global loop, currentPlayer, bird, prevscore, score, bird1, coin
        superx = coin.x + 50
        supery = coin.y + 50
        if self.y <= 7:
            if score > prevscore:
                prevscore = score
                encrypt_and_save_integer(prevscore, b'yo', 'encrypt/encrypt.bin')
            loop = "over"
            currentPlayer = bird1
        elif self.y >= 373:
            if score > prevscore:
                prevscore = score
                encrypt_and_save_integer(prevscore, b'yo', 'encrypt/encrypt.bin')
            loop = "over"
            self.img = bird1
        elif self.y >= coin.y and self.y <= supery and self.x >= coin.x and self.x <= superx and coin.showing == True:
            coin.collect(coin)

    def flap(self):
        global flapping, flapamount, flapamount2
        flapping = True
        flapamount = 0
        flapamount2 = 15
        gui.mixer.Sound.play(flap)

player = Player()

def addSpikes(side):
    global lrand, rrand, score, calcscore
    rrand = [1000]
    lrand = [1000]
    scoreloop = int(calcscore / 3)
    scoreloop2 = int(calcscore / 1.5)
    if scoreloop != scoreloop2:
        scoreloop = random.randint(scoreloop, scoreloop2)
    if side == "Right":
        while scoreloop > 0:
            rightrand = random.randint(0, 382)
            sp = takeClosest(rightrand, rrand)
            if sp > rightrand:
                roundedy3 = sp - rightrand
            else:
                roundedy3 = rightrand - sp
            if roundedy3 > 14:
                scoreloop -= 1
                rrand.append(rightrand)
            
    elif side == "Left":
        while scoreloop > 0:
            leftrand = random.randint(0, 382)
            sp = takeClosest(leftrand, lrand)
            if sp > leftrand:
                roundedy3 = sp - leftrand
            else:
                roundedy3 = leftrand - sp
            if roundedy3 > 14:
                scoreloop -= 1
                lrand.append(leftrand)

var = var[1:]
loop = "False"
while True:
    if useDiscord == True:#_______________________________________________________________________________________________________________________________________________________________________________________________
        click = 1
        while useDiscord == True:
            if loop == "False":
                gui.mixer.music.unload()
                gui.mixer.music.load(var+"\Sprites\lobbymusic.mp3")
                if playing == True:
                    gui.mixer.music.play(-1)
            while loop == "Selection":
                for event in gui.event.get():
                    if event.type == QUIT:  # Exit the game on close
                        loop = "False"
                        gui.quit()
                        sys.exit()

                    if event.type == gui.MOUSEBUTTONDOWN:
                            if event.button == 1:
                                click += 1

                            if click == 1:
                                bird1 = avatar1_
                                currentPlayer = bird1
                                bird2 = avatar1
                                selectedPlayer = 1
                                player.img = currentPlayer

                            if click == 2:
                                bird1 = avatar2_
                                currentPlayer = bird1
                                bird2 = avatar2
                                selectedPlayer = 2
                                player.img = currentPlayer

                            if click == 3:
                                bird1 = avatar3_
                                currentPlayer = bird1
                                bird2 = avatar3
                                selectedPlayer = 3
                                player.img = currentPlayer

                            if click >= 3:
                                click = 0

                    if event.type == gui.KEYDOWN:
                        if event.key == gui.K_1:
                            bird1 = avatar1_
                            currentPlayer = bird1
                            bird2 = avatar1
                            selectedPlayer = 1
                            player.img = currentPlayer

                        if event.key == gui.K_2:
                            bird1 = avatar2_
                            currentPlayer = bird1
                            bird2 = avatar2
                            selectedPlayer = 2
                            player.img = currentPlayer

                        if event.key == gui.K_3:
                            bird1 = avatar3_
                            currentPlayer = bird1
                            bird2 = avatar3
                            selectedPlayer = 3
                            player.img = currentPlayer

                        if event.key == gui.K_b:
                            if backy == 1:
                                back_set = background2
                                backy = 2
                            else:
                                back_set = background
                                backy = 1
                            
                        if event.key == gui.K_BACKSPACE:
                            loop = "False"

                display.fill((0, 0, 0))
                display.blit(back_set, (0, 0))
                clock.tick(60)
                RPC.update(
                    large_image="logo1",
                    large_text="birb",
                    details=f"High score Of {prevscore}.",
                    state="In The Cosmetics Menu",
                    start=prestime,
                    buttons= [{"label": "Discord and Download","url":"https://discord.gg/TWHrUn9S2u"}]
                )
                display.blit(sel, (75, 15))
                display.blit(text3, (5, 350))
                display.blit(text4, (5, 380))
                display.blit(back, (5, 325))
                display.blit(avatar10, (95, 175))
                display.blit(avatar20, (335, 175))
                display.blit(avatar30, (555, 175))

                if selectedPlayer == 1:
                    display.blit(goldring, (70, 150))
                elif selectedPlayer == 2:
                    display.blit(goldring, (310, 150))
                elif selectedPlayer == 3:
                    display.blit(goldring, (530, 150))
                elif selectedPlayer == 4:
                    pass
                else:
                    print("Avatar error")
                gui.display.update()
        
            while loop == "False":
                for event in gui.event.get():

                    if event.type == QUIT:  # Exit the game on close
                        loop = "False"
                        gui.quit()
                        sys.exit()

                    if event.type == gui.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            loop = "True"
                        else:
                            pass

                    if event.type == gui.KEYDOWN:
                        if event.key == gui.K_c:
                            loop = "Selection"
                        elif event.key == gui.K_s:
                            if playing == True:
                                playing = False
                                gui.mixer.music.stop()
                            else:
                                playing = True
                                gui.mixer.music.play(-1)
                        else:
                            loop = "True"
                    
                haw = retrieve_and_decrypt_integer(b'yo', 'encrypt/encrypt.bin')
                haw2 = retrieve_and_decrypt_integer(b'tooyo', 'encrypt/1.bin')
                exec(text2exec)
                exec(text9exec2)
                clock.tick(60)
                display.fill((0, 0, 0))
                RPC.update(
                    large_image="logo1",
                    large_text="birb",
                    details=f"High score Of {prevscore}.",
                    state="In The Main Menu",
                    start=prestime,
                    buttons= [{"label": "Discord and Download","url":"https://discord.gg/TWHrUn9S2u"}]
                )
                display.blit(back_set, (0, 0))
                if playing == True:
                    display.blit(muon, (650, 320))
                else:
                    display.blit(muoff, (650, 320))

                display.blit(home, (0, 0))
                display.blit(text5, (200, 350))
                display.blit(text2, (235, 20))
                display.blit(text9, (60, 25))
                display.blit(coinimg, (0, 15))
                display.blit(spike_down_long, (0, 382))
                display.blit(spike_up_long, (0, 0))
                gui.display.update()

            if loop == "True":
                rrand = [1000]
                lrand = [1000]
                currentPlayer = bird1
                score = 0
                player.x_movement = -7
                player.y = 150
                player.x = 360
                player.y_movement = 2.5
                speed = 7
                ycalc = 2
                speedupamount = -2
                calcscore = score
                coin.amount = 0
                exec(text7exec)
                coin.showing = False
                last_button_press -= 3000
                gui.mixer.music.unload()
                gui.mixer.music.load(var+"\Sprites\S1.mp3")
                if playing == True:
                    gui.mixer.music.play(-1)
            while loop == "True":
                for event in gui.event.get():
                    if event.type == QUIT:  # Exit the game on close
                        loop = "False"
                        gui.quit()
                        sys.exit()

                    if event.type == gui.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            player.flap()
                        else:
                            pass

                    if event.type == gui.KEYDOWN:
                        if event.key == gui.K_SPACE:
                            player.flap()
                        if event.key == gui.K_p:
                            current_time = gui.time.get_ticks()
                            time_since_last_press = current_time - last_button_press
                            if time_since_last_press >= cooldown_time:
                                pause_game(display, clock)

                            else:
                                hi = True
                                hiballs = 70
                            last_button_press = current_time

                        if event.key == gui.K_BACKSPACE:
                            if score > prevscore:
                                prevscore = score
                                encrypt_and_save_integer(prevscore, b'yo', 'encrypt/encrypt.bin')
                            loop = "over"

                clock.tick(60)
                exec(text7exec)
                exec(textexec)
                display.fill((0, 0, 0))
                display.blit(back_set, (0, 0))

                if flapping == True:
                    if flapamount < 19:    
                        player.y_movement = -0.1
                        flapamount += 1
                        flapamount2 /= 1.15
                        player.y -= flapamount2
                    else:
                        flapamount = 0
                        flapping = False
                        player.y_movement = 0.1
                        ycalc = 1.5

                else:
                    if ycalc < 8:
                        ycalc *= 1.06
                    else:
                        ycalc *= 1.01
                    player.y += ycalc

                coin.gen(coin)
                if coin.showing == True: 
                    display.blit(coinimg, (coin.x, coin.y))

                display.blit(text, (300, 20))
                display.blit(text7, (300, 360))

                if hi == True:
                    if hiballs >= 1:
                        display.blit(text8, (110, 175))
                        hiballs -= 1
                    else:
                        hiballs = 0
                if speedingup == True:
                    display.blit(text6, (125, 175))

                player.update()
                player.check_bounce()
                player.check_collision()
                RPC.update(
                    large_image="logo1",
                    large_text="birb",
                    details=f"High score Of {prevscore}.",
                    state=f"In Game, Score: {score},   Coins: {coin.amount}",
                    start=prestime,
                    buttons= [{"label": "Discord and Download","url":"https://discord.gg/TWHrUn9S2u"}]
                )
                blitting = len(rrand)
                while blitting > 0:
                    blitting -= 1
                    rrander = rrand[blitting]
                    display.blit(spike_right, (704, rrander))
                blitting = len(lrand)
                while blitting > 0:
                    blitting -= 1
                    lrander = lrand[blitting]
                    display.blit(spike_left, (0, lrander))
                display.blit(spike_down_long, (0, 382))

                display.blit(spike_up_long, (0, 0))
                gui.display.update()
            if loop == "over":
                totalcoins += coin.amount
                encrypt_and_save_integer(totalcoins, b'tooyo', 'encrypt/1.bin')
                gui.mixer.Sound.play(death)
                gui.mixer.music.pause()
            while loop == "over":
                for event in gui.event.get():
                    if event.type == QUIT:  # Exit the game on close
                        loop = "False"
                        gui.quit()
                        sys.exit()

                    if event.type == gui.KEYDOWN:
                        loop = "False"

                    if event.type == gui.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            loop = "False"
                clock.tick(60)
                RPC.update(
                    large_image="logo1",
                    large_text="birb",
                    details=f"High score Of {prevscore}.",
                    state=f"Died With {score} Score.",
                    start=prestime,
                    buttons= [{"label": "Discord and Download","url":"https://discord.gg/TWHrUn9S2u"}]
                )
                display.blit(gameover, (25, 75))
                display.blit(gameover1, (25, 200))
                gui.display.update()
    else:#__________________________________________________________________________________________________________________________________________________________________________________________________________________________________
        click = 1
        while useDiscord == False:
            if loop == "False":
                gui.mixer.music.unload()
                gui.mixer.music.load(var+"\Sprites\lobbymusic.mp3")
                if playing == True:
                    gui.mixer.music.play(-1)
            while loop == "Selection":
                for event in gui.event.get():
                    if event.type == QUIT:  # Exit the game on close
                        loop = "False"
                        gui.quit()
                        sys.exit()

                    if event.type == gui.MOUSEBUTTONDOWN:
                            if event.button == 1:
                                click += 1

                            if click == 1:
                                bird1 = avatar1_
                                currentPlayer = bird1
                                bird2 = avatar1
                                selectedPlayer = 1
                                player.img = currentPlayer

                            if click == 2:
                                bird1 = avatar2_
                                currentPlayer = bird1
                                bird2 = avatar2
                                selectedPlayer = 2
                                player.img = currentPlayer
                            if click == 3:
                                bird1 = avatar3_
                                currentPlayer = bird1
                                bird2 = avatar3
                                selectedPlayer = 3
                                player.img = currentPlayer

                            if click >= 3:
                                click = 0

                    if event.type == gui.KEYDOWN:
                        if event.key == gui.K_1:
                            bird1 = avatar1_
                            currentPlayer = bird1
                            bird2 = avatar1
                            selectedPlayer = 1
                            player.img = currentPlayer

                        if event.key == gui.K_2:
                            bird1 = avatar2_
                            currentPlayer = bird1
                            bird2 = avatar2
                            selectedPlayer = 2
                            player.img = currentPlayer

                        if event.key == gui.K_3:
                            bird1 = avatar3_
                            currentPlayer = bird1
                            bird2 = avatar3
                            selectedPlayer = 3
                            player.img = currentPlayer

                        if event.key == gui.K_b:
                            if backy == 1:
                                back_set = background2
                                backy = 2
                            else:
                                back_set = background
                                backy = 1
                            
                        if event.key == gui.K_BACKSPACE:
                            loop = "False"

                display.fill((0, 0, 0))
                display.blit(back_set, (0, 0))
                clock.tick(60)
                display.blit(sel, (75, 15))
                display.blit(text3, (5, 350))
                display.blit(text4, (5, 380))
                display.blit(back, (5, 325))
                display.blit(avatar10, (95, 175))
                display.blit(avatar20, (335, 175))
                display.blit(avatar30, (555, 175))

                if selectedPlayer == 1:
                    display.blit(goldring, (70, 150))
                elif selectedPlayer == 2:
                    display.blit(goldring, (310, 150))
                elif selectedPlayer == 3:
                    display.blit(goldring, (530, 150))
                elif selectedPlayer == 4:
                    pass
                else:
                    print("Avatar error")
                gui.display.update()

            while loop == "False":
                for event in gui.event.get():
                    if event.type == QUIT:  # Exit the game on close
                        loop = "False"
                        gui.quit()
                        sys.exit()

                    if event.type == gui.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            loop = "True"
                        else:
                            pass

                    if event.type == gui.KEYDOWN:
                        if event.key == gui.K_c:
                            loop = "Selection"
                        elif event.key == gui.K_s:
                            if playing == True:
                                playing = False
                                gui.mixer.music.stop()
                            else:
                                playing = True
                                gui.mixer.music.play(-1)
                        else:
                            loop = "True"
                    
                haw = retrieve_and_decrypt_integer(b'yo', 'encrypt/encrypt.bin')
                haw2 = retrieve_and_decrypt_integer(b'tooyo', 'encrypt/1.bin')
                exec(text2exec)
                exec(text9exec2)
                clock.tick(60)
                display.fill((0, 0, 0))
                display.blit(back_set, (0, 0))
                if playing == True:
                    display.blit(muon, (650, 320))
                else:
                    display.blit(muoff, (650, 320))

                display.blit(home, (0, 0))
                display.blit(text5, (200, 350))
                display.blit(text2, (235, 20))
                display.blit(text9, (60, 25))
                display.blit(coinimg, (0, 15))
                display.blit(spike_down_long, (0, 382))
                display.blit(spike_up_long, (0, 0))
                gui.display.update()

            if loop == "True":
                rrand = [1000]
                lrand = [1000]
                currentPlayer = bird1
                score = 0
                player.x_movement = -7
                player.y = 150
                player.x = 360
                player.y_movement = 2.5
                speed = 7
                ycalc = 2
                speedupamount = -2
                calcscore = score
                coin.amount = 0
                exec(text7exec)
                coin.showing = False
                last_button_press -= 3000
                gui.mixer.music.unload()
                gui.mixer.music.load(var+"\Sprites\S1.mp3")
                if playing == True:
                    gui.mixer.music.play(-1)

            while loop == "True":
                for event in gui.event.get():
                    if event.type == QUIT:  # Exit the game on close
                        loop = "False"
                        gui.quit()
                        sys.exit()

                    if event.type == gui.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            player.flap()
                        else:
                            pass

                    if event.type == gui.KEYDOWN:
                        if event.key == gui.K_SPACE:
                            player.flap()
                        if event.key == gui.K_p:
                            current_time = gui.time.get_ticks()
                            time_since_last_press = current_time - last_button_press
                            if time_since_last_press >= cooldown_time:
                                pause_game(display, clock)
                            else:
                                hi = True
                                hiballs = 70
                            last_button_press = current_time
                        if event.key == gui.K_BACKSPACE:
                            if score > prevscore:
                                prevscore = score
                                encrypt_and_save_integer(prevscore, b'yo', 'encrypt/encrypt.bin')
                            loop = "over"

                clock.tick(60)
                exec(text7exec)
                exec(textexec)
                display.fill((0, 0, 0))
                display.blit(back_set, (0, 0))
                if flapping == True:
                    if flapamount < 19:    
                        player.y_movement = -0.1
                        flapamount += 1
                        flapamount2 /= 1.15
                        player.y -= flapamount2
                    else:
                        flapamount = 0
                        flapping = False
                        player.y_movement = 0.1
                        ycalc = 1.5
                else:
                    if ycalc < 8:
                        ycalc *= 1.06
                    else:
                        ycalc *= 1.01
                    player.y += ycalc

                coin.gen(coin)
                if coin.showing == True: 
                    display.blit(coinimg, (coin.x, coin.y))

                display.blit(text, (300, 20))
                display.blit(text7, (300, 360))
                if hi == True:
                    if hiballs >= 1:
                        display.blit(text8, (110, 175))
                        hiballs -= 1
                    else:
                        hiballs = 0
                if speedingup == True:
                    display.blit(text6, (125, 175))

                player.update()
                player.check_bounce()
                player.check_collision()
                blitting = len(rrand)
                while blitting > 0:
                    blitting -= 1
                    rrander = rrand[blitting]
                    display.blit(spike_right, (704, rrander))
                blitting = len(lrand)
                while blitting > 0:
                    blitting -= 1
                    lrander = lrand[blitting]
                    display.blit(spike_left, (0, lrander))
                display.blit(spike_down_long, (0, 382))

                display.blit(spike_up_long, (0, 0))
                gui.display.update()
            if loop == "over":
                totalcoins += coin.amount
                encrypt_and_save_integer(totalcoins, b'tooyo', 'encrypt/1.bin')
                gui.mixer.Sound.play(death)
                gui.mixer.music.pause()
            while loop == "over":
                for event in gui.event.get():
                    if event.type == QUIT:  # Exit the game on close
                        loop = "False"
                        gui.quit()
                        sys.exit()

                    if event.type == gui.KEYDOWN:
                        loop = "False"

                    if event.type == gui.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            loop = "False"
                clock.tick(60)
                display.blit(gameover, (25, 75))
                display.blit(gameover1, (25, 200))
                gui.display.update()