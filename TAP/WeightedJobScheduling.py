class Job:
    def __init__(self, start, finish, weight):
        self.start = start
        self.finish = finish
        self.weight = weight

    def nonConflictingJob(self, job):
        return 1 if self.start >=  job.finish else 0

    def __str__(self):
        return "Start: " + str(self.start) + "  Finish: " + str(self.finish) + "  Weight: " + str(self.weight)


#binary search based function => Complexity of the weight job scheduling is O(nlogn)
def findLatestNonConflictingJob(jobs, index, p):
    left, right = 0, index - 1

    while left <= right:
        mid = (left + right) // 2
        if jobs[index].start >= jobs[mid].finish:
            if jobs[index].start > jobs[mid + 1].finish and jobs[mid + 1].weight >= jobs[mid].weight:
                jobs[index]
                print(Jobs[mid + 1])
                left = mid + 1
            else:
                return mid
        else:
            right = mid - 1

    return  -1

def scheduleJobs(jobs, n, p, opt):
    opt[0] = jobs[0].weight

    for i in range(1,n):
        inclJob = jobs[i].weight

        index = findLatestNonConflictingJob(jobs, i, p)
        if index != -1:
            inclJob = inclJob + opt[index]
            p[i] = index
        else:
            p[i] = -1

        opt[i] = max(inclJob, opt[i-1])
        if inclJob == max(inclJob, opt[i-1]):
            p[i] = index
        else:
            -1

    return opt[n-1]

if __name__ == '__main__':
    Jobs = []
    with open("weighted_job_scheduling.txt") as fin:
        for line in fin:
            s, f, w = [int(val) for val in line.split()]
            Jobs.append(Job(s,f,w))


    n = len(Jobs)

    Jobs = sorted(Jobs, key = lambda j:j.finish)

    print("Jobs which need to be schedule in order to have optimal profit: ")
    for i in range(n):
        print(Jobs[i])

    p = [None] * n
    opt = [0 for _ in range(n)]

    maxProfit = scheduleJobs(Jobs, n, p, opt)
    print(opt)
    print(p)
    print("")

    print("Maximum weight:", maxProfit)
    print("Jobs: ")

    i = opt.index(max(opt))
    while i != None and i != -1:
        print(" ", Jobs[i])
        i = p[i]



