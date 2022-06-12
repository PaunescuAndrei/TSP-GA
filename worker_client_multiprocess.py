import multiprocessing
import signal
from threading import Event, Lock, Thread
import uuid
from worker_client import GeneticAlgorithm

def init_worker():
    signal.signal(signal.SIGINT, signal.SIG_IGN)

if (__name__ == '__main__'):

    def driver_func():
        PROCESSES = 1
        workers = []
        for i in range(PROCESSES):
            workers.append(GeneticAlgorithm(id = str(uuid.uuid4())))

        pool = multiprocessing.Pool(PROCESSES, init_worker)

        p = ('192.168.100.40',25565)
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