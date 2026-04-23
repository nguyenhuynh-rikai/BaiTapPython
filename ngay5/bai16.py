import random
import time

def temperature_sensor():
    while True:
        temp = round(random.uniform(20, 35), 2)
        yield temp
        time.sleep(1)

sensor = temperature_sensor()

for _ in range(5):
    print(next(sensor))