# pyright: reportWildcardImportFromLibrary=false

from typing import cast

from direct.showbase.Loader import Loader
from panda3d.core import *
from panda3d.core import NodePath, Vec3, Texture

from CollideObjectBase import (
    SphereCollideObject, InverseSphereCollideObject, CapsuleCollideableObject
)


# planet model and collider
class Planet(SphereCollideObject):
    def __init__(self, loader: Loader, modelPath: str, parentNode: NodePath,
                 nodeName: str, texPath: str, posVec: Vec3, scaleVec: float):
        super(Planet, self).__init__(
            loader, modelPath, parentNode, nodeName, Vec3(0, 0, 0), 0.9
        )
        self.modelNode.setPos(posVec)
        self.modelNode.setScale(scaleVec)
        tex = cast(Texture, loader.loadTexture(texPath))
        self.modelNode.setTexture(tex, 1)


# universe model and collider
class Universe(InverseSphereCollideObject):
    def __init__(self, loader: Loader, modelPath: str, parentNode: NodePath,
                 nodeName: str, texPath: str, posVec: Vec3, scaleVec: float):
        super(Universe, self).__init__(
            loader, modelPath, parentNode, nodeName, Vec3(0, 0, 0), 0.9
        )
        self.modelNode.setPos(posVec)
        self.modelNode.setScale(scaleVec)
        tex = cast(Texture, loader.loadTexture(texPath))
        self.modelNode.setTexture(tex, 1)


# space station and capsule
class SpaceStation(CapsuleCollideableObject):
    def __init__(self, loader: Loader, modelPath: str, parentNode: NodePath,
                 nodeName: str, texPath: str, posVec: Vec3, scaleVec: float):
        super(SpaceStation, self).__init__(
            loader, modelPath, parentNode, nodeName, 1, -1, 5, 1, -1, -5, 10
        )
        self.modelNode.setPos(posVec)
        self.modelNode.setScale(scaleVec)
        tex = cast(Texture, loader.loadTexture(texPath))
        self.modelNode.setTexture(tex, 1)


# drone model and collider
class Drone(SphereCollideObject):
    # counts the drones
    droneCount = 0

    def __init__(self, loader: Loader, modelPath: str, parentNode: NodePath,
                 nodeName: str, texPath: str, posVec: Vec3, scaleVec: float):
        Drone.droneCount += 1
        super(Drone, self).__init__(
            loader, modelPath, parentNode, nodeName + str(Drone.droneCount),
            Vec3(0, 0, 0), 0.9
        )
        self.modelNode.setPos(posVec)
        self.modelNode.setScale(scaleVec)
        tex = cast(Texture, loader.loadTexture(texPath))
        self.modelNode.setTexture(tex, 1)
