import cocos
from cocos import menu
from cocos.actions.tiledgrid_actions import TurnOffTiles
from cocos.menu import *
import numpy as np
import cocos.euclid as eu
import cocos.collision_model as cm
import cocos.layer 
import cocos.sprite
from collections import defaultdict
from pyglet.clock import schedule
from pyglet.window import key
import pyglet.image
from pyglet.image import Animation
import pygame
import random
import cocos.actions as ac
import time

pygame.init()
start_bgm = pygame.mixer.Sound("assets/bgm.mp3")
grass_sound = pygame.mixer.Sound("assets/grass.mp3")
gun_sound=pygame.mixer.Sound("assets/k2.mp3")
trumble_sound = pygame.mixer.Sound("assets/trumblesound.mp3")
crouch_sound = pygame.mixer.Sound("assets/crouch.mp3")
die_sound = pygame.mixer.Sound("assets/die.mp3")
minefinder_sound=pygame.mixer.Sound("assets/신호음.mp3")
rocket_sound=pygame.mixer.Sound("assets/rocket.mp3")
grenadepin_sound = pygame.mixer.Sound("assets/핀.mp3")
grenade_sound=pygame.mixer.Sound("assets/grenade.mp3")
cannon_sound=pygame.mixer.Sound("assets/cannon.mp3")
explosion_sound=pygame.mixer.Sound("assets/explosion.mp3")
cannon2_sound=pygame.mixer.Sound("assets/cannon2.mp3")
mine_sound=pygame.mixer.Sound("assets/mine.mp3")
helicopter_sound=pygame.mixer.Sound("assets/helicopter.mp3")
clear_sound=pygame.mixer.Sound("assets/clear.mp3")
loud_sound=pygame.mixer.Sound("assets/기상나팔.mp3")

rightraw = pyglet.image.load('assets/rightrun.png')
rightseq = pyglet.image.ImageGrid(rightraw, 1, 9 )
rightrun = Animation.from_image_sequence(rightseq, 0.09, True)

leftraw = pyglet.image.load('assets/leftrun.png')
leftseq = pyglet.image.ImageGrid(leftraw, 1, 9 )
leftrun = Animation.from_image_sequence(leftseq, 0.09, True)

tumblerightraw = pyglet.image.load('assets/righttumble.png')
tumblerightseq = pyglet.image.ImageGrid(tumblerightraw, 1, 9 )
righttumble = Animation.from_image_sequence(tumblerightseq, 0.04, False)

tumbleleftraw = pyglet.image.load('assets/lefttumble.png')
tumbleleftseq = pyglet.image.ImageGrid(tumbleleftraw, 1, 9 )
lefttumble = Animation.from_image_sequence(tumbleleftseq, 0.04, False)

fireraw = pyglet.image.load('assets/fire.png')
fireseq = pyglet.image.ImageGrid(fireraw, 1, 35 )
fire = Animation.from_image_sequence(fireseq, 0.04, False)

bigfireraw = pyglet.image.load('assets/대폭발.png')
bigfireseq = pyglet.image.ImageGrid(bigfireraw, 1, 16 )
bigfire = Animation.from_image_sequence(bigfireseq, 0.04, False)

explosionraw = pyglet.image.load('assets/explosion.png')
explosionseq = pyglet.image.ImageGrid(explosionraw, 1, 24 )
explosion = Animation.from_image_sequence(explosionseq, 0.12, False)

class HUD(cocos.layer.Layer):
    def __init__(self):
        super(HUD, self).__init__()
        self.time_text = cocos.text.Label('', font_size=30, color=(255, 255, 255, 255))
        self.time_text.position = (350, 750)
        self.add(self.time_text)

    def update_time(self, minute, second):
        self.time_text.element.text = '%s : %s' % (minute, second)

    def show_game_clear(self, score, time, clear, enemys, moves, difficulty):
        self.remove(self.time_text)        
        self.score_text= cocos.text.Label('', font_size = 80, color=(0, 0, 0, 255), position= (270, 450))
        self.score_text.element.text= ('%s' % score)
        self.times_text= cocos.text.Label('', font_size = 20, color=(0, 0, 0, 255), position= (500, 345))
        self.times_text.element.text= ('+%s' % time)
        self.clear_text= cocos.text.Label('', font_size = 20, color=(0, 0, 0, 255), position= (500, 385))
        self.clear_text.element.text= ('+%s' % clear)
        self.enemys_text= cocos.text.Label('', font_size = 20, color=(0, 0, 0, 255), position= (500, 300))
        self.enemys_text.element.text= ('+%s' % enemys)
        self.moves_text= cocos.text.Label('', font_size = 20, color=(0, 0, 0, 255), position= (500, 260),)
        self.moves_text.element.text= ('+%s' % moves)
        self.difficulty_text= cocos.text.Label('', font_size = 20, color=(0, 0, 0, 255), position= (500, 220),)
        self.difficulty_text.element.text= ('x%s' % difficulty)
        self.add(self.times_text)
        self.add(self.score_text)
        self.add(self.clear_text)
        self.add(self.enemys_text)
        self.add(self.moves_text)
        self.add(self.difficulty_text)

    def show_game_over(self, score, clear, enemys, moves, difficulty):
        self.remove(self.time_text)
        self.score_text= cocos.text.Label('', font_size = 80, color=(0, 0, 0, 255), position= (270, 450))
        self.score_text.element.text= ('%s' % score)
        self.clear_text= cocos.text.Label('', font_size = 20, color=(0, 0, 0, 255), position= (500, 345))
        self.clear_text.element.text= ('+%s' % clear)
        self.enemys_text= cocos.text.Label('', font_size = 20, color=(0, 0, 0, 255), position= (500, 300))
        self.enemys_text.element.text= ('+%s' % enemys)
        self.moves_text= cocos.text.Label('', font_size = 20, color=(0, 0, 0, 255), position= (500, 260),)
        self.moves_text.element.text= ('+%s' % moves)
        self.difficulty_text= cocos.text.Label('', font_size = 20, color=(0, 0, 0, 255), position= (500, 220),)
        self.difficulty_text.element.text= ('x%s' % difficulty)
        self.add(self.score_text)
        self.add(self.clear_text)
        self.add(self.enemys_text)
        self.add(self.moves_text)
        self.add(self.difficulty_text)

    def show_statistics(self, level, missiles, grenades, bombs, fogs, moves, trumbles, iswin ):
        if iswin==0:
            self.remove(self.times_text)
        
        self.statistics_difficulty_text= cocos.text.Label('', font_size = 40, color=(255, 255, 255, 255), position= (600, 730))
        self.statistics_difficulty_text.element.text= ('%s' % level)
        
        self.statistics_missiles_text= cocos.text.Label('', font_size = 40, color=(255, 255, 255, 255), position= (650, 620))
        self.statistics_missiles_text.element.text= ('%s' % missiles)
        self.statistics_grenades_text= cocos.text.Label('', font_size = 40, color=(255, 255, 255, 255), position= (650, 520))
        self.statistics_grenades_text.element.text= '%s' % grenades
        self.statistics_bombs_text= cocos.text.Label('', font_size = 40, color=(255, 255, 255, 255), position= (650, 420))
        self.statistics_bombs_text.element.text= '%s' % bombs
        self.statistics_fogs_text= cocos.text.Label('', font_size = 40, color=(255, 255, 255, 255), position= (650, 320))
        self.statistics_fogs_text.element.text= '%s' % fogs
        self.statistics_moves_text= cocos.text.Label('', font_size = 40, color=(255, 255, 255, 255), position= (600, 200))
        self.statistics_moves_text.element.text= ('%sm' % moves)
        self.statistics_trumbles_text= cocos.text.Label('', font_size = 40, color=(255, 255, 255, 255), position= (650, 100))
        self.statistics_trumbles_text.element.text= '%s' % trumbles
        self.remove(self.score_text)
        self.remove(self.clear_text)
        self.remove(self.enemys_text)
        self.remove(self.moves_text)
        self.remove(self.difficulty_text)
        self.add(self.statistics_difficulty_text)
        self.add(self.statistics_missiles_text)
        self.add(self.statistics_grenades_text)
        self.add(self.statistics_bombs_text)
        self.add(self.statistics_fogs_text)
        self.add(self.statistics_moves_text)
        self.add(self.statistics_trumbles_text)

class Actor(cocos.sprite.Sprite):
    def __init__(self, x, y, image):
        super(Actor, self).__init__(image)
        self.position = eu.Vector2(x, y)

class Player(Actor):
    KEYS_PRESSED = defaultdict(int)
    def __init__(self):
        Actor.__init__(self,400,400, "assets/playercm.png")  # 플레이어 생성
        self.isCrouch=False
        self.isRight=True
        self.seewhere = 4 #위1 왼쪽2 아래3 오른쪽4
        self.see_layer = cocos.sprite.Sprite('assets/seeright.png', position = (390, 400))
        self.player_layer = cocos.sprite.Sprite('assets/rightstand.png', position = (415, 430))
        self.cshape = cm.AARectShape(eu.Vector2(400, 400), 25, 25)
        self.cancrouchstand=True #앉고일어나기 가능?
        self.canseechange=True #시야전환 가능?
        self.movewhere = 0 #움직이고있냐~ 위1 왼쪽2 아래3 오른쪽4 안 움직임0
        

        self.movechange =False #움직임에 변화가 있었냐?

        self.isFire=False
        self.firetime=0

        self.istrumble = False
        self.trumbletime=0

        self.akeyreleased=True
        self.skeyreleased=True
        self.dkeyreleased=True
        self.wkeyreleased=True

        self.Minefind=False
        self.canpresstab=True

        self.wherefog =0
        self.fogsprite = cocos.sprite.Sprite('assets/downspeaker.png', position=(400,400))
        self.fogonce=True
        self.fogs=0


        
    def update(self, dt):
        pressed = Player.KEYS_PRESSED
        
        f_pressed = pressed[key.F] ==1
        w_pressed = pressed[key.W] == 1
        a_pressed = pressed[key.A] == 1
        s_pressed = pressed[key.S] == 1
        d_pressed = pressed[key.D] == 1
        up_pressed = pressed[key.UP] == 1
        down_pressed = pressed[key.DOWN] == 1
        left_pressed = pressed[key.LEFT] == 1
        right_pressed = pressed[key.RIGHT] == 1
        e_pressed = pressed[key.E]==1
        space_pressed = pressed[key.SPACE]==1
        tab_pressed = pressed[key.TAB]==1

        #tab키
        if self.canpresstab ==False and tab_pressed ==False and self.isFire==False and self.istrumble==False:
            self.canpresstab=True
        if self.canpresstab and tab_pressed:
            self.canpresstab=False
            if self.Minefind:
                self.Minefind=False
                self.parent.remove(self.mindfinder_layer)
            else:
                self.Minefind = True
                if self.seewhere==1:
                    self.mindfinder_layer = cocos.sprite.Sprite('assets/mineup.png', position = (400, 400))
                elif self.seewhere == 2:
                    self.mindfinder_layer = cocos.sprite.Sprite('assets/mineleft.png', position = (400, 400))
                elif self.seewhere == 3: 
                    self.mindfinder_layer = cocos.sprite.Sprite('assets/minedown.png', position = (400, 400))
                elif self.seewhere == 4: 
                    self.mindfinder_layer = cocos.sprite.Sprite('assets/mineright.png', position = (400, 400))

                self.parent.add(self.mindfinder_layer, z=2)


        if up_pressed == False and down_pressed == False and left_pressed == False and right_pressed == False and self.isFire==False and self.istrumble==False : #시야전환가능한지확인
            self.canseechange=True

        if self.canseechange: #시야전환
            if self.seewhere!=1 and up_pressed: # 위 방향키 누르면 
                self.seewhere = 1
                self.parent.remove(self.see_layer)
                self.see_layer = cocos.sprite.Sprite('assets/seeup.png', position = (400, 380))
                self.parent.add(self.see_layer, z=6)
                self.canseechange=False
                if self.Minefind:
                    self.parent.remove(self.mindfinder_layer)
                    self.mindfinder_layer = cocos.sprite.Sprite('assets/mineup.png', position = (400, 400))
                    self.parent.add(self.mindfinder_layer, z=2)
            elif self.seewhere!=2 and left_pressed :
                self.seewhere = 2   
                self.parent.remove(self.see_layer)
                self.see_layer = cocos.sprite.Sprite('assets/seeleft.png', position = (415, 400))
                self.parent.add(self.see_layer, z=6)
                self.canseechange=False
                if self.Minefind:
                    self.parent.remove(self.mindfinder_layer)
                    self.mindfinder_layer = cocos.sprite.Sprite('assets/mineleft.png', position = (400, 400))
                    self.parent.add(self.mindfinder_layer, z=2)
            elif self.seewhere!=3 and down_pressed :
                self.seewhere = 3
                self.parent.remove(self.see_layer)
                self.see_layer = cocos.sprite.Sprite('assets/seedown.png', position = (400, 420))
                self.parent.add(self.see_layer, z=6)
                if self.Minefind:
                    self.parent.remove(self.mindfinder_layer)
                    self.mindfinder_layer = cocos.sprite.Sprite('assets/minedown.png', position = (400, 400))
                    self.parent.add(self.mindfinder_layer, z=2)
                self.canseechange=False
            elif self.seewhere!=4 and right_pressed :
                self.seewhere = 4
                self.parent.remove(self.see_layer)
                self.see_layer = cocos.sprite.Sprite('assets/seeright.png', position = (390, 400))
                self.parent.add(self.see_layer, z=6)
                self.canseechange=False
                if self.Minefind:
                    self.parent.remove(self.mindfinder_layer)
                    self.mindfinder_layer = cocos.sprite.Sprite('assets/mineright.png', position = (400, 400))
                    self.parent.add(self.mindfinder_layer, z=2)

        if self.istrumble:
            if(self.trumbletime >50):
                self.istrumble = False
                
                self.trumbletime=0
                if w_pressed: 
                    self.movewhere = 1
                    self.isCrouch=False
                    self.movechange=True
                    self.wkeyreleased = False
                elif a_pressed :
                    self.movewhere = 2
                    self.isCrouch=False
                    self.isRight=False
                    self.movechange=True
                    self.akeyreleased = False
                elif s_pressed : 
                    self.movewhere = 3
                    self.isCrouch=False
                    self.movechange=True
                    self.skeyreleased = False
                elif d_pressed :
                    self.movewhere = 4
                    self.isCrouch=False
                    self.isRight=True
                    self.movechange=True
                    self.dkeyreleased = False
            else:
                self.trumbletime+=dt*100
        
        if self.isFire:

            if(self.firetime >200):
                self.firetime = 0
                self.isFire = False
                
                self.parent.remove(self.fire_layer)
                self.fogonce=True
                if w_pressed: 
                    self.movewhere = 1
                    self.isCrouch=False
                    self.movechange=True
                    self.wkeyreleased = False
                elif a_pressed :
                    self.movewhere = 2
                    self.isCrouch=False
                    self.isRight=False
                    self.movechange=True
                    self.akeyreleased = False
                elif s_pressed : 
                    self.movewhere = 3
                    self.isCrouch=False
                    self.movechange=True
                    self.skeyreleased = False
                elif d_pressed :
                    self.movewhere = 4
                    self.isCrouch=False
                    self.isRight=True
                    self.movechange=True
                    self.dkeyreleased = False

            elif self.firetime>100 and self.fogonce:
                if self.wherefog!=0:
                    if self.wherefog==self.seewhere:
                        self.wherefog=0
                        loud_sound.stop()
                        self.parent.remove(self.fogsprite)
                        self.fogs+=1
                        
                self.firetime+=dt*100
                self.fogonce = False
            else:
                self.firetime+=dt*100

        
        if self.trumbletime==0  and self.firetime ==0:

            if f_pressed:
                self.isFire=True
                self.movechange = True
                self.movewhere = 0
                self.isCrouch=False
                self.canseechange=False
                self.canpresstab = False
                return

            if w_pressed ==False:
                self.wkeyreleased=True
                if(self.movewhere==1):
                    self.movewhere=0
                    self.movechange=True
            if s_pressed==False:
                self.skeyreleased=True
                if(self.movewhere==3):
                    self.movewhere=0
                    self.movechange=True
            if a_pressed ==False:
                self.akeyreleased = True
                if(self.movewhere==2):
                    self.movewhere=0
                    self.movechange=True
            if d_pressed ==False:
                self.dkeyreleased=True
                if(self.movewhere==4):
                    self.movewhere=0
                    self.movechange=True

            if e_pressed == False:
                self.cancrouchstand=True


            if self.movewhere!=1 and self.wkeyreleased and w_pressed: #지금 위쪽으로 안 움직이고 있고 위 방향키가 떼졌다가 눌린거라면
                self.movewhere = 1
                self.isCrouch=False
                self.movechange=True
                self.wkeyreleased = False
            elif self.movewhere!=2 and self.akeyreleased and a_pressed :
                self.movewhere = 2
                self.isCrouch=False
                self.isRight=False
                self.movechange=True
                self.akeyreleased = False
            elif self.movewhere!=3 and self.skeyreleased and s_pressed : 
                self.movewhere = 3
                self.isCrouch=False
                self.movechange=True
                self.skeyreleased = False
            elif self.movewhere!=4 and self.dkeyreleased and d_pressed :
                self.movewhere = 4
                self.isCrouch=False
                self.isRight=True
                self.movechange=True
                self.dkeyreleased = False

            if self.cancrouchstand:
                if self.isCrouch == False and e_pressed:
                    self.isCrouch = True
                    self.cancrouchstand=False
                    self.movewhere=0
                    self.movechange=True
                    
                elif self.isCrouch== True and e_pressed:
                    self.isCrouch = False
                    self.cancrouchstand=False
                    self.movewhere=0
                    self.movechange=True
            
            if space_pressed and self.movewhere!=0 and self.istrumble==False:
                self.movechange=True
                self.istrumble=True
                self.isCrouch=False
                self.canseechange=False
                self.canpresstab=False        

class GameLayer(cocos.layer.Layer):
    is_event_handler = True

    
    def on_key_press(self, k, _):  #어떤 키가 눌렸는지 확인하는 거
        Player.KEYS_PRESSED[k] = 1 

    def on_key_release(self, k, _): # 어떤 키가 떼졌는지 확인.
        Player.KEYS_PRESSED[k] = 0

    def __init__(self, difficulty, hud_layer):
        super(GameLayer, self).__init__()
        self.difficulty = difficulty # 0,1,2
        self.background_layer = cocos.sprite.Sprite('assets/green.png', position = (400, 400), anchor=(2400 ,2400))
        self.isGrassSound=False
        self.grasstime=0

        self.isMineSound=False
        self.minesoundtime=0
        self.minesoundterm=0

        self.diecode=0
        self.justonce=False
        self.staticonce=False

        self.trumbles=0


        self.player = Player() # 플레이어 객체 선언
        self.add(self.background_layer, z=0)
        self.add(self.player, z=1) #layer에 플레이어 추가.
        self.add(self.player.see_layer, z=6)
        self.add(self.player.player_layer, z=3)
        self.difficulty_settings()
        self.make_end_spot() #0~3
        self.make_mine()
        self.mapMovX=0
        self.mapMovY=0
        self.fogwaittime=0

        self.Enemy=0
        self.enemywaittime=0
        #self.EnemyTerm은 다시 enemy가 나오기 까지의 최소 시간
        self.enemyTime=0
        self.enemymovX=0
        self.enemymovY=0
        self.hud = hud_layer
        self.minute=0
        self.second=0

        self.missiles=0
        self.grenades=0
        self.bombs=0
        self.moves=0
        

        self.schedule( self.update)
    
    def make_end_spot(self):
        self.endpoint =random.randint(0,3) #왼쪽위 부터 시계방향 
        print(self.endpoint)

        if self.endpoint ==0:
            self.helix=-1400
            self.heliy= 2300
        elif self.endpoint==1:
            self.helix=2300
            self.heliy = 2300
        elif self.endpoint ==2:
            self.helix = 2300
            self.heliy = -1400
        else:
            self.helix = -1400
            self.heliy = -1400
        self.helicopter=cocos.sprite.Sprite('assets/helicopter.png', position =(self.helix, self.heliy))
        self.add(self.helicopter, z=3)

    def make_mine(self):
        self.minemap = [[-1 for y in range(20)] for x in range(20)] # 가로x세로 40x 40 범위해서 지뢰심어야지~
        for y in range(20):  
            for x in range(20):
                # 도착지점이랑, 시작지점은 지뢰 없어야 됨.
                #
                nexttime =False
                for yy in range (-1,2): #지뢰 띄엄띄엄 설치하게
                    if y+yy >=20 or y+yy<0:
                        continue
                    if nexttime:
                        break
                    for xx in range (-1, 2):
                        if x+xx >=20 or x+xx<0:
                            continue
                        if self.minemap[x+xx][y+yy]==1:
                            nexttime = True
                            break
                if nexttime==False:
                    rand = random.randint(0, 9)
                    if rand >=self.randommine:
                        self.minemap[x][y] = 1 
        #출발지점 지뢰 제거
        self.minemap[9][9]=-1
        self.minemap[9][10]=-1
        self.minemap[10][9] =-1
        self.minemap[10][10] = -1
        
        #최종지역 지뢰 제거 및 승리 표시(2번)
        if self.endpoint==0: 
            self.minemap[0][19] = 2
        elif self.endpoint ==1: 
            self.minemap[19][19] = 2
        elif self.endpoint == 2 : 
            self.minemap[19][0] = 2
        elif self.endpoint ==3 : 
            self.minemap[0][0] = 2

    def find_mine(self):
        if self.player.Minefind: # 지뢰탐지기가 켜져 있다면
            x = (self.mapMovX+2000) #현재위치
            y = self.mapMovY+2000 #현재위치
            if self.player.seewhere== 1:#위쪽 보고있다면
                for i in range(1,6):#5번
                    offset=i*50
                    xxx=int(x) //200
                    if y+offset>=4000 : #범위 벗어나면 그냥 넘겨
                        yyy=3990 //200
                    else:
                        yyy = int(y+offset) // 200
                    if self.minemap[xxx][yyy]==1:#지뢰 있으면
                        self.minesoundterm = i/4
                        return True
            elif self.player.seewhere== 3:#아래쪽 보고있다면
                for i in range(1,6):#5번
                    offset=i*(-50)
                    xxx=int(x) //200
                    if y+offset <=0 :
                        yyy=0
                    else:
                        yyy = int(y+offset) // 200
                    if self.minemap[xxx][yyy]==1:#지뢰 있으면
                        self.minesoundterm = i/4
                        return True
            
            elif self.player.seewhere== 2:#왼쪽 보고있다면
                for i in range(1,6):#5번
                    offset=i*(-50)
                    if x+offset <=0 :
                        xxx=0
                    else:
                        xxx=int(x+offset) //200
                    yyy = int(y) // 200
                    if self.minemap[xxx][yyy]==1:#지뢰 있으면
                        self.minesoundterm = i/4
                        return True
            elif self.player.seewhere== 4:#왼쪽 보고있다면
                for i in range(1,6):#5번
                    offset=i*(50)
                    if x+offset >=4000 :
                        xxx=3990//200
                    else:
                        xxx=int(x+offset) //200
                    yyy = int(y) // 200
                    if self.minemap[xxx][yyy]==1:#지뢰 있으면
                        self.minesoundterm = i/4
                        return True
            return False
        else:
            return False

    def is_on_mine(self): #지뢰면은 죽고 목적지라면 승리!
        xx = int((self.mapMovX+2000) //200)
        yy = int((self.mapMovY+2000) //200)
        if(self.minemap[xx][yy]==1):
            self.diecode=1
            self.game_over()
        elif self.minemap[xx][yy]==2:
            self.game_clear()

    def difficulty_settings(self):
        if self.difficulty ==0: #easy
            self.randommine = 7
            self.EnemyTerm = 8
            self.maxtime=10
        
        elif self.difficulty == 1 :#noraml
            self.randommine = 5
            self.EnemyTerm = 4
            self.maxtime= 5

        else: # hard
            self.randommine = 3
            self.EnemyTerm = 1
            self.maxtime= 3

    def time(self, time):
        if self.second>60:
            self.second = 0
            self.minute+=1
        else:
            self.second+=time
        if self.minute==self.maxtime:
            self.diecode = 2
            self.game_over()
    
    def update(self, dt):
        self.time(dt)
        self.hud.update_time(self.maxtime-self.minute-1,59-int(self.second))

        

        self.player.update(dt)
        if(self.player.movechange):
            self.remove(self.player.player_layer)
            self.changePlayerMothion(self.player)
            self.add(self.player.player_layer, z=3)
            self.player.movechange=False

        if(self.player.istrumble==False):
            self.moveMap(self.player.movewhere, dt)
            self.grassSound(dt)
        else:
            if(self.player.trumbletime<30):
                self.trumblemoveMap(self.player.movewhere, dt)
        if self.find_mine():
            self.mindFinderSound(dt)
        
        self.spawn_enemy_waiting(dt)
        self.spawn_fog_waiting(dt)
        if self.Enemy!=0:
            if self.Enemy==1:
                self.missile_control(dt)
            elif self.Enemy==2:
                self.grenade_control(dt)
            elif self.Enemy==3:
                self.cannon_control(dt)
        

    def changePlayerMothion(self, player):
        if player.isFire:
                if player.seewhere ==1:
                    player.player_layer = cocos.sprite.Sprite("assets/upshoot.png", position = (400, 430))
                    player.fire_layer = cocos.sprite.Sprite(fire, position = (395, 494))
                    
                elif player.seewhere ==2:
                    player.player_layer = cocos.sprite.Sprite("assets/leftcrouch.png", position = (381, 430))
                    player.fire_layer = cocos.sprite.Sprite(fire, position = (327, 455))
                elif player.seewhere ==3:
                    player.player_layer = cocos.sprite.Sprite("assets/downshoot.png", position = (400, 430))
                    player.fire_layer = cocos.sprite.Sprite(fire, position = (430, 385))
                elif player.seewhere ==4:
                    player.player_layer = cocos.sprite.Sprite("assets/rightcrouch.png", position = (412, 430))
                    player.fire_layer = cocos.sprite.Sprite(fire, position = (465, 455))
                gun_sound.play()
                
                self.add(player.fire_layer, z=3)
        else:        
            if player.isRight:
                if player.istrumble : # 구르기 눌렀다면
                    self.trumbles+=1
                    player.player_layer = cocos.sprite.Sprite(righttumble, position = (400, 430))
                    trumble_sound.play()

                elif player.isCrouch:
                    player.player_layer = cocos.sprite.Sprite('assets/rightliedown.png', position = (400, 400))
                    crouch_sound.play()

                elif player.movewhere!=0:
                    player.player_layer = cocos.sprite.Sprite(rightrun, position = (415, 430))
        
                else: #앉아잇지도않고 움직이지도않는데 오른쪽이야 그럼 서있는거지
                    player.player_layer = cocos.sprite.Sprite('assets/rightstand.png', position = (415, 430))
            elif player.isRight==False:
                if player.istrumble : # 구르기 눌렀다면
                    self.trumbles+=1
                    player.player_layer = cocos.sprite.Sprite(lefttumble, position = (365, 430))
                    trumble_sound.play()
                elif player.isCrouch:
                    player.player_layer = cocos.sprite.Sprite('assets/leftliedown.png', position = (385, 400))
                    crouch_sound.play()
                elif player.movewhere!=0:
                    player.player_layer = cocos.sprite.Sprite(leftrun, position = (385, 430))

                else: #앉아잇지도않고 움직이지도않는데 왼쪽이야 그럼 서있는거지
                    player.player_layer = cocos.sprite.Sprite('assets/leftstand.png', position = (380, 430))
        
    def moveMap(self, move, time):
        if move==0:
            return
        tempmapmovx=self.mapMovX
        tempmapmovy=self.mapMovY
        if abs(self.mapMovX)>=1950 :
            if self.mapMovX <0:
                self.mapMovX = -1949
            else:
                self.mapMovX = 1949
        elif abs(self.mapMovY)>=1950:
            if self.mapMovY <0:
                self.mapMovY = -1949
            else:
                self.mapMovY = 1949
        elif move ==1:
            self.mapMovY+=(time*150)
        elif move ==2:
            self.mapMovX -=(time*150)
        elif move ==3:
            self.mapMovY -=(time*150)
        elif move == 4:
            self.mapMovX +=(time*150)
        self.enemymovX-=(tempmapmovx-self.mapMovX)
        self.enemymovY -= (tempmapmovy-self.mapMovY)
        self.moves+= (abs(tempmapmovx-self.mapMovX) + abs(tempmapmovy-self.mapMovY))
        self.remove(self.background_layer)
        self.background_layer = cocos.sprite.Sprite('assets/green.png', position = (400, 400), anchor=(2400+self.mapMovX ,2400 + self.mapMovY))

        self.add(self.background_layer, z=0)
        self.remove(self.helicopter)
        self.helicopter=cocos.sprite.Sprite('assets/helicopter.png', position = (self.helix-self.mapMovX, self.heliy-self.mapMovY))
        self.add(self.helicopter, z=3)

        self.is_on_mine()
        self.find_mine()
 
    def trumblemoveMap(self, move, time):
        tempmapmovx=self.mapMovX
        tempmapmovy=self.mapMovY
        if abs(self.mapMovX)>=1950 :
            if self.mapMovX <0:
                self.mapMovX = -1949
            else:
                self.mapMovX = 1949
        elif abs(self.mapMovY)>=1950:
            if self.mapMovY <0:
                self.mapMovY = -1949
            else:
                self.mapMovY = 1949
        elif move ==1 :
            self.mapMovY+=(time*600)
        elif move ==2:
            self.mapMovX-=(time*600)
        elif move ==3:
            self.mapMovY-=(time*600)
        elif move == 4:
            self.mapMovX+=(time*600)
        self.enemymovX-=(tempmapmovx-self.mapMovX)
        self.enemymovY -= (tempmapmovy-self.mapMovY)
        self.moves+= (abs(tempmapmovx-self.mapMovX) + abs(tempmapmovy-self.mapMovY))
        self.remove(self.background_layer)
        self.background_layer = cocos.sprite.Sprite('assets/green.png', position = (400, 400), anchor=(2400+self.mapMovX ,2400 + self.mapMovY))
        self.add(self.background_layer, z=0)
        self.remove(self.helicopter)
        self.helicopter=cocos.sprite.Sprite('assets/helicopter.png', position = (self.helix-self.mapMovX, self.heliy-self.mapMovY))
        self.add(self.helicopter, z=3)
        self.is_on_mine()
        self.find_mine()
            
    def grassSound(self, time):
        if self.isGrassSound:
            if(self.grasstime > 1):
                self.isGrassSound=False
                self.grasstime =0
            else:
                self.grasstime+=time*2.5
        elif(self.player.movewhere!=0 and self.isGrassSound==False):
            grass_sound.play()
            self.isGrassSound=True

    def mindFinderSound(self, time):
        if self.isMineSound:
            if(self.minesoundtime > self.minesoundterm):
                self.isMineSound=False
                self.minesoundtime = 0
            else:
                self.minesoundtime+=time*2.5
        else:
            minefinder_sound.play()
            self.isMineSound=True

    def spawn_enemy_waiting(self, time):
        if self.Enemy!=0:
            return
        else:
            if self.enemywaittime>=self.EnemyTerm:
                self.enemywaittime=0
                rand = random.randint(0,10)
                if rand <6:
                    self.spawn_enemy()
                
            else:
                pass
                self.enemywaittime+=time
    
    def spawn_fog_waiting(self,time):
        if self.player.wherefog!=0:
            return
        else:
            if self.fogwaittime>=self.EnemyTerm+0.7:
                self.fogwaittime=0
                rand = random.randint(0,10)
                if rand<4:
                    self.spawn_fog()
            else:
                pass
                self.fogwaittime+=time

    def spawn_enemy(self):
        self.enemymovX=0
        self.enemymovY=0
        self.Enemy = random.randint(1,3)
        
    
        if self.Enemy ==1: #1번이 미사일
            rocket_sound.play()
            self.missilenum = random.randint(1,12) #시계방향, 1 위쪽, 4 오른쪽 이렇게
            self.missilesprite = cocos.sprite.Sprite('assets/downmissile.png', position = (-100, -100))
            self.add(self.missilesprite)
        elif self.Enemy==2: #수류탄
            self.grenadeonce = True
            grenadepin_sound.play()

        elif self.Enemy==3 : #곡사포
            cannon_sound.play()
            cannon2_sound.play()
            self.cannonspotsprite = cocos.sprite.Sprite('assets/playercm.png', position = (400,400))
            self.add(self.cannonspotsprite)
            self.grenadeonce = True

    def spawn_fog(self):
        self.player.wherefog = random.randint(1,4)#1은 위, 반시계방향
        if self.player.wherefog ==1:
            self.player.fogsprite = cocos.sprite.Sprite('assets/upspeaker.png', position= (400, 770))
        elif self.player.wherefog ==2:
            self.player.fogsprite = cocos.sprite.Sprite('assets/leftspeaker.png', position= (30, 430))
        elif self.player.wherefog ==3:
            self.player.fogsprite = cocos.sprite.Sprite('assets/downspeaker.png', position= (430, 30))
        elif self.player.wherefog ==4:
            self.player.fogsprite = cocos.sprite.Sprite('assets/rightspeaker.png', position= (770, 400))
        self.add(self.player.fogsprite, z=2)
        loud_sound.play(-1)

    #만약 self.Enemy=해당숫자일경우에 update에서 call
    def missile_control(self, time) :
        if self.enemyTime >= 5: #미사일 스폰 된 후 일정 시간 지나면
            self.remove(self.missilesprite)
            self.Enemy = 0
            self.enemyTime=0
            self.missiles+=1
        else:
            self.enemyTime+=time
            self.remove(self.missilesprite)
            speed = 500
            if self.missilenum == 1:
                xx=300-self.enemymovX
                yy= 1600-(self.enemyTime)*speed-self.enemymovY
                self.missilesprite = cocos.sprite.Sprite('assets/downmissile.png', position = (xx,yy))
                self.add(self.missilesprite, z=2)
                if (xx>=350 and xx<=450) and (yy<=525 and yy>=350):
                    self.diecode = 3
                    self.game_over()
            elif self.missilenum ==2 :
                xx=400-self.enemymovX
                yy= 1600-(self.enemyTime)*speed-self.enemymovY
                self.missilesprite = cocos.sprite.Sprite('assets/downmissile.png', position = (xx,yy))
                self.add(self.missilesprite, z=2)
                if (xx>=350 and xx<=450) and (yy<=525 and yy>=350):
                    self.diecode = 3
                    self.game_over()
            elif self.missilenum ==3 :
                xx=500-self.enemymovX
                yy= 1600-(self.enemyTime)*speed-self.enemymovY
                self.missilesprite = cocos.sprite.Sprite('assets/downmissile.png', position = (xx,yy))
                self.add(self.missilesprite, z=2)
                if (xx>=350 and xx<=450) and (yy<=525 and yy>=350):
                    self.diecode = 3
                    self.game_over()
            elif self.missilenum ==4 : #오른쪽
                xx=1600-self.enemymovX-(self.enemyTime)*speed
                yy= 500-self.enemymovY
                self.missilesprite = cocos.sprite.Sprite('assets/leftmissile.png', position = (xx,yy))
                self.add(self.missilesprite, z=2)
                if (xx<=525 and xx>=350) and (yy>=350 and yy<=450):
                    self.diecode = 3
                    self.game_over()
            elif self.missilenum ==5 : #오른쪽
                xx=1600-self.enemymovX-(self.enemyTime)*speed
                yy= 400-self.enemymovY
                self.missilesprite = cocos.sprite.Sprite('assets/leftmissile.png', position = (xx,yy))
                self.add(self.missilesprite, z=2)
                if (xx<=525 and xx>=350) and (yy>=350 and yy<=450):
                    self.diecode = 3
                    self.game_over()
            elif self.missilenum ==6 : #오른쪽
                xx=1600-self.enemymovX-(self.enemyTime)*speed
                yy= 300-self.enemymovY
                self.missilesprite = cocos.sprite.Sprite('assets/leftmissile.png', position = (xx,yy))
                self.add(self.missilesprite, z=4)
                if (xx<=525 and xx>=350) and (yy>=350 and yy<=450):
                    self.diecode = 3
                    self.game_over()
            elif self.missilenum ==7: #아래쪽
                xx=500-self.enemymovX
                yy= -800 +(self.enemyTime)*speed-self.enemymovY
                self.missilesprite = cocos.sprite.Sprite('assets/upmissile.png', position = (xx,yy))
                self.add(self.missilesprite, z=4)
                if (xx>=350 and xx<=450) and (yy<=450 and yy>=275):
                    self.diecode = 3
                    self.game_over()
            elif self.missilenum ==8: #아래쪽
                xx=400-self.enemymovX
                yy= -800 +(self.enemyTime)*speed-self.enemymovY
                self.missilesprite = cocos.sprite.Sprite('assets/upmissile.png', position = (xx,yy))
                self.add(self.missilesprite, z=4)
                if (xx>=350 and xx<=450) and (yy<=450 and yy>=275):
                    self.diecode = 3
                    self.game_over()

            elif self.missilenum ==9: #아래쪽
                xx=300-self.enemymovX
                yy= -800 +(self.enemyTime)*speed-self.enemymovY
                self.missilesprite = cocos.sprite.Sprite('assets/upmissile.png', position = (xx,yy))
                self.add(self.missilesprite, z=4)
                if (xx>=350 and xx<=450) and (yy<=450 and yy>=275):
                    self.diecode = 3
                    self.game_over()

            elif self.missilenum ==10: #왼쪽
                xx=-800-self.enemymovX+(self.enemyTime)*speed
                yy= 300 -self.enemymovY
                self.missilesprite = cocos.sprite.Sprite('assets/rightmissile.png', position = (xx,yy))
                self.add(self.missilesprite, z=4)
                if (xx<=450 and xx>=275) and (yy>=350 and yy<=450):
                    self.diecode = 3
                    self.game_over()
            elif self.missilenum ==11: #왼쪽
                xx=-800-self.enemymovX+(self.enemyTime)*speed
                yy= 400 -self.enemymovY
                self.missilesprite = cocos.sprite.Sprite('assets/rightmissile.png', position = (xx,yy))
                self.add(self.missilesprite, z=2)
                if (xx<=450 and xx>=275) and (yy>=350 and yy<=450):
                    self.diecode = 3
                    self.game_over()
            elif self.missilenum ==12: #왼쪽
                xx=-800-self.enemymovX+(self.enemyTime)*speed
                yy= 500 -self.enemymovY
                self.missilesprite = cocos.sprite.Sprite('assets/rightmissile.png', position = (xx,yy))
                self.add(self.missilesprite, z=2)
                if (xx<=450 and xx>=275) and (yy>=350 and yy<=450):
                    self.diecode = 3
                    self.game_over()
            
    def grenade_control(self, time):

        if self.enemyTime >=3.5:
            self.remove(self.bigfireanim)
            self.Enemy = 0
            self.enemyTime=0
            self.grenades+=1
        
        elif self.enemyTime >= 3 and self.grenadeonce: #스폰 된 후 일정 시간 지나면
            self.grenadeonce=False
            self.bigfireanim= cocos.sprite.Sprite(bigfire, position = (400, 480))

            self.add(self.bigfireanim, z=4)
            
            grenade_sound.play()
            
            if self.player.isCrouch==False:
                self.diecode=4
                self.game_over()
        elif self.enemyTime>=3 :
            if self.player.isCrouch!=True:
                self.diecode=4
                self.game_over()
            self.enemyTime +=time
        else:
            self.enemyTime+=time
    
    def cannon_control(self,time):
        if self.enemyTime >=4:
            self.remove(self.explosion)
            self.Enemy = 0
            self.enemyTime=0
            self.bombs+=1
        
        elif self.enemyTime >= 3 and self.grenadeonce: #스폰 된 후 일정 시간 지나면
            self.remove(self.cannonspotsprite)
            self.grenadeonce=False
            self.explosion= cocos.sprite.Sprite(explosion, position = (400-self.enemymovX,900-self.enemymovY ))
            self.add(self.explosion, z=4)
            explosion_sound.play()
            
            if (abs(self.enemymovX)<350 and abs(self.enemymovY)<350) or self.player.isCrouch!=True:
                self.diecode=5
                self.game_over()
        elif self.enemyTime>=3 :
            if self.player.isCrouch!=True:
                self.diecode=6
                self.game_over()
            self.enemyTime +=time

        elif self.enemyTime>=1 and self.grenadeonce :
            self.enemyTime+=time
            self.remove(self.cannonspotsprite)
            self.cannonspotsprite = cocos.sprite.Sprite('assets/cannonspot.png', position = (400-self.enemymovX,400-self.enemymovY))
            self.add(self.cannonspotsprite, z=2)
        else:
            self.enemyTime +=time
               
    def game_over(self):
        self.unschedule(self.update)
        obstacle = (self.missiles+self.bombs+self.grenades)*300
        move = int(self.moves)//10
        
        score = ( move+obstacle)*(self.difficulty+1)
        loud_sound.stop()

        
        if self.diecode==1:
            mine_sound.play()
            time.sleep(1)
            grenade_sound.play()
            end=cocos.sprite.Sprite("assets/end1.png",position=(400,400))
            self.add(end, z=8)
        elif self.diecode==2:
            self.remove(self.helicopter)
            helicopter_sound.play()
            time.sleep(3)
            end = cocos.sprite.Sprite("assets/end2.png",position = (400, 400) )
            self.add(end, z=8)
        elif self.diecode==3:
            grenade_sound.play()
            end=cocos.sprite.Sprite("assets/end3.png",position = (400, 400))
            self.add(end, z=8)
        elif self.diecode ==4:
            die_sound.play()
            end=cocos.sprite.Sprite("assets/end4.png",position = (400, 400))
            self.add(end, z=8)
        elif self.diecode==5:
            end=cocos.sprite.Sprite("assets/end5.png",position = (400, 400))
            self.add(end, z=8)
        elif self.diecode ==6:
            die_sound.play()
            end=cocos.sprite.Sprite("assets/end6.png",position = (400, 400))
            self.add(end, z=8)

        self.hud.show_game_over(score, 0,obstacle, move, self.difficulty+1)
        
        schedule(self.retry_game)
           # start_bgm.play(-1)
            #cocos.director.director.pop()
    
    def retry_game(self, dt):
        pressed = Player.KEYS_PRESSED
        r_pressed = pressed[key.R]==1
        j_pressed = pressed[key.J]==1
        
        if r_pressed and self.justonce!=True:
            self.justonce=True
            helicopter_sound.stop()
            clear_sound.stop()
            start_bgm.play(-1)
            cocos.director.director.pop()
        if j_pressed and self.staticonce!=True:
            if self.difficulty==0:
                diff = 'Easy'
            elif self.difficulty==1:
                diff = 'Normal'
            else:
                diff ='Hard'
            
            self.hud.show_statistics(diff, self.missiles, self.grenades, self.bombs, self.player.fogs, int(self.moves)//30, self.trumbles, self.diecode)
            self.staticonce=True
            self.add(cocos.sprite.Sprite("assets/통계.png" ,position=(400, 400)), z=10)

    def game_clear(self):
        loud_sound.stop()
        clear_sound.play()
        helicopter_sound.play()
        self.unschedule(self.update)
        obstacle = (self.missiles+self.bombs+self.grenades)*300
        move = int(self.moves)//10
        times = ((self.maxtime-self.minute-1)*60 + 59-int(self.second))*10
        score = (5000+times+move+obstacle)*(self.difficulty+1)

        end=cocos.sprite.Sprite("assets/clear.png",position=(400,400))
        self.add(end, z=8)
        

        self.hud.show_game_clear(score,times, 5000,  obstacle, move, self.difficulty+1)
        
        schedule(self.retry_game)

class HowLayer(cocos.layer.Layer):
    KEYS_PRESSED = defaultdict(int)
    is_event_handler = True
    def on_key_press(self, k, _):  #어떤 키가 눌렸는지 확인하는 거
        HowLayer.KEYS_PRESSED[k] = 1 

    def on_key_release(self, k, _): # 어떤 키가 떼졌는지 확인.
        HowLayer.KEYS_PRESSED[k] = 0
    
    def __init__ (self):
        super(HowLayer, self).__init__()
        self.howindex=1
        self.leftonce=True
        self.rightonce=True
        self.ronce=True
        self.eonce = True
        self.schedule( self.update)
        self.add(cocos.sprite.Sprite("assets/1.png", position=(400, 400)), z=1)
        self.layer2 = cocos.sprite.Sprite("assets/2.png", position=(400, 400))
        self.layer3 = cocos.sprite.Sprite("assets/3.png", position=(400, 400))
        self.layer4 = cocos.sprite.Sprite("assets/4.png", position=(400, 400))
        self.layer5 = cocos.sprite.Sprite("assets/5.png", position=(400, 400))
        self.layer6 = cocos.sprite.Sprite("assets/6.png", position=(400, 400))

    def update(self, dt):
        pressed = HowLayer.KEYS_PRESSED
        
        left_pressed = pressed[key.LEFT] ==1
        right_pressed = pressed[key.RIGHT]==1
        r_pressed = pressed[key.R]==1
        e_pressed = pressed[key.E]==1

        if self.leftonce!=True and left_pressed!=True:
            self.leftonce=True
        if self.rightonce!=True and right_pressed!=True:
            self.rightonce=True
        if self.ronce!=True and r_pressed!=True:
            self.ronce=True
        if self.eonce!=True and e_pressed!=True:
            self.eonce=True
        
        if left_pressed and self.leftonce:
            self.leftonce=False
            if self.howindex==2:
                self.howindex-=1
                self.remove(self.layer2)
            elif self.howindex==3:
                self.howindex-=1
                self.remove(self.layer3)
            elif self.howindex==4:
                self.howindex-=1
                self.remove(self.layer4)
            elif self.howindex==5:
                self.howindex-=1
                self.remove(self.layer5)
            elif self.howindex==6:
                self.howindex-=1
                self.remove(self.layer6)
        
        if right_pressed and self.rightonce:
            self.rightonce=False
            if self.howindex==1:
                self.howindex+=1
                self.add(self.layer2, z=self.howindex)
            elif self.howindex==2:
                self.howindex+=1
                self.add(self.layer3, z= self.howindex)
            elif self.howindex==3:
                self.howindex+=1
                self.add(self.layer4, z= self.howindex)
            elif self.howindex==4:
                self.howindex+=1
                self.add(self.layer5, z= self.howindex)
            elif self.howindex==5:
                self.howindex+=1
                self.add(self.layer6, z= self.howindex)
        
        if r_pressed and self.ronce:
            start_bgm.play(-1)
            cocos.director.director.pop()

        if e_pressed and self.eonce:
            self.eonce=False
            if self.howindex==2:
                minefinder_sound.play()
            elif self.howindex==3:
                rocket_sound.play()
            elif self.howindex==4:
                grenadepin_sound.play()
            elif self.howindex==5:
                cannon_sound.play()
                cannon2_sound.play()

class MainMenu(Menu):
    
    def __init__(self):
        start_bgm.play(-1)
        color_layer = cocos.sprite.Sprite('assets/menu.png', position = (400, 400))
        scene.add(color_layer)
        super(MainMenu, self).__init__('')
        self.font_item['font_name'] = 'Times New Roman'
        self.font_item_selected['font_name'] = 'Times New Roman'

        self.selDifficulty = 0
        self.difficulty = ['Easy', 'Normal', 'Hard']
        
        a= 400
        b= 330

        menuposition =[[b,a],[b,a-50],[b,a-100],[b,a-150],[b,a-200]]

        items = list()
        items.append(MenuItem('New Game', self.start_game))
        items.append(MenuItem('How to Play', self.how_to_play))
        items.append(MultipleMenuItem('Difficuly: ', self.set_difficulty, self.difficulty, 0))
        items.append(ToggleMenuItem('Show FPS: ', self.show_fps, False))
        items.append(MenuItem('Quit', pyglet.app.exit))
        self.create_menu(items, selected_effect=None, unselected_effect=None,
                    activated_effect=None, layout_strategy=fixedPositionMenuLayout(menuposition))

    def start_game(self):
        loud_sound.stop()
        start_bgm.stop()

        
        scene = cocos.scene.Scene()
        
        hud_layer = HUD()
        scene.add(hud_layer, z=2)
        scene.add(GameLayer(self.selDifficulty, hud_layer), z=1)
        
        cocos.director.director.push(scene)
        Player.KEYS_PRESSED = defaultdict(int)

    def how_to_play(self):
        loud_sound.stop()
        start_bgm.stop()
        
        scene = cocos.scene.Scene()
        scene.add(HowLayer(), z=1)
        cocos.director.director.push(scene)
        HowLayer.KEYS_PRESSED=defaultdict(int)


        

        

    def set_difficulty(self, index):
        self.selDifficulty = index
        
    def show_fps(self, val):
        cocos.director.director.show_FPS = val

if __name__ == '__main__':
    cocos.director.director.init(caption='약진 앞으로!', width = 800, height = 800)

    scene = cocos.scene.Scene()
    scene.add(MainMenu())
    
    cocos.director.director.run(scene)
