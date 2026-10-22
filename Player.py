from typing import cast

from direct.showbase.Loader import Loader
from direct.task import Task
from panda3d.core import NodePath, Vec3, Texture, ClockObject

from CollideObjectBase import SphereCollideObject


# spaceship model and collider
class Spaceship(SphereCollideObject):
    def __init__(self, loader: Loader, taskMgr, accept, modelPath: str,
                 parentNode: NodePath, nodeName: str, texPath: str,
                 posVec: Vec3, scaleVec: float):
        super(Spaceship, self).__init__(
            loader, modelPath, parentNode, nodeName, Vec3(0, 0, 0), 1
        )
        self.taskManager = taskMgr
        self.accept = accept
        self.modelNode.setPos(posVec)
        self.modelNode.setScale(scaleVec)
        tex = cast(Texture, loader.loadTexture(texPath))
        # replace the ship texture
        self.modelNode.clearTexture()
        self.modelNode.setTexture(tex, 1)
        self.SetKeyBindings()

    def SetKeyBindings(self):
        # ship key bindings
        self.accept('space', self.Thrust, [1])
        self.accept('space-up', self.Thrust, [0])

        self.accept('arrow_left', self.LeftTurn, [1])
        self.accept('arrow_left-up', self.LeftTurn, [0])
        self.accept('arrow_right', self.RightTurn, [1])
        self.accept('arrow_right-up', self.RightTurn, [0])

        self.accept('arrow_up', self.TurnUp, [1])
        self.accept('arrow_up-up', self.TurnUp, [0])
        self.accept('arrow_down', self.TurnDown, [1])
        self.accept('arrow_down-up', self.TurnDown, [0])

        self.accept('q', self.RollLeft, [1])
        self.accept('q-up', self.RollLeft, [0])
        self.accept('e', self.RollRight, [1])
        self.accept('e-up', self.RollRight, [0])

    def Thrust(self, keyDown):
        if keyDown:
            if not self.taskManager.hasTaskNamed('forward-thrust'):
                self.taskManager.add(self.ApplyThrust, 'forward-thrust')
        else:
            self.taskManager.remove('forward-thrust')

    def ApplyThrust(self, _task):
        # forward direction
        rate = 20 * ClockObject.getGlobalClock().getDt()
        trajectory = self.modelNode.getParent().getRelativeVector(
            self.modelNode, Vec3.forward()
        )
        trajectory.normalize()
        self.modelNode.setFluidPos(self.modelNode.getPos() + trajectory * rate)
        return Task.cont

    def LeftTurn(self, keyDown):
        if keyDown:
            if not self.taskManager.hasTaskNamed('left-turn'):
                self.taskManager.add(self.ApplyLeftTurn, 'left-turn')
        else:
            self.taskManager.remove('left-turn')

    def ApplyLeftTurn(self, _task):
        rate = 75 * ClockObject.getGlobalClock().getDt()
        self.modelNode.setH(self.modelNode.getH() + rate)
        return Task.cont

    def RightTurn(self, keyDown):
        if keyDown:
            if not self.taskManager.hasTaskNamed('right-turn'):
                self.taskManager.add(self.ApplyRightTurn, 'right-turn')
        else:
            self.taskManager.remove('right-turn')

    def ApplyRightTurn(self, _task):
        rate = 75 * ClockObject.getGlobalClock().getDt()
        self.modelNode.setH(self.modelNode.getH() - rate)
        return Task.cont

    def TurnUp(self, keyDown):
        if keyDown:
            if not self.taskManager.hasTaskNamed('turn-up'):
                self.taskManager.add(self.ApplyTurnUp, 'turn-up')
        else:
            self.taskManager.remove('turn-up')

    def ApplyTurnUp(self, _task):
        rate = 75 * ClockObject.getGlobalClock().getDt()
        self.modelNode.setP(self.modelNode.getP() + rate)
        return Task.cont

    def TurnDown(self, keyDown):
        if keyDown:
            if not self.taskManager.hasTaskNamed('turn-down'):
                self.taskManager.add(self.ApplyTurnDown, 'turn-down')
        else:
            self.taskManager.remove('turn-down')

    def ApplyTurnDown(self, _task):
        rate = 75 * ClockObject.getGlobalClock().getDt()
        self.modelNode.setP(self.modelNode.getP() - rate)
        return Task.cont

    def RollLeft(self, keyDown):
        if keyDown:
            if not self.taskManager.hasTaskNamed('roll-left'):
                self.taskManager.add(self.ApplyRollLeft, 'roll-left')
        else:
            self.taskManager.remove('roll-left')

    def ApplyRollLeft(self, _task):
        rate = 75 * ClockObject.getGlobalClock().getDt()
        self.modelNode.setR(self.modelNode.getR() - rate)
        return Task.cont

    def RollRight(self, keyDown):
        if keyDown:
            if not self.taskManager.hasTaskNamed('roll-right'):
                self.taskManager.add(self.ApplyRollRight, 'roll-right')
        else:
            self.taskManager.remove('roll-right')

    def ApplyRollRight(self, _task):
        rate = 75 * ClockObject.getGlobalClock().getDt()
        self.modelNode.setR(self.modelNode.getR() + rate)
        return Task.cont


# player ship
class Player(Spaceship):
    pass
