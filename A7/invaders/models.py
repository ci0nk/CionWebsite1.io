"""
Models module for Alien Invaders

This module contains the model classes for the Alien Invaders game. Anything
that you interact with on the screen is model: the ship, the laser bolts, and
the aliens.

Just because something is a model does not mean there has to be a special
class for it. Unless you need something special for your extra gameplay
features, Ship and Aliens could just be an instance of GImage that you move
across the screen. You only need a new class when you add extra features to
an object. So technically Bolt, which has a velocity, is really the only model
that needs to have its own class.

With that said, we have included the subclasses for Ship and Aliens. That is
because there are a lot of constants in consts.py for initializing the
objects, and you might want to add a custom initializer.  With that said,
feel free to keep the pass underneath the class definitions if you do not want
to do that.

You are free to add even more models to this module.  You may wish to do this
when you add new features to your game, such as power-ups.  If you are unsure
about whether to make a new class or not, please ask on Piazza.

Connie Zhang (cz467) and Cion Kim (ck758)
# DATE COMPLETED HERE
"""
from consts import *
from game2d import *

# PRIMARY RULE: Models are not allowed to access anything in any module other
# than consts.py.  If you need extra information from Gameplay, then it should
# be a parameter in your method, and Wave should pass it as a argument when it
# calls the method.


class Ship(GImage):
    """
    A class to represent the game ship.

    At the very least, you want a __init__ method to initialize the ships
    dimensions. These dimensions are all specified in consts.py.

    You should probably add a method for moving the ship.  While moving a
    ship just means changing the x attribute (which you can do directly),
    you want to prevent the player from moving the ship offscreen.  This
    is an ideal thing to do in a method.

    You also MIGHT want to add code to detect a collision with a bolt. We
    do not require this.  You could put this method in Wave if you wanted to.
    But the advantage of putting it here is that Ships and Aliens collide
    with different bolts.  Ships collide with Alien bolts, not Ship bolts.
    And Aliens collide with Ship bolts, not Alien bolts. An easy way to
    keep this straight is for this class to have its own collision method.

    However, there is no need for any more attributes other than those
    inherited by GImage. You would only add attributes if you needed them
    for extra gameplay features (like animation).
    """
    #  IF YOU ADD ATTRIBUTES, LIST THEM BELOW

    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)

    # INITIALIZER TO CREATE A NEW SHIP
    def __init__(self,x,y,width,height,source, ship=None, aliens=0, bolts=None, dline=0, lives=0, time=0):
        super().__init__(x=GAME_WIDTH/2,y=SHIP_BOTTOM+(SHIP_HEIGHT/2),width=SHIP_WIDTH,height=SHIP_HEIGHT,source=source)

        self._ship = ship
        self._aliens = aliens
        self._bolts = bolts
        self._dline = dline
        self._lives = lives
        self._time = time


    # METHODS TO MOVE THE SHIP AND CHECK FOR COLLISIONS
    def collideshipdies(self,ship,bolt):
        """
        Returns True if the player bolt collides with this alien

        This method returns False if bolt was not fired by the player.

        Parameter bolt: The laser bolt to check
        Precondition: bolt is of class Bolt
        """
        if ship != []:
            if bolt != []:
                if ship.contains((bolt.x,bolt.y)) or \
                ship.contains((bolt.x + BOLT_WIDTH,bolt.y)) or \
                ship.contains((bolt.x ,bolt.y + BOLT_HEIGHT)) or \
                ship.contains((bolt.x + BOLT_WIDTH,bolt.y + BOLT_HEIGHT)):
                    return True


    # COROUTINE METHOD TO ANIMATE THE SHIP

    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY


class Alien(GImage):
    """
    A class to represent a single alien.

    At the very least, you want a __init__ method to initialize the alien
    dimensions. These dimensions are all specified in consts.py.

    You also MIGHT want to add code to detect a collision with a bolt. We
    do not require this.  You could put this method in Wave if you wanted to.
    But the advantage of putting it here is that Ships and Aliens collide
    with different bolts.  Ships collide with Alien bolts, not Ship bolts.
    And Aliens collide with Ship bolts, not Alien bolts. An easy way to
    keep this straight is for this class to have its own collision method.

    However, there is no need for any more attributes other than those
    inherited by GImage. You would only add attributes if you needed them
    for extra gameplay features (like giving each alien a score value).
    """
    #  IF YOU ADD ATTRIBUTES, LIST THEM BELOW
    pass

    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)

    # INITIALIZER TO CREATE AN ALIEN

    '''def __init__(self, x,y,width,height,source):
        super().__init__(x=x,y=y,width=ALIEN_WIDTH,height=ALIEN_HEIGHT,source='alien1.png')'''

        # make sure to define correctly later
    def __init__(self,x,y,width,height,source, ship=None, aliens=0, bolts=None, dline=0, lives=0, time=0):
        super().__init__(x=x,y=y,width=ALIEN_WIDTH,height=ALIEN_HEIGHT,source=source)
        self._ship = ship
        self._aliens = aliens
        self._bolts = bolts
        self._dline = dline
        self._lives = lives
        self._time = time


    # METHOD TO CHECK FOR COLLISION (IF DESIRED)
    def collidealiendies(self,alien,bolt):
        """
        Returns True if the player bolt collides with this alien

        This method returns False if bolt was not fired by the player.

        Parameter bolt: The laser bolt to check
        Precondition: bolt is of class Bolt
        """
        if alien != None:
            if bolt != []:
                if alien.contains((bolt[0].x,bolt[0].y)) or \
                alien.contains((bolt[0].x + BOLT_WIDTH,bolt[0].y)) or \
                alien.contains((bolt[0].x ,bolt[0].y + BOLT_HEIGHT)) or \
                alien.contains((bolt[0].x + BOLT_WIDTH,bolt[0].y + BOLT_HEIGHT)):
                    return True
    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY


class Bolt(GRectangle):
    """
    A class representing a laser bolt.

    Laser bolts are often just thin, white rectangles. The size of the bolt
    is determined by constants in consts.py. We MUST subclass GRectangle,
    because we need to add an extra (hidden) attribute for the velocity of
    the bolt.

    The class Wave will need to look at these attributes, so you will need
    getters for them.  However, it is possible to write this assignment with
    no setters for the velocities.  That is because the velocity is fixed and
    cannot change once the bolt is fired.

    In addition to the getters, you need to write the __init__ method to set
    the starting velocity. This __init__ method will need to call the __init__
    from GRectangle as a  helper.

    You also MIGHT want to create a method to move the bolt.  You move the
    bolt by adding the velocity to the y-position.  However, the getter
    allows Wave to do this on its own, so this method is not required.
    """
    # INSTANCE ATTRIBUTES:
    # Attribute _velocity: the velocity in y direction
    # Invariant: _velocity is an int or float

    # LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    pass

    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)


    # INITIALIZER TO SET THE VELOCITY
    def __init__(self,x,y,width,height,source, ship=[], aliens=[], bolts=[], dline=0, lives=0, time=0):
        super().__init__(x=x,y=y,width=BOLT_WIDTH,height=BOLT_HEIGHT,fillcolor='red', linecolor='orange')
        self._ship = ship
        self._aliens = aliens
        self._bolts = bolts
        self._dline = dline
        self._lives = lives
        self._time = time
        self._velocity = BOLT_SPEED
    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY

# IF YOU NEED ADDITIONAL MODEL CLASSES, THEY GO HERE
