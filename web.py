from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome()
driver.get("chrome://dino")
assert "chrome://dino" in driver.title

elem = driver.find_element_by_tag_name("body")
elem.send_keys(Keys.ARROW_UP)

driver.execute_script("Runner.instance_.play()")
driver.execute_script("Runner.instance_.restart()")

while True:
    if driver.execute_script("return Runner.instance_.crashed"):
        driver.execute_script("Runner.instance_.restart()")
driver.close()