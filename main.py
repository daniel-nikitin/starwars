from random import choice, randint

import arcade

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
SCREEN_TITLE = 'WWDW'


class Flcn(arcade.Sprite):
    def __init__(self):
        super().__init__(filename="flcn0.png", scale=0.7)
        self.picture0 = arcade.load_texture("flcn0.png")
        self.picture1 = arcade.load_texture("flcn1.png")
        self.picture2 = arcade.load_texture("flcn2.png")

    def change_skin(self):
        self.texture = choice([self.picture0, self.picture1, self.picture2])


class Laser(arcade.Sprite):
    def __init__(self):
        super().__init__(filename="laser.png", scale=1)
        self.center_x = window.flcn.center_x
        self.center_y = window.flcn.center_y
        self.change_y = 10
    def laser_limit(self):
        if self.bottom > 700:
            self.kill()
    def update(self):
        self.move()
        self.laser_limit()


    def move(self):
        self.center_y += self.change_y

class Tiefighters(arcade.Sprite):
    def __init__(self):
        super().__init__(filename="other/big1.png",scale= 0.7)

    def update(self):
        self.move()

    def move(self):
        self.center_y += self.change_y


class Meteorite(arcade.Sprite):
    def __init__(self):

        super().__init__(filename="meteorit.png")
        self.spawn()

    def move(self):
        self.center_y -= self.change_y
        if self.top < 0:
            self.spawn()

    def spawn(self):
        self.bottom = SCREEN_HEIGHT
        self.change_y = randint(1, 10)
        self.center_x = randint(0, SCREEN_WIDTH)


class Game(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.lasers = arcade.SpriteList()
        self.pressed_mouse = False
        self.set_mouse_visible(False)
        self.flcn = Flcn()
        self.flcn.center_x = 1
        self.flcn.center_y = 90
        self.pause_image = arcade.load_texture("other/PAUSE.png")
        self.pause = False
        self.bg = arcade.load_texture("background.jpg")
        self.bg2 = arcade.load_texture("other/space_background_2.png")
        self.meteorite = Meteorite()
        self.tie_list = arcade.SpriteList()
        self.tiefighters_spawn()
        self.space = arcade.load_sound("laser.wav")
        #self.loud_music = arcade.load_sound("new hope")
    def tiefighters_spawn(self):
        for i in range(500):
            tiefighter = Tiefighters()
            tiefighter.center_y = 700+100*i
            tiefighter.change_y = -10
            tiefighter.center_x = randint(0 ,1000)
            self.tie_list.append(tiefighter)


    def on_mouse_motion(self, x, y, dx, dy):
        if self.pause == True:
            return
        self.flcn.center_x = x

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.pressed_mouse = True
            laser = Laser()
            arcade.play_sound(self.space)
            self.lasers.append(laser)

    def on_mouse_release(self, x: int, y: int, button: int, modifiers: int):
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.pressed_mouse = False
    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.ESCAPE:
            self.pause = not self.pause
        if self.pause == True:
            return
        if symbol == arcade.key.R:
            self.flcn.change_skin()
        if symbol == arcade.key.SPACE :
            arcade.play_sound(self.space)
            laser = Laser()
            self.lasers.append(laser)
    def on_key_release(self, symbol: int, modifiers: int):
        pass

    def on_draw(self):
        self.clear()
        arcade.draw_texture_rectangle(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, SCREEN_WIDTH, SCREEN_HEIGHT, self.bg)
        arcade.draw_texture_rectangle(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, SCREEN_WIDTH, SCREEN_HEIGHT, self.bg2)
        self.flcn.draw()
        self.meteorite.draw()
        self.lasers.draw()
        if self.pause == True:
            arcade.draw_texture_rectangle(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, self.pause_image.width / 2,
                                          self.pause_image.height / 2, self.pause_image)
        self.tie_list.draw()

    def update(self, delta_time: float):
        if self.pause == True:
            return
        self.lasers.update()
        self.tie_list.update()
        self.meteorite.move()
        if self.pressed_mouse == True:

            laser = Laser()
            arcade.play_sound(self.space)
            self.lasers.append(laser)
        for laser in self.lasers:
            hitbox = arcade.check_for_collision_with_list(laser, self.tie_list)
            if len(hitbox) > 0:
                laser.kill()

                for enemy in hitbox:
                    enemy.kill()
window = Game(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
arcade.run()
