import numpy as np

class individual:
    def __init__(self, i = -1, g = np.array([]), e = 0, f = 0):
        self.id = i
        self.genes = g
        self.energy = e
        self.fitness = f

    def __repr__(self):
        g = ""
        for i in self.genes:
            g = g + str(i) + "\n"
        return "ID: " + str(self.id) + "\nGenes:\n" + g +  "\nEnergy: " + str(self.energy) + "\nFitness: " + str(self.fitness)

    #Felipe/Alan
    def eatPacket(self, packet = None):
        """Alimentar a individuo con packet.

        Args:
            packet: El paquete parseado para alimentar a la población (def = None)
        """
        print("Eat packet")

    #Felipe/Alan
    def mutate(self):
        """Mutar el individuo."""

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
        print("Initialize population")

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