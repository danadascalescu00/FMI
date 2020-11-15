jobs = []
with open('schedule.txt') as fin:
    n = int(fin.readline())
    for i in range(n):
        input = []
        input.append(i+1)
        input.extend([int(value) for value in fin.readline().split()])
        jobs.append(input)
fin.close()

jobs = sorted(jobs, key=lambda v:v[2])
print(jobs)

print("Propunere: ")
start = delay = 0
for i in range(n):
    print(jobs[i][0], ":", start, start + jobs[i][1], start + jobs[i][1] - jobs[i][2])
    if start + jobs[i][1] - jobs[i][2] > delay:
        delay = start + jobs[i][1] - jobs[i][2]
    start = start + jobs[i][1]
print("Intarziere ", delay)
