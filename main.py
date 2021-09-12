import numpy as np
import random

#Tamaño de matriz para la inicialización inicial de la población
initialMatrixSize = 5

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
        fMarkov = self.genes[packetAnt]
        packets = self.choosePackets(fMarkov)

        for i in packets:
            if i == packet:
                self.fitness+1
                break

        print("Eat packet")

    def choosePackets(self, fMarkov = []):
        """Elegir apuesta individuo.
        
        Args:
            fMarkov: Fila en la matriz de markov del agente, que corresponde al paquete anteriormente llegado
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
        for i in self.genes.itervalues():
            rand = random.random()
            if rand <= mutacion:
                n1 = random.randint(0,len(i)-1)
                n2 = random.randint(0,len(i)-1)
                temp = i[n1][1]
                i[n1][1] = i[n2][1]
                i[n2][1] = temp 
    
    # mutacion es el porcentaje de mutacion para cada gen del individuo. Escogiendo
    # dos random se logra intercambiar las probabilidades de cada packet 



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
            gene = {}
            for j in range(initialMatrixSize):
                packetID = str(hash(random.random()))
                g = []
                m = 100
                for k in range(initialMatrixSize):
                    val = random.randint(0, m)
                    if(k == initialMatrixSize - 1):
                        val = m
                    m = m - val
                    g.append([str(hash(random.random())), val / 100])
                gene[packetID] = g
            self.population.append(individual(i, gene, 0, 0))


    #---
    def feedPop(self, packet = None):
        """Alimentar a la poblacion de este modelo.

        Args:
            packet: El paquete con que se va a alimentar (def = None)
        """
        for i in self.population:
            i.eatPacket(packet)

    def selectParents(self, num = 0):
        """Seleccionar una cantidad num de padres del modelo y retornar como lista.
        
        Args:
            num: Cantidad de padres a seleccionar (def = 0)
        
        Returns:
            l: Lista de padres
        """

    def signalAmount(self):
        """Calcular y retornar la cantidad de feromona/señal que este modelo emite.
        
        Returns:
            f: Cantidad de feromona que el modelo emite
        """

#Martin
def parsePacket(file = None):
    """Interpretar 1 linea del archivo de entrada, retornar el resultado.

    Args:
        file: Archivo a leer (def = None)
    
    Returns:
        p: Paquete procesado
    """
    print("Parse 1 packet into model format")

def crossIndividuals(parent1 = None, parent2 = None):
    """Hacer 2 hijos a partir de los padres y retornarlos.

    Args:
        parent1: Padre 1 para crear un hijo (def = None)
        parent2: Padre 2 para crear un hijo (def = None)
    
    Returns:
        h1, h2: Los 2 hijos
    """
    print("Make 2 children from parents")


#Creamos los modelos
selfModel = model()
selfModels = [selfModel]
nonSelfModels = []

#Inicializamos la poblacion
selfModel.initializePop()

print(selfModel)

while(True):
    models = selfModels + nonSelfModels
    #Leemos y procesamos el siguiente paquete
    packet = parsePacket()

    #Alimentamos a el/los modelos
    for i in models:
        i.feedPop(packet)
    
    #Realizamos la seleccion de padres
    for i in models:
        parents = i.selectParents()

        newPop = []
        #Realizamos la cruza
        for j in range(0, len(parents), 2):
            h1, h2 = crossIndividuals(parents[j], parents[j + 1])
            h1.mutate()
            h2.mutate()
            newPop.append(h1)
            newPop.append(h2)
        i.population = newPop


#Este es el ciclo de vida basico para el modelo, le falta la interaccion entre los 2+ modelos