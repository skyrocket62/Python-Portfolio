# WRITTEN BY REMINGTON PONCE (MARCH 2022).
# BUILT BY MY OWN PASSION FOR PYTHON AND TO AUTOMATE A TASK FOR A CONTRACT EMPLOYMENT.
# THIS IS A SHORT, FUNCTIONAL PROGRAM TO AUTOMATICALLY DOWNLOAD A VARYING NUMBER OF INDIVIDUAL DATA FILES OVER A SPECIFIED DATE RANGE.
# (LOGIN CREDENTIALS BELOW ARE REDACTED)

from selenium import webdriver
from selenium.webdriver.common.by import By
import time, datetime

ids = {'CATS1': '216751', 'CATS2': '216755', 'CATS3': '216753', 'PM': '216743', 'GPE': '216739'}


service = input('For which service do you want data? (options are "CATS", "PM" (panther mover), and "GPE". Only one service at a time.)')
startDate = input('Start date? (must be in format YYYY,MM,DD)')
endDate = input('End date? (must be in format YYYY,MM,DD)')

startDate = startDate.split(',')
for num in range(len(startDate)):
    startDate[num] = int(startDate[num])
startDate = datetime.date(startDate[0], startDate[1], startDate[2])
endDate = endDate.split(',')
for num in range(len(endDate)):
    endDate[num] = int(endDate[num])
endDate = datetime.date(endDate[0], endDate[1], endDate[2])


web = webdriver.Chrome('/Users/remingtonponce/PyCharmProjects/chromedriver')
link = 'https://manager.transloc.com/agencies/fiu/reports/performance/arrivals-departures/'
web.get(link)
time.sleep(0.5)

username = '<redacted>'
Username = web.find_element(By.XPATH, value = '//*[@id="username"]')
Username.send_keys(username)

password = '<redacted>'
Password = web.find_element(By.XPATH, value = '//*[@id="password"]')
Password.send_keys(password)

login = web.find_element(By.XPATH, value = '/html/body/div/div[2]/div/div/form/div[6]/div/div/input')
login.click()
time.sleep(1)


date = startDate
while date != (endDate + datetime.timedelta(days = 1)):
    stringDate = str(date).replace('-', '/')
    stringDate = stringDate[5:] + '/' + stringDate[:4]

    if service == 'CATS':
        for shuttle in ['CATS1', 'CATS2', 'CATS3']:
            link = 'https://manager.transloc.com/agencies/fiu/reports/performance/arrivals-departures/all-buses/' + ids[shuttle] + '/?s=' + stringDate
            web.get(link)
            time.sleep(0.5)

            download = web.find_element(By.XPATH, value = '//*[@id="content"]/div[1]/div/div/a')
            download.click()

        date += datetime.timedelta(days = 1)

    else:
        link = 'https://manager.transloc.com/agencies/fiu/reports/performance/arrivals-departures/all-buses/' + ids[service] + '/?s=' + stringDate
        web.get(link)
        time.sleep(0.5)

        download = web.find_element(By.XPATH, value = '//*[@id="content"]/div[1]/div/div/a')
        download.click()

        date += datetime.timedelta(days = 1)



# EXCEL SECTION BELOW


