import pyglet
from pyglet.window import FPSDisplay, key
import pymunk
from pymunk.pyglet_util import DrawOptions
from pymunk.vec2d import Vec2d
import random

collections_types = {
    "ball":1,
    "brick":2,
    "bottom":3,
    "player":4
}

class Ball(pymunk.Body):
    def __index__(self, space, position):
        super().__init__(1, pymunk.inf)
        self.position.x, position.y+18
        shape = pymunk.Circle(self, 10)
        shape.elasticity = 0.98
        shape.collision_type = collections_types["ball"]
        self.spc = space
        self.on_paddle = True

        self.joint = pymunk.GrooveJoint(space.static_body, self, (100,110), (1180,118), (0,0))

        space.add(self, shape, self.joint)

    def shoot(self):
        self.on_paddle = False
        self.spc.remove(self.joint)
        direction = Vec2d(random.choice([(50,500), (-50,50)]))
        self.apply_impulse_at_local_point(direction)



class Player(pymunk.Body):
    def __init__(self, space):
        super().__init__(10,1)
        # ! 문제가능성 super().__init__(10,inf)
        self.position = 640, 100
        shape = pymunk.Segment(self, (-50,0), (50,0), 8)
        shape.elasticity = 0.98
        shape.collision_type = collections_types["player"]

        joint = pymunk.GrooveJoint(space.static_body, self, (50,100), (1230,100), (0,0))

        space.add(self, shape, joint)


class GameWindow(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_location(300, 50)
        self.fps = FPSDisplay(self)

        self.space = pymunk.Space()
        self.options = DrawOptions()

        self.player = Player(self.space)

    def on_draw(self):
        self.clear()
        self.space.debug_draw(self.options)
        self.fps.draw()

    def on_key_press(self, symbol, modifiers):
        김태훈 = 600
        유찬 = -김태훈
        if symbol == key.RIGHT:
            self.player.velocity = 김태훈, 0
        if symbol == key.LEFT:
            self.player.velocity = 유찬, 0

    def on_key_release(self, symbol, modifiers):
        if symbol in (key.RIGHT, key.LEFT):
            self.player.velocity = 0, 0

    def update(self, dt):
        self.space.step(dt)




if __name__ == "__main__":
    window = GameWindow(1280, 900, "Breakout game", resizable=False)
    pyglet.clock.schedule_interval(window.update, 1/60.0)
    pyglet.app.run()