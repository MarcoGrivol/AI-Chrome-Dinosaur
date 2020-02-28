from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

class Game:
    def __init__(self):
        self._driver = webdriver.Chrome()
        self._element = self._driver.find_element_by_tag_name("body")
       
        self._currentSpeed = 0
        self.score = 0
        self._obstaclesCount = 0
        self._distance = 0

        self._start()
    
    def _start(self):
        self._driver.get("chrome://dino")
        assert "chrome://dino" in self._driver.title
        # the main part of the algorithm only starts after the first chrash of the game
        # it should be manually triggered   
        # self._driver.execute_script(init_script)
        while not self._driver.execute_script("return Runner.instance_.crashed"):
            pass

    def _restart(self):
        self._driver.execute_script("Runner.instance_.restart()")
    
    def _getData(self):
        self._currentSpeed = self._driver.execute_script("return Runner.instance_.currentSpeed")
        self._score = self._driver.execute_script("return Runner.instance_.distanceMeter.digits")
        self._score = ''.join(self._score)
        self._obstaclesCount = self._driver.execute_script("return Runner.instance_.horizon.obstacles")
        
        obstacleXPos = self._driver.execute_script("return Runner.instance_.horizon.obstacles[0].xPos")
        dinoXPos = self._driver.execute_script("return Runner.instance_.tRex.config.WIDTH")

        self._distance = obstacleXPos - dinoXPos

    def play(self):
        while True:
            self._restart()
            while not self._driver.execute_script("return Runner.instance_.crashed"):
                try:
                    self._getData()
                    print(self._distance, self._currentSpeed)
                except:
                    pass

jogo = Game()
jogo.play()