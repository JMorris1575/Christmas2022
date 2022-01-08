#####################
The St. Nicholas Game
#####################

I'm planning to add a new game to the website for Christmas 2022, a game involving helping St. Nicholas deliver bags of
gold to poor families. The details of the game design will probably come to me gradually during the year and especially
as I work my way through similar tutorials. This document will serve as a place where I can jot down my ideas as they
come to me.

************************
Topdown Shooter Tutorial
************************

I am currently (Starting in December 2021) working through the Topdown Shooter tutorial at:

https://www.youtube.com/channel/UCLzFt-NdfCm8WFKTyqD0yJw

and it has already given me a few ideas.

The St. Nicholas Sprite
=======================

The Kenney topdown shooter character spritesheet had a character I thought I could modify with GIMP to become a sprite
for the St. Nicholas character. This is how it looks now:

.. image:: images/StNicholas.png

Node Based Composition
======================

In Part 7 of the tutorial, around 5:00, Joe speaks of "Node Based Composition" as a way of implementing DRY (Don't
Repeat Yourself). He says that Node Based Composition means to create a separate node within the scene that stores
the information needed and access it from there. This can help because it is a separate scene that can be dragged and
dropped into any other scene that needs it. Whether that will be helpful or not remains to be seen.

Dependency Injection
====================

I'm learning more about how to connect different nodes of my tree, a problem I had when writing the Concentration
program. In Part 8 of the tutorial he talks about something he calls "dependency injection" as a method for
easily making calls between nodes on the same level in the tree (sibling nodes, I believe). A higher level node sends
the necessary nodes to the lower-level nodes so that, if the hierarchy changes, the new information can be easily
changed in the calling function of the higher level node instead of my trying to find all the references to it.

*****************
Building the Game
*****************

Here I will describe the gradual development of the game. As it stands now, I only have a rudimentary idea of what I
want in the game but I think that is alright. Ideas will come to me as I start to build it.

Here is a table of contents:

#. :ref:`initial_ideas`
#. :ref:`gold_bags`

.. _initial_ideas:

Initial Ideas
=============

 Meanwhile, here are my initial ideas:

#. It will be in the genre of the "topdown shooter" style of game but the "shooting" will actually be gift-giving. St.
   Nicholas will move through the town streets tossing bags of gold into the homes of needy people.
#. The game will have several levels, yet to be determined. Each level may contain any or all of the following:

   A. A maze of streets to get through to find the home(s) of needy people.
   #. Robbers who can steal gold from the kindly saint if they get close enough.
   #. Objects that can be picked up, as in an adventure game, to unlock doors or be rid of obstacles.

#. Perhaps the challenge of each level will have to be completed in a certain amount of time.
#. A HUD (Heads Up Display) can be used to display how many bags of gold St. Nicholas has left and the time remaining if
   that option is used.

First Steps
===========

Here is a list of steps to complete as I start to build the game:

#. Create the game. (See :ref:`create_game`)
#. Create the St. Nicholas character and display it in the game. (See :ref:`st_nick`)
#. Add the ability to move St. Nicholas using the keyboard. (See :ref:`keyboard_move`)
#. Have the St. Nicholas character face the direction he is moving. (See :ref:`orienting_st_nick`)
#. Add the ability to move St. Nicholas with arrows on the display screen. (See :ref:`button_move`)
#. Save the St. Nicholas character in his own scene in an ``actors`` directory. (See :ref:`st_nick_to_scene`)

.. _create_game:

Creating the Game
-----------------

I'm going to have to come up with a good name for the game. Perhaps "St. Nicholas Adventure." Not bad for a first try.

I created a new Project called ``StNicholasAdventure`` and chose GLES2 as the renderer because that was suggested for
games to be played on the web.

Following Part 1 of the jmbiv tutorial (https://www.youtube.com/watch?v=gXkkNSfxLRI ) I started by changing
the default import preset to ``2D Pixel`` to simplify the bitmaps I will use in the game. This probably isn't really
necessary but, like the tutorial, I don't need the higher quality for this game.

I made the size of the game 800 x 600 to see if I like that. It should fit nicely into ten columns of a Bootstrap
container of the ``lg`` size. (See https://getbootstrap.com/docs/5.1/layout/containers/ ) The whole container is 960 px
wide so each of the twelve columns would be 80 pixels. Ten columns would be 800 pixels.

I set the game to expand and shrink with the size of the device on the ``General`` tab of
``Project->Project Settings...->Display->Window->Stretch``. I set the ``mode`` to ``2d`` and Aspect to ``keep``.

I elected to create a ``2D Scene`` which I called ``Main`` and saved it as ``Main.tscn`` in the default folder.

I ran the game and got a 800 x 600 grey box. Just what I wanted at this point!

.. _st_nick:

Displaying St. Nicholas
-----------------------

I added a ``KinematicBody2D`` as a child of the ``Main`` scene and a ``Sprite`` node as a child of that.

I created an ``actors`` folder under the ``res://`` folder and an ``images`` folder inside of that. I copied
the ``StNicholas.png`` image I had created earlier (apparently on the rectory computer) and add it as the texture for
the ``Sprite`` node.

The texture for the St. Nicholas character is 38 x 43. Perhaps my roadways should all be multiples of 50 pixels wide.

I added a ``CollisionShape2D`` as a child of the ``StNick`` node and gave it a ``CapsuleShape`` as its
``CollisionShape2D``.

I moved the character a litte into the game where it could be seen and, when I ran the game, it all looked good.

.. _keyboard_move:

Move St. Nicholas with Keyboard
-------------------------------

After watching Part 2 of the jmbiv Top-down Shooter Tutorial at https://www.youtube.com/watch?v=tIug3S4r5iE I was able
to get the St. Nicholas characted to move with the arrow keys, with the numpad keys and with the W, A, S and D keys
without difficulty.

Godot has default actions of ``ui_up``, ``ui_down``, ``ui_left`` and ``ui_right`` that are already connected to the
arrow keys and the numpad keys but, according to the documentation at: "Because these actions are used for focus they
should not be used for any gameplay code." That means I will need to create my own ``up``, ``down``, ``left`` and
``right`` actions and map all those keys to them. On the ``Input Map`` tab of the ``Project->Project Settings...``
window, I simply entered the names of the actions at the top and pressed ``Add``. Then I selected each one and clicked
the ``+`` button to add the arrow keys, each of the W, A, S  and D keys, and the corresponding joystick buttons. I used
``Key`` rather than ``Physical Key``. I don't yet completely know the difference.

I added a script to the ``StNick`` node and wrote the following code::

    extends KinematicBody2D


    export (int) var speed = 100


    func _ready() -> void:
        pass


    func _process(delta: float) -> void:
        var movement_direction := Vector2.ZERO

        if Input.is_action_pressed("up"):
            movement_direction.y = -1
        if Input.is_action_pressed("down"):
            movement_direction.y = 1
        if Input.is_action_pressed("left"):
            movement_direction.x = -1
        if Input.is_action_pressed("right"):
            movement_direction.x = 1

        movement_direction = movement_direction.normalized()
        move_and_slide(movement_direction * speed)

The St. Nicholas character now moves around in response to all the movement keys.

.. _orienting_st_nick:

Orienting St. Nicholas in the Direction of Motion
-------------------------------------------------

The only method I could find in the ``KinematicBody2D`` documentation, which is actually inherited from ``Node2D``,
is the ``look_at(Vector2 point)`` method. Since it takes a ``Vector2 point`` as its input I can't just use
``movement_direction``. I can, however, add the ``movement_direction`` to the character's ``global_position`` and use
that as the point to look at. So, all I had to do was to add the line:

    ``look_at(global_position + movement_direction)``

between the ``movement_direction = ...`` and ``move_and_slide(...`` lines in the code above.

.. _button_move:

Move St. Nicholas with Display Buttons
--------------------------------------

The St. Nicholas character also needs to move around on a cell phone or tablet screen that has no keyboard. I think that
adding arrow buttons to both ends of the screen should allow users of cell phones or tablets to play the game using
their thumbs on those buttons but I may have to investigate how this is usually done.

It seems that Godot's ``TouchScreenButton`` is what I should use. It can be configured, in the node editor I think,
to appear always, for testing, or only on touch screens, for deployment.

I found some game icons at https://www.kenney.nl/assets/game-icons and went to ``PNG`` folder to copy just the ones I
wanted. I started with the 2x size but may change that later. I put them in a new folder under the game folder called
``global images``.

I created four ``TouchScreenButton``s as children of ``Main`` and named them ``UpButton``, ``DownButton``,
``LeftButton`` and ``RightButton`` respectively. I drag/dropped the corresponding icon into the ``Normal`` property of
each. Later I may want to create images for the ``Pressed`` property.

I created a script under ``Main`` and added the following code::

    extends Node2D


    func _ready() -> void:
        $UpButton.action = "up"
        $DownButton.action = "down"
        $LeftButton.action = "left"
        $RightButton.action = "right"

For testing purposes I went to ``Project Settings`` under ``Input Settings->Pointing->Emulate Touch From Mouse`` and set
it to ``true``.

I tested the onscreen buttons with the mouse and they worked fine. Then I set the ``Visibility Mode`` to
``TouchScreen Only`` for each of the buttons but they still show up on my computer screen. That is because when
``Emulate Touch From Mouse`` is on, ``TouchScreenButton``s are always visible.

.. _st_nick_to_scene:

Creating a Separate Scene for St. Nick
--------------------------------------

The ``StNick`` node now only exists as a child of the main scene. As in the jmbiv tutorial, I want to separate it into
its own scene. Right-clicking it in the tree and selecting ``Save Branch as Scene`` I placed StNick.tscn in the
``actors`` directory.

.. _gold_bags:

Bags of Gold
============

St. Nicholas can carry the bags of gold in his hand, but that makes it more likely that thieves will take them. If he
keeps them in his pocket they won't necessarily know he has them and may not bother him.

That may be a matter of setting the probabilities in some kind of a random function for the thieves but first I need to
implement the behavior of the bags of gold. Here is what needs to be done:

#. Find or Create an Icon for the gold bags. (See :ref:`gold_bag_icon`)
#. Create a separate scene for gold bags. (See :ref:`create_gold_bag`)
#. Implement the process for St. Nicholas to throw a gold bag. (See :ref:`throwing_gold_bag`)
#. Implement the hiding and revealing process for gold bags. (See :ref:`pocket_gold_bag`)

.. _gold_bag_icon:

The Gold Bag Icon
-----------------

I couldn't find any ready-made images of gold bags from Kenney so I went to https://openclipart.org and found something
I might be able to edit in Gimp. In the process I thought I might like to show that a bag had already been tossed in a
particular location by displaying an image of a bag that had opened and spilled a few coins so I also downloaded a
treasure chest for the use of its coins.

To look right the images can only be maybe 16 x 16 pixels, not a lot to work with! I finally settled on 20 x 20 but they
still look pretty tiny! Maybe they will look bigger in the game.

I did create textures for a bag for St. Nicholas to throw, and another one to lie open on the floor after he throws it.
Which brings to mind a question: what should happen if he throws it in the wrong place? Should he have to go pick it up
before the thieves get it?

.. _create_gold_bag:

Creating the Gold Bag
---------------------

The jmbiv Top-Down Shooter tutorial I am watching uses ``Area2D`` nodes for the bullets but I don't know if they will
be best to use for the bags of gold. I don't think they handle collisions and I might want my gold bags to collide off
walls and things if they are thrown from the wrong place. They should have to go through an open window I think.
``RigidBody2D`` nodes seemed too complicated to use in a top-down shooter so I settled on using a ``KinematicsBody2D``
node.

I will start, as he did in his tutorial, with a ``GoldBag`` as a child of the ``StNick`` node and already placed in his
right hand and then make it into it's own scene. I will create an ``objects`` directory for the ``GoldBag`` node in
anticipation of other objects that may be added later.

Once I did this I discovered a problem. Having two ``KinematicBody2D``s in contact with one another, with their
``CollisionShape2D``s overlapping meant they were always in a collision state. St. Nicholas went flying off the screen
to the upper left. I had to set the Collision Layers and Collision Masks for each object. I put St. Nicholas in layer 1
and turned off his interactions (turned off the mask) on layers one and two. I put the gold bag in layer 2 and turned
off his interactions with layers one and two. I set both of them to interact with layer 3 objects whatever they may turn
out to be. (I'm thinking walls and other things in the environment.)

Once I did that it started to work as expected, I could move St. Nicholas and the bag of gold moved with him but I don't
really like the looks of the bag of gold. It's too dark in color and doesn't look much like a bag of gold. I may try to
lighten it up, try for another image of a bag, or maybe just opt for gold coins which are readily available as game
assets.

I made some new textures which, for the moment, look better to me, though I may want to rotate it a little. I'm
currently using the 20 x 20 image: ``bag-of-gold-cartoon-small.png``.

.. _throwing_gold_bag:

Throwing the Gold Bag
---------------------

When the player hits the space bar, or a cell phone or tablet user hits some kind of a "Throw" button, the gold bag
should leave St. Nicholas in the direction he is facing and fly through the air to its landing place. Later I can
implement such things as checking that it really gets to a proper target area or if it bounces off walls or objects in
the environment. Here I am just concerned about it moving from St. Nicholas' hand to a certain distance away.

This may take some doing so I'll break it into steps:

#. Separate the GoldBag into its own scene. (See :ref:`gold_bag_scene`)
#. Display the GoldBag in St. Nicholas' hand. (See :ref:`gold_bag_in_hand`)
#. Set up the throwing input keys and stub in a procedure that will throw them. (See :ref:`throwing_input`)
#. Establish starting and ending points of the throw. (See :ref:`chart_throw`)
#. Animate the throw. (See :ref:`throw_animation`)

.. _gold_bag_scene:

Separating the GoldBag into its own Scene
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This was easy and will help in the process of supplying ``GoldBag``s in the future. This can be when St. Nicholas enters
a new level and starts with a certain number of gold bags or when he has lost some through bad throws or thieves and has
to go back home and pick up some more.

In the StNick scene I right-clicked the ``GoldBag`` and selected ``Save Branch as Scene`` and selected the ``objects``
directory for it where its images are already stored.

.. _gold_bag_in_hand:

Getting the GoldBag into StNick's Hand
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Then, as he did in Part 3 of the Tutorial (around 11:20), I can add a ``GoldBag`` to the StNick scene as a
``PackedScene`` export variable. This will allow me to create new instances of the ``GoldBag`` scene from within the
``StNick`` scene. I drag-dropped ``GoldBag.tscn`` into the ``StNick`` scene and deleted the ``GoldBag`` scene that used
to be there. Eventually, I think, some other part of the program will instantiate the gold bags but, for now, I will
create one in the ``_ready()`` function::

    func _ready() -> void:
        gold_bag = GoldBag.instance()
        gold_bag.set_position(Vector2(16, 17))
        add_child(gold_bag)

I had already moved the ``GoldBag``'s sprite into St. Nicholas' right hand but I zeroed that out since it will probably
complicate animating them when thrown. For now I will move it to his hand with the given ``position()`` method.

.. _throwing_input:

Input for Throwing
^^^^^^^^^^^^^^^^^^

.. _chart_throw:

Mapping the Throw
^^^^^^^^^^^^^^^^^

.. _throw_animation:

Animating the Throw
^^^^^^^^^^^^^^^^^^^

.. _pocket_gold_bag:

Gold Bags in the Pocket
-----------------------

