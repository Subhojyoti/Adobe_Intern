'''
Created on Sept 5, 2016

@author: Subhojyoti
'''


import matplotlib
import numpy
import fileinput
import threading
import  multiprocessing
from multiprocessing import Manager
#matplotlib.use('backend_interagg')
#matplotlib.use('module://backend_interagg')
matplotlib.use('TkAgg')
from matplotlib import pyplot as plt

class plot4(object):

    def __init__(self):
        '''
        Constructor
        '''

    #self.outfile='NewExpt1/expt2/'

    def column(self,A, j):
        return [A[i][j] for i in range(len(A))]

    def transpose(self,A):
        return [self.column(A, j) for j in range(len(A[0]))]

    def plot_show(self,actionRegret,legend):

        episode=[]

        for t in range(0,self.timestep):
            actionRegret[t]=actionRegret[t]/self.limit
            episode.append(t);


        #print self.actionRegret
        #plot1,=plt.plot(episode,actionRegret,'r--',color='red',label='ClusUCB');
        #plot2,=plt.plot(episode,actionRegret1,color='green',label='MOSS');
        ax1 = plt.subplot(111)
        plt.ylabel('Cumulative Regret',fontsize=18)
        plt.xlabel('timesteps',fontsize=18)
        ax1.plot(episode, actionRegret,label=legend)


        plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=2,
               ncol=2, mode="expand", borderaxespad=0.)

        plt.show()

    def fileReadWrite(self,id,name,filename,actionRegret,timestep):


        t=0
        count=0
        for line in fileinput.input([filename]):

            try:

                line1=line.split("\n")
                take=float(line1[0])


                actionRegret[t]=actionRegret[t]+take
                t=t+1
                if t==self.timestep:
                    t=0
                    count=count+1
                    print str(filename)+": "+str(count)

                #prev=take
                '''
                if count==6:
                    print t
                    break
                '''
            except ValueError,e:
                print  str(filename)+ " Error:" +str(e) +": Count: " +str(count)+ " t: "+str(t)
        #print self.actionRegret
        print  str(filename)+" done"
        
        f = open(str(self.outfile+'plotFinal')+str(name)+".txt", 'w')
        for r in range(len(actionRegret)):
            f.write(str(r+1)+"\t"+str((actionRegret[r]/self.limit))+"\n")
        f.close()
        
        f1 = open(str(self.outfile)+str("comp_subsampled_"+name)+".txt", 'w')
        
        self.subsampled = []
        divid = int(timestep/20)
        for r in range(len(actionRegret)):
            if (r+1)%divid == 0:
                self.subsampled.append(actionRegret[r]/self.limit)
                f1.write(str(r+1)+"\t"+str((actionRegret[r]/self.limit))+"\n")
        f1.close()
        

    def fileRead(self,id,name,filename):
    #def regretWeightsGraph(filename,filename1,filename2):
        with open(str(self.outfile+'plotFinal')+str(name)+".txt", 'r') as infile:
            lines = infile.readlines()
            #print lines

        regret =  [eval(line.split("\t")[1]) for line in lines]
        #print "lines: " + str(lines)
        #data = transpose(lines)



        scale = [eval(line.split("\t")[0]) for line in lines]

        print  str(self.outfile)+str(name)+".txt"+" done"

        return regret,scale
    
    def fileRead1(self,id,name,filename):
    #def regretWeightsGraph(filename,filename1,filename2):
        with open(str(self.outfile+'comp_subsampled_')+str(name)+".txt", 'r') as infile:
            lines = infile.readlines()
            #print lines

        regret =  [eval(line.split("\t")[1]) for line in lines]
        #print "lines: " + str(lines)
        #data = transpose(lines)



        scale = [eval(line.split("\t")[0]) for line in lines]

        print  str(self.outfile)+str(name)+".txt"+" done"

        return regret,scale


    '''
    def fileRead(self,id,name,actionRegret):


        t=0
        count=0
        for line in fileinput.input([str(self.out_file)+str(name)+".txt"]):

            try:



                #line1 = [eval(line.split("\t")[1]) for line in line]
                #print line1





                #line1=line.split("\n")
                take=float(line[0])


                actionRegret[t]=actionRegret[t]+take
                t=t+1
                if t==self.timestep:
                    t=0
                    count=count+1
                    print str(self.out_file)+str(id)+": "+str(count)

                #prev=take
                #if count==61:
                #    print t
            except ValueError,e:
                print  str(self.out_file)+str(id)+ " Error:" +str(e) +": Count: " +str(count)+ " t: "+str(t)
        #print self.actionRegret
        print  str(self.out_file)+str(id)+" done"
        return actionRegret
    '''
    #def regretWeightsGraph(filename,filename1,filename2,filename3,filename4,filename5,filename6):
    #def regretWeightsGraph(filename,filename1,filename2,filename3):
    #def regretWeightsGraph(self,filename,filename1,filename2,filename3,filename4):
    #def regretWeightsGraph(self,filename,filename1,filename2,filename3,filename4,filename5):
    def regretWeightsGraph(self, limit, timestep, outfile, filename, takeName, algoname):

        self.limit = limit
        self.timestep = timestep
        #self.timestep=300000

        #print self.actionRegret1
        #print self.actionRegret
        
        
        self.outfile = outfile
        
        #takeName = "CustomEXP0RR2"
        self.takeName = takeName
        self.filename = filename

        self.actionRegret=[0.0 for i in range(self.timestep)]
        '''
        self.actionRegret1=[0.0 for i in range(self.timestep)]
        self.actionRegret2=[0.0 for i in range(self.timestep)]
        self.actionRegret3=[0.0 for i in range(self.timestep)]
        self.actionRegret4=[0.0 for i in range(self.timestep)]
        self.actionRegret5=[0.0 for i in range(self.timestep)]
        '''

        jobs=[]
        
        process=multiprocessing.Process(target=self.fileReadWrite,args=(0,self.takeName,self.filename, self.actionRegret,self.timestep))
        jobs.append(process)
        '''
        process1=multiprocessing.Process(target=self.fileReadWrite,args=(1,'clUCB_3',filename1, self.actionRegret1))
        jobs.append(process1)

        process2=multiprocessing.Process(target=self.fileReadWrite,args=(2,'clUCB_5',filename2, self.actionRegret2))
        jobs.append(process2)

        process3=multiprocessing.Process(target=self.fileReadWrite,args=(3,'clUCB_10',filename3, self.actionRegret3))
        jobs.append(process3)

        process4=multiprocessing.Process(target=self.fileReadWrite,args=(4,'clUCB_15',filename4, self.actionRegret4))
        jobs.append(process4)

        process5=multiprocessing.Process(target=self.fileReadWrite,args=(5,'clUCB_25',filename5, self.actionRegret4))
        jobs.append(process5)
        '''


        for job in jobs:
            job.start()

        for job in jobs:
            job.join()



        plotRegret,scale=self.fileRead(0,self.takeName,self.actionRegret)
        plotRegret1,scale1=self.fileRead1(0,self.takeName,self.actionRegret)
        
        
        
        #print self.actionRegret,self.actionRegret1,self.actionRegret2,self.actionRegret3


        #print self.actionRegret
        #plot1,=plt.plot(episode,actionRegret,'r--',color='red',label='ClusUCB');
        #plot2,=plt.plot(episode,actionRegret1,color='green',label='MOSS');
        ax1 = plt.subplot(211)
        plt.ylabel('Cumulative Regret',fontsize=18)
        plt.xlabel('timesteps',fontsize=18)
        ax1.plot(scale, plotRegret,'r+',label=algoname)
        
        ax2 = plt.subplot(212)
        plt.ylabel('Cumulative Regret',fontsize=18)
        plt.xlabel('timesteps',fontsize=18)
        ax2.plot(scale1, plotRegret1,'r+',label=algoname)
        

        plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=2,
               ncol=2, mode="expand", borderaxespad=0.)

        plt.show()
        #plt.ion()




if __name__ == "__main__":

    obj = plot4()
    
    limit = 1
    timestep = 4000000
    outfile = "NewExpt1/expt6/"
    takeName = "NewMetaEXP0RR1"
    filename = str(outfile)+"testRegret"+str(takeName)+".txt"
    algoname = takeName
    
    obj.regretWeightsGraph(limit, timestep, outfile, filename, takeName, algoname)
