from typing import cast

from direct.showbase.Loader import Loader
from panda3d.core import (
    PandaNode, NodePath, Vec3, CollisionNode, CollisionSphere,
    CollisionInvSphere, CollisionCapsule
)


# base scene object
class PlacedObject(PandaNode):
    def __init__(self, loader: Loader, modelPath: str, parentNode: NodePath,
                 nodeName: str):
        PandaNode.__init__(self, nodeName)
        self.modelNode = cast(NodePath, loader.loadModel(modelPath))
        self.modelNode.reparentTo(parentNode)
        self.modelNode.setName(nodeName)


# attach a collision node
class CollidableObject(PlacedObject):
    def __init__(self, loader: Loader, modelPath: str, parentNode: NodePath,
                 nodeName: str):
        super(CollidableObject, self).__init__(loader, modelPath, parentNode, nodeName)
        self.collisionNode = self.modelNode.attachNewNode(
            CollisionNode(nodeName + '_cNode')
        )


# sphere collider
class SphereCollideObject(CollidableObject):
    def __init__(self, loader: Loader, modelPath: str, parentNode: NodePath,
                 nodeName: str, colPositionVec: Vec3, colRadius: float):
        super(SphereCollideObject, self).__init__(loader, modelPath, parentNode, nodeName)
        self.collisionNode.node().addSolid(
            CollisionSphere(colPositionVec.x, colPositionVec.y, colPositionVec.z, colRadius)
        )
        # self.collisionNode.show()


# inside of the universe
class InverseSphereCollideObject(CollidableObject):
    def __init__(self, loader: Loader, modelPath: str, parentNode: NodePath,
                 nodeName: str, colPositionVec: Vec3, colRadius: float):
        super(InverseSphereCollideObject, self).__init__(loader, modelPath, parentNode, nodeName)
        self.collisionNode.node().addSolid(
            CollisionInvSphere(colPositionVec.x, colPositionVec.y, colPositionVec.z, colRadius)
        )
        # self.collisionNode.show()


# station collider
class CapsuleCollideableObject(CollidableObject):
    def __init__(self, loader: Loader, modelPath: str, parentNode: NodePath,
                 nodeName: str, ax: float, ay: float, az: float,
                 bx: float, by: float, bz: float, r: float):
        super(CapsuleCollideableObject, self).__init__(loader, modelPath, parentNode, nodeName)
        self.collisionNode.node().addSolid(
            CollisionCapsule(ax, ay, az, bx, by, bz, r)
        )
        # self.collisionNode.show()
