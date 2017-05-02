import time
import random
from main2 import Triple, Collection

def average_of(num):
    def decorator(func):
        def wrapper(*arg):
            ave = [func(*arg) for _ in range(num)]
            return sum(ave)/len(ave)
        return wrapper
    return decorator

@average_of(5)
def power_ten(power):
    a=[]
    for _ in range(int(10**power)):
        x = random.randint(1,10000)
        y = random.randint(1,10000)
        while(x == y):
            y = random.randint(1,10000)
        a.append(Triple(min(x,y), max(x,y),random.randint(1,10)))
    a.sort()

    c = Collection(a)
    start = time.time()
    c.next_previous_possibility()
    c.solve()
    stop = time.time()
    return stop - start


x_axis = [i/10 for i in range(1,51)]
y_axis = []
for power in [i/10 for i in range(1,51)]:
    y_axis.append(power_ten(power))
