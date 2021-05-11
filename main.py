from day_1 import task as task1
from day_2 import task as task2
from day_3 import task as task3
from day_4 import task as task4
from day_5 import task as task5
from day_6 import task as task6
from day_7 import task as task7


def getData(path):
    with open(path) as f:
        data = f.readlines()
        data = [x.strip() for x in data]
    return data


def getDataWithEmptyLines(path):
    lines = []
    i = 0
    with open(path) as f:
        for line in f:
            if line != '\n':
                if i < len(lines):
                    lines[i] += ' ' + line
                else:
                    lines.append(line)
            else:
                i += 1
    for i in range(len(lines)):
        lines[i] = lines[i].replace('\n', '')
    return lines


if __name__ == '__main__':
    # task1.task(getData('day_1/input.txt'))
    # task2.task(getData('day_2/input.txt'))
    # task3.task(getData('day_3/input.txt'))
    # task4.task(getDataWithEmptyLines('day_4/input.txt'))
    # task5.task(getData('day_5/input.txt'))
    # task6.task(getDataWithEmptyLines('day_6/input.txt'))
    task7.task(getData('day_7/input.txt'))
