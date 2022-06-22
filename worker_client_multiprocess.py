import multiprocessing
import signal
import sys
from threading import Event, Lock, Thread
import uuid
from worker_client import GeneticAlgorithm

IP = '192.168.100.40'
PORT = 25565
PROCESSES = 1

def init_worker():
    signal.signal(signal.SIGINT, signal.SIG_IGN)

if (__name__ == '__main__'):
    if(len(sys.argv) == 2):
        PROCESSES = int(sys.argv[1])

    def driver_func():
        workers = []
        for i in range(PROCESSES):
            workers.append(GeneticAlgorithm(id = str(uuid.uuid4())))

        pool = multiprocessing.Pool(PROCESSES, init_worker)

        p = (IP,PORT)
        results = [pool.apply_async(worker.start, args=p, kwds={'printresults': False}) for worker in workers]

        try:
            while True:
                Event().wait(timeout=0.5)
                if all([r.ready() for r in results]):
                    break
                
        except KeyboardInterrupt:
            pool.terminate()
            pool.join()
        finally:
            pool.close()
            pool.join()
            
    driver_func()