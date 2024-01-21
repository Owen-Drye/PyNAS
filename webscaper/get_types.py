from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

dict = {}
web_driver = webdriver.Firefox()
web_driver.get("https://support.microsoft.com/en-us/windows/common-file-name-extensions-in-windows-da4a4430-8e76-89c5-59f7-1cdbbc75cb01")
rows = web_driver.find_elements(By.TAG_NAME, 'tr')

for row in rows:
    values = row.find_elements(By.XPATH, '*')
    for extension in values[0].find_element(By.XPATH, '*').text.split(','):
        dict[extension] = values[1].find_element(By.XPATH, '*').text


print(dict)

