from itertools import combinations
from pdb import set_trace

class Rect(object):
    def __init__(self, pos=PVector(), w=1, h=1):
        self.pos = pos
        self.width = w
        self.height = h


class Circle(object):
    def __init__(self, x=0, y=0, radius=1):
        self.x = x
        self.y = y
        self.radius = radius


class PhysicsBody:
    def __init__(self, element, shape=Rect()):
        self.element = element
        self.shape = shape
        self.vel = PVector()
        self.mass = 1.
        self.bounce = 0.

    @property
    def invMass(self):
        if self.mass == 0:
            return 0
        return 1/self.mass

class PhysicsWorld:
    def __init__(self):
        self.g = 50.
        self.bodies = []
        self.prevTime = 0.
        self.speed = 2

    def update(self, event):
        t = frameCount / frameRate
        delta = t - self.prevTime
        self.prevTime = t

        for pair in combinations(self.bodies, 2):
            self.collide(*pair)


        for e in self.bodies:
            # gravity
            f = PVector(0, e.mass * self.g)  # F = ma
            e.vel.add(f.mult(e.invMass).mult(delta))
            # air resistance
            e.vel.mult(.98)

            vv = PVector.mult(e.vel, delta*self.speed) # s = vt
            e.element.x += min(vv.x, 20)
            e.element.y += min(vv.y, 20)

    def collide(self, a, b):
        m = self.calcCollision(a, b)
        if (m["collides"]):
            relV = b.vel - a.vel
            normalVel = PVector.dot(relV, m["normal"])
            if normalVel > 0:
                return
            
            e = min(a.bounce, b.bounce)

            j = -(1 + e) * normalVel
            j /= a.invMass + b.invMass
            
            impulse = PVector.mult(m["normal"], j)
            massSum = a.mass + b.mass
            ratio = a.mass / massSum
            a.vel.sub(PVector.mult(impulse, ratio))
            # dPos = PVector.mult(m["normal"], max(m["penetration"]-.01, 0) / (a.invMass + b.invMass) * 2.).mult(ratio)
            # a.element.x += dPos.x
            # a.element.y += dPos.y
            ratio = b.mass / massSum
            b.vel.add(PVector.mult(impulse, ratio))
            # dPos = PVector.mult(m["normal"], max(m["penetration"]-.01, 0) / (a.invMass + b.invMass) * 2.).mult(ratio)
            # b.element.x += dPos.x
            # b.element.y += dPos.y

            # correction
            c = PVector.mult(m["normal"], max(m["penetration"]-.01, 0) / (a.invMass + b.invMass) * 0.2)
            ca = PVector.mult(c, a.invMass)
            cb = PVector.mult(c, b.invMass)
            a.element.x -= ca.x
            a.element.y -= ca.y
            b.element.x += cb.x
            b.element.y += cb.y

    def calcCollision(self, a, b):
        m = {"collides": False}

        aPos = PVector.add(PVector(a.element.x, a.element.y), a.shape.pos)
        bPos = PVector.add(PVector(b.element.x, b.element.y), b.shape.pos)

        if type(a.shape) == Circle:
            if type(b.shape) == Circle:
                raise NotImplementedError
            elif type(b.shape) == Rect:
                raise NotImplementedError
        else:
            if type(b.shape) == Rect:
                # m["collides"] = s.x + self.shape.width >= o.x and s.x <= o.x + other.shape.width and s.y + self.shape.height >= o.y and s.y <= o.y + other.shape.height
                
                n = PVector.sub(bPos, aPos)
                
                xOverlap = a.shape.width/2 + b.shape.width/2 - abs(n.x)
                
                if xOverlap > 0:
                    yOverlap = a.shape.height/2 + b.shape.height/2 - abs(n.y)
                    if yOverlap > 0:
                        if xOverlap < yOverlap:
                            if n.x < 0:
                                m["normal"] = PVector(1, 0)
                            else:
                                m["normal"] = PVector(-1, 0)
                            m["penetration"] = xOverlap
                            m["collides"] = True
                        else:
                            if n.y < 0:
                                m["normal"] = PVector(0, -1)
                            else:
                                m["normal"] = PVector(0, 1)
                            m["penetration"] = yOverlap
                            m["collides"] = True
            else:
                # m["collides"] = other.collides(self)
                raise NotImplementedError
        return m
