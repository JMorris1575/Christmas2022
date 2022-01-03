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

Node Based ?????
================

I'm learning more about how to connect different nodes of my tree, a problem I had when writing the Concentration
program. In section eight of the tutorial he talks about something he calls "dependency injection" as a method for
easily making calls between nodes on the same level in the tree (sibling nodes, I believe). A higher level node sends
the necessary nodes to the lower-level nodes so that, if the hierarchy changes, the new information can be easily
changed in the calling function of the higher level node instead of my trying to find all the references to it.

He also has a name for the structuring idea he's following, Node Based something-or-other perhaps. That may be mentioned
in section 7 or earlier.

