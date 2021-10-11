import numpy as np
import random, copy
import matplotlib.pyplot as plt

#Tamaño de matriz para la inicialización inicial de la población
initialMatrixSize = 2
contadorIndividuos = 0

#Contador para tipos de paquetes, para actualizar los genes de los agentes y el comodin
packetList = {}

class individual:
    #El diccionario "genes" tiene la forma:
    # {
    #   packetID: [[packetID, probability], ..., [packetID, probability]], 
    #   .
    #   .
    #   .
    #   packetID: [[packetID, probability], ..., [packetID, probability]]
    # }
    # packetID es el string resultante del hash (o lo que sea que se vaya a usar) de identificación de cada tipo de paquete
    def __init__(self, i = -1, g = {}, e = 0, f = 0):
        self.id = i
        self.genes = g
        self.energy = e
        self.fitness = f

    def __repr__(self):
        g = ""
        for i in self.genes:
            g = g + str(i) + ": " + str(self.genes[i]) + "\n"
        return "ID: " + str(self.id) + "\nGenes:\n" + g +  "\nEnergy: " + str(self.energy) + "\nFitness: " + str(self.fitness) + "\n--------------------\n"

    #Felipe/Alan
    def eatPacket(self, packet = None, packetAnt = None):
        """Alimentar a individuo con packet.

        Args:
            packet: El paquete parseado para alimentar a la población (def = None)
            packetAnt: El paquete parseado anteriormente (def = None)
        """
        #print(packetAnt)
        if(packetAnt == None or packetAnt not in self.genes.keys()):
            packetAnt = "*"
        fMarkov = self.genes[packetAnt]
        packets = self.choosePackets(fMarkov)
        if packet in packets or (packet not in self.genes.keys() and "*" in packets):
            self.fitness = self.fitness + 1

    def choosePackets(self, fMarkov = []):
        """Elegir apuesta individuo.
        
        Args:
            fMarkov: Fila en la matriz de markov del agente, que corresponde al paquete anteriormente llegado

        Returns:
            packets: Paquetes a los cuales se le apuesta.
        """
        packets = [] # Se guardaran las mejores opciones
        margen = 0.1
        max = [None, 0]
        for i in fMarkov:
            if max[1] <= i[1]:
                max = i
        packets.append(max[0])

        for i in fMarkov:
            if i[1] >= max[1]-(max[1]*margen) and max != i:
                packets.append(i[0])
        
        return packets
    
    #Felipe/Alan
    def mutate(self):
        """Mutar el individuo."""
        mutacion = 0.05
        for i in self.genes.keys():
            rand = random.random()
            if rand <= mutacion:
                n1 = random.randint(0,len(self.genes[i])-1)
                n2 = random.randint(0,len(self.genes[i])-1)
                temp = self.genes[i][n1][1]
                self.genes[i][n1][1] = self.genes[i][n2][1]
                self.genes[i][n2][1] = temp 
    
    # mutacion es el porcentaje de mutacion para cada gen del individuo. Escogiendo
    # dos random se logra intercambiar las probabilidades de cada packet    

    def updateGenesWithPacket(self, packet = None):
        """Actualizar los genes de los individuos para incluir el paquete 'packet', visto muchas veces.

        Args:
            packet: El paquete que se quiere agregar a los genes de la poblacion (def = None)
        """
        for i in self.genes:
            newPacketChance = round(self.genes[i][0][1] / 2, 2)
            newJchance = self.genes[i][0][1] - newPacketChance
            self.genes[i].append([packet, newPacketChance])
            self.genes[i][0][1] = newJchance
        #print(selfModel)

        self.genes[packet] = []    
        geneLine = []
        m = 100
        for i in self.genes:
            val = random.randint(0, m)
            m = m - val
            geneLine.append([i, val / 100])
        geneLine[-1][1] = (val + m) / 100
        self.genes[packet] = geneLine
        #print("Post update:")
        #print(self)
        #input()



class model:
    def __init__(self, pop = [], signal = False):
        self.population = pop
        self.signal = signal

    def __repr__(self):
        return str(self.population)

    #Matias
    def initializePop(self, num = 100):
        """Generar población inicial.
    
        Args:
            num: Tamaño de la población (def = 100)
        """
        for i in range(num):
            gene = {
                "*" : [["*", 1]]
            }
            self.population.append(individual(i, gene, 0, 0))
        contadorIndividuos = num


    #---
    def feedPop(self, packet = None, lastPacket = None):
        """Alimentar a la poblacion de este modelo.

        Args:
            packet: El paquete con que se va a alimentar (def = None)
            lastPacket: Paquete anteriormente recibido
        """
        for i in self.population:
            i.eatPacket(packet, lastPacket)

    #Felipe/Alan
    def selectParents(self, num = 2):
        """Seleccionar num padres (usando torneo) y retornarlos como lista.
        
        Returns:
            p: Lista de padres
        """
        p = []
        for i in range(num):
            p.append(self.torneoSelect(2))
        
        return p

    def torneoSelect(self, size = 2):
        """ Seleccionar mejor opcion, retornandola. Si ambos son iguales, se retorna uno al azar.

        Returns:
            o1 o o2: Mejor opcion.
        """
        #popCopy = copy.deepcopy(self.population)
        #random.shuffle(popCopy)
        #participants = popCopy[0:size]
        #participants.sort(key = orderByFitness, reverse = True)
        #return participants[0]

        popIDs = []
        for i in range(size):
            popIDs.append(1)
        for i in range(len(self.population) - size):
            popIDs.append(0)

        random.shuffle(popIDs)
        participants = [i for i, j in zip(self.population, popIDs) if j]
        participants.sort(key = orderByFitness, reverse = True)
        return copy.deepcopy(participants[0])

        #o1 = random.choice(self.population)
        #o2 = random.choice(self.population)
        #if o1.fitness > o2.fitness:
        #    return o1
        #elif o1.fitness < o2.fitness:
        #    return o2
        #else:
        #    return random.choice([o1,o2])

    def checkDictionaryUpdate(self):
        """Revisar si hay algun paquete nuevo que agregar a su matriz de markov
        """
        commonPackets = list(dict(filter(lambda p: int(p[1]) >= 10, packetList.items())).keys())
        for i in commonPackets:
            for j in self.population:
                if(i not in j.genes):
                    j.updateGenesWithPacket(i)

    def signalAmount(self):
        """Calcular y retornar la cantidad de feromona/señal que este modelo emite.
        
        Returns:
            f: Cantidad de feromona que el modelo emite
        """

def elitism(population,news):
    """Ordenar segun fitness y eliminar a los peores reemplazandolos por los hijos creados.
        
    Args:
        population: Poblacion que va a conservar a los mejores
        news: Hijos creados que se agregaran a la poblacion (population)
    """
    sorted(population, key = orderByFitness)
    population = population[:(len(population)-len(news))]
    population.extend(news)

def orderByFitness(x):
    return x.fitness

#Martin
def makeUsableList(inputList = None):
    """Recibir una lista con todos los elementos de la entrada, retornar una lista con solo los elementos relevantes.
    Esto depende mucho de la entrada y su formato, de momento se trabaja igual como se hacia en CyES, quedando abierto a cambios una vez que se sepa como van a llegar los datos que nos van a entregar
    
    Args:
        inputList: Lista completa (def = None)

    Returns:
        usableList: Lista con solo los elementos relevantes
    """
    usableList = []
    usableList.append(inputList[7])
    usableList.append(inputList[8])
    usableList.append(inputList[9])
    
    for i in range(11,19):
        usableList.append(inputList[i])
    
    for i in range(25,54):
        usableList.append(inputList[i])
            
    return usableList
    
def parsePacket(file = None):
    """Interpretar 1 linea del archivo de entrada, retornar el resultado.

    Args:
        file: Archivo a leer (def = None)
    
    Returns:
        p: Paquete procesado, en forma de string
    """
    p = []
    line = file.readline()
    for elem in line.split():
        p.append(int(elem))
    p = ''.join(map(str, makeUsableList(p)))
    return p
    
#Felipe/Alan
def crossIndividuals(parent1 = {}, parent2 = {}):
    """Hacer 2 hijos a partir de los genes de los padres y retornarlos.

    Args:
        parent1: Genes del padre 1 para crear un hijo (def = None)
        parent2: Genes del padre 2 para crear un hijo (def = None)
    
    Returns:
        h1, h2: Los 2 hijos
    """
    d1 = {}
    d2 = {}
    c = 0
    for i in parent1.keys():
        if c % 2 == 0:
            d1[i] = parent1[i]
            d2[i] = parent2[i]
        else:
            d1[i] = parent2[i]
            d2[i] = parent1[i]
        c = c + 1
    global contadorIndividuos
    contadorIndividuos = contadorIndividuos + 2
    return individual(contadorIndividuos-1,d1,0,0),individual(contadorIndividuos,d2,0,0)

def evaluatePop(model = None):
    """Obtener una evaluación de la población del modelo "model".

    Args:
        model: El modelo a evaluar (def = None)

    Returns:
        totalFitness: La suma de las fitness de toda la población.
    """
    totalFitness = 0
    for i in model.population:
        totalFitness = totalFitness + i.fitness

    return totalFitness

#Creamos los modelos
selfModel = model()
selfModels = [selfModel]
nonSelfModels = []

#Inicializamos la poblacion
selfModel.initializePop()

#print(selfModel)

file1 = open("testInput/datosNormales.txt", "rt")
file2 = open("testInput/datosAtaque.txt", "rt")

currentFile = file1

ticks = 0

fitnessHistory = []

lastPacket = None

while(True):
    ticks = ticks + 1
    models = selfModels + nonSelfModels
    if(ticks == 251):
        currentFile = file2
    #Leemos y procesamos el siguiente paquete
    try:
        packet = parsePacket(currentFile)
    except(IndexError):
        print("Parece que se terminó el archivo")
        plt.plot(fitnessHistory)
        plt.show()
        print(models)
        exit(0)

    if(packet in packetList):
        packetList[packet] = packetList[packet] + 1
    else:
        packetList[packet] = 1

    #Alimentamos a el/los modelos
    for i in models:
        i.feedPop(packet, lastPacket)

    fitnessHistory.append(evaluatePop(i))

    #print(selfModel)
    #input()
    percentageElitism = 0.4
    #Esto controla cada cuantas generaciones se realiza una cruza. (def = 1, osea en todas)
    if(not ticks % 1):
        print(ticks)
        #Realizamos la seleccion de padres
        for i in models:
            parentsSize = int(len(i.population)*(1-percentageElitism))
            parents = i.selectParents(parentsSize if parentsSize%2==0 else parentsSize+1)
            #Realizamos la cruza
            new = []
            for j in range(0, len(parents), 2):
                h1, h2 = crossIndividuals(parents[j].genes, parents[j + 1].genes)
                h1.mutate()
                h2.mutate()
                new.append(h1)
                new.append(h2)
            elitism(i.population,new)
                    
        #Actualizamos la matriz de todos los agentes si hay un nuevo paquete que agregar a sus genes
        i.checkDictionaryUpdate()
            
    lastPacket = packet


#Este es el ciclo de vida basico para el modelo, le falta la interaccion entre los 2+ modelos