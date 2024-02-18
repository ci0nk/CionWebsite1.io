"""
Subcontroller module for Alien Invaders

This module contains the subcontroller to manage a single level or wave in
the Alien Invaders game.  Instances of Wave represent a single wave. Whenever
you move to a new level, you are expected to make a new instance of the class.

The subcontroller Wave manages the ship, the aliens and any laser bolts on
screen. These are model objects.  Their classes are defined in models.py.

Most of your work on this assignment will be in either this module or
models.py. Whether a helper method belongs in this module or models.py is
often a complicated issue.  If you do not know, ask on Piazza and we will
answer.

Connie Zhang (cz467) and Cion Kim (ck758)
# DATE COMPLETED HERE
"""
from game2d import *
from consts import *
from models import *
import random

# PRIMARY RULE: Wave can only access attributes in models.py via getters/setters
# Wave is NOT allowed to access anything in app.py (Subcontrollers are not
# permitted to access anything in their parent. To see why, take CS 3152)


class Wave(object):
    """
    This class controls a single level or wave of Alien Invaders.

    This subcontroller has a reference to the ship, aliens, and any laser bolts
    on screen. It animates the laser bolts, removing any aliens as necessary.
    It also marches the aliens back and forth across the screen until they are
    all destroyed or they reach the defense line (at which point the player
    loses). When the wave is complete, you  should create a NEW instance of
    Wave (in Invaders) if you want to make a new wave of aliens.

    If you want to pause the game, tell this controller to draw, but do not
    update.  See subcontrollers.py from Lecture 24 for an example.  This
    class will be similar to than one in how it interacts with the main class
    Invaders.

    All of the attributes of this class ar to be hidden. You may find that
    you want to access an attribute in class Invaders. It is okay if you do,
    but you MAY NOT ACCESS THE ATTRIBUTES DIRECTLY. You must use a getter
    and/or setter for any attribute that you need to access in Invaders.
    Only add the getters and setters that you need for Invaders. You can keep
    everything else hidden.

    """
    # HIDDEN ATTRIBUTES:
    # Attribute _ship: the player ship to control
    # Invariant: _ship is a Ship object or None
    #
    # Attribute _aliens: the 2d list of aliens in the wave
    # Invariant: _aliens is a rectangular 2d list containing Alien objects or None
    #
    # Attribute _bolts: the laser bolts currently on screen
    # Invariant: _bolts is a list of Bolt objects, possibly empty
    #
    # Attribute _dline: the defensive line being protected
    # Invariant : _dline is a GPath object
    #
    # Attribute _lives: the number of lives left
    # Invariant: _lives is an int >= 0
    #
    # Attribute _time: the amount of time since the last Alien "step"
    # Invariant: _time is a float >= 0s
    #
    # new
    # Attribute _boltfirestep: the amount of time since the last bolt "step"
    # Invariant:
    # Attribute: _step
    #
    # You may change any attribute above, as long as you update the invariant
    # You may also add any new attributes as long as you document them.
    # LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    # Attribute _trackalien: tracks whether the aliens are moving right or left
    # Invariant: _trackalien is a bool

    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getAliens(self):
        return self._aliens

    # INITIALIZER (standard form) TO CREATE SHIP AND ALIENS
    def __init__(self):
        self.__initAlien__()

        self._ship = Ship(x=GAME_WIDTH/2,y=SHIP_BOTTOM+(SHIP_HEIGHT/2),width=SHIP_WIDTH,height=SHIP_HEIGHT,source='rocket.png')
        self._dline = GPath(points=[0,DEFENSE_LINE,GAME_WIDTH,DEFENSE_LINE],linewidth=1, linecolor='black')
        self._time = 0
        self._trackalien = True

        self._shipbolts = []
        self._alienbolts = []
        self._boltfirestep = 1
        self._lives = 3

    def __initAlien__(self):
        self._aliens = []
        cli=[]
        if (ALIEN_ROWS%2)==1:
            for j in range(ALIENS_IN_ROW):
                cli.append(Alien(x=(j+1)*(ALIEN_H_SEP+ALIEN_WIDTH),y=GAME_HEIGHT-ALIEN_CEILING,width=ALIEN_WIDTH,height=ALIEN_HEIGHT,source=ALIEN_IMAGES[int((ALIEN_ROWS/2)+0.5)%len(ALIEN_IMAGES)-1]))
            self._aliens.append(cli)
            for i in range(ALIEN_ROWS//2):
                ali = []
                bli = []
                for j in range(ALIENS_IN_ROW):
                    yvalue = GAME_HEIGHT-ALIEN_CEILING-(2*i*(ALIEN_V_SEP+ALIEN_HEIGHT))
                    ali.append(Alien(x=(j+1)*(ALIEN_H_SEP+ALIEN_WIDTH),y=yvalue-(ALIEN_V_SEP+ALIEN_HEIGHT),width=ALIEN_WIDTH,height=ALIEN_HEIGHT,source=ALIEN_IMAGES[int((ALIEN_ROWS/2)+0.5)%len(ALIEN_IMAGES)-2-i]))
                    bli.append(Alien(x=(j+1)*(ALIEN_H_SEP+ALIEN_WIDTH),y=yvalue-2*(ALIEN_V_SEP+ALIEN_HEIGHT),width=ALIEN_WIDTH,height=ALIEN_HEIGHT,source=ALIEN_IMAGES[int((ALIEN_ROWS/2)+0.5)%len(ALIEN_IMAGES)-2-i]))
                self._aliens.append(ali)
                self._aliens.append(bli)
        else:
            for i in range(ALIEN_ROWS//2):
                ali = []
                bli = []
                for j in range(ALIENS_IN_ROW):
                    yvalue = GAME_HEIGHT-ALIEN_CEILING-(2*i*(ALIEN_V_SEP+ALIEN_HEIGHT))
                    ali.append(Alien(x=(j+1)*(ALIEN_H_SEP+ALIEN_WIDTH),y=yvalue-ALIEN_HEIGHT,width=ALIEN_WIDTH,height=ALIEN_HEIGHT,source=ALIEN_IMAGES[(ALIEN_ROWS//2)%len(ALIEN_IMAGES)-1-i]))
                    bli.append(Alien(x=(j+1)*(ALIEN_H_SEP+ALIEN_WIDTH),y=yvalue-(ALIEN_V_SEP+ALIEN_HEIGHT),width=ALIEN_WIDTH,height=ALIEN_HEIGHT,source=ALIEN_IMAGES[((ALIEN_ROWS//2))%len(ALIEN_IMAGES)-1-i]))
                self._aliens.append(ali)
                self._aliens.append(bli)


    # UPDATE METHOD TO MOVE THE SHIP, ALIENS, AND LASER BOLTS
    def update(self,input,dt):
        #moving the ship
        if self._ship != None:
            pos = self._ship.x
            if pos <= SHIP_WIDTH/2:
                pos = SHIP_WIDTH/2
            if pos >= GAME_WIDTH-SHIP_WIDTH/2:
                pos = GAME_WIDTH-SHIP_WIDTH/2

            if input.is_key_down('left'):
                pos -= SHIP_MOVEMENT
            if input.is_key_down('right'):
                pos += SHIP_MOVEMENT

            self._ship.x = pos
        #moving the aliens
        self._time += dt
        self._boltfirestep = random.randint(1,BOLT_RATE)

        self.trackalienmove(dt)

        self.__shipbolt(input)
        self.__moveshipbolt()
        self.__alienbolt()
        self.__movealienbolt()
        self.__lastaliens()
        self.__shipdies()
        self.__aliendies()


    def trackalienmove(self,dt):
        # need to find the most right, left alien
        if self.__rightmostcol().x <= GAME_WIDTH - ALIEN_H_SEP - \
        ALIEN_WIDTH/2 and self.__leftmostcol().x >= ALIEN_H_SEP+ALIEN_WIDTH/2 :
            self.__movealienwave(dt)
        else:
            self._trackalien = not self._trackalien
            self.__aliendownstop(dt)

    def __aliendownstop(self,dt):
        # need to find the most bottom alien
        if self.__bottomalien().y - ALIEN_HEIGHT/2 >= DEFENSE_LINE:
            for Alien in self._aliens:
                for alie in Alien:
                    if alie != None:
                        alie.y -= ALIEN_V_WALK
                        if self._trackalien == True:
                            alie.x = alie.x + ALIEN_H_WALK
                        else:
                            alie.x = alie.x - ALIEN_H_WALK

    def mostbottomalien(self):
        if self.__bottomalien() != None:
            return self.__bottomalien().y

    def __movealienwave(self,dt):
        if ALIEN_SPEED < self._time:
            self._boltfirestep -= 1
            #for i in range(ALIENS_IN_ROW):
            for Alien in self._aliens:
                for alie in Alien:
                    if alie != None:
                        self._time = 0
                        # when the x reaches the end, we want to stop
                        if self._trackalien == True :
                            alie.x += ALIEN_H_WALK
                            alie.y = alie.y
                        elif self._trackalien == False :
                            alie.x -= ALIEN_H_WALK
                            alie.y = alie.y

    def __shipbolt(self,input):
        if input.is_key_pressed('up'):
            if self._shipbolts == []:
                if self._ship != None:
                    self._shipbolts.append(Bolt(x=self._ship.x,y=SHIP_BOTTOM+SHIP_HEIGHT,width=BOLT_WIDTH,height=BOLT_HEIGHT,source='red'))
        self.__moveshipbolt()

    def __alienbolt(self):
        ran = random.choice(self.__lastaliens())
        if self._boltfirestep == 0:
            # need to change __lastaliens to be ok even when one row is gone
            self._alienbolts.append(Bolt(x=ran.x,y=ran.y-ALIEN_HEIGHT/2,width=BOLT_WIDTH,height=BOLT_HEIGHT,source='red'))
            self._boltfirestep = random.randint(1,BOLT_RATE)
        self.__movealienbolt()

    def __moveshipbolt(self):
        # Fine
        i=0
        while i < len(self._shipbolts):
            if self._shipbolts[i].y >= GAME_HEIGHT:
                self._shipbolts.remove(self._shipbolts[i])
            else:
                self._shipbolts[i].y += BOLT_SPEED
                i += 1

    def __movealienbolt(self):
        # Fine
        i=0
        while i < len(self._alienbolts):
            #if self._alienbolts[i].y <= GAME_HEIGHT:
            #    self._alienbolts.remove(self._alienbolts[i])
            #else:
            self._alienbolts[i].y -= BOLT_SPEED
            i += 1

    def __bottomalien(self):
        maxlen = 0
        b = 0
        c = []
        for i in range(ALIENS_IN_ROW):
            x = []
            for j in range(ALIEN_ROWS):
                if self._aliens[j][i] != None:
                    x.append(self._aliens[j][i])
                    b = j
            if b >= maxlen:
                maxlen = b
                if x != []:
                    c = x[-1]
        return c

    def __rightmostcol(self):
        #for every col
        for i in range(ALIENS_IN_ROW):
            #for every row
            for j in range(ALIEN_ROWS):
                if self._aliens[ALIEN_ROWS-j-1][ALIENS_IN_ROW-i-1] != None:
                    return self._aliens[ALIEN_ROWS-j-1][ALIENS_IN_ROW-i-1]

    def __leftmostcol(self):
        #for every col
        for i in range(ALIENS_IN_ROW):
            #for every row
            for j in range(ALIEN_ROWS):
                if self._aliens[j][i] != None:
                    return self._aliens[j][i]

    def __lastaliens(self):
        # Need to change __lastaliens to be ok even when one row is gone
        x = []
        y = []
        for i in range(ALIENS_IN_ROW):
            for j in range(ALIEN_ROWS):
                if self._aliens[j][i] != None:
                    x.append(self._aliens[j][i])
            if x != []:
                y.append(x[-1])
        return y


    def __aliendies(self):
        for i in range(len(self._aliens)):
            for j in range(len(self._aliens[i])):
                if self._aliens[i][j] != None:
                    if self._aliens[i][j].collidealiendies(self._aliens[i][j],self._shipbolts) == True:
                        self._aliens[i][j] = None
                        self._shipbolts = []

    def __shipdies(self):
        if self._ship != []:
            for i in range(len(self._alienbolts)):
                if self._ship != None:
                    if self._ship.collideshipdies(self._ship,self._alienbolts[i]) == True:
                        self._ship = None
                        self._alienbolts.remove(self._alienbolts[i])
                        self._lives -= 1


    def getshipnone(self):
        if self._ship == None:
            return True

    def getaliennone(self):
        a=0
        for Aliens in self._aliens:
            for alie in Aliens:
                if alie != None:
                    a += 1
        if a==0:
            return True

    def getLives(self):
        return self._lives

    def setShip(self,ship):
        self._ship = ship


    # DRAW METHOD TO DRAW THE SHIP, ALIENS, DEFENSIVE LINE AND BOLTS
    def draw(self,view):
        for i in range(ALIEN_ROWS):
            for j in range(ALIENS_IN_ROW):
                if self._aliens[i][j] != None:
                    self._aliens[i][j].draw(view)

        if self._ship != None:
            self._ship.draw(view)

        self._dline.draw(view)

        for i in range(len(self._shipbolts)):
            self._shipbolts[i].draw(view)

        for i in range(len(self._alienbolts)):
            self._alienbolts[i].draw(view)



    # HELPER METHODS FOR COLLISION DETECTION
