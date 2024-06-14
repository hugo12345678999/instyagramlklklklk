from flask import Flask, render_template, request, redirect, url_for
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time

app = Flask(__name__)

def login_instagram(username, password):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        driver.get("https://www.instagram.com/accounts/login/")
        time.sleep(3)
        
        username_input = driver.find_element(By.NAME, "username")
        username_input.send_keys(username)
        
        password_input = driver.find_element(By.NAME, "password")
        password_input.send_keys(password)
        
        password_input.send_keys(Keys.RETURN)
        time.sleep(5)
        
        if "login" in driver.current_url:
            return "Login falhou."
        else:
            return "Login bem-sucedido."
    finally:
        driver.quit()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        result = login_instagram(username, password)
        return result
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
