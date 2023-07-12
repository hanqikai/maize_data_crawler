import requests
from lxml import etree
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.common.exceptions import TimeoutException 


def get_browser():
    chrome_options = webdriver.ChromeOptions()
    #chrome_options.add_argument('--headless')
    chrome_options.add_argument('--ignore-certificate-errors')    # 忽略证书错误
    # 忽略 Bluetooth: bluetooth_adapter_winrt.cc:1075 Getting Default Adapter failed. 错误
    chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
    # 忽略 DevTools listening on ws://127.0.0.1... 提示
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    browser = webdriver.Chrome(options=chrome_options)
    return browser

def get_content(url):
    print(f"正在处理: {url}")
    browser = get_browser()
    browser.set_page_load_timeout(100)
    browser.implicitly_wait(100)
    try:
        browser.get(url)
    except TimeoutException:
        print(f"Page---{url}--- load time out but we keep going!")
        pass
    time.sleep(10)
    question = browser.find_element(By.XPATH, '//*[@id="index_ques"]/h6').text
    img_list = []
    img_elements = browser.find_elements(By.XPATH, '//*[@id="index_ques"]/ul/li/a/img')
    for img in img_elements:
        src = img.get_attribute('src')
        src = src.replace("small/", '')
        img_list.append(src)
    people_info = browser.find_element(By.XPATH, '//*[@id="index_ques"]/p/span[1]/b').text
    time_ = browser.find_element(By.XPATH, '//*[@id="index_ques"]/p/span[3]').text
    loc = browser.find_element(By.XPATH, '//*[@id="index_ques"]/p/span[2]').text
    info = {"people": people_info, "time": time_, "location": loc}
    all_ans = []
    answers = browser.find_elements(By.XPATH, '//*[@id="index_replys"]/div/div[1]/p')
    for ans in answers:
        all_ans.append(ans.text)
    browser.quit()
    return question, all_ans, img_list.copy(), info

def get_all_url(url, page, key_words):
        browser = get_browser()
        browser.set_page_load_timeout(100)
        browser.implicitly_wait(100)
        try:
            browser.get(url)
        except TimeoutException:
            print(f"Page---{url}--- load timed out but we keep going!")
            pass
        input_element = browser.find_element(By.XPATH, '//*[@id="text_keywords"]')
        input_element.clear()
        input_element.send_keys(key_words)
        button = browser.find_element(By.XPATH, '//*[@id="formId"]/div[1]/div/div[1]/button')
        button.click()
        time.sleep(10)
        page_info = browser.find_element(By.XPATH, '//*[@id="formId"]/div[2]/div/div[4]/div/ul/li[3]').text
        p1, p2 = page_info.split('/')
        p1, p2 = int(p1[3:]), int(p2)
        for p in range(page, p2 + 1):
            try:
                print(f"正在运行第{p}页...")
                if p == page:
                    input_element = browser.find_element(By.XPATH, '//*[@id="pageValue"]')
                    input_element.clear()
                    input_element.send_keys(f"{page}")
                    button = browser.find_element(By.XPATH, '//*[@id="formId"]/div[2]/div/div[4]/div/ul/li[6]/a')
                    button.click()
                    time.sleep(20)
                url_list = []
                for i in range(1, 21):
                    image_element = browser.find_element(By.XPATH,  f'//*[@id="njwd_main_box_left_img_list"]/div[{i}]/h6/a').get_attribute("href")
                    time.sleep(1.8)
                    url_list.append(image_element)
                if p == 1: browser.find_element(By.XPATH, '//*[@id="formId"]/div[2]/div/div[4]/div/ul/li[4]/a').click()
                else: browser.find_element(By.XPATH, '//*[@id="formId"]/div[2]/div/div[4]/div/ul/li[6]/a').click()
                time.sleep(10)
                f = open(f"njtg_url_list_{key_words}.txt", mode='a+', encoding='utf-8')
                for cur_url in url_list:
                    f.writelines(cur_url + '\n')
                f.close()
            except Exception as e:
                print(f"出错了，运行到了第{p}页...")
                print(e)
                browser.quit()
                return p
        browser.quit()


if __name__ == "__main__":
    page = 0
    key_words = "玉米病害"
    for _ in range(1000):
        a = get_all_url("http://njtg.nercita.org.cn/tech/question/list.shtml?code=0", page, key_words=key_words)
        page = a
