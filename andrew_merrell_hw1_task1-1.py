"""
This program lists out Catlan numbers that are smaller than a billion
Using the factorial method from math and interger division
"""
from math import factorial as fct
def catlan(num):
    if num < 2:
        return 1
    return fct(2 * num) // (fct(num+1) * fct(num))

#this would be the main()
result = 0
i = 0
while True:
    result = catlan(i)
    if result > 1e9:
        break
    print('The', i,'number in the Catalan series is', result)
    i = i + 1 # so tempted to i++