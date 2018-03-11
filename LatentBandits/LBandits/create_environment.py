'''
Created on Jan 27, 2016

@author: Subhojyoti
'''

import math
import random
import numpy
import fileinput

class CreateEnvironment(object):
    '''
    classdocs
    '''


    def __init__(self,filename):
        '''
        Constructor
        '''
        self.filename = filename


    def readenv(self):
        data=[]
        #filename="env/env1/AP8.txt"
        for line in fileinput.input([self.filename]):

            try:
                line1 = [line.split(", ") or line.split("\n") ]
                #print numpy.shape(line1)
                #print line1
                take=[]
                for i in range(len(line1[0])):
                    take.append(float(line1[0][i]))
                #print take
                data.append(take)
            except ValueError,e:
                print e
        #print data
        self.means=(data[0])
        self.variance=(data[1])

    def create(self, rank, users, numActions, gap):
    
        #Set the environment

        self.numActions = numActions
        self.users = users
        self.rank = rank
        self.gap = gap

        '''
        self.means =[]
        self.variance=[]
        self.readenv()
        '''

        self.means =[[0.0 for i in range(self.numActions)] for j in range(0,self.users)]
        self.variance=[[0.0 for i in range(self.numActions)] for j in range(0,self.users)]
        
        '''
        for i in range(0,self.rank):
            self.means[i][self.numActions - i -1] = 1.0
        '''
        
        #for i in range(self.rank,self.users):
        for i in range(0,self.users):
            
            take=[0.0 for r in range(0,self.numActions)]
            pick_max = random.randint(self.numActions - self.rank, self.numActions -1)
            
            self.means[i][pick_max] = random.uniform(self.gap, 1.0)
            take[pick_max] = self.means[i][pick_max]
            
            print "max: " + str(take[pick_max])
            sum_take = 0.0
            for j in range(0,self.numActions):
                
                if j!= pick_max:
                    take[j] = (random.uniform(0.0 , (1.0 - take[pick_max])/(self.numActions - 1)))
                    sum_take = sum_take + take[j]
            
            #sum_take  = sum(take)
            
            print sum_take
            for j in range(0,self.numActions):
                
                if j!= pick_max:
                    self.means[i][j] = take[j]
            
            
            '''
            #swap
            max_item = max(range(0,self.numActions), key=lambda p: self.means[i][p])
            pick_max = random.randint(self.numActions - self.rank, self.numActions -1)
            #print pick_max
            temp = self.means[i][pick_max]
            self.means[i][pick_max] = self.means[i][max_item]
            self.means[i][max_item] = temp
            '''
                
        f = open(self.filename, 'w')
        for j in range(0,self.users):
            print sum(self.means[j])
            f.writelines("%s\n" % (', '.join(["%.3f" % i for i in self.means[j]])))
            #f.writelines("%s\n" % (', '.join(["%.3f" % i for i in self.variance])))
        f.close()


        print self.means
        print self.variance


if __name__ == "__main__":

        numActions = 64
        users = 64
        rank = 2
        gap = 0.5
        filename = 'env/env1/AP8.txt'
        
        obj=CreateEnvironment(filename)
        obj.create(rank, users, numActions, gap)

                