'''python manage.py shell 

import utils 

function(jfkjkr)'''

#COSINE SIMILARITY FUNCTIONS STUFF:
def dot_p(vector1, vector2): #dot product of 2 vectors as list
    dotP = 0
    for i in range(0,len(vector1)): #iterating through each index
        #multiplying the ith vector values together and adding it to running total
        dotP += vector1[i]*vector2[i]
    return dotP 

def sqrt_sum(vector): #calculating size of vector (list representation)
    sumOfSquares = 0
    for vNum in vector: #getting the sum of squares of vector
        sumOfSquares += vNum**2
    return sumOfSquares**0.5 #returning the square root of the vector elements added together (size of vector)

#function for the vector similarity score
def v_cosine_similarity(vector1,vector2):
    #work out the cos theta between the 2 vectors:
    v1dotv2 = dot_p(vector1,vector2)#do the dot product
    v1size = sqrt_sum(vector1)#do the sqrt of sum for each
    v2size = sqrt_sum(vector2)
    cSimilarity = v1dotv2 / (v1size * v2size)#cos theta = dotp divited by (size1 x size2)
    return cSimilarity #return a value between -1 and 1: 1 means more similar

#FILLING 2D ARRAY FUNCTIONS
def array_matches_list():
    #use a for loop to iterate through the 2d array for matrix and do the v cosine similarity for 
    for i in range:
        pass

#1.get the sliding scale values for each question and have it as a vector, represented in a list - list for the methods like sum

#2.get the similarity score from function and have as a 2d array, null for itself position


#use this array to find best matches - need an algorithm for this!

#if time have external ai to asses?