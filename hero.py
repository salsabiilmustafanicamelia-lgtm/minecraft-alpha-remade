# напиши свой код здесь (napishi svoy kod zdes')
class Hero():
    def __init__(self, pos, land):
        self.mode = True
        self.land = land
        self.hero = loader.loadModel('smiley')
        self.hero.setColor(1, 1, 0, 1)
        self.hero.setScale(0.3)
        self.hero.setPos(pos)
        self.hero.reparentTo(render)
        self.cameraBind()
        self.accept_events()

        # ==== Camera Section Start

    def cameraBind(self): #POV 1st person Hero
        base.disableMouse()
        base.camera.setH(180)
        base.camera.reparentTo(self.hero)
        base.camera.setPos(0, 0, 1.5)
        self.cameraOn = True

    def cameraUp(self): #POV 3rd person Hero (or spectator mode)
        pos = self.hero.getPos()
        base.mouseInterfaceNode.setPos(-pos[0], -pos[1], -pos[2]-3)
        base.camera.reparentTo(render)
        base.enableMouse()
        self.cameraOn = False

    def changeView(self):
        if self.cameraOn:
            self.cameraUp()
        else:
            self.cameraBind()

    # ==== Camera Section End


    # ==== Rotation Section Start

    def turn_left(self):
        self.hero.setH((self.hero.getH() + 5) % 360)

    def turn_right(self):
        self.hero.setH((self.hero.getH() - 5) % 360)

    # ==== Rotation Section End


    # ==== Direction Check Section Start
    def look_at(self, angle):
        x_from = round(self.hero.getX())
        y_from = round(self.hero.getY())
        z_from = round(self.hero.getZ())

        dx, dy = self.check_dir(angle)
        x_to = x_from + dx
        y_to = y_from + dy
        return x_to, y_to, z_from

    def check_dir(self, angle):
        if angle >= 0 and angle <= 20:
            return (0, -1)
        elif angle <= 65:
            return (1, -1)
        elif angle <= 110:
            return (1, 0)
        elif angle <= 155:
            return (1, 1)
        elif angle <= 200:
            return (0, 1)
        elif angle <= 245:
            return (-1, 1)
        elif angle <= 290:
            return (-1, 0)
        elif angle <= 335:
            return (-1, -1)
        else:
            return (0, -1)

    # ==== Direction Check Section End


    # ==== Movement Section Start

    def just_move(self, angle): #Movement for 3rd person
        pos = self.look_at(angle)
        self.hero.setPos(pos)

    def try_move(self, angle): #Movement for 1st person
        pos = self.look_at(angle)
        if self.land.isEmpty(pos):
            #Going down a block
            pos = self.land.findHighestEmpty(pos)
            self.hero.setPos(pos)
        else:
            #GOing up a block
            pos = pos[0], pos[1], pos[2] + 1
            if self.land.isEmpty(pos):
                self.hero.setPos(pos)

    def changeMode(self):
        if self.mode:
            self.mode = False
        else:
            self.mode = True

    def move_to(self, angle): #Switch mode movement
        if self.mode:
            self.just_move(angle)
        else:
            self.try_move(angle)
    # ==== Movement Section End


    # ==== Movement Direction Section Start
    def forward(self):
        angle = self.hero.getH() % 360
        self.move_to(angle)

    def back(self):
        angle = (self.hero.getH() + 180) % 360
        self.move_to(angle)

    def left(self):
        angle = (self.hero.getH() + 90) % 360
        self.move_to(angle)

    def right(self):
        angle = (self.hero.getH() + 270) % 360
        self.move_to(angle)

    def up(self):
        if self.mode:
            self.hero.setZ(self.hero.getZ() + 1)

    def down(self):
        if self.mode and self.hero.getZ() > 1:
            self.hero.setZ(self.hero.getZ() - 1)

    #Arrow key = arrow_up, arrow_down, arrow_left, arrow_right

    # ==== Movement Direction Section End


    # ==== Map Manipulation Section Start

    def build(self):
        angle = self.hero.getH() % 360
        pos = self.look_at(angle)
        if self.mode:
            self.land.addBlock(pos) #Spectator
        else:
            self.land.buildBlock(pos) #First Person

    def destroy(self):
        angle = self.hero.getH() % 360
        pos = self.look_at(angle)
        if self.mode:
            self.land.delBlock(pos) #Spectator
        else:
            self.land.delBlockFrom(pos) #First Person

    # ==== Map Manipulation Section Start

    def accept_events(self):
        base.accept('v', self.changeView) #Change camera view

        base.accept('z', self.changeMode)

        base.accept('n', self.turn_left)
        base.accept('n' + '-repeat', self.turn_left)
        base.accept('m', self.turn_right)
        base.accept('m' + '-repeat', self.turn_right)

        base.accept('a', self.left)
        base.accept('a' + '-repeat', self.left)

        base.accept('s', self.back)
        base.accept('s' + '-repeat', self.back)

        base.accept('d', self.right)
        base.accept('d' + '-repeat', self.right)

        base.accept('w', self.forward)
        base.accept('w' + '-repeat', self.forward)

        base.accept('q', self.up)
        base.accept('q' + '-repeat', self.up)

        base.accept('e', self.down)
        base.accept('e' + '-repeat', self.down)

        base.accept('j', self.build)
        base.accept('k', self.destroy)

        base.accept('o', self.land.saveMap)
        base.accept('p', self.land.loadMap)