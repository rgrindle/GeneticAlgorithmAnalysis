# GeneticAlgorithmVisualizations.py - This script contains helpful functions be visualizing the results of genetic algorithnms generated with C++
# This functions require matplotlib, numpy, and pandas.

# Author: R Grindle
# Date: Feb 18, 2016
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os.path as path


# check for "interesting" histogram data
def checkForInterestingData(count):
    for c in count:
        if(c > 15 and c < 85):
            print("True")
            return True
    return False

# save a histogram of commands in specific situations
# only saves the "interesting" histograms
def saveAlgorithmHistograms(gen,filename):
    #filename = "C:/Users/ryang/Documents/Visual Studio 2015/Projects/KKKORG/RobbyTheRobot/data/algorithm/Robby/"
    df = pd.read_csv(filename+"generation"+str(gen)+".csv", header=None)
    sum = 0    # let's count the number of interesting hists

    for col in range(512):
        data = df.iloc[0:,col].values
        #count = data[np.where(data==3)].size    # there must be a way to measure the size of what where returns
        #print(len(np.where(data==4)))
        (count, bins, patches) = plt.hist(data,bins=[-0.5,0.5,1.5,2.5,3.5,4.5,5.5], rwidth=.9)
        #print(count)

        if(checkForInterestingData(count)):
        #if(count > 15 and count < 85):
            sum = sum + 1
            plt.title("Histogram of Responses to Situation "+str(col))
            plt.xlabel("Response")
            plt.ylabel("Frequency")
            plt.savefig(filename+"../../visual/1/histogram/generation"+str(gen)+"_situtation"+str(col)+".png")
        plt.clf()    # clear figure

    print(sum)

# Save the progression from randomly generated commands to a correct result(s).
def saveSituationalCommandHistory(situation,filelocation):

    for gen in range(1,10000):
        filename = filelocation+"/generation"+str(gen)+".csv"

        if not path.isfile(filename):
            yLabels = ["Move Forward", "Move Backward", "Move Left", "Move Right", "Move Random", "Pick Up Can"]
            plt.yticks(range(6), yLabels)
            plt.subplots_adjust(left=0.2)
            plt.ylim([-0.5,5.5])
            plt.grid()
            plt.title("History of Commands for Situation "+str(situation))
            plt.xlabel("Generation")
            plt.savefig(filelocation+"history/situation"+str(situation)+".png")
            plt.clf()
            return

        df = pd.read_csv(filename, header=None)
        data = list(df.iloc[0:,situation].values)
        #(count, bins, patches) = plt.hist(data,bins=[-0.5,0.5,1.5,2.5,3.5,4.5,5.5], rwidth=.9)

        # for command in range(6):
        #     count = data.count(command)
        #     plt.plot(gen, command, 'or', markeredgecolor='r', alpha=count/100.0)

        for command in range(6):
            if data.count(command) > 10:
                plt.plot(gen, command, 'or', markeredgecolor='r', markersize=.1)

        # activeCommands = []
        #     for command in range(6):
        #         if data.count(command) > 10:
        #             activeCommands.append(command)
        #             plt.plot([gen]*len(activeCommands), activeCommands, 'or', markeredgecolor='r')


    yLabels = ["Move Forward", "Move Backward", "Move Left", "Move Right", "Move Random", "Pick Up Can"]
    plt.yticks(range(6), yLabels)
    plt.subplots_adjust(left=0.2)
    plt.ylim([-0.5,5.5])
    plt.grid(True)
    plt.title("History of Commands for Situation "+str(situation))
    plt.xlabel("Generation")
    plt.savefig(filelocation+"history/situation"+str(situation)+".png")
    plt.clf()    # clear figure
    #plt.show()

# Label each situation as "Happens", "Never Happens", or "Not Possible"
def labelSituations(numberOfSituation,fileout):
    data = []

    for situation in range(numberOfSituation):
        if situation & 1 and situation & 32:
            data.append('Not Possible')    # not possible
        elif situation & 2 and situation & 64:
            data.append('Not Possible')    # not possible
        elif situation & 4 and situation & 128:
            data.append('Not Possible')    # not possible
        elif situation & 8 and situation & 256:
            data.append('Not Possible')    # not possible
        elif situation & 1 and situation & 2:
            data.append('Never Happens')    # never happens for 10x10
        elif situation & 4 and situation & 8:
            data.append('Never Happens')    # never happens for 10x10
        else:
            data.append('Happens')    # happens

    #print(data)
    df = pd.DataFrame(data, columns = ["Occurrence"])
    df.index.name = "Situation"
    df.to_csv(fileout+"/situationalOccurrence.csv")

# Plot the fitness score vs generation.
def plotGenerations(filename,title):
    filedata = pd.read_csv(filename+"/score_data.csv")
    #filedata = numpy.loadtxt("C:/Users/ryang/Documents/Visual Studio 2015/Projects/KKKORG/RobbyTheRobot/data/score/score_data.csv", delimiter=",")

    generation = filedata.iloc[0:,0].values
    minimum = filedata.iloc[0:,1].values
    mean = filedata.iloc[0:,2].values
    median = filedata.iloc[0:,3].values
    maximum = filedata.iloc[0:,4].values

    plt.figure();
    ax = plt.subplot(111)
    plt.plot(generation,minimum,'+k',label="Minimum");
    #plt.hold();
    plt.plot(generation,mean,'+r',label="Mean");
    plt.plot(generation,median,'+b',label="Median");
    plt.plot(generation,maximum,'+g',label="Maximum");
    plt.ylim(-800,500)
    plt.grid();

    plt.title(title);
    plt.xlabel("Generations");
    plt.ylabel("Fitness Score");

    # Shrink current axis by 20%
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])

    #plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3, ncol=2, mode="expand", borderaxespad=0.)
    plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    #plt.legend();
    plt.show();

def compareAlgorithms(robot1, robot2, gen, filelocation):
    df = pd.read_csv(filelocation+"/generation"+str(gen)+".csv", header=None)

    alg1 = df.iloc[robot1,0:].values
    alg2 = df.iloc[robot2,0:].values

    differences = 0

    for (a,b) in zip(alg1,alg2):
        if a != b:
            differences = differences + 1

    return differences

def findAvergeDifferenceBetweenAlgorithms(initialGen, finalGen, filelocation):
    numberOfGens = finalGen-initialGen
    differenceSum = 0
    data = []

    for gen in range(initialGen,numberOfGens+initialGen):
        for robot1 in range(100):    # 1 less then make index so i+1 is in range
            for robot2 in range(robot1+1,100):
                individualDiff = compareAlgorithms(robot1, robot2, gen, filelocation)
                differenceSum = differenceSum + individualDiff
                data.append([robot1,robot2, individualDiff])

    differenceAvg = differenceSum/numberOfGens/4950    # 4950 = sum from 1 to 99 which is the number of robot pairs
    data.append(["","",differenceAvg])
    df = pd.DataFrame(data, columns = ["Robot a","Robot b","Algorithm Difference"])
    df.to_csv(filelocation+"Differences/AlgorithmDifferences"+str(initialGen)+"-"+str(initialGen+numberOfGens)+".csv")
    print(differenceSum)
    print(differenceAvg)
    return differenceAvg

#################################################################################################################################
# Visualization for Mitchell's data files
#    Code that generates this data can be found here: http://web.cecs.pdx.edu/~mm/RobbyTheRobot/
#################################################################################################################################

# Plot the fitness score vs generation.
def mitchell_plotGenerations(run_num,filename,title):
    filedata = pd.read_csv(filename+"/"+str(run_num)+".short",sep='\t')

    generation = filedata.iloc[0:,0].values
    maximum = filedata.iloc[0:,1].values

    plt.figure();
    plt.plot(generation,maximum,'+g',label="Maximum");
    plt.ylim(-800,500)
    plt.grid();

    plt.title(title);
    plt.xlabel("Generations");
    plt.ylabel("Fitness Score");

    plt.show();

# Convert Robby the Robot algorithm from Mitchell's format to Grindle's
# Commands
    # Michell uses [0, 6]
        # 0 -
        # 1 -
        # 2 -
        # 3 -
        # 4 -
        # 5 -
    # Grindle uses [0, 5]
        # 0 - North
        # 1 - South
        # 2 - East
        # 3 - West
        # 4 - Stay
        # 5 - Pick Up Can
        # 6 - Random
def mitchell2Grindle(algorithm):
    # set vars for Grindle and Mitchell commands

    # grindle
    g_north     = 0
    g_south     = 1
    g_west         = 2
    g_east         = 3
    g_random     = 4
    g_can         = 5

    # mitchell
    m_north     = 0
    m_south     = 1
    m_east         = 2
    m_west         = 3
    m_stay         = 4
    m_can         = 5
    m_random     = 6

    for a in algorithm:
        if a == m_north:
            a = g_north
        elif a == m_south:
            a = g_south
        elif a == m_west:
            a = g_west
        elif a == m_east:
            a = g_east
        elif a == m_random:
            a = g_random
        elif a == m_can:
            a = g_can
        elif a == m_stay:    # if stay is the command what should it become
            print("Warning: Replacing stay command.")
            a = g_random

    return algorithm
