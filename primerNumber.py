import optparse
import queue
import threading
import time

class Worker(threading.Thread):

    def __init__(self, work_queue, number, arrayTemp):
        super().__init__()
        self.work_queue = work_queue
        self.number = number
        self.arrayTemp = arrayTemp#define a destination to store output

    def run(self):
        while True:
            try:
                argList = self.work_queue.get()
                self.process(argList)
            finally:
                self.work_queue.task_done()

    def process(self, argList):#screening method
        divided = argList[0]
        startPos = argList[1]
        endPos = argList[2]
        arrayTemp = self.arrayTemp
        for i in range(startPos , endPos + 1):
            arrayTemp[i] = bool(arrayTemp[i] and i % divided)
        return

def main():
    opts, maxNumber = parse_options()
    try:
        maxNumber = int(maxNumber)
    except ValueError:
        print("Parameter should be an Integer.")
        return
    if maxNumber <= 1:
        print("Parameter should larger than 1.")
        return
    arrayTemp = [True] * (maxNumber + 1)
    arrayTemp[0] = 0
    arrayTemp[1] = False
    numThread = maxNumber//10
    work_queue = queue.Queue()
    for i in range(numThread):
        number = "{0}: ".format(i + 1) if opts.debug else ""
        worker = Worker(work_queue, number, arrayTemp)
        worker.daemon = True
        worker.start()
    sqrt = int(maxNumber**0.5)
    for i in range(1,sqrt):
        if(arrayTemp[i]):
            rang = 10
            for j in range(maxNumber//10 + 1):
                start = i + 1 + j * rang
                start = start if start < maxNumber else maxNumber
                end = start + rang - 1
                end = end if end < maxNumber else maxNumber
                work_queue.put([i,start,end])
    work_queue.join()
    for i in range(1,maxNumber+1):
        if arrayTemp[i]:
            print(i)
    return

def parse_options():#get max number
    parser = optparse.OptionParser(
            usage=("usage: %prog [options] number"
                   'Parameter should be a positive number which larger than 1'))
    parser.add_option("-d", "--debug", dest="debug", default=False,
                      action="store_true")
    opts, args = parser.parse_args()
    if len(args) == 0:
        parser.error("A number and at least one path must be specified")
    return opts, args[0]

main()
print('Running time: %s Seconds'%time.process_time())#output running time