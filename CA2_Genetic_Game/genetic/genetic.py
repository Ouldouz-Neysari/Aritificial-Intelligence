import random
import math
#TODO assign numbers to variables below
crossoverProbability = 0.5
carryPercentage = 0.5
populationSize =20



class EquationBuilder:
    
    def __init__(self, operators, operands, equationLength, goalNumber):
        self.operators = operators
        self.operands = operands
        self.equationLength = equationLength
        self.goalNumber = goalNumber

        # Create the earliest population at the begining
        self.population = self.makeFirstPopulation()
        
        self.pop_fit_dict={}
        
    def makeFirstPopulation(self):
        
        population=[]
        operand_number=int((self.equationLength+1)/2)
        for j in range(populationSize):
          chro=""
          for i in range(operand_number-1):
            rand_operand_i=random.randrange(len(self.operands))
            rand_operator_i=random.randrange(len(self.operators))
            chro+=str(self.operands[rand_operand_i])
            chro+=str(self.operators[rand_operator_i])

          rand_operand_i=random.randrange(len(self.operands))
          chro+=str(self.operands[rand_operand_i])
          population.append(chro)

        
        return population

        #TODO create random chromosomes to build the early population, and return it
    
    def findEquation(self):
        # Create a new generation of chromosomes, and make it better in every iteration
        while (True):
            random.shuffle(self.population)

            fitnesses = []
            #print("popsize",populationSize,len(self.population))
            for i in range(len(self.population)):
              
              fit_perc=self.calcFitness(self.population[i])
              #print("fit_perc",fit_perc)
              fitnesses.append(fit_perc)
              self.pop_fit_dict[self.population[i]]=fit_perc
              if fit_perc == 0:                
                return self.population[i]

                



                #TODO calculate the fitness of each chromosome
                #TODO return chromosome if a solution is found, else save the fitness in an array

            #TODO find the best chromosomes based on their fitnesses, and carry them directly to the next generation (optional)
            sorted_pop={k: v for k, v in sorted(self.pop_fit_dict.items(), key=lambda item: item[1])}
            sorted_pop_list=list(sorted_pop.keys())           
            carriedChromosomes = []
            for i in range(0, int(populationSize*carryPercentage)):
                carriedChromosomes.append(sorted_pop_list[i]) 

            # A pool consisting of potential candidates for mating (crossover and mutation)    
            matingPool = self.createMatingPool()

            # The pool consisting of chromosomes after crossover
            crossoverPool = self.createCrossoverPool(matingPool)

            # Delete the previous population
            self.population.clear()
            # Create the portion of population that is undergone crossover and mutation
            for i in range(populationSize - int(populationSize*carryPercentage)):
                self.population.append(self.mutate(crossoverPool[i]))
                
            # Add the prominent chromosomes directly to next generation
            self.population.extend(carriedChromosomes)
    
    def createMatingPool(self):
        sorted_pop_fit={k: v for k, v in sorted(self.pop_fit_dict.items(), key=lambda item: item[1])}

        primary_list=[]
        sorted_pop_fit_list=list(sorted_pop_fit.keys())
        for i in range(populationSize):
          for j in range(populationSize-i):
            primary_list.append(sorted_pop_fit_list[i])

        random.shuffle(primary_list)
        matingPool=primary_list[:populationSize]

        #TODO make a brand new custom pool to accentuate prominent chromosomes (optional)
        #TODO create the matingPool using custom pool created in the last step and return it
        return matingPool
    
    def createCrossoverPool(self, matingPool):
        crossoverPool = []

        for i in range(len(matingPool)):
            if random.random() > crossoverProbability:
                #TODO don't perform crossover and add the chromosomes to the next generation directly to crossoverPool
                crossoverPool.append(matingPool[i])
            else:
                par_i1=random.randrange(len(matingPool))
                parent1=matingPool[par_i1]
                par_i2=random.randrange(len(matingPool))
                parent2=matingPool[par_i2]
                cross_point=random.randrange(self.equationLength)
                child1=parent1[:cross_point]+parent2[cross_point:]
                child2=parent2[:cross_point]+parent1[cross_point:]

                crossoverPool.append(str(child1))
                crossoverPool.append(str(child2))
                

                #TODO find 2 child chromosomes, crossover, and add the result to crossoverPool
        return crossoverPool
    
    def mutate(self, chromosome):
        for i in range(3):
          random_index=random.randrange(len(chromosome))
          
          if(random_index%2==0):
            opn_i=random.randrange(len(self.operands))
            chromosome=chromosome[:random_index]+str(self.operands[opn_i])+chromosome[random_index+1:]  
          else:
            opr_i=random.randrange(len(self.operators))
            chromosome=chromosome[:random_index]+str(self.operators[opr_i])+chromosome[random_index+1:]        
        #TODO mutate the input chromosome 
        return chromosome

    def calcFitness(self, chromosome):
        result=0
        st=[]
        i=0
        
        #TODO define the fitness measure here
        while i <(len(chromosome)):
          if(chromosome[i]=="*"):

            opn1=st.pop()
            opn2=chromosome[i+1]

            tmp=int(opn1)*int(opn2)
            st.append(tmp)
            i+=2
          else:
            st.append(chromosome[i])
            i+=1

        result=int(st[0])
        new_length=int((len(st)-1)/2)
        for j in range(new_length):
          if(st[2*j+1]=="+"):
            result+=int(st[2*j+2])
          else:
            result-=int(st[2*j+2])
        
        diff=abs(result-self.goalNumber)


        return diff

          
            
equationLength = int(input())
operands = list(input().split())
operators=list(input().split())
goalNumber = int(input())

equationBuilder = EquationBuilder(operators, operands, equationLength, goalNumber)
equation = equationBuilder.findEquation()
print(equation)