from selenium import webdriver
import os
# https://sites.google.com/a/chromium.org/chromedriver/downloads
# https://beomi.github.io/2017/09/28/HowToMakeWebCrawler-Headless-Chrome/

options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument('headless')
options.add_argument('window-size=1920x1080')

driver = webdriver.Chrome(os.getcwd()+'\\chromedriver.exe', chrome_options=options)
TEST_URL = 'https://intoli.com/blog/making-chrome-headless-undetectable/chrome-headless-test.html'
driver.get(TEST_URL)
driver.execute_script("Object.defineProperty(navigator, 'plugins', {get: function() {return[1, 2, 3, 4, 5]}})")
# lanuages 속성을 업데이트해주기
driver.execute_script("Object.defineProperty(navigator, 'languages', {get: function() {return ['ko-KR', 'ko']}})")

user_agent = driver.find_element_by_css_selector('#user-agent').text
plugins_length = driver.find_element_by_css_selector('#plugins-length').text
languages = driver.find_element_by_css_selector('#languages').text

print('User-Agent: ', user_agent)
print('Plugin length: ', plugins_length)
print('languages: ', languages)

driver.quit()

# driver.get('http://naver.com')
# driver.implicitly_wait(3)

# driver.get_screenshot_as_file('naver_main.png')

# driver.quit()