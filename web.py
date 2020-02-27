from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

# driver = webdriver.Chrome()
# driver.get("chrome://dino")
# assert "chrome://dino" in driver.title

# # play the game till it crashes then restart and play
# while not driver.execute_script("return Runner.instance_.crashed"):
#     pass

# driver.execute_script("Runner.instance_.restart()")

# element = driver.find_element_by_tag_name("body")
# element.send_keys(Keys.ARROW_UP)

# while True:
#     pass

# driver.close()
init_script = "document.getElementsByClassName('runner-canvas')[0].id = 'runner-canvas';" \
              "setInterval(function (){Runner.instance_.tRex.xPos = 0}, 500);" \
              "setInterval(function (){Runner.instance_.tRex.xInitialPos = 0}, 500);"
class Game:
    def __init__(self):
        self._driver = webdriver.Chrome()
        self.element = self._driver.find_element_by_tag_name("body")

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
        data = self._driver.execute_script("return Runner.instance_.")


    def play(self):
        self._restart()
        while not self._driver.execute_script("return Runner.instance_.crashed"):
            try:
                pos = self._driver.execute_script("return Runner.instance_.horizon.obstacles[0].xPos")
                dino = self._driver.execute_script("return Runner.instance_.tRex.config.WIDTH")
                offset = self._driver.execute_script("return Runner.instance_.tRex.xPos")
                print(pos - dino)
            except:
                pass

jogo = Game()
jogo.play()