def read(task):
    with open("activitati.txt") as fin:
        N = int(fin.readline())
        for line in fin:
            task.append([int(x) for x in line.split()])
    fin.close()

def main():
    task = []
    read(task)
    task = sorted(task, key = lambda t:t[1])
    print("1. ", task[0])

    fin, count = task[0][1], 1
    for i in range(1,len(task)):
        if task[i][0] > fin:
            print(i,". ", task[i])
            fin = task[i][1]
            count += 1
    print("Numarul activitatilor selectate: ", count)

if __name__ == '__main__':
    main()