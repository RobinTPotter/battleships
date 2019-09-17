from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time 
from config import Config
import threading

class Test(threading.Thread):        
    def run(self):
        time.sleep(5)

        options = Options()

        player1 = webdriver.Chrome(options=options, executable_path=Config.CHROME_DRIVER)
        player1.get("http://localhost:{0}".format(Config.PORT))        
        player1.find_element_by_link_text('Login').click()
        username = player1.find_element_by_id('username')
        username.send_keys('robin')
        player1.find_element_by_id('submit').click()      
        join = player1.find_element_by_link_text('join!')
        join.click()
        
        player2 = webdriver.Chrome(options=options, executable_path=Config.CHROME_DRIVER)
        player2.get("http://localhost:{0}".format(Config.PORT))     
        player2.find_element_by_link_text('Login').click()
        username = player2.find_element_by_id('username')
        username.send_keys('nobby')
        player2.find_element_by_id('submit').click()
        join = player2.find_element_by_link_text('join!')
        join.click()
        