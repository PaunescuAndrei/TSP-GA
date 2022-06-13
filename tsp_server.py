import multiprocessing
from multiprocessing.connection import Listener
import os
import signal
import threading
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from threading import Event, Lock, Thread
import sys
import random
import math
import queue
import time
import socket
import datetime
import numpy as np
from qtui.MainWindow import Ui_MainWindow
import qtui.SwitchInstance

BENCHMARK_MODE = False
BENCHMARK_TIME = 60
BENCHMARK_RUNS = 5

def extract_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
    try:       
        s.connect(('10.255.255.255', 1))
        ip = s.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip

class TreeWidgetItem(QTreeWidgetItem):        
    def __lt__(self, other):
        column = self.treeWidget().sortColumn()
        key1 = self.text(column)
        key2 = other.text(column)
        if column == 2:
            try:
                return float(key1) < float(key2)
            except ValueError:
                return key1 < key2
        return key1.lower() < key2.lower()

class GeneticAlgorithmThread(Thread):
    def __init__(self,App:"MainApp"):
        Thread.__init__(self)
        self.App = App
        self.stopsig = App.stop
        self.data_lock = App.data_lock
        self.Chromosome_Size = None
        self.Coordinates = None
        self.Population_Size = 500
        self.Mutation_Probability = 0.33
        self.Crossover_Probability = 0.44
        self.Elite_Percent = 0.05
        self.Method = True
        self.Selection_Probability = 0.6
        self.Migration_Percent = 0.15
        self.File = "data\\berlin52.tsp"
        #dj38.tsp 6656
        #berlin52.tsp 7542
        #qa194.tsp 9352
        #wi29.tsp 27603
        #eil105.tsp 629
        self.Best = None
        self.Optimal_Solution = 7542
        self.mydict = {}
        self.workQueue = queue.LifoQueue()
        self.running = False
        self.starttime = None
        self.instance_date = datetime.datetime.now()
        self.newfile = None
        self.newoptim = None

    def switchInstance(self,path,optim):
        self.newfile = path
        self.newoptim = optim
        self.starttime = datetime.datetime.now()
        self.instance_date = datetime.datetime.now()

    def stop_ga(self):
        self.running = False

    def start_ga(self):
        self.starttime = datetime.datetime.now()
        self.running = True

    def read_data(self,path):
        infile = open(path, 'r')

        while True:
            line = infile.readline().strip()
            if( line.split()[0] == "NAME"):
                Name = line.split()[2]
            if( line.split()[0] == "DIMENSION"):
                Dimension = int(line.split()[2])
            if( line.split()[0] == "NODE_COORD_SECTION"):
                break

        nodelist = []
        for i in range(0, Dimension):
            x,y = (infile.readline().strip().split()[1:])
            tup=(float(x),float(y))
            nodelist.append(tup)

        infile.close()

        return Dimension,nodelist

    def Generate_Chromosome(self,Chromosome_Size):
        Chromosome = list(range(0,Chromosome_Size))
        random.shuffle(Chromosome)
        return Chromosome

    def Evaluate_pair(self,pair,coordinates,mydict):
        a,b = pair
        if (a,b) in mydict:
            return mydict[(a,b)]
        else:
            newcost = round(math.sqrt(((coordinates[a][0]-coordinates[b][0])) ** 2 + (coordinates[a][1]-coordinates[b][1]) ** 2 ))
            mydict[(a,b)] = newcost
            return newcost

    def Evaluate(self,Chromosome,coordinates,mydict):
        n = len(Chromosome)
        cost=0
        for i in range(n)[1:]:
            cost += self.Evaluate_pair((Chromosome[i-1],Chromosome[i]),coordinates,mydict)
        cost += self.Evaluate_pair((Chromosome[n-1],Chromosome[0]),coordinates,mydict)
        return cost
    

    def Generate_Population(self,Population_Size, Chromosome_Size):
        Population = []
        for i in range(Population_Size):
            Population.append(self.Generate_Chromosome(Chromosome_Size))
        return Population

    def BestSoFar(self,Population,Coordinates,mydict):
        BestSol = Population[0]
        for Solution in Population[1:]:
            if self.Evaluate(Solution,Coordinates,mydict) < self.Evaluate(BestSol,Coordinates,mydict):
                BestSol = Solution
        return BestSol

    def updatePopulation(self,newPopulation,id,ip):
        eval_list = []
        eval_list_old = []

        for Chromosome in self.Population:
            eval_list_old.append(self.Evaluate(Chromosome,self.Coordinates,self.mydict))

        eval_max_old = max(eval_list_old)
            
        for value in range(len(eval_list_old)):
            eval_list_old[value] = eval_max_old-eval_list_old[value] + 1

        for Chromosome in newPopulation:
            eval_list.append(self.Evaluate(Chromosome,self.Coordinates,self.mydict))

        eval_max = max(eval_list)
            
        for value in range(len(eval_list)):
            eval_list[value] = eval_max-eval_list[value] + 1

        best_value = max(eval_list)
        worst_value = min(eval_list_old)
        best_pos = eval_list.index(best_value) 

        count = 0

        while best_value > worst_value:
            best_pos = eval_list.index(best_value) 
            worst_pos = eval_list_old.index(worst_value)
            if not newPopulation[best_pos] in self.Population:
                self.Population[worst_pos] = newPopulation[best_pos].copy()
                eval_list_old[worst_pos] = best_value
                count +=1
            del eval_list[best_pos]
            del newPopulation[best_pos]
            try:
                best_value = max(eval_list)
            except ValueError:
                best_value = 0
            try:
                worst_value = min(eval_list_old)
            except ValueError:
                worst_value = sys.maxsize
        
        if count > 0:
            self.App.updateContributorsSignal.emit(id,ip,count)

    def run(self):
        self.Chromosome_Size,self.Coordinates = self.read_data(self.File)
        self.Population = self.Generate_Population(self.Population_Size*4, self.Chromosome_Size)
        self.Best = self.BestSoFar(self.Population,self.Coordinates,self.mydict).copy()

        while (True and not self.stopsig.is_set()):
            if(self.newfile):
                self.File = self.newfile
                self.Optimal_Solution = self.newoptim
                self.mydict.clear()
                self.Chromosome_Size,self.Coordinates = self.read_data(self.File)
                self.Population = self.Generate_Population(self.Population_Size*4, self.Chromosome_Size)
                self.Best = self.BestSoFar(self.Population,self.Coordinates,self.mydict).copy()
                self.App.mainWindow.updateFile()
                self.newfile = None
                self.newoptim = None
            elif not self.workQueue.empty():
                msgdata,ip = self.workQueue.get()
                msg,id,tspfile,pop,instance_date = msgdata 
                if(tspfile == self.File and instance_date == self.instance_date):
                    bestpop = self.BestSoFar(pop,self.Coordinates,self.mydict).copy()
                    bestpop_value = self.Evaluate(bestpop,self.Coordinates,self.mydict)
                    self.updatePopulation(pop,id,ip[0])
                    if bestpop_value < self.Evaluate(self.Best,self.Coordinates,self.mydict):
                        self.Best = bestpop.copy()
                        if bestpop_value == self.Optimal_Solution:
                            self.stop_ga()
                self.workQueue.task_done()
            Event().wait(timeout=0.1)

class WorkerListener(Thread):
    def __init__(self,App:"MainApp"):
        Thread.__init__(self)
        self.App = App
        self.stopsig = App.stop
        self.data_lock = App.data_lock
        self.connections = {}

    def sendPopulation(self,conn,worker_id,msg,ip,port):
        conn.send(msg)
        self.App.logMessageSignal.emit(f"{time.strftime('[%d/%m/%Y , %H:%M:%S]')} Population sent to {worker_id} ({ip}:{port}).")

    def sendWork(self,conn,worker_id,msg,ip,port):
        conn.send(msg)
        self.App.logMessageSignal.emit(f"{time.strftime('[%d/%m/%Y , %H:%M:%S]')} Work sent to {worker_id} ({ip}:{port}).")

    def sendStop(self,conn,worker_id,msg,ip,port):
        conn.send(msg)
        self.App.logMessageSignal.emit(f"{time.strftime('[%d/%m/%Y , %H:%M:%S]')} Stop signal sent to {worker_id} ({ip}:{port}).")

    def sendChangeInstance(self,conn,worker_id,msg,ip,port):
        conn.send(msg)
        self.App.logMessageSignal.emit(f"{time.strftime('[%d/%m/%Y , %H:%M:%S]')} Change Instance to {self.App.GA.File} signal sent to {worker_id} ({ip}:{port}).")

    def run(self):
        running = True
        listener = Listener(address=(extract_ip(), 25565), authkey=b'secret password')

        def getWork():
            p = (self.App.GA.Population_Size, self.App.GA.Mutation_Probability, self.App.GA.Crossover_Probability, self.App.GA.Elite_Percent, self.App.GA.Method, self.App.GA.Selection_Probability,self.App.GA.Migration_Percent,self.App.GA.File,self.App.GA.instance_date,self.App.GA.Optimal_Solution)
            return (p,(self.App.GA.Chromosome_Size,self.App.GA.Coordinates))

        def serviceConnection(conn,id):
            while not conn.closed:
                try:
                    self.connections[id] = conn
                    msg = conn.recv()
                    if msg[0] == 'GetWork':
                        self.App.logMessageSignal.emit(f"{time.strftime('[%d/%m/%Y , %H:%M:%S]')} Work request from {msg[1]} ({listener.last_accepted[0]}:{listener.last_accepted[1]}).")
                        if(self.App.GA.running):
                            threading.Thread(target=self.sendWork, args=(conn,msg[1],("Work",getWork()),listener.last_accepted[0],listener.last_accepted[1],)).start()
                        else:
                            threading.Thread(target=self.sendStop, args=(conn,msg[1],("Stop",),listener.last_accepted[0],listener.last_accepted[1],)).start()
                    if msg[0] == 'UpdatePopulation':
                        self.App.logMessageSignal.emit(f"{time.strftime('[%d/%m/%Y , %H:%M:%S]')} Update Population request from {msg[1]} ({listener.last_accepted[0]}:{listener.last_accepted[1]}).")
                        if(self.App.GA.running):
                            if(msg[2] == self.App.GA.File and msg[4] == self.App.GA.instance_date):
                                threading.Thread(target=self.sendPopulation, args=(conn,msg[1],("Migration",self.App.GA.File,self.App.GA.Population),listener.last_accepted[0],listener.last_accepted[1],)).start()
                                self.App.GA.workQueue.put((msg,listener.last_accepted))
                            else:
                                threading.Thread(target=self.sendChangeInstance, args=(conn,msg[1],("ChangeInstance",self.App.GA.File),listener.last_accepted[0],listener.last_accepted[1],)).start()
                        else:
                            threading.Thread(target=self.sendStop, args=(conn,msg[1],("Stop",),listener.last_accepted[0],listener.last_accepted[1],)).start()
                    if msg[0] == 'CloseConnection':
                        conn.close()
                        break
                except (ConnectionResetError, OSError, EOFError):
                    conn.close()
                    break
            if conn.closed:
                with self.data_lock:
                    if id in self.connections:
                        del self.connections[id]
                self.App.deleteContributorsSignal.emit(id)

        while running:
            try:
                conn = listener.accept()
                msg = conn.recv()
                if msg[0] == 'Connect':
                    self.App.updateContributorsSignal.emit(msg[1],listener.last_accepted[0],0)
                    self.connections[msg[1]] = conn
                    threading.Thread(target=serviceConnection, args=(conn,msg[1],)).start()
                if msg == 'CloseConnection':
                    conn.close()
                    break
                if msg == 'CloseServer':
                    conn.close()
                    running = False
                    break
            except (multiprocessing.context.AuthenticationError, OSError, EOFError):
                pass

class switchInstanceDialog(QDialog,qtui.SwitchInstance.Ui_Dialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.browseButton.clicked.connect(self.getFile)
    def getFile(self):
        fileName , _ = QFileDialog.getOpenFileName(self, 'Switch Instance')
        self.filepath.setText(fileName)

class MainWindow(QMainWindow,Ui_MainWindow):

    def __init__(self,App: "MainApp"):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.setWindowTitle(f"TSP Genetic Algorithm")
        self.splitter.setStretchFactor(0,5)
        self.splitter.setStretchFactor(1,2)
        self.App = App
        self.oldBest = None
        self.plotitems = None
        self.updateFile()
        self.contributorsTree.sortByColumn(2,Qt.SortOrder.DescendingOrder)
        self.stopButton.clicked.connect(lambda : self.App.GA.stop_ga())
        self.startButton.clicked.connect(lambda : self.App.GA.start_ga())
        self.switchButton.clicked.connect(self.switchInstanceButton)
        self.exportButton.clicked.connect(self.exportSolution)
        self.logsqueue = queue.Queue() 
        self.benchmark_runs = []
        self.benchmark_run = [None]*BENCHMARK_TIME

        timer = QTimer(self)
        timer.timeout.connect(self.updateGraph)
        if BENCHMARK_MODE:
            timer.setInterval(200)  
        else:
            timer.setInterval(2000)  
        timer.start()

        timer2 = QTimer(self)
        timer2.timeout.connect(self.updateMessages)
        timer2.setInterval(2000)  
        timer2.start()

        timer3 = QTimer(self)
        timer3.timeout.connect(self.updateTimeElapsed)
        if BENCHMARK_MODE:
            timer3.setInterval(200)  
        else:
            timer3.setInterval(1000)  
        timer3.start()

    def updateFile(self):
        self.currentInstanceValue.setText(os.path.basename(self.App.GA.File))
        self.optimal_best_value.setText(str(self.App.GA.Optimal_Solution)) 
        self.oldBest = None
        self.current_best_value.setText("None")
        if(self.plotitems):
            for i in self.plotitems:
                i.clear()
            self.plotitems = []

    def updateTimeElapsed(self):
        if(self.App.GA.running and self.App.GA.starttime):
            elapsed_seconds = (datetime.datetime.now() - self.App.GA.starttime).total_seconds()
            if BENCHMARK_MODE:
                while(self.App.mainWindow.current_best_value.text() == "None"):
                    Event().wait(timeout=0.100)
                    self.App.GA.starttime = datetime.datetime.now()
                if(elapsed_seconds <= BENCHMARK_TIME):
                    self.benchmark_run[int(elapsed_seconds)] = int(self.App.mainWindow.current_best_value.text())
                else:
                    self.benchmark_runs.append(self.benchmark_run.copy())
                    self.benchmark_run = [None]*BENCHMARK_TIME
                    if(len(self.benchmark_runs) == BENCHMARK_RUNS):
                        self.App.GA.stop_ga()
                        arr = np.array(self.benchmark_runs)
                        results = list(np.average(arr,axis=0))
                        with open('benchmark.txt','a+') as f:
                            f.write(f"{self.App.GA.File} | {len(self.App.WL.connections)} | {str(results)}\n")
                        self.benchmark_runs.clear()
                    else:
                        self.App.GA.switchInstance(self.App.GA.File,self.App.GA.Optimal_Solution)
                        while(self.App.GA.newfile):
                            Event().wait(timeout=0.100)
                        self.App.GA.starttime = datetime.datetime.now()
                    print(len(self.benchmark_runs))
            h = int(elapsed_seconds // 3600)
            m = int(elapsed_seconds % 3600 // 60)
            s = int(elapsed_seconds % 60)
            self.timeElapsedValue.setText('{:02d}:{:02d}:{:02d}'.format(h, m, s))

    def updateGraph(self):
        if self.App.GA.Best:
            if(self.oldBest != self.App.GA.Best):
                val = self.App.GA.Evaluate(self.App.GA.Best,self.App.GA.Coordinates,self.App.GA.mydict)
                self.current_best_value.setText(str(val))
                if(not BENCHMARK_MODE):
                    if self.plotitems:
                        for j in range(len(self.App.GA.Best)-1):
                            self.plotitems[j].setData([self.App.GA.Coordinates[self.App.GA.Best[j]][0],self.App.GA.Coordinates[self.App.GA.Best[j+1]][0]], [self.App.GA.Coordinates[self.App.GA.Best[j]][1],self.App.GA.Coordinates[self.App.GA.Best[j+1]][1]], symbol ='x', symbolPen ='g', symbolBrush = 0.2)
                        self.plotitems[-1].setData([self.App.GA.Coordinates[self.App.GA.Best[len(self.App.GA.Best)-1]][0],self.App.GA.Coordinates[self.App.GA.Best[0]][0]], [self.App.GA.Coordinates[self.App.GA.Best[len(self.App.GA.Best)-1]][1],self.App.GA.Coordinates[self.App.GA.Best[0]][1]], symbol ='x', symbolPen ='g', symbolBrush = 0.2)
                    else:
                        self.plotitems = []
                        for j in range(len(self.App.GA.Best)-1):
                            self.plotitems.append(self.graphPlot.plot([self.App.GA.Coordinates[self.App.GA.Best[j]][0],self.App.GA.Coordinates[self.App.GA.Best[j+1]][0]], [self.App.GA.Coordinates[self.App.GA.Best[j]][1],self.App.GA.Coordinates[self.App.GA.Best[j+1]][1]], symbol ='x', symbolPen ='g', symbolBrush = 0.2))
                        self.plotitems.append(self.graphPlot.plot([self.App.GA.Coordinates[self.App.GA.Best[len(self.App.GA.Best)-1]][0],self.App.GA.Coordinates[self.App.GA.Best[0]][0]], [self.App.GA.Coordinates[self.App.GA.Best[len(self.App.GA.Best)-1]][1],self.App.GA.Coordinates[self.App.GA.Best[0]][1]], symbol ='x', symbolPen ='g', symbolBrush = 0.2))
                self.oldBest = self.App.GA.Best

    def updateMessages(self):
        logs = []
        if(self.logList.count() > 1000):
            self.logList.clear()
        while self.logsqueue.qsize() != 0:
            logs.append(self.logsqueue.get_nowait())
            self.logsqueue.task_done()
        self.logList.addItems(logs)
        self.logList.scrollToBottom()

    def logMessage(self,msg):
        self.logsqueue.put(msg)

    def updateContributor(self,id,ip,count):
        try:
            item = self.contributorsTree.findItems(id,Qt.MatchExactly, 0)[0]
            item.setText(2,str(int(item.text(2)) + count))
        except:
            if(count == 0):
                item = TreeWidgetItem([id,ip,"0"])
                self.contributorsTree.addTopLevelItem(item)

    def deleteContributor(self,id):
        try:
            item = self.contributorsTree.findItems(id,Qt.MatchExactly, 0)[0] 
            root = self.contributorsTree.invisibleRootItem()
            (item.parent() or root).removeChild(item)
        except:
            pass
    
    def switchInstanceButton(self):
        dialog = switchInstanceDialog(self)
        value = dialog.exec()
        if(value == QDialog.Accepted):
            if os.path.isfile(dialog.filepath.text()):
                self.App.GA.switchInstance(dialog.filepath.text(),dialog.optimalValue.value())
        dialog.deleteLater()     

    def exportSolution(self):
        filename, _ = QFileDialog.getSaveFileName(self, 'Export Solution')
        with open(filename, 'w') as f:
            f.write(f'NAME : {os.path.basename(self.App.GA.File)}\n')
            f.write(f'COMMENT : Length = {self.current_best_value.text()}\n')
            f.write(f'TYPE : TOUR\n')
            f.write(f'DIMENSION : {self.App.GA.Chromosome_Size}\n')
            f.write(f'TOUR_SECTION\n')
            for node in self.App.GA.Best:
                f.write(f'{node}\n')
            f.write(f'-1\n')
            f.write(f'EOF')

class MainApp(QApplication):

    updateContributorsSignal = Signal(str,str,int)
    deleteContributorsSignal = Signal(str)
    logMessageSignal = Signal(str)

    def __init__(self, args):
        super(MainApp, self).__init__(args)

        self.stop = Event()
        self.data_lock = Lock()

        self.GA = GeneticAlgorithmThread(self)
        self.GA.daemon = True

        self.mainWindow = MainWindow(self)

        self.WL = WorkerListener(self)
        self.WL.daemon = True

        self.updateContributorsSignal.connect(self.mainWindow.updateContributor)
        self.deleteContributorsSignal.connect(self.mainWindow.deleteContributor)
        self.logMessageSignal.connect(self.mainWindow.logMessage)

        signal.signal(signal.SIGINT, lambda signal, frame: self.handler(self.stop))  
        self.aboutToQuit.connect(lambda :self.handler(self.stop))

        QApplication.setStyle("Fusion")
        dark_palette = QPalette()
        dark_palette.setColor(QPalette.Window, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.WindowText, Qt.white)
        dark_palette.setColor(QPalette.Base, QColor(35, 35, 35))
        dark_palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ToolTipBase, QColor(25, 25, 25))
        dark_palette.setColor(QPalette.ToolTipText, Qt.white)
        dark_palette.setColor(QPalette.Text, Qt.white)
        dark_palette.setColor(QPalette.Button, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ButtonText, Qt.white)
        dark_palette.setColor(QPalette.BrightText, Qt.red)
        dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.HighlightedText, QColor(35, 35, 35))
        dark_palette.setColor(QPalette.Active, QPalette.Button, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.Disabled, QPalette.ButtonText, Qt.darkGray)
        dark_palette.setColor(QPalette.Disabled, QPalette.WindowText, Qt.darkGray)
        dark_palette.setColor(QPalette.Disabled, QPalette.Text, Qt.darkGray)
        dark_palette.setColor(QPalette.Disabled, QPalette.Light, QColor(53, 53, 53))
        QApplication.setPalette(dark_palette)

        self.mainWindow.show()
        self.GA.start()
        self.WL.start()
        self.exec_()

    def handler(self,stop):
        stop.set()
        for conn in self.WL.connections.values():
            conn.close()

if (__name__ == '__main__'):
    app = MainApp(sys.argv)