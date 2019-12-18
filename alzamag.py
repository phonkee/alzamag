"""
@author 'Peter Vrba <phonkee@phonkee.eu>'
"""
import json
import time

import click
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class Magazine:
    name = None
    last_update = None
    image = None
    issues = None


class MagazineIssue:
    id = None
    impage = None


@click.command()
@click.option('--count', default=1, help='number of greetings')
@click.option('--email', required=True, help='alza.cz email')
@click.option('--target', default=".", help='target directory')
@click.password_option('--password', required=True, help='alza.cz password')
def update(count, email, password, target):
    """Update magazines"""
    print("target", target)
    print("hello", count, email, password)
    driver = webdriver.Firefox()
    driver.get("http://alza.cz")
    python_button = driver.find_elements_by_xpath("//*[@id='lblLogin']")[0]
    python_button.click()

    time.sleep(1)
    name = driver.find_elements_by_xpath("//*[@id='i_name']")[0]
    name.send_keys(Keys.BACKSPACE)
    name.send_keys(email)

    pwd = driver.find_elements_by_xpath("//*[@id='i_psw']")[0]
    pwd.send_keys(Keys.BACKSPACE)
    pwd.send_keys(password)

    driver.find_elements_by_xpath("//*[@id='btnLogin']")[0].click()
    time.sleep(2)

    driver.get("https://www.alza.cz/muj-ucet/casopisy.htm")

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'item')))

    # blockMagazines
    # .item
    #   .item.img
    #   c1.inner - name
    #   c2.last - last date

    for item in driver.find_elements_by_css_selector("#blockMagazines .item"):
        mag = Magazine()
        mag.name = item.find_element_by_css_selector(".c1").get_attribute('innerHTML')
        mag.last_update = item.find_element_by_css_selector(".c2").get_attribute('innerHTML')
        mag.image = item.find_element_by_css_selector("img").get_attribute('src')
        item.click()
        name = "#blockMagazines .detail .c{}".format(item.get_attribute("data-column"))

        WebDriverWait(driver, 10).until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, name)))

        all_of_em = driver.find_elements_by_css_selector(name)
        print(all_of_em)

        # detItemInline
        print(json.dumps(mag.__dict__))

        time.sleep(1)

    # after click .magDetailGrid
    # item in detail grid .detItemInline (data-id="2172116")
    # paging - class="pgn"

    time.sleep(100)
    driver.close()


if __name__ == "__main__":
    update()
