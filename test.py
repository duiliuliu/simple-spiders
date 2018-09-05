from concurrent.futures import ThreadPoolExecutor, wait, as_completed
from time import sleep
from random import randint
def return_after_random_secs(num):
    sleep(randint(1, 5))
    print("Return of {}".format(num))
    return "Return of {}".format(num)
pool = ThreadPoolExecutor(5)
futures = []
for x in range(10):
    print('add ',x)
    futures.append(pool.submit(return_after_random_secs, x))


print(as_completed(futures))



