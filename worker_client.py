from multiprocessing.connection import Client
import signal
import sys 
from threading import Event, Lock, Thread
import random
import time
import math
import copy
import uuid

class GeneticAlgorithm():
    def __init__(self,id):
        self.id = id
        self.conn = None
        self.running = False
        self.file = None

    def Generate_Chromosome(self,Chromosome_Size):
        Chromosome = list(range(0,Chromosome_Size))
        random.shuffle(Chromosome)
        return Chromosome

    def Evaluate_pair(self,pair,coordinates,cache_dict):
        a,b = pair
        if (a,b) in cache_dict:
            return cache_dict[(a,b)]
        else:
            newcost = round(math.sqrt(((coordinates[a][0]-coordinates[b][0])) ** 2 + (coordinates[a][1]-coordinates[b][1]) ** 2 ))
            cache_dict[(a,b)] = newcost
            return newcost

    def Evaluate(self,Chromosome,coordinates,cache_dict):
        n = len(Chromosome)
        cost=0
        for i in range(n)[1:]:
            cost += self.Evaluate_pair((Chromosome[i-1],Chromosome[i]),coordinates,cache_dict)
        cost += self.Evaluate_pair((Chromosome[n-1],Chromosome[0]),coordinates,cache_dict)
        return cost

    def Generate_Population(self,Population_Size, Chromosome_Size):
        Population = []
        for i in range(Population_Size):
            Population.append(self.Generate_Chromosome(Chromosome_Size))
        return Population

    def Select_Tournament(self,Population,Population_Size,Coordinates,Elite_Percent,Selection_Probability,cache_dict):
        eval_list = []
        pop_list = copy.deepcopy(Population)
        New_Population = []
        Elite_Pop = []

        for Chromosome in Population:
            eval_list.append(self.Evaluate(Chromosome,Coordinates,cache_dict))

        eval_max = max(eval_list)
            
        for value in range(len(eval_list)):
            eval_list[value] = eval_max-eval_list[value] + 1

        Elite_Numbers = int(math.floor(Elite_Percent*Population_Size)) + 1
        
        for i in range(Population_Size - Elite_Numbers):

            random_chromosome1 = random.randint(0,Population_Size-1)
            random_chromosome2 = random.randint(0,Population_Size-1)

            if random.random() < Selection_Probability:
                if eval_list[random_chromosome1] > eval_list[random_chromosome2]:
                    New_Population.append(pop_list[random_chromosome1].copy())
                else:
                    New_Population.append(pop_list[random_chromosome2].copy())
            else:
                if eval_list[random_chromosome2] > eval_list[random_chromosome2]:
                    New_Population.append(pop_list[random_chromosome2].copy())
                else:
                    New_Population.append(pop_list[random_chromosome1].copy())
        
        best_pos = eval_list.index(max(eval_list)) 
        Elite_Pop.append(pop_list[best_pos].copy())

        for i in range(Elite_Numbers-1):
            best_pos = eval_list.index(max(eval_list)) 
            Elite_Pop.append(pop_list[best_pos].copy())
            del eval_list[best_pos]
            del pop_list[best_pos]

        return Elite_Pop.copy() + New_Population.copy()

    def Partially_Mapped_Crossover(self,Population,Population_Size,Chromosome_Size, Crossover_Probability):
        Parents = []
        for i in range(Population_Size):
            if random.random() < Crossover_Probability:
                Parents.append((i,Population[i].copy()))
        if (len(Parents) % 2 == 1):
            Parents.pop(-1)

        while Parents:
            C1_pos=random.randint(0, len(Parents)-1)       
            C2_pos=random.randint(0, len(Parents)-1)
            while(C1_pos == C2_pos):
                C2_pos=random.randint(0, len(Parents)-1)

            i = random.randint(1, Chromosome_Size)
            j = random.randint(1, Chromosome_Size)
            if j < i:
                i,j = j,i

            Parent_A = Parents[C1_pos][1]
            Parent_B = Parents[C2_pos][1]

            Child_B = [None] * i + Parent_A[i:j] + [None] * (len(Parent_A)-j)
            Child_A = [None] * i + Parent_B[i:j] + [None] * (len(Parent_A)-j)

            for k in range(0,i):
                if Parent_A[k] not in Parent_B[i:j]:
                    Child_A[k] = Parent_A[k]

            for k in range(j,len(Parent_A)):
                if Parent_A[k] not in Parent_B[i:j]:
                    Child_A[k] = Parent_A[k]

            for k in range(0,i):
                if Parent_B[k] not in Parent_A[i:j]:
                    Child_B[k] = Parent_B[k]

            for k in range(j,len(Parent_B)):
                if Parent_B[k] not in Parent_A[i:j]:
                    Child_B[k] = Parent_B[k]

            for k in range(len(Parent_A)):
                if(Child_A[k] == None):
                    tmp = Parent_A[k]
                    while True:
                        value = Parent_A[i:j][Parent_B[i:j].index(tmp)]
                        if(value in Parent_B[i:j]):
                            tmp = value
                        else:
                            Child_A[k] = value
                            break

            for k in range(len(Parent_B)):
                if(Child_B[k] == None):
                    tmp = Parent_B[k]
                    while True:
                        value = Parent_B[i:j][Parent_A[i:j].index(tmp)]
                        if(value in Parent_A[i:j]):
                            tmp = value
                        else:
                            Child_B[k] = value
                            break

            Population[Parents[C1_pos][0]] = Child_A
            Population[Parents[C2_pos][0]] = Child_B

            if(C1_pos > C2_pos):
                del Parents[C1_pos]
                del Parents[C2_pos]
            else:
                del Parents[C2_pos]
                del Parents[C1_pos]
        return Population

    def Mutate(self,Population, Mutation_Probability,Dimension):
        newPopulation = copy.deepcopy(Population)
        for Chromosome in range(len(newPopulation)):
            if random.random() < Mutation_Probability:
                a = random.randint(0,Dimension-1)
                b =random.randint(a,Dimension-1)
                while a<b:
                    newPopulation[Chromosome][a],newPopulation[Chromosome][b] = newPopulation[Chromosome][b],newPopulation[Chromosome][a]
                    if random.random() < Mutation_Probability:
                        j = random.randint(0,Dimension-1)
                        newPopulation[Chromosome][a],newPopulation[Chromosome][j] = newPopulation[Chromosome][j],newPopulation[Chromosome][a]
                    a+=1
                    b-=1
        return newPopulation

    def BestSoFar(self,Population,Coordinates,cache_dict):
        BestSol = Population[0]
        for Solution in Population[1:]:
            if self.Evaluate(Solution,Coordinates,cache_dict) < self.Evaluate(BestSol,Coordinates,cache_dict):
                BestSol = Solution
        return BestSol

    def Migration(self,Population,NewPopulation,Percentage,Coordinates,cache_dict):
        eval_list = []
        pop_list = copy.deepcopy(Population)
        Old_Population = []
        Elite_Pop = []
        Population_Size = len(Population)

        for Chromosome in Population:
            eval_list.append(self.Evaluate(Chromosome,Coordinates,cache_dict))

        eval_max = max(eval_list)
            
        for value in range(len(eval_list)):
            eval_list[value] = eval_max-eval_list[value] + 1

        Elite_Numbers = int(math.floor(Percentage*Population_Size)) + 1
        best_pos = eval_list.index(max(eval_list))

        for i in range(Population_Size - Elite_Numbers):
            best_pos = eval_list.index(max(eval_list))
            Old_Population.append(pop_list[best_pos].copy())
            del eval_list[best_pos]
            del pop_list[best_pos]

        eval_list.clear()
        for Chromosome in NewPopulation:
            eval_list.append(self.Evaluate(Chromosome,Coordinates,cache_dict))

        eval_max = max(eval_list)
            
        for value in range(len(eval_list)):
            eval_list[value] = eval_max-eval_list[value] + 1

        best_pos = eval_list.index(max(eval_list)) 
        Elite_Pop.append(NewPopulation[best_pos].copy())

        for i in range(Elite_Numbers-1):
            best_pos = eval_list.index(max(eval_list)) 
            Elite_Pop.append(NewPopulation[best_pos].copy())
            del eval_list[best_pos]
            del NewPopulation[best_pos]

        return Elite_Pop.copy() + Old_Population.copy()

    def initConnection(self,ip,port):
        self.conn = Client((ip, port), authkey=b'secret password')
        self.conn.send(('Connect',self.id))

    def getWork(self):
        self.conn.send(('GetWork',self.id))
        msg = self.conn.recv() 
        if msg[0] == 'Work':
            return msg[1]
        if msg[0] == 'Stop':
            self.running = False
        return None,(None,None)

    def updatePopulation(self,Population,Migration_Percent,Coordinates,cache_dict,last=False):
        try:
            self.conn.send(('UpdatePopulation',self.id,self.file,Population))
            msg = self.conn.recv() 
            if msg[0] == 'Migration':
                return self.Migration(Population,msg[2],Migration_Percent,Coordinates,cache_dict)
            if msg[0] == 'ChangeInstance':
                self.running = False
            elif msg[0] == 'Stop':
                self.running = False
        except ConnectionRefusedError:
            pass
        except ConnectionResetError:
            pass
        except TimeoutError:
            pass
        return Population

    def start(self,ip,port,printresults = True):
        self.initConnection(ip,port)
        while True:
            p,(Chromosome_Size,Coordinates) = self.getWork()
            if p:
                self.file = p[7]
                self.GA(*p,Chromosome_Size=Chromosome_Size,Coordinates=Coordinates,printresults=printresults)
            # Event().wait(timeout=5)
            time.sleep(5)

    def GA(self, Population_Size, Mutation_Probability, Crossover_Probability, Elite_Percent, Method, Selection_Probability,Migration_Percent,File,Optimal_Solution,Chromosome_Size = None,Coordinates = None,printresults=True):
        self.running = True

        if(not Chromosome_Size or not Coordinates):
            Chromosome_Size,Coordinates = self.read_data(File)      

        Population = self.Generate_Population(Population_Size, Chromosome_Size)
        cache_dict = {}

        Best = self.BestSoFar(Population,Coordinates,cache_dict).copy()
        BestPopulation2 = Best.copy()

        Mutation_Default = Mutation_Probability
        Crossover_Default = Crossover_Probability
        count = 0
        count2 = 0
        trigger = False

        i = 0
        while self.running:

            Population = self.Partially_Mapped_Crossover(Population,Population_Size,Chromosome_Size,Crossover_Probability)
            Population = self.Mutate(Population, Mutation_Probability,Chromosome_Size)
            Population = self.Select_Tournament(Population,Population_Size,Coordinates,Elite_Percent,Selection_Probability,cache_dict)
            BestPopulation = self.BestSoFar(Population, Coordinates,cache_dict).copy()

            if Method == True:
                if count2 == 80:
                    Mutation_Probability = Mutation_Default * 3
                    Crossover_Probability = Crossover_Default * 1.5
                    trigger = True
                    count2=0
                if trigger == True:
                    count = count + 1
                    count2=0
                if count > 20:
                    Mutation_Probability = Mutation_Default
                    Crossover_Probability = Crossover_Default
                    trigger = False
                    count = 0

            if (BestPopulation == BestPopulation2):
                count2 = count2 + 1
            else:
                BestPopulation2 = BestPopulation.copy()
                count2 = 0
                
            if(printresults):
                print(i, end="        ")
                print("Mutation Probability:", end = " ")
                print(Mutation_Probability)
                print(i, end="        ")
                print("Crossover Probability:", end = " ")
                print(Crossover_Probability)
                print(i, end="        ")
                print("Best this generation:", end = " ")
                print(self.Evaluate(BestPopulation,Coordinates,cache_dict))
                print(i, end="        ")
                print("Best so far:", end = " ")
                print(self.Evaluate(Best,Coordinates,cache_dict))
                print("____________________________________________________")

            if (self.Evaluate(Best,Coordinates,cache_dict) == Optimal_Solution):
                self.updatePopulation(Population,Migration_Percent,Coordinates,cache_dict)
                return Best  
            elif self.Evaluate(BestPopulation,Coordinates,cache_dict) < self.Evaluate(Best,Coordinates,cache_dict):
                Population = self.updatePopulation(Population,Migration_Percent,Coordinates,cache_dict)
                Best = self.BestSoFar(Population, Coordinates,cache_dict).copy()
            elif i != 0 and (i % 100) == 0:
                Population = self.updatePopulation(Population,Migration_Percent,Coordinates,cache_dict)
                Best = self.BestSoFar(Population, Coordinates,cache_dict).copy()
            i += 1 
        return Best

if (__name__ == '__main__'):
    def signal_handler(signal, frame):
        sys.exit(0)
    signal.signal(signal.SIGINT, signal_handler)

    worker = GeneticAlgorithm(id = str(uuid.uuid4()))
    worker.start(ip= '192.168.100.40',port = 25565)
    