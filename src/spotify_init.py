import os
import spotipy
import time
from spotipy import oauth2
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By


def chrome():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--window-size=1420,1080')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(chrome_options=chrome_options)
    return driver


def spotify_login(browser, email, password):
    email_input = browser.find_element_by_id('login-username')
    password_input = browser.find_element_by_id('login-password')
    login_button = browser.find_element_by_id('login-button')
    email_input.send_keys(email)
    password_input.send_keys(password)
    login_button.click()
    time.sleep(3)


def spotify_accept(browser):
    try:
        confirmation = browser.find_element(
            By.XPATH, '//button[text()="OKAY"]')
        confirmation.click()
    except NoSuchElementException:
        pass
    time.sleep(3)


def spotify(scope):
    client_id = os.getenv('SPOTIPY_CLIENT_ID')
    client_secret = os.getenv('SPOTIPY_CLIENT_SECRET')
    redirect_uri = os.getenv('SPOTIPY_REDIRECT_URI')
    email = os.getenv('OSP_EMAIL')
    password = os.getenv('OSP_PASSWORD')

    if not client_id:
        raise spotipy.SpotifyException(550, -1, 'no credentials set')

    sp_oauth = oauth2.SpotifyOAuth(
        client_id,
        client_secret,
        redirect_uri,
        scope=scope)
    auth_url = sp_oauth.get_authorize_url()

    browser = chrome()
    browser.get(auth_url)
    spotify_login(browser, email, password)
    spotify_accept(browser)
    response = browser.current_url
    browser.close()

    code = sp_oauth.parse_response_code(response)
    token_info = sp_oauth.get_access_token(code)

    if token_info:
        return spotipy.Spotify(auth=token_info['access_token'])
    else:
        raise Exception
