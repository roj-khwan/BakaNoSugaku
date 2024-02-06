import random as rnd
import math

#customizable part
population_num = 4
num_range = range(0, 30)
crossover_rate = 50
mutation_rate = 10
answer = 30
coeffs = [1, -1, 1, -1, 1, -1, 1, -1, 1, -1]

'''
coeffs = [a, b, c, d]
answer = (a * x) + (b * y) + (c * z) + (d * n)
'''

def Evaluate(chromosome):
    return sum([coeffs[i] * chromosome[i] for i in range(len(coeffs))])

def FitnessEvaluate(population):

    #get each gene value when applied to the equation
    values = []
    for chromosome in population:
        values.append(Evaluate(chromosome))

    #get the accuration of each gene
    #the closest to 1 is the value that have the most accuration
    fitnesses = []
    for value in values:
        dist = abs(value - answer)
        fitnesses.append(1 / (1 + dist))

    #get the cumulation weight to help select the chosen generation for next gen
    cum_weight = []
    for fitness in fitnesses:
        cum_weight.append(fitness/sum(fitnesses))

    return value, fitnesses, cum_weight

def Crossover(population, cum_weight):

    #choose good random gene by using cum weight
    good_population = []
    for i in range(population_num):
        
        stackCum = 0
        rValue = rnd.random()
        for runningIndex in range(population_num):
            
            stackCum += cum_weight[runningIndex]
            if stackCum >= rValue:
                good_population.append(population[runningIndex])
                break

    #randoming choosing pair
    pairing_population = []
    single_population = []
    for pair in good_population:
        if rnd.random() < crossover_rate / 100:
            pairing_population.append(pair)
        else:
            single_population.append(pair)

    #pairing the pairing chromosome with next pairing chromosome
    pair_population = []
    for index in range(len(pairing_population)):
        pair_population.append((pairing_population[index], pairing_population[(index + 1) % len(pairing_population)]))

    #crossovering the random mid point in chromosome
    new_population = []
    for pair in pair_population:
        mid = rnd.randint(1, len(coeffs) - 1)
        new_population.append(pair[0][0:mid] + pair[1][mid:len(coeffs)])

    #add old single population to new one
    new_population += single_population
    
    return new_population

def Mutation(population):
    
    #mutate few index
    mutation_index = []
    for population_index in range(population_num):
        for gene_index in range(len(coeffs)):
            if rnd.random() <= mutation_rate / 100:
                mutation_index.append(population_index * population_num + gene_index * len(coeffs))
                population[population_index][gene_index] = rnd.choice(num_range)

    print(f' {len(mutation_index)}')

    return population

if __name__ == "__main__":

    population = [[rnd.choice(num_range) for i in coeffs] for i in range(population_num)]

    gen_num = 0
    while (True):

        values, fitnesses, cum_weight = FitnessEvaluate(population)

        best_score = math.inf
        best_chromosome = []
        for chromosome in population:
            score = abs(Evaluate(chromosome) - answer)
            if score < best_score:
                best_chromosome = chromosome
                best_score = score


        print(f'Gen {gen_num} best score - {best_score} best chromosome - {", ".join(map(str, best_chromosome))}')
        # print("Population - " + " | ".join([", ".join(map(str, chromosome)) for chromosome in population]))

        if 1 in fitnesses:
            print(population[fitnesses.index(1)])
            break

        new_population = Crossover(population, cum_weight)

        mutate_population = Mutation(new_population)

        gen_num += 1