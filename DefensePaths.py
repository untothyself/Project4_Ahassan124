# pyright: reportWildcardImportFromLibrary=false

import math
import random

from panda3d.core import *
from panda3d.core import Vec3


# x circle
def CircleX(step: int, count: int, radius: float) -> Vec3:
    angle = 2 * math.pi * step / count
    return Vec3(0, radius * math.cos(angle), radius * math.sin(angle))


# y circle
def CircleY(step: int, count: int, radius: float) -> Vec3:
    angle = 2 * math.pi * step / count
    return Vec3(radius * math.cos(angle), 0, radius * math.sin(angle))


# z circle
def CircleZ(step: int, count: int, radius: float) -> Vec3:
    angle = 2 * math.pi * step / count
    return Vec3(radius * math.cos(angle), radius * math.sin(angle), 0)


# random drone cloud
def Cloud(radius: float) -> Vec3:
    x = 2 * random.random() - 1
    y = 2 * random.random() - 1
    z = 2 * random.random() - 1
    unitVec = Vec3(x, y, z)
    # avoid a zero vector
    if unitVec.lengthSquared() == 0:
        unitVec = Vec3(1, 0, 0)
    unitVec.normalize()
    return unitVec * radius


# baseball seams pattern
def BaseballSeams(step: int, numSeams: int, B: float, F: float = 1) -> Vec3:
    time = step / float(numSeams) * 2 * math.pi
    F4 = 0
    R = 1

    xxx = math.cos(time) - B * math.cos(3 * time)
    yyy = math.sin(time) + B * math.sin(3 * time)
    zzz = F * math.cos(2 * time) + F4 * math.cos(4 * time)

    rrr = math.sqrt(xxx ** 2 + yyy ** 2 + zzz ** 2)
    x = R * xxx / rrr
    y = R * yyy / rrr
    z = R * zzz / rrr

    return Vec3(x, y, z)
