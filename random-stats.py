import random
import matplotlib.pyplot as plt

number_of_numbers = 20
number_of_runs = 30
x = 0
all_map = []

while x <= number_of_runs:
    map = []
    i = 0
    while i <= number_of_numbers:
        number = random.randint(1, 10)
        map.append(number)
        all_map.append(number)
        i += 1

    x += 1
    print(map)

plt.hist(all_map, 50)
plt.show()



