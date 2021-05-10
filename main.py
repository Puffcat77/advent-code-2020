from day_1 import task as task1
from day_2 import task as task2
from day_3 import task as task3


def getData(path):
    with open(path) as f:
        data = f.readlines()
        data = [x.strip() for x in data]
    return data


if __name__ == '__main__':
    # task1.task(getData('day_1/input.txt'))
    # task2.task(getData('day_2/input.txt'))
    task3.task(getData('day_3/input.txt'))
