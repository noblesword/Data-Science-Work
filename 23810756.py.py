"""
    CITS1401: Project 1 - S1, 2023
    Student Name: Saif Ali Athyaab
    Student ID: 23810756
    
    This program is written to open, ingest, and pre-process the given file.
    The files are restricted to country information containing 6 columns:
        1. Name of the country - string
        2. Population - integer
        3. Yearly Change - float
        4. Net Change - float
        5. Region - string
    We are interested in finding 4 main statistics for each given input file and input region:
        1. The maximum and minimum population where there's a positive net change
        2. The average and standard deviation in population
        3. The population density of each country
        4. The correlation coefficient between population and land area

"""
#function to return the max and min populations
def getMaxMin(matrix, region):
    names, population= [],[]

    for row in matrix:
        if row[5]==region and float(row[3])>0: #logic to include only postive net change values
            names.append(row[0])
            population.append(int(row[1]))
            
    if not population: # Edge Case - If no data is available in population array, return empty list
        return []    
    
    #extracting the indices to pass on to the names array
    max_index = population.index(max(population))
    min_index = population.index(min(population))

    return [names[max_index], names[min_index]]

#function to return the avg and std dev
def getStats(population):
    num_of_countries = len(population)
    
    if num_of_countries < 1:
        return []  # Edge Case - Empty input gives empty output
    
    average = sum(population) / num_of_countries #first we compute the average by simple sum/n formula
    #then we calculate the variance where avg value is plugged in
    variance = sum((x - average) ** 2 for x in population) / (num_of_countries-1)
    std_dev = variance ** 0.5 #finally we compute the std dev which is root of variance
    return [round(average,4), round(std_dev,4)]

#function to return the densities of countries
def getDensity(names,population,land_area):
    density = []
    for i in range(len(population)):
        if land_area[i] == 0: #Edge Case - check for zeroes to prevent divide by zero scenario
            density.append((names[i], None))
        else:
            density.append((names[i], round((population[i]/land_area[i]),4)))
    
    #sorting the countries list
    country_with_density = sorted(density, key=lambda x: x[1], reverse=True)
    
    return country_with_density

#function to return the correlation between population and land area columns
def getCorrelation(population, land_area):
    n_pop= len(population)
    n_area = len(population)
    
    # Edge Case - Check if population and land_area are not empty
    if not population or not land_area:
        return 0
    
    # Edge Case - Check if population and land_area have the same length
    if n_pop != n_area:
        return 0
    
    #simple average calculation
    avg_pop = sum(population) / n_pop
    avg_area = sum(land_area) / n_area
    
    #first we calculate the covariance
    covariance=0
    for i in range(n_pop):
        covariance += (population[i] - avg_pop) * (land_area[i] - avg_area)

    covariance /= n_pop
    
    #next we calculate the std dev for population, area
    std_dev_pop = 0
    std_dev_area = 0
    for i in range(n_pop):
        std_dev_pop += (population[i] - avg_pop) ** 2
        std_dev_area += (land_area[i] - avg_area) ** 2
    
    std_dev_pop = (std_dev_pop / n_pop) ** 0.5
    std_dev_area = (std_dev_area / n_area) ** 0.5
    
    # Edge Case - Check if standard deviations are not zero
    if std_dev_pop == 0 or std_dev_area == 0:
        return 0

    # Calculate correlation coefficient from covariance and std dev of population and area
    corr_coef = covariance / (std_dev_pop * std_dev_area)

    return round(corr_coef,4) 

#main function where program execution starts and calls other functions for completing the statistical tasks
def main(csvfile, region):
    
    country_file = open(csvfile,'r') #opening the given file in read mode
    matrix=[] #initialising the data structure where processed file data will be stored
    
    #iterating over each line in the file
    for x in country_file:
        line=x.split(",") #splitting each line into a list of elements
        line=[value.rstrip("\n") for value in line] #eliminating the newline character from each list
        matrix.append(line) #storing the list of line into the 2-D matrix
    
    #function call for 1st statistical task
    #have called by passing through matrix directly due to net change condition
    MaxMin = getMaxMin(matrix,region)
    #initialising empty arrays for each column
    names, population, net_change, land_area = [],[],[],[]
    #iterating row-wise to populate the initialised column arrays
    for row in matrix:
        #considering only the rows with the input region to save space
        if row[5]==region:
            names.append(row[0])
            population.append(int(row[1]))
            # not extracted yearly change as its not used to save space
            net_change.append(float(row[3]))
            land_area.append(int(row[4]))
           
    country_file.close() #closing the opened file for graceful termination
    
    #function calls for remaining 3 statistical tasks
    stdvAverage=getStats(population)
    density = getDensity(names,population,land_area)   
    corr = getCorrelation(population,land_area)
    
    return MaxMin, stdvAverage, density, corr