from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from twilio.rest import Client 

def purchase(username, password):
    browser = webdriver.Firefox()
    browser.get('https://www.walmart.com/account/login?tid=0&returnUrl=%2F')
    
    #Login
    login(browser, username, password)

    #Get Item URL https://www.walmart.com/ip/PlayStation-5-Console/363472942
    browser.get('https://www.walmart.com/ip/Mainstays-Wood-14-Jumbo-Head-Spoon/45081846')
    
    #Add to Cart
    wait_for_Add_to_cart_button(browser)
    send_sms()

    #Checkout
    WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, 
    '/html/body/div[1]/div/div/div/div/div/div[1]/div/div[1]/div/div[2]/div/div/div/div/div[3]/div/div/div[2]/div/div[2]/div/button[1]/span'))).click()


def login(browser, username, password):
    browser.find_element_by_xpath(
        '//*[@id="email"]').send_keys(username + Keys.RETURN)
    browser.find_element_by_xpath(
        '//*[@id="password"]').send_keys(password + Keys.RETURN)

def wait_for_Add_to_cart_button(browser):
    while True:
        try:
            addToCartButton = browser.find_element_by_xpath('//*[@id="add-on-atc-container"]/div[1]/section/div[1]/div[3]/button/span/span')
            break
        except NoSuchElementException:
            browser.refresh()
            continue

    addToCartButton.click()

def send_sms():
    account_sid = '${account_sid}'
    auth_token = '${auth_token}'
    client = Client(account_sid, auth_token)

    message = client.messages \
                    .create(
                        body="${message_body}",
                        from_='${from_phone_number}',
                        to='${to_phone_number}'
                    )
    print(message.sid)

purchase('${user_name}','${password}')