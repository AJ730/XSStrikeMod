from threading import Event

from selenium import webdriver
import time

from selenium.webdriver.common.by import By

global driver

def initiate_driver():
    print("sample test case started")
    driver = webdriver.Chrome(r'/home/kali/WebstormProjects/XSStrike/xss/chromedriver')

    driver.maximize_window()
    driver.get("https://www.google.com/")

    print("Google Chrome is responding")

def accept():
    agree = driver.find_element(By.ID,"L2AGLb")
    agree.click()

    print("Accepted License")

def search(query):
    #click on the Google search button
    search_bar = driver.find_element(By.NAME, query)

def halt():
    Event().wait()

