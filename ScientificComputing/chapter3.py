import datetime
import time

def next_5digit_int():
    time.sleep(0.123)
    current_time = datetime.datetime.now().time()
    random_no = int(current_time.strftime('%S%f'))
    return random_no/1000
for x in range(0,10):
    i = next_5digit_int()
    print i 