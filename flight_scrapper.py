import time
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from apscheduler.schedulers.blocking import BlockingScheduler

job_start = datetime.now() + timedelta(seconds=3)
flight_sched = BlockingScheduler()

#choose webdriver
options = Options()
options.add_argument("--headless")


def calculate_start(
        start: datetime,
        hours = 0,
        minutes= 0,
        seconds = 0
) :
    start_time = start + timedelta(hours=hours,
                                   minutes=minutes,
                                   seconds=seconds)
    return start_time.strftime('%Y-%m-%d %H:%M:%S')



@flight_sched.scheduled_job('interval', minutes=60, start_date=calculate_start(job_start, seconds=0))
def get_prices():
    driver = webdriver.Firefox(options=options)
    print('Buscando...')
    driver.get("https://123milhas.com/v2/busca?de=SAO&para=MVD&ida=18-09-2022&volta=25-09-2022&adultos=2&criancas=0&classe=3")
    time.sleep(20)
    print('Parseando ...')
    prices = driver.find_elements(By.CLASS_NAME, "ordenation-card__text")

    recommended = prices[1].text
    cheaper = prices[4].text

    for element in prices:
        print(element.text)
    try:
        driver.close()
        driver.quit()
        driver.dispose()
    except:
        pass


if __name__ == '__main__':
    print('Startando serviços...')
    # flight_sched.start()
    get_prices()
