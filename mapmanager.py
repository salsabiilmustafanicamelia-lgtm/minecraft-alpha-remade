# write the code for creating and managing the map here
# напиши здесь код создания и управления картой
from panda3d.core import LoaderOptions
import os
import pickle

class MapManager:
    def __init__(self):
        self.model = 'block.egg'
        self.texture = (
            'stone.png',
            'sand.png',
            'grass.jpg'
            )
        # self.color = (0.4, 0.2, 0.56, 1) #rgba

        self.colors = [
            (0.5, 0.6, 0.7, 1),
            (0.5, 0.5, 0.4, 1),
            (0.25, 0.5, 0.3, 1),
            (0.3, 0.55, 0.35, 1),
            (0.35, 0.60, 0.4, 1)
        ]

        self.startNew()

        # self.addBlock((0, 10, 5))
        # self.addBlock((1, 10, 5))
        # self.addBlock((2, 10, 5))

    def getColor(self, z):
        if z < len(self.colors):
            return self.colors[z]
        else:
            return self.colors[len(self.colors)-1]

    def getTexture(self, z):
        if z < len(self.texture):
            return self.texture[z]
        else:
            return self.texture[len(self.texture)-1]

    def loadTextureSafe(self, filename):
        if not os.path.exists(filename):
            return None
        try:
            return loader.loadTexture(filename)
        except Exception:
            return None

    def startNew(self):
        self.land = render.attachNewNode('Land')

    def addBlock(self, position):
        self.block = loader.loadModel(self.model)
        self.block.setPos(position)

        texture = self.loadTextureSafe(self.getTexture(int(position[2])))
        if texture is not None:
            self.block.setTexture(texture)

        self.color = self.getColor(int(position[2]))
        self.block.setColor(self.color)
        self.block.setTag("at", str(position))
        self.block.reparentTo(self.land)

    def clear(self):
        self.land.removeNode()
        self.startNew()

    def loadLand(self, filename):
        self.clear()
        self.skybox = loader.loadModel('skybox.egg')
        texture = self.loadTextureSafe('skybox.jpg')
        if texture is not None:
            self.skybox.setTexture(texture)
        self.skybox.setScale(2000)
        self.skybox.setPos(22, 22, 0)
        self.skybox.reparentTo(render)

        with open(filename) as file:
            y = 0 
            for line in file: #mengakses stiap baris
                x = 0
                line = line.split(' ') #berhasil mengakses
                for z in line:
                    for z0 in range(int(z)+1):
                        blok = self.addBlock((x, y, z0))
                    x += 1
                y += 1
        return x, y

    def findBlocks(self, pos):
        return self.land.findAllMatches("=at=" + str(pos))

    def isEmpty(self, pos): #Check block empty or not
        blocks = self.findBlocks(pos)
        if blocks:
            return False
        else:
            return True

    def findHighestEmpty(self, pos):
        x, y, z = pos
        z = 1
        while not self.isEmpty((x, y, z)):
            z += 1
        return (x, y, z)

    def buildBlock(self, pos):
        x, y, z = pos
        new = self.findHighestEmpty(pos)
        if new[2] <= z + 1:
            self.addBlock(new)

    def delBlock(self, position): #Mode player = True
        blocks = self.findBlocks(position)
        for block in blocks:
            block.removeNode()

    def delBlockFrom(self, position):
        x, y, z = self.findHighestEmpty(position) #Mode player = False
        pos = x, y, z-1
        for block in self.findBlocks(pos):
            block.removeNode()

    def saveMap(self):
        blocks = self.land.getChildren() 
        with open('my_map.dat', 'wb') as file_out:
            #Saving amount of blocks
            pickle.dump(len(blocks), file_out)

            #Reading per block
            for block in blocks:
                #To remember position
                x, y, z = block.getPos()
                pos = (int(x), int(y), int(z))
                pickle.dump(pos, file_out)

    def loadMap(self):
        #reset
        self.clear()

        #Open file to read
        with open('my_map.dat', 'rb') as file_in:
            #Read amount of existing blocks
            length = pickle.load(file_in)

            for i in range(length):
                #Read position
                pos = pickle.load(file_in)

                #Make new block
                self.addBlock(pos)