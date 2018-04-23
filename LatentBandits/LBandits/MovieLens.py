'''
Created on Mar 24, 2018

@author: subhomuk
'''

import csv

class Movielens(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
     
     
    def read_file(self,filename):
        
        with open(filename, 'rb') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
            for row in spamreader:
                #print ', '.join(row)
                print row
     
        
if __name__ == "__main__":
    
    obj = Movielens()
    
    #filename = 'env/MovieLens/movies.csv'
    #filename = 'env/MovieLens/links.csv'
    filename = 'env/MovieLens/tags.csv'
    
    obj.read_file(filename)
    
    
    
    
    
    
    
    
        