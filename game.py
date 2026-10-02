#write here a code for main window of the game
from panda3d.core import AmbientLight, VBase4
from direct.showbase.ShowBase import ShowBase
from mapmanager import MapManager
from hero import Hero

class Game(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.land = MapManager()

        # self.model = loader.loadModel('Boeing707.egg')
        # self.model.setTexture(loader.loadTexture("BoeingTexture.tif"))
        # self.model.reparentTo(render)
        # self.model.setScale(0.1)
        # self.model.setPos(0, 25, 0)
        x, y = self.land.loadLand("landcustom.txt")
        self.hero = Hero((x//2, y//2,3), self.land)
        base.camLens.setFov(90)

        alight = AmbientLight('alight')
        alight.set_color(VBase4(1, 1, 1, 1))
        alnp = self.render.attach_new_node(alight)
        self.render.set_light(alnp)


game = Game()
game.run()