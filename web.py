from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

class Game:
    def __init__(self):
        self._currentSpeed = 0
        self._score = 0
        self._obstacleYPos = 0
        self._obstaclesCount = 0
        self._distance = 0
        self._isJumping = 0

        self._driver = webdriver.Chrome()
        self._start()
        self._element = self._driver.find_element_by_tag_name("body")
    
    def _start(self):
        self._driver.get("chrome://dino")
        assert "chrome://dino" in self._driver.title
        # the main part of the algorithm only starts after the first chrash of the game
        # it should be manually triggered   
        # self._driver.execute_script(init_script)
        while not self._driver.execute_script("return Runner.instance_.crashed"):
            pass

    def _pause(self):
        self._driver.execute_script("Runner.instance_.pause()")

    def _restart(self):
        self._driver.execute_script("Runner.instance_.restart()")

    # ducking will not work properly unless the down arrow is hold
    # this can be simulated with the following script
    def _duck(self, isDucking):
        if isDucking:
            self._driver.execute_script("Runner.instance_.tRex.update(0, Trex.status.DUCKING)")
            self._driver.execute_script("Runner.instance_.tRex.ducking = true")
        else:
            self._driver.execute_script("Runner.instance_.tRex.update(0, Trex.status.RUNNING)")
            self._driver.execute_script("Runner.instance_.tRex.ducking = false")

    def _jump(self):
        self._element.send_keys(Keys.ARROW_UP)

    def _doNothing(self):
        pass

    def endSession(self):
        self._driver.close()
    
    def _updateData(self):
        self._currentSpeed = self._driver.execute_script("return Runner.instance_.currentSpeed")
        self._score = self._driver.execute_script("return Runner.instance_.distanceMeter.digits")
        self._score = float(''.join(self._score))
        self._obstaclesCount = self._driver.execute_script("return Runner.instance_.horizon.obstacles")
        self._obstaclesCount = float(len(self._obstaclesCount))
        self._isJumping = float(self._driver.execute_script("return Runner.instance_.tRex.jumping"))
        # if there is no object ignore error
        try:
            obstacleXPos = self._driver.execute_script("return Runner.instance_.horizon.obstacles[0].xPos")
            dinoXPos = self._driver.execute_script("return Runner.instance_.tRex.config.WIDTH")
            self._distance = obstacleXPos - dinoXPos
            # 100 is the ground
            self._obstacleYPos = self._driver.execute_script("return Runner.instance_.horizon.obstacles[0].yPos")
            self._obstaclesYPos = 100 - self._obstacleYPos
        except:
            self._distance = 800
            self._obstacleYPos = 0

    def _dataAsArray(self):
        output = []
        output.append([self._currentSpeed])
        output.append([self._obstacleYPos])
        output.append([self._obstaclesCount])
        output.append([self._isJumping])
        output.append([self._distance])
        return output

    # executes the game until it crashes and return the score
    def play(self, brain):
        isDucking = False
        self._restart()
        while not self._driver.execute_script("return Runner.instance_.crashed"):
            self._updateData()
            gameData = self._dataAsArray()
            output = brain.runInputs(gameData)
            # x < -0.1 duck
            # -0.1 <= x <= 0.1 do nothing
            # x > 0.1 jump
            # print(gameData, output, isDucking, self._isJumping())
            # print("-----------------------------------------------------------------------")
            if output > 0.2:
                if isDucking:
                    isDucking = False
                    self._duck(isDucking)
                self._jump()
            elif output < -0.2:
                # only call duck if a state is changed and not in mid air
                if not isDucking and not self._isJumping:
                    isDucking = True
                    self._duck(isDucking)
            else:
                if isDucking:
                    isDucking = False
                    self._duck(isDucking)

        self._updateData()
        return self._score

if __name__ == "__main__":
    from brain import Brain
    layers = [5, 8, 1]
    brain = Brain(layers)

    jogo = Game()
    data = jogo.play(brain)
    print(data)
    jogo.endSession()
