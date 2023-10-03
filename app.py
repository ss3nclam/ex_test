import time

import schedule

from app_core.data import (check_cities_table, commit_weather, get_cities_list,
                           get_weather, init_cities)
from app_core.settings import app_verbose, config


def job(cities:list):
    for city in cities:
        weather = get_weather(city['id'], city['name'], city['longitude'], city['latitude'])
        if weather:
            commit_weather(city['id'], city['name'], weather)


def main():
    if not check_cities_table():
        init_cities()
    cities_list = get_cities_list()
    if cities_list:
        time_delta = int(config['SCHEDULER']['time_delta'])
        schedule.every(time_delta).hours.do(job, cities_list)
        while True:
            schedule.run_pending()
            time.sleep(1)
    else:
        print('Something was wrong!')


if __name__ == '__main__':
    main()