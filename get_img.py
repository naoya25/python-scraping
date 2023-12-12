from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.webdriver import WebDriver
from bs4 import BeautifulSoup
from time import sleep
import urllib.request
import os


def main():
    driver = webdriver.Chrome()
    isLogin = do_login(driver=driver)
    if not isLogin:
        return "Login faild."

    tag_name = "dog"
    save_images(driver=driver, tag_name=tag_name)

    sleep(10)
    driver.close()
    return "Finish All!"


def do_login(driver: WebDriver) -> bool:
    driver.get("https://www.instagram.com/")

    try:
        driver.implicitly_wait(30)
        id_elem = driver.find_element(By.NAME, "username")
        pass_elem = driver.find_element(By.NAME, "password")
        login_btn = driver.find_element(By.XPATH, '//*[@id="loginForm"]/div/div[3]/button')

        id_elem.send_keys("******")
        pass_elem.send_keys("******")
        login_btn.click()
        sleep(10)
    except Exception as e:
        print(f"Error: {e}")
        return False

    return True


def save_images(driver: WebDriver, tag_name: str) -> None:
    driver.get(f"https://www.instagram.com/explore/tags/{tag_name}")
    driver.implicitly_wait(30)
    sleep(30)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    driver.implicitly_wait(30)
    sleep(5)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    img_tags = soup.find_all("img")

    os.makedirs("images", exist_ok=True)
    for i, img in enumerate(img_tags):
        img_url = img["src"]
        img_name = f"image_{i}.png"

        urllib.request.urlretrieve(img_url, os.path.join("images", img_name))
        print(f"Image saved: {img_name}")


if __name__ == "__main__":
    print(main())
