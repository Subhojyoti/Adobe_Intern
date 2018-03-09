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

    out_file='NewExpt/expt5/'

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

        f = open(str(self.out_file+'plotFinal')+str(name)+".txt", 'w')
        for r in range(len(actionRegret)):
            f.write(str(r+1)+"\t"+str((actionRegret[r]/self.limit))+"\n")
        f.close()
        
        f1 = open(str(self.out_file)+str("comp_subsampled_"+name)+".txt", 'w')
        
        divid = int(timestep/10)
        for r in range(len(actionRegret)):
            if (r+1)%divid == 0:
                f1.write(str(r+1)+"\t"+str((actionRegret[r]/self.limit))+"\n")
        f1.close()

    def fileRead(self,id,name,filename):
    #def regretWeightsGraph(filename,filename1,filename2):
        with open(str(self.out_file+'plotFinal')+str(name)+".txt", 'r') as infile:
            lines = infile.readlines()
            #print lines

        regret =  [eval(line.split("\t")[1]) for line in lines]
        #print "lines: " + str(lines)
        #data = transpose(lines)



        scale = [eval(line.split("\t")[0]) for line in lines]

        print  str(self.out_file)+str(name)+".txt"+" done"

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
    def regretWeightsGraph(self,filename):

        self.limit=100
        self.timestep=2000
        #self.timestep=300000

        #print self.actionRegret1
        #print self.actionRegret

        takeName="GLBUCB0RR1"

        self.actionRegret=[0.0 for i in range(self.timestep)]
        '''
        self.actionRegret1=[0.0 for i in range(self.timestep)]
        self.actionRegret2=[0.0 for i in range(self.timestep)]
        self.actionRegret3=[0.0 for i in range(self.timestep)]
        self.actionRegret4=[0.0 for i in range(self.timestep)]
        self.actionRegret5=[0.0 for i in range(self.timestep)]
        '''



        jobs=[]


        process=multiprocessing.Process(target=self.fileReadWrite,args=(0,takeName,filename, self.actionRegret,self.timestep))
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



        self.actionRegret,scale=self.fileRead(0,takeName,self.actionRegret)
        '''
        self.actionRegret1,scale=self.fileRead(1,'clUCB_3',self.actionRegret1)
        self.actionRegret2,scale=self.fileRead(2,'clUCB_5',self.actionRegret2)
        self.actionRegret3,scale=self.fileRead(3,'clUCB_10',self.actionRegret3)
        self.actionRegret4,scale=self.fileRead(4,'clUCB_15',self.actionRegret4)
        self.actionRegret5,scale=self.fileRead(5,'clUCB_25',self.actionRegret5)
        '''
        #print self.actionRegret,self.actionRegret1,self.actionRegret2,self.actionRegret3


        #print self.actionRegret
        #plot1,=plt.plot(episode,actionRegret,'r--',color='red',label='ClusUCB');
        #plot2,=plt.plot(episode,actionRegret1,color='green',label='MOSS');
        ax1 = plt.subplot(111)
        plt.ylabel('Cumulative Regret',fontsize=18)
        plt.xlabel('timesteps',fontsize=18)
        ax1.plot(scale, self.actionRegret,'r+',label="Algorithm")
        '''
        ax1.plot(scale, self.actionRegret1,'r.',label="ClusUCB(Clustering,p=3)")
        ax1.plot(scale, self.actionRegret2,'b--',label="ClusUCB(Clustering,p=5)")
        ax1.plot(scale, self.actionRegret3,'k:',label="ClusUCB(Clustering,p=10)")
        ax1.plot(scale, self.actionRegret4,'y-',label="ClusUCB(Clustering,p=15)")
        ax1.plot(scale, self.actionRegret5,'m',label="ClusUCB(Clustering,p=25)")
        '''


        plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=2,
               ncol=2, mode="expand", borderaxespad=0.)

        plt.show()
        #plt.ion()




if __name__ == "__main__":

    obj=plot4()

    #regretWeightsGraph('ucbTest1/testRN110UCB_2m_0.47.txt','ucbTest1/testR1_2m_0.47.txt','ucbTest/testRNUCB1_new.txt', "Regret of UCB\n10 actions, 1 million rounds")
    #regretWeightsGraph('ucbTest1/testRNUCB_new.txt','ucbTest1/testR_new.txt','ucbTest1/testRNUCB1_new.txt', "Regret of UCB\n10 actions, 1 million rounds")
    #regretWeightsGraph('testExp/testCLUCB1000_final.txt','testExp/testR_new7.txt','testExp/testUCB.txt','testExp/testR_new6.txt', "Regret of UCB\n10 actions, 1 million rounds")

    #obj.regretWeightsGraph('testFinal3/clUCB6.txt','testFinal3/testMOSS1.txt', 'testFinal3/testUCB11.txt' ,'testFinal3/testEps1.txt','testFinal3/testEpsn1.txt','testFinal3/testEXP1.txt','testFinal3/testUCBD1.txt','testFinal3/testUCB21.txt','testFinal3/testTS1.txt','testFinal3/testUCBT1.txt','testFinal3/testUCBV1.txt','testFinal3/testKLUCB1.txt', "Regret of UCB\n10 actions, 1 million rounds")

    #obj.regretWeightsGraph('expt5/testRegretDMED01.txt','expt5/testRegret02.txt','expt5/testRegretMOSS01.txt','expt5/testRegretUCB01.txt','expt5/testRegretUCBV01.txt','expt5/testRegretUCBV01.txt')
    #print obj.a[0.0 for i in range(timestep)]ctionRegret

    #obj.regretWeightsGraph('expt6/testRegret01.txt','expt6/testRegret02.txt','expt6/testRegretMOSS01.txt','expt6/testRegretUCB01.txt','expt6/testRegretUCBR.txt')
    #obj.regretWeightsGraph('expt3/testRegretclUCB01_1.txt','expt3/testRegretclUCB01_3.txt','expt3/testRegretclUCB01_5.txt','expt3/testRegretclUCB01_10.txt','expt3/testRegretclUCB01_15.txt','expt3/testRegretclUCB01_25.txt')
    obj.regretWeightsGraph('NewExpt/expt5/testRegretGLBUCB0RR1.txt')


    #regretWeightsGraph('testFinal2/testRegret06.txt','testFinal2/testRegret07.txt','testFinal2/testRegret08.txt','testFinal2/testRegret09.txt','testFinal2/testRegret010.txt','testFinal2/testRegret011.txt','testFinal2/testRegretMOSS020.txt')
    #regretWeightsGraph('testFinal3/testRegret01.txt','testFinal3/testRegret02.txt','testFinal3/testRegret03.txt','testFinal3/testRegret04.txt','testFinal3/testRegret05.txt','testFinal3/testRegret06.txt','testFinal3/testRegretMOSS01.txt')
    #regretWeightsGraph('testFinal3/testRegret01.txt','testFinal3/testRegret02.txt','testFinal3/testRegret03.txt','testFinal3/testRegretMOSS02.txt','testFinal3/testRegret04.txt','testFinal3/testRegret05.txt')
    #regretWeightsGraph('testFinal3/testRegret01.txt','testFinal3/testRegret02.txt','testFinal3/testRegret03.txt','testFinal3/testRegretMOSS02.txt','testFinal3/testRegret04.txt','testFinal3/testRegretUCB01.txt')


    #regretWeightsGraph('testExp/clusUCB2_4.txt','testExp/testMOSS1.txt','testExp/testUCB_11_15_1.txt','testExp/testEps_11_15.txt','testExp/testEpsn_11_15.txt','testExp/testUCBD_11_15.txt', "Regret of UCB\n10 actions, 1 million rounds")

    #regretWeightsGraph('test1/testCLUCB2_final_10_1.txt','test1/testEXP_10_1.txt','test1/testUCB_10_14_1.txt','test1/testEps_1.txt', "Regret of UCB\n10 actions, 1 million rounds")
