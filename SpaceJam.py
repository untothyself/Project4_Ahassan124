from typing import cast

from direct.showbase.ShowBase import ShowBase
from direct.showbase.Loader import Loader
from panda3d.core import (
    NodePath, Vec3, CollisionTraverser, CollisionHandlerPusher
)

import DefensePaths as defensePaths
import SpaceJamClasses as spaceJamClasses
import Player as playerClasses


class SpaceJam(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.disableMouse()

        # exit key
        self.accept('escape', self.userExit)

        # asset loader and scene graph
        self.sceneLoader = cast(Loader, self.loader)
        self.sceneRender = cast(NodePath, self.render)

        self.SetupScene()
        self.SetupDefenses()
        self.SetCamera()
        self.SetupCollisions()

    def SetupScene(self):
        loader = self.sceneLoader
        render = self.sceneRender
        planetModel = './Assets/Planets/protoPlanet.x'

        # load the universe
        self.Universe = spaceJamClasses.Universe(
            loader, './Assets/Universe/Universe.x', render,
            'Universe', './Assets/Universe/Universe.jpg',
            Vec3(0, 0, 0), 15000
        )

        # load the planets and their textures
        self.Planet1 = spaceJamClasses.Planet(
            loader, planetModel, render, 'Mercury',
            './Assets/Planets/mercury.jpg', Vec3(-30, 70, 18), 7
        )
        self.Planet2 = spaceJamClasses.Planet(
            loader, planetModel, render, 'Venus',
            './Assets/Planets/venus.jpg', Vec3(-18, 100, -14), 9
        )
        self.Planet3 = spaceJamClasses.Planet(
            loader, planetModel, render, 'Earth',
            './Assets/Planets/earth.jpg', Vec3(22, 75, 12), 9
        )
        self.Planet4 = spaceJamClasses.Planet(
            loader, planetModel, render, 'Mars',
            './Assets/Planets/mars.jpg', Vec3(40, 105, -10), 8
        )
        self.Planet5 = spaceJamClasses.Planet(
            loader, planetModel, render, 'Jupiter',
            './Assets/Planets/jupiter.jpg', Vec3(-34, 135, -8), 12
        )
        self.Planet6 = spaceJamClasses.Planet(
            loader, planetModel, render, 'Saturn',
            './Assets/Planets/saturn.jpg', Vec3(30, 145, 28), 11
        )

        # space station and player ship
        self.SpaceStation = spaceJamClasses.SpaceStation(
            loader, './Assets/Space Station/spaceStation.x', render,
            'Space Station', './Assets/Space Station/SpaceStation1_Dif2.png',
            Vec3(0, 105, 14), 0.8
        )
        self.SpaceStation.modelNode.setHpr(30, 10, 0)

        self.Player = playerClasses.Player(
            loader, self.taskMgr, self.accept,
            './Assets/Spaceships/Dumbledore.egg', render,
            'Player', './Assets/Spaceships/spacejet_C.png',
            Vec3(0, 35, -4), 3
        )
        self.Player.modelNode.setHpr(0, 0, 0)

    def AddDrone(self, centerObject, offset: Vec3, red=1.0, green=1.0, blue=1.0):
        # drone position around the object
        position = centerObject.modelNode.getPos() + offset
        drone = spaceJamClasses.Drone(
            self.sceneLoader,
            './Assets/Drone Defender/DroneDefender.x',
            self.sceneRender,
            'Drone', './Assets/Drone Defender/octotoad1_auv.png',
            position, 0.38
        )
        # drone color
        drone.modelNode.setColorScale(red, green, blue, 1.0)

    def DrawCircleXDefense(self, centerObject, step: int, count: int, radius: float):
        offset = defensePaths.CircleX(step, count, radius)
        self.AddDrone(centerObject, offset, 1.0, 0.2, 0.2)

    def DrawCircleYDefense(self, centerObject, step: int, count: int, radius: float):
        offset = defensePaths.CircleY(step, count, radius)
        self.AddDrone(centerObject, offset, 0.2, 1.0, 0.2)

    def DrawCircleZDefense(self, centerObject, step: int, count: int, radius: float):
        offset = defensePaths.CircleZ(step, count, radius)
        self.AddDrone(centerObject, offset, 0.2, 0.4, 1.0)

    def DrawCloudDefense(self, centerObject, radius: float):
        offset = defensePaths.Cloud(radius)
        self.AddDrone(centerObject, offset)

    def DrawBaseballSeams(self, centerObject, step: int, count: int, radius: float):
        offset = defensePaths.BaseballSeams(step, count, 0.4) * radius
        self.AddDrone(centerObject, offset)

    def SetupDefenses(self):
        # circle defenses for the first three planets
        for step in range(12):
            self.DrawCircleXDefense(self.Planet1, step, 12, 12)
            self.DrawCircleYDefense(self.Planet2, step, 12, 15)
            self.DrawCircleZDefense(self.Planet3, step, 12, 16)

        # drone cloud around jupiter
        for step in range(20):
            self.DrawCloudDefense(self.Planet5, 18)

        # baseball seams around the station
        for step in range(28):
            self.DrawBaseballSeams(self.SpaceStation, step, 28, 14)

    def SetCamera(self):
        # camera follows the player
        self.disableMouse()
        camera = cast(NodePath, self.camera)
        camera.reparentTo(self.Player.modelNode)
        camera.setPos(0, -15, 5)
        camera.lookAt(0, 15, 0)

    def SetupCollisions(self):
        # check collisions in the scene
        self.cTrav = CollisionTraverser()
        self.pusher = CollisionHandlerPusher()
        self.pusher.addCollider(self.Player.collisionNode, self.Player.modelNode)
        self.cTrav.addCollider(self.Player.collisionNode, self.pusher)
        self.cTrav.showCollisions(self.sceneRender)


app = SpaceJam()
app.run()
