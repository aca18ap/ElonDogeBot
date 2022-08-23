from usr import getUsersFromFile
from collections import deque
from twt import startListening, processTweet
from multiprocessing import Process, Queue
import sys

def twitterBoot(q):
    startListening(q)
    

def queueMonitor(q):
    ##Constantly monitoring the queue for jobs to be done
    while True:
        if q.empty() is False:
            job = q.get()
            processTweet(job)
    
def main():
    q = Queue()
    print("Starting twitter bot")
    tp = Process(target=twitterBoot, args=(q,))
    print("Starting queue monitoring")
    qp = Process(target=queueMonitor, args=(q,))

    tp.start()
    qp.start()

if __name__ == '__main__':
    print('Booting up')
    main()