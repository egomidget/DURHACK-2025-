'''python manage.py shell 

import utils 

function(jfkjkr)'''
import networkx as nx #using this for the graph for built in blossom algorithm

#COSINE SIMILARITY FUNCTIONS STUFF:
#sub function
def dot_p(vector1, vector2): #dot product of 2 vectors as list
    dotP = 0
    for i in range(0,len(vector1)-2): #iterating through each index minus 2 to ignore the name and session id
        #multiplying the ith vector values together and adding it to running total
        dotP += vector1[i]*vector2[i]
    return dotP 

#sub function
def sqrt_sum(vector): #calculating size of vector (list representation)
    sumOfSquares = 0
    for vNum in vector[:-2]: #getting the sum of squares of vector
        sumOfSquares += vNum**2
    return sumOfSquares**0.5 #returning the square root of the vector elements added together (size of vector)

#sub function for the vector similarity score
def v_cosine_similarity(vector1,vector2):
    #work out the cos theta between the 2 vectors:
    v1dotv2 = dot_p(vector1,vector2)#do the dot product
    v1size = sqrt_sum(vector1)#do the sqrt of sum for each
    v2size = sqrt_sum(vector2)
    cSimilarity = v1dotv2 / (v1size * v2size)#cos theta = dotp divited by (size1 x size2)
    return cSimilarity #return a value between -1 and 1: 1 means more similar

#FILLING 2D ARRAY FUNCTIONS
def array_matches_list(vectorsArray): #2d vectors input as an array
    dimension = len(vectorsArray) #minus 2 to ignore name and session id
    #use a for loop to iterate through the 2d array for matrix and do the v cosine similarity for 
    similarityArray = [[None] * dimension for _ in range(dimension)]#make list
    for row in range(0,dimension): 
        for col in range(row+1,dimension): #optimised by mirroring over the leading diagonal and only filling in top triangle (change the 0 here to i+1 and mirror) not doing yet incase breaks
            if row == col:
                continue
            similarityValue = v_cosine_similarity(vectorsArray[row],vectorsArray[col])
            similarityArray[row][col] = similarityValue
            similarityArray[col][row] = similarityValue #mirroring across leading diagonal
    return similarityArray

#GETTING SIMILARITY PAIR
#sub function - create graph
def create_graph(arrayOfSimilarities):
    G = nx.Graph()
    G.add_nodes_from(range(len(arrayOfSimilarities)))#adding nodes numbered 0,1,2... for representing the vector nums
    
    #add edges
    for i in range(len(arrayOfSimilarities)):
        for j in range(i + 1, len(arrayOfSimilarities)): #i+1 so onlt doing top triangle
            G.add_edge(i, j, weight=arrayOfSimilarities[i][j])
    return G

#graph and match
def graph_match(arrayOfSimilarities):
    weightedGraph = create_graph(arrayOfSimilarities) #get graph
    return list(nx.algorithms.matching.max_weight_matching(weightedGraph, maxcardinality=True))#get 2 item tuples of pairs. one will be left unpaired

def pairsIntoNames(pairTuples, ogVectorList, similarities): #get format like [("ID1","ID3",0.99),("ID2","ID6",0.67)]
    results = []
    for i, j in pairTuples:
        id1 = ogVectorList[i][-1]  #getting the id from the og vector big list (assuming id is last)
        id2 = ogVectorList[j][-1]
       
        similarity = similarities[i][j]
        results.append((id1, id2, similarity))
    
    return results



        
def input_vectors_output_pairs(allTheAnswers):
    #1.get the sliding scale values for each question (input) and have it as a vector, represented in a list - list for the methods like sum

    #2.get the similarity score from function and have as a 2d array, null for itself position
    similaritiesMatrix = array_matches_list(allTheAnswers)

    #use this array to find best matches
    return pairsIntoNames(graph_match(similaritiesMatrix),allTheAnswers,similaritiesMatrix)


#if time have external ai to asses?