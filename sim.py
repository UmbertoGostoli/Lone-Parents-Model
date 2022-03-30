
from person import Person
from person import Population
from shift import Shift
from shift import CostUnit
from shift import CareSlot
from house import House
from house import Town
from house import Map
import random
import math
import pylab
import Tkinter
import struct
import time
import sys
import pprint
import pickle
import numpy as np
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import csv
import os
import copy
from collections import OrderedDict
import operator
import itertools
from itertools import izip_longest
import networkx as nx
import pdb
# from PIL import ImageTk         
# from PIL import Image



class Sim:
    """Instantiates a single run of the simulation."""    
    def __init__ (self, scenario, params, folder):
        
        self.p = OrderedDict(params)
        
        self.dataMap = ['town_x', 'town_y', 'x', 'y', 'size', 'unmetNeed'] 
        
        self.dataPyramid = ['year', 'Class Age 0', 'Class Age 1', 'Class Age 2', 'Class Age 3', 'Class Age 4', 'Class Age 5', 'Class Age 6', 'Class Age 7',
                            'Class Age 8', 'Class Age 9', 'Class Age 10', 'Class Age 11', 'Class Age 12', 'Class Age 13', 'Class Age 14', 'Class Age 15',
                            'Class Age 16', 'Class Age 17', 'Class Age 18', 'Class Age 19', 'Class Age 20', 'Class Age 21', 'Class Age 22', 'Class Age 23', 
                            'Class Age 24']
        
        self.houseData = ['year', 'House name', 'size']
        
        self.householdData = ['ID', 'Sex', 'Age', 'Health']
        
        self.log = ['year', 'message']
        
        self.Outputs = ['year', 'month', 'period', 'currentPop', 'popFromStart', 'numHouseholds', 'averageHouseholdSize', 'marriageTally', 
                        'marriagePropNow', 'divorceTally', 'shareSingleParents', 'shareFemaleSingleParent', 
                        'taxPayers', 'taxBurden', 'familyCareRatio', 'employmentRate', 'shareWorkingHours', 
                        'publicSocialCare', 'costPublicSocialCare', 'sharePublicSocialCare', 'costTaxFreeSocialCare', 
                        'publicChildCare', 'costPublicChildCare', 'sharePublicChildCare', 'costTaxFreeChildCare', 
                        'totalTaxRevenue', 'totalPensionRevenue', 'pensionExpenditure', 'totalHospitalizationCost', 
                        'classShare_1', 'classShare_2', 'classShare_3', 'classShare_4', 'classShare_5', 'totalInformalChildCare', 
                        'formalChildCare', 'totalUnmetChildCareNeed', 'childcareIncomeShare', 'shareInformalChildCare', 'shareCareGivers', 
                        'ratioFemaleMaleCarers', 'shareMaleCarers', 'shareFemaleCarers', 'ratioWage', 'ratioIncome', 
                        'shareFamilyCarer', 'share_over20Hours_FamilyCarers', 'numSocialCarers', 'averageHoursOfCare', 'share_40to64_carers', 
                        'share_over65_carers', 'share_10PlusHours_over70', 'totalSocialCareNeed', 
                        'totalInformalSocialCare', 'totalFormalSocialCare', 'totalUnmetSocialCareNeed', 
                        'totalSocialCare', 'share_InformalSocialCare', 'share_UnmetSocialCareNeed', 'totalOWSC', 'shareOWSC', 'totalCostOWSC', 
                        'singleHousehold_UC', 'coupleHousehold_UC', 'incomePerCapita_Single', 'incomePerCapita_Couple',
                        'q1_socialCareNeed', 'q1_informalSocialCare', 'q1_formalSocialCare', 'q1_unmetSocialCareNeed', 'q1_outOfWorkSocialCare',
                        'q2_socialCareNeed', 'q2_informalSocialCare', 'q2_formalSocialCare', 'q2_unmetSocialCareNeed', 'q2_outOfWorkSocialCare',
                        'q3_socialCareNeed', 'q3_informalSocialCare', 'q3_formalSocialCare', 'q3_unmetSocialCareNeed', 'q3_outOfWorkSocialCare',
                        'q4_socialCareNeed', 'q4_informalSocialCare', 'q4_formalSocialCare', 'q4_unmetSocialCareNeed', 'q4_outOfWorkSocialCare',
                        'q5_socialCareNeed', 'q5_informalSocialCare', 'q5_formalSocialCare', 'q5_unmetSocialCareNeed', 'q5_outOfWorkSocialCare',
                        'grossDomesticProduct', 'publicCareToGDP', 'onhUnmetChildcareNeed', 'medianChildCareNeedONH',
                        'totalHoursOffWork', 'indIQ1', 'indIQ2', 'indIQ3', 'indIQ4', 'indIQ5', 'origIQ1', 'origIQ2', 'origIQ3', 'origIQ4', 'origIQ5', 
                        'dispIQ1', 'dispIQ2', 'dispIQ3', 'dispIQ4', 'dispIQ5', 'netIQ1', 'netIQ2', 'netIQ3', 'netIQ4', 'etIQ5', 'shareSES_1', 
                        'shareSES_2', 'shareSES_3', 'shareSES_4', 'shareSES_5', 'internalChildCare', 'internalSocialCare', 'externalChildCare', 
                        'externalSocialCare', 'shareInternalCare', 'aggregateChildBenefits', 'aggregateDisabledChildrenBenefits', 'aggregatePIP', 
                        'aggregateAttendanceAllowance', 'aggregateCarersAllowance', 'aggregateUC', 'aggregateHousingElement', 
                        'aggregatePensionCredit', 'totalBenefits', 'benefitsIncomeShare']
        
        self.outputData = pd.DataFrame()
        # Save initial parametrs into Scenario folder
        self.folder = folder + '/Scenario_' + str(scenario)
        if not os.path.exists(self.folder):
            os.makedirs(self.folder)
        filePath = self.folder + '/scenarioParameters.csv'
        c = params.copy()
        for key, value in c.iteritems():
            if not isinstance(value, list):
                c[key] = [value]
        with open(filePath, "wb") as f:
            csv.writer(f).writerow(c.keys())
            csv.writer(f).writerows(itertools.izip_longest(*c.values()))
        
        
        ####  SES variables   #####
        self.socialClassShares = []
        self.careNeedShares = []
        self.householdIncomes = []
        self.individualIncomes = []
        self.incomeFrequencies = []
        self.sesPops = []
        self.sesPopsShares = []
        self.hiredPeople = []
        ## Statistical tallies
        self.times = []
        self.pops = []
        self.avgHouseholdSize = []
        self.marriageTally = 0
        self.numMarriages = []
        self.divorceTally = 0
        self.numDivorces = []
        self.totalCareDemand = []
        self.totalCareSupply = []
        self.informalSocialCareSupply = 0
        self.totalHospitalizationCost = 0
        self.hospitalizationCost = []
        self.numTaxpayers = []
        self.totalUnmetNeed = []
        self.totalChildCareNeed = 0
        self.totalSocialCareNeed = 0
        self.totalUnmetCareNeed = 0
        self.totalUnmetChildCareNeed = 0
        self.totalUnmetSocialCareNeed = 0
        self.internalChildCare = 0
        self.internalSocialCare = 0
        self.externalChildCare = 0
        self.externalSocialCare = 0
        self.shareUnmetNeed = []
        self.totalFamilyCare = []
        self.inHouseInformalCare = 0
        self.totalTaxBurden = []
        self.marriageProp = []
        self.shareLoneParents = []
        self.shareFemaleLoneParents = []
        self.employmentRate = []
        self.shareWorkingHours = []
        self.publicCareProvision = []
        
        self.householdsWithFormalChildCare = []
        self.periodFormalCare = False
        self.totalFormalCare = 0
        self.previousTotalFormalCare = 0
        
        self.publicSocialCare = 0
        self.costPublicSocialCare = 0
        self.grossDomesticProduct = 0
        self.costTaxFreeSocialCare = 0
        self.costTaxFreeChildCare = 0
        self.costPublicChildCare = 0
        self.publicChildCare = 0
        self.sharePublicSocialCare = 0
        self.sharePublicChildCare = 0
        self.stateTaxRevenue = []
        self.totalTaxRevenue = 0
        self.statePensionRevenue = []
        self.totalPensionRevenue = 0
        self.statePensionExpenditure = []
        self.pensionExpenditure = 0
        self.aggregateChildBenefits = 0
        self.aggregateDisabledChildrenBenefits = 0
        self.aggregatePIP = 0
        self.aggregateAttendanceAllowance = 0
        self.aggregateCarersAllowance = 0
        self.aggregateUC = 0
        self.aggregateHousingElement = 0
        self.aggregatePensionCredit = 0
        
        self.onhUnmetChildcareNeed = 0
        self.medianChildCareNeedONH = 0
        self.totalHoursOffWork = 0
        self.allCareSlots = []
        ## Counters and storage
        self.year = self.p['startYear']
        self.pyramid = PopPyramid(self.p['num5YearAgeClasses'],
                                  self.p['numCareLevels'])
        self.textUpdateList = []
        
        self.socialCareNetwork = nx.DiGraph()

        self.aggregateSchedule = [0]*24
        # if self.p['interactiveGraphics']:
        # self.window = Tkinter.Tk()
        # self.canvas = Tkinter.Canvas(self.window,
        #                        width=self.p['screenWidth'],
        #                        height=self.p['screenHeight'],
        #                        background=self.p['bgColour'])


    def run(self, policy, policyParams, seed):
        """Run the simulation from year start to year end."""

        #pprint.pprint(self.p)
        #raw_input("Happy with these parameters?  Press enter to run.")
        self.randSeed = seed
        random.seed(self.randSeed)
        np.random.seed(self.randSeed)

        self.initializePop()
        
        if self.p['interactiveGraphics']:
            self.initializeCanvas()     
            
        # Save policy parameters in Policy folder
        policyFolder = self.folder + '/Policy_' + str(policy)
        if not os.path.exists(policyFolder):
            os.makedirs(policyFolder)
        filePath = policyFolder + '/policyParameters.csv'
        c = policyParams.copy()
        for key, value in c.iteritems():
            if not isinstance(value, list):
                c[key] = [value]
        with open(filePath, "wb") as f:
            csv.writer(f).writerow(c.keys())
            csv.writer(f).writerows(itertools.izip_longest(*c.values()))
        
        if policy == 0:
            startYear = int(self.p['startYear'])
        else:
            startYear = int(self.p['policyStartYear'])
        
        
        startSim = time.time()
        
        dataHouseholdFolder = os.path.join(policyFolder, 'DataHousehold')
        if not os.path.exists(dataHouseholdFolder):
            os.makedirs(dataHouseholdFolder)
        
        dataMapFolder = os.path.join(policyFolder, 'DataMap')
        if not os.path.exists(dataMapFolder):
            os.makedirs(dataMapFolder)
        
        if not os.path.exists(policyFolder):
            os.makedirs(policyFolder)
        with open(os.path.join(policyFolder, "Log.csv"), "w") as file:
            writer = csv.writer(file, delimiter = ",", lineterminator='\r')
            writer.writerow((self.log))
            
        if not os.path.exists(policyFolder):
            os.makedirs(policyFolder)
        with open(os.path.join(policyFolder, "HouseData.csv"), "w") as file:
            writer = csv.writer(file, delimiter = ",", lineterminator='\r')
            writer.writerow((self.houseData))
        
        if not os.path.exists(policyFolder):
            os.makedirs(policyFolder)
        with open(os.path.join(policyFolder, "Pyramid_Male_0.csv"), "w") as file:
            writer = csv.writer(file, delimiter = ",", lineterminator='\r')
            writer.writerow((self.dataPyramid))
            
        if not os.path.exists(policyFolder):
            os.makedirs(policyFolder)
        with open(os.path.join(policyFolder, "Pyramid_Male_1.csv"), "w") as file:
            writer = csv.writer(file, delimiter = ",", lineterminator='\r')
            writer.writerow((self.dataPyramid))
            
        if not os.path.exists(policyFolder):
            os.makedirs(policyFolder)
        with open(os.path.join(policyFolder, "Pyramid_Male_2.csv"), "w") as file:
            writer = csv.writer(file, delimiter = ",", lineterminator='\r')
            writer.writerow((self.dataPyramid))
            
        if not os.path.exists(policyFolder):
            os.makedirs(policyFolder)
        with open(os.path.join(policyFolder, "Pyramid_Male_3.csv"), "w") as file:
            writer = csv.writer(file, delimiter = ",", lineterminator='\r')
            writer.writerow((self.dataPyramid))
            
        if not os.path.exists(policyFolder):
            os.makedirs(policyFolder)
        with open(os.path.join(policyFolder, "Pyramid_Male_4.csv"), "w") as file:
            writer = csv.writer(file, delimiter = ",", lineterminator='\r')
            writer.writerow((self.dataPyramid))
            
        if not os.path.exists(policyFolder):
            os.makedirs(policyFolder)
        with open(os.path.join(policyFolder, "Pyramid_Female_0.csv"), "w") as file:
            writer = csv.writer(file, delimiter = ",", lineterminator='\r')
            writer.writerow((self.dataPyramid))
            
        if not os.path.exists(policyFolder):
            os.makedirs(policyFolder)
        with open(os.path.join(policyFolder, "Pyramid_Female_1.csv"), "w") as file:
            writer = csv.writer(file, delimiter = ",", lineterminator='\r')
            writer.writerow((self.dataPyramid))
            
        if not os.path.exists(policyFolder):
            os.makedirs(policyFolder)
        with open(os.path.join(policyFolder, "Pyramid_Female_2.csv"), "w") as file:
            writer = csv.writer(file, delimiter = ",", lineterminator='\r')
            writer.writerow((self.dataPyramid))
            
        if not os.path.exists(policyFolder):
            os.makedirs(policyFolder)
        with open(os.path.join(policyFolder, "Pyramid_Female_3.csv"), "w") as file:
            writer = csv.writer(file, delimiter = ",", lineterminator='\r')
            writer.writerow((self.dataPyramid))
            
        if not os.path.exists(policyFolder):
            os.makedirs(policyFolder)
        with open(os.path.join(policyFolder, "Pyramid_Female_4.csv"), "w") as file:
            writer = csv.writer(file, delimiter = ",", lineterminator='\r')
            writer.writerow((self.dataPyramid))
             
        self.month = 0
        self.period = 0
        for self.year in range(startYear, int(self.p['endYear']+1)):
            
            print 'Policy: ' + str(policy)
            
            for month in range(1, 13):
                self.month = month
                self.period += 1
                if policyParams and self.year == self.p['policyStartYear'] and month == 1:
                    keys = policyParams.keys()
                    for k in keys[1:]:
                        self.p[k] = policyParams[k]
                    
                    # From list of agents to list of indexes
                    if policy == 0:
                        
                        print 'Saving the simulation....'
                        
                        self.from_Agents_to_IDs()
                        
                        # Save outputs
                        self.outputData = pd.read_csv(policyFolder + '/Outputs.csv')
                        self.outputData.to_csv(policyFolder + '/tempOutputs.csv', index=False)
                        # Save simulation
                        pickle.dump(self.pop, open(policyFolder + '/save.p', 'wb'))
                        pickle.dump(self.map, open(policyFolder + '/save.m', 'wb'))
                    
                    # Upload simulation
                    print 'Uploading the simulation....'
                    
                    self.pop = pickle.load(open(self.folder + '/Policy_0/save.p', 'rb'))
                    self.map = pickle.load(open(self.folder + '/Policy_0/save.m', 'rb'))
                    
                    self.from_IDs_to_Agents()
                    
                    # Upload outputs
                    if policy != 0:
                        self.outputData = pd.read_csv(self.folder + '/Policy_0/tempOutputs.csv')
                        self.outputData.to_csv(policyFolder + '/Outputs.csv', index=False)
          
                self.doOneMonth(policyFolder, dataMapFolder, dataHouseholdFolder, self.year, month, self.period)
                
    #            self.from_Agents_to_IDs()
    #            pickle.dump(self.pop, open('Canvas_Pop/save.p_'+str(self.year), 'wb'))
    #            pickle.dump(self.map, open('Canvas_Map/save.m_'+str(self.year), 'wb'))
    #            self.from_IDs_to_Agents()
              
                print ''
            
        endSim = time.time()
        
        simulationTime = endSim - startSim
        
        print 'Simulation time: ' + str(simulationTime)
        
        if self.p['singleRunGraphs']:
            self.doGraphs()
    
        if self.p['interactiveGraphics']:
            print "Entering main loop to hold graphics up there."
            self.window.mainloop()

        return self.totalTaxBurden[-1]


    def initializePop(self):
        """
        Set up the initial population and the map.
        We may want to do this from scratch, and we may want to do it
        by loading things from a pre-generated file.
        """
        #reading JH's fertility projections from a CSV into a numpy array
        self.fert_data = np.genfromtxt('babyrate.txt.csv', skip_header=0, delimiter=',')

        #reading JH's fertility projections from two CSVs into two numpy arrays
        self.death_female = np.genfromtxt('deathrate.fem.csv', skip_header=0, delimiter=',')
        
        self.death_male = np.genfromtxt('deathrate.male.csv', skip_header=0, delimiter=',')
        
        self.unemployment_series = np.genfromtxt('unemploymentrate.csv', skip_header=0, delimiter=',')
        
        self.incomeDistribution = np.genfromtxt('incomeDistribution.csv', skip_header=0, delimiter=',')
        
        self.incomesPercentiles = np.genfromtxt('incomesPercentiles.csv', skip_header=0, delimiter=',')
        
        self.wealthPercentiles = np.genfromtxt('wealthDistribution.csv', skip_header=0, delimiter=',')
        
        ## First the map, towns, and houses
        self.shiftsPool = self.createShifts()
        
        if self.p['loadFromFile'] == False:
            self.map = Map(self.p['mapGridXDimension'],
                           self.p['mapGridYDimension'],
                           self.p['townGridDimension'],
                           self.p['cdfHouseClasses'],
                           self.p['ukMap'],
                           self.p['ukClassBias'],
                           self.p['mapDensityModifier'],
                           self.p['lha_1'], self.p['lha_2'], self.p['lha_3'], self.p['lha_4'])
        else:
            self.map = pickle.load(open("initMap.txt","rb"))


        ## Now the people who will live on it

        if self.p['loadFromFile'] == False:
            self.pop = Population(self.p['initialPop'],
                                  self.p['startYear'],
                                  self.p['minStartAge'],
                                  self.p['maxStartAge'],
                                  self.p['workingAge'],
                                  self.p['incomeInitialLevels'],
                                  self.p['incomeFinalLevels'],
                                  self.p['incomeGrowthRate'],
                                  self.p['workDiscountingTime'],
                                  self.p['wageVar'],
                                  self.p['weeklyHours'][0])
            ## Now put the people into some houses
            ## They've already been partnered up so put the men in first, then women to follow
            men = [x for x in self.pop.allPeople if x.sex == 'male']

            remainingHouses = []
            remainingHouses.extend(self.map.allHouses)
        
            for man in men:
                man.house = random.choice(remainingHouses)
                man.sec = man.house.size  ## This may not always work, assumes house classes = SEC classes!
                self.map.occupiedHouses.append(man.house)            
                remainingHouses.remove(man.house)
                woman = man.partner
                woman.house = man.house
                woman.sec = man.sec
                man.yearMarried.append(int(self.p['startYear']))
                woman.yearMarried.append(int(self.p['startYear']))
                man.house.occupants.append(man)
                man.house.occupants.append(woman)
                self.hiredPeople.extend([man, woman])
                
            # Compute class and age shares
            classShares = []
            for c in range(int(self.p['numberClasses'])):
                classPop = [x for x in self.pop.allPeople if x.classRank == c]
                classShares.append(float(len(classPop))/float(len(self.pop.allPeople)))
            ageBandShares = []
            for c in range(int(self.p['numberClasses'])):
                classPop = [x for x in self.pop.allPeople if x.classRank == c]
                ageBandSharesByClass = []
                for b in range(int(self.p['numberAgeBands'])):
                    agePop = [x for x in classPop if self.ageBand(x.age) == b]
                    if len(classPop) > 0:
                        ageBandSharesByClass.append(float(len(agePop))/float(len(classPop)))
                    else:
                        ageBandSharesByClass.append(0)
                ageBandShares.append(ageBandSharesByClass)
            unemploymentRate = self.unemployment_series[0]
            for person in self.hiredPeople:
                person.unemploymentIndex = self.computeUR(unemploymentRate, classShares, ageBandShares[person.classRank], 
                                                          self.p['unemploymentClassBias'], self.p['unemploymentAgeBias'], 
                                                          person.classRank, self.ageBand(person.age))
                
            self.assignJobs(self.hiredPeople, -1)
            
        else:
            self.pop = pickle.load(open("initPop.txt","rb"))

        ## Choose one house to be the display house
        self.displayHouse = self.pop.allPeople[0].house
        self.displayHouse.display = True
        self.nextDisplayHouse = None
        
        # Assign wealth
        self.updateWealth()
    
    def createShifts(self):
        allShifts = []
        numShifts = [int(round(x)) for x in self.p['shiftsWeights']]
        hours = []
        for hourIndex in range(len(numShifts)):
            hours.extend([hourIndex]*numShifts[hourIndex])
        allHours = list(np.random.choice(hours, 9000))
        shifts = []
        for i in range(1000):
            shift = []
            hour = np.random.choice(allHours)
            shift.append(hour)
            allHours.remove(hour)
            if hour == 0:
                nextHours = [23, 1]
            elif hour == 23:
                nextHours = [22, 0]
            else:
                nextHours = [hour-1, hour+1]
            weights = []
            for nextHour in nextHours:
                weights.append(float(len([x for x in allHours if x == nextHour])))
            if sum(weights) == 0:
                break
            probs = [x/sum(weights) for x in weights]
            nextHour = np.random.choice(nextHours, p = probs)
            if nextHours.index(nextHour) == 0:
                shift = [nextHour]+shift
            else:
                shift.append(nextHour)
            allHours.remove(nextHour)
            while len(shift) < 8:
                a = -1
                b = -1
                if shift[0] == 0:
                    a = 23
                else:
                    a = shift[0]-1
                if shift[-1] == 23:
                    b = 0
                else:
                    b = shift[-1]+1
                nextHours = [a,b]
                weights = [float(len([x for x in allHours if x == a])), float(len([x for x in allHours if x == b]))]
                if sum(weights) == 0:
                    break
                probs = [x/sum(weights) for x in weights]
                nextHour = np.random.choice(nextHours, p = probs)
                if nextHours.index(nextHour) == 0:
                    shift = [nextHour]+shift
                else:
                    shift.append(nextHour)
                allHours.remove(nextHour)
            shifts.append(shift)
            # pdb.set_trace()
    
        for shift in shifts:
            days = []
            weSocIndex = 0
            if np.random.random() < self.p['probSaturdayShift']:
                days.append(6)
                weSocIndex -= 1
            if np.random.random() < self.p['probSundayShift']:
                days.append(7)
                weSocIndex -= (1 + self.p['sundaySocialIndex'])
            if len(days) == 0:
                days = range(1, 6)
            elif len(days) == 1:
                days.extend(np.random.choice(range(1, 6), 4, replace=False))
            else:
                days.extend(np.random.choice(range(1, 6), 3, replace=False))
                
            startHour = (shift[0]+7)%24+1
            socIndex = np.exp(self.p['shiftBeta']*self.p['shiftsWeights'][shift[0]]+self.p['dayBeta']*weSocIndex)
            
            newShift = Shift(days, startHour, shift[0], shift, socIndex)
            allShifts.append(newShift)
        
        return allShifts
        
    def from_Agents_to_IDs(self):
        for person in self.pop.allPeople:
            if person.mother != None:
                person.motherID = person.mother.id
            else:
                person.motherID = -1
            if person.father != None:
                person.fatherID = person.father.id
            else:
                person.fatherID = -1
            person.childrenID = [x.id for x in person.children]
            person.houseID = person.house.id
            person.mother = None
            person.father = None
            person.children = []
            person.house = None
        
        for house in self.map.allHouses:
            house.occupantsID = [x.id for x in house.occupants]
            house.occupants = []
        
    def from_IDs_to_Agents(self):
        for person in self.pop.allPeople:
            if person.motherID != -1:
                person.mother = [x for x in self.pop.allPeople if x.id == person.motherID][0]
            else:
                person.mother = None
            if person.fatherID != -1:
                person.father = [x for x in self.pop.allPeople if x.id == person.fatherID][0]
            else:
                person.father = None
                
            person.children = [x for x in self.pop.allPeople if x.id in person.childrenID]
            
        for person in self.pop.allPeople:
            person.house = [x for x in self.map.allHouses if x.id == person.houseID][0]
            if person in self.pop.livingPeople:
                person.house.occupants.append(person)
    

    def doOneMonth(self, policyFolder, dataMapFolder, dataHouseholdFolder, year, month, period):
        """Run one year of simulated time."""

        ##print "Sim Year: ", self.year, "OH count:", len(self.map.occupiedHouses), "H count:", len(self.map.allHouses)
        print 'Year: ' + str(year) + ' - Month: ' + str(month)
        # self.checkHouseholds(0)
        
        startYear = time.time()
        
        print 'Tot population: ' + str(len(self.pop.livingPeople))
        # print 'Doing fucntion 1...'
        
        self.computeClassShares()
        
        # print 'Doing doDeaths...'
      
        ###################   Do Deaths   #############################
        
        # self.checkIndependentAgents(0)
      
        self.doDeaths(policyFolder, month)
        
        # self.checkIndependentAgents(1)
        
        self.doAdoptions(policyFolder)
        
        # self.checkIndependentAgents(1)
        
        
        ###################   Do Care Transitions   ##########################
        
        # self.doCareTransitions()
        
        # print 'Doing fucntion 4...'
        
        
        self.doCareTransitions_UCN(policyFolder, month)
        
        # self.checkIndependentAgents(1.1)
        

        self.computeIncome(month)
        
        if month == 12:
            self.computeIncomeQuintileShares()
        
        self.updateWealth_Ind()
        
        
        # self.checkIncome(2)
        
        print 'Doing jobMarket...'
        
        self.jobMarket(year, month)
        # Here, people change job, find a job if unemployed and lose a job if employed.
        # The historical UK unemployment rate is the input.
        # Unmeployement rates are adjusted for age and SES.
        # Upon losing the job, a new unemplyed agent is assigned an 'unemployment duration' draw from the empirical distribution.
        # Unemployment duration is also age and SES specific.
        
        self.computeAggregateSchedule()
        
        # print 'Doing fucntion 9...'
        # self.checkIncome(3)
        
        
        # self.computeTax()
        

        # print 'Doing startCareAllocation...'
 
        self.startCareAllocation()
        
        if year >= self.p['careAllocationFromYear']:
            
            self.allocateWeeklyCare()
            
            # self.checkHouseholdsProvidingFormalCare()
        
        # print 'Doing fucntion 7...'
        # self.checkIncome(5)
        
        
        ##### Temporarily bypassing social care alloction
        
        ## self.allocateSocialCare_Ind()
    
        # print 'Doing fucntion 8...'
    
        self.updateUnmetCareNeed()
        
        self.doAgeTransitions(policyFolder, month)
        
        # self.checkIndependentAgents(1.2)
        
        
        self.doSocialTransition(policyFolder, month)
        
        
        # self.checkIndependentAgents(1.3)
        
        
        # Each year
        self.houseOwnership(year)
        
        
        # Compute benefits.
        # They increase the household income in the following period.
        if self.p['withBenefits'] == True:
            self.computeBenefits()
        
        # self.publicCareEntitlements()
        
        # print 'Doing fucntion 10...'
        
        # self.checkHouseholds(0)
        
        self.doBirths(policyFolder, month)
        
        # self.checkIndependentAgents(1.3)
        # print 'Doing fucntion 11...'
  
        
        
        
        
        # print 'Doing fucntion 12...'
        
        # self.updateWealth()
        
        
      
        # print 'Doing fucntion 13...'
        
        # self.doSocialTransition_TD()
        
        # self.checkIndependentAgents(2)
        
        # print 'Doing fucntion 14...'
        
        self.doDivorces(policyFolder, month)
        
        # self.checkIndependentAgents(3)
        
        self.doMarriages(policyFolder, month)
        
        
        # self.checkIndependentAgents(4)
        
        # print 'Doing fucntion 16...'
        print 'Doing doMovingAround...'
        
        self.doMovingAround(policyFolder)
        
        
        # self.checkIndependentAgents(5)
        
        # print 'Doing householdRelocation...'
        
        # self.householdRelocation(policyFolder)
        
        
        # print 'Doing fucntion 17...'
        
        self.pyramid.update(self.year, self.p['num5YearAgeClasses'], self.p['numCareLevels'],
                            self.p['pixelsInPopPyramid'], self.pop.livingPeople)
        
        
        # print 'Doing fucntion 18...'
        
        self.healthCareCost()
        
        self.doStats(policyFolder, dataMapFolder, dataHouseholdFolder, period)
        
        if (self.p['interactiveGraphics']):
            self.updateCanvas()
            
        endYear = time.time()
        
        print 'Year execution time: ' + str(endYear - startYear)

            
        # print 'Did doStats'
        
    def checkIndependentAgents(self, n):
        for house in self.map.occupiedHouses:
            
            independentHousehold = [x for x in house.occupants if x.independentStatus == True]
            
            if len(independentHousehold) < 1 or len(independentHousehold) > 2:
                print 'Error: wrong number of independet agents!'
                print 'Step: ' + str(n)
                print 'There are ' + str(len(independentHousehold)) + ' independent agents.'
                print 'Independent agents: ' + str(independentHousehold)
                print 'All members: ' + str(len(house.occupants))
                print 'Status: ' + str([x.status for x in house.occupants])
                print 'Member ages: ' + str([x.age for x in house.occupants])
                sys.exit()
            if len(independentHousehold) == 2:
                partners = [x for x in house.occupants if x.partner != None]
                if len(partners) > 2:
                    print 'Error: there is more than one couple!'
                    print 'Step: ' + str(n)
                    print 'Independent agents: ' + str(independentHousehold)
                    print 'Partners: ' + str(partners)
                    print 'All members: ' + str(len(house.occupants))
                    print 'Status: ' + str([x.status for x in house.occupants])
                    print 'Member ages: ' + str([x.age for x in house.occupants])
                    sys.exit()

    def checkHouseholds(self, n):
        
#        for member in self.pop.livingPeople:
#            if member.partner != None and member.house != member.partner.house:
#                print 'Step: ' + str(n)
#                print 'Couple not living together'
#                print member.id
#                print member.dead
#                print member.independentStatus
#                print member.yearMarried
#                print member.partner.id
#                print member.partner.partner.id
#                print member.partner.dead
#                print member.partner.independentStatus
#                print member.partner.yearMarried
#                sys.exit()
    
        for house in self.map.occupiedHouses:
            
            household = house.occupants
            
#            if len(household) != len(set(household)):
#                print 'Step: ' + str(n)
#                print 'Error: person counted twice'
#                sys.exit()
                
#            if len(household) == 0:
#                print 'Step: ' + str(n)
#                print 'Error: occupied house is empty!'
#                sys.exit()
                
            married = [x for x in household if x.partner != None]
            
#            if len(married) > 2:
#                print 'Step: ' + str(n)
#                print 'Error: more than a couple in a house'
#                for member in married:
#                    print member.id
#                    print member.age
#                    print member.status
#                    print member.independentStatus
#                    print member.classRank
#                    print member.sex
#                    print member.income
#                    print member.careNeedLevel
#                    print 'Person partner id: ' + str(member.partner.id)
#                sys.exit()
                
#            if len(married) == 1:
#                print 'Step: ' + str(n)
#                print 'Error: married person not living with partner'
#                sys.exit()
           
            independentPeople = [x for x in household if x.independentStatus == True]
            
#            if len(independentPeople) == 0:
#                print 'Error: no independent people in the house'
#                print 'Step: ' + str(n)
#                for member in household:
#                    print member.id
#                    print member.age
#                    print member.status
#                    print member.classRank
#                    print member.sex
#                    print member.income
#                    print member.careNeedLevel
#                    print 'Father: ' + str(member.father.id)
#                    print member.father.dead
#                    print member.father.deadYear
#                    print member.father.yearMarried
#                    print member.father.yearDivorced
#                    print 'Mother: ' + str(member.mother.id)
#                    print member.mother.dead
#                    print member.mother.deadYear
#                    print member.mother.yearMarried
#                    print member.mother.yearDivorced
#                    
#                    if member.partner != None:
#                        print 'Person partner id: ' + str(member.partner.id)
#                    if member.mother.partner != None:
#                        print 'Person mother partner id: ' + str(member.mother.partner.id)
#                        print 'Person mother partner children: ' + str([x.id for x in member.mother.partner.children])
#                        if member.mother.partner.partner != None:
#                            print 'Person father partner id: ' + str(member.mother.partner.partner.id)
#                    if member.father.partner != None:
#                        print 'Person father partner id: ' + str(member.father.partner.id)
#                        print 'Person father partner children: ' + str([x.id for x in member.father.partner.children])
#                        if member.father.partner.partner != None:
#                            print 'Person father partner partner id: ' + str(member.father.partner.partner.id)
#                sys.exit()
                
            
####################   doDeath - SES version    ################################################
    def computeClassShares(self):
        
        self.socialClassShares[:] = []
        self.careNeedShares[:] = []
        peopleWithRank = [x for x in self.pop.livingPeople if x.classRank != -1]
        numPop = float(len(peopleWithRank))
        for c in range(int(self.p['numberClasses'])):
            classPop = [x for x in peopleWithRank if x.classRank == c]
            numclassPop = float(len(classPop))
            self.socialClassShares.append(numclassPop/numPop)
            
            needShares = []
            for b in range(int(self.p['numCareLevels'])):
                needPop = [x for x in classPop if x.careNeedLevel == b]
                numNeedPop = float(len(needPop))
                if numclassPop > 0:
                    needShares.append(numNeedPop/numclassPop)
                else:
                    needShares.append(0.0)
            self.careNeedShares.append(needShares)    
            
        print self.socialClassShares
    
    def deathProb(self, baseRate, person):  ##, shareUnmetNeed, classPop):
        
        classRank = person.classRank
        if person.status == 'child' or person.status == 'student':
            classRank = person.parentsClassRank
        
        if person.sex == 'male':
            mortalityBias = self.p['maleMortalityBias']
        else:
            mortalityBias = self.p['femaleMortalityBias']
        
        deathProb = baseRate
        
        a = 0
        for i in range(int(self.p['numberClasses'])):
            a += self.socialClassShares[i]*math.pow(mortalityBias, i)
            
        if a > 0:
            
            lowClassRate = baseRate/a
            
            classRate = lowClassRate*math.pow(mortalityBias, classRank)
            
            deathProb = classRate
           
            b = 0
            for i in range(int(self.p['numCareLevels'])):
                b += self.careNeedShares[classRank][i]*math.pow(self.p['careNeedBias'], (self.p['numCareLevels']-1) - i)
                
            if b > 0:
                
                higherNeedRate = classRate/b
               
                deathProb = higherNeedRate*math.pow(self.p['careNeedBias'], (self.p['numCareLevels']-1) - person.careNeedLevel) # deathProb
      
        # Add the effect of unmet care need on mortality rate for each care need level
        
        ##### Temporarily by-passing the effect of Unmet Care Need   #############
        
#        a = 0
#        for x in classPop:
#            a += math.pow(self.p['unmetCareNeedBias'], 1-x.averageShareUnmetNeed)
#        higherUnmetNeed = (classRate*len(classPop))/a
#        deathProb = higherUnmetNeed*math.pow(self.p['unmetCareNeedBias'], 1-shareUnmetNeed)
        
        return deathProb
    
    def deathProb_UCN(self, baseRate, sex, classRank, needLevel, shareUnmetNeed, classPop):
        
        if sex == 'male':
            mortalityBias = self.p['maleMortalityBias']
        else:
            mortalityBias = self.p['femaleMortalityBias']
        
        a = 0
        for i in range(self.p['numberClasses']):
            a += self.socialClassShares[i]*math.pow( mortalityBias, i)
        lowClassRate = baseRate/a
        
        classRate = lowClassRate*math.pow(mortalityBias, classRank)
       
        a = 0
        for i in range(self.p['numCareLevels']):
            a += self.careNeedShares[classRank][i]*math.pow(self.p['careNeedBias'], (self.p['numCareLevels']-1) - i)
        higherNeedRate = classRate/a
       
        classRate = higherNeedRate*math.pow(self.p['careNeedBias'], (self.p['numCareLevels']-1) - needLevel) # deathProb
      
        # Add the effect of unmet care need on mortality rate for each care need level
        
        ##### Temporarily by-passing the effect of Unmet Care Need   #############
        
        a = 0
        for x in classPop:
            a += math.pow(self.p['unmetCareNeedBias'], 1-x.averageShareUnmetNeed)
        higherUnmetNeed = (classRate*len(classPop))/a
        deathProb = higherUnmetNeed*math.pow(self.p['unmetCareNeedBias'], 1-shareUnmetNeed)
        
        return deathProb
    
    def doDeaths(self, policyFolder, month):
        
        preDeath = len(self.pop.livingPeople)
        
        deaths = [0, 0, 0, 0, 0]
        """Consider the possibility of death for each person in the sim."""
        for person in self.pop.livingPeople:
            age = person.age
            
            ####     Death process with histroical data  after 1950   ##################
            if self.year >= 1950:
                if age > 109:
                    age = 109
                if person.sex == 'male':
                    rawRate = self.death_male[age, self.year-1950]
                if person.sex == 'female':
                    rawRate = self.death_female[age, self.year-1950]
                    
                classPop = [x for x in self.pop.livingPeople if x.careNeedLevel == person.careNeedLevel]
                
                dieProb = self.deathProb(rawRate, person)
                
                person.lifeExpectancy = max(90-person.age, 3)
                # dieProb = self.deathProb_UCN(rawRate, person, person.averageShareUnmetNeed, classPop)

            #############################################################################
            
                if np.random.random() < dieProb and np.random.choice([x+1 for x in range(12)]) == month:
                    person.dead = True
                    person.deadYear = self.year
                    person.house.occupants.remove(person)
                    if len(person.house.occupants) == 0:
                        self.map.occupiedHouses.remove(person.house)
                        if (self.p['interactiveGraphics']):
                            self.canvas.itemconfig(person.house.icon, state='hidden')
                    if person.partner != None:
                        person.partner.partner = None
                    if person.house == self.displayHouse:
                        messageString = str(self.year) + ": #" + str(person.id) + " died aged " + str(age) + "." 
                        self.textUpdateList.append(messageString)
                        
                        with open(os.path.join(policyFolder, "Log.csv"), "a") as file:
                            writer = csv.writer(file, delimiter = ",", lineterminator='\r')
                            writer.writerow([self.year, messageString])
                
            else: 
                #######   Death process with made-up rates  ######################
                babyDieProb = 0.0
                if age < 1:
                    babyDieProb = self.p['babyDieProb']
                if person.sex == 'male':
                    ageDieProb = (math.exp(age/self.p['maleAgeScaling']))*self.p['maleAgeDieProb'] 
                else:
                    ageDieProb = (math.exp(age/self.p['femaleAgeScaling']))* self.p['femaleAgeDieProb']
                rawRate = self.p['baseDieProb'] + babyDieProb + ageDieProb
                
                classPop = [x for x in self.pop.livingPeople if x.careNeedLevel == person.careNeedLevel]
                
                dieProb = self.deathProb(rawRate, person)
                
                person.lifeExpectancy = max(90-person.age, 5)
                #### Temporarily by-passing the effect of unmet care need   ######
                # dieProb = self.deathProb_UCN(rawRate, person.parentsClassRank, person.careNeedLevel, person.averageShareUnmetNeed, classPop)
                
                if np.random.random() < dieProb and np.random.choice([x+1 for x in range(12)]) == month:
                    person.dead = True
                    person.deadYear = self.year
                    deaths[person.classRank] += 1
                    person.house.occupants.remove(person)
                    if len(person.house.occupants) == 0:
                        self.map.occupiedHouses.remove(person.house)
                        if (self.p['interactiveGraphics']):
                            self.canvas.itemconfig(person.house.icon, state='hidden')
                    if person.partner != None:
                        person.partner.partner = None
                    if person.house == self.displayHouse:
                        messageString = str(self.year) + ": #" + str(person.id) + " died aged " + str(age) + "." 
                        self.textUpdateList.append(messageString)
                        
                        with open(os.path.join(policyFolder, "Log.csv"), "a") as file:
                            writer = csv.writer(file, delimiter = ",", lineterminator='\r')
                            writer.writerow([self.year, messageString])
                        
                  
        self.pop.livingPeople[:] = [x for x in self.pop.livingPeople if x.dead == False]
        
        postDeath = len(self.pop.livingPeople)
        
        print('the number of deaths is: ' + str(preDeath - postDeath))      
        
    def doAdoptions(self, policyFolder):
        for person in self.pop.livingPeople:
            # Chneg status of workers living with parents (who died)
            if (person.status == 'worker' or person.status == 'unemployed') and len([x for x in person.house.occupants if x.independentStatus == True]) == 0:
                person.independentStatus = True
                
            if person.status == 'student' and len([x for x in person.house.occupants if x.independentStatus == True]) == 0:
                if person.mother.dead:
                    if person.father.dead:
                        person.independentStatus = True
                        self.startWorking(person)
                        if person.house == self.displayHouse:
                            messageString = str(self.year) + ": #" + str(person.id) + "'s parents are both dead."
                            self.textUpdateList.append(messageString)
                                
                            with open(os.path.join(policyFolder, "Log.csv"), "a") as file:
                                writer = csv.writer(file, delimiter = ",", lineterminator='\r')
                                writer.writerow([self.year, messageString])
                    else:
                        self.addMember(person.father.house, person.house,[person], 0, policyFolder)
                else:
                    self.addMember(person.mother.house, person.house, [person], 0, policyFolder)
            
            ## If somebody is a *child* at home and their parents have died, they need to be adopted
            if person.status == 'retired' and len([x for x in person.house.occupants if x.independentStatus == True]) == 0:
                person.independentStatus = True
            
            indipendentHealthyInHouse = len([x for x in person.house.occupants if x.independentStatus == True])
            if (person.status == 'child' or person.status == 'teenager') and indipendentHealthyInHouse == 0:
                potentialMothers = [x for x in self.pop.livingPeople if x.status != 'child' and x.sex == 'female' and x.partner != None]
                if person.mother.dead:
                    if person.father.dead:
                        if person.house == self.displayHouse:
                            messageString = str(self.year) + ": #" + str(person.id) + "will now be adopted."
                            self.textUpdateList.append(messageString)
                            
                            with open(os.path.join(policyFolder, "Log.csv"), "a") as file:
                                writer = csv.writer(file, delimiter = ",", lineterminator='\r')
                                writer.writerow([self.year, messageString])
        
                        while True:
                            adoptiveMother = random.choice(potentialMothers)
                            if adoptiveMother.status == 'worker' or adoptiveMother.partner.status == 'worker':
                                break
        
                        person.mother = adoptiveMother
                        adoptiveMother.children.append(person)
                        person.father = adoptiveMother.partner
                        adoptiveMother.partner.children.append(person)                
        
                        if adoptiveMother.house == self.displayHouse:
                            messageString = str(self.year) + ": #" + str(person.id) + " has been newly adopted by " + str(adoptiveMother.id) + "." 
                            self.textUpdateList.append(messageString)
                                
                            with open(os.path.join(policyFolder, "Log.csv"), "a") as file:
                                writer = csv.writer(file, delimiter = ",", lineterminator='\r')
                                writer.writerow([self.year, messageString])
                            
                            
                        self.addMember(adoptiveMother.house,person.house,[person], 0, policyFolder)   
                    else:
                        self.addMember(person.father.house, person.house,[person], 0, policyFolder)
                else:
                    self.addMember(person.mother.house, person.house,[person], 0, policyFolder)

    def doCareTransitions(self, policyFolder, month):
        """Consider the possibility of each person coming to require care."""
        peopleNotInCriticalCare = [x for x in self.pop.livingPeople if x.careNeedLevel < self.p['numCareLevels']-1]
        for person in peopleNotInCriticalCare:
            age = self.year - person.birthdate
            if person.sex == 'male':
                ageCareProb = ( ( math.exp( age /
                                            self.p['maleAgeCareScaling'] ) )
                               * self.p['personCareProb'] )
            else:
                ageCareProb = ( ( math.exp( age /
                                           self.p['femaleAgeCareScaling'] ) )
                               * self.p['personCareProb'] )
            careProb = self.p['baseCareProb'] + ageCareProb
            
            if np.random.random() < careProb and np.random.choice([x+1 for x in range(12)]) == month:
                multiStepTransition = np.random.random()
                if multiStepTransition < self.p['cdfCareTransition'][0]:
                    person.careNeedLevel += 1
                elif multiStepTransition < self.p['cdfCareTransition'][1]:
                    person.careNeedLevel += 2
                elif multiStepTransition < self.p['cdfCareTransition'][2]:
                    person.careNeedLevel += 3
                else:
                    person.careNeedLevel += 4
                    
                if person.careNeedLevel >= self.p['numCareLevels']:
                    person.careNeedLevel = int(self.p['numCareLevels'] - 1)
                            
                if person.house == self.displayHouse:
                    messageString = str(self.year) + ": #" + str(person.id) + " now has "
                    messageString += self.p['careLevelNames'][int(person.careNeedLevel)] + " care needs." 
                    self.textUpdateList.append(messageString)
                    
                    with open(os.path.join(policyFolder, "Log.csv"), "a") as file:
                        writer = csv.writer(file, delimiter = ",", lineterminator='\r')
                        writer.writerow([self.year, messageString])
    

           
    def doCareTransitions_UCN(self, policyFolder, month):
        """Consider the possibility of each person coming to require care."""
        peopleNotInCriticalCare = [x for x in self.pop.livingPeople if x.careNeedLevel < self.p['numCareLevels']-1]
        for person in peopleNotInCriticalCare:
            age = self.year - person.birthdate
            if person.sex == 'male':
                ageCareProb = ((math.exp(age/self.p['maleAgeCareScaling']))*self.p['personCareProb'] )
            else:
                ageCareProb = ((math.exp(age/self.p['femaleAgeCareScaling']))*self.p['personCareProb'] )
                
            baseProb = self.p['baseCareProb'] + ageCareProb
            
            baseProb = self.baseRate(self.p['careBias'], baseProb)
            
            unmetNeedFactor = 1.0/math.exp(self.p['unmetNeedExponent']*person.averageShareUnmetNeed)
            
            
            classRank = person.classRank
            if person.status == 'child' or person.status == 'student':
                classRank = person.parentsClassRank
            
            careProb = baseProb*math.pow(self.p['careBias'], classRank)/unmetNeedFactor 
            
            
            #### Alternative prob which depends on care level and unmet care need   #####################################
            # careProb = baseProb # baseProb*math.pow(self.p['careBias'], person.classRank)/unmetNeedFactor
            
            
            if np.random.random() < careProb and np.random.choice([x+1 for x in range(12)]) == month:
                baseTransition = self.baseRate(self.p['careBias'], 1.0-self.p['careTransitionRate'])
                if baseTransition >= 1.0:
                    print 'Error: base transition >= 1'
                    # sys.exit()
                    
                    
                if person.careNeedLevel > 0:
                    unmetNeedFactor = 1.0/math.exp(self.p['unmetNeedExponent']*person.averageShareUnmetNeed)
                else:
                    unmetNeedFactor = 1.0
                transitionRate = (1.0 - baseTransition*math.pow(self.p['careBias'], classRank))*unmetNeedFactor
                
                stepCare = 1
                bound = transitionRate
                
                while np.random.random() > bound and stepCare < self.p['numCareLevels'] - 1:
                    stepCare += 1
                    bound += (1.0-bound)*transitionRate
                    
                initialCareNeedLevel = person.careNeedLevel
                person.careNeedLevel += stepCare
                
                if person.careNeedLevel >= self.p['numCareLevels']:
                    person.careNeedLevel = int(self.p['numCareLevels'] - 1)
                if person.careNeedLevel > 1:
                    # person.status = 'inactive'
                    person.wage = 0
                    person.income = 0
                    person.workingHours = 0
                    person.weeklyTime = [[0]*24, [0]*24, [0]*24, [0]*24, [0]*24, [0]*24, [0]*24]
                    person.maxWeeklySupplies = [0, 0, 0, 0]
                    person.residualDailySupplies = [0]*7
                    person.residualWeeklySupplies = [x for x in person.maxWeeklySupplies]
                    
                if initialCareNeedLevel != person.careNeedLevel:
                    person.hoursSocialCareDemand = self.p['careDemandInHours'][person.careNeedLevel]
                    # person.weeklyNeeds = self.needsWeeklySchedule(person.careNeedLevel)
                           
                if person.house == self.displayHouse:
                    messageString = str(self.year) + ": #" + str(person.id) + " now has "
                    messageString += self.p['careLevelNames'][person.careNeedLevel] + " care needs." 
                    self.textUpdateList.append(messageString)
                    
                    with open(os.path.join(policyFolder, "Log.csv"), "a") as file:
                        writer = csv.writer(file, delimiter = ",", lineterminator='\r')
                        writer.writerow([self.year, messageString])
                
    def needsWeeklySchedule(self, careLevel):
        careNeed = self.p['careDemandInHours'][careLevel]
        weeklySchedule = [[0]*24, [0]*24, [0]*24, [0]*24, [0]*24, [0]*24, [0]*24]
        # Sample hours
        hoursOfNeed = []
        totHours = 0
        if np.random.random() < self.p['probHelpWithMeals'][careLevel-1]:
            hoursOfNeed.append(np.random.choice(self.p['mealsHours'][0]))
            hoursOfNeed.append(np.random.choice(self.p['mealsHours'][1]))
            totHours += 2*7
        while totHours < careNeed:
            activity = np.random.choice(self.p['careActivities'])
            if activity == 'morning':
                morningHours = [x for x in self.p['morningActivitiesHours'] if x not in hoursOfNeed]
                if len(morningHours) > 0:
                    hour = np.random.choice(morningHours)
                    hoursOfNeed.append(hour)
                    totHours += 7
            if activity == 'bedtime':
                eveningHours = [x for x in self.p['eveningActivitiesHours'] if x not in hoursOfNeed]
                if len(eveningHours) > 0:
                    hour = np.random.choice(eveningHours)
                    hoursOfNeed.append(hour)
                    totHours += 7
            if activity == 'miscellaneous':
                miscellaneousHours = [x for x in range(8, 23) if x not in hoursOfNeed]
                if len(miscellaneousHours) > 0:
                    hour = np.random.choice(miscellaneousHours)
                    hoursOfNeed.append(hour)
                    totHours += 7

        # Set the corresponding cells in the schedule matri to 1
        for hour in hoursOfNeed:
            indexFromHour = -1
            b = -7
            if hour < 8:
                b = 17
            indexFromHour = (hour-1)%24+b
            for i in weeklySchedule:
                i[indexFromHour] = 1
        return weeklySchedule
        
    
    def baseRate(self, bias, cp):
        a = 0
        for i in range(int(self.p['numberClasses'])):
            a += self.socialClassShares[i]*math.pow(bias, i)
        baseRate = cp/a
        return (baseRate)
    
    def updateUnmetCareNeed(self):
        
        for house in self.map.occupiedHouses:
            house.totalUnmetSocialCareNeed = sum([x.unmetSocialCareNeed for x in house.occupants])
            house.careNetwork.clear()
            house.suppliers[:] = []
            house.demandNetwork.clear()
            house.receivers[:] = []
        
        for person in self.pop.livingPeople:
            person.careNetwork.clear()
            person.suppliers[:] = []
            if person.careNeedLevel > 0:
                person.cumulativeUnmetNeed *= self.p['unmetCareNeedDiscountParam']
                person.cumulativeUnmetNeed += person.unmetSocialCareNeed
                person.totalDiscountedShareUnmetNeed *= self.p['shareUnmetNeedDiscountParam']
                person.totalDiscountedTime *= self.p['shareUnmetNeedDiscountParam']
                person.totalDiscountedShareUnmetNeed += person.unmetSocialCareNeed/person.hoursSocialCareDemand
                person.totalDiscountedTime += 1
                person.averageShareUnmetNeed = person.totalDiscountedShareUnmetNeed/person.totalDiscountedTime
    
    
    def startCareAllocation(self):
        # print 'Doing fucntion 5-a...'
        self.resetCareVariables_KN()
        # print 'Doing fucntion 5-b...'
        
        # print 'Doing fucntion 5.c...'
        self.computeSocialCareNeeds_W() # self.computeSocialCareNeeds_W() if social care paid with wealth
        # print 'Doing fucntion 5.d...'
        self.computeChildCareNeeds()
        # print 'Doing fucntion 5-e...'
        
        self.householdCareSupply()
        
        self.householdCareNetwork()
        
        self.updateNetworkSupplies()
        
        self.computeNetCareDemand()
        
        # self.computeTownAttractiveness()
        
    def computeAggregateSchedule(self):
        self.aggregateSchedule[:] = [0]*24
        workers = [x for x in self.pop.livingPeople if x.status == 'worker' if x.maternityStatus == False and x.careNeedLevel == 0]
        for worker in workers:
            for i in range(7):
                if i+1 not in worker.daysOff:
                    for j in range(24):
                        self.aggregateSchedule[j] += worker.jobSchedule[i][j]
                    
        # hoursFrequencies = [x for x in self.aggregateSchedule]
        print 'Hours frequencies: ' + str(self.aggregateSchedule)
    
    def checkTimeSchedule(self, agents):
        for agent in agents:
            print 'agent id: ' + str(agent.id)
            print 'agent status: ' + str(agent.status)
            print 'agent weekly schedule: ' + str(agent.weeklyTime)
    
    def allocateWeeklyCare(self):
        
        print 'Doing allocateWeeklyCare'
        
        
        # self.publicChildCare = 0
        self.parentsChildCare = 0
        self.householdChildCare = 0
        self.d1Childcare = 0
        self.d2Childcare = 0
        self.formalChildCare = 0
        self.outOfWorkChildCare_osh = 0
        self.outOfWorkChildCare_wsh = 0
        self.unmetChildCare = 0
        # We assume that parents first and foremost allocate their time to theri children, of whose care thery are primarily responsible
        

        for house in self.map.occupiedHouses:
            house.careSlots[:] = []
        
        CareProvision1_extim = 0
        CareProvision2_extim = 0
        CareProvision3_extim = 0
        CareProvision4_extim = 0
        CareProvision5_extim = 0
        CareProvision6_extim = 0
        CareProvision7_extim = 0
        
        self.internalChildCare = 0
        self.internalSocialCare = 0
        
        housesChildcareNeeds = [x for x in self.map.occupiedHouses if x.totalChildCareNeed > 0]
        for house in housesChildcareNeeds:
            household = [x for x in house.occupants]
            parents = [x for x in household if x.independentStatus == True]
            for i in range(7):
                for j in range(24):
                    if house.childrenCareNeedSchedule[i][j] > 0:
                        slotSuppliers = [x for x in parents if x.weeklyTime[i][j] == 1]
                        if len(slotSuppliers) > 0:
                            slotChildren = [x for x in house.childrenInNeedByHour[i][j]]
                            if i > 4 or (i < 5 and j > 9):
                                if sum([x.privateChildCareNeed_ONH for x in slotChildren]) > 0:
                                    careWeight = sum([np.exp(self.p['ageCareBeta']*np.power(x.privateChildCareNeed_ONH, self.p['ageDeltaExp'])) for x in slotChildren])
                                    cost = 0
                                    supplyWeight = sum([x.residualWeeklySupplies[0] for x in slotSuppliers])
                                    if np.power(supplyWeight, self.p['supplyWeightExp']) > 0:
                                        probIndex = careWeight/np.power(supplyWeight, self.p['supplyWeightExp'])
                                    else:
                                        probIndex = 0
                                    needSlot = CareSlot(house, i, j, True, careWeight, probIndex, cost, slotChildren, slotSuppliers)
                                    needSlot.minAge = min([x.age for x in slotChildren if x.privateChildCareNeed_ONH > 0])
                                    house.careSlots.append(needSlot)
                            else:
                                if sum([x.privateChildCareNeed_WNH for x in slotChildren]) > 0:
                                    careWeight = sum([np.exp(self.p['ageCareBeta']*np.power(x.privateChildCareNeed_WNH, self.p['ageDeltaExp'])) for x in slotChildren])
                                    cost = self.p['priceChildCare']*sum([x.privateChildCareNeed_WNH for x in slotChildren])
                                    supplyWeight = sum([x.residualWeeklySupplies[0] for x in slotSuppliers])
                                    supplyWeight += self.p['incomeCareFactor']*max(house.totalIncome-house.povertyLineIncome, 0.0)/cost
                                    if np.power(supplyWeight, self.p['supplyWeightExp']) > 0:
                                        probIndex = careWeight/np.power(supplyWeight, self.p['supplyWeightExp'])
                                    else:
                                        probIndex = 0
                                    needSlot = CareSlot(house, i, j, True, careWeight, probIndex, cost, slotChildren, slotSuppliers)
                                    needSlot.minAge = min([x.age for x in slotChildren if x.privateChildCareNeed_WNH > 0])
                                    house.careSlots.append(needSlot)
                                
            
            # Care provision 1: parents alocating all their free time
            
            start = time.time()
            
            wnhSlots = [x for x in house.careSlots if x.day < 5 and x.hour < 10]
            onhSlots = [x for x in house.careSlots if x not in wnhSlots]
            for careSlot in onhSlots:
                privateCare = sum([x.privateChildCareNeed_ONH for x in careSlot.receivers])
                if privateCare > 0:
                    supplier = np.random.choice(parents)
                    supplier.weeklyTime[careSlot.day][careSlot.hour] = 0
                    house.childrenCareNeedSchedule[careSlot.day][careSlot.hour] = 0
                    house.householdInformalSupplySchedule[careSlot.day][careSlot.hour] -= 1
                    house.childrenInNeedByHour[careSlot.day][careSlot.hour] = []
                    house.shiftTable[careSlot.day][careSlot.hour] = supplier
                    for d in range(4):
                        supplier.residualWeeklySupplies[d] -= 1
                        house.householdInformalSupplies[d] -= 1
                    supplier.residualWeeklySupplies = [max(x, 0) for x in supplier.residualWeeklySupplies]
                    house.householdInformalSupplies = [max(x, 0) for x in house.householdInformalSupplies]
                    if len(supplier.residualDailySupplies) < careSlot.day+1:
                        print careSlot.day
                        print supplier.residualDailySupplies
                        print supplier.age
                        print supplier.status
                        print supplier.careNeedLevel
                        
                    supplier.residualDailySupplies[careSlot.day] = max(supplier.residualDailySupplies[careSlot.day]-1, 0)
                    for i in range(len(supplier.residualDailySupplies)):
                        if supplier.residualWeeklySupplies[0] < supplier.residualDailySupplies[i]:
                            supplier.residualDailySupplies[i] = supplier.residualWeeklySupplies[0]
                    for agent in careSlot.receivers:
                        agent.unmetWeeklyNeeds[careSlot.day][careSlot.hour] = 0
                        agent.unmetChildCareNeed = max(agent.unmetChildCareNeed-1, 0)
                        agent.informalChildCareReceived += 1
                        self.internalChildCare += 1
                        agent.totalChildCareNeed = max(agent.totalChildCareNeed-1, 0)
                        agent.privateChildCareNeed_ONH = max(agent.privateChildCareNeed_ONH-1, 0)
                        house.privateChildCareNeed_ONH -= 1
                        house.totalChilcareNeed_ONH -= 1
                        house.totalUnmetChildCareNeed -= 1
            
            wnhSlots.sort(key=operator.attrgetter("numReceivers"))
            for careSlot in wnhSlots:
                privateCare = sum([x.privateChildCareNeed_WNH for x in careSlot.receivers])
                if privateCare > 0:
                    supplier = np.random.choice(parents)
                    supplier.weeklyTime[careSlot.day][careSlot.hour] = 0
                    house.childrenCareNeedSchedule[careSlot.day][careSlot.hour] = 0
                    house.householdInformalSupplySchedule[careSlot.day][careSlot.hour] -= 1
                    house.childrenInNeedByHour[careSlot.day][careSlot.hour] = []
                    house.shiftTable[careSlot.day][careSlot.hour] = supplier
                    for d in range(4):
                        supplier.residualWeeklySupplies[d] -= 1
                        house.householdInformalSupplies[d] -= 1
                    supplier.residualWeeklySupplies = [max(x, 0) for x in supplier.residualWeeklySupplies]
                    house.householdInformalSupplies = [max(x, 0) for x in house.householdInformalSupplies]
                    supplier.residualDailySupplies[careSlot.day] = max(supplier.residualDailySupplies[careSlot.day]-1, 0)
                    for i in range(len(supplier.residualDailySupplies)):
                        if supplier.residualWeeklySupplies[0] < supplier.residualDailySupplies[i]:
                            supplier.residualDailySupplies[i] = supplier.residualWeeklySupplies[0]
                    for agent in careSlot.receivers:
                        agent.unmetWeeklyNeeds[careSlot.day][careSlot.hour] = 0
                        agent.unmetChildCareNeed = max(agent.unmetChildCareNeed-1, 0)
                        agent.totalChildCareNeed = max(agent.totalChildCareNeed-1, 0)
                        agent.informalChildCareReceived += 1
                        self.internalChildCare += 1
                        house.totalChilcareNeed_WNH -= 1
                        house.totalUnmetChildCareNeed -= 1
                        agent.privateChildCareNeed_WNH = max(agent.privateChildCareNeed_WNH-1, 0)
                        house.privateChildCareNeed_WNH -= 1
                        
            end = time.time()
            CareProvision1_extim += (end - start)
            
        for house in self.map.occupiedHouses:
            house.totalChildCareNeed = sum([(x.privateChildCareNeed_WNH+x.privateChildCareNeed_ONH) for x in house.childCareRecipients])
            house.totalSocialCareNeed = sum([x.privateSocialCareNeed for x in house.socialCareRecipients])
            house.totalCareNeed = house.totalChildCareNeed+house.totalSocialCareNeed
        # Create a list of the household's childcare slots
        # Add the list of social care needs
        
        housesWSCCN = [x for x in self.map.occupiedHouses if x.totalCareNeed > 0]
        for house in housesWSCCN:
            householdSuppliers = [x for x in house.occupants if x.potentialCarer == True]
            house.careSlots[:] = []
            for i in range(7):
                for j in range(24):
                    if house.childrenCareNeedSchedule[i][j] > 0:
                        slotSuppliers = [x for x in householdSuppliers if x.residualDailySupplies[i] > 0 and x.weeklyTime[i][j] == 1]
                        if len(slotSuppliers) > 0:
                            slotChildren = [x for x in house.childrenInNeedByHour[i][j]]
                            if i > 4 or (i < 5 and j > 9):
                                if sum([x.privateChildCareNeed_ONH for x in slotChildren]) > 0:
                                    careWeight = sum([np.exp(self.p['ageCareBeta']*np.power(x.privateChildCareNeed_ONH, self.p['ageDeltaExp'])) for x in slotChildren])
                                    cost = 0
                                    supplyWeight = sum([x.residualWeeklySupplies[0] for x in slotSuppliers])
                                    if np.power(supplyWeight, self.p['supplyWeightExp']) > 0:
                                        probIndex = careWeight/np.power(supplyWeight, self.p['supplyWeightExp'])
                                    else:
                                        probIndex = 0
                                    needSlot = CareSlot(house, i, j, True, careWeight, probIndex, cost, slotChildren, slotSuppliers)
                                    needSlot.minAge = min([x.age for x in slotChildren if x.privateChildCareNeed_ONH > 0])
                                    house.careSlots.append(needSlot)
                            else:
                                if sum([x.privateChildCareNeed_WNH for x in slotChildren]) > 0:
                                    careWeight = sum([np.exp(self.p['ageCareBeta']*np.power(x.privateChildCareNeed_WNH, self.p['ageDeltaExp'])) for x in slotChildren])
                                    cost = self.p['priceChildCare']*sum([x.privateChildCareNeed_WNH for x in slotChildren])
                                    supplyWeight = sum([x.residualWeeklySupplies[0] for x in slotSuppliers])
                                    supplyWeight += self.p['incomeCareFactor']*max(house.totalIncome-house.povertyLineIncome, 0.0)/cost
                                    if np.power(supplyWeight, self.p['supplyWeightExp']) > 0:
                                        probIndex = careWeight/np.power(supplyWeight, self.p['supplyWeightExp'])
                                    else:
                                        probIndex = 0
                                    needSlot = CareSlot(house, i, j, True, careWeight, probIndex, cost, slotChildren, slotSuppliers)
                                    needSlot.minAge = min([x.age for x in slotChildren if x.privateChildCareNeed_WNH > 0])
                                    house.careSlots.append(needSlot)
                                
            socialCareReceivers = [x for x in house.occupants if x.privateSocialCareNeed > 0]
            for person in socialCareReceivers:
                # These agents have a number of fixed hours (associated to day and hour)
                # and a number of flexible hours.
                for i in range(7):
                    if person.fixedNeedSchedule[0][0] == 1:
                        hour = 0
                        slotSuppliers = [x for x in householdSuppliers if x.residualDailySupplies[i] > 0 and x.weeklyTime[i][hour] == 1]
                        if len(slotSuppliers) > 0 and person.privateSocialCareNeed > 0:
                            careWeight = np.exp(self.p['socialCareBeta']*np.power(person.privateSocialCareNeed, self.p['careDeltaExp']))
                            cost = self.p['priceSocialCare']
                            supplyWeight = sum([x.residualWeeklySupplies[0] for x in slotSuppliers])
                            supplyWeight += self.p['incomeCareFactor']*max(house.totalIncome-house.povertyLineIncome, 0.0)/cost
                            probIndex = careWeight/np.power(supplyWeight, self.p['supplyWeightExp'])
                            needSlot = CareSlot(house, i, hour, False, careWeight, probIndex, cost, [person], slotSuppliers)
                            house.careSlots.append(needSlot)
                        
                    if person.fixedNeedSchedule[0][1] == 1:
                        hour = 1
                        slotSuppliers = [x for x in householdSuppliers if x.residualDailySupplies[i] > 0 and x.weeklyTime[i][hour] == 1]
                        if len(slotSuppliers) > 0 and person.privateSocialCareNeed > 0:
                            careWeight = np.exp(self.p['socialCareBeta']*np.power(person.privateSocialCareNeed, self.p['careDeltaExp']))
                            cost = self.p['priceSocialCare']
                            supplyWeight = sum([x.residualWeeklySupplies[0] for x in slotSuppliers])
                            supplyWeight += self.p['incomeCareFactor']*max(house.totalIncome-house.povertyLineIncome, 0.0)/cost
                            probIndex = careWeight/np.power(supplyWeight, self.p['supplyWeightExp'])
                            needSlot = CareSlot(house, i, hour, False, careWeight, probIndex, cost, [person], slotSuppliers)
                            house.careSlots.append(needSlot)
                        
                    if person.fixedNeedSchedule[1][0] == 1:
                        hour = 4
                        slotSuppliers = [x for x in householdSuppliers if x.residualDailySupplies[i] > 0 and x.weeklyTime[i][hour] == 1]
                        if len(slotSuppliers) > 0 and person.privateSocialCareNeed > 0:
                            careWeight = np.exp(self.p['socialCareBeta']*np.power(person.privateSocialCareNeed, self.p['careDeltaExp']))
                            cost = self.p['priceSocialCare']
                            supplyWeight = sum([x.residualWeeklySupplies[0] for x in slotSuppliers])
                            supplyWeight += self.p['incomeCareFactor']*max(house.totalIncome-house.povertyLineIncome, 0.0)/cost    
                            probIndex = careWeight/np.power(supplyWeight, self.p['supplyWeightExp'])
                            needSlot = CareSlot(house, i, hour, False, careWeight, probIndex, cost, [person], slotSuppliers)
                            house.careSlots.append(needSlot)
                        
                    if person.fixedNeedSchedule[1][1] == 1:
                        hour = 5
                        slotSuppliers = [x for x in householdSuppliers if x.residualDailySupplies[i] > 0 and x.weeklyTime[i][hour] == 1]
                        if len(slotSuppliers) > 0 and person.privateSocialCareNeed > 0:
                            careWeight = np.exp(self.p['socialCareBeta']*np.power(person.privateSocialCareNeed, self.p['careDeltaExp']))
                            cost = self.p['priceSocialCare']
                            supplyWeight = sum([x.residualWeeklySupplies[0] for x in slotSuppliers])
                            supplyWeight += self.p['incomeCareFactor']*max(house.totalIncome-house.povertyLineIncome, 0.0)/cost
                            probIndex = careWeight/np.power(supplyWeight, self.p['supplyWeightExp'])
                            needSlot = CareSlot(house, i, hour, False, careWeight, probIndex, cost, [person], slotSuppliers)
                            house.careSlots.append(needSlot)
                        
                    if person.fixedNeedSchedule[2][0] == 1:
                        hour = 10
                        slotSuppliers = [x for x in householdSuppliers if x.residualDailySupplies[i] > 0 and x.weeklyTime[i][hour] == 1]
                        if len(slotSuppliers) > 0 and person.privateSocialCareNeed > 0:
                            careWeight = np.exp(self.p['socialCareBeta']*np.power(person.privateSocialCareNeed, self.p['careDeltaExp']))
                            cost = self.p['priceSocialCare']
                            supplyWeight = sum([x.residualWeeklySupplies[0] for x in slotSuppliers])
                            supplyWeight += self.p['incomeCareFactor']*max(house.totalIncome-house.povertyLineIncome, 0.0)/cost
                            probIndex = careWeight/np.power(supplyWeight, self.p['supplyWeightExp'])
                            needSlot = CareSlot(house, i, hour, False, careWeight, probIndex, cost, [person], slotSuppliers)
                            house.careSlots.append(needSlot)
                        
                    if person.fixedNeedSchedule[2][1] == 1:
                        hour = 11
                        slotSuppliers = [x for x in householdSuppliers if x.residualDailySupplies[i] > 0 and x.weeklyTime[i][hour] == 1]
                        if len(slotSuppliers) > 0 and person.privateSocialCareNeed > 0:
                            careWeight = np.exp(self.p['socialCareBeta']*np.power(person.privateSocialCareNeed, self.p['careDeltaExp']))
                            cost = self.p['priceSocialCare']
                            supplyWeight = sum([x.residualWeeklySupplies[0] for x in slotSuppliers])
                            supplyWeight += self.p['incomeCareFactor']*max(house.totalIncome-house.povertyLineIncome, 0.0)/cost
                            probIndex = careWeight/np.power(supplyWeight, self.p['supplyWeightExp'])
                            needSlot = CareSlot(house, i, hour, False, careWeight, probIndex, cost, [person], slotSuppliers)
                            house.careSlots.append(needSlot)
                        
                    if person.fixedNeedSchedule[3][0] == 1:
                        hour = 13
                        slotSuppliers = [x for x in householdSuppliers if x.residualDailySupplies[i] > 0 and x.weeklyTime[i][hour] == 1]
                        if len(slotSuppliers) > 0 and person.privateSocialCareNeed > 0:
                            careWeight = np.exp(self.p['socialCareBeta']*np.power(person.privateSocialCareNeed, self.p['careDeltaExp']))
                            cost = self.p['priceSocialCare']
                            supplyWeight = sum([x.residualWeeklySupplies[0] for x in slotSuppliers])
                            supplyWeight += self.p['incomeCareFactor']*max(house.totalIncome-house.povertyLineIncome, 0.0)/cost
                            probIndex = careWeight/np.power(supplyWeight, self.p['supplyWeightExp'])
                            needSlot = CareSlot(house, i, hour, False, careWeight, probIndex, cost, [person], slotSuppliers)
                            house.careSlots.append(needSlot)
                        
                    if person.fixedNeedSchedule[3][1] == 1:
                        hour = 14
                        slotSuppliers = [x for x in householdSuppliers if x.residualDailySupplies[i] > 0 and x.weeklyTime[i][hour] == 1]
                        if len(slotSuppliers) > 0 and person.privateSocialCareNeed > 0:
                            careWeight = np.exp(self.p['socialCareBeta']*np.power(person.privateSocialCareNeed, self.p['careDeltaExp']))
                            cost = self.p['priceSocialCare']
                            supplyWeight = sum([x.residualWeeklySupplies[0] for x in slotSuppliers])
                            supplyWeight += self.p['incomeCareFactor']*max(house.totalIncome-house.povertyLineIncome, 0.0)/cost
                            probIndex = careWeight/np.power(supplyWeight, self.p['supplyWeightExp'])
                            needSlot = CareSlot(house, i, hour, False, careWeight, probIndex, cost, [person], slotSuppliers)
                            house.careSlots.append(needSlot)
                            
                    for j in range(person.weelyFlexibleNeeds[i]):
                        slotSuppliers = [x for x in householdSuppliers if x.residualDailySupplies[i] > 0 and sum(x.weeklyTime[i][:10]) > 0]
                        if len(slotSuppliers) > 0 and person.privateSocialCareNeed > 0:
                            careWeight = np.exp(self.p['socialCareBeta']*np.power(person.privateSocialCareNeed, self.p['careDeltaExp']))
                            cost = self.p['priceSocialCare']
                            supplyWeight = sum([x.residualWeeklySupplies[0] for x in slotSuppliers])
                            supplyWeight += self.p['incomeCareFactor']*max(house.totalIncome-house.povertyLineIncome, 0.0)/cost
                            probIndex = careWeight/np.power(supplyWeight, self.p['supplyWeightExp'])
                            needSlot = CareSlot(house, i, -1, False, careWeight, probIndex, cost, [person], slotSuppliers)
                            house.careSlots.append(needSlot)
                
            ## Now a loop starts for the internal allocation of care
            ## The loop stops when either there is no more residual care need or no more available supply.
            # 1- Select all the care slots with children aged 7 or below
            # Loop to assign informal care and out-of-hours care 
            start = time.time()
            
            priorityCareSlots = [x for x in house.careSlots if x.childCare == True and x.minAge < self.p['priorityAgeThreshold']]
            while len(priorityCareSlots) > 0:
                # 1 - A care slot is randomly sampled
                weights = [x.probIndex for x in priorityCareSlots]
                probs = [x/sum(weights) for x in weights]
                careSlot = np.random.choice(priorityCareSlots, p = probs)
                # 2 - A supplier is sampled based on residual daily (or weekly, for flexible care) supply
                weightSuppliers = [float(x.residualDailySupplies[careSlot.day]) for x in careSlot.suppliers]
                if sum(weightSuppliers) == 0:
                    print [x.residualDailySupplies[careSlot.day] for x in careSlot.suppliers]
                probs = [x/sum(weightSuppliers) for x in weightSuppliers]
                supplier = np.random.choice(careSlot.suppliers, p = probs)
                # 3 - All the time need and time records are updated
                supplier.weeklyTime[careSlot.day][careSlot.hour] = 0
                house.childrenCareNeedSchedule[careSlot.day][careSlot.hour] = 0
                house.householdInformalSupplySchedule[careSlot.day][careSlot.hour] -= 1
                house.childrenInNeedByHour[careSlot.day][careSlot.hour] = []
                house.shiftTable[careSlot.day][careSlot.hour] = supplier
                for d in range(4):
                    supplier.residualWeeklySupplies[d] -= 1
                    house.householdInformalSupplies[d] -= 1
                supplier.residualWeeklySupplies = [max(x, 0) for x in supplier.residualWeeklySupplies]
                house.householdInformalSupplies = [max(x, 0) for x in house.householdInformalSupplies]
                supplier.residualDailySupplies[careSlot.day] = max(supplier.residualDailySupplies[careSlot.day]-1, 0)
                for i in range(len(supplier.residualDailySupplies)):
                    if supplier.residualWeeklySupplies[0] < supplier.residualDailySupplies[i]:
                        supplier.residualDailySupplies[i] = supplier.residualWeeklySupplies[0]
                for agent in careSlot.receivers:
                    agent.unmetWeeklyNeeds[careSlot.day][careSlot.hour] = 0
                    agent.unmetChildCareNeed = max(agent.unmetChildCareNeed-1, 0)
                    agent.totalChildCareNeed = max(agent.totalChildCareNeed-1, 0)
                    agent.informalChildCareReceived += 1
                    self.internalChildCare += 1
                    # house.totalChildCareNeed -= 1
                    house.totalUnmetChildCareNeed -= 1
                    if careSlot.day < 5 and careSlot.hour < 10:
                        agent.privateChildCareNeed_WNH = max(agent.privateChildCareNeed_WNH-1, 0)
                        house.privateChildCareNeed_WNH -= 1
                        house.totalChilcareNeed_WNH -= 1
                    else:
                        house.totalChilcareNeed_ONH -= 1
                        agent.privateChildCareNeed_ONH = max(agent.privateChildCareNeed_ONH-1, 0)
                        house.privateChildCareNeed_ONH -= 1
                # 4 - The pool of 'active' care slots is updated
                priorityCareSlots.remove(careSlot)
                house.careSlots.remove(careSlot)
                # Update slots
                residualSlots = [x for x in priorityCareSlots if len([y for y in x.suppliers if y.residualDailySupplies[x.day] > 0]) > 0]
                house.careSlots = [x for x in house.careSlots if len([y for y in x.suppliers if y.residualDailySupplies[x.day] > 0]) > 0]
                for slot in residualSlots:
                    if careSlot.day < 5 and careSlot.hour < 10:
                        careWeight = sum([np.exp(self.p['ageCareBeta']*np.power(x.privateChildCareNeed_WNH, self.p['ageDeltaExp'])) for x in slot.receivers])
                    else:
                        careWeight = sum([np.exp(self.p['ageCareBeta']*np.power(x.privateChildCareNeed_ONH, self.p['ageDeltaExp'])) for x in slot.receivers])
                    slot.careWeight = careWeight
                    supplyWeight = sum([x.residualWeeklySupplies[0] for x in slot.suppliers])
                    if slot.day < 5 and slot.hour < 10: # In this case, childcare can be bought
                        supplyWeight += self.p['incomeCareFactor']*max(house.totalIncome-house.povertyLineIncome, 0.0)/slot.cost
                    slot.probIndex = slot.careWeight/np.power(supplyWeight, self.p['supplyWeightExp'])
                slots_WNH = [x for x in house.careSlots if x.day < 5 and x.hour < 10]
                slots_ONH = [x for x in house.careSlots if x not in slots_WNH]
                house.careSlots = [x for x in slots_WNH if sum([y.privateChildCareNeed_WNH for y in x.receivers])> 0] + [x for x in slots_ONH if sum([y.privateChildCareNeed_ONH for y in x.receivers])> 0]
                slots_WNH = [x for x in residualSlots if x.day < 5 and x.hour < 10]
                slots_ONH = [x for x in residualSlots if x not in slots_WNH]
                priorityCareSlots = [x for x in slots_WNH if sum([y.privateChildCareNeed_WNH for y in x.receivers])> 0] + [x for x in slots_ONH if sum([y.privateChildCareNeed_ONH for y in x.receivers])> 0]
            
            end = time.time()
            CareProvision2_extim += (end - start)
            
            start = time.time()
            # repeat the loop for the remaining 'active' slots
            while len(house.careSlots) > 0:
                # 1 - A care slot is randomly sampled
                weights = [x.probIndex for x in house.careSlots]
                probs = [x/sum(weights) for x in weights]
                careSlot = np.random.choice(house.careSlots, p = probs)
                # 2 - A supplier is sampled based on residual daily supply
                weightSuppliers = [float(x.residualDailySupplies[careSlot.day]) for x in careSlot.suppliers]
                probs = [x/sum(weightSuppliers) for x in weightSuppliers]
                supplier = np.random.choice(careSlot.suppliers, p = probs)
                # Update supply's record
                supplier.weeklyTime[careSlot.day][careSlot.hour] = 0
                house.householdInformalSupplySchedule[careSlot.day][careSlot.hour] -= 1
                house.childrenInNeedByHour[careSlot.day][careSlot.hour] = []
                house.shiftTable[careSlot.day][careSlot.hour] = supplier
                for d in range(4):
                    supplier.residualWeeklySupplies[d] -= 1
                    house.householdInformalSupplies[d] -= 1
                supplier.residualWeeklySupplies = [max(x, 0) for x in supplier.residualWeeklySupplies]
                house.householdInformalSupplies = [max(x, 0) for x in house.householdInformalSupplies]
                supplier.residualDailySupplies[careSlot.day] = max(supplier.residualDailySupplies[careSlot.day]-1, 0)
                for i in range(len(supplier.residualDailySupplies)):
                    if supplier.residualWeeklySupplies[0] < supplier.residualDailySupplies[i]:
                        supplier.residualDailySupplies[i] = supplier.residualWeeklySupplies[0]
                # Update receivers' records
                if careSlot.childCare == True:
                    house.childrenCareNeedSchedule[careSlot.day][careSlot.hour] = 0
                    for agent in careSlot.receivers:
                        agent.unmetWeeklyNeeds[careSlot.day][careSlot.hour] = 0
                        agent.unmetChildCareNeed = max(agent.unmetChildCareNeed-1, 0)
                        agent.totalChildCareNeed = max(agent.totalChildCareNeed-1, 0)
                        agent.informalChildCareReceived += 1
                        self.internalChildCare += 1
                        # house.totalChildCareNeed -= 1
                        house.totalUnmetChildCareNeed -= 1
                        if careSlot.day < 5 and careSlot.hour < 10:
                            agent.privateChildCareNeed_WNH = max(agent.privateChildCareNeed_WNH-1, 0)
                            house.privateChildCareNeed_WNH -= 1
                            house.totalChilcareNeed_WNH -= 1
                        else:
                            house.totalChilcareNeed_ONH -= 1
                            agent.privateChildCareNeed_ONH = max(agent.privateChildCareNeed_ONH-1, 0)
                            house.privateChildCareNeed_ONH -= 1
                else:
                    supplier.socialWork += 1
                    person = careSlot.receivers[0]
                    person.privateSocialCareNeed = max(person.privateSocialCareNeed-1, 0)
                    person.unmetSocialCareNeed = max(person.unmetSocialCareNeed-1, 0)
                    person.informalSocialCareReceived += 1
                    self.internalSocialCare += 1
                    # house.totalSocialCareNeed -= 1
                    house.totalUnmetSocialCareNeed -= 1
                    if careSlot.hour == -1:
                        person.weelyFlexibleNeeds[careSlot.day] = max(person.weelyFlexibleNeeds[careSlot.day]-1, 0)
                    else:
                        if careSlot.hour == 0:
                            person.fixedNeedSchedule[0][0] = 0
                        elif careSlot.hour == 1:
                            person.fixedNeedSchedule[0][1] = 0
                        elif careSlot.hour == 4:
                            person.fixedNeedSchedule[1][0] = 0
                        elif careSlot.hour == 5:
                            person.fixedNeedSchedule[1][1] = 0
                        elif careSlot.hour == 10:
                            person.fixedNeedSchedule[2][0] = 0
                        elif careSlot.hour == 11:
                            person.fixedNeedSchedule[2][1] = 0
                        elif careSlot.hour == 13:
                            person.fixedNeedSchedule[3][0] = 0
                        elif careSlot.hour == 14:
                            person.fixedNeedSchedule[3][1] = 0
                # Update slots
#                house.totalChildCareNeed = sum([(x.privateChildCareNeed_WNH+x.privateChildCareNeed_ONH) for x in house.childCareRecipients])
#                house.totalSocialCareNeed = sum([x.privateSocialCareNeed for x in house.socialCareRecipients])
#                house.totalCareNeed = house.totalChildCareNeed+house.totalSocialCareNeed
                house.careSlots.remove(careSlot)
                notFlexibleSlots = [x for x in house.careSlots if x.hour != -1]
                flexibleSlots = [x for x in house.careSlots if x.hour == -1]
                house.careSlots = [x for x in notFlexibleSlots if len([y for y in x.suppliers if y.residualDailySupplies[x.day] > 0]) > 0]
                house.careSlots += [x for x in flexibleSlots if len([y for y in x.suppliers if y.residualDailySupplies[x.day] > 0 and sum(y.weeklyTime[x.day][:10]) > 0]) > 0]
                for slot in house.careSlots:
                    if slot.childCare == True:
                        if slot.day < 5 and slot.hour < 10:
                            careWeight = sum([np.exp(self.p['ageCareBeta']*np.power(x.privateChildCareNeed_WNH, self.p['ageDeltaExp'])) for x in slot.receivers])
                        else:
                            careWeight = sum([np.exp(self.p['ageCareBeta']*np.power(x.privateChildCareNeed_ONH, self.p['ageDeltaExp'])) for x in slot.receivers])
                        slot.careWeight = careWeight
                        supplyWeight = sum([x.residualWeeklySupplies[0] for x in slot.suppliers])
                        if slot.day < 5 and slot.hour < 10: # In this case, childcare can be bought
                            supplyWeight += self.p['incomeCareFactor']*max(house.totalIncome-house.povertyLineIncome, 0.0)/slot.cost
                        slot.probIndex = slot.careWeight/np.power(supplyWeight, self.p['supplyWeightExp'])
                    else:
                        slot.careWeight = np.exp(self.p['socialCareBeta']*np.power(slot.receivers[0].privateSocialCareNeed, self.p['careDeltaExp']))
                        supplyWeight = sum([x.residualWeeklySupplies[0] for x in slot.suppliers])
                        supplyWeight += self.p['incomeCareFactor']*max(house.totalIncome-house.povertyLineIncome, 0.0)/slot.cost
                        slot.probIndex = slot.careWeight/np.power(supplyWeight, self.p['supplyWeightExp'])
                slots_WNH = [x for x in house.careSlots if x.childCare == True and x.day < 5 and x.hour < 10]
                slots_ONH = [x for x in house.careSlots if x.childCare == True and x not in slots_WNH]
                socialSlots = [x for x in house.careSlots if x.childCare == False]
                house.careSlots = [x for x in slots_WNH if sum([y.privateChildCareNeed_WNH for y in x.receivers])> 0] + [x for x in slots_ONH if sum([y.privateChildCareNeed_ONH for y in x.receivers])> 0]
                house.careSlots += [x for x in socialSlots if sum([y.privateSocialCareNeed for y in x.receivers])> 0]
            
            end = time.time()
            CareProvision3_extim += (end - start)
            
        for house in self.map.occupiedHouses:
            house.totalChildCareNeed = sum([(x.privateChildCareNeed_WNH+x.privateChildCareNeed_ONH) for x in house.childCareRecipients])
            priorityChildren = [x for x in house.childCareRecipients if x.age < self.p['priorityAgeThreshold']]
            house.totalPriorityCareNeed = sum([(x.privateChildCareNeed_WNH+x.privateChildCareNeed_ONH) for x in priorityChildren])
            house.totalSocialCareNeed = sum([x.privateSocialCareNeed for x in house.socialCareRecipients])
            house.totalCareNeed = house.totalChildCareNeed+house.totalSocialCareNeed
            # Compute care need residual care supply of household after internal provision
            # (Used in relocation)
            house.needAfterHouseholdCare = house.totalCareNeed
            house.availableWeeklySupplies = []
            for d in range(4):
                careSupply = sum([x.residualWeeklySupplies[d] for x in house.occupants if x.potentialCarer == True])
                house.availableWeeklySupplies.append(careSupply)
         
        # Repeat for the external care.
        # The suppliers in these case are the members of the households of relatives at kinship distance 1
        # First, a receiving housheold is sampled with probability proportional to the residual total care need,
        # divided by the household's income.
        # Then, the above loop is repeated.
        
        # Repeat twice
        
        if self.p['externalCare'] == True:
            self.externalChildCare = 0
            self.externalSocialCare = 0
            for d in range(2):
                kd = d+1
                for house in self.map.occupiedHouses:
                    house.careSlots[:] = []
                    house.priorityCareSlots = []
                # Start loopd with extranl informal care
                housesWSCCN = [x for x in self.map.occupiedHouses if house.totalCareNeed > 0]
                for house in housesWSCCN:
                    for i in range(7):
                        for j in range(24):
                            if house.childrenCareNeedSchedule[i][j] > 0:
                                # The suppliers here are all the members of the households at kinship distance 1
                                slotSuppliers = self.getHouseSuppliers(house, i, j, kd)
                                if len(slotSuppliers) > 0:
                                    slotChildren = [x for x in house.childrenInNeedByHour[i][j]]
                                    if i > 4 or (i < 5 and j > 9):
                                        if sum([x.privateChildCareNeed_ONH for x in slotChildren]) > 0:
                                            careWeight = sum([np.exp(self.p['ageCareBeta']*np.power(x.privateChildCareNeed_ONH, self.p['ageDeltaExp'])) for x in slotChildren])
                                            cost = 0
                                            supplyWeight = sum([x.residualWeeklySupplies[kd] for x in slotSuppliers])
                                            if np.power(supplyWeight, self.p['supplyWeightExp']) > 0:
                                                probIndex = careWeight/np.power(supplyWeight, self.p['supplyWeightExp'])
                                            else:
                                                probIndex = 0
                                            needSlot = CareSlot(house, i, j, True, careWeight, probIndex, cost, slotChildren, slotSuppliers)
                                            needSlot.minAge = min([x.age for x in slotChildren if x.privateChildCareNeed_ONH > 0])
                                            house.careSlots.append(needSlot)
                                    else:
                                        if sum([x.privateChildCareNeed_WNH for x in slotChildren]) > 0:
                                            careWeight = sum([np.exp(self.p['ageCareBeta']*np.power(x.privateChildCareNeed_WNH, self.p['ageDeltaExp'])) for x in slotChildren])
                                            cost = self.p['priceChildCare']*sum([x.privateChildCareNeed_WNH for x in slotChildren])
                                            supplyWeight = sum([x.residualWeeklySupplies[kd] for x in slotSuppliers])
                                            supplyWeight += self.p['incomeCareFactor']*max(house.totalPotentialIncome-house.povertyLineIncome, 0.0)/cost
                                            if np.power(supplyWeight, self.p['supplyWeightExp']) > 0:
                                                probIndex = careWeight/np.power(supplyWeight, self.p['supplyWeightExp'])
                                            else:
                                                probIndex = 0
                                            needSlot = CareSlot(house, i, j, True, careWeight, probIndex, cost, slotChildren, slotSuppliers)
                                            needSlot.minAge = min([x.age for x in slotChildren if x.privateChildCareNeed_WNH > 0])
                                            house.careSlots.append(needSlot)
                    house.priorityCareSlots = [x for x in house.careSlots if x.childCare == True and x.minAge < self.p['priorityAgeThreshold']]        
                    priorityChildren = [x for x in house.childCareRecipients if x.age < self.p['priorityAgeThreshold']]
                    house.totalPriorityCareNeed = sum([(x.privateChildCareNeed_WNH+x.privateChildCareNeed_ONH) for x in priorityChildren])
                    socialCareReceivers = [x for x in house.occupants if x.privateSocialCareNeed > 0]
                    for person in socialCareReceivers:
                        # These agents have a number of fixed hours (associated to day and hour)
                        # and a number of flexible hours.
                        for i in range(7):
                            if person.fixedNeedSchedule[0][0] == 1:
                                hour = 0
                                slotSuppliers = self.getPersonSuppliers(person, i, hour, kd)
                                if len(slotSuppliers) > 0 and person.privateSocialCareNeed > 0:
                                    careWeight = np.exp(self.p['socialCareBeta']*np.power(person.privateSocialCareNeed, self.p['careDeltaExp']))
                                    cost = self.p['priceSocialCare']
                                    supplyWeight = sum([x.residualWeeklySupplies[kd] for x in slotSuppliers])
                                    supplyWeight += self.p['incomeCareFactor']*max(house.totalPotentialIncome-house.povertyLineIncome, 0.0)/cost
                                    probIndex = careWeight/np.power(supplyWeight, self.p['supplyWeightExp'])
                                    needSlot = CareSlot(house, i, hour, False, careWeight, probIndex, cost, [person], slotSuppliers)
                                    house.careSlots.append(needSlot)
                                
                            if person.fixedNeedSchedule[0][1] == 1:
                                hour = 1
                                slotSuppliers = self.getPersonSuppliers(person, i, hour, kd)
                                if len(slotSuppliers) > 0 and person.privateSocialCareNeed > 0:
                                    careWeight = np.exp(self.p['socialCareBeta']*np.power(person.privateSocialCareNeed, self.p['careDeltaExp']))
                                    cost = self.p['priceSocialCare']
                                    supplyWeight = sum([x.residualWeeklySupplies[kd] for x in slotSuppliers])
                                    supplyWeight += self.p['incomeCareFactor']*max(house.totalPotentialIncome-house.povertyLineIncome, 0.0)/cost
                                    probIndex = careWeight/np.power(supplyWeight, self.p['supplyWeightExp'])
                                    needSlot = CareSlot(house, i, hour, False, careWeight, probIndex, cost, [person], slotSuppliers)
                                    house.careSlots.append(needSlot)
                                
                            if person.fixedNeedSchedule[1][0] == 1:
                                hour = 4
                                slotSuppliers = self.getPersonSuppliers(person, i, hour, kd)
                                if len(slotSuppliers) > 0 and person.privateSocialCareNeed > 0:
                                    careWeight = np.exp(self.p['socialCareBeta']*np.power(person.privateSocialCareNeed, self.p['careDeltaExp']))
                                    cost = self.p['priceSocialCare']
                                    supplyWeight = sum([x.residualWeeklySupplies[kd] for x in slotSuppliers])
                                    supplyWeight += self.p['incomeCareFactor']*max(house.totalPotentialIncome-house.povertyLineIncome, 0.0)/cost    
                                    probIndex = careWeight/np.power(supplyWeight, self.p['supplyWeightExp'])
                                    needSlot = CareSlot(house, i, hour, False, careWeight, probIndex, cost, [person], slotSuppliers)
                                    house.careSlots.append(needSlot)
                                
                            if person.fixedNeedSchedule[1][1] == 1:
                                hour = 5
                                slotSuppliers = self.getPersonSuppliers(person, i, hour, kd)
                                if len(slotSuppliers) > 0 and person.privateSocialCareNeed > 0:
                                    careWeight = np.exp(self.p['socialCareBeta']*np.power(person.privateSocialCareNeed, self.p['careDeltaExp']))
                                    cost = self.p['priceSocialCare']
                                    supplyWeight = sum([x.residualWeeklySupplies[kd] for x in slotSuppliers])
                                    supplyWeight += self.p['incomeCareFactor']*max(house.totalPotentialIncome-house.povertyLineIncome, 0.0)/cost
                                    probIndex = careWeight/np.power(supplyWeight, self.p['supplyWeightExp'])
                                    needSlot = CareSlot(house, i, hour, False, careWeight, probIndex, cost, [person], slotSuppliers)
                                    house.careSlots.append(needSlot)
                                
                            if person.fixedNeedSchedule[2][0] == 1:
                                hour = 10
                                slotSuppliers = self.getPersonSuppliers(person, i, hour, kd)
                                if len(slotSuppliers) > 0 and person.privateSocialCareNeed > 0:
                                    careWeight = np.exp(self.p['socialCareBeta']*np.power(person.privateSocialCareNeed, self.p['careDeltaExp']))
                                    cost = self.p['priceSocialCare']
                                    supplyWeight = sum([x.residualWeeklySupplies[kd] for x in slotSuppliers])
                                    supplyWeight += self.p['incomeCareFactor']*max(house.totalPotentialIncome-house.povertyLineIncome, 0.0)/cost
                                    probIndex = careWeight/np.power(supplyWeight, self.p['supplyWeightExp'])
                                    needSlot = CareSlot(house, i, hour, False, careWeight, probIndex, cost, [person], slotSuppliers)
                                    house.careSlots.append(needSlot)
                                
                            if person.fixedNeedSchedule[2][1] == 1:
                                hour = 11
                                slotSuppliers = self.getPersonSuppliers(person, i, hour, kd)
                                if len(slotSuppliers) > 0 and person.privateSocialCareNeed > 0:
                                    careWeight = np.exp(self.p['socialCareBeta']*np.power(person.privateSocialCareNeed, self.p['careDeltaExp']))
                                    cost = self.p['priceSocialCare']
                                    supplyWeight = sum([x.residualWeeklySupplies[kd] for x in slotSuppliers])
                                    supplyWeight += self.p['incomeCareFactor']*max(house.totalPotentialIncome-house.povertyLineIncome, 0.0)/cost
                                    probIndex = careWeight/np.power(supplyWeight, self.p['supplyWeightExp'])
                                    needSlot = CareSlot(house, i, hour, False, careWeight, probIndex, cost, [person], slotSuppliers)
                                    house.careSlots.append(needSlot)
                                
                            if person.fixedNeedSchedule[3][0] == 1:
                                hour = 13
                                slotSuppliers = self.getPersonSuppliers(person, i, hour, kd)
                                if len(slotSuppliers) > 0 and person.privateSocialCareNeed > 0:
                                    careWeight = np.exp(self.p['socialCareBeta']*np.power(person.privateSocialCareNeed, self.p['careDeltaExp']))
                                    cost = self.p['priceSocialCare']
                                    supplyWeight = sum([x.residualWeeklySupplies[kd] for x in slotSuppliers])
                                    supplyWeight += self.p['incomeCareFactor']*max(house.totalPotentialIncome-house.povertyLineIncome, 0.0)/cost
                                    probIndex = careWeight/np.power(supplyWeight, self.p['supplyWeightExp'])
                                    needSlot = CareSlot(house, i, hour, False, careWeight, probIndex, cost, [person], slotSuppliers)
                                    house.careSlots.append(needSlot)
                                
                            if person.fixedNeedSchedule[3][1] == 1:
                                hour = 14
                                slotSuppliers = self.getPersonSuppliers(person, i, hour, kd)
                                if len(slotSuppliers) > 0 and person.privateSocialCareNeed > 0:
                                    careWeight = np.exp(self.p['socialCareBeta']*np.power(person.privateSocialCareNeed, self.p['careDeltaExp']))
                                    cost = self.p['priceSocialCare']
                                    supplyWeight = sum([x.residualWeeklySupplies[kd] for x in slotSuppliers])
                                    supplyWeight += self.p['incomeCareFactor']*max(house.totalPotentialIncome-house.povertyLineIncome, 0.0)/cost
                                    probIndex = careWeight/np.power(supplyWeight, self.p['supplyWeightExp'])
                                    needSlot = CareSlot(house, i, hour, False, careWeight, probIndex, cost, [person], slotSuppliers)
                                    house.careSlots.append(needSlot)
                                    
                            for j in range(person.weelyFlexibleNeeds[i]):
                                slotSuppliers = self.getPersonSuppliers(person, i, -1, kd)
                                if len(slotSuppliers) > 0 and person.privateSocialCareNeed > 0:
                                    careWeight = np.exp(self.p['socialCareBeta']*np.power(person.privateSocialCareNeed, self.p['careDeltaExp']))
                                    cost = self.p['priceSocialCare']
                                    supplyWeight = sum([x.residualWeeklySupplies[kd] for x in slotSuppliers])
                                    supplyWeight += self.p['incomeCareFactor']*max(house.totalPotentialIncome-house.povertyLineIncome, 0.0)/cost
                                    probIndex = careWeight/np.power(supplyWeight, self.p['supplyWeightExp'])
                                    needSlot = CareSlot(house, i, -1, False, careWeight, probIndex, cost, [person], slotSuppliers)
                                    house.careSlots.append(needSlot)
                
                    houseSlotsIds = [x.id for x in house.careSlots]
                    prioritySlotsIds = [x.id for x in house.priorityCareSlots]
                    for slotid in prioritySlotsIds:
                        if slotid not in houseSlotsIds:
                            print 'House id: ' + str(house.id)
                            print 'Careslots IDs: ' + str(houseSlotsIds)
                            print 'Priority slots id: ' + str(prioritySlotsIds)
                            print 'Error: slot id do not match (0)!'
                            sys.exit()
                ## housesWCN = [x for x in self.map.occupiedHouses if len(x.careSlots) > 0]
                
                housesPCS = [x for x in self.map.occupiedHouses if len(x.priorityCareSlots) > 0 and x.totalPriorityCareNeed > 0]
                
                housesWithZeroSuppliersSlots = []
                housesWithEmptySlots = []
                for household in housesPCS:
                    
                    houseSlotsIds = [x.id for x in household.careSlots]
                    prioritySlotsIds = [x.id for x in household.priorityCareSlots]
                    for slotid in prioritySlotsIds:
                        if slotid not in houseSlotsIds:
                            housesWithEmptySlots.append(household)
                    noSuppliersSlots = [x for x in household.careSlots if len(x.suppliers) == 0]
                    if len(noSuppliersSlots) > 0:
                        housesWithZeroSuppliersSlots.append(household)
                        
                if len(housesWithEmptySlots) > 0:
                    print 'Error after provision: households in list with empty slots'
                    print 'Receiving house: ' + str(house.id)
                    for house in housesWithEmptySlots:
                        houseSlotsIds = [x.id for x in household.careSlots]
                        prioritySlotsIds = [x.id for x in household.priorityCareSlots]
                        print 'House id: ' + str(house.id)
                        print 'Careslots IDs: ' + str(houseSlotsIds)
                        print 'Priority slots id: ' + str(prioritySlotsIds)
                        print 'Error: slot id do not match (0)!'
                    sys.exit()
                
                # Debugging code
                if len(housesWithZeroSuppliersSlots) > 0:
                    print 'Error before provision'
                    for house in housesWithZeroSuppliersSlots:
                        print 'Slots with no suppliers: ' + str(len(noSuppliersSlots))
                        print 'No-suppliers slots id: ' + str([x.id for x in noSuppliersSlots])
                        priorityCareSlotsZeroSuppliers = [x for x in house.priorityCareSlots if len(slot.suppliers) == 0]
                        print 'No-suppliers priority slots id: ' + str([x.id for x in priorityCareSlotsZeroSuppliers])
                        print 'House with slot with no suppliers: ' + str(house.id)
                        
                    sys.exit()
                
                
                
                start = time.time()
                
                while len(housesPCS) > 0:
                    weightHouses = [float(x.totalPriorityCareNeed) for x in housesPCS]
                    probs = [x/sum(weightHouses) for x in weightHouses]
                    house = np.random.choice(housesPCS, p = probs)
                    
                    # Debugging code
                    houseSlotsIds = [x.id for x in house.careSlots]
                    prioritySlotsIds = [x.id for x in house.priorityCareSlots]
                    for slotid in prioritySlotsIds:
                        if slotid not in houseSlotsIds:
                            print 'House id: ' + str(house.id)
                            print 'Careslots IDs: ' + str(houseSlotsIds)
                            print 'Priority slots id: ' + str(prioritySlotsIds)
                            print 'Error: slot id do not match (1)!'
                            sys.exit()
                    
                    # 1 - A care slot is randomly sampled
                    weights = [float(x.probIndex) for x in house.priorityCareSlots]
                    probs = [x/sum(weights) for x in weights]
                    careSlot = np.random.choice(house.priorityCareSlots, p = probs)
                    # 2 - A supplier is sampled based on residual daily (or weekly, for flexible care) supply
                    weightSuppliers = [float(x.residualDailySupplies[careSlot.day]) for x in careSlot.suppliers]
                    if sum(weightSuppliers) == 0:
                        print [x.residualDailySupplies[careSlot.day] for x in careSlot.suppliers]
                    probs = [x/sum(weightSuppliers) for x in weightSuppliers]
                    supplier = np.random.choice(careSlot.suppliers, p = probs)
                    # 3 - All the time need and time records are updated
                    supplier.weeklyTime[careSlot.day][careSlot.hour] = 0
                    house.childrenCareNeedSchedule[careSlot.day][careSlot.hour] = 0
                    house.householdInformalSupplySchedule[careSlot.day][careSlot.hour] -= 1
                    house.childrenInNeedByHour[careSlot.day][careSlot.hour] = []
                    house.shiftTable[careSlot.day][careSlot.hour] = supplier
                    for d in range(4):
                        supplier.residualWeeklySupplies[d] -= 1
                        house.householdInformalSupplies[d] -= 1
                    supplier.residualWeeklySupplies = [max(x, 0) for x in supplier.residualWeeklySupplies]
                    house.householdInformalSupplies = [max(x, 0) for x in house.householdInformalSupplies]
                    supplier.residualDailySupplies[careSlot.day] = max(supplier.residualDailySupplies[careSlot.day]-1, 0)
                    for i in range(len(supplier.residualDailySupplies)):
                        if supplier.residualWeeklySupplies[kd] < supplier.residualDailySupplies[i]:
                            supplier.residualDailySupplies[i] = supplier.residualWeeklySupplies[kd]
                    for agent in careSlot.receivers:
                        agent.unmetWeeklyNeeds[careSlot.day][careSlot.hour] = 0
                        agent.unmetChildCareNeed = max(agent.unmetChildCareNeed-1, 0)
                        agent.totalChildCareNeed = max(agent.totalChildCareNeed-1, 0)
                        agent.informalChildCareReceived += 1
                        self.externalChildCare += 1
                        # house.totalChildCareNeed -= 1
                        house.totalUnmetChildCareNeed -= 1
                        if careSlot.day < 5 and careSlot.hour < 10:
                            agent.privateChildCareNeed_WNH = max(agent.privateChildCareNeed_WNH-1, 0)
                            house.privateChildCareNeed_WNH -= 1
                            house.totalChilcareNeed_WNH -= 1
                        else:
                            house.totalChilcareNeed_ONH -= 1
                            agent.privateChildCareNeed_ONH = max(agent.privateChildCareNeed_ONH-1, 0)
                            house.privateChildCareNeed_ONH -= 1
                    
                    # 4 - The pool of 'active' care slots is updated
                    if len([x for x in house.careSlots if x.id == careSlot.id]) == 0:
                        print 'Careslot id: ' + str(careSlot.id)
                        print 'House care slots ids: ' + str([x.id for x in house.careSlots])
                        print 'Priority slots id: ' + str(prioritySlotsIds)
                        sys.exit()
                    
                    
                    house.careSlots.remove([x for x in house.careSlots if x.id == careSlot.id][0])
                    house.totalChildCareNeed = sum([(x.privateChildCareNeed_WNH+x.privateChildCareNeed_ONH) for x in house.childCareRecipients])
                    house.totalSocialCareNeed = sum([x.privateSocialCareNeed for x in house.socialCareRecipients])
                    house.totalCareNeed = house.totalChildCareNeed+house.totalSocialCareNeed
                    priorityChildren = [x for x in house.childCareRecipients if x.age < self.p['priorityAgeThreshold']]
                    house.totalPriorityCareNeed = sum([(x.privateChildCareNeed_WNH+x.privateChildCareNeed_ONH) for x in priorityChildren])
                    # Update slots
                    householdsIDs = [x.id for x in supplier.householdsToHelp]
                    
                    for household in supplier.householdsToHelp:
                        
                        notFlexibleSlots = [x for x in household.careSlots if x.hour != -1]
                        flexibleSlots = [x for x in household.careSlots if x.hour == -1]
                        household.careSlots = [x for x in notFlexibleSlots if len([y for y in x.suppliers if y.residualDailySupplies[x.day] > 0]) > 0]
                        household.careSlots += [x for x in flexibleSlots if len([y for y in x.suppliers if y.residualDailySupplies[x.day] > 0 and sum(y.weeklyTime[x.day][:10]) > 0]) > 0]
                        for slot in household.careSlots:
                            if slot.hour == -1:
                                slot.suppliers = [x for x in slot.suppliers if x.residualWeeklySupplies[d] > 0]
                            else:
                                slot.suppliers = [x for x in slot.suppliers if x.weeklyTime[slot.day][slot.hour] == 1 and x.residualDailySupplies[slot.day] > 0 and x.residualWeeklySupplies[d] > 0]
                            # Update the prob index if remaining slots
                            if len(slot.suppliers) > 0:
                                if slot.childCare == True:
                                    if slot.day < 5 and slot.hour < 10:
                                        careWeight = sum([np.exp(self.p['ageCareBeta']*np.power(x.privateChildCareNeed_WNH, self.p['ageDeltaExp'])) for x in slot.receivers])
                                    else:
                                        careWeight = sum([np.exp(self.p['ageCareBeta']*np.power(x.privateChildCareNeed_ONH, self.p['ageDeltaExp'])) for x in slot.receivers])
                                    slot.careWeight = careWeight
                                    supplyWeight = sum([x.residualWeeklySupplies[kd] for x in slot.suppliers])
                                    if slot.day < 5 and slot.hour < 10: # In this case, childcare can be bought
                                        supplyWeight += self.p['incomeCareFactor']*max(household.totalPotentialIncome-household.povertyLineIncome, 0.0)/slot.cost
                                    slot.probIndex = slot.careWeight/np.power(supplyWeight, self.p['supplyWeightExp'])
                                else:
                                    slot.careWeight = np.exp(self.p['socialCareBeta']*np.power(slot.receivers[0].privateSocialCareNeed, self.p['careDeltaExp']))
                                    supplyWeight = sum([x.residualWeeklySupplies[kd] for x in slot.suppliers])
                                    supplyWeight += self.p['incomeCareFactor']*max(household.totalPotentialIncome-household.povertyLineIncome, 0.0)/slot.cost
                                    slot.probIndex = slot.careWeight/np.power(supplyWeight, self.p['supplyWeightExp'])
                        household.careSlots = [x for x in household.careSlots if len(x.suppliers) > 0]
                        slots_WNH = [x for x in household.careSlots if x.childCare == True and x.day < 5 and x.hour < 10]
                        slots_ONH = [x for x in household.careSlots if x.childCare == True and x not in slots_WNH]
                        socialSlots = [x for x in household.careSlots if x.childCare == False]
                        household.careSlots = [x for x in slots_WNH if sum([y.privateChildCareNeed_WNH for y in x.receivers])> 0] + [x for x in slots_ONH if sum([y.privateChildCareNeed_ONH for y in x.receivers]) > 0]
                        household.careSlots += [x for x in socialSlots if sum([y.privateSocialCareNeed for y in x.receivers])> 0]
                        household.priorityCareSlots = [x for x in household.careSlots if x.childCare == True and x.minAge < self.p['priorityAgeThreshold']]
                        
                        # Debugging code
                        houseSlotsIds = [x.id for x in household.careSlots]
                        prioritySlotsIds = [x.id for x in household.priorityCareSlots]
                        for slotid in prioritySlotsIds:
                            if slotid not in houseSlotsIds:
                                print 'House id: ' + str(household.id)
                                print 'House related: ' + str(householdsIDs)
                                print 'Careslots IDs: ' + str(houseSlotsIds)
                                print 'Priority slots id: ' + str(prioritySlotsIds)
                                print 'Error: slot id do not match (2)!'
                                sys.exit()
                        
                    # Update list of households with priority careslots
                    
                    housesPCS = [x for x in self.map.occupiedHouses if len(x.priorityCareSlots) > 0 and x.totalPriorityCareNeed > 0]
                    
                    housesWithZeroSuppliersSlots = []
                    housesWithEmptySlots = []
                    for household in housesPCS:
                        
                        houseSlotsIds = [x.id for x in household.careSlots]
                        prioritySlotsIds = [x.id for x in household.priorityCareSlots]
                        for slotid in prioritySlotsIds:
                            if slotid not in houseSlotsIds:
                                housesWithEmptySlots.append(household)
                        noSuppliersSlots = [x for x in household.careSlots if len(x.suppliers) == 0]
                        if len(noSuppliersSlots) > 0:
                            housesWithZeroSuppliersSlots.append(household)
                            
                    if len(housesWithEmptySlots) > 0:
                        print 'Error after provision: households in list with empty slots'
                        print 'Receiving house: ' + str(house.id)
                        for house in housesWithEmptySlots:
                            houseSlotsIds = [x.id for x in household.careSlots]
                            prioritySlotsIds = [x.id for x in household.priorityCareSlots]
                            print 'House id: ' + str(house.id)
                            print 'House related: ' + str(householdsIDs)
                            print 'Careslots IDs: ' + str(houseSlotsIds)
                            print 'Priority slots id: ' + str(prioritySlotsIds)
                            print 'Error: slot id do not match (3)!'
                        sys.exit()
                        
                    if len(housesWithZeroSuppliersSlots) > 0:
                        print 'Error after provision'
                        print 'Receiving house: ' + str(house.id)
                        for house in housesWithZeroSuppliersSlots:
                            print 'Slots with no suppliers: ' + str(len(noSuppliersSlots))
                            print 'No-suppliers slots id: ' + str([x.id for x in noSuppliersSlots])
                            priorityCareSlotsZeroSuppliers = [x for x in house.priorityCareSlots if len(slot.suppliers) == 0]
                            print 'No-suppliers priority slots id: ' + str([x.id for x in priorityCareSlotsZeroSuppliers])
                            print 'Houses affected by previous provision: ' + str(householdsIDs)
                            print 'House with slot with no suppliers: ' + str(house.id)
                            if house.id in householdsIDs:
                                print 'House is in households affected'
                            else:
                                print 'House is NOT in households affected'
                            
                        sys.exit()
                    
                        
                    
                end = time.time()
                CareProvision4_extim += (end - start)
            
            for d in range(2):
                kd = d+1
                for house in self.map.occupiedHouses:
                    house.careSlots[:] = []
                # Start loopd with extranl informal care
                # housesWSCCN = [x for x in self.map.occupiedHouses if house.totalCareNeed > 0]
                for house in self.map.occupiedHouses:
                    for i in range(7):
                        for j in range(24):
                            if house.childrenCareNeedSchedule[i][j] > 0:
                                # The suppliers here are all the members of the households at kinship distance 1
                                slotSuppliers = self.getHouseSuppliers(house, i, j, kd)
                                if len(slotSuppliers) > 0:
                                    slotChildren = [x for x in house.childrenInNeedByHour[i][j]]
                                    if i > 4 or (i < 5 and j > 9):
                                        if sum([x.privateChildCareNeed_ONH for x in slotChildren]) > 0:
                                            careWeight = sum([np.exp(self.p['ageCareBeta']*np.power(x.privateChildCareNeed_ONH, self.p['ageDeltaExp'])) for x in slotChildren])
                                            cost = 0
                                            supplyWeight = sum([x.residualWeeklySupplies[kd] for x in slotSuppliers])
                                            if np.power(supplyWeight, self.p['supplyWeightExp']) > 0:
                                                probIndex = careWeight/np.power(supplyWeight, self.p['supplyWeightExp'])
                                            else:
                                                probIndex = 0
                                            needSlot = CareSlot(house, i, j, True, careWeight, probIndex, cost, slotChildren, slotSuppliers)
                                            needSlot.minAge = min([x.age for x in slotChildren if x.privateChildCareNeed_ONH > 0])
                                            house.careSlots.append(needSlot)
                                    else:
                                        if sum([x.privateChildCareNeed_WNH for x in slotChildren]) > 0:
                                            careWeight = sum([np.exp(self.p['ageCareBeta']*np.power(x.privateChildCareNeed_WNH, self.p['ageDeltaExp'])) for x in slotChildren])
                                            cost = self.p['priceChildCare']*sum([x.privateChildCareNeed_WNH for x in slotChildren])
                                            supplyWeight = sum([x.residualWeeklySupplies[kd] for x in slotSuppliers])
                                            supplyWeight += self.p['incomeCareFactor']*max(house.totalPotentialIncome-house.povertyLineIncome, 0.0)/cost
                                            if np.power(supplyWeight, self.p['supplyWeightExp']) > 0:
                                                probIndex = careWeight/np.power(supplyWeight, self.p['supplyWeightExp'])
                                            else:
                                                probIndex = 0
                                            needSlot = CareSlot(house, i, j, True, careWeight, probIndex, cost, slotChildren, slotSuppliers)
                                            needSlot.minAge = min([x.age for x in slotChildren if x.privateChildCareNeed_WNH > 0])
                                            house.careSlots.append(needSlot)
                                        
                    socialCareReceivers = [x for x in house.occupants if x.privateSocialCareNeed > 0]
                    for person in socialCareReceivers:
                        # These agents have a number of fixed hours (associated to day and hour)
                        # and a number of flexible hours.
                        for i in range(7):
                            if person.fixedNeedSchedule[0][0] == 1:
                                hour = 0
                                slotSuppliers = self.getPersonSuppliers(person, i, hour, kd)
                                if len(slotSuppliers) > 0 and person.privateSocialCareNeed > 0:
                                    careWeight = np.exp(self.p['socialCareBeta']*np.power(person.privateSocialCareNeed, self.p['careDeltaExp']))
                                    cost = self.p['priceSocialCare']
                                    supplyWeight = sum([x.residualWeeklySupplies[kd] for x in slotSuppliers])
                                    supplyWeight += self.p['incomeCareFactor']*max(house.totalPotentialIncome-house.povertyLineIncome, 0.0)/cost
                                    probIndex = careWeight/np.power(supplyWeight, self.p['supplyWeightExp'])
                                    needSlot = CareSlot(house, i, hour, False, careWeight, probIndex, cost, [person], slotSuppliers)
                                    house.careSlots.append(needSlot)
                                
                            if person.fixedNeedSchedule[0][1] == 1:
                                hour = 1
                                slotSuppliers = self.getPersonSuppliers(person, i, hour, kd)
                                if len(slotSuppliers) > 0 and person.privateSocialCareNeed > 0:
                                    careWeight = np.exp(self.p['socialCareBeta']*np.power(person.privateSocialCareNeed, self.p['careDeltaExp']))
                                    cost = self.p['priceSocialCare']
                                    supplyWeight = sum([x.residualWeeklySupplies[kd] for x in slotSuppliers])
                                    supplyWeight += self.p['incomeCareFactor']*max(house.totalPotentialIncome-house.povertyLineIncome, 0.0)/cost
                                    probIndex = careWeight/np.power(supplyWeight, self.p['supplyWeightExp'])
                                    needSlot = CareSlot(house, i, hour, False, careWeight, probIndex, cost, [person], slotSuppliers)
                                    house.careSlots.append(needSlot)
                                
                            if person.fixedNeedSchedule[1][0] == 1:
                                hour = 4
                                slotSuppliers = self.getPersonSuppliers(person, i, hour, kd)
                                if len(slotSuppliers) > 0 and person.privateSocialCareNeed > 0:
                                    careWeight = np.exp(self.p['socialCareBeta']*np.power(person.privateSocialCareNeed, self.p['careDeltaExp']))
                                    cost = self.p['priceSocialCare']
                                    supplyWeight = sum([x.residualWeeklySupplies[kd] for x in slotSuppliers])
                                    supplyWeight += self.p['incomeCareFactor']*max(house.totalPotentialIncome-house.povertyLineIncome, 0.0)/cost    
                                    probIndex = careWeight/np.power(supplyWeight, self.p['supplyWeightExp'])
                                    needSlot = CareSlot(house, i, hour, False, careWeight, probIndex, cost, [person], slotSuppliers)
                                    house.careSlots.append(needSlot)
                                
                            if person.fixedNeedSchedule[1][1] == 1:
                                hour = 5
                                slotSuppliers = self.getPersonSuppliers(person, i, hour, kd)
                                if len(slotSuppliers) > 0 and person.privateSocialCareNeed > 0:
                                    careWeight = np.exp(self.p['socialCareBeta']*np.power(person.privateSocialCareNeed, self.p['careDeltaExp']))
                                    cost = self.p['priceSocialCare']
                                    supplyWeight = sum([x.residualWeeklySupplies[kd] for x in slotSuppliers])
                                    supplyWeight += self.p['incomeCareFactor']*max(house.totalPotentialIncome-house.povertyLineIncome, 0.0)/cost
                                    probIndex = careWeight/np.power(supplyWeight, self.p['supplyWeightExp'])
                                    needSlot = CareSlot(house, i, hour, False, careWeight, probIndex, cost, [person], slotSuppliers)
                                    house.careSlots.append(needSlot)
                                
                            if person.fixedNeedSchedule[2][0] == 1:
                                hour = 10
                                slotSuppliers = self.getPersonSuppliers(person, i, hour, kd)
                                if len(slotSuppliers) > 0 and person.privateSocialCareNeed > 0:
                                    careWeight = np.exp(self.p['socialCareBeta']*np.power(person.privateSocialCareNeed, self.p['careDeltaExp']))
                                    cost = self.p['priceSocialCare']
                                    supplyWeight = sum([x.residualWeeklySupplies[kd] for x in slotSuppliers])
                                    supplyWeight += self.p['incomeCareFactor']*max(house.totalPotentialIncome-house.povertyLineIncome, 0.0)/cost
                                    probIndex = careWeight/np.power(supplyWeight, self.p['supplyWeightExp'])
                                    needSlot = CareSlot(house, i, hour, False, careWeight, probIndex, cost, [person], slotSuppliers)
                                    house.careSlots.append(needSlot)
                                
                            if person.fixedNeedSchedule[2][1] == 1:
                                hour = 11
                                slotSuppliers = self.getPersonSuppliers(person, i, hour, kd)
                                if len(slotSuppliers) > 0 and person.privateSocialCareNeed > 0:
                                    careWeight = np.exp(self.p['socialCareBeta']*np.power(person.privateSocialCareNeed, self.p['careDeltaExp']))
                                    cost = self.p['priceSocialCare']
                                    supplyWeight = sum([x.residualWeeklySupplies[kd] for x in slotSuppliers])
                                    supplyWeight += self.p['incomeCareFactor']*max(house.totalPotentialIncome-house.povertyLineIncome, 0.0)/cost
                                    probIndex = careWeight/np.power(supplyWeight, self.p['supplyWeightExp'])
                                    needSlot = CareSlot(house, i, hour, False, careWeight, probIndex, cost, [person], slotSuppliers)
                                    house.careSlots.append(needSlot)
                                
                            if person.fixedNeedSchedule[3][0] == 1:
                                hour = 13
                                slotSuppliers = self.getPersonSuppliers(person, i, hour, kd)
                                if len(slotSuppliers) > 0 and person.privateSocialCareNeed > 0:
                                    careWeight = np.exp(self.p['socialCareBeta']*np.power(person.privateSocialCareNeed, self.p['careDeltaExp']))
                                    cost = self.p['priceSocialCare']
                                    supplyWeight = sum([x.residualWeeklySupplies[kd] for x in slotSuppliers])
                                    supplyWeight += self.p['incomeCareFactor']*max(house.totalPotentialIncome-house.povertyLineIncome, 0.0)/cost
                                    probIndex = careWeight/np.power(supplyWeight, self.p['supplyWeightExp'])
                                    needSlot = CareSlot(house, i, hour, False, careWeight, probIndex, cost, [person], slotSuppliers)
                                    house.careSlots.append(needSlot)
                                
                            if person.fixedNeedSchedule[3][1] == 1:
                                hour = 14
                                slotSuppliers = self.getPersonSuppliers(person, i, hour, kd)
                                if len(slotSuppliers) > 0 and person.privateSocialCareNeed > 0:
                                    careWeight = np.exp(self.p['socialCareBeta']*np.power(person.privateSocialCareNeed, self.p['careDeltaExp']))
                                    cost = self.p['priceSocialCare']
                                    supplyWeight = sum([x.residualWeeklySupplies[kd] for x in slotSuppliers])
                                    supplyWeight += self.p['incomeCareFactor']*max(house.totalPotentialIncome-house.povertyLineIncome, 0.0)/cost
                                    probIndex = careWeight/np.power(supplyWeight, self.p['supplyWeightExp'])
                                    needSlot = CareSlot(house, i, hour, False, careWeight, probIndex, cost, [person], slotSuppliers)
                                    house.careSlots.append(needSlot)
                                    
                            for j in range(person.weelyFlexibleNeeds[i]):
                                slotSuppliers = self.getPersonSuppliers(person, i, -1, kd)
                                if len(slotSuppliers) > 0 and person.privateSocialCareNeed > 0:
                                    careWeight = np.exp(self.p['socialCareBeta']*np.power(person.privateSocialCareNeed, self.p['careDeltaExp']))
                                    cost = self.p['priceSocialCare']
                                    supplyWeight = sum([x.residualWeeklySupplies[kd] for x in slotSuppliers])
                                    supplyWeight += self.p['incomeCareFactor']*max(house.totalPotentialIncome-house.povertyLineIncome, 0.0)/cost
                                    probIndex = careWeight/np.power(supplyWeight, self.p['supplyWeightExp'])
                                    needSlot = CareSlot(house, i, -1, False, careWeight, probIndex, cost, [person], slotSuppliers)
                                    house.careSlots.append(needSlot)
                
                start = time.time()
                
                housesWCN = [x for x in self.map.occupiedHouses if len(x.careSlots) > 0]
                
                
                housesWithZeroSuppliersSlots = []
                for household in housesWCN:
                    noSuppliersSlots = [x for x in household.careSlots if len(x.suppliers) == 0]
                    if len(noSuppliersSlots) > 0:
                        housesWithZeroSuppliersSlots.append(household)
                if len(housesWithZeroSuppliersSlots) > 0:
                    print 'Error before provision (2)'
                    for house in housesWithZeroSuppliersSlots:
                        print 'Slots with no suppliers: ' + str(len(noSuppliersSlots))
                        print 'No-suppliers slots id: ' + str([x.id for x in noSuppliersSlots])
                        print 'House with slot with no suppliers: ' + str(house.id)
                        
                    sys.exit()
                
                
                while len(housesWCN) > 0:
                    # 1 - Sample an house based on total care need
                    weightHouses = [float(x.totalCareNeed) for x in housesWCN]
                    probs = [x/sum(weightHouses) for x in weightHouses]
                    house = np.random.choice(housesWCN, p = probs)
                    # 2 - Sample a slot based on the slots' probIndex (weights)
                    weightSlots = [float(x.probIndex) for x in house.careSlots]
                    probs = [x/sum(weightSlots) for x in weightSlots]
                    careSlot = np.random.choice(house.careSlots, p = probs)
                    # 3 - Sample a supplier for the sampled slot, based on residual daily supplies
                    weightSuppliers = [float(x.residualDailySupplies[careSlot.day]) for x in careSlot.suppliers]
                    
                    if weightSuppliers == 0:
                        print 'Error: probs less than 1!'
                        print 'Weight suppliers: ' + str(weightSuppliers)
                        print 'Probs: ' + str(probs)
                        sys.exit()
                    
                    
                    probs = [x/sum(weightSuppliers) for x in weightSuppliers]
                    
                    
                        
                    supplier = np.random.choice(careSlot.suppliers, p = probs)
                    # 4 - The hour of care is provided by the supplier to the receiver in the sampled house: update care scores
                    supplier.weeklyTime[careSlot.day][careSlot.hour] = 0
                    house.householdInformalSupplySchedule[careSlot.day][careSlot.hour] -= 1
                    house.childrenInNeedByHour[careSlot.day][careSlot.hour] = []
                    house.shiftTable[careSlot.day][careSlot.hour] = supplier
                    for d in range(4):
                        supplier.residualWeeklySupplies[d] -= 1
                        house.householdInformalSupplies[d] -= 1
                    supplier.residualWeeklySupplies = [max(x, 0) for x in supplier.residualWeeklySupplies]
                    house.householdInformalSupplies = [max(x, 0) for x in house.householdInformalSupplies]
                    supplier.residualDailySupplies[careSlot.day] = max(supplier.residualDailySupplies[careSlot.day]-1, 0)
                    for i in range(len(supplier.residualDailySupplies)):
                        if supplier.residualWeeklySupplies[kd] < supplier.residualDailySupplies[i]:
                            supplier.residualDailySupplies[i] = supplier.residualWeeklySupplies[kd]
                    # Update receivers' records
                    if careSlot.childCare == True:
                        house.childrenCareNeedSchedule[careSlot.day][careSlot.hour] = 0
                        for agent in careSlot.receivers:
                            agent.unmetWeeklyNeeds[careSlot.day][careSlot.hour] = 0
                            agent.unmetChildCareNeed = max(agent.unmetChildCareNeed-1, 0)
                            agent.totalChildCareNeed = max(agent.totalChildCareNeed-1, 0)
                            agent.informalChildCareReceived += 1
                            self.externalChildCare += 1
                            # house.totalChildCareNeed -= 1
                            house.totalUnmetChildCareNeed -= 1
                            if careSlot.day < 5 and careSlot.hour < 10:
                                agent.privateChildCareNeed_WNH = max(agent.privateChildCareNeed_WNH-1, 0)
                                house.privateChildCareNeed_WNH -= 1
                                house.totalChilcareNeed_WNH -= 1
                            else:
                                house.totalChilcareNeed_ONH -= 1
                                agent.privateChildCareNeed_ONH = max(agent.privateChildCareNeed_ONH-1, 0)
                                house.privateChildCareNeed_ONH -= 1
                    else:
                        supplier.socialWork += 1
                        person = careSlot.receivers[0]
                        person.privateSocialCareNeed = max(person.privateSocialCareNeed-1, 0)
                        person.unmetSocialCareNeed = max(person.unmetSocialCareNeed-1, 0)
                        person.informalSocialCareReceived += 1
                        self.externalSocialCare += 1
                        # house.totalSocialCareNeed -= 1
                        house.totalUnmetSocialCareNeed -= 1
                        if careSlot.hour == -1:
                            person.weelyFlexibleNeeds[careSlot.day] = max(person.weelyFlexibleNeeds[careSlot.day]-1, 0)
                        else:
                            if careSlot.hour == 0:
                                person.fixedNeedSchedule[0][0] = 0
                            elif careSlot.hour == 1:
                                person.fixedNeedSchedule[0][1] = 0
                            elif careSlot.hour == 4:
                                person.fixedNeedSchedule[1][0] = 0
                            elif careSlot.hour == 5:
                                person.fixedNeedSchedule[1][1] = 0
                            elif careSlot.hour == 10:
                                person.fixedNeedSchedule[2][0] = 0
                            elif careSlot.hour == 11:
                                person.fixedNeedSchedule[2][1] = 0
                            elif careSlot.hour == 13:
                                person.fixedNeedSchedule[3][0] = 0
                            elif careSlot.hour == 14:
                                person.fixedNeedSchedule[3][1] = 0
                                
                    house.totalChildCareNeed = sum([(x.privateChildCareNeed_WNH+x.privateChildCareNeed_ONH) for x in house.childCareRecipients])
                    house.totalSocialCareNeed = sum([x.privateSocialCareNeed for x in house.socialCareRecipients])
                    house.totalCareNeed = house.totalChildCareNeed+house.totalSocialCareNeed
                    
                    house.careSlots.remove([x for x in house.careSlots if x.id == careSlot.id][0])
                    
                    for household in supplier.householdsToHelp:
                        
                        notFlexibleSlots = [x for x in household.careSlots if x.hour != -1]
                        flexibleSlots = [x for x in household.careSlots if x.hour == -1]
                        household.careSlots = [x for x in notFlexibleSlots if len([y for y in x.suppliers if y.residualDailySupplies[x.day] > 0]) > 0]
                        household.careSlots += [x for x in flexibleSlots if len([y for y in x.suppliers if y.residualDailySupplies[x.day] > 0 and sum(y.weeklyTime[x.day][:10]) > 0]) > 0]
                        
                        for slot in household.careSlots:
                            if slot.hour == -1:
                                slot.suppliers = [x for x in slot.suppliers if x.residualWeeklySupplies[d] > 0]
                            else:
                                slot.suppliers = [x for x in slot.suppliers if x.weeklyTime[slot.day][slot.hour] == 1 and x.residualDailySupplies[slot.day] > 0 and x.residualWeeklySupplies[d] > 0]
                            # Update the prob index if remaining slots
                            if len(slot.suppliers) > 0:
                                if slot.childCare == True:
                                    if slot.day < 5 and slot.hour < 10:
                                        careWeight = sum([np.exp(self.p['ageCareBeta']*np.power(x.privateChildCareNeed_WNH, self.p['ageDeltaExp'])) for x in slot.receivers])
                                    else:
                                        careWeight = sum([np.exp(self.p['ageCareBeta']*np.power(x.privateChildCareNeed_ONH, self.p['ageDeltaExp'])) for x in slot.receivers])
                                    slot.careWeight = careWeight
                                    supplyWeight = sum([x.residualWeeklySupplies[kd] for x in slot.suppliers])
                                    if slot.day < 5 and slot.hour < 10: # In this case, childcare can be bought
                                        supplyWeight += self.p['incomeCareFactor']*max(house.totalPotentialIncome-house.povertyLineIncome, 0.0)/slot.cost
                                    slot.probIndex = slot.careWeight/np.power(supplyWeight, self.p['supplyWeightExp'])
                                else:
                                    slot.careWeight = np.exp(self.p['socialCareBeta']*np.power(slot.receivers[0].privateSocialCareNeed, self.p['careDeltaExp']))
                                    supplyWeight = sum([x.residualWeeklySupplies[kd] for x in slot.suppliers])
                                    supplyWeight += self.p['incomeCareFactor']*max(house.totalPotentialIncome-house.povertyLineIncome, 0.0)/slot.cost
                                    slot.probIndex = slot.careWeight/np.power(supplyWeight, self.p['supplyWeightExp'])
                        household.careSlots = [x for x in household.careSlots if len(x.suppliers) > 0]
                        slots_WNH = [x for x in household.careSlots if x.childCare == True and x.day < 5 and x.hour < 10]
                        slots_ONH = [x for x in household.careSlots if x.childCare == True and x not in slots_WNH]
                        socialSlots = [x for x in household.careSlots if x.childCare == False]
                        household.careSlots = [x for x in slots_WNH if sum([y.privateChildCareNeed_WNH for y in x.receivers])> 0] + [x for x in slots_ONH if sum([y.privateChildCareNeed_ONH for y in x.receivers]) > 0]
                        household.careSlots += [x for x in socialSlots if sum([y.privateSocialCareNeed for y in x.receivers])> 0]
                        
                        
                    housesWCN = [x for x in self.map.occupiedHouses if len(x.careSlots) > 0]
                    
                    housesWithZeroSuppliersSlots = []
                    for household in housesWCN:
                        noSuppliersSlots = [x for x in household.careSlots if len(x.suppliers) == 0]
                        if len(noSuppliersSlots) > 0:
                            housesWithZeroSuppliersSlots.append(household)
                    if len(housesWithZeroSuppliersSlots) > 0:
                        print 'Error after provision (2)'
                        print 'Receiving house: ' + str(house.id)
                        for house in housesWithZeroSuppliersSlots:
                            print 'Slots with no suppliers: ' + str(len(noSuppliersSlots))
                            print 'No-suppliers slots id: ' + str([x.id for x in noSuppliersSlots])
                            print 'House with slot with no suppliers: ' + str(house.id)
                            
                        sys.exit()
                
                zeroCareNeedHouses = [x for x in housesWCN if x.totalCareNeed <= 0]
                if len(zeroCareNeedHouses) > 0:
                    print 'Error: houses with zero care need and slots!'
                    for house in zeroCareNeedHouses:
                        print 'House id: ' + str(house.id)
                        print house.totalCareNeed
                        print [x.id for x in house.childCareRecipients]
                        print [x.id for x in house.socialCareRecipients]
                        print [x.privateChildCareNeed_WNH for x in house.childCareRecipients]
                        print [x.privateChildCareNeed_ONH for x in house.childCareRecipients]
                        print [x.privateSocialCareNeed for x in house.socialCareRecipients]
                        for slot in house.careSlots:
                            print [x.id for x in slot.receivers]
                            print [x.privateChildCareNeed_WNH for x in slot.receivers]
                            print [x.privateChildCareNeed_ONH for x in slot.receivers]
                            print [x.privateSocialCareNeed for x in slot.receivers]
                        print ''
                    sys.exit()
                    
            end = time.time()
            CareProvision5_extim += (end - start)
        
        # Now, start to allocate income (i.e. formal care of informal care taken from working hours)
        # There are two kinds of income:
        # - income from work
        # - income from welfare
        # If formal care is not possible, only if there are agents with free working hours care of the informal kind can be provided.
        # If formal care is possible:
        # - case A: there are occupied workers.
        #   - a) if lowest wage is lower than cost of social care, the worker takes time off work to provide for informal care
        #   - b) if lowest wage is higher than cost of care, then the household pays for formal care. If there is income
        #        from welfare, this is used, so no worker will need to allocate free working hours.
        #        Otherwise, the highest-wage worker will allocate free working hours to pay for the formal care provided.
        # - case B: there aren't occupied workers. In this case, only formal care is provided.
        
        for house in self.map.occupiedHouses:
            house.costFormalCare = 0
            house.careSlots[:] = []
            house.carriedOverCost = 0
            house.slotWithCareSuppliers_ONH = 0
            house.slotWithCareSuppliers_WNH = 0
            house.numCostGreaterThanWage = 0
            house.numNoSuppliers = 0
            house.numCostSmallerThanWage = 0
            
            # Compute the residual childcare and social care fro each household
            house.residualCareNeed_PreFormal = sum([x.privateChildCareNeed_WNH for x in house.childCareRecipients])
            house.residualCareNeed_PreFormal += sum([x.privateChildCareNeed_ONH for x in house.childCareRecipients])
            house.residualCareNeed_PreFormal += sum([x.privateSocialCareNeed for x in house.socialCareRecipients])
            
            house.unmetChildCareNeed_Pre = sum([x.unmetChildCareNeed for x in house.childCareRecipients])
            house.totalCareNeed_Pre = house.totalCareNeed
            
            house.totalOutOfWorkChildCare_Pre = sum([x.outOfWorkChildCare for x in house.occupants])
            
            
            
        # Start loopd with extranl informal care
        housesWSCCN = [x for x in self.map.occupiedHouses if x.totalCareNeed > 0]
        self.allCareSlots[:] = []
        
        # Check max income for care
        zeroIncomeForCareHouseholds = len([x for x in housesWSCCN if x.totalPotentialIncome-x.povertyLineIncome <= 0])
        shareOfZeroIncomeForCareHouseholds = 0
        if len(housesWSCCN) > 0:
            shareOfZeroIncomeForCareHouseholds = float(zeroIncomeForCareHouseholds)/float(len(housesWSCCN))
        print 'Share of zero income households: ' + str(shareOfZeroIncomeForCareHouseholds)
    
        
        for house in housesWSCCN:
            suppliers = [x for x in house.occupants if x.independentStatus == True]
            maxIncomeForCare = house.totalPotentialIncome-house.povertyLineIncome
            # Each house with outstanding private care need, has to satisfy it by resorting to its income
            # For childcare slots outside the nurseries' opening hours, the parents need to take hours of work to provide for informal care.
            # The childcare slots outside the nurseries' opening hours with children with residual care needs aged below 8, are served first.
            # The other care slots, are divided into high-price and low price, according to whether the cost to satisfy them 
            # is, respectively, higher or lower than the lowest-wage worker with available working hours to allocate to social care.
            # The high-price slots are satisfied by taking hours of work to provide for informal care, whereas
            # the low-price slots are satisfied by buying formal care.
            # Slots are sampled according to their total residual private care.
            # Three caveats:
            # - children below the age of 8 are served first
            # - the process ends either when all the care need has been satisfied or when the household hits the Survival Income limit.
            # - the income needed to satisfy ALL of the household care need is computed for comparison purposes.
            house.onhSlots_Pre = 0
            house.wnhSlots_Pre = 0
            for i in range(7):
                for j in range(24):
                    if house.childrenCareNeedSchedule[i][j] > 0:
                        slotSuppliers_ONH = [x for x in suppliers if x.afterCareJS[i][j] == 1 and x.freeWorkingHours > 0]
                        slotSuppliers_WNH = [x for x in suppliers if x.freeWorkingHours > 0]
                        slotChildren = [x for x in house.childrenInNeedByHour[i][j]]
    #                    totalPrivateNeed = sum([x.privateChildCareNeed_WNH for x in slotChildren])+sum([x.privateChildCareNeed_ONH for x in slotChildren])
    #                    if totalPrivateNeed > 0:
                        if i > 4 or (i < 5 and j > 9):
                            if sum([x.privateChildCareNeed_ONH for x in slotChildren]) > 0 and len(slotSuppliers_ONH) > 0:
                                careWeight = sum([x.privateChildCareNeed_ONH for x in slotChildren])
                                cost = 0
                                probIndex = careWeight
                                needSlot = CareSlot(house, i, j, True, careWeight, probIndex, cost, slotChildren, slotSuppliers_ONH)
                                needSlot.minAge = min([x.age for x in slotChildren if x.privateChildCareNeed_ONH > 0])
                                house.careSlots.append(needSlot)
                                house.onhSlots_Pre += 1
                        else:
                            if sum([x.privateChildCareNeed_WNH for x in slotChildren]) > 0 and len(slotSuppliers_WNH) > 0:
                                careWeight = sum([x.privateChildCareNeed_WNH for x in slotChildren])
                                cost = self.p['priceChildCare']*careWeight
                                probIndex = careWeight
                                needSlot = CareSlot(house, i, j, True, careWeight, probIndex, cost, slotChildren, slotSuppliers_WNH)
                                needSlot.minAge = min([x.age for x in slotChildren if x.privateChildCareNeed_WNH > 0])
                                house.careSlots.append(needSlot)
                                house.wnhSlots_Pre += 1
            
            house.totalChildCareSlots_Pre = len(house.careSlots)
            
            socialCareReceivers = [x for x in house.occupants if x.privateSocialCareNeed > 0]
            for person in socialCareReceivers:
                careWeight = person.privateSocialCareNeed
                cost = self.p['priceSocialCare']
                probIndex = careWeight
                # These agents have a number of fixed hours (associated to day and hour)
                # and a number of flexible hours.
                for i in range(7):
                    if person.fixedNeedSchedule[0][0] == 1:
                        hour = 0
                        slotSuppliers = [x for x in suppliers if x.freeWorkingHours > 0]
                        if person.privateSocialCareNeed > 0:
                            needSlot = CareSlot(house, i, hour, False, careWeight, probIndex, cost, [person], slotSuppliers)
                            house.careSlots.append(needSlot)
                        
                    if person.fixedNeedSchedule[0][1] == 1:
                        hour = 1
                        slotSuppliers = [x for x in suppliers if x.freeWorkingHours > 0]
                        if person.privateSocialCareNeed > 0:
                            needSlot = CareSlot(house, i, hour, False, careWeight, probIndex, cost, [person], slotSuppliers)
                            house.careSlots.append(needSlot)
                        
                    if person.fixedNeedSchedule[1][0] == 1:
                        hour = 4
                        slotSuppliers = [x for x in suppliers if x.freeWorkingHours > 0]
                        if person.privateSocialCareNeed > 0:
                            needSlot = CareSlot(house, i, hour, False, careWeight, probIndex, cost, [person], slotSuppliers)
                            house.careSlots.append(needSlot)
                        
                    if person.fixedNeedSchedule[1][1] == 1:
                        hour = 5
                        slotSuppliers = [x for x in suppliers if x.freeWorkingHours > 0]
                        if person.privateSocialCareNeed > 0:
                            needSlot = CareSlot(house, i, hour, False, careWeight, probIndex, cost, [person], slotSuppliers)
                            house.careSlots.append(needSlot)
                        
                    if person.fixedNeedSchedule[2][0] == 1:
                        hour = 10
                        slotSuppliers = [x for x in suppliers if x.freeWorkingHours > 0]
                        if person.privateSocialCareNeed > 0:
                            needSlot = CareSlot(house, i, hour, False, careWeight, probIndex, cost, [person], slotSuppliers)
                            house.careSlots.append(needSlot)
                        
                    if person.fixedNeedSchedule[2][1] == 1:
                        hour = 11
                        slotSuppliers = [x for x in suppliers if x.freeWorkingHours > 0]
                        if person.privateSocialCareNeed > 0:
                            needSlot = CareSlot(house, i, hour, False, careWeight, probIndex, cost, [person], slotSuppliers)
                            house.careSlots.append(needSlot)
                        
                    if person.fixedNeedSchedule[3][0] == 1:
                        hour = 13
                        slotSuppliers = [x for x in suppliers if x.freeWorkingHours > 0]
                        if person.privateSocialCareNeed > 0:
                            needSlot = CareSlot(house, i, hour, False, careWeight, probIndex, cost, [person], slotSuppliers)
                            house.careSlots.append(needSlot)
                        
                    if person.fixedNeedSchedule[3][1] == 1:
                        hour = 14
                        slotSuppliers = [x for x in suppliers if x.freeWorkingHours > 0]
                        if person.privateSocialCareNeed > 0:
                            needSlot = CareSlot(house, i, hour, False, careWeight, probIndex, cost, [person], slotSuppliers)
                            house.careSlots.append(needSlot)
                            
                    for j in range(person.weelyFlexibleNeeds[i]):
                        slotSuppliers = [x for x in suppliers if x.freeWorkingHours > 0]
                        if person.privateSocialCareNeed > 0:
                            needSlot = CareSlot(house, i, -1, False, careWeight, probIndex, cost, [person], slotSuppliers)
                            house.careSlots.append(needSlot)
                
            ## Now a loop starts for the internal allocation of care
            ## The loop stops when either there is no more residual care need or no more available supply.
            # 1- Select all the care slots with children aged 7 or below
            # Loop to assign informal care and out-of-hours care 
            
            start = time.time()
            
            priorityCareSlots = [x for x in house.careSlots if x.childCare == True and x.minAge < self.p['priorityAgeThreshold']]
            
            house.totalPriorityCareSlots_Pre = len(priorityCareSlots)
            
            while maxIncomeForCare > 0 and len(priorityCareSlots) > 0:
                # 1 - A care slot is randomly sampled
                weights = [float(x.probIndex) for x in priorityCareSlots]
                probs = [x/sum(weights) for x in weights]
                careSlot = np.random.choice(priorityCareSlots, p = probs)
                # If there are workers....
                slotSuppliers = []
                
                # 2 - Check: if slot is ONH or WNH
                if careSlot.day > 4 or (careSlot.day < 5 and careSlot.hour > 9):
                # Sort wage from low to high
                    careSlot.suppliers.sort(key=operator.attrgetter("wage"))
                    careSupplier = careSlot.suppliers[0]
                    house.slotWithCareSuppliers_ONH += 1
                    
                    careSupplier.afterCareJS[careSlot.day][careSlot.hour] = 0
                    house.childrenCareNeedSchedule[careSlot.day][careSlot.hour] = 0
                    house.childrenInNeedByHour[careSlot.day][careSlot.hour] = []
                    careSupplier.outOfWorkChildCare += 1
                    maxIncomeForCare = max(maxIncomeForCare-careSupplier.wage, 0.0)
                    careSupplier.availableWorkingHours -= 1
                    careSupplier.freeWorkingHours -= 1
                    house.shiftTable[careSlot.day][careSlot.hour] = supplier
                    for agent in careSlot.receivers:
                        agent.unmetWeeklyNeeds[careSlot.day][careSlot.hour] = 0
                        agent.unmetChildCareNeed = max(agent.unmetChildCareNeed-1, 0)
                        agent.totalChildCareNeed = max(agent.totalChildCareNeed-1, 0)
                        agent.privateChildCareNeed_ONH = max(agent.privateChildCareNeed_ONH-1, 0)
                        agent.informalChildCareReceived += 1
                        self.internalChildCare += 1
                        house.privateChildCareNeed_ONH -= 1
                        house.totalUnmetChildCareNeed -= 1
                        house.totalChilcareNeed_ONH -= 1
                else:
                    suppliersWithTime = [x for x in careSlot.suppliers if x.afterCareJS[i][j] == 1]
                    if len(suppliersWithTime) > 0:
                        # Sort wage from low to high
                        suppliersWithTime.sort(key=operator.attrgetter("wage"))
                        careSupplier = suppliersWithTime[0]
                    if len(suppliersWithTime) > 0 and careSlot.cost-house.carriedOverCost > careSupplier.wage:
                        
                        house.slotWithCareSuppliers_WNH += 1
                        house.numCostGreaterThanWage += 1
                        
                        careSupplier.afterCareJS[careSlot.day][careSlot.hour] = 0
                        careSupplier.outOfWorkChildCare += 1
                        house.childrenCareNeedSchedule[careSlot.day][careSlot.hour] = 0
                        house.childrenInNeedByHour[careSlot.day][careSlot.hour] = []
                        maxIncomeForCare = max(maxIncomeForCare-careSupplier.wage, 0.0)
                        careSupplier.availableWorkingHours -= 1
                        careSupplier.freeWorkingHours -= 1
                        house.shiftTable[careSlot.day][careSlot.hour] = supplier
                        for agent in careSlot.receivers:
                            agent.unmetWeeklyNeeds[careSlot.day][careSlot.hour] = 0
                            agent.unmetChildCareNeed = max(agent.unmetChildCareNeed-1, 0)
                            agent.totalChildCareNeed = max(agent.totalChildCareNeed-1, 0)
                            agent.privateChildCareNeed_WNH = max(agent.privateChildCareNeed_WNH-1, 0)
                            agent.informalChildCareReceived += 1
                            self.internalChildCare += 1
                            house.privateChildCareNeed_WNH -= 1
                            house.totalUnmetChildCareNeed -= 1
                            house.totalChilcareNeed_WNH -= 1
                    elif len(suppliersWithTime) == 0 or careSlot.cost-house.carriedOverCost < careSupplier.wage:
                        
#                        if len(suppliersWithTime) == 0:
#                            house.numNoSuppliers += 1
#                        if careSlot.cost-house.carriedOverCost < careSupplier.wage:
#                            house.numCostSmallerThanWage += 1
                        
                        
                        additionalCost = max(careSlot.cost-house.carriedOverCost, 0.0)
                        maxIncomeForCare -= additionalCost
                        maxIncomeForCare = max(maxIncomeForCare, 0.0)
                        house.childrenCareNeedSchedule[careSlot.day][careSlot.hour] = 0
                        house.childrenInNeedByHour[careSlot.day][careSlot.hour] = []
                        if house.carriedOverCost > careSlot.cost:
                            house.carriedOverCost -= careSlot.cost
                        else:
                            if house.potentialIncomeFromWelfare < additionalCost:
                                house.potentialIncomeFromWelfare = 0
                                if len(slotSuppliers) > 0:
                                    residualCost = additionalCost - house.potentialIncomeFromWelfare
                                    maxWage = careSlot.suppliers[-1].wage
                                    additionalIncome = np.ceil(residualCost/maxWage)*maxWage
                                    careSlot.suppliers[-1].freeWorkingHours -= int(np.ceil(residualCost/maxWage))
                                    careSlot.suppliers[-1].freeWorkingHours = max(careSlot.suppliers[-1].freeWorkingHours, 0)
                                    house.carriedOverCost = max(additionalIncome-residualCost, 0.0)
                                else:
                                    house.carriedOverCost = 0
                            else:
                                house.potentialIncomeFromWelfare -= additionalCost
                                house.carriedOverCost = 0
                                
                        house.formalChildCare += len([x for x in careSlot.receivers if x.privateChildCareNeed_WNH > 0])                    
                        house.costFormalCare += additionalCost
                        house.costFormalChildCare += additionalCost
                        
                        # Degugging code
#                            if house not in self.householdsWithFormalChildCare and self.periodFormalCare == False:
#                                self.householdsWithFormalChildCare.append(house)
                                    
                        for agent in careSlot.receivers:
                            agent.unmetWeeklyNeeds[careSlot.day][careSlot.hour] = 0
                            agent.unmetChildCareNeed = max(agent.unmetChildCareNeed-1, 0)
                            agent.totalChildCareNeed = max(agent.totalChildCareNeed-1, 0)
                            agent.privateChildCareNeed_WNH = max(agent.privateChildCareNeed_WNH-1, 0)
                            agent.formalChildCareReceived += 1
                            self.internalChildCare += 1
                            house.privateChildCareNeed_WNH -= 1
                            house.totalUnmetChildCareNeed -= 1
                            house.totalChilcareNeed_WNH -= 1
                                
                priorityCareSlots.remove(careSlot)
                house.careSlots.remove(careSlot)
                
                
                slots_WNH = [x for x in house.careSlots if x.day < 5 and x.hour < 10 and len([y for y in x.suppliers if y.afterCareJS[x.day][x.hour] == 1 and y.freeWorkingHours > 0]) > 0]
                slots_ONH = [x for x in house.careSlots if x not in slots_WNH and len([y for y in x.suppliers if y.afterCareJS[x.day][x.hour] == 1 and y.freeWorkingHours > 0]) > 0]
                house.careSlots = [x for x in slots_WNH if sum([y.privateChildCareNeed_WNH for y in x.receivers])> 0] + [x for x in slots_ONH if sum([y.privateChildCareNeed_ONH for y in x.receivers])> 0]
                for slot in house.careSlots:
                    if careSlot.day > 4 or (careSlot.day < 5 and careSlot.hour > 9):
                        slot.suppliers = [x for x in suppliers if x.afterCareJS[slot.day][slot.hour] == 1 and x.freeWorkingHours > 0]
                    else:
                        slot.suppliers = [x for x in suppliers if x.freeWorkingHours > 0]
                house.careSlots = [x for x in house.careSlots if len(x.suppliers) > 0]
                slots_WNH = [x for x in priorityCareSlots if x.day < 5 and x.hour < 10 and len([y for y in x.suppliers if y.afterCareJS[x.day][x.hour] == 1 and y.freeWorkingHours > 0]) > 0]
                slots_ONH = [x for x in priorityCareSlots if x not in slots_WNH and len([y for y in x.suppliers if y.afterCareJS[x.day][x.hour] == 1 and y.freeWorkingHours > 0]) > 0]
                priorityCareSlots = [x for x in slots_WNH if sum([y.privateChildCareNeed_WNH for y in x.receivers])> 0] + [x for x in slots_ONH if sum([y.privateChildCareNeed_ONH for y in x.receivers])> 0]
                for slot in priorityCareSlots:
                    if careSlot.day > 4 or (careSlot.day < 5 and careSlot.hour > 9):
                        slot.suppliers = [x for x in suppliers if x.afterCareJS[slot.day][slot.hour] == 1 and x.freeWorkingHours > 0]
                    else:
                        slot.suppliers = [x for x in suppliers if x.freeWorkingHours > 0]
                priorityCareSlots = [x for x in priorityCareSlots if len(x.suppliers) > 0]
        
            end = time.time()
            CareProvision6_extim += (end - start)
            
            # Update list fo care slots: probability of being served proportional to product between unmet social care and residual income for care
            remainingSlots = []
            for slot in house.careSlots:
                if careSlot.childCare == True:
                    careWeight = sum([x.privateChildCareNeed_WNH+x.privateChildCareNeed_ONH for x in slot.receivers])*maxIncomeForCare
                    if careSlot.day > 4 or (careSlot.day < 5 and careSlot.hour > 9):
                        slot.suppliers = [x for x in suppliers if x.afterCareJS[slot.day][slot.hour] == 1 and x.freeWorkingHours > 0]
                    else:
                        slot.suppliers = [x for x in suppliers if x.freeWorkingHours > 0]
                else:
                    careWeight = sum([x.privateSocialCareNeed  for x in slot.receivers])*maxIncomeForCare
                    slot.suppliers = [x for x in suppliers if x.afterCareJS[slot.day][slot.hour] == 1 and x.freeWorkingHours > 0]
                
                prob = (np.exp(self.p['probIncomeCare']*careWeight)-1.0)/np.exp(self.p['probIncomeCare']*careWeight)
                
                if len(slot.suppliers) > 0 and np.random.random() < prob:
                    remainingSlots.append(slot)
                    
            house.careSlots = [x for x in remainingSlots]
            
            start = time.time()
            # Repeat for all the other social care needs
            while maxIncomeForCare > 0 and len(house.careSlots) > 0:
                # 1 - A care slot is randomly sampled
                weights = [float(x.probIndex) for x in house.careSlots]
                probs = [x/sum(weights) for x in weights]
                careSlot = np.random.choice(house.careSlots, p = probs)
                
                if len(careSlot.suppliers) == 0:
                    print 'Error: care slot has no formal care supplier!'
                    sys.exit()
                
                slotSuppliers = []
                # 2 - Check: if slot is ONH or WNH
                if careSlot.childCare == True:
                    if careSlot.day > 4 or (careSlot.day < 5 and careSlot.hour > 9):
                        careSlot.suppliers.sort(key=operator.attrgetter("wage"))
                        careSupplier = careSlot.suppliers[0]
                        careSupplier.afterCareJS[careSlot.day][careSlot.hour] = 0
                        careSupplier.outOfWorkChildCare += 1
                        careSupplier.availableWorkingHours -= 1
                        careSupplier.freeWorkingHours -= 1
                        house.shiftTable[careSlot.day][careSlot.hour] = supplier
                        maxIncomeForCare = max(maxIncomeForCare-careSupplier.wage, 0.0)
                        house.childrenCareNeedSchedule[careSlot.day][careSlot.hour] = 0
                        house.childrenInNeedByHour[careSlot.day][careSlot.hour] = []
                        for agent in careSlot.receivers:
                            agent.unmetWeeklyNeeds[careSlot.day][careSlot.hour] = 0
                            agent.unmetChildCareNeed = max(agent.unmetChildCareNeed-1, 0)
                            agent.totalChildCareNeed = max(agent.totalChildCareNeed-1, 0)
                            agent.privateChildCareNeed_ONH = max(agent.privateChildCareNeed_ONH-1, 0)
                            agent.informalChildCareReceived += 1
                            self.internalChildCare += 1
                            house.privateChildCareNeed_ONH -= 1
                            house.totalUnmetChildCareNeed -= 1
                            house.totalChilcareNeed_ONH -= 1
                    else:
                        suppliersWithTime = [x for x in careSlot.suppliers if x.afterCareJS[i][j] == 1]
                        if len(suppliersWithTime) > 0:
                            # Sort wage from low to high
                            suppliersWithTime.sort(key=operator.attrgetter("wage"))
                            careSupplier = suppliersWithTime[0]
                        if len(suppliersWithTime) > 0 and careSlot.cost-house.carriedOverCost > careSupplier.wage:
                            careSupplier.afterCareJS[careSlot.day][careSlot.hour] = 0
                            careSupplier.outOfWorkChildCare += 1
                            house.childrenCareNeedSchedule[careSlot.day][careSlot.hour] = 0
                            house.childrenInNeedByHour[careSlot.day][careSlot.hour] = []
                            maxIncomeForCare = max(maxIncomeForCare-careSupplier.wage, 0.0)
                            careSupplier.availableWorkingHours -= 1
                            careSupplier.freeWorkingHours -= 1
                            house.shiftTable[careSlot.day][careSlot.hour] = supplier
                            for agent in careSlot.receivers:
                                agent.unmetWeeklyNeeds[careSlot.day][careSlot.hour] = 0
                                agent.unmetChildCareNeed = max(agent.unmetChildCareNeed-1, 0)
                                agent.totalChildCareNeed = max(agent.totalChildCareNeed-1, 0)
                                agent.privateChildCareNeed_WNH = max(agent.privateChildCareNeed_WNH-1, 0)
                                agent.informalChildCareReceived += 1
                                self.internalChildCare += 1
                                house.privateChildCareNeed_WNH -= 1
                                house.totalUnmetChildCareNeed -= 1
                                house.totalChilcareNeed_WNH -= 1
                        elif len(suppliersWithTime) == 0 or careSlot.cost-house.carriedOverCost < careSupplier.wage:
                            additionalCost = max(careSlot.cost-house.carriedOverCost, 0.0)
                            maxIncomeForCare -= additionalCost
                            maxIncomeForCare = max(maxIncomeForCare, 0.0)
                            house.childrenCareNeedSchedule[careSlot.day][careSlot.hour] = 0
                            house.childrenInNeedByHour[careSlot.day][careSlot.hour] = []
                            if house.carriedOverCost > careSlot.cost:
                                house.carriedOverCost -= careSlot.cost
                            else:
                                if house.potentialIncomeFromWelfare < additionalCost:
                                    house.potentialIncomeFromWelfare = 0
                                    if len(slotSuppliers) > 0:
                                        residualCost = additionalCost - house.potentialIncomeFromWelfare
                                        maxWage = careSlot.suppliers[-1].wage
                                        additionalIncome = np.ceil(residualCost/maxWage)*maxWage
                                        careSlot.suppliers[-1].freeWorkingHours -= int(np.ceil(residualCost/maxWage))
                                        careSlot.suppliers[-1].freeWorkingHours = max(careSlot.suppliers[-1].freeWorkingHours, 0)
                                        house.carriedOverCost = max(additionalIncome-residualCost, 0.0)
                                    else:
                                        house.carriedOverCost = 0
                                else:
                                    house.potentialIncomeFromWelfare -= additionalCost
                                    house.carriedOverCost = 0
                                        
                            house.formalChildCare += len([x for x in careSlot.receivers if x.privateChildCareNeed_WNH > 0])                    
                            house.costFormalCare += additionalCost
                            house.costFormalChildCare += additionalCost
                            
                            # Degugging code
#                                if house not in self.householdsWithFormalChildCare and self.periodFormalCare == False:
#                                    self.householdsWithFormalChildCare.append(house)
                                        
                            for agent in careSlot.receivers:
                                agent.unmetWeeklyNeeds[careSlot.day][careSlot.hour] = 0
                                agent.unmetChildCareNeed = max(agent.unmetChildCareNeed-1, 0)
                                agent.totalChildCareNeed = max(agent.totalChildCareNeed-1, 0)
                                agent.privateChildCareNeed_WNH = max(agent.privateChildCareNeed_WNH-1, 0)
                                agent.formalChildCareReceived += 1
                                self.internalChildCare += 1
                                house.privateChildCareNeed_WNH -= 1
                                house.totalUnmetChildCareNeed -= 1
                                house.totalChilcareNeed_WNH -= 1
                else:
                    # Social care slot.
                    # If cost higher than lowest wage, better if the worker takes hour off work to provide for social care
                    suppliersWithTime = [x for x in careSlot.suppliers if x.afterCareJS[i][j] == 1]
                    if len(suppliersWithTime) > 0:
                        # Sort wage from low to high
                        suppliersWithTime.sort(key=operator.attrgetter("wage"))
                        careSupplier = suppliersWithTime[0]
                    if len(suppliersWithTime) > 0 and careSlot.cost-house.carriedOverCost > careSupplier.wage:
                        careSupplier.afterCareJS[careSlot.day][careSlot.hour] = 0
                        maxIncomeForCare = max(maxIncomeForCare-careSupplier.wage, 0.0)
                        careSupplier.socialWork += 1
                        careSupplier.availableWorkingHours -= 1
                        careSupplier.freeWorkingHours -= 1
                        careSupplier.outOfWorkSocialCare += 1
                        house.shiftTable[careSlot.day][careSlot.hour] = supplier
                        # Update receiver's state
                        receiver = careSlot.receivers[0]
                        person.privateSocialCareNeed = max(receiver.privateSocialCareNeed-1, 0)
                        person.unmetSocialCareNeed = max(receiver.unmetSocialCareNeed-1, 0)
                        person.informalSocialCareReceived += 1
                        self.internalSocialCare += 1
                        # house.totalSocialCareNeed -= 1
                        
                        if careSlot.hour == -1:
                            person.weelyFlexibleNeeds[careSlot.day] = max(person.weelyFlexibleNeeds[careSlot.day]-1, 0)
                        else:
                            if careSlot.hour == 0:
                                person.fixedNeedSchedule[0][0] = 0
                            elif careSlot.hour == 1:
                                person.fixedNeedSchedule[0][1] = 0
                            elif careSlot.hour == 4:
                                person.fixedNeedSchedule[1][0] = 0
                            elif careSlot.hour == 5:
                                person.fixedNeedSchedule[1][1] = 0
                            elif careSlot.hour == 10:
                                person.fixedNeedSchedule[2][0] = 0
                            elif careSlot.hour == 11:
                                person.fixedNeedSchedule[2][1] = 0
                            elif careSlot.hour == 13:
                                person.fixedNeedSchedule[3][0] = 0
                            elif careSlot.hour == 14:
                                person.fixedNeedSchedule[3][1] = 0  
                                
                    elif len(suppliersWithTime) == 0 or careSlot.cost-house.carriedOverCost < careSupplier.wage:
                        additionalCost = max(careSlot.cost-house.carriedOverCost, 0.0)
                        maxIncomeForCare -= additionalCost
                        maxIncomeForCare = max(maxIncomeForCare, 0.0)
                        if house.carriedOverCost > careSlot.cost:
                            house.carriedOverCost -= careSlot.cost
                        else:
                            if house.potentialIncomeFromWelfare < additionalCost:
                                house.potentialIncomeFromWelfare = 0
                                if len(slotSuppliers) > 0:
                                    residualCost = additionalCost - house.potentialIncomeFromWelfare
                                    maxWage = careSlot.suppliers[-1].wage
                                    additionalIncome = np.ceil(residualCost/maxWage)*maxWage
                                    careSlot.suppliers[-1].freeWorkingHours -= int(np.ceil(residualCost/maxWage))
                                    careSlot.suppliers[-1].freeWorkingHours = max(careSlot.suppliers[-1].freeWorkingHours, 0)
                                    house.carriedOverCost = max(additionalIncome-residualCost, 0.0)
                                else:
                                    house.carriedOverCost = 0
                            else:
                                house.potentialIncomeFromWelfare -= additionalCost
                                house.carriedOverCost = 0
                                
                        house.formalSocialCare += 1
                        house.costFormalCare += additionalCost
                        house.costFormalSocialCare += additionalCost
                        house.totalUnmetSocialCareNeed -= 1
                        
                        # Degugging code
#                            if house not in self.householdsWithFormalChildCare and self.periodFormalCare == False:
#                                self.householdsWithFormalChildCare.append(house)
                            
                        # Update receiver's state
                        receiver = careSlot.receivers[0]
                        person.privateSocialCareNeed = max(receiver.privateSocialCareNeed-1, 0)
                        person.unmetSocialCareNeed = max(receiver.unmetSocialCareNeed-1, 0)
                        person.formalSocialCareReceived += 1
                        self.internalSocialCare += 1
                        # house.totalSocialCareNeed -= 1
                        
                        if careSlot.hour == -1:
                            person.weelyFlexibleNeeds[careSlot.day] = max(person.weelyFlexibleNeeds[careSlot.day]-1, 0)
                        else:
                            if careSlot.hour == 0:
                                person.fixedNeedSchedule[0][0] = 0
                            elif careSlot.hour == 1:
                                person.fixedNeedSchedule[0][1] = 0
                            elif careSlot.hour == 4:
                                person.fixedNeedSchedule[1][0] = 0
                            elif careSlot.hour == 5:
                                person.fixedNeedSchedule[1][1] = 0
                            elif careSlot.hour == 10:
                                person.fixedNeedSchedule[2][0] = 0
                            elif careSlot.hour == 11:
                                person.fixedNeedSchedule[2][1] = 0
                            elif careSlot.hour == 13:
                                person.fixedNeedSchedule[3][0] = 0
                            elif careSlot.hour == 14:
                                person.fixedNeedSchedule[3][1] = 0  
                    
                house.careSlots.remove(careSlot)
                remainingSlots = []
                for slot in house.careSlots:
                    careWeight = 0
                    if careSlot.childCare == True:
                        careWeight = sum([x.privateChildCareNeed_WNH+x.privateChildCareNeed_ONH for x in slot.receivers])*maxIncomeForCare
                    else:
                        careWeight = sum([x.privateSocialCareNeed  for x in slot.receivers])*maxIncomeForCare
                    prob = (np.exp(self.p['probIncomeCare']*careWeight)-1.0)/np.exp(self.p['probIncomeCare']*careWeight)
                    if careSlot.childCare == True:
                        if careSlot.day > 4 or (careSlot.day < 5 and careSlot.hour > 9):
                            slot.suppliers = [x for x in suppliers if x.afterCareJS[slot.day][slot.hour] == 1 and x.freeWorkingHours > 0]
                        else:
                            slot.suppliers = [x for x in suppliers if x.freeWorkingHours > 0]
                    else:  
                        slot.suppliers = [x for x in suppliers if x.afterCareJS[slot.day][slot.hour] == 1 and x.freeWorkingHours > 0]
                    if len(slot.suppliers) > 0 and np.random.random() < prob:
                        remainingSlots.append(slot)
                house.careSlots = [x for x in remainingSlots]
#                slots_WNH = [x for x in house.careSlots if x.day < 5 and x.hour < 10]
#                slots_ONH = [x for x in house.careSlots if x not in slots_WNH]
#                house.careSlots = [x for x in slots_WNH if sum([y.privateChildCareNeed_WNH for y in x.receivers])> 0] + [x for x in slots_ONH if sum([y.privateChildCareNeed_ONH for y in x.receivers])> 0]
            end = time.time()
            CareProvision7_extim += (end - start) 
            
        # Allocate public care
        # Satisfy residual care needs of agents with the public child/social care owed to them.
        self.totalUnmetChildCareNeed = 0
        self.totalUnmetSocialCareNeed = 0
        for house in self.map.occupiedHouses:
            house.totalUnmetChildCareNeed = 0
            house.totalUnmetSocialCareNeed = 0
            for agent in house.childCareRecipients:
                agent.unmetchildCareNeed = 0
                agent.residualPublicCare = agent.publicCareSupply
                for i in range(7):
                    for j in range(24):
                        if i < 4 and j < 10:
                            if agent.unmetWeeklyNeeds[i][j] == 1:
                                if agent.residualPublicCare == 0:
                                    agent.unmetChildCareNeed += 1
                                    house.totalUnmetChildCareNeed += 1
                                    self.totalUnmetChildCareNeed += 1
                                else:
                                    agent.residualPublicCare -= 1
                                    agent.unmetWeeklyNeeds[i][j] = 0
                        else:
                            if agent.unmetWeeklyNeeds[i][j] == 1:
                                agent.unmetchildCareNeed += 1
                                house.totalUnmetChildCareNeed += 1
                                self.totalUnmetChildCareNeed += 1
                
            for agent in house.socialCareRecipients:
                agent.unmetSocialCareNeed = 0
                agent.residualPublicCare = agent.publicCareSupply
                for i in range(4):
                    for j in range(2):
                        if agent.fixedNeedSchedule[i][j] == 1:
                            if agent.publicCareSupply == 0:
                                agent.unmetSocialCareNeed += 1
                                house.totalUnmetSocialCareNeed += 1
                                self.totalUnmetSocialCareNeed += 1
                            else:
                                agent.residualPublicCare -= 1
                                agent.fixedNeedSchedule[i][j] = 0
                unmetFlexibleNeeds = sum([x for x in agent.weelyFlexibleNeeds])
                if unmetFlexibleNeeds > agent.residualPublicCare:
                    unmetFlexibleNeeds -= agent.residualPublicCare
                    agent.unmetSocialCareNeed += unmetFlexibleNeeds
                    house.totalUnmetSocialCareNeed += unmetFlexibleNeeds
                    self.totalUnmetSocialCareNeed += unmetFlexibleNeeds
                    agent.residualPublicCare = 0
                else:
                    agent.residualPublicCare -= unmetFlexibleNeeds
        
            house.totalUnmetCareNeed = house.totalUnmetSocialCareNeed+house.totalUnmetChildCareNeed

        self.totalUnmetCareNeed = self.totalUnmetChildCareNeed+self.totalUnmetSocialCareNeed
        if self.totalChildCareNeed > 0:
            print 'Share unmet childcare need: ' + str(float(self.totalUnmetChildCareNeed)/float(self.totalChildCareNeed))
        if self.totalSocialCareNeed > 0:
            print 'Share unmet social care need: ' + str(float(self.totalUnmetSocialCareNeed)/float(self.totalSocialCareNeed))
        
        print 'Care provision 1 time: ' + str(CareProvision1_extim)
        print 'Care provision 2 time: ' + str(CareProvision2_extim)
        print 'Care provision 3 time: ' + str(CareProvision3_extim)
        print 'Care provision 4 time: ' + str(CareProvision4_extim)
        print 'Care provision 5 time: ' + str(CareProvision5_extim)
        print 'Care provision 6 time: ' + str(CareProvision6_extim)
        print 'Care provision 7 time: ' + str(CareProvision7_extim)
        
    def checkHouseholdsProvidingFormalCare(self):
        if len(self.householdsWithFormalChildCare) > 0:
            print ''
            print 'Number of houses with formal care: ' + str(len(self.householdsWithFormalChildCare))
            print 'Houses ids: ' + str([x.id for x in self.householdsWithFormalChildCare])
            for house in self.householdsWithFormalChildCare[:2]:
                print 'House id: ' + str(house.id)
                print 'Household size: ' + str(len(house.occupants))
                print 'Household ages: ' + str([x.age for x in house.occupants])
                print 'Household statuses: ' + str([x.status for x in house.occupants])
                print 'Childcare needs: ' + str([x.totalChildCareNeed for x in house.occupants])
                print 'Social care need levels: ' + str([x.careNeedLevel for x in house.occupants])
                print 'Residual care needs (pre): ' + str(house.residualCareNeed_PreFormal)
                print 'Unmet child care need (pre): ' + str(house.unmetChildCareNeed_Pre)
                print 'House total care need (pre): ' + str(house.totalCareNeed_Pre)
                print 'House childcare slots (pre): ' + str(house.totalChildCareSlots_Pre)
                print 'House priority slots (pre): ' + str(house.totalPriorityCareSlots_Pre)
                print 'House onh slots: ' + str(house.onhSlots_Pre)
                print 'House wnh slots: ' + str(house.wnhSlots_Pre)
                
                print 'Out of work care (pre): ' + str(house.totalOutOfWorkChildCare_Pre)
                print 'Out of work care (post): ' + str(sum([x.outOfWorkChildCare for x in house.occupants]))
                
                print 'slotWithCareSuppliers_ONH: ' + str(house.slotWithCareSuppliers_ONH)
                print 'slotWithCareSuppliers_WNH: ' + str(house.slotWithCareSuppliers_WNH)
                print 'numCostGreaterThanWage: ' + str(house.numCostGreaterThanWage)
                print 'numCostSmallerThanWage: ' + str(house.numCostSmallerThanWage)
                print 'numNoSuppliers: ' + str(house.numNoSuppliers)
                
                
                print 'Formal child care: ' + str(house.formalChildCare)
                print 'Formal social care: ' + str(house.formalSocialCare)
                print 'Household unmet child care need: ' + str(house.totalUnmetSocialCareNeed)
                print 'Carers: ' + str([x.potentialCarer for x in house.occupants])
                print 'Wages: ' + str([x.wage for x in house.occupants])
                print 'Pensions: ' + str([x.pension for x in house.occupants])
                print 'Income from work: ' + str(house.potentialIncomeFromWork)
                print 'Income from welfare: ' + str(house.potentialIncomeFromWelfare)
                print 'Total income: ' + str(house.totalPotentialIncome)
                print 'Poverty line: ' + str(house.povertyLineIncome)
                print ''
        

    def getHouseSuppliers(self, house, day, hour, d):
        if d == 1:
            supplyingHouses = [x for x in house.d1Households]
        else:
            supplyingHouses = [x for x in house.d2Households]
        suppliers = []
        for h in supplyingHouses:
            houseSuppliers = [x for x in h.occupants if x.potentialCarer == True and x.weeklyTime[day][hour] == 1 and x.residualDailySupplies[day] > 0 and x.residualWeeklySupplies[d] > 0]
            for agent in houseSuppliers:
                if house not in agent.householdsToHelp:
                    agent.householdsToHelp.append(house)
            suppliers.extend(houseSuppliers)
        return suppliers
    
    def getPersonSuppliers(self, person, day, hour, d):
        suppliers = []
        if d == 1:
            supplyingHouses = [x for x in person.d1Households]
        else:
            supplyingHouses = [x for x in person.d2Households]
        if hour != -1:
            for h in supplyingHouses:
                houseSuppliers = [x for x in h.occupants if x.potentialCarer == True and x.weeklyTime[day][hour] == 1 and x.residualDailySupplies[day] > 0 and x.residualWeeklySupplies[d] > 0]
                for agent in houseSuppliers:
                    if person.house not in agent.householdsToHelp:
                        agent.householdsToHelp.append(person.house)
                suppliers.extend(houseSuppliers)
        else:
            for h in supplyingHouses:
                houseSuppliers = [x for x in h.occupants if x.potentialCarer == True and x.residualDailySupplies[day] > 0 and sum(x.weeklyTime[day][:10]) > 0 and x.residualWeeklySupplies[d] > 0]
                for agent in houseSuppliers:
                    if person.house not in agent.householdsToHelp:
                        agent.householdsToHelp.append(person.house)
                suppliers.extend(houseSuppliers)
        return suppliers
        
        
    def oldCareProvisionCode(self):
        
        # First, the household's informal care is allocated to slots with children aged below 8.
        housesChildcareNeeds = [x for x in self.map.occupiedHouses if x.totalChilcareNeed_ONH > 0]
        for house in housesChildcareNeeds:
            # First, informal care is allocated to children aged 1-7 year old
            priorityAges = [x for x in house.childrenAges if x < self.p['priorityAgeThreshold']]
            for c in priorityAges:
                for h in range(house.numberOfCarers):
                    for i in range(7):
                        s = 10
                        if i > 4:
                            s = 0
                        for j in range(s, 24): 
                            if house.childMinAge[i][j] == c and house.householdInformalSupplySchedule[i][j] == h+1:
                                suppliers = [x for x in house.householdInformalSuppliers[i][j] if x.weeklyTime[i][j] == 1 and x.residualDailySupplies[i] > 0 and x.residualWeeklySupplies[0] > 0]
                                # Sort suppliers according to total residual availability on that day
                                if len(suppliers) > 0:
                                    weights = [float(x.residualDailySupplies[i]) for x in suppliers]
                                    probs = [x/sum(weights) for x in weights]
                                    supplier = np.random.choice(suppliers, p = probs)
                                    supplier.weeklyTime[i][j] = 0
                                    house.childrenCareNeedSchedule[i][j] = 0
                                    house.householdInformalSupplySchedule[i][j] -= 1
                                    house.shiftTable[i][j] = supplier
                                    for d in range(4):
                                        supplier.residualWeeklySupplies[d] -= 1
                                        house.householdInformalSupplies[d] -= 1
                                    supplier.residualWeeklySupplies = [max(x, 0) for x in supplier.residualWeeklySupplies]
                                    house.householdInformalSupplies = [max(x, 0) for x in house.householdInformalSupplies]
                                    supplier.residualDailySupplies[i] -= 1
                                    supplier.residualDailySupplies[i] = [max(x, 0) for x in supplier.residualDailySupplies[i]]
                                    if supplier.residualWeeklySupplies[0] < supplier.residualDailySupplies[i]:
                                        
                                        for agent in house.childrenInNeedByHour[i][j]:
                                            agent.unmetWeeklyNeeds[i][j] = 0
                                            agent.residualChildcareNeed -= 1
                                            house.totalChilcareNeed -= 1
                                            house.totalChilcareNeed_ONH -= 1
                                    

        # For the allocation of the remaining internal informal care, a list of care slots is created.
        # Each care slot if associated with a weight, representing the quantity of care, and a total potential supply.
        # Care slots are randomly sampled with probabilities:
        # - directly proportional to their weight
        # - inversely proportional to the amout of potential supply (slots with zero supply are excluded)
        # 
        housesWSCCN = [x for x in self.map.occupiedHouses if x.totalChilcareNeed_ONH > 0 and x.totalSocialCareNeed > 0]
        
        
        # Houses with only Childcare need
        housesCCN = [x for x in self.map.occupiedHouses if x.totalChilcareNeed_ONH > 0 and x not in housesWSCCN]
        
        # Houses with only social care need
        housesSCN = [x for x in self.map.occupiedHouses if x.totalSocialCareNeed > 0 and x not in housesWSCCN]
        

        
        
        
        
        
                                
        ################################################################################                            
        ###
        ###  Now allocate social care to household's members with social care needs
        ###
        ###################################################################################
        
        
        # Check if there is unmet child care outside the nurseries/schools opening hours
        # If there is, seek care from other households at distance 1
        housesWithExternalSupply = self.updateNetworkSchedule('ONH', 1)
        while len(housesWithExternalSupply) > 0:
            weights = [float(x.totalChilcareNeed_ONH) for x in housesWithExternalSupply]
            probs = [x/sum(weights) for x in weights]
            house = np.random.choice(housesWithExternalSupply, p = probs)
            for h in range(house.maxHourSuppliers):
                for c in range(house.numChildcareReceivers, 0, -1):
                    for i in range(7):
                        s = 10
                        if i > 4:
                            s = 0
                        for j in range(s, 24): 
                            if house.childrenCareNeedSchedule[i][j] == c and house.d1SuppliesSchedule[i][j] == h+1:
                                suppliers = [x for x in house.d1WeeklySuppliers[i][j] if x.weeklyTime[i][j] == 1 and x.residualDailySupplies[i] > 0 and x.residualWeeklySupplies[1] > 0]
                                # Sort suppliers according to total residual availability on that day
                                if len(suppliers) > 0:
                                    weights = [float(x.residualDailySupplies[i]) for x in suppliers]
                                    probs = [x/sum(weights) for x in weights]
                                    supplier = np.random.choice(suppliers, p = probs)
                                    supplyingHouse = supplier.house
                                    supplier.weeklyTime[i][j] = 0
                                    house.childrenCareNeedSchedule[i][j] = 0
                                    house.d1SuppliesSchedule[i][j] -= 1
                                    supplier.residualDailySupplies[i] -= 1
                                    supplier.residualDailySupplies[i] = [max(x, 0) for x in supplier.residualDailySupplies[i]]
                                    house.shiftTable[i][j] = supplier
                                    for d in range(4):
                                        supplier.residualWeeklySupplies[d] -= 1
                                        supplyingHouse.householdInformalSupplies[d] -= 1
                                    supplier.residualWeeklySupplies = [max(x, 0) for x in supplier.residualWeeklySupplies]
                                    supplyingHouse.householdInformalSupplies = [max(x, 0) for x in supplyingHouse.householdInformalSupplies]
                                    for agent in house.childrenInNeedByHour[i][j]:
                                        agent.unmetWeeklyNeeds[i][j] = 0
                                        agent.residualChildcareNeed -= 1
                                        house.totalChilcareNeed -= 1
                                        house.totalChilcareNeed_ONH -= 1
            housesWithExternalSupply = self.updateNetworkSchedule('ONH', 1)
            
        # Serve slots with children aged > 7 with the supply of relatives ONLY serving children
        # Serve slots of social care (starting with high unmet care needs) with supply of relatives serving ONLY people with social care needs
        # For suppliers of BOTH child and social care, random sample of ALL slots (aggregate childcare and individual social care)
        
            
        ################################################################################                            
        ###
        ###  Now allocate social care to household's members with social care needs
        ###
        ###################################################################################
            
        
        # Distance 2: Aunts and uncles
        housesWithExternalSupply = self.updateNetworkSchedule('ONH', 2)
        while len(housesWithExternalSupply) > 0:
            # Randomly sample a receiving household depending on amount of residual childcare need
            weights = [float(x.totalChilcareNeed_ONH) for x in housesWithExternalSupply]
            probs = [x/sum(weights) for x in weights]
            house = np.random.choice(housesWithExternalSupply, p = probs)
            for h in range(house.maxHourSuppliers):
                for c in range(house.numChildcareReceivers, 0, -1):
                    for i in range(7):
                        s = 10
                        if i > 4:
                            s = 0
                        for j in range(s, 24): 
                            if house.childrenCareNeedSchedule[i][j] == c and house.d2SuppliesSchedule[i][j] == h+1:
                                suppliers = [x for x in house.d2WeeklySuppliers[i][j] if x.weeklyTime[i][j] == 1 and x.residualDailySupplies[i] > 0 and x.residualWeeklySupplies[2] > 0]
                                # Sort suppliers according to total residual availability on that day
                                if len(suppliers) > 0:
                                    weights = [float(x.residualDailySupplies[i]) for x in suppliers]
                                    probs = [x/sum(weights) for x in weights]
                                    supplier = np.random.choice(suppliers, p = probs)
                                    supplyingHouse = supplier.house
                                    supplier.weeklyTime[i][j] = 0
                                    house.childrenCareNeedSchedule[i][j] = 0
                                    house.d2SuppliesSchedule[i][j] -= 1
                                    supplier.residualDailySupplies[i] -= 1
                                    supplier.residualDailySupplies[i] = [max(x, 0) for x in supplier.residualDailySupplies[i]]
                                    house.shiftTable[i][j] = supplier
                                    for d in range(4):
                                        supplier.residualWeeklySupplies[d] -= 1
                                        supplyingHouse.householdInformalSupplies[d] -= 1
                                    supplier.residualWeeklySupplies = [max(x, 0) for x in supplier.residualWeeklySupplies]
                                    supplyingHouse.householdInformalSupplies = [max(x, 0) for x in supplyingHouse.householdInformalSupplies]
                                    for agent in house.childrenInNeedByHour[i][j]:
                                        agent.unmetWeeklyNeeds[i][j] = 0
                                        agent.residualChildcareNeed -= 1
                                        house.totalChilcareNeed -= 1
                                        house.totalChilcareNeed_ONH -= 1
            housesWithExternalSupply = self.updateNetworkSchedule('ONH', 2)
        
        # If there is, parents need to take hours off work (until minimum income threshold reached)
        housesChildcareNeeds = [x for x in self.map.occupiedHouses if x.totalChilcareNeed_ONH > 0]
        self.totalHoursOffWork = 0
        for house in housesChildcareNeeds:
            parents = [x for x in house.occupants if x.independentStatus == True]
            for parent in parents:
                parent.hoursOffWork = 0
            lowWageParent = parents[0]
            residualSupplies = [lowWageParent.workingHours]
            if len(parents) > 1:
                highWageParent = parents[1]
                if parents[0].wage > parents[1].wage:
                    lowWageParent = parents[1]
                    highWageParent = parents[0]
                residualSupplies = [lowWageParent.workingHours, highWageParent.workingHours]
            house.householdHoursOffWork = 0
            for c in range(house.numChildcareReceivers, 0, -1):
                for i in range(7):
                    s = 10
                    if i > 4:
                        s = 0
                    for j in range(s, 24):
                        if house.childrenCareNeedSchedule[i][j] == c:
                            if residualSupplies[0] > 0:
                                lowWageParent.weeklyTime[i][j] = 0
                                house.childrenCareNeedSchedule[i][j] = 0
                                house.shiftTable[i][j] = lowWageParent
                                residualSupplies[0] -= 1
                                lowWageParent.workingHours -= 1
                                lowWageParent.hoursOffWork += 1
                                house.householdHoursOffWork += 1
                                self.totalHoursOffWork += 1
                                # Do the out-of-work care reduces the daily and weekly availability?
#                                for d in range(4):
#                                    lowWageParent.residualWeeklySupplies[d] -= 1
#                                    house.householdInformalSupplies[d] -= 1
#                                lowWageParent.residualWeeklySupplies = [max(x, 0) for x in parent.residualWeeklySupplies]
#                                house.householdInformalSupplies = [max(x, 0) for x in house.householdInformalSupplies]
                                for agent in house.childrenInNeedByHour[i][j]:
                                    agent.unmetWeeklyNeeds[i][j] = 0
                                    agent.residualChildcareNeed -= 1
                                    house.totalChilcareNeed -= 1
                                    house.totalChilcareNeed_ONH -= 1
                            elif len(residualSupplies) > 1 and residualSupplies[1] > 0:
                                highWageParent.weeklyTime[i][j] = 0
                                house.childrenCareNeedSchedule[i][j] = 0
                                house.shiftTable[i][j] = highWageParent
                                residualSupplies[1] -= 1
                                highWageParent.workingHours -= 1
                                highWageParent.hoursOffWork += 1
                                house.householdHoursOffWork += 1
                                self.totalHoursOffWork += 1
#                                for d in range(4):
#                                    highWageParent.residualWeeklySupplies[d] -= 1
#                                    house.householdInformalSupplies[d] -= 1
#                                highWageParent.residualWeeklySupplies = [max(x, 0) for x in parent.residualWeeklySupplies]
#                                house.householdInformalSupplies = [max(x, 0) for x in house.householdInformalSupplies]
                                for agent in house.childrenInNeedByHour[i][j]:
                                    agent.unmetWeeklyNeeds[i][j] = 0
                                    agent.residualChildcareNeed -= 1
                                    house.totalChilcareNeed -= 1
                                    house.totalChilcareNeed_ONH -= 1
                                
        housesChildcareNeeds = [x for x in self.map.occupiedHouses if x.totalChilcareNeed_ONH > 0]
                
        print 'There are ' + str(len(housesChildcareNeeds)) + ' households with unmet childcare need outside nursery hours.'
        unmetChildcareNeeds = [x.totalChilcareNeed_ONH for x in housesChildcareNeeds]
        self.onhUnmetChildcareNeed = sum(unmetChildcareNeeds)
        self.medianChildCareNeedONH = 0
        if len(unmetChildcareNeeds) > 0:
            self.medianChildCareNeedONH = np.median(unmetChildcareNeeds)
            print 'Min unmet childcare needs: ' + str(min(unmetChildcareNeeds))
            print 'Max unmet childcare needs: ' + str(max(unmetChildcareNeeds))
            print 'Median unmet childcare needs: ' + str(np.median(unmetChildcareNeeds))   
        print 'Total hours of unmet childcare need are: ' + str(self.onhUnmetChildcareNeed)
        print 'The total hours off work outside nursary hours are ' + str(self.totalHoursOffWork)
            
        # 2 - Childcare needs within the nurseries/schools opening hours (here, possibility to buy formal care)
       
        # The logic of the allocation of informal care now changes: the hours which need to be satisfied first are those
        # characterized by a high cost of childcare (i.e. the hours when ther are many children needing care)
        # First compute the cost of chilcare hours.
        self.updateChildCareData()
        
        housesChildcareNeeds = [x for x in self.map.occupiedHouses if x.totalChilcareNeed_WNH > 0]
        for house in housesChildcareNeeds:
            parents = [x for x in household if x.independentStatus == True]
            # slotsWithSuppliers = [x for x in house.costUnits]
            # listCosts = list(set([x.cost for x in slotsWithSuppliers]))
            # listCosts.sort(reverse=True)
            # for cost in house.costUnits:
                # slotsByCost = [x for x in slotsWithSuppliers if x.cost == cost]
                # slotsByCost.sort(key=operator.attrgetter("numSuppliers"))
            for slot in house.costUnits:
                for parent in parents:
                    if parent.weeklyTime[slot.day][slot.hours] == 1:
                        parent.weeklyTime[slot.day][slot.hours] = 0
                        parent.residualDailySupplies[i] -= 1
                        parent.residualDailySupplies[i] = max(parent.residualDailySupplies[i], 0)
                        house.shiftTable[slot.day][slot.hours] = parent
                        for d in range(4):
                            parent.residualWeeklySupplies[d] -= 1
                            house.householdInformalSupplies[d] -= 1
                        parent.residualWeeklySupplies = [max(x, 0) for x in parent.residualWeeklySupplies]
                        house.householdInformalSupplies = [max(x, 0) for x in house.householdInformalSupplies]
                        house.childrenCareNeedSchedule[slot.day][slot.hours] = 0
                        for agent in house.childrenInNeedByHour[slot.day][slot.hours]:
                            agent.residualChildcareNeed -= 1
                            agent.unmetWeeklyNeeds[slot.day][slot.hours] = 0
                            house.totalChilcareNeed -= 1
                            house.totalChilcareNeed_WNH -= 1
                        house.costUnits.remove(slot)
            
        self.updateChildCareData()   
       
        # Now, allocate the time of the other members of the household, starting with the hours with less help first.
        housesChildcareNeeds = [x for x in self.map.occupiedHouses if x.totalChilcareNeed_WNH > 0]
        for house in housesChildcareNeeds:
            slotsWithSuppliers = [x for x in house.costUnits if x.numSuppliers > 0]
            listCosts = list(set([x.cost for x in slotsWithSuppliers]))
            listCosts.sort(reverse=True)
            for cost in listCosts:
                slotsByCost = [x for x in slotsWithSuppliers if x.cost == cost]
                slotsByCost.sort(key=operator.attrgetter("numSuppliers"))
                for slot in slotsByCost:
                    weights = [float(x.residualDailySupplies[i]) for x in slot.suppliers]
                    probs = [x/sum(weights) for x in weights]
                    supplier = np.random.choice(slot.suppliers, p = probs)
                    supplier.residualDailySupplies[i] -= 1
                    house.shiftTable[i][j] = supplier
                    for d in range(4):
                        supplier.residualWeeklySupplies[d] -= 1
                        house.householdInformalSupplies[d] -= 1
                    supplier.residualWeeklySupplies = [max(x, 0) for x in supplier.residualWeeklySupplies]
                    house.householdInformalSupplies = [max(x, 0) for x in house.householdInformalSupplies]
                    supplier.weeklyTime[i][j] = 0
                    house.householdInformalSupplySchedule[i][j] -= 1
                    house.childrenCareNeedSchedule[i][j] = 0
                    for agent in house.childrenInNeedByHour[i][j]:
                        agent.unmetWeeklyNeeds[i][j] = 0
                        agent.residualChildcareNeed -= 1
                        house.totalChilcareNeed -= 1
                        house.totalChilcareNeed_WNH -= 1
                                          
        # Now tap into the informal care availability of close relatives (granparents and independent brothers)
        housesWithExternalSupply = self.updateNetworkSchedule('WNH', 1)
        while len(housesWithExternalSupply) > 0:
            self.updateChildCareData()
            weights = [float(x.totalChilcareNeed_WNH) for x in housesWithExternalSupply]
            probs = [x/sum(weights) for x in weights]
            house = np.random.choice(housesWithExternalSupply, p = probs)
            slotsWithSuppliers = [x for x in house.costUnits if x.numSuppliers > 0]
            listCosts = list(set([x.cost for x in slotsWithSuppliers]))
            listCosts.sort(reverse=True)
            slotsByCost = [x for x in slotsWithSuppliers if x.cost == listCosts[0]]
            slotsByCost.sort(key=operator.attrgetter("numSuppliers"))
            for h in range(house.maxHourSuppliers):
                for i in range(5):
                    for j in range(10): 
                        if house.childrenCareNeedSchedule[i][j] > 0 and house.d1SuppliesSchedule[i][j] == h+1:
                            suppliers = [x for x in house.d1WeeklySuppliers[i][j] if x.weeklyTime[i][j] == 1 and x.residualDailySupplies[i] > 0 and x.residualWeeklySupplies[1] > 0]
                            # Sort suppliers according to total residual availability on that day
                            if len(suppliers) > 0:
                                weights = [float(x.residualDailySupplies[i]) for x in suppliers]
                                probs = [x/sum(weights) for x in weights]
                                supplier = np.random.choice(suppliers, p = probs)
                                supplyingHouse = supplier.house
                                supplier.residualDailySupplies[i] -= 1
                                house.shiftTable[i][j] = supplier
                                for d in range(4):
                                    supplier.residualWeeklySupplies[d] -= 1
                                    supplyingHouse.householdInformalSupplies[d] -= 1
                                supplier.residualWeeklySupplies = [max(x, 0) for x in supplier.residualWeeklySupplies]
                                supplyingHouse.householdInformalSupplies = [max(x, 0) for x in supplyingHouse.householdInformalSupplies]
                                supplier.weeklyTime[i][j] = 0
                                house.d1SuppliesSchedule[i][j] -= 1
                                house.childrenCareNeedSchedule[i][j] = 0
                                for agent in house.childrenInNeedByHour[i][j]:
                                    agent.unmetWeeklyNeeds[i][j] = 0
                                    agent.residualChildcareNeed -= 1
                                    house.totalChilcareNeed -= 1
                                    house.totalChilcareNeed_WNH -= 1
            
            housesWithExternalSupply = self.updateNetworkSchedule('WNH', 1)
        
        # Distance 2 suppliers
        housesWithExternalSupply = self.updateNetworkSchedule('WNH', 2)
        while len(housesWithExternalSupply) > 0:
            self.updateChildCareData()
            # Randomly sample a receiving household depending on amount of residual childcare need
            weights = [float(x.totalChilcareNeed_WNH) for x in housesWithExternalSupply]
            probs = [x/sum(weights) for x in weights]
            house = np.random.choice(housesWithExternalSupply, p = probs)
            for h in range(house.maxHourSuppliers):
                for i in range(5):
                    for j in range(10): 
                        if house.childrenCareNeedSchedule[i][j] > 0 and house.d2SuppliesSchedule[i][j] == h+1:
                            suppliers = [x for x in house.d2WeeklySuppliers[i][j] if x.weeklyTime[i][j] == 1 and x.residualDailySupplies[i] > 0 and x.residualWeeklySupplies[2] > 0]
                            # Sort suppliers according to total residual availability on that day
                            if len(suppliers) > 0:
                                weights = [float(x.residualDailySupplies[i]) for x in suppliers]
                                probs = [x/sum(weights) for x in weights]
                                supplier = np.random.choice(suppliers, p = probs)
                                supplyingHouse = supplier.house
                                supplier.residualDailySupplies[i] -= 1
                                house.shiftTable[i][j] = supplier
                                for d in range(4):
                                    supplier.residualWeeklySupplies[d] -= 1
                                    supplyingHouse.householdInformalSupplies[d] -= 1
                                supplier.residualWeeklySupplies = [max(x, 0) for x in supplier.residualWeeklySupplies]
                                supplyingHouse.householdInformalSupplies = [max(x, 0) for x in supplyingHouse.householdInformalSupplies]
                                supplier.weeklyTime[i][j] = 0
                                house.d2SuppliesSchedule[i][j] -= 1
                                house.childrenCareNeedSchedule[i][j] = 0
                                for agent in house.childrenInNeedByHour[i][j]:
                                    agent.unmetWeeklyNeeds[i][j] = 0
                                    agent.residualChildcareNeed -= 1
                                    house.totalChilcareNeed -= 1
                                    house.totalChilcareNeed_WNH -= 1
            housesWithExternalSupply = self.updateNetworkSchedule('WNH', 2)
        
        
        # Allocate public childcare
        housesChildcareNeeds = [x for x in self.map.occupiedHouses if x.totalChilcareNeed_WNH > 0]
        for house in housesChildcareNeeds:
            children = [x for x in house.occupants if x.age >= 2 and x.age < 5 and x.publicCareSupply > 0]
            for child in children:
                residualPublicSupply = child.publicCareSupply
                for d in range(house.numberOfCarers+1):
                    for i in range(5):
                        for j in range(10):
                            if child.unmetWeeklyNeeds[i][j] == 1 and residualPublicSupply > 0 and house.householdInformalSupplySchedule[i][j] == d:
                                child.unmetWeeklyNeeds[i][j] = 0
                                agent.residualChildcareNeed -= 1
                                house.childrenCareNeedSchedule[i][j] -= 1
                                residualPublicSupply -= 1
                                house.totalChilcareNeed -= 1
                                house.totalChilcareNeed_WNH -= 1
        
        
        # Now, buy child care if there is unmet child care in the nurseries' opening hours (8-18)
        # It can be done either by using the household's income or by taking hours off work (if the price of childcare is above the lowest wage)
        housesChildcareNeeds = [x for x in self.map.occupiedHouses if x.totalChilcareNeed_WNH > 0]
        for house in housesChildcareNeeds:
            # Determine the low earning and high earning parent
            # Loop through the weekly costs. 
            # Where the cost is higher than the lowest wage, the low-wage parent takes time off work.
            # Where the cost is lower than the lowest wage, the income is used to satisfy it, by reseving 
            # the corresponding number of the high-wage parent's working hours.
            parents = [x for x in house.occupants if x.independentStatus == True]
            lowWageParent = parents[0]
            lowestWage = parents[0].wage
            if len(parents) > 1:
                highWageParent = parents[1]
                highestWage = parents[1].wage
                if parents[1].wage < parents[0].wage:
                    lowWageParent = parents[1]
                    lowestWage = parents[1].wage
                    highWageParent = parents[0]
                    highestWage = parents[0].wage
            house.costUnits.sort(key=operator.attrgetter("cost"), reverse = True)
            # for costUnit in house.costUnits:
                # if costUnit.cost > lowestWage:
                    # In this case, the low-wage parent takes hours off work to provide childcare.
                    
                    
                # else:
                    # In this case, the childcare is paid with the housheold income.
                    # First, the income which does not depend on work is used.
                    # Then, the income that depends on work, and the corresponding number of the high-wage parent's working hours
                    # are reserved.
                    
                        
        
       
        
        
            # Check if public care enough for residual need, else, go to Step 2
            
            # Step 2: allocate the available time of granparents livig in the household
            
            # Check if public care enough for residual need, else go to Step 3 (and so on)
            
            # Step 3. Allocate public childcare (Childen aged 2 to 4)
        
            # Step 4. Buy residual childcare (if enough income), either buy spending income or taking time off work.
            
            
        # 3 - If enough income, dispense from informal care starting from the last suppliers (either buy spending income or taking time off work)
    
    
    def updateHouseholdChildCareNeeds(self, house): 
        householdCarers = [x for x in house.occupants if x.potentialCarer == True]
        # Update the weekly schedule information
        house.householdInformalSuppliers = []
        house.householdInformalSupplySchedule = []
        for i in range(7):
            day = []
            suppliers = []
            for j in range(24):
                careAvailabilityScore = sum([x.weeklyTime[i][j] for x in householdCarers if x.residualWeeklySupplies[0] > 0 and x.residualDailySupplies[i] > 0])
                day.append(careAvailabilityScore)
                suppliers.append([x for x in householdCarers if x.weeklyTime[i][j] == 1 and x.residualWeeklySupplies[0] > 0 and x.residualDailySupplies[i] > 0])
            house.householdInformalSupplySchedule.append(day)
            house.householdInformalSuppliers.append(suppliers)
        
        children = [x for x in house.occupants if x.age > 0 and x.age < self.p['ageTeenagers']]
        teenAgers = [x for x in house.occupants if x.age >= self.p['ageTeenagers'] and x.age < self.p['workingAge'][0]]
        recipients = children+teenAgers
        house.childrenCareNeedSchedule = []
        house.childrenInNeedByHour = []
        house.childMinAge = []
        for i in range(7):
            day = []
            hourReceivers = []
            receiversMinAge = []
            for j in range(24):
                totalChildCareNeed = sum([x.unmetWeeklyNeeds[i][j] for x in receivers if x.privateChildCareNeed > 0])
                day.append(totalChildCareNeed)
                hourReceivers.append([x for x in receivers if x.unmetWeeklyNeeds[i][j] == 1 and x.privateChildCareNeed > 0])
                if len([x for x in receivers if x.unmetWeeklyNeeds[i][j] == 1]) > 0:
                    receiversMinAge.append(min([x.age for x in receivers if x.unmetWeeklyNeeds[i][j] == 1 and x.privateChildCareNeed > 0]))
                else:
                    receiversMinAge.append(-1)
            house.childrenInNeedByHour.append(hourReceivers)
            house.childrenCareNeedSchedule.append(day)
            house.childMinAge.append(receiversMinAge)
    
    def updateChildCareData(self):
        
        housesChildcareNeeds = [x for x in self.map.occupiedHouses if x.totalChilcareNeed_WNH > 0]
        for house in housesChildcareNeeds:
            householdCarers = [x for x in house.occupants if x.potentialCarer == True]
            # Update the weekly schedule information
            house.householdInformalSuppliers = []
            house.householdInformalSupplySchedule = []
            for i in range(7):
                day = []
                suppliers = []
                for j in range(24):
                    careAvailabilityScore = sum([x.weeklyTime[i][j] for x in householdCarers if x.residualWeeklySupplies[0] > 0 and x.residualDailySupplies[i] > 0])
                    day.append(careAvailabilityScore)
                    suppliers.append([x for x in householdCarers if x.weeklyTime[i][j] == 1 and x.residualWeeklySupplies[0] > 0 and x.residualDailySupplies[i] > 0])
                house.householdInformalSupplySchedule.append(day)
                house.householdInformalSuppliers.append(suppliers)
            
            children = [x for x in house.occupants if x.age > 0 and x.age < self.p['ageTeenagers']]
            teenAgers = [x for x in house.occupants if x.age >= self.p['ageTeenagers'] and x.age < self.p['workingAge'][0]]
            recipients = children+teenAgers
            house.childrenCareNeedSchedule = []
            house.childrenInNeedByHour = []
            house.childMinAge = []
            for i in range(7):
                day = []
                hourReceivers = []
                receiversMinAge = []
                for j in range(24):
                    totalChildCareNeed = sum([x.unmetWeeklyNeeds[i][j] for x in recipients])
                    day.append(totalChildCareNeed)
                    hourReceivers.append([x for x in recipients if x.unmetWeeklyNeeds[i][j] == 1])
                    if len([x for x in recipients if x.unmetWeeklyNeeds[i][j] == 1]) > 0:
                        receiversMinAge.append(min([x.age for x in recipients if x.unmetWeeklyNeeds[i][j] == 1]))
                    else:
                        receiversMinAge.append(-1)
                house.childrenInNeedByHour.append(hourReceivers)
                house.childrenCareNeedSchedule.append(day)
                house.childMinAge.append(receiversMinAge)
        
            house.weeklyChildCareCosts = []
            house.costUnits = []
            for i in range(5):
                dailyCosts = []
                for j in range(10): 
                    informalCareChildren = [x for x in house.childrenInNeedByHour[i][j] if x.residualChildcareNeed > x.publicCareSupply]
                    if len(informalCareChildren) > 0 and house.childrenCareNeedSchedule[i][j] > 0:
                        dailyCost = float(house.childrenCareNeedSchedule[i][j])*self.p['priceChildCare']
                        newChildCareCostUnit = CostUnit(i, j, dailyCost, house.childrenInNeedByHour[i][j], house.householdInformalSupplySchedule[i][j], house.householdInformalSuppliers[i][j])
                        house.costUnits.append(newChildCareCostUnit)
                        dailyCosts.append(dailyCost)
                        house.weeklyChildCareCosts.append(dailyCosts)
        
    def updateNetworkSchedule(self, hourBand, distance):
        
        if hourBand == 'ONH':
            housesChildcareNeeds = [x for x in self.map.occupiedHouses if x.totalChilcareNeed_ONH > 0]
        else:
            housesChildcareNeeds = [x for x in self.map.occupiedHouses if x.totalChilcareNeed_WNH > 0]
            
        for house in housesChildcareNeeds:
            parents = [x for x in house.occupants if x.independentStatus == True]
            suppliers = []
            if distance == 1:
                for supplier in house.d1Households:
                    carers = [x for x in supplier.occupants if x.potentialCarer == True and x.residualWeeklySupplies[1] > 0] 
                    suppliers.extend(carers)
                schedule = [[0]*24, [0]*24, [0]*24, [0]*24, [0]*24, [0]*24, [0]*24]
                weeklySuppliers = []
                maxHourSuppliers = 0
                totalD1Supply_HB = 0
                if hourBand == 'ONH': 
                    for i in range(7):
                        dailySuppliers = []
                        for j in range(24): 
                            hourSuppliers = [x for x in suppliers if x.weeklyTime[i][j] == 1 and x.residualDailySupplies[i] > 0]
                            if len(hourSuppliers) > maxHourSuppliers:
                                maxHourSuppliers = len(hourSuppliers)
                            schedule[i][j] = len(hourSuppliers)
                            if house.childrenCareNeedSchedule[i][j] > 0 and (i > 4 or (i < 5 and j > 9)):
                                totalD1Supply_HB += len(hourSuppliers)
                            dailySuppliers.append(hourSuppliers)
                        weeklySuppliers.append(dailySuppliers)
                    house.totalD1Supply_ONH = totalD1Supply_HB
                else:
                    for i in range(7):
                        dailySuppliers = []
                        for j in range(24): 
                            hourSuppliers = [x for x in suppliers if x.weeklyTime[i][j] == 1 and x.residualDailySupplies[i] > 0]
                            if len(hourSuppliers) > maxHourSuppliers:
                                maxHourSuppliers = len(hourSuppliers)
                            schedule[i][j] = len(hourSuppliers)
                            if house.childrenCareNeedSchedule[i][j] > 0 and (i < 5 and j < 10):
                                totalD1Supply_HB += len(hourSuppliers)
                            dailySuppliers.append(hourSuppliers)
                        weeklySuppliers.append(dailySuppliers)
                    house.totalD1Supply_WNH = totalD1Supply_HB
                house.d1SuppliesSchedule = schedule
                house.d1WeeklySuppliers = weeklySuppliers
                house.maxHourSuppliers = maxHourSuppliers
            else:
                for supplier in house.d2Households:
                    carers = [x for x in supplier.occupants if x.potentialCarer == True and x.residualWeeklySupplies[2] > 0] 
                    suppliers.extend(carers)
                schedule = [[0]*24, [0]*24, [0]*24, [0]*24, [0]*24, [0]*24, [0]*24]
                weeklySuppliers = []
                maxHourSuppliers = 0
                totalD2Supply_HB = 0
                if hourBand == 'ONH': 
                    for i in range(7):
                        dailySuppliers = []
                        for j in range(24): 
                            hourSuppliers = [x for x in suppliers if x.weeklyTime[i][j] == 1 and x.residualDailySupplies[i] > 0]
                            if len(hourSuppliers) > maxHourSuppliers:
                                maxHourSuppliers = len(hourSuppliers)
                            schedule[i][j] = len(hourSuppliers)
                            if house.childrenCareNeedSchedule[i][j] > 0 and (i > 4 or (i < 5 and j > 9)):
                                totalD2Supply_HB += len(hourSuppliers)
                            dailySuppliers.append(hourSuppliers)
                        weeklySuppliers.append(dailySuppliers)
                    house.totalD2Supply_ONH = totalD2Supply_HB
                else:
                    for i in range(7):
                        dailySuppliers = []
                        for j in range(24): 
                            hourSuppliers = [x for x in suppliers if x.weeklyTime[i][j] == 1 and x.residualDailySupplies[i] > 0]
                            if len(hourSuppliers) > maxHourSuppliers:
                                maxHourSuppliers = len(hourSuppliers)
                            schedule[i][j] = len(hourSuppliers)
                            if house.childrenCareNeedSchedule[i][j] > 0 and (i < 5 and j < 10):
                                totalD2Supply_HB += len(hourSuppliers)
                            dailySuppliers.append(hourSuppliers)
                        weeklySuppliers.append(dailySuppliers)
                    house.totalD2Supply_WNH = totalD2Supply_HB
                house.d2SuppliesSchedule = schedule
                house.d2WeeklySuppliers = weeklySuppliers
                house.maxHourSuppliers = maxHourSuppliers
                
        if distance == 1:
            if hourBand == 'ONH':
                return [x for x in housesChildcareNeeds if x.totalD1Supply_ONH > 0]
            else:
                return [x for x in housesChildcareNeeds if x.totalD1Supply_WNH > 0]
        else:
            if hourBand == 'ONH':
                return [x for x in housesChildcareNeeds if x.totalD2Supply_ONH > 0]
            else:
                return [x for x in housesChildcareNeeds if x.totalD2Supply_WNH > 0]
        
    def allocateChildCare(self):
        
        print 'Doing childcare allocation....'
        

        self.costTaxFreeChildCare = 0

        receivers = [x for x in self.map.occupiedHouses if x.totalChildCareNeed > 0]
        for receiver in receivers:
            self.computeChildCareNetworkSupply(receiver)
        residualReceivers = [x for x in receivers if x.networkSupply > 0]
        
        print 'There are ' + str(len(residualReceivers)) + ' households with childcare need'
        
        while len(residualReceivers) > 0:
    
            #################    Check if transfer is done: Pre need and supply   ######################################
            preChildCareNeed = sum([x.totalChildCareNeed for x in residualReceivers])
            preNetworkSupply = sum([x.networkSupply for x in residualReceivers])
            #########################################################################################
            
            # An household is selected depending on total child care need
            childCareNeeds = [x.totalChildCareNeed for x in residualReceivers]
            
            probReceivers = [float(i)/sum(childCareNeeds) for i in childCareNeeds]
        
            receiver = np.random.choice(residualReceivers, p = probReceivers)
            
            ###    Individual check   ##########################
            preReceiverCareNeed = receiver.totalChildCareNeed
            ###########################################################
            
            case = 0
            if receiver.highPriceChildCare > 0:
            # If the receiver has childcare need more expensive than social care, it will try to satisfy it with informal care. 
            # Only if there in no enough informal care the formal care will be suppllied.
            # Therefore, the supplier will be chosen according to the informal care availability, and only if there is no informal care availability left,
            # it will be chosen according to the formal care availability.
                # Select a supplier based on availability of informal supply.
                if sum(receiver.networkInformalSupplies) > 0:
                    # A supplier is selected based on informal care availability
                    probSuppliers = [i/sum(receiver.networkInformalSupplies) for i in receiver.networkInformalSupplies]
                    supplier = np.random.choice(receiver.suppliers, p = probSuppliers)
                    case = 1
                    self.transferInformalChildCare(receiver, supplier)
                    
                elif receiver.formalChildCareSupply > 0:
                    supplier = receiver
                    # Formal supply: the supplier can only be the household itself.
                    case = 2
                    self.outOfIncomeChildCare(receiver)
                
            elif receiver.lowPriceChildCare > 0:
                # In this case, a random selection based on relative availability will be done until the ratio between 
                # the available informal care and the household's social care need is above 1, i.e. there is enough informal care
                # to satisfy the household's social care need.
                # As the ratio goes below 1, only out-of-income care will be supplied, as all the available informal care will be
                # allocated to social care.
                totalCare = sum(receiver.networkInformalSupplies) + receiver.formalChildCareSupply
                typesOfCare = ['informal care', 'formal care']
                if totalCare > 0:
                    probInformalCare = max(sum(receiver.networkInformalSupplies)-receiver.totalUnmetSocialCareNeed, 0)/totalCare
                    probs = [probInformalCare, 1.0-probInformalCare]
                    care = np.random.choice(typesOfCare, p = probs)
                    if receiver.formalChildCareSupply == 0 or care == 'informal care':
                        probSuppliers = [i/sum(receiver.networkInformalSupplies) for i in receiver.networkInformalSupplies]
                        supplier = np.random.choice(receiver.suppliers, p = probSuppliers)
                        case = self.transferInformalChildCare(receiver, supplier)
                    else:
                        supplier = receiver
                        case = 5
                        self.outOfIncomeChildCare(receiver)

            postReceiverCareNeed = receiver.totalChildCareNeed
            
            if postReceiverCareNeed >= preReceiverCareNeed:
                print case
                print 'Error: child care iteration withount allocation!'
                # sys.exit()
            
            ########################################################### 
        
            receivers = [x for x in self.map.occupiedHouses if x.totalChildCareNeed > 0]
            
            for otherReceiver in receivers:
                if otherReceiver == receiver:
                    continue
                self.updateChildCareNetworkSupply(otherReceiver, supplier, 4)
           
            residualReceivers = [x for x in receivers if x.networkSupply > 0]
            
            #################    Check if transfer is done: Post need and supply   ######################################
            
            postChildCareNeed = sum([x.totalChildCareNeed for x in residualReceivers])
            postNetworkSupply = sum([x.networkSupply for x in residualReceivers])
            
            # print [x.totalChildCareNeed for x in residualReceivers]
            
            
#            print postChildCareNeed
#            print preChildCareNeed
#            print ''
            if postChildCareNeed >= preChildCareNeed:
                print 'Error: child care iteration withount allocation!'
                # sys.exit()
                
            #########################################################################################
            
#        if self.year == 1862:
#            sys.exit()
        
    def allocateSocialCare(self):
        
        self.inHouseInformalCare = 0
        
        self.computeResidualIncomeForSocialCare() # self.computeResidualIncomeForSocialCare()
        
        # self.householdCareNetwork_netSupply()
        
        receivers = [x for x in self.map.occupiedHouses if x.totalUnmetSocialCareNeed > 0]
        for receiver in receivers:
            self.computeSocialCareNetworkSupply_W(receiver) ###  Add social care from wealth.....
            
            #######    Temporarily excluding out-of-wealth care   ##########
            # self.computeSocialCareNetworkSupply_W(receiver)
            
        residualReceivers = [x for x in receivers if x.networkSupply > 0]
        
        
        
        while len(residualReceivers) > 0:
            
            #################    Check if transfer is done: Pre need and supply   ######################################
            
            preSocialCareNeed = sum([x.totalUnmetSocialCareNeed for x in residualReceivers])
            preNetworkSupply = sum([x.networkSupply for x in residualReceivers])
            
            #########################################################################################
            
            
            socialCareNeeds = [x.totalUnmetSocialCareNeed for x in residualReceivers]
            probReceivers = [i/sum(socialCareNeeds) for i in socialCareNeeds]
            receiver = np.random.choice(residualReceivers, p = probReceivers)
            
            if self.socialCareNetwork.has_node(receiver) == False:
                self.socialCareNetwork.add_node(receiver, internalSupply = 0)
            
            ###    Individual check   ##########################
            
            preReceiverCareNeed = receiver.totalUnmetSocialCareNeed
            
            ###########################################################
            suppliersWeights = []
            for supplier in receiver.suppliers:
                indexSupplier = receiver.suppliers.index(supplier)
                informalSupply = receiver.networkInformalSupplies[indexSupplier]
                formalSocialCare = receiver.networkFormalSocialCareSupplies[indexSupplier]
                careFromWealth = 0
                if receiver == supplier:
                    careFromWealth = receiver.careSupplyFromWealth
                totalFormaCare = formalSocialCare + careFromWealth
                informalFactor = math.pow(informalSupply, self.p['betaInformalCare'])
                formalFactor = math.pow(totalFormaCare, (1-self.p['betaInformalCare']))
                suppliersWeights.append(informalFactor+formalFactor)
            
            probSuppliers = [i/sum(suppliersWeights) for i in suppliersWeights]
            
            
            supplier = np.random.choice(receiver.suppliers, p = probSuppliers)
            
            if self.socialCareNetwork.has_node(supplier) == False:
                self.socialCareNetwork.add_node(supplier, internalSupply = 0)
            
            if self.socialCareNetwork.has_edge(receiver, supplier) == False:
                self.socialCareNetwork.add_edge(receiver, supplier, careTransferred = 0)
        
            self.transferSocialCare_W(receiver, supplier) # self.transferSocialCare(receiver, supplier)
            
            ###    Individual check   ##########################
            
            postReceiverCareNeed = receiver.totalUnmetSocialCareNeed
            
            if postReceiverCareNeed >= preReceiverCareNeed:
                print 'Error: social care iteration withount allocation!'
                sys.exit()
            
            ########################################################### 
            
            receivers = [x for x in self.map.occupiedHouses if x.totalUnmetSocialCareNeed > 0]
            for otherReceiver in receivers:
                if otherReceiver == receiver:
                    continue
                self.updateSocialCareNetworkSupply_W(otherReceiver, supplier, 0) # self.updateSocialCareNetworkSupply(receiver, supplier, 0)
            residualReceivers = [x for x in receivers if x.networkSupply > 0]
            
            
            #################    Check if transfer is done: Post need and supply   ######################################
            
            postSocialCareNeed = sum([x.totalUnmetSocialCareNeed for x in residualReceivers])
            postNetworkSupply = sum([x.networkSupply for x in residualReceivers])
        
            if postSocialCareNeed >= preSocialCareNeed:
                print 'Error: social care iteration withount allocation!'
                # sys.exit()
                
            #########################################################################################
    
    
    def allocateSocialCare_Ind(self):
        
        self.inHouseInformalCare = 0
        
        self.computeResidualIncomeForSocialCare()
        
        receivers = [x for x in self.pop.livingPeople if x.unmetSocialCareNeed > 0]
        for receiver in receivers:
            self.computeSocialCareNetworkSupply_Ind(receiver)
        residualReceivers = [x for x in receivers if x.networkSupply > 0]
        
        while len(residualReceivers) > 0:
            
            #################    Check if transfer is done: Pre need and supply   ######################################
            
            preSocialCareNeed = sum([x.unmetSocialCareNeed for x in residualReceivers])
            preNetworkSupply = sum([x.networkSupply for x in residualReceivers])
            
            #########################################################################################
            
            # Sample a care reciever with a probability proportional to unmet care need
            socialCareNeeds = [x.unmetSocialCareNeed for x in residualReceivers]
            probReceivers = [i/sum(socialCareNeeds) for i in socialCareNeeds]
            receiver = np.random.choice(residualReceivers, p = probReceivers)
            
            if self.socialCareNetwork.has_node(receiver) == False:
                self.socialCareNetwork.add_node(receiver, internalSupply = 0)
            
            ###    Individual check   ##########################
            preReceiverCareNeed = receiver.unmetSocialCareNeed
            ###########################################################
            
            suppliersWeights = list(receiver.weightedTotalSupplies)
            potentialSuppliers = list(receiver.suppliers)
            suppliersWeights.append(receiver.careSupplyFromWealth)
            potentialSuppliers.append(receiver)
            
            probSuppliers = [i/sum(suppliersWeights) for i in suppliersWeights]
            supplier = np.random.choice(potentialSuppliers, p = probSuppliers)
            
            if self.socialCareNetwork.has_node(supplier) == False:
                self.socialCareNetwork.add_node(supplier, internalSupply = 0)
            
            if self.socialCareNetwork.has_edge(receiver, supplier) == False:
                self.socialCareNetwork.add_edge(receiver, supplier, careTransferred = 0)
        
            self.transferSocialCare_Ind(receiver, supplier) # self.transferSocialCare(receiver, supplier)
            
            ###    Individual check   ##########################
            
            postReceiverCareNeed = receiver.unmetSocialCareNeed
            
            if postReceiverCareNeed >= preReceiverCareNeed:
                print 'Error: social care iteration withount allocation!'
                sys.exit()
            
            ########################################################### 
            
            receivers = [x for x in self.pop.livingPeople if x.unmetSocialCareNeed > 0]
            for otherReceiver in receivers:
                if otherReceiver == receiver:
                    continue
                self.updateSocialCareNetworkSupply_Ind(otherReceiver, supplier, 0) # self.updateSocialCareNetworkSupply(receiver, supplier, 0)
            residualReceivers = [x for x in receivers if x.networkSupply > 0]
            
            
            #################    Check if transfer is done: Post need and supply   ######################################
            
            postSocialCareNeed = sum([x.unmetSocialCareNeed for x in residualReceivers])
            postNetworkSupply = sum([x.networkSupply for x in residualReceivers])
        
            if postSocialCareNeed >= preSocialCareNeed:
                print 'Error: social care iteration withount allocation!'
                # sys.exit()
                
            #########################################################################################
    
    
    def transferSocialCare(self, receiver, supplier):
        
        distance = 0
        if receiver != supplier:
            distance = receiver.careNetwork[receiver][supplier]['distance']
        
        indexSupplier = receiver.suppliers.index(supplier)
        informalSupply = receiver.networkInformalSupplies[indexSupplier]
        formalSocialCare = receiver.networkFormalSocialCareSupplies[indexSupplier]
        
        # Select kind of care based on supplier availability
        kindsOfCare = ['informal care', 'out-of-income care'] # Add an 'out-of-wealth' care............
        care = 'out-of-income care'
        if supplier.town == receiver.town:
            careWeights = [informalSupply, formalSocialCare]
            careProbs = [x/sum(careWeights) for x in careWeights]
            care = np.random.choice(kindsOfCare, p = careProbs) 
        
        if care == 'informal care':
        
            household = list(supplier.occupants)
            householdCarers = [x for x in household if x.age >= self.p['ageTeenagers'] and x.maternityStatus == False]
            # If informal care is provided, it satisfies the most expensive cumulated child care need.
            for member in householdCarers:
                member.residualInformalSupply = member.residualInformalSupplies[distance]
            householdCarers.sort(key=operator.attrgetter("residualInformalSupply"), reverse=True)
            
            residualCare = min(self.p['quantumCare'], receiver.totalUnmetSocialCareNeed)
            if residualCare < 1.0:
                residualCare = 1.0
            
            careTransferred = 0
            for i in householdCarers:
                careForNeed = min(i.residualInformalSupply, residualCare)
                if careForNeed < 1.0:
                    careForNeed = 1.0
                if i in receiver.occupants and careForNeed > 0:
                    i.careForFamily = True
                i.socialWork += careForNeed
                if careForNeed > 0:
                    for j in range(4):
                        i.residualInformalSupplies[j] -= careForNeed
                        i.residualInformalSupplies[j] = float(max(int(i.residualInformalSupplies[j]), 0))
                    careTransferred += careForNeed
                    residualCare -= careForNeed
                    if residualCare <= 0:
                        break
                    
            if receiver == supplier:
                self.inHouseInformalCare += careTransferred
                
            if  receiver != supplier:
                receiver.networkSupport += careTransferred
            
            receiverOccupants = list(receiver.occupants)
            careTakers = [x for x in receiverOccupants if x.unmetSocialCareNeed > 0]
            careTakers.sort(key=operator.attrgetter("unmetSocialCareNeed"), reverse=True)
            residualCare = careTransferred
            for person in careTakers:
                personalCare = min(person.unmetSocialCareNeed, residualCare)
                person.unmetSocialCareNeed -= personalCare
                person.unmetSocialCareNeed = float(max(int(person.unmetSocialCareNeed), 0))
                person.informalSocialCareReceived += personalCare
                residualCare -= personalCare
                if residualCare <= 0:
                    break
            receiver.totalUnmetSocialCareNeed = sum([x.unmetSocialCareNeed for x in careTakers])
            receiver.informalSocialCareReceived += careTransferred
            
            self.updateSocialCareNetworkSupply(receiver, supplier, 1)
            
        elif care == 'out-of-income care':
            household = list(supplier.occupants)
            employed = [x for x in household if x.status == 'worker' and x.availableWorkingHours > 0 and x.maternityStatus == False]
            
            maxFormalCare = receiver.networkFormalSocialCareSupplies[indexSupplier]
            
            residualCare = min(self.p['quantumCare'], receiver.totalUnmetSocialCareNeed, maxFormalCare)
            if residualCare < 1.0:
                residualCare = 1.0
            
            costQuantumSocialCare = self.socialCareCost(supplier, residualCare)
            priceSocialCare = costQuantumSocialCare/residualCare
            
            if supplier.town != receiver.town or len(employed) == 0: # Only formal care is possible
                
#                print 'Supplier id: ' + str(supplier.id)
#                print 'Pre income for social care: ' + str(supplier.residualIncomeForSocialCare)
#                print 'Cost quantum social care: ' + str(costQuantumSocialCare)
                
                for j in range(4):
                    supplier.residualIncomeForSocialCare[j] -= costQuantumSocialCare
                    supplier.residualIncomeForSocialCare[j] = max(supplier.residualIncomeForSocialCare[j], 0.0)
                supplier.householdFormalSupplyCost += costQuantumSocialCare
                
                careTransferred = 0
                if len(employed) > 0:
                    employed.sort(key=operator.attrgetter("wage"), reverse=True)
                    residualCare = self.p['quantumCare']
                    for worker in employed:
                        maxCare = costQuantumSocialCare/worker.wage
                        workerCare = min(maxCare, residualCare)
                        if workerCare < 1.0:
                            workerCare = 1.0
                        worker.availableWorkingHours -= workerCare
                        worker.availableWorkingHours = float(max(int(worker.availableWorkingHours), 0))
                        careTransferred += workerCare
                        costQuantumSocialCare -= workerCare*worker.wage
                        residualCare -= workerCare
                        if residualCare <= 0:
                            break
                
                # print 'Post income for social care: ' + str(supplier.residualIncomeForSocialCare)
                
                receiverOccupants = list(receiver.occupants)                
                careTakers = [x for x in receiverOccupants if x.unmetSocialCareNeed > 0]
                careTakers.sort(key=operator.attrgetter("unmetSocialCareNeed"), reverse=True)
                residualCare = careTransferred
                for person in careTakers:
                    personalCare = min(person.unmetSocialCareNeed, residualCare)
                    person.unmetSocialCareNeed -= personalCare
                    person.unmetSocialCareNeed = float(max(int(person.unmetSocialCareNeed), 0))
                    person.formalSocialCareReceived += personalCare
                    residualCare -= personalCare
                    if residualCare <= 0:
                        break
                receiver.totalUnmetSocialCareNeed = sum([x.unmetSocialCareNeed for x in careTakers])
                receiver.formalSocialCareReceived += careTransferred
                
                self.updateSocialCareNetworkSupply(receiver, supplier, 2)
                
            else:
                # Select the worker with the lowest pay
                employed.sort(key=operator.attrgetter("wage"))
                
                carer = employed[0]
                if carer.wage > priceSocialCare: # In this case, it is more convenient to pay for formal care
                    for j in range(4):
                        supplier.residualIncomeForSocialCare[j] -= costQuantumSocialCare
                        supplier.residualIncomeForSocialCare[j] = max(supplier.residualIncomeForSocialCare[j], 0)
                    supplier.householdFormalSupplyCost += costQuantumSocialCare
                    
                    employed.sort(key=operator.attrgetter("wage"), reverse=True)
                    careToAllocate = residualCare
                    careTransferred = 0
                    for worker in employed:
                        maxCare = costQuantumSocialCare/worker.wage
                        workerCare = min(maxCare, careToAllocate)
                        if workerCare < 1.0:
                            workerCare = 1.0
                        careTransferred += workerCare
                        worker.availableWorkingHours -= workerCare
                        worker.availableWorkingHours = float(max(int(worker.availableWorkingHours), 0))
                        costQuantumSocialCare -= workerCare*worker.wage
                        careToAllocate -= workerCare
                        if careToAllocate <= 0:
                            break
                        
                    # employed[0].availableWorkingHours -= costQuantumSocialCare/employed[0].wage
                    # employed[0].availableWorkingHours = max(employed[0].availableWorkingHours, 0)
                    
                    receiverOccupants = list(receiver.occupants)
                    careTakers = [x for x in receiverOccupants if x.unmetSocialCareNeed > 0]
                    careTakers.sort(key=operator.attrgetter("unmetSocialCareNeed"), reverse=True)
                    residualCare = careTransferred
                    for person in careTakers:
                        personalCare = min(person.unmetSocialCareNeed, residualCare)
                        person.unmetSocialCareNeed -= personalCare
                        person.unmetSocialCareNeed = float(max(int(person.unmetSocialCareNeed), 0))
                        person.formalSocialCareReceived += personalCare
                        residualCare -= personalCare
                        if residualCare <= 0:
                            break
                    receiver.totalUnmetSocialCareNeed = sum([x.unmetSocialCareNeed for x in careTakers])
                    receiver.formalSocialCareReceived += careTransferred
                    
                    self.updateSocialCareNetworkSupply(receiver, supplier, 3)
                    
                else: # In this case, it is more convenient to take time off work to provide informal care.
                    print 'Case 4'
                    print 'Carer pre available working hours: ' + str(carer.availableWorkingHours)
                    
                    if receiver == supplier:
                        self.inHouseInformalCare += self.p['quantumCare']
                    
                    careTransferred = min(self.p['quantumCare'], carer.availableWorkingHours)
                    if careTransferred == 0:
                        print 'No residual working hours in carer'
                        sys.exit()
                    if careTransferred < 1.0:
                        careTransferred = 1.0
                    if carer in receiver.occupants and careTransferred > 0:
                        carer.careForFamily = True
                    incomeForCare = careTransferred*carer.wage
                    carer.availableWorkingHours -= careTransferred #self.p['quantumCare']
                    carer.availableWorkingHours = float(max(0, int(carer.availableWorkingHours)))
                    carer.residualWorkingHours -= careTransferred
                    carer.residualWorkingHours = float(max(0, int(carer.residualWorkingHours)))
                    carer.outOfWorkSocialCare += careTransferred
                    carer.socialWork += careTransferred
                    
                    print 'Care transferred: ' + str(careTransferred)
                    print 'Carer wage: ' + str(carer.wage)
                    print 'Carer post available working hours: ' + str(carer.availableWorkingHours)
                    print 'Pre-residual Income for care (4): ' + str(supplier.residualIncomeForSocialCare)
                    
                    for j in range(4):
                        supplier.residualIncomeForSocialCare[j] -= incomeForCare
                        supplier.residualIncomeForSocialCare[j] = max(supplier.residualIncomeForSocialCare[j], 0)
                        
                    print 'Post-residual Income for care (4): ' + str(supplier.residualIncomeForSocialCare)
                    
                    receiverOccupants = list(receiver.occupants)
                    careTakers = [x for x in receiverOccupants if x.unmetSocialCareNeed > 0]
                    careTakers.sort(key=operator.attrgetter("unmetSocialCareNeed"), reverse=True)
                    residualCare = careTransferred
                    for person in careTakers:
                        personalCare = min(person.unmetSocialCareNeed, residualCare)
                        person.unmetSocialCareNeed -= personalCare
                        person.unmetSocialCareNeed = float(max(int(person.unmetSocialCareNeed), 0))
                        person.informalSocialCareReceived += personalCare
                        residualCare -= personalCare
                        if residualCare <= 0:
                            break
                    receiver.totalUnmetSocialCareNeed = sum([x.unmetSocialCareNeed for x in careTakers])
                    receiver.informalSocialCareReceived += careTransferred
                    
                    self.updateSocialCareNetworkSupply(receiver, supplier, 4)
            
            
    def transferSocialCare_W(self, receiver, supplier):
        
        distance = 0
        if receiver != supplier:
            distance = receiver.careNetwork[receiver][supplier]['distance']
        
        indexSupplier = receiver.suppliers.index(supplier)
        informalSupply = receiver.networkInformalSupplies[indexSupplier]
        formalSocialCare = receiver.networkFormalSocialCareSupplies[indexSupplier]
        careFromWealth = 0
        if receiver == supplier:
            careFromWealth = receiver.careSupplyFromWealth
        totalFormaCare = formalSocialCare + careFromWealth
        informalFactor = math.pow(informalSupply, self.p['betaInformalCare'])
        formalFactor = math.pow(totalFormaCare, (1-self.p['betaInformalCare']))
        probInformalCare = informalFactor/(informalFactor+formalFactor)
        # Select kind of care based on supplier availability
        kindsOfCare = ['informal care', 'formal care'] # Add an 'out-of-wealth' care............
        care = 'out-of-income care'
        if supplier.town == receiver.town:
            # careWeights = [informalSupply, formalSocialCare, careFromWealth]
            # careProbs = [x/sum(careWeights) for x in careWeights]
            careProbs = [probInformalCare, 1-probInformalCare]
            care = np.random.choice(kindsOfCare, p = careProbs) 
        
        if care == 'informal care':
            
            
            household = list(supplier.occupants)
            householdCarers = [x for x in household if x.age >= self.p['ageTeenagers'] and x.maternityStatus == False]
            # If informal care is provided, it satisfies the most expensive cumulated child care need.
            for member in householdCarers:
                member.residualInformalSupply = member.residualInformalSupplies[distance]
            householdCarers.sort(key=operator.attrgetter("residualInformalSupply"), reverse=True)
            
            residualCare = min(self.p['quantumCare'], receiver.totalUnmetSocialCareNeed)
            if residualCare < 1.0:
                residualCare = 1.0
            
            careTransferred = 0
            for i in householdCarers:
                careForNeed = min(i.residualInformalSupply, residualCare)
                if careForNeed < 1.0:
                    careForNeed = 1.0
                if i in receiver.occupants and careForNeed > 0:
                    i.careForFamily = True
                i.socialWork += careForNeed
                if careForNeed > 0:
                    for j in range(4):
                        i.residualInformalSupplies[j] -= careForNeed
                        i.residualInformalSupplies[j] = float(max(int(i.residualInformalSupplies[j]), 0))
                    careTransferred += careForNeed
                    residualCare -= careForNeed
                    if residualCare <= 0:
                        break
                    
            if receiver == supplier:
                self.inHouseInformalCare += careTransferred
                
            if  receiver != supplier:
                receiver.networkSupport += careTransferred
                
            if receiver != supplier:
                self.socialCareNetwork[receiver][supplier]['careTransferred'] += careTransferred
            else:
                self.socialCareNetwork.node[receiver]['internalSupply'] += careTransferred
            
            receiverOccupants = list(receiver.occupants)
            careTakers = [x for x in receiverOccupants if x.unmetSocialCareNeed > 0]
            careTakers.sort(key=operator.attrgetter("unmetSocialCareNeed"), reverse=True)
            residualCare = careTransferred
            for person in careTakers:
                personalCare = min(person.unmetSocialCareNeed, residualCare)
                person.unmetSocialCareNeed -= personalCare
                person.unmetSocialCareNeed = float(max(int(person.unmetSocialCareNeed), 0))
                person.informalSocialCareReceived += personalCare
                residualCare -= personalCare
                if residualCare <= 0:
                    break
            receiver.totalUnmetSocialCareNeed = sum([x.unmetSocialCareNeed for x in careTakers])
            receiver.informalSocialCareReceived += careTransferred
            
            self.updateSocialCareNetworkSupply_W(receiver, supplier, 1)
            
            
#            if receiver == supplier:
#                self.inHouseInformalCare += self.p['quantumCare']
#                
#            household = list(supplier.occupants)
#            householdCarers = [x for x in household if x.age >= self.p['ageTeenagers'] and x.maternityStatus == False]
#            # If informal care is provided, it satisfies the most expensive cumulated child care need.
#            for member in householdCarers:
#                member.residualInformalSupply = member.residualInformalSupplies[distance]
#            householdCarers.sort(key=operator.attrgetter("residualInformalSupply"), reverse=True)
#            
#            if  receiver != supplier:
#                receiver.networkSupport += self.p['quantumCare']
#                
#            residualCare = self.p['quantumCare']
#            for i in householdCarers:
#                careForNeed = min(i.residualInformalSupply, residualCare)
#                if i in receiver.occupants and careForNeed > 0:
#                    i.careForFamily = True
#                i.socialWork += careForNeed
#                if careForNeed > 0:
#                    for j in range(4):
#                        i.residualInformalSupplies[j] -= careForNeed
#                        i.residualInformalSupplies[j] = max(i.residualInformalSupplies[j], 0)
#                    residualCare -= careForNeed
#                    if residualCare <= 0:
#                        break
#            
#            if receiver != supplier:
#                self.socialCareNetwork[receiver][supplier]['careTransferred'] += self.p['quantumCare']
#            else:
#                self.socialCareNetwork.node[receiver]['internalSupply'] += self.p['quantumCare']
#            
#            receiverOccupants = list(receiver.occupants)
#            careTakers = [x for x in receiverOccupants if x.unmetSocialCareNeed > 0]
#            careTakers.sort(key=operator.attrgetter("unmetSocialCareNeed"), reverse=True)
#            residualCare = self.p['quantumCare']
#            for person in careTakers:
#                personalCare = min(person.unmetSocialCareNeed, residualCare)
#                person.unmetSocialCareNeed -= personalCare
#                person.unmetSocialCareNeed = max(person.unmetSocialCareNeed, 0)
#                person.informalSocialCareReceived += personalCare
#                residualCare -= personalCare
#                if residualCare <= 0:
#                    break
#            receiver.totalUnmetSocialCareNeed = sum([x.unmetSocialCareNeed for x in careTakers])
#            receiver.informalSocialCareReceived += self.p['quantumCare']
#            
#            self.updateSocialCareNetworkSupply_W(receiver, supplier, 1)
            
        else: 
        
            household = list(supplier.occupants)
            employed = [x for x in household if x.status == 'worker' and x.availableWorkingHours > 0 and x.maternityStatus == False]
            
            maxFormalCare = receiver.networkFormalSocialCareSupplies[indexSupplier]
            
            residualCare = min(self.p['quantumCare'], receiver.totalUnmetSocialCareNeed, maxFormalCare)
            if residualCare < 1.0:
                residualCare = 1.0
            
            costQuantumSocialCare = self.socialCareCost(supplier, residualCare)
            priceSocialCare = costQuantumSocialCare/residualCare
            
            if supplier.town != receiver.town or len(employed) == 0 or formalSocialCare == 0: # Only formal care is possible
                kindsOfCare = ['out-of-income care', 'out-of-wealth care']
                weights = [formalSocialCare, careFromWealth]
                careProbs = [x/sum(weights) for x in weights]
                care = np.random.choice(kindsOfCare, p = careProbs)
                if care == 'out-of-income care':
                    for j in range(4):
                        supplier.residualIncomeForSocialCare[j] -= costQuantumSocialCare
                        supplier.residualIncomeForSocialCare[j] = max(supplier.residualIncomeForSocialCare[j], 0.0)
                    supplier.householdFormalSupplyCost += costQuantumSocialCare
                    
                    careTransferred = 0
                    if len(employed) > 0:
                        employed.sort(key=operator.attrgetter("wage"), reverse=True)
                        residualCare = self.p['quantumCare']
                        for worker in employed:
                            maxCare = costQuantumSocialCare/worker.wage
                            workerCare = min(maxCare, residualCare)
                            if workerCare < 1.0:
                                workerCare = 1.0
                            worker.availableWorkingHours -= workerCare
                            worker.availableWorkingHours = float(max(int(worker.availableWorkingHours), 0))
                            worker.incomeExpenses += workerCare*worker.wage
                            careTransferred += workerCare
                            costQuantumSocialCare -= workerCare*worker.wage
                            residualCare -= workerCare
                            if residualCare <= 0:
                                break
                    
                    # print 'Post income for social care: ' + str(supplier.residualIncomeForSocialCare)
                    
                    receiverOccupants = list(receiver.occupants)                
                    careTakers = [x for x in receiverOccupants if x.unmetSocialCareNeed > 0]
                    careTakers.sort(key=operator.attrgetter("unmetSocialCareNeed"), reverse=True)
                    residualCare = careTransferred
                    for person in careTakers:
                        personalCare = min(person.unmetSocialCareNeed, residualCare)
                        person.unmetSocialCareNeed -= personalCare
                        person.unmetSocialCareNeed = float(max(int(person.unmetSocialCareNeed), 0))
                        person.formalSocialCareReceived += personalCare
                        residualCare -= personalCare
                        if residualCare <= 0:
                            break
                    receiver.totalUnmetSocialCareNeed = sum([x.unmetSocialCareNeed for x in careTakers])
                    receiver.formalSocialCareReceived += careTransferred
                    
                    self.updateSocialCareNetworkSupply_W(receiver, supplier, 2)
                
                
                
#                # Sample out-of-income/out-of-wealth according to quantity
#                kindsOfCare = ['out-of-income care', 'out-of-wealth care']
#                weights = [formalSocialCare, careFromWealth]
#                careProbs = [x/sum(weights) for x in weights]
#                care = np.random.choice(kindsOfCare, p = careProbs)
#                if care == 'out-of-income care':
#                    for j in range(4):
#                        supplier.residualIncomeForSocialCare[j] -= costQuantumSocialCare
#                        supplier.residualIncomeForSocialCare[j] = max(supplier.residualIncomeForSocialCare[j], 0.0)
#                    supplier.householdFormalSupplyCost += costQuantumSocialCare
#                    
#                    if len(employed) > 0:
#                        employed.sort(key=operator.attrgetter("wage"), reverse=True)
#                        residualCare = self.p['quantumCare']
#                        for worker in employed:
#                            maxCare = costQuantumSocialCare/worker.wage
#                            workerCare = min(maxCare, residualCare)
#                            worker.availableWorkingHours -= workerCare
#                            worker.availableWorkingHours = max(worker.availableWorkingHours, 0)
#                            costQuantumSocialCare -= workerCare*worker.wage
#                        
#                            worker.careExpenses += workerCare*worker.wage
#                            
#                            residualCare -= workerCare
#                            if residualCare <= 0:
#                                break
#                    
#                    # print 'Post income for social care: ' + str(supplier.residualIncomeForSocialCare)
#                    
#                    receiverOccupants = list(receiver.occupants)                
#                    careTakers = [x for x in receiverOccupants if x.unmetSocialCareNeed > 0]
#                    careTakers.sort(key=operator.attrgetter("unmetSocialCareNeed"), reverse=True)
#                    residualCare = self.p['quantumCare']
#                    for person in careTakers:
#                        personalCare = min(person.unmetSocialCareNeed, residualCare)
#                        person.unmetSocialCareNeed -= personalCare
#                        person.unmetSocialCareNeed = max(person.unmetSocialCareNeed, 0)
#                        person.formalSocialCareReceived += personalCare
#                        residualCare -= personalCare
#                        if residualCare <= 0:
#                            break
#                    receiver.totalUnmetSocialCareNeed = sum([x.unmetSocialCareNeed for x in careTakers])
#                    receiver.formalSocialCareReceived += self.p['quantumCare']
#                    
#                    self.updateSocialCareNetworkSupply_W(receiver, supplier, 2)
                    
                else:
                    household = list(supplier.occupants)
                    householdCarers = [x for x in household if x.wealthForCare > 0]
                    householdCarers.sort(key=operator.attrgetter("wealthForCare"), reverse=True)
                    maxSupply = min(self.p['quantumCare'], sum([int(x.wealthForCare/self.p['priceSocialCare']*(1.0 - self.p['socialCareTaxFreeRate'])) for x in householdCarers]))
                    residualCare = maxSupply
                    careSupplied = 0
                    for i in householdCarers:
                        careForNeed = min(int(i.wealthForCare/self.p['priceSocialCare']*(1.0 - self.p['socialCareTaxFreeRate'])), residualCare)
                        if i in receiver.occupants and careForNeed > 0:
                            i.careForFamily = True
                        i.socialWork += careForNeed
                        if careForNeed > 0:
                            
                            i.wealthForCare -= careForNeed*self.p['priceSocialCare']
                            i.wealthForCare = max(i.wealthForCare, 0)
                            # i.financialWealth -= careForNeed*self.p['priceSocialCare']
                            # i.financialWealth = max(i.financialWealth, 0)
                            i.wealthSpentOnCare += careForNeed*self.p['priceSocialCare']
                            i.wealthPV = i.financialWealth*math.pow(1.0 + self.p['pensionReturnRate'], i.lifeExpectancy)
                            careSupplied += careForNeed
                            residualCare -= careForNeed
                            if residualCare <= 0:
                                break
                            
                    receiverOccupants = list(receiver.occupants)
                    careTakers = [x for x in receiverOccupants if x.unmetSocialCareNeed > 0]
                    careTakers.sort(key=operator.attrgetter("unmetSocialCareNeed"), reverse=True)
                    residualCare = careSupplied
                    for person in careTakers:
                        personalCare = min(person.unmetSocialCareNeed, residualCare)
                        person.unmetSocialCareNeed -= personalCare
                        person.unmetSocialCareNeed = max(person.unmetSocialCareNeed, 0)
                        person.formalSocialCareReceived += personalCare
                        residualCare -= personalCare
                        if residualCare <= 0:
                            break
                    receiver.totalUnmetSocialCareNeed = sum([x.unmetSocialCareNeed for x in careTakers])
                    receiver.formalSocialCareReceived += self.p['quantumCare']
                    
                    self.updateSocialCareNetworkSupply_W(receiver, supplier, 10)
                    
#                for j in range(4):
#                    supplier.residualIncomeForSocialCare[j] -= costQuantumSocialCare
#                    supplier.residualIncomeForSocialCare[j] = max(supplier.residualIncomeForSocialCare[j], 0.0)
#                supplier.householdFormalSupplyCost += costQuantumSocialCare
#                
#                if len(employed) > 0:
#                    employed.sort(key=operator.attrgetter("wage"), reverse=True)
#                    residualCare = self.p['quantumCare']
#                    for worker in employed:
#                        maxCare = costQuantumSocialCare/worker.wage
#                        workerCare = min(maxCare, residualCare)
#                        worker.availableWorkingHours -= workerCare
#                        worker.availableWorkingHours = max(worker.availableWorkingHours, 0)
#                        costQuantumSocialCare -= workerCare*worker.wage
#                        residualCare -= workerCare
#                        if residualCare <= 0:
#                            break
#             
#                receiverOccupants = list(receiver.occupants)                
#                careTakers = [x for x in receiverOccupants if x.unmetSocialCareNeed > 0]
#                careTakers.sort(key=operator.attrgetter("unmetSocialCareNeed"), reverse=True)
#                residualCare = self.p['quantumCare']
#                for person in careTakers:
#                    personalCare = min(person.unmetSocialCareNeed, residualCare)
#                    person.unmetSocialCareNeed -= personalCare
#                    person.unmetSocialCareNeed = max(person.unmetSocialCareNeed, 0)
#                    person.formalSocialCareReceived += personalCare
#                    residualCare -= personalCare
#                    if residualCare <= 0:
#                        break
#                receiver.totalUnmetSocialCareNeed = sum([x.unmetSocialCareNeed for x in careTakers])
#                receiver.formalSocialCareReceived += self.p['quantumCare']
#                
#                self.updateSocialCareNetworkSupply_W(receiver, supplier, 2)
                
            else:
                employed.sort(key=operator.attrgetter("wage"))
                
                carer = employed[0]
                if carer.wage > priceSocialCare: # In this case, it is more convenient to pay for formal care
                    
                    # Sample out-of-income/out-of-wealth according to quantity
                    kindsOfCare = ['out-of-income care', 'out-of-wealth care']
                    weights = [formalSocialCare, careFromWealth]
                    careProbs = [x/sum(weights) for x in weights]
                    care = np.random.choice(kindsOfCare, p = careProbs)
                    if care == 'out-of-income care':
                        
                        for j in range(4):
                            supplier.residualIncomeForSocialCare[j] -= costQuantumSocialCare
                            supplier.residualIncomeForSocialCare[j] = max(supplier.residualIncomeForSocialCare[j], 0.0)
                        supplier.householdFormalSupplyCost += costQuantumSocialCare
                        
                        careTransferred = 0
                        if len(employed) > 0:
                            employed.sort(key=operator.attrgetter("wage"), reverse=True)
                            residualCare = self.p['quantumCare']
                            for worker in employed:
                                maxCare = costQuantumSocialCare/worker.wage
                                workerCare = min(maxCare, residualCare)
                                if workerCare < 1.0:
                                    workerCare = 1.0
                                worker.availableWorkingHours -= workerCare
                                worker.availableWorkingHours = float(max(int(worker.availableWorkingHours), 0))
                                worker.incomeExpenses += workerCare*worker.wage
                                careTransferred += workerCare
                                costQuantumSocialCare -= workerCare*worker.wage
                                residualCare -= workerCare
                                if residualCare <= 0:
                                    break
                        
                        # print 'Post income for social care: ' + str(supplier.residualIncomeForSocialCare)
                        
                        receiverOccupants = list(receiver.occupants)                
                        careTakers = [x for x in receiverOccupants if x.unmetSocialCareNeed > 0]
                        careTakers.sort(key=operator.attrgetter("unmetSocialCareNeed"), reverse=True)
                        residualCare = careTransferred
                        for person in careTakers:
                            personalCare = min(person.unmetSocialCareNeed, residualCare)
                            person.unmetSocialCareNeed -= personalCare
                            person.unmetSocialCareNeed = float(max(int(person.unmetSocialCareNeed), 0))
                            person.formalSocialCareReceived += personalCare
                            residualCare -= personalCare
                            if residualCare <= 0:
                                break
                        receiver.totalUnmetSocialCareNeed = sum([x.unmetSocialCareNeed for x in careTakers])
                        receiver.formalSocialCareReceived += careTransferred
                        
                        self.updateSocialCareNetworkSupply_W(receiver, supplier, 2)
                        
                        
                    
#                        for j in range(4):
#                            supplier.residualIncomeForSocialCare[j] -= costQuantumSocialCare
#                            supplier.residualIncomeForSocialCare[j] = max(supplier.residualIncomeForSocialCare[j], 0.0)
#                        supplier.householdFormalSupplyCost += costQuantumSocialCare
#                        
#                        if len(employed) > 0:
#                            employed.sort(key=operator.attrgetter("wage"), reverse=True)
#                            residualCare = self.p['quantumCare']
#                            for worker in employed:
#                                maxCare = costQuantumSocialCare/worker.wage
#                                workerCare = min(maxCare, residualCare)
#                                worker.availableWorkingHours -= workerCare
#                                worker.availableWorkingHours = max(worker.availableWorkingHours, 0)
#                                costQuantumSocialCare -= workerCare*worker.wage
#
#                                worker.careExpenses += workerCare*worker.wage
#                            
#                                residualCare -= workerCare
#                                if residualCare <= 0:
#                                    break
#                        
#                        # print 'Post income for social care: ' + str(supplier.residualIncomeForSocialCare)
#                        
#                        receiverOccupants = list(receiver.occupants)                
#                        careTakers = [x for x in receiverOccupants if x.unmetSocialCareNeed > 0]
#                        careTakers.sort(key=operator.attrgetter("unmetSocialCareNeed"), reverse=True)
#                        residualCare = self.p['quantumCare']
#                        for person in careTakers:
#                            personalCare = min(person.unmetSocialCareNeed, residualCare)
#                            person.unmetSocialCareNeed -= personalCare
#                            person.unmetSocialCareNeed = max(person.unmetSocialCareNeed, 0)
#                            person.formalSocialCareReceived += personalCare
#                            residualCare -= personalCare
#                            if residualCare <= 0:
#                                break
#                        receiver.totalUnmetSocialCareNeed = sum([x.unmetSocialCareNeed for x in careTakers])
#                        receiver.formalSocialCareReceived += self.p['quantumCare']
#                        
#                        self.updateSocialCareNetworkSupply_W(receiver, supplier, 2)
                        
                    else:
                        household = list(supplier.occupants)
                        householdCarers = [x for x in household if x.wealthForCare > 0]
                        householdCarers.sort(key=operator.attrgetter("wealthForCare"), reverse=True)
                        maxSupply = min(self.p['quantumCare'], sum([int(x.wealthForCare/self.p['priceSocialCare']*(1.0 - self.p['socialCareTaxFreeRate'])) for x in householdCarers]))
                        residualCare = maxSupply
                        careSupplied = 0
                        for i in householdCarers:
                            careForNeed = min(int(i.wealthForCare/self.p['priceSocialCare']*(1.0 - self.p['socialCareTaxFreeRate'])), residualCare)
                            if i in receiver.occupants and careForNeed > 0:
                                i.careForFamily = True
                            i.socialWork += careForNeed
                            if careForNeed > 0:
                                
                                i.wealthForCare -= careForNeed*self.p['priceSocialCare']
                                i.wealthForCare = max(i.wealthForCare, 0)
                                # i.financialWealth -= careForNeed*self.p['priceSocialCare']
                                # i.financialWealth = max(i.financialWealth, 0)
                                i.wealthSpentOnCare += careForNeed*self.p['priceSocialCare']
                                i.wealthPV = i.financialWealth*math.pow(1.0 + self.p['pensionReturnRate'], i.lifeExpectancy)
                                careSupplied += careForNeed
                                residualCare -= careForNeed
                                if residualCare <= 0:
                                    break
                                
                        receiverOccupants = list(receiver.occupants)
                        careTakers = [x for x in receiverOccupants if x.unmetSocialCareNeed > 0]
                        careTakers.sort(key=operator.attrgetter("unmetSocialCareNeed"), reverse=True)
                        residualCare = careSupplied
                        for person in careTakers:
                            personalCare = min(person.unmetSocialCareNeed, residualCare)
                            person.unmetSocialCareNeed -= personalCare
                            person.unmetSocialCareNeed = max(person.unmetSocialCareNeed, 0)
                            person.formalSocialCareReceived += personalCare
                            residualCare -= personalCare
                            if residualCare <= 0:
                                break
                        receiver.totalUnmetSocialCareNeed = sum([x.unmetSocialCareNeed for x in careTakers])
                        receiver.formalSocialCareReceived += self.p['quantumCare']
                        
                        self.updateSocialCareNetworkSupply_W(receiver, supplier, 10)
                    
                    
                        
                        

#                    for j in range(4):
#                        supplier.residualIncomeForSocialCare[j] -= costQuantumSocialCare
#                        supplier.residualIncomeForSocialCare[j] = max(supplier.residualIncomeForSocialCare[j], 0)
#                    supplier.householdFormalSupplyCost += costQuantumSocialCare
#                    
#                    employed.sort(key=operator.attrgetter("wage"), reverse=True)
#                    residualCare = self.p['quantumCare']
#                    for worker in employed:
#                        maxCare = costQuantumSocialCare/worker.wage
#                        workerCare = min(maxCare, residualCare)
#                        worker.availableWorkingHours -= workerCare
#                        worker.availableWorkingHours = max(worker.availableWorkingHours, 0)
#                        costQuantumSocialCare -= workerCare*worker.wage
#                        residualCare -= workerCare
#                        if residualCare <= 0:
#                            break
#                    
#                    receiverOccupants = list(receiver.occupants)
#                    careTakers = [x for x in receiverOccupants if x.unmetSocialCareNeed > 0]
#                    careTakers.sort(key=operator.attrgetter("unmetSocialCareNeed"), reverse=True)
#                    residualCare = self.p['quantumCare']
#                    for person in careTakers:
#                        personalCare = min(person.unmetSocialCareNeed, residualCare)
#                        person.unmetSocialCareNeed -= personalCare
#                        person.unmetSocialCareNeed = max(person.unmetSocialCareNeed, 0)
#                        person.formalSocialCareReceived += personalCare
#                        residualCare -= personalCare
#                        if residualCare <= 0:
#                            break
#                    receiver.totalUnmetSocialCareNeed = sum([x.unmetSocialCareNeed for x in careTakers])
#                    receiver.formalSocialCareReceived += self.p['quantumCare']
#                    
#                    self.updateSocialCareNetworkSupply_W(receiver, supplier, 3)
                    
                else: # In this case, it is more convenient to take time off work to provide informal care: out-of-income
#                    print 'Case 4'
#                    print 'Carer pre available working hours: ' + str(carer.availableWorkingHours)
                    
                    if receiver == supplier:
                        self.inHouseInformalCare += self.p['quantumCare']
                    
                    careTransferred = min(self.p['quantumCare'], carer.availableWorkingHours)
                    if careTransferred == 0:
                        print 'No residual working hours in carer'
                        sys.exit()
                    if carer in receiver.occupants and careTransferred > 0:
                        carer.careForFamily = True
                    incomeForCare = careTransferred*carer.wage
                    carer.availableWorkingHours -= careTransferred #self.p['quantumCare']
                    carer.availableWorkingHours = max(0, carer.availableWorkingHours)
                    carer.residualWorkingHours -= careTransferred
                    carer.residualWorkingHours = max(0, carer.residualWorkingHours)
                    carer.outOfWorkSocialCare += careTransferred
                    carer.socialWork += careTransferred
                    
                    
                    if receiver != supplier:
                        self.socialCareNetwork[receiver][supplier]['careTransferred'] += careTransferred
                    else:
                        self.socialCareNetwork.node[receiver]['internalSupply'] += careTransferred
#                    print 'Care transferred: ' + str(careTransferred)
#                    print 'Carer wage: ' + str(carer.wage)
#                    print 'Carer post available working hours: ' + str(carer.availableWorkingHours)
#                    print 'Pre-residual Income for care (4): ' + str(supplier.residualIncomeForSocialCare)
                    
                    for j in range(4):
                        supplier.residualIncomeForSocialCare[j] -= incomeForCare
                        supplier.residualIncomeForSocialCare[j] = max(supplier.residualIncomeForSocialCare[j], 0)
                        
#                    print 'Post-residual Income for care (4): ' + str(supplier.residualIncomeForSocialCare)
                    
                    receiverOccupants = list(receiver.occupants)
                    careTakers = [x for x in receiverOccupants if x.unmetSocialCareNeed > 0]
                    careTakers.sort(key=operator.attrgetter("unmetSocialCareNeed"), reverse=True)
                    residualCare = careTransferred
                    for person in careTakers:
                        personalCare = min(person.unmetSocialCareNeed, residualCare)
                        person.unmetSocialCareNeed -= personalCare
                        person.unmetSocialCareNeed = max(person.unmetSocialCareNeed, 0)
                        person.informalSocialCareReceived += personalCare
                        residualCare -= personalCare
                        if residualCare <= 0:
                            break
                    receiver.totalUnmetSocialCareNeed = sum([x.unmetSocialCareNeed for x in careTakers])
                    receiver.informalSocialCareReceived += self.p['quantumCare']
                    
                    self.updateSocialCareNetworkSupply_W(receiver, supplier, 4)
                    
#        else: # Out-of-wealth care
#            household = list(supplier.occupants)
#            householdCarers = [x for x in household if x.wealthForCare > 0]
#            householdCarers.sort(key=operator.attrgetter("wealthForCare"), reverse=True)
#            maxSupply = min(self.p['quantumCare'], sum([int(x.wealthForCare/self.p['priceSocialCare']) for x in householdCarers]))
#            residualCare = maxSupply
#            careSupplied = 0
#            for i in householdCarers:
#                careForNeed = min(int(i.wealthForCare/self.p['priceSocialCare']), residualCare)
#                if i in receiver.occupants and careForNeed > 0:
#                    i.careForFamily = True
#                i.socialWork += careForNeed
#                if careForNeed > 0:
#                    
#                    i.wealthForCare -= careForNeed*self.p['priceSocialCare']
#                    i.wealthForCare = max(i.wealthForCare, 0)
#                    i.financialWealth -= careForNeed*self.p['priceSocialCare']
#                    i.financialWealth = max(i.financialWealth, 0)
#                    i.wealthSpentOnCare += careForNeed*self.p['priceSocialCare']
#                    i.wealthPV = i.financialWealth*math.pow(1.0 + self.p['pensionReturnRate'], i.lifeExpectancy)
#                    careSupplied += careForNeed
#
#                    residualCare -= careForNeed
#                    if residualCare <= 0:
#                        break
#                    
#            receiverOccupants = list(receiver.occupants)
#            careTakers = [x for x in receiverOccupants if x.unmetSocialCareNeed > 0]
#            careTakers.sort(key=operator.attrgetter("unmetSocialCareNeed"), reverse=True)
#            residualCare = careSupplied
#            for person in careTakers:
#                personalCare = min(person.unmetSocialCareNeed, residualCare)
#                person.unmetSocialCareNeed -= personalCare
#                person.unmetSocialCareNeed = max(person.unmetSocialCareNeed, 0)
#                person.formalSocialCareReceived += personalCare
#                residualCare -= personalCare
#                if residualCare <= 0:
#                    break
#            receiver.totalUnmetSocialCareNeed = sum([x.unmetSocialCareNeed for x in careTakers])
#            receiver.formalSocialCareReceived += self.p['quantumCare']
#            
#            self.updateSocialCareNetworkSupply_W(receiver, supplier, 10)
                    
    def transferSocialCare_Ind(self, receiver, supplier):
        
        if receiver != supplier:
            # In this case, care is provided with resources from people other than the care receiver
            distance = receiver.careNetwork[receiver][supplier]['distance']
            indexSupplier = receiver.suppliers.index(supplier)
            informalSupply = receiver.networkInformalSupplies[indexSupplier]
            formalSocialCare = receiver.networkFormalSocialCareSupplies[indexSupplier]

            informalFactor = math.pow(informalSupply, self.p['betaInformalCare'])
            formalFactor = math.pow(formalSocialCare, self.p['betaFormalCare'])
            probInformalCare = informalFactor/(informalFactor+formalFactor)
            # Select kind of care based on supplier availability
            care = 'formal care'
            if supplier.house.town == receiver.house.town:
                # careWeights = [informalSupply, formalSocialCare, careFromWealth]
                # careProbs = [x/sum(careWeights) for x in careWeights]
                careProbs = [probInformalCare, 1-probInformalCare]
                care = np.random.choice(['informal care', 'formal care'], p = careProbs) 
            
            if care == 'informal care':
            
                household = list(supplier.house.occupants)
                householdCarers = [x for x in household if x.age >= self.p['ageTeenagers'] and x.maternityStatus == False]
                # If informal care is provided, it satisfies the most expensive cumulated child care need.
                for member in householdCarers:
                    member.residualInformalSupply = member.residualInformalSupplies[distance]
                householdCarers.sort(key=operator.attrgetter("residualInformalSupply"), reverse=True)
                
                residualCare = min(self.p['quantumCare'], receiver.unmetSocialCareNeed)
                if residualCare < 1.0:
                    residualCare = 1.0
                
                careTransferred = 0
                for i in householdCarers:
                    careForNeed = min(i.residualInformalSupply, residualCare)
                    if careForNeed < 1.0:
                        careForNeed = 1.0
                    if i in receiver.house.occupants and careForNeed > 0:
                        i.careForFamily = True
                    i.socialWork += careForNeed
                    if careForNeed > 0:
                        for j in range(4):
                            i.residualInformalSupplies[j] -= careForNeed
                            i.residualInformalSupplies[j] = float(max(int(i.residualInformalSupplies[j]), 0))
                        careTransferred += careForNeed
                        residualCare -= careForNeed
                        if residualCare <= 0:
                            break
                        
                if receiver.house.id == supplier.house.id:
                    self.inHouseInformalCare += careTransferred
                    
                if  receiver.house.id != supplier.house.id:
                    receiver.house.networkSupport += careTransferred
                    
                if receiver != supplier:
                    self.socialCareNetwork[receiver][supplier]['careTransferred'] += careTransferred
                else:
                    self.socialCareNetwork.node[receiver]['internalSupply'] += careTransferred

                receiver.unmetSocialCareNeed -= careTransferred
                receiver.unmetSocialCareNeed = float(max(int(receiver.unmetSocialCareNeed), 0))
                receiver.informalSocialCareReceived += careTransferred
                receiver.house.informalSocialCareReceived += careTransferred
                
                self.updateSocialCareNetworkSupply_Ind(receiver, supplier, 1)
                
            else: # Out-of-income care. Could be formal or informal: if different town, only formal; otherwise, depends on lowest wage
                household = list(supplier.house.occupants)
                employed = [x for x in household if x.status == 'worker' and x.availableWorkingHours > 0 and x.maternityStatus == False]
                notWorkingEarners = [x for x in household if x.income > 0 and x.status != 'worker']
                
                maxFormalCare = receiver.networkFormalSocialCareSupplies[indexSupplier]
                
                residualCare = min(self.p['quantumCare'], receiver.unmetSocialCareNeed, maxFormalCare)
                if residualCare < 1.0:
                    residualCare = 1.0
                
                costQuantumSocialCare = self.socialCareCost(supplier, residualCare)
                priceSocialCare = costQuantumSocialCare/residualCare
                
                if supplier.house.town != receiver.house.town or len(employed) == 0: # Only formal care is possible
                    for j in range(4):
                        supplier.house.residualIncomeForSocialCare[j] -= costQuantumSocialCare
                        supplier.house.residualIncomeForSocialCare[j] = max(supplier.house.residualIncomeForSocialCare[j], 0.0)
                    supplier.house.householdFormalSupplyCost += costQuantumSocialCare
                    
                    # careTransferred = residualCare
                    residualCost = costQuantumSocialCare
                    careTransferred = 0
                    if len(notWorkingEarners) > 0:
                        careTransferred = 0
                        notWorkingEarners.sort(key=operator.attrgetter("residualIncome"), reverse=True)
                        for notWorking in notWorkingEarners:
                            if residualCost > notWorking.residualIncome:
                                residualCost -= notWorking.residualIncome
                                memberCareContribution = (notWorking.residualIncome/costQuantumSocialCare)*residualCare
                                careTransferred += memberCareContribution
                                residualCare -= memberCareContribution
                                notWorking.incomeExpenses += notWorking.residualIncome
                                notWorking.residualIncome = 0
                            else:
                                notWorking.residualIncome -= residualCost
                                memberCareContribution = (residualCost/costQuantumSocialCare)*residualCare
                                careTransferred += memberCareContribution
                                residualCare -= memberCareContribution
                                notWorking.residualIncome = max(notWorking.residualIncome, 0.0)
                                notWorking.incomeExpenses += residualCost
                                residualCost = 0
                                break
                    
                    if len(employed) > 0:
                        if residualCare > 0:
                            employed.sort(key=operator.attrgetter("wage"), reverse=True)
                            for worker in employed:
                                maxCare = residualCost/worker.wage
                                workerCare = min(maxCare, residualCare)
                                if workerCare < 1.0:
                                    workerCare = 1.0
                                worker.availableWorkingHours -= workerCare
                                worker.availableWorkingHours = float(max(int(worker.availableWorkingHours), 0))
                                worker.incomeExpenses += workerCare*worker.wage
                                careTransferred += workerCare
                                residualCost -= workerCare*worker.wage
                                residualCare -= workerCare
                                if residualCare <= 0:
                                    break
                                
                    careTransferred = math.ceil(careTransferred)
                    # print 'Post income for social care: ' + str(supplier.residualIncomeForSocialCare)
                    receiver.unmetSocialCareNeed -= careTransferred
                    receiver.unmetSocialCareNeed = float(max(int(receiver.unmetSocialCareNeed), 0))
                    receiver.formalSocialCareReceived += careTransferred
                    receiver.house.formalSocialCareReceived += careTransferred
                    
                    self.updateSocialCareNetworkSupply_Ind(receiver, supplier, 2)
                    
                else:
                    # Select the worker with the lowest pay
                    employed.sort(key=operator.attrgetter("wage"))
                    
                    carer = employed[0]
                    if carer.wage > priceSocialCare: # In this case, it is more convenient to pay for formal care
                        for j in range(4):
                            supplier.house.residualIncomeForSocialCare[j] -= costQuantumSocialCare
                            supplier.house.residualIncomeForSocialCare[j] = max(supplier.house.residualIncomeForSocialCare[j], 0)
                        supplier.house.householdFormalSupplyCost += costQuantumSocialCare
                        
                        residualCost = costQuantumSocialCare
                        careTransferred = 0
                        if len(notWorkingEarners) > 0:
                            careTransferred = 0
                            notWorkingEarners.sort(key=operator.attrgetter("residualIncome"), reverse=True)
                            for notWorking in notWorkingEarners:
                                if residualCost > notWorking.residualIncome:
                                    residualCost -= notWorking.residualIncome
                                    memberCareContribution = (notWorking.residualIncome/costQuantumSocialCare)*residualCare
                                    careTransferred += memberCareContribution
                                    residualCare -= memberCareContribution
                                    notWorking.incomeExpenses += notWorking.residualIncome
                                    notWorking.residualIncome = 0
                                else:
                                    notWorking.residualIncome -= residualCost
                                    memberCareContribution = (residualCost/costQuantumSocialCare)*residualCare
                                    careTransferred += memberCareContribution
                                    residualCare -= memberCareContribution
                                    notWorking.residualIncome = max(notWorking.residualIncome, 0.0)
                                    notWorking.incomeExpenses += residualCost
                                    residualCost = 0
                                    break
                        
                        
                        # Workers working hours must be commited to earn salary to buy formal care, so are not available for informal care.
                        if residualCare > 0:
                            employed.sort(key=operator.attrgetter("wage"), reverse=True)
                            careToAllocate = residualCare
                            for worker in employed:
                                maxCare = residualCost/worker.wage
                                workerCare = min(maxCare, careToAllocate)
                                if workerCare < 1.0:
                                    workerCare = 1.0
                                careTransferred += workerCare
                                worker.availableWorkingHours -= workerCare
                                worker.availableWorkingHours = float(max(int(worker.availableWorkingHours), 0))
                                worker.incomeExpenses += workerCare*worker.wage
                                residualCost -= workerCare*worker.wage
                                careToAllocate -= workerCare
                                if careToAllocate <= 0:
                                    break
                                
                        careTransferred = math.ceil(careTransferred)
                        receiver.unmetSocialCareNeed -= careTransferred
                        receiver.unmetSocialCareNeed = float(max(int(receiver.unmetSocialCareNeed), 0))
                        receiver.formalSocialCareReceived += careTransferred
                        receiver.house.formalSocialCareReceived += careTransferred
                        
                        self.updateSocialCareNetworkSupply_Ind(receiver, supplier, 3)
                        
                    else: # In this case, it is more convenient to take time off work to provide informal care.
#                        print 'Case 4'
#                        print 'Carer pre available working hours: ' + str(carer.availableWorkingHours)
                        
                        
                        
                        careTransferred = min(self.p['quantumCare'], carer.availableWorkingHours, receiver.unmetSocialCareNeed)
                        if careTransferred == 0:
                            print 'No residual working hours in carer'
                            sys.exit()
                        if careTransferred < 1.0:
                            careTransferred = 1.0
                        if carer in receiver.house.occupants and careTransferred > 0:
                            carer.careForFamily = True
                        incomeForCare = careTransferred*carer.wage
                        carer.availableWorkingHours -= careTransferred #self.p['quantumCare']
                        carer.availableWorkingHours = float(max(0, int(carer.availableWorkingHours)))
                        carer.residualWorkingHours -= careTransferred
                        carer.residualWorkingHours = float(max(0, int(carer.residualWorkingHours)))
                        carer.outOfWorkSocialCare += careTransferred
                        carer.socialWork += careTransferred
                        carer.house.outOfWorkSocialCare += careTransferred
                        
                        if receiver.house.id == supplier.house.id:
                            self.inHouseInformalCare += careTransferred
                        
#                        print 'Care transferred: ' + str(careTransferred)
#                        print 'Carer wage: ' + str(carer.wage)
#                        print 'Carer post available working hours: ' + str(carer.availableWorkingHours)
#                        print 'Pre-residual Income for care (4): ' + str(supplier.house.residualIncomeForSocialCare)
                        
                        for j in range(4):
                            supplier.house.residualIncomeForSocialCare[j] -= incomeForCare
                            supplier.house.residualIncomeForSocialCare[j] = max(supplier.house.residualIncomeForSocialCare[j], 0)
                            
                        # print 'Post-residual Income for care (4): ' + str(supplier.house.residualIncomeForSocialCare)
                        careTransferred = math.ceil(careTransferred)
                        receiver.unmetSocialCareNeed -= careTransferred
                        receiver.unmetSocialCareNeed = float(max(int(receiver.unmetSocialCareNeed), 0))
                        receiver.informalSocialCareReceived += careTransferred
                        receiver.house.informalSocialCareReceived += careTransferred
                        
                        self.updateSocialCareNetworkSupply_Ind(receiver, supplier, 4)
                
                
        else: # In this case, formal care is paid with the receiver's wealth
            careSupplied = min(receiver.careSupplyFromWealth, self.p['quantumCare'], receiver.unmetSocialCareNeed)
            receiver.wealthForCare -= careSupplied*self.p['priceSocialCare']*(1.0 - self.p['socialCareTaxFreeRate'])
            receiver.wealthForCare = max(receiver.wealthForCare, 0)
            receiver.wealthSpentOnCare += careSupplied*self.p['priceSocialCare']*(1.0 - self.p['socialCareTaxFreeRate'])

            receiver.unmetSocialCareNeed -= careSupplied
            receiver.unmetSocialCareNeed = max(receiver.unmetSocialCareNeed, 0)
            receiver.formalSocialCareReceived += careSupplied
            receiver.house.formalSocialCareReceived += careSupplied
            self.updateSocialCareNetworkSupply_Ind(receiver, supplier, 10)
            
        
    def socialCareCost(self, person, care):
        house = person.house
        availableIncomeByTaxBand = self.updateIncomeByTaxBand(house)
        prices = [self.p['priceSocialCare']*(1.0 - self.p['socialCareTaxFreeRate'])*(1.0-x*self.p['taxBreakRate']) for x in self.p['taxationRates']]
        cost = 0
        residualCare = care
        for i in range(len(availableIncomeByTaxBand)):
            # house.incomeByTaxBand[i] needs to be updated at every transfer of formal care, net of time off work and total formal care cost
            if availableIncomeByTaxBand[i]/prices[i] > residualCare:
                cost += residualCare*prices[i]
                availableIncomeByTaxBand[i] -= residualCare*prices[i]
                break
            else:
                cost += availableIncomeByTaxBand[i]
                residualCare -= availableIncomeByTaxBand[i]/prices[i]
                availableIncomeByTaxBand[i] = 0
        return cost    
        
        
    def computeResidualIncomeForSocialCare(self):
        
        # incomeShares = []
        
        for house in self.map.occupiedHouses:
            
            household = list(house.occupants)
            householdCarers = [x for x in household if x.age >= self.p['ageTeenagers'] and x.maternityStatus == False]
            employed = [x for x in householdCarers if x.status == 'worker']
            
            employed = [x for x in householdCarers if x.status == 'worker']
            for worker in employed:
                worker.potentialIncome = worker.residualWorkingHours*worker.wage
                
            incomes = [x.potentialIncome for x in householdCarers]
            incomes.extend([x.income for x in household if x.status == 'retired'])
            netIncome = sum(incomes) - house.householdFormalSupplyCost
            netIncome = max(netIncome, 0)
            incomePerCapita = netIncome/float(len(household))
            
            house.householdInformalSupply = []
            for i in range(4):
                house.householdInformalSupply.append(sum([x.residualInformalSupplies[i] for x in householdCarers]))
    
            taxBands = len(self.p['taxBrackets'])
            house.incomeByTaxBand = [0]*taxBands
            house.incomeByTaxBand[-1] = sum(incomes)
            for i in range(taxBands-1):
                for income in incomes:
                    if income > self.p['taxBrackets'][i]:
                        bracket = income-self.p['taxBrackets'][i]
                        house.incomeByTaxBand[i] += bracket
                        house.incomeByTaxBand[-1] -= bracket
                        incomes[incomes.index(income)] -= bracket
            
#            ############  Check Variable  ############################
#            if self.year == self.p['getCheckVariablesAtYear']:
#                self.perCapitaHouseholdIncome.append(incomePerCapita)
#            ##########################################################
     
            incomeForCareShare_D0 = 1.0 - 1.0/math.exp(self.p['incomeCareParam']*incomePerCapita)
            
            # incomeShares.append(incomeForCareShare_D0)
            
            incomeForCareShare_D1 = (1.0 - 1.0/math.exp(self.p['incomeCareParam']*incomePerCapita))*self.p['formalCareDiscountFactor']
            
            # print incomeForCareShare_D1
            
            residualIncomeForCare_D0 = netIncome*incomeForCareShare_D0
            residualIncomeForCare_D1 = netIncome*incomeForCareShare_D1
            
            house.residualIncomeForSocialCare = [residualIncomeForCare_D0, residualIncomeForCare_D1, 0, 0]
            
            # Compute total supply of household
            house.totalSupplies = [self.updateFormalSocialCareSupplies(house, x) for x in [0, 1]]
            house.totalSupplies.extend([0,0])
            
            for j in range(4):
                house.totalSupplies[j] += sum([x.residualInformalSupplies[j] for x in house.occupants])
                
            # Add supply from wealth
            peopleWithNeed = [x for x in house.occupants if x.wealthForCare > 0]
            house.totalLifeExpectancy = sum([x.lifeExpectancy for x in peopleWithNeed])
            house.careSupplyFromWealth = 0
            if house.totalLifeExpectancy > 0:
                house.wealthForCare = sum([x.wealthForCare for x in peopleWithNeed])
                # weeklyWealth = sum([x.wealthForCare for x in peopleWithNeed]) # /float(52*house.totalLifeExpectancy)
                house.totalSupplies[0] += float(int(house.wealthForCare/self.p['priceSocialCare']*(1.0 - self.p['socialCareTaxFreeRate'])))
                
            house.netCareSupply = house.totalSupplies[0] - house.totalSocialCareNeed
            
            
    
    def computeSocialCareNetworkSupply(self, house):
        
        town = house.town
        house.networkSupply = 0
        house.networkTotalSupplies = []
        house.weightedTotalSupplies = []
        house.networkInformalSupplies = []
        house.networkFormalSocialCareSupplies = []
        
        # Care from wealth
        peopleWithNeed = [x for x in house.occupants if x.wealthForCare > 0]
        house.totalLifeExpectancy = sum([x.lifeExpectancy for x in peopleWithNeed])
        house.careSupplyFromWealth = 0
        if house.totalLifeExpectancy > 0:
            house.wealthForCare = sum([x.wealthForCare for x in peopleWithNeed])
            weeklyWealth = sum([x.financialWealth for x in peopleWithNeed])/float(52*house.totalLifeExpectancy)
            house.careSupplyFromWealth = float(int(weeklyWealth/self.p['priceSocialCare']*(1.0 - self.p['socialCareTaxFreeRate'])))
            
        house.networkSupply += house.careSupplyFromWealth
        
        house.suppliers = [house]
        house.suppliers.extend(list(house.careNetwork.neighbors(house)))
        
        for supplier in house.suppliers:
            distance = 0
            if supplier != house:
                distance = house.careNetwork[house][supplier]['distance']
                
#            careFromWealth = 0
#            if supplier == house:
#                careFromWealth = house.careSupplyFromWealth
#            weightedCareFromWealth = careFromWealth*self.p['weightCareFromWealth']
            
            # Informal Care Supplies
            household = list(supplier.occupants)
            householdCarers = [x for x in household if x.age >= self.p['ageTeenagers'] and x.maternityStatus == False]
            # householdInformalSupply = []
            # for i in range(4):
                # householdInformalSupply.append(sum([x.residualInformalSupplies[i] for x in householdCarers]))
            informalSupply = 0
            if supplier.town == town:
                informalSupply = float(sum([x.residualInformalSupplies[distance] for x in householdCarers]))
            house.networkInformalSupplies.append(informalSupply)
            house.networkSupply += informalSupply
            weightedInformalSupply = informalSupply
            
            # Formal Social Care supply
            maxFormalSocialCare = float(self.updateFormalSocialCareSupplies(supplier, distance))
            house.networkFormalSocialCareSupplies.append(maxFormalSocialCare)
            weightedMaxFormalSocialCare = maxFormalSocialCare
            
            house.networkTotalSupplies.append(informalSupply+maxFormalSocialCare)
            house.weightedTotalSupplies.append(weightedInformalSupply+weightedMaxFormalSocialCare)
            house.networkSupply += maxFormalSocialCare
            
    def computeSocialCareNetworkSupply_W(self, house):
        
        town = house.town
        house.networkSupply = 0
        house.networkTotalSupplies = []
        house.weightedTotalSupplies = []
        house.networkInformalSupplies = []
        house.networkFormalSocialCareSupplies = []
        # Care from wealth
        peopleWithNeed = [x for x in house.occupants if x.wealthForCare > 0]
        house.totalLifeExpectancy = sum([x.lifeExpectancy for x in peopleWithNeed])
        house.careSupplyFromWealth = 0
        if house.totalLifeExpectancy > 0:
            house.wealthForCare = sum([x.wealthForCare for x in peopleWithNeed])
            # weeklyWealth = sum([x.wealthForCare for x in peopleWithNeed])/float(52*house.totalLifeExpectancy)
            house.careSupplyFromWealth = float(int(house.wealthForCare/self.p['priceSocialCare']*(1.0 - self.p['socialCareTaxFreeRate'])))
            
        house.networkSupply += house.careSupplyFromWealth
        
        house.suppliers = [house]
        house.suppliers.extend(list(house.careNetwork.neighbors(house)))
        
        for supplier in house.suppliers:
            distance = 0
            if supplier != house:
                distance = house.careNetwork[house][supplier]['distance']
                
            careFromWealth = 0
            if supplier == house:
                careFromWealth = house.careSupplyFromWealth
            weightedCareFromWealth = careFromWealth #*self.p['weightCareFromWealth']
            
            # Informal Care Supplies
            household = list(supplier.occupants)
            householdCarers = [x for x in household if x.age >= self.p['ageTeenagers'] and x.maternityStatus == False]
            # householdInformalSupply = []
            # for i in range(4):
                # householdInformalSupply.append(sum([x.residualInformalSupplies[i] for x in householdCarers]))
            informalSupply = 0
            if supplier.town == town:
                informalSupply = float(sum([x.residualInformalSupplies[distance] for x in householdCarers]))
            house.networkInformalSupplies.append(informalSupply)
            house.networkSupply += informalSupply
            weightedInformalSupply = informalSupply
            
            # Formal Social Care supply
            maxFormalSocialCare = float(self.updateFormalSocialCareSupplies(supplier, distance))
            house.networkFormalSocialCareSupplies.append(maxFormalSocialCare)
            weightedMaxFormalSocialCare = maxFormalSocialCare #*self.p['weightCareFromIncome']
            
            house.networkTotalSupplies.append(informalSupply+maxFormalSocialCare+careFromWealth)
            house.weightedTotalSupplies.append(weightedInformalSupply+weightedMaxFormalSocialCare+weightedCareFromWealth)
            house.networkSupply += maxFormalSocialCare
            
    def computeSocialCareNetworkSupply_Ind(self, person):
        
        town = person.house.town
        person.networkSupply = 0
        person.networkTotalSupplies = []
        person.weightedTotalSupplies = []
        person.networkInformalSupplies = []
        person.networkFormalSocialCareSupplies = []
        
        person.suppliers = list(person.careNetwork.neighbors(person))
        
#        print person.id
#        print [x.id for x in person.suppliers]
        
        person.careSupplyFromWealth = float(int(person.wealthForCare/self.p['priceSocialCare']*(1.0 - self.p['socialCareTaxFreeRate'])))
        careFromWealth = person.careSupplyFromWealth
        # weightedCareFromWealth = careFromWealth*self.p['weightCareFromWealth']
        person.networkSupply += person.careSupplyFromWealth
        
        for supplier in person.suppliers:
            
            supplierTown = supplier.house.town
            distance = person.careNetwork[person][supplier]['distance']
                
            # Informal Care Supplies
            household = list(supplier.house.occupants)
            householdCarers = [x for x in household if x.age >= self.p['ageTeenagers'] and x.maternityStatus == False]
            # householdInformalSupply = []
            # for i in range(4):
                # householdInformalSupply.append(sum([x.residualInformalSupplies[i] for x in householdCarers]))
            informalSupply = 0
            if supplierTown == town:
                informalSupply = float(sum([x.residualInformalSupplies[distance] for x in householdCarers]))
            person.networkInformalSupplies.append(informalSupply)
            person.networkSupply += informalSupply
            weightedInformalSupply = informalSupply
            
            # Formal Social Care supply
            maxFormalSocialCare = float(self.updateFormalSocialCareSupplies_Ind(supplier, distance))
            person.networkFormalSocialCareSupplies.append(maxFormalSocialCare)
            
            informalFactor = math.pow(informalSupply, self.p['betaInformalCare'])
            formalFactor = math.pow(maxFormalSocialCare, self.p['betaFormalCare'])
            
            # weightedMaxFormalSocialCare = maxFormalSocialCare*self.p['weightCareFromIncome']
            
            person.networkTotalSupplies.append(informalSupply+maxFormalSocialCare)
            person.weightedTotalSupplies.append(informalFactor+formalFactor)
            person.networkSupply += maxFormalSocialCare
        
    def updateSocialCareNetworkSupply(self, house, supplier, n):
        
        town = house.town
        
        oldSupply = house.networkSupply
        oldInformalSupplies = list(house.networkInformalSupplies)
        oldFormalCareSupplies = list(house.networkFormalSocialCareSupplies)
        oldTotalSupplies = list(house.networkTotalSupplies)
        oldWealthForCare = house.wealthForCare
        oldCareFromWealth = house.careSupplyFromWealth
        
        peopleWithNeed = [x for x in house.occupants if x.wealthForCare > 0]
        
#        if n == 10:
#            print 'Wealth for care; ' + str([x.wealthForCare for x in peopleWithNeed])
        
        # totalLifeExpectancy = sum([x.lifeExpectancy for x in peopleWithNeed])
        house.careSupplyFromWealth = 0
        if house.totalLifeExpectancy > 0:
            house.wealthForCare = sum([x.wealthForCare for x in peopleWithNeed])
            weeklyWealth = sum([x.financialWealth for x in peopleWithNeed])/float(52*house.totalLifeExpectancy)
            house.careSupplyFromWealth = float(int(weeklyWealth/self.p['priceSocialCare']*(1.0 - self.p['socialCareTaxFreeRate'])))
            
#            if n == 10:
#                print 'House life expectancy: ' + str(house.totalLifeExpectancy)
#                print 'Weekly wealth: ' + str(weeklyWealth)
#                print 'Care supply from wealth: ' + str(house.careSupplyFromWealth)
#                print 'Old wealth for care: ' + str(oldWealthForCare)
#                print 'New wealth for care: ' + str(house.wealthForCare)
                
        
        if supplier in house.suppliers:
        
            supplierIndex = house.suppliers.index(supplier)
            
#            careFromWealth = 0
#            if supplier == house:
#                careFromWealth = house.careSupplyFromWealth
#            weightedCareFromWealth = careFromWealth*self.p['weightCareFromWealth']
        
            distance = 0
            if supplier != house:
                distance = house.careNetwork[house][supplier]['distance']
                
            household = list(supplier.occupants)
            householdCarers = [x for x in household if x.age >= self.p['ageTeenagers'] and x.maternityStatus == False]
            householdInformalSupply = []
            for i in range(4):
                householdInformalSupply.append(sum([x.residualInformalSupplies[i] for x in householdCarers]))
            informalSupply = 0
            if supplier.town == town:
                informalSupply = float(sum([x.residualInformalSupplies[distance] for x in householdCarers]))
            house.networkInformalSupplies[supplierIndex] = informalSupply
            weightedInformalSupply = informalSupply
            
            # print 'Updating formal care supply...'
            maxFormalSocialCare = float(self.updateFormalSocialCareSupplies(supplier, distance))
            weightedMaxFormalSocialCare = maxFormalSocialCare
    
            house.networkFormalSocialCareSupplies[supplierIndex] = maxFormalSocialCare
            
            house.networkTotalSupplies[supplierIndex] = informalSupply+maxFormalSocialCare
            house.weightedTotalSupplies[supplierIndex] = weightedInformalSupply+weightedMaxFormalSocialCare
            
            house.networkSupply = sum(house.networkTotalSupplies)
            
            if house.networkSupply >= oldSupply and n != 0 and n != 10:
                print 'Error: social care supply did not decrease!'
                print 'Case: ' + str(n)
                print house.id
                print [x.id for x in house.suppliers]
                print supplierIndex
                print supplier.id
                print ''
                print oldSupply
                print house.networkSupply
                print ''
                print oldInformalSupplies
                print house.networkInformalSupplies
                print ''
                print oldFormalCareSupplies
                print house.networkFormalSocialCareSupplies
                print ''
                print oldCareFromWealth
                print house.careSupplyFromWealth
                print ''
                print oldTotalSupplies
                print house.networkTotalSupplies
                
                sys.exit()
    
    def updateSocialCareNetworkSupply_W(self, house, supplier, n):
        
        town = house.town
        
        oldSupply = house.networkSupply
        oldInformalSupplies = list(house.networkInformalSupplies)
        oldFormalCareSupplies = list(house.networkFormalSocialCareSupplies)
        oldTotalSupplies = list(house.networkTotalSupplies)
        oldWealthForCare = house.wealthForCare
        oldCareFromWealth = house.careSupplyFromWealth
        
        peopleWithNeed = [x for x in house.occupants if x.wealthForCare > 0]
        
#        if n == 10:
#            print 'Wealth for care; ' + str([x.wealthForCare for x in peopleWithNeed])
        
        # totalLifeExpectancy = sum([x.lifeExpectancy for x in peopleWithNeed])
        house.careSupplyFromWealth = 0
        if house.totalLifeExpectancy > 0:
            house.wealthForCare = sum([x.wealthForCare for x in peopleWithNeed])
            weeklyWealth = sum([x.wealthForCare for x in peopleWithNeed]) # /float(52*house.totalLifeExpectancy)
            house.careSupplyFromWealth = float(int(house.wealthForCare/self.p['priceSocialCare']*(1.0 - self.p['socialCareTaxFreeRate'])))
            
#            if n == 10:
#                print 'House life expectancy: ' + str(house.totalLifeExpectancy)
#                print 'Weekly wealth: ' + str(weeklyWealth)
#                print 'Care supply from wealth: ' + str(house.careSupplyFromWealth)
#                print 'Old wealth for care: ' + str(oldWealthForCare)
#                print 'New wealth for care: ' + str(house.wealthForCare)
                
        
        if supplier in house.suppliers:
        
            supplierIndex = house.suppliers.index(supplier)
            
            careFromWealth = 0
            if supplier == house:
                careFromWealth = house.careSupplyFromWealth
            weightedCareFromWealth = careFromWealth #*self.p['weightCareFromWealth']
        
            distance = 0
            if supplier != house:
                distance = house.careNetwork[house][supplier]['distance']
                
            household = list(supplier.occupants)
            householdCarers = [x for x in household if x.age >= self.p['ageTeenagers'] and x.maternityStatus == False]
            householdInformalSupply = []
            for i in range(4):
                householdInformalSupply.append(sum([x.residualInformalSupplies[i] for x in householdCarers]))
            informalSupply = 0
            if supplier.town == town:
                informalSupply = float(sum([x.residualInformalSupplies[distance] for x in householdCarers]))
            house.networkInformalSupplies[supplierIndex] = informalSupply
            weightedInformalSupply = informalSupply
            
            # print 'Updating formal care supply...'
            maxFormalSocialCare = float(self.updateFormalSocialCareSupplies(supplier, distance))
            weightedMaxFormalSocialCare = maxFormalSocialCare #*self.p['weightCareFromIncome']
    
            house.networkFormalSocialCareSupplies[supplierIndex] = maxFormalSocialCare
            
            house.networkTotalSupplies[supplierIndex] = informalSupply+maxFormalSocialCare+careFromWealth
            house.weightedTotalSupplies[supplierIndex] = weightedInformalSupply+weightedMaxFormalSocialCare+weightedCareFromWealth
            
            house.networkSupply = sum(house.networkTotalSupplies)
            
            if house.networkSupply >= oldSupply and n != 0 and n != 10:
                print 'Error: social care supply did not decrease!'
                print 'Case: ' + str(n)
                print house.id
                print [x.id for x in house.suppliers]
                print supplierIndex
                print supplier.id
                print ''
                print oldSupply
                print house.networkSupply
                print ''
                print oldInformalSupplies
                print house.networkInformalSupplies
                print ''
                print oldFormalCareSupplies
                print house.networkFormalSocialCareSupplies
                print ''
                print oldCareFromWealth
                print house.careSupplyFromWealth
                print ''
                print oldTotalSupplies
                print house.networkTotalSupplies
                
                sys.exit()    
        
    def updateSocialCareNetworkSupply_Ind(self, receiver, supplier, n):
        
        town = receiver.house.town
        
        oldSupply = receiver.networkSupply
        oldInformalSupplies = list(receiver.networkInformalSupplies)
        oldFormalCareSupplies = list(receiver.networkFormalSocialCareSupplies)
        oldTotalSupplies = list(receiver.networkTotalSupplies)
        oldWealthForCare = receiver.wealthForCare
        oldCareFromWealth = receiver.careSupplyFromWealth
        
        receiver.careSupplyFromWealth = float(int(receiver.wealthForCare/self.p['priceSocialCare']*(1.0 - self.p['socialCareTaxFreeRate'])))
        careFromWealth = receiver.careSupplyFromWealth
        # weightedCareFromWealth = careFromWealth*self.p['weightCareFromWealth']
        receiver.networkSupply = receiver.careSupplyFromWealth
        
        houses = [x.house for x in receiver.suppliers]
        if supplier.house in houses:
            
            supplier = [x for x in receiver.suppliers if x.house.id == supplier.house.id][0]
            supplierIndex = receiver.suppliers.index(supplier)
            
            # suppliers = list(receiver.careNetwork.neighbors(receiver))
            
#            if supplier not in suppliers:
#                print 'Error: supplier not in network!'
#                print receiver.id
#                print [x.id for x in receiver.suppliers]
#                print [x.id for x in suppliers]
#                sys.exit()
            
            distance = receiver.careNetwork[receiver][supplier]['distance']
                
            household = list(supplier.house.occupants)
            householdCarers = [x for x in household if x.age >= self.p['ageTeenagers'] and x.maternityStatus == False]
            householdInformalSupply = []
            for i in range(4):
                householdInformalSupply.append(sum([x.residualInformalSupplies[i] for x in householdCarers]))
            informalSupply = 0
            if supplier.house.town == town:
                informalSupply = float(sum([x.residualInformalSupplies[distance] for x in householdCarers]))
            receiver.networkInformalSupplies[supplierIndex] = informalSupply
            weightedInformalSupply = informalSupply
            
            # print 'Updating formal care supply...'
            maxFormalSocialCare = float(self.updateFormalSocialCareSupplies_Ind(supplier, distance))
            weightedMaxFormalSocialCare = maxFormalSocialCare #*self.p['weightCareFromIncome']
    
            receiver.networkFormalSocialCareSupplies[supplierIndex] = maxFormalSocialCare
            
            informalFactor = math.pow(informalSupply, self.p['betaInformalCare'])
            formalFactor = math.pow(maxFormalSocialCare, self.p['betaFormalCare'])
            
            receiver.networkTotalSupplies[supplierIndex] = informalSupply+maxFormalSocialCare
            receiver.weightedTotalSupplies[supplierIndex] = informalFactor+formalFactor
            
        receiver.networkSupply += sum(receiver.networkTotalSupplies)
        
        # receiver.networkSupply += receiver.careSupplyFromWealth
         
        if receiver.networkSupply >= oldSupply and n != 0 and n != 10:
            print 'Error: social care supply did not decrease!'
            print 'Case: ' + str(n)
            print receiver.id
            print [x.id for x in receiver.suppliers]
            print supplierIndex
            print supplier.id
            print ''
            print oldSupply
            print receiver.networkSupply
            print ''
            print oldInformalSupplies
            print receiver.networkInformalSupplies
            print ''
            print oldFormalCareSupplies
            print receiver.networkFormalSocialCareSupplies
            print ''
            print oldCareFromWealth
            print receiver.careSupplyFromWealth
            print ''
            print oldTotalSupplies
            print receiver.networkTotalSupplies
            
            sys.exit() 
                
    def transferInformalChildCare(self, receiver, supplier):
        distance = 0
        if receiver != supplier:
            distance = receiver.careNetwork[receiver][supplier]['distance']
        
        householdCarers = [x for x in supplier.occupants if x.residualInformalSupplies[distance] > 0]
        # Sort the suppliers in order of decreasing informal supply
        totInformalSupply = 0
        for member in householdCarers:
            member.residualInformalSupply = member.residualInformalSupplies[distance]
            totInformalSupply += member.residualInformalSupply
        # Order care provider according to supply
        householdCarers.sort(key=operator.attrgetter("residualInformalSupply"), reverse=True)
        
        if totInformalSupply == 0:
            print 'Error: totInformalSupply is zero!'
            sys.exit()
       
        residualCare = min(self.p['quantumCare'], receiver.totalChildCareNeed)
        if residualCare < 1.0:
            residualCare = 1.0
            
        careTransferred = 0
        for i in householdCarers:
            careForNeed = min(i.residualInformalSupply, residualCare)
            if careForNeed < 1.0:
                careForNeed = 1.0
            i.childWork += careForNeed
            if careForNeed > 0:
                careTransferred += careForNeed
                for j in range(4):
                    i.residualInformalSupplies[j] -= careForNeed
                    i.residualInformalSupplies[j] = float(max(int(i.residualInformalSupplies[j]), 0))
                residualCare -= careForNeed
                if residualCare <= 0:
                    break
                
        if  receiver != supplier:
            receiver.networkSupport += careTransferred
            
        if careTransferred == 0:
            print 'Informal care'
            print 'Residual care: ' + str(residualCare)
            print 'Error: care transferred is equal to zero!'
            sys.exit()
        
        # Decrease the child care needs of the receiver
        children = [x for x in receiver.occupants if x.age > 0 and x.age < self.p['ageTeenagers'] and x.unmetChildCareNeed > 0]
        # preChildCareNeed = list([x.unmetChildCareNeed for x in children])
        
        # Because of the one-to-many nature of child care, the informal care provided decreases the care need of all the household's children
        for child in children:
            child.informalChildCareReceived += min(careTransferred, child.unmetChildCareNeed)
            child.unmetChildCareNeed -= careTransferred
            child.unmetChildCareNeed = float(max(int(child.unmetChildCareNeed), 0))
        # postChildCareNeed = list([x.unmetChildCareNeed for x in children])
        receiver.totalChildCareNeed = sum([x.unmetChildCareNeed for x in children])
        receiver.informalChildCareReceived += careTransferred

        self.updateChildCareNeeds(receiver)
        
        self.updateChildCareNetworkSupply(receiver, supplier, 1)
        
    def outOfIncomeChildCare(self, receiver):

        employed = [x for x in receiver.occupants if x.status == 'worker' and x.availableWorkingHours > 0 and x.maternityStatus == False]
        children = [x for x in receiver.occupants if x.age > 0 and x.age < self.p['ageTeenagers'] and x.unmetChildCareNeed > 0]
        notWorkingEarners = [x for x in receiver.occupants if x.income > 0 and x.status != 'worker']
        maxFormalSupply = receiver.formalChildCareSupply
        careSupply = min(self.p['quantumCare'], receiver.totalChildCareNeed, maxFormalSupply)
        
        if careSupply == 0:
            print 'Error: careSupply OOI is equal to zero!'
            print ''
            sys.exit()
        
        if careSupply < 1.0:
            careSupply = 1.0
        
        potentialCostChildCare = self.computePotentialFormalChildCareCost(receiver, careSupply)
        valueInformalChildCare = potentialCostChildCare/careSupply
        
        if len(employed) > 0:
            employed.sort(key=operator.attrgetter("wage"))
            carer = employed[0]
            
        if len(employed) == 0 or carer.wage >= valueInformalChildCare: # In this case, it is more convenient to pay formal care 
           
            costQuantumChildCare = self.childCareCost(children, careSupply)
            receiver.residualIncomeForChildCare -= costQuantumChildCare
            receiver.residualIncomeForChildCare = max(receiver.residualIncomeForChildCare, 0)
            receiver.householdFormalSupplyCost += costQuantumChildCare
            
            totalCareResources = receiver.residualIncomeForChildCare + receiver.householdFormalSupplyCost
            income = self.computeHouseholdIncome(receiver)
            
            #Reducing the available working hours for informal care
            careTransferred = 0
            residualCost = costQuantumChildCare
            residualCare = careSupply
            if len(employed) > 0:
                if len(notWorkingEarners) > 0:
                    notWorkingEarners.sort(key=operator.attrgetter("residualIncome"), reverse=True)
                    for notWorking in notWorkingEarners:
                        if residualCost > notWorking.residualIncome:
                            residualCost -= notWorking.residualIncome
                            memberCareContribution = (notWorking.residualIncome/costQuantumChildCare)*careSupply
                            careTransferred += memberCareContribution
                            residualCare -= memberCareContribution
                            notWorking.incomeExpenses += notWorking.residualIncome
                            notWorking.residualIncome = 0
                        else:
                            notWorking.residualIncome -= residualCost
                            memberCareContribution = (residualCost/costQuantumChildCare)*careSupply
                            careTransferred += memberCareContribution
                            residualCare -= memberCareContribution
                            notWorking.residualIncome = max(notWorking.residualIncome, 0.0)
                            notWorking.incomeExpenses += residualCost
                            residualCost = 0
                            break
                        
                if residualCost > 0:
                    employed.sort(key=operator.attrgetter("wage"), reverse=True)
                    for worker in employed:
                        maxCare = residualCost/worker.wage
                        workerCare = min(maxCare, residualCare)
                        if workerCare < 1.0:
                            workerCare = 1.0
                        careTransferred += workerCare
                        worker.incomeExpenses += workerCare*worker.wage
                        residualCost -= workerCare*worker.wage
                        worker.availableWorkingHours -= workerCare
                        worker.availableWorkingHours = float(max(int(worker.availableWorkingHours), 0))
                        residualCare -= workerCare
                        if residualCare <= 0:
                            break
            else:
                # Change this: only the not-working agent with the highets residual income will provide care
                careTransferred = careSupply
                notWorkingEarners.sort(key=operator.attrgetter("residualIncome"), reverse=True)
                for notWorking in notWorkingEarners:
                    if residualCost > notWorking.residualIncome:
                        residualCost -= notWorking.residualIncome
                        notWorking.incomeExpenses += notWorking.residualIncome
                        notWorking.residualIncome = 0
                    else:
                        notWorking.residualIncome -= residualCost
                        notWorking.residualIncome = max(notWorking.residualIncome, 0.0)
                        notWorking.incomeExpenses += residualCost
                        residualCost = 0
                        break
                #employed.sort(key=operator.attrgetter("wage"), reverse=True)
                #employed[0].availableWorkingHours -= costQuantumChildCare/employed[0].wage
                #employed[0].availableWorkingHours = max(employed[0].availableWorkingHours, 0)
                
            formalChildCares = [x.formalChildCareReceived for x in children if x.formalChildCareReceived < self.p['childcareTaxFreeCap']]
            if len(formalChildCares) > 0:
                children.sort(key=operator.attrgetter("formalChildCareReceived"))
            else:
                children.sort(key=operator.attrgetter("unmetChildCareNeed"), reverse = True)
            
            if careTransferred == 0:
                print 'Out-of-income formal care'
                print 'Error: care transferred is equal to zero!'
                sys.exit()
            
            residualCare = careTransferred
            for child in children:
                careForChild = min(child.unmetChildCareNeed, residualCare)
                if careForChild > 0:
                    child.formalChildCareReceived += careForChild
                    child.unmetChildCareNeed -= careForChild
                    child.unmetChildCareNeed = float(max(int(child.unmetChildCareNeed), 0))
                residualCare -= careForChild
                if residualCare <= 0:
                    break
            receiver.totalChildCareNeed = sum([x.unmetChildCareNeed for x in children])
            receiver.formalChildCareReceived += careTransferred 
            receiver.formalChildCareCost += costQuantumChildCare
            
            self.updateChildCareNeeds(receiver)

            self.updateChildCareNetworkSupply(receiver, receiver, 2)
            
        else: # In this case, it is more convenient to take time off work to provide informal care
           
            incomeBefore = self.computeHouseholdIncome(receiver)
            # print 'Household income before: ' + str(incomeBefore)
            
            residualIncomeBefore = receiver.residualIncomeForChildCare
            # print 'Residual Income for child care before: ' + str(residualIncomeBefore)
            
            childcareExpense = receiver.householdFormalSupplyCost
            # print 'Childcare expense: ' + str(childcareExpense)
            total = residualIncomeBefore+childcareExpense
          
            # Care transferred
            careTransferred = min(careSupply, carer.availableWorkingHours)
            if careTransferred < 1.0:
                careTransferred = 1.0
            # print 'Care transferred: ' + str(careTransferred)
            if careTransferred == 0:
                print 'Out-of-income informal care'
                print 'Error: care transferred is equal to zero!'
                sys.exit()
            
            carer.availableWorkingHours -= careTransferred #self.p['quantumCare']
            carer.availableWorkingHours = float(max(0, int(carer.availableWorkingHours)))
            carer.residualWorkingHours -= careTransferred
            carer.residualWorkingHours = float(max(0, int(carer.residualWorkingHours)))
            carer.outOfWorkChildCare += careTransferred
            carer.childWork += careTransferred #self.p['quantumCare']
            receiver.residualIncomeForChildCare -= carer.wage*careTransferred #self.p['quantumCare']
            # print 'Miised income for care: ' + str(carer.wage*self.p['quantumCare'])
            
            receiver.residualIncomeForChildCare = max(receiver.residualIncomeForChildCare, 0)
           
            incomeAfter = self.computeHouseholdIncome(receiver)
            # print 'Household income After: ' + str(incomeAfter)
            
            residualIncomeAfter = receiver.residualIncomeForChildCare
            # print 'Residual Income for child care After: ' + str(residualIncomeAfter)
            
            total = residualIncomeAfter+childcareExpense
            
            totalCareResources = receiver.residualIncomeForChildCare + receiver.householdFormalSupplyCost
            income = self.computeHouseholdIncome(receiver)
            
            children = [x for x in receiver.occupants if x.age > 0 and x.age < self.p['ageTeenagers'] and x.unmetChildCareNeed > 0]
            for child in children:
                child.informalChildCareReceived += min(careTransferred, child.unmetChildCareNeed)
                child.unmetChildCareNeed -= careTransferred
                child.unmetChildCareNeed = float(max(int(child.unmetChildCareNeed), 0))
            receiver.totalChildCareNeed = sum([x.unmetChildCareNeed for x in children])
            receiver.informalChildCareReceived = sum([x.informalChildCareReceived for x in children])
            
            self.updateChildCareNeeds(receiver)

            self.updateChildCareNetworkSupply(receiver, receiver, 3)
        
        
    def transferChildCare(self, receiver, supplier, index):
        case = -1
        # Transfer quantim of care: decide who trasfers which kind of care (informal or formal) to whom
        informalSupply = receiver.networkInformalSupplies[index]
        formalChildCare = 0
        if receiver == supplier:
            formalChildCare = receiver.formalChildCareSupply
        # Select kind of care based on supplier availability
        kindsOfCare = ['informal care', 'formal care']
        care = 'formal care'
        if supplier.town == receiver.town:
            careWeights = [informalSupply, formalChildCare]
            careProbs = [x/sum(careWeights) for x in careWeights]
            care = np.random.choice(kindsOfCare, p = careProbs) 
        
        # If 'informal care' is selected: informal care provider are sorted in decreasing order.
        # Their supply is used to satisfy the most expensive care need.
        if care == 'informal care':
            case = 3
#            print 'tranfer child care: informal (3)'
#            print informalSupply
            self.transferInformalChildCare(receiver, supplier)
        else:
            case = 4
#            print 'tranfer child care: formal (4)'
#            print formalChildCare
        # Both formal and out-of-income informal care are possible: choice depends on price of child care and lowest wage.
            self.outOfIncomeChildCare(receiver)
            
        return case
    
    def childCareCost(self, children, careSupply):
        children.sort(key=operator.attrgetter("formalChildCareReceived"))
        cost = 0
        residualCare = careSupply
        for child in children:
            careForChild = min(child.unmetChildCareNeed, residualCare)
            if careForChild + child.formalChildCareReceived <= self.p['childcareTaxFreeCap']:
                cost += self.p['priceChildCare']*(1.0-self.p['childCareTaxFreeRate'])*careForChild
                self.costTaxFreeChildCare += self.p['priceChildCare']*self.p['childCareTaxFreeRate']*careForChild
            else:
                if child.formalChildCareReceived >= self.p['childcareTaxFreeCap']:
                    cost += self.p['priceChildCare']*careForChild
                else:
                    discountedCare = self.p['childcareTaxFreeCap']-child.formalChildCareReceived
                    cost1 = discountedCare*self.p['priceChildCare']*(1.0-self.p['childCareTaxFreeRate'])
                    self.costTaxFreeChildCare += discountedCare*self.p['priceChildCare']*self.p['childCareTaxFreeRate']
                    fullPriceCare = careForChild - discountedCare
                    cost2 = fullPriceCare*self.p['priceChildCare']
                    cost += (cost1 + cost2)
            residualCare -= careForChild
            if residualCare <= 0:
                break
        return cost
    
    def computeHouseholdIncome(self, house):
        householdCarers = [x for x in house.occupants if x.age >= self.p['ageTeenagers'] and x.maternityStatus == False]
        employed = [x for x in householdCarers if x.status == 'worker']
        householdIncome = 0
        for worker in employed:
            worker.income = worker.residualWorkingHours*worker.wage
            
        householdIncome = sum([x.income for x in householdCarers])

        return householdIncome
        
        
    def updateChildCareNeeds(self, house):
        children = [x for x in house.occupants if x.age > 0 and x.age < self.p['ageTeenagers']]
        children.sort(key=operator.attrgetter("unmetChildCareNeed"))
        residualNeeds = [x.unmetChildCareNeed for x in children]
        
        # print 'Unmet child care needs: ' + str(residualNeeds)
        
        marginalNeeds = []
        numbers = []
        toSubtract = 0
        for need in residualNeeds:
            marginalNeed = need-toSubtract
            marginalNeed = max(marginalNeed, 0)
            if marginalNeed > 0:
                marginalNeeds.append(marginalNeed)
                num = len([x for x in residualNeeds if x >= need])
                numbers.append(num)                
                toSubtract = need
        house.childCareNeeds = marginalNeeds
        house.cumulatedChildren = numbers
        
        # print 'House child care needs: ' + str(house.childCareNeeds)
        
        prices = []
        residualCare = 0
        cumulatedCare = 0
        for i in range(len(numbers)):
            cost = 0
            residualCare = house.childCareNeeds[i]
            for child in children[-numbers[i]:]:
                if cumulatedCare + residualCare + child.formalChildCareReceived <= self.p['childcareTaxFreeCap']:
                    cost += self.p['priceChildCare']*(1.0-self.p['childCareTaxFreeRate'])*residualCare
                else:
                    if child.formalChildCareReceived + cumulatedCare >= self.p['childcareTaxFreeCap']:
                        cost += self.p['priceChildCare']*residualCare
                    else:
                        discountedCare = self.p['childcareTaxFreeCap'] - (child.formalChildCareReceived + cumulatedCare)
                        cost1 = discountedCare*self.p['priceChildCare']*(1.0-self.p['childCareTaxFreeRate'])
                        fullPriceCare = residualCare - discountedCare
                        cost2 = fullPriceCare*self.p['priceChildCare']
                        cost += (cost1 + cost2)
            cumulatedCare += house.childCareNeeds[i]
            prices.append(cost/house.childCareNeeds[i])
        house.childCarePrices = prices
        
        # print 'House child care prices: ' + str(house.childCarePrices)
        
        house.highPriceChildCare = 0
        house.lowPriceChildCare = 0
        for i in range(len(house.childCarePrices)):
            if house.childCarePrices[i] >= self.p['priceSocialCare']*(1.0 - self.p['socialCareTaxFreeRate']):
                house.highPriceChildCare += house.childCareNeeds[i]
            else:
                house.lowPriceChildCare += house.childCareNeeds[i]
        
        
        if house.totalChildCareNeed > 0 and (house.highPriceChildCare+house.lowPriceChildCare) <= 0:
            print 'Error: mismatch between total child care needs in updateChildCareNeeds'
            print house.totalChildCareNeed
            print house.childCareNeeds
            print house.childCarePrices
            print house.highPriceChildCare
            print house.lowPriceChildCare
            sys.exit()
        # print 'High price care in updateChildCare: ' + str(house.highPriceChildCare)
            
        # print 'Low price care in updateChildCare: ' + str(house.lowPriceChildCare)
                    
    def computePotentialFormalChildCareCost(self, house, careSupply):
        # How much would the household have to pay to provide the same amount of care through formal childcare as a quantum of informal care?
        cost = 0
        residualNeed = careSupply
        for i in range(len(house.childCareNeeds)):
            careForChild = min(house.childCareNeeds[i], residualNeed)
            cost += careForChild*house.childCarePrices[i]
            residualNeed -= careForChild
            if residualNeed <= 0:
                break
        return cost
        
    def computeChildCareNetworkSupply(self, house):
        
        town = house.town
        
       
        
        house.networkSupply = 0
        house.formalChildCareSupply = 0
        house.networkTotalSupplies = []
        house.networkInformalSupplies = []
        house.childCareWeights = []
        house.formalCaresRatios = []
        house.suppliers = [house]
        house.suppliers.extend(list(house.careNetwork.neighbors(house)))
        
        # Household supply
        
#        household = list(house.occupants)
#        householdCarers = [x for x in household if x.residualInformalSupplies[0] > 0]
#        informalSupply = sum([x.residualInformalSupplies[0] for x in householdCarers])
#        house.networkInformalSupplies.append(informalSupply)
#        house.formalChildCareSupply = self.updateFormalChildCareSupplies(house)
#        householdTotalSupply = informalSupply + house.formalChildCareSupply
#        house.networkTotalSupplies.append(householdTotalSupply)
#        house.networkSupply = householdTotalSupply
#        
        for supplier in house.suppliers:
            
            if supplier == house:
                household = list(house.occupants)
                householdCarers = [x for x in household if x.residualInformalSupplies[0] > 0]
                informalSupply = sum([x.residualInformalSupplies[0] for x in householdCarers])
                house.networkInformalSupplies.append(informalSupply)
                house.formalChildCareSupply = self.updateFormalChildCareSupplies(house)
                householdTotalSupply = informalSupply + house.formalChildCareSupply
                house.networkTotalSupplies.append(householdTotalSupply)
                house.networkSupply += householdTotalSupply
            else:
                distance = house.careNetwork[house][supplier]['distance']
                household = list(supplier.occupants)
                householdCarers = [x for x in household if x.residualInformalSupplies[distance] > 0]
                # Informal supply is available only if in the same town
                informalSupply = 0
                if supplier.town == town:
                    informalSupply = sum([x.residualInformalSupplies[distance] for x in householdCarers])
                house.networkInformalSupplies.append(informalSupply)
                house.networkTotalSupplies.append(informalSupply)
                house.networkSupply += informalSupply
            
    def updateChildCareNetworkSupply(self, house, supplier, n):
        
        children = [x for x in house.occupants if x.age > 0 and x.age < self.p['ageTeenagers']]
        
        
        oldSupply = house.networkSupply
        oldFormalSupply = house.formalChildCareSupply
        oldInformalSupplies = list(house.networkInformalSupplies)
        
        town = house.town
        
        if supplier in house.suppliers:
        
            supplierIndex = house.suppliers.index(supplier)
        
            distance = 0
            if supplier != house:
                distance = house.careNetwork[house][supplier]['distance']
                
            household = list(supplier.occupants)
            householdCarers = [x for x in household if x.residualInformalSupplies[distance] > 0]
            # Informal supply is available only if in the same town
            informalSupply = 0
            if supplier.town == town:
                informalSupply = sum([x.residualInformalSupplies[distance] for x in householdCarers])
            house.networkInformalSupplies[supplierIndex] = informalSupply
            house.networkTotalSupplies[supplierIndex] = informalSupply
            
            if house == supplier:
                
               #  print 'Updating formal child care supply.....'
                residualFormalChilCare = sum([max(self.p['maxFormalChildCare'] - x.formalChildCareReceived, 0) for x in children])
                house.formalChildCareSupply = min(self.updateFormalChildCareSupplies(house), residualFormalChilCare)
                house.networkTotalSupplies[supplierIndex] += house.formalChildCareSupply

            house.networkSupply = sum(house.networkTotalSupplies)
            
#            if n != 4 and n != 3:
#                if house.networkSupply >= oldSupply and house:
#                    print ''
#                    print 'Case; ' + str(n)
#                    print oldSupply
#                    print house.networkSupply
#                    print ''
#                    print oldInformalSupplies
#                    print house.networkInformalSupplies
#                    print ''
#                    print oldFormalSupply
#                    print house.formalChildCareSupply
#                    print 'Error: child supply did not change'
#                    sys.exit()
            
    
    def updateIncomeByTaxBand(self, house):
        householdCarers = [x for x in house.occupants if x.age >= self.p['ageTeenagers'] and x.maternityStatus == False]
        employed = [x for x in householdCarers if x.status == 'worker']
        householdIncome = 0
        for worker in employed:
            worker.income = worker.residualWorkingHours*worker.wage
        incomes = [x.income for x in householdCarers]
        
        taxBands = len(self.p['taxBrackets'])
        house.incomeByTaxBand = [0]*taxBands
        house.incomeByTaxBand[-1] = sum(incomes)
        for i in range(taxBands-1):
            for income in incomes:
                if income > self.p['taxBrackets'][i]:
                    bracket = income-self.p['taxBrackets'][i]
                    house.incomeByTaxBand[i] += bracket
                    house.incomeByTaxBand[-1] -= bracket
                    incomes[incomes.index(income)] -= bracket
        # Available income by tax band
        house.availableIncomeByTaxBand = house.incomeByTaxBand
        careExpense = house.householdFormalSupplyCost
        for i in range(len(house.availableIncomeByTaxBand)):
            if house.availableIncomeByTaxBand[i] > careExpense:
                house.availableIncomeByTaxBand[i] -= careExpense
                careExpense = 0
                break
            else:
                careExpense -= house.availableIncomeByTaxBand[i]
                house.availableIncomeByTaxBand[i] = 0
        return house.availableIncomeByTaxBand        
    
#    def updateFormalSocialCareSupplies(self, house, distance):
#        availableIncomeByTaxBand = list(self.updateIncomeByTaxBand(house))
#        residualIncomeForCare = house.residualIncomeForSocialCare[distance]
#        
#        # print 'residual Income for care: ' + str(residualIncomeForCare)
#        
#        # How much social care can the household buy with the residual income for care?
#        prices = [self.p['priceSocialCare']*(1.0 - self.p['socialCareTaxFreeRate'])*(1.0-x*self.p['taxBreakRate']) for x in self.p['taxationRates']]
#        incomeByTaxBand = list(availableIncomeByTaxBand)
#        totalHours = 0
#        for i in range(len(incomeByTaxBand)):
#            if residualIncomeForCare > incomeByTaxBand[i]:
#                totalHours += incomeByTaxBand[i]/prices[i]
#                residualIncomeForCare -= incomeByTaxBand[i]
#            else:
#                totalHours += residualIncomeForCare/prices[i]
#                break
#        
#        # print 'Tot hours: ' + str(totalHours)
#        
#        socialCareSupplies = round(totalHours)
#        
#        # socialCareSupplies = int((totalHours+self.p['quantumCare']/2)/self.p['quantumCare'])*self.p['quantumCare']
#        return socialCareSupplies
        
    def updateFormalSocialCareSupplies(self, house, distance):
        
        # The out-of-income social care is given by the sum of the informal social care provided by taking hours off work and the formal care paid through the
        # residual income.
        
        # availableIncomeByTaxBand = list(self.updateIncomeByTaxBand(house))
        residualIncomeForCare = house.residualIncomeForSocialCare[distance]
        workers = [x for x in house.occupants if x.status == 'worker' and x.availableWorkingHours > 0]
        workers.sort(key=operator.attrgetter("wage"))
        prices = [self.p['priceSocialCare']*(1.0 - self.p['socialCareTaxFreeRate'])*(1.0-x*self.p['taxBreakRate']) for x in self.p['taxationRates']]
        
        totHours = 0
        for worker in workers:
            if residualIncomeForCare == 0:
                break
            workerIncome = worker.availableWorkingHours*worker.wage
            for i in range(len(self.p['taxBrackets'])):
                bracket = max(workerIncome-self.p['taxBrackets'][i], 0)
                incomeForFormalCare = min(bracket, residualIncomeForCare)
                workerIncome -= incomeForFormalCare
                if prices[i] > worker.wage:
                    totHours += incomeForFormalCare/worker.wage
                else:
                    totHours += incomeForFormalCare/prices[i]
                residualIncomeForCare -= incomeForFormalCare
                residualIncomeForCare = max(residualIncomeForCare, 0)
                if residualIncomeForCare == 0:
                    break
        # print 'Tot hours: ' + str(totalHours)
        
        socialCareSupplies = int(totHours)
        
        # socialCareSupplies = int((totalHours+self.p['quantumCare']/2)/self.p['quantumCare'])*self.p['quantumCare']
        return socialCareSupplies    
    
    def updateFormalSocialCareSupplies_Ind(self, supplier, distance):
        
        # The out-of-income social care is given by the sum of the informal social care provided by taking hours off work and the formal care paid through the
        # residual income.
        house = supplier.house
        # availableIncomeByTaxBand = list(self.updateIncomeByTaxBand(house))
        residualIncomeForCare = house.residualIncomeForSocialCare[distance]
        workers = [x for x in house.occupants if x.status == 'worker' and x.availableWorkingHours > 0]
        workers.sort(key=operator.attrgetter("wage"))
        prices = [self.p['priceSocialCare']*(1.0 - self.p['socialCareTaxFreeRate'])*(1.0-x*self.p['taxBreakRate']) for x in self.p['taxationRates']]
        
        totHours = 0
        for worker in workers:
            if residualIncomeForCare == 0:
                break
            workerIncome = worker.availableWorkingHours*worker.wage
            for i in range(len(self.p['taxBrackets'])):
                bracket = max(workerIncome-self.p['taxBrackets'][i], 0)
                incomeForFormalCare = min(bracket, residualIncomeForCare)
                workerIncome -= incomeForFormalCare
                if prices[i] > worker.wage:
                    totHours += incomeForFormalCare/worker.wage
                else:
                    totHours += incomeForFormalCare/prices[i]
                residualIncomeForCare -= incomeForFormalCare
                residualIncomeForCare = max(residualIncomeForCare, 0)
                if residualIncomeForCare == 0:
                    break
        # print 'Tot hours: ' + str(totalHours)
        
        socialCareSupplies = int(totHours)
        
        # socialCareSupplies = int((totalHours+self.p['quantumCare']/2)/self.p['quantumCare'])*self.p['quantumCare']
        return socialCareSupplies

    def updateFormalChildCareSupplies(self, receiver):
        
        # residualIncomeForCare = receiver.residualIncomeForChildCare
        
        
        receiverOccupants = receiver.occupants
        notWorkingEarners = [x for x in receiverOccupants if x.income > 0 and x.status != 'worker']
        children = [x for x in receiverOccupants if x.age > 0 and x.age < self.p['ageTeenagers']]
        workers = [x for x in receiverOccupants if x.status == 'worker' and x.availableWorkingHours > 0]
        workers.sort(key=operator.attrgetter("wage"))
        availableHours = [x.availableWorkingHours for x in workers]
        wages = [x.wage for x in workers]
        
        residualNeeds = list(receiver.childCareNeeds)
       
        totHours = 0
        for i in range(len(receiver.childCareNeeds)):
            for j in range(len(workers)):
                if receiver.childCarePrices[i] > wages[j]:
                    if availableHours[j] > residualNeeds[i]:
                        totHours += residualNeeds[i]*receiver.cumulatedChildren[i]
                        availableHours[j] -= residualNeeds[i]
                        residualNeeds[i] = 0
                        break
                    else:
                        totHours += availableHours[j]*receiver.cumulatedChildren[i]
                        residualNeeds[i] -= availableHours[j]
                        availableHours[j] = 0
                        
        # The remaining income is used to provide formal child care
        residualIncomeForCare = sum([x.residualIncome for x in notWorkingEarners])
        residualIncomeForCare += sum(np.multiply(availableHours,wages))
        
        # List of residual formal child care below the tax free cap (i.e. for which the household get the discounted price)
        formalChilCareReceived = [x.formalChildCareReceived for x in children]
        
        discountedNeed = [max(self.p['childcareTaxFreeCap']-x, 0) for x in formalChilCareReceived]
        
        # Total cost of discounted child care 
        discountedCost = sum(discountedNeed)*self.p['priceChildCare']*(1.0-self.p['childCareTaxFreeRate'])
    
        if residualIncomeForCare > discountedCost:
            totHours += sum(discountedNeed)
            residualIncomeForCare -= discountedCost
            totHours += residualIncomeForCare/self.p['priceChildCare']
        else:
            totHours += residualIncomeForCare/(self.p['priceChildCare']*(1.0-self.p['childCareTaxFreeRate']))
       
        # totHours = int((totHours+self.p['quantumCare']/2)/self.p['quantumCare'])*self.p['quantumCare']   
        totHours = int(totHours)
        
        return totHours

#    def updateFormalChildCareSupplies(self, receiver):
#        
#        residualIncomeForCare = receiver.residualIncomeForChildCare
#        receiverOccupants = receiver.occupants
#        children = [x for x in receiverOccupants if x.age > 0 and x.age < self.p['ageTeenagers']]
#        formalChilCareReceived = [x.formalChildCareReceived for x in children]
#        
#        # print 'Formal child care received:' + str(formalChilCareReceived)
#        
#        discountedNeed = [max(self.p['childcareTaxFreeCap']-x, 0) for x in formalChilCareReceived]
#        
#        # print 'Discounted need: ' + str(discountedNeed)
#        
#        discountedCost = sum(discountedNeed)*self.p['priceChildCare']*(1.0-self.p['childCareTaxFreeRate'])
#        
#        # print 'Discounted Cost: ' + str(discountedCost)
#        
#        totHours = 0
#        if residualIncomeForCare > discountedCost:
#            totHours = sum(discountedNeed)
#            residualIncomeForCare -= discountedCost
#            totHours += residualIncomeForCare/self.p['priceChildCare']
#        else:
#            totHours = residualIncomeForCare/(self.p['priceChildCare']*(1.0-self.p['childCareTaxFreeRate']))
#            
#        # print 'Total formal supply hours: ' + str(totHours)
#        
#        # totHours = int((totHours+self.p['quantumCare']/2)/self.p['quantumCare'])*self.p['quantumCare']   
#        totHours = round(totHours)
#        
#        return totHours
            
    def resetCareVariables_KN(self):
        
        for house in self.map.occupiedHouses:
            
            house.careNetwork.clear()
            house.demandNetwork.clear()
            house.totalSocialCareNeed = 0
            house.totalUnmetSocialCareNeed = 0
            house.formalSocialCare = 0
            house.formalChildCare = 0
            house.costFormalSocialCare = 0
            house.costFormalChildCare = 0
            
            house.totalChildCareNeed = 0
            house.totalPriorityCareNeed = 0
            house.childCareNeeds = []
            house.childCarePrices = []
            house.highPriceChildCare = 0
            house.lowPriceChildCare = 0
            house.residualIncomeForChildCare = 0
            house.initialResidualIncomeForChildCare = 0
            house.residualIncomeForSocialCare = []
            house.householdInformalSupplies = []
            house.householdFormalSupply = []
            house.networkSupply = 0
            house.networkTotalSupplies = []
            house.networkInformalSupplies = []
            house.formalChildCareSupply = 0
            house.networkFormalSocialCareSupplies = []
            house.totalSupplies = []
            house.netCareSupply = 0
            house.childCareWeights = []
            house.formalCaresRatios = []
            house.informalChildCareReceived = 0
            house.informalSocialCareReceived = 0
            house.formalChildCareReceived = 0
            house.formalChildCareCost = 0
            house.formalSocialCareReceived = 0
            house.householdFormalSupplyCost = 0
            house.wealthForCare = 0
            house.incomeByTaxBand = []
            house.averageChildCarePrice = 0
            house.networkSupport = 0
            house.outOfWorkSocialCare = 0
            house.townAttractiveness = []
            house.netCareDemand = 0
            house.careAttractionFactor = 0
            house.newOccupancy = False
            
            house.totalCareNeed = 0
            house.residualCareNeed_PreFormal = 0
            house.residualCareNeed_PostFormal = 0
            
            
            for person in house.occupants:
                person.careNetwork.clear()
                person.potentialCarer = False
                person.hoursChildCareDemand = 0
                person.netChildCareDemand = 0
                person.unmetChildCareNeed = 0
                person.hoursSocialCareDemand = 0
                person.unmetSocialCareNeed = 0
                person.informalChildCareReceived = 0
                person.formalChildCareReceived = 0
                person.publicChildCareContribution = 0
                person.informalSocialCareReceived = 0
                person.formalSocialCareReceived = 0
                person.childWork = 0
                person.socialWork = 0
                person.potentialIncome = 0
                person.wealthPV = 0
                person.wealthForCare = 0
                person.incomeExpenses = 0
                person.outOfWorkChildCare = 0
                person.outOfWorkSocialCare = 0
                person.residualWorkingHours = 0
                person.availableWorkingHours = 0
                person.residualInformalSupplies = [0.0, 0.0, 0.0, 0.0]
                person.residualInformalSupply = 0
                person.hoursInformalSupplies = [0.0, 0.0, 0.0, 0.0]
                person.maxFormalCareSupply = 0
                person.totalSupply = 0
                person.informalSupplyByKinship = [0.0, 0.0, 0.0, 0.0]
                person.formalSupplyByKinship = [0.0, 0.0, 0.0, 0.0]
                person.careForFamily = False
                person.wealthSpentOnCare = 0
                person.privateSocialCareNeed = 0
                person.privateChildCareNeed = 0
                # Social care provision variables
                person.householdsToHelp = []
                person.networkSupply = 0
                person.networkTotalSupplies = []
                person.weightedTotalSupplies = []
                person.networkInformalSupplies = []
                person.networkFormalSocialCareSupplies = []
                person.suppliers = []
    
    def householdCareNetwork(self):
        for house in self.map.occupiedHouses:
            visited = []
            household = [x for x in house.occupants]
            parents = [x for x in household if x.independentStatus == True]
            house.d1Households = []
            house.d2Households = []
            for member in parents:
                # Grandparents
                if member.father != None:
                    nok = member.father
                    if nok.dead == False and nok not in household and nok.house not in visited and nok.house.town == house.town:
                        if nok.house.householdInformalSupplies[1] > 0:
                            house.d1Households.append(nok.house)
                            visited.append(nok.house)
                    nok = member.mother
                    if nok.dead == False and nok not in household and nok.house not in visited and nok.house.town == house.town:
                        if nok.house.householdInformalSupplies[1] > 0:
                            house.d1Households.append(nok.house)
                            visited.append(nok.house)
                # Brothers
                for child in member.children:
                    nok = child
                    if nok.dead == False and nok not in household and nok.house not in visited and nok.house.town == house.town:
                        if nok.house.householdInformalSupplies[1] > 0:
                            house.d1Households.append(nok.house)
                            visited.append(nok.house)
            # Aunts and uncles
            for member in parents:
                if member.father != None:
                    brothers = list(set(member.father.children + member.mother.children))
                    brothers.remove(member)
                    for brother in brothers:
                        nok = brother
                        if nok.dead == False and nok not in household and nok.house not in visited and nok.house.town == house.town:
                            if nok.house.householdInformalSupplies[2] > 0:
                                house.d2Households.append(nok.house)
                                visited.append(nok.house)
        
            # Network of people with care needs.
            visited = []
            peopleInNeed = [x for x in household if x.careNeedLevel > 0]
            for member in peopleInNeed:
                member.d1Households = []
                member.d2Households = []
                # Parents
                if member.father != None:
                    nok = member.father
                    if nok.dead == False and nok not in household and nok.house not in visited and nok.house.town == house.town:
                        if nok.house.householdInformalSupplies[1] > 0:
                            member.d1Households.append(nok.house)
                            visited.append(nok.house)
                    nok = member.mother
                    if nok.dead == False and nok not in household and nok.house not in visited and nok.house.town == house.town:
                        if nok.house.householdInformalSupplies[1] > 0:
                            member.d1Households.append(nok.house)
                            visited.append(nok.house)
                # Children
                for child in member.children:
                    nok = child
                    if nok.dead == False and nok not in household and nok.house not in visited and nok.house.town == house.town:
                        if nok.house.householdInformalSupplies[1] > 0:
                            member.d1Households.append(nok.house)
                            visited.append(nok.house)
                            
            # Brothers
            for member in peopleInNeed:
                if member.father != None:
                    brothers = list(set(member.father.children + member.mother.children))
                    brothers.remove(member)
                    for brother in brothers:
                        nok = brother
                        if nok.dead == False and nok not in household and nok.house not in visited and nok.house.town == house.town:
                            if nok.house.householdInformalSupplies[2] > 0:
                                member.d2Households.append(nok.house)
                                visited.append(nok.house)
                
                
            
    def householdCareNetwork_Ext(self):
        
        # Create two care netwroks:
        # - an household care network for child care (a child care need is a household need)
        # - a person care network for social care (as socila care is personal)
        
        for house in self.map.occupiedHouses:
        
            house.careNetwork.add_node(house)
            house.demandNetwork.add_node(house)
            
            visited = []
            visited.append(house)
            
            household = list(house.occupants)
            residualCareNeed = sum([x.unmetSocialCareNeed for x in household])
            # Distance 1
            for member in household:
                
                if member.father != None:
                    nok = member.father
                    if nok.dead == False and nok not in household and nok.house not in visited:
                        house.careNetwork.add_edge(house, nok.house, distance = 1)
                        visited.append(nok.house)
                    nok = member.mother
                    if nok.dead == False and nok not in household and nok.house not in visited:
                        house.careNetwork.add_edge(house, nok.house, distance = 1)
                        visited.append(nok.house)
                for child in member.children:
                    nok = child
                    if nok.dead == False and nok not in household and nok.house not in visited:
                        house.careNetwork.add_edge(house, nok.house, distance = 1)
                        visited.append(nok.house)
                        
            # Distance 2
            for member in household:
                if member.father != None:
                    if member.father.father != None:
                        nok = member.father.father
                        if nok.dead == False and nok not in household and nok.house not in visited:
                            house.careNetwork.add_edge(house, nok.house, distance = 2)
                            visited.append(nok.house)
                        nok = member.father.mother
                        if nok.dead == False and nok not in household and nok.house not in visited:
                            house.careNetwork.add_edge(house, nok.house, distance = 2)
                            visited.append(nok.house)
                    if member.mother.father != None:
                        nok = member.mother.father
                        if nok.dead == False and nok not in household and nok.house not in visited:
                            house.careNetwork.add_edge(house, nok.house, distance = 2)
                            visited.append(nok.house)
                        nok = member.mother.mother
                        if nok.dead == False and nok not in household and nok.house not in visited:
                            house.careNetwork.add_edge(house, nok.house, distance = 2)
                            visited.append(nok.house)
                    brothers = list(set(member.father.children + member.mother.children))
                    brothers.remove(member)
                    for brother in brothers:
                        nok = brother
                        if nok.dead == False and nok not in household and nok.house not in visited:
                            house.careNetwork.add_edge(house, nok.house, distance = 2)
                            visited.append(nok.house)
                for child in member.children:
                    for grandchild in child.children:
                        nok = grandchild
                        if nok.dead == False and nok not in household and nok.house not in visited:
                            house.careNetwork.add_edge(house, nok.house, distance = 2)
                            visited.append(nok.house)
                            
            # Distance 3
            for member in household:
                uncles = []
                if member.father != None:
                    if member.father.father != None:
                        uncles = list(set(member.father.father.children + member.father.mother.children))
                        uncles.remove(member.father)
                    if member.mother.father != None:
                        uncles.extend(list(set(member.mother.father.children + member.mother.mother.children)))
                        uncles.remove(member.mother)
                    for uncle in uncles:
                        nok = uncle
                        if nok.dead == False and nok not in household and nok.house not in visited:
                            house.careNetwork.add_edge(house, nok.house, distance = 3)
                            visited.append(nok.house)
                    brothers = list(set(member.father.children + member.mother.children))
                    brothers.remove(member)
                    for brother in brothers:
                        for child in brother.children:
                            nok = child
                            if nok.dead == False and nok not in household and nok.house not in visited:
                                house.careNetwork.add_edge(house, nok.house, distance = 3)
                                visited.append(nok.house)
                                
        peopleInNeed = [x for x in self.pop.livingPeople if x.unmetSocialCareNeed > 0]
        for person in peopleInNeed:
            visited = []
            person.careNetwork.add_node(person)
            household = list(person.house.occupants)
            if len(household) > 1:
                otherMembers = [x for x in household if x.id != person.id]
                person.careNetwork.add_edge(person, otherMembers[0], distance = 0)
                visited.append(person.house)
            # First level
            if person.father != None:
                nok = person.father
                if nok.dead == False and nok.house not in visited:
                    person.careNetwork.add_edge(person, nok, distance = 1)
                    visited.append(nok.house)
                nok = person.mother
                if nok.dead == False and nok.house not in visited:
                    person.careNetwork.add_edge(person, nok, distance = 1)
                    visited.append(nok.house)
            for child in person.children:
                nok = child
                if nok.dead == False and nok.house not in visited:
                    person.careNetwork.add_edge(person, nok, distance = 1)
                    visited.append(nok.house)
            # Second level
            if person.father != None:
                if person.father.father != None:
                    nok = person.father.father
                    if nok.dead == False and nok.house not in visited:
                        person.careNetwork.add_edge(person, nok, distance = 2)
                        visited.append(nok.house)
                    nok = person.father.mother
                    if nok.dead == False and nok.house not in visited:
                        person.careNetwork.add_edge(person, nok, distance = 2)
                        visited.append(nok.house)
                if person.mother.father != None:
                    nok = person.mother.father
                    if nok.dead == False and nok.house not in visited:
                        person.careNetwork.add_edge(person, nok, distance = 2)
                        visited.append(nok.house)
                    nok = person.mother.mother
                    if nok.dead == False and nok.house not in visited:
                        person.careNetwork.add_edge(person, nok, distance = 2)
                        visited.append(nok.house)
                brothers = list(set(person.father.children + person.mother.children))
                brothers.remove(person)
                for brother in brothers:
                    nok = brother
                    if nok.dead == False and nok.house not in visited:
                        person.careNetwork.add_edge(person, nok, distance = 2)
                        visited.append(nok.house)
            for child in person.children:
                for grandchild in child.children:
                    nok = grandchild
                    if nok.dead == False and nok.house not in visited:
                        person.careNetwork.add_edge(person, nok, distance = 2)
                        visited.append(nok.house)
            # Third level
            uncles = []
            if person.father != None:
                if person.father.father != None:
                    uncles = list(set(person.father.father.children + person.father.mother.children))
                    uncles.remove(person.father)
                if person.mother.father != None:
                    uncles.extend(list(set(person.mother.father.children + person.mother.mother.children)))
                    uncles.remove(person.mother)
                for uncle in uncles:
                    nok = uncle
                    if nok.dead == False and nok.house not in visited:
                        person.careNetwork.add_edge(person, nok, distance = 3)
                        visited.append(nok.house)
                brothers = list(set(person.father.children + person.mother.children))
                brothers.remove(person)
                for brother in brothers:
                    for child in brother.children:
                        nok = child
                        if nok.dead == False and nok.house not in visited:
                            person.careNetwork.add_edge(person, nok, distance = 3)
                            visited.append(nok.house)
        # A demand-network is created for each household.
        for house in self.map.occupiedHouses:
            suppliers = house.careNetwork.successors(house)
            distances = [house.careNetwork[house][x]['distance'] for x in suppliers]
            for supplier in suppliers:
                if supplier.demandNetwork.has_edge(supplier, house) == True:
                    continue
                supplier.demandNetwork.add_edge(supplier, house, distance = distances[suppliers.index(supplier)])
    
    def householdSocialCareNetwork(self):
        
        
        for house in self.map.occupiedHouses:
            
            house.careNetwork.clear()
            house.careNetwork.add_node(house, netDemand = 0)
            
            visited = []
            visited.append(house)
            
            household = list(house.occupants)
            residualCareNeed = max(sum([x.unmetSocialCareNeed for x in household])-house.totalSupplies[0], 0)
            # Distance 1
            for member in household:
                distanceOne = []
                if member.father != None:
                    nok = member.father
                    if nok.dead == False and nok not in household and nok.house not in visited:
                        distanceOne.append(nok.house)
                    nok = member.mother
                    if nok.dead == False and nok not in household and nok.house not in visited:
                        distanceOne.append(nok.house)
                for child in member.children:
                    nok = child
                    if nok.dead == False and nok not in household and nok.house not in visited:
                        distanceOne.append(nok.house)
            
            np.random.shuffle(distanceOne)
            
            for supplier in distanceOne:
                # Compute prob
                exponent = (residualCareNeed+1)/math.exp(self.p['distanceExp'])
                prob = (math.exp(self.p['networkExp']*exponent)-1)/math.exp(self.p['networkExp']*exponent)
                
                print 'Prob kinship network: ' + str(prob)
                
                if supplier not in visited and np.random.random() < prob:
                    house.careNetwork.add_node(supplier, netDemand = 0)
                    house.careNetwork.add_edge(house, supplier, distance = 1, careTransferred = 0)
                    residualCareNeed -= supplier.totalSupplies[1]
                    residualCareNeed = max(residualCareNeed, 0)
                    visited.append(supplier)
                
                
            # Distance 2
            for member in household:
                distanceTwo = []
                if member.father != None:
                    if member.father.father != None:
                        nok = member.father.father
                        if nok.dead == False and nok not in household and nok.house not in visited:
                            distanceTwo.append(nok.house)
                        nok = member.father.mother
                        if nok.dead == False and nok not in household and nok.house not in visited:
                            distanceTwo.append(nok.house)
                    if member.mother.father != None:
                        nok = member.mother.father
                        if nok.dead == False and nok not in household and nok.house not in visited:
                            distanceTwo.append(nok.house)
                        nok = member.mother.mother
                        if nok.dead == False and nok not in household and nok.house not in visited:
                            distanceTwo.append(nok.house)
                    brothers = list(set(member.father.children + member.mother.children))
                    brothers.remove(member)
                    for brother in brothers:
                        nok = brother
                        if nok.dead == False and nok not in household and nok.house not in visited:
                            distanceTwo.append(nok.house)
                for child in member.children:
                    for grandchild in child.children:
                        nok = grandchild
                        if nok.dead == False and nok not in household and nok.house not in visited:
                            distanceTwo.append(nok.house)
                            
            np.random.shuffle(distanceTwo)
            
            for supplier in distanceTwo:
                # Compute prob
                exponent = (residualCareNeed+1)/math.exp(self.p['distanceExp']*2.0)
                prob = (math.exp(self.p['networkExp']*exponent)-1)/math.exp(self.p['networkExp']*exponent)
                if supplier not in visited and np.random.random() < prob:
                    house.careNetwork.add_edge(house, supplier, distance = 2)
                    residualCareNeed -= supplier.totalSupplies[2]
                    residualCareNeed = max(residualCareNeed, 0)
                    visited.append(supplier)
                            
            # Distance 3
            for member in household:
                distanceThree = []
                uncles = []
                if member.father != None:
                    if member.father.father != None:
                        uncles = list(set(member.father.father.children + member.father.mother.children))
                        uncles.remove(member.father)
                    if member.mother.father != None:
                        uncles.extend(list(set(member.mother.father.children + member.mother.mother.children)))
                        uncles.remove(member.mother)
                    for uncle in uncles:
                        nok = uncle
                        if nok.dead == False and nok not in household and nok.house not in visited:
                            distanceThree.append(nok.house)
                    brothers = list(set(member.father.children + member.mother.children))
                    brothers.remove(member)
                    for brother in brothers:
                        for child in brother.children:
                            nok = child
                            if nok.dead == False and nok not in household and nok.house not in visited:
                                distanceThree.append(nok.house)
                                
            np.random.shuffle(distanceThree)
            
            for supplier in distanceThree:
                # Compute prob
                exponent = (residualCareNeed+1)/math.exp(self.p['distanceExp']*3.0)
                prob = (math.exp(self.p['networkExp']*exponent)-1)/math.exp(self.p['networkExp']*exponent)
                if supplier not in visited and np.random.random() < prob:
                    house.careNetwork.add_edge(house, supplier, distance = 3)
                    residualCareNeed -= supplier.totalSupplies[3]
                    residualCareNeed = max(residualCareNeed, 0)
                    visited.append(supplier)
                    
                    
    def householdCareNetwork_netSupply(self):
        
        for house in self.map.occupiedHouses:
            house.careNetwork.clear()
            house.careNetwork.add_node(house)
            
            visited = []
            visited.append(house)
            
            household = list(house.occupants)
            residualCareNeed = sum([x.unmetSocialCareNeed for x in household])
            # Distance 1
            for member in household:
                
                if member.father != None:
                    nok = member.father
                    if nok.dead == False and nok not in household and nok.house not in visited and nok.house.netCareSupply > 0:
                        house.careNetwork.add_edge(house, nok.house, distance = 1)
                        visited.append(nok.house)
                    nok = member.mother
                    if nok.dead == False and nok not in household and nok.house not in visited and nok.house.netCareSupply > 0:
                        house.careNetwork.add_edge(house, nok.house, distance = 1)
                        visited.append(nok.house)
                for child in member.children:
                    nok = child
                    if nok.dead == False and nok not in household and nok.house not in visited and nok.house.netCareSupply > 0:
                        house.careNetwork.add_edge(house, nok.house, distance = 1)
                        visited.append(nok.house)
                        
            # Distance 2
            for member in household:
                if member.father != None:
                    if member.father.father != None:
                        nok = member.father.father
                        if nok.dead == False and nok not in household and nok.house not in visited and nok.house.netCareSupply > 0:
                            house.careNetwork.add_edge(house, nok.house, distance = 2)
                            visited.append(nok.house)
                        nok = member.father.mother
                        if nok.dead == False and nok not in household and nok.house not in visited and nok.house.netCareSupply > 0:
                            house.careNetwork.add_edge(house, nok.house, distance = 2)
                            visited.append(nok.house)
                    if member.mother.father != None:
                        nok = member.mother.father
                        if nok.dead == False and nok not in household and nok.house not in visited and nok.house.netCareSupply > 0:
                            house.careNetwork.add_edge(house, nok.house, distance = 2)
                            visited.append(nok.house)
                        nok = member.mother.mother
                        if nok.dead == False and nok not in household and nok.house not in visited and nok.house.netCareSupply > 0:
                            house.careNetwork.add_edge(house, nok.house, distance = 2)
                            visited.append(nok.house)
                    brothers = list(set(member.father.children + member.mother.children))
                    brothers.remove(member)
                    for brother in brothers:
                        nok = brother
                        if nok.dead == False and nok not in household and nok.house not in visited and nok.house.netCareSupply > 0:
                            house.careNetwork.add_edge(house, nok.house, distance = 2)
                            visited.append(nok.house)
                for child in member.children:
                    for grandchild in child.children:
                        nok = grandchild
                        if nok.dead == False and nok not in household and nok.house not in visited and nok.house.netCareSupply > 0:
                            house.careNetwork.add_edge(house, nok.house, distance = 2)
                            visited.append(nok.house)
                            
            # Distance 3
            for member in household:
                uncles = []
                if member.father != None:
                    if member.father.father != None:
                        uncles = list(set(member.father.father.children + member.father.mother.children))
                        uncles.remove(member.father)
                    if member.mother.father != None:
                        uncles.extend(list(set(member.mother.father.children + member.mother.mother.children)))
                        uncles.remove(member.mother)
                    for uncle in uncles:
                        nok = uncle
                        if nok.dead == False and nok not in household and nok.house not in visited and nok.house.netCareSupply > 0:
                            house.careNetwork.add_edge(house, nok.house, distance = 3)
                            visited.append(nok.house)
                    brothers = list(set(member.father.children + member.mother.children))
                    brothers.remove(member)
                    for brother in brothers:
                        for child in brother.children:
                            nok = child
                            if nok.dead == False and nok not in household and nok.house not in visited and nok.house.netCareSupply > 0:
                                house.careNetwork.add_edge(house, nok.house, distance = 3)
                                visited.append(nok.house)
                                      
    def computeSocialCareNeeds(self):
        
        self.publicSocialCare = 0
        for house in self.map.occupiedHouses:
            house.socialCareRecipients = []
            household = list(house.occupants)
            for person in household:
                careNeed = self.p['careDemandInHours'][person.careNeedLevel]
                person.hoursSocialCareDemand = careNeed
                person.unmetSocialCareNeed = person.hoursSocialCareDemand
                person.fixedNeedSchedule = [[0, 0], [0, 0], [0, 0], [0, 0]]
                person.flexibleNeed = 0
                if person.unmetSocialCareNeed > 0:
                    house.socialCareRecipients.append(person)
                    dailyHours = person.unmetSocialCareNeed/7
                    totHours = 0
                    flexibleHours = 0
                    selected = []
                    while totHours < dailyHours:
                        if person.flexibleNeed < dailyHours/2 and np.random.random() < self.p['probFlexibleNeed']:
                            person.flexibleNeed += 1
                        else:
                            j = 0
                            if np.random.random() < 0.5:
                                j = 1
                            remaining = [x for x in range(4) if x not in selected]
                            if len(remaining) == 0:
                                remaining = range(4)
                            i = np.random.choice(remaining)
                            selected.append(i)
                            person.needSchedule[i][j] = 1
                        totHours = person.flexibleNeed
                        for n in range(4):
                            totHours += sum(person.needSchedule[n])
                
                if person.unmetSocialCareNeed > 0:
                    person.wealthPV = person.financialWealth*math.pow(1.0 + self.p['pensionReturnRate'], person.lifeExpectancy)
                    person.wealthForCare = person.financialWealth
                
                preCareNeed = person.unmetSocialCareNeed
                
                if person.careNeedLevel >= self.p['publicCareNeedLevel'] and person.age >= self.p['publicCareAgeLimit'] and person.independentStatus == True:
                    socialCareCost = person.unmetSocialCareNeed*self.p['priceSocialCare']*(1.0 - self.p['socialCareTaxFreeRate'])
                    # The state pays for all the social care need that cannot be satisfied by the person with his income (leaving him a minimum income)
                    if socialCareCost > person.income - self.p['minimumIncomeGuarantee']:
                        if person.income > self.p['minimumIncomeGuarantee']:
                            stateContribution = 0
                            if person.wealth <= self.p['minWealthMeansTest']:
                                stateContribution = (socialCareCost - (person.income - self.p['minimumIncomeGuarantee']))
                            elif  person.wealth > self.p['minWealthMeansTest'] and person.wealth < self.p['maxWealthMeansTest']:
                                stateContribution = (socialCareCost - (person.income - self.p['minimumIncomeGuarantee']))
                                stateContribution -= int(person.wealth/self.p['wealthToPoundReduction'])
                                stateContribution = max(stateContribution, 0)
                            stateCare = stateContribution/(self.p['priceSocialCare']*(1.0 - self.p['socialCareTaxFreeRate']))
                            stateCare = int((stateCare+self.p['quantumCare']/2)/self.p['quantumCare'])*self.p['quantumCare']
                            # print 'State Care: ' + str(stateCare)
                            if stateCare < 0:
                                print 'Error: public care is negative!'
                                sys.exit()
                            self.publicSocialCare += stateCare
                            person.unmetSocialCareNeed -= stateCare   
                        else:
                            stateContribution = 0
                            if person.wealth <= self.p['minWealthMeansTest']:
                                stateContribution = socialCareCost
                            elif  person.wealth > self.p['minWealthMeansTest'] and person.wealth < self.p['maxWealthMeansTest']:
                                stateContribution = socialCareCost
                                stateContribution -= int(person.wealth/self.p['wealthToPoundReduction'])
                                stateContribution = max(stateContribution, 0)
                            stateCare = stateContribution/(self.p['priceSocialCare']*(1.0 - self.p['socialCareTaxFreeRate']))
                            stateCare = int((stateCare+self.p['quantumCare']/2)/self.p['quantumCare'])*self.p['quantumCare']
                            # print 'State Care: ' + str(stateCare)
                            if stateCare < 0:
                                print 'Error: public care is negative!'
                                sys.exit()
                            self.publicSocialCare += stateCare
                            person.unmetSocialCareNeed -= stateCare
                        
                        postCareNeed = person.unmetSocialCareNeed
                        
                        if postCareNeed > preCareNeed or postCareNeed < 0:
                            print postCareNeed
                            print preCareNeed
                            print person.income
                            print stateContribution
                            print stateCare
                            # sys.exit()
                            
                        
            house.totalSocialCareNeed = sum([x.hoursSocialCareDemand for x in household])
            house.totalUnmetSocialCareNeed = sum([x.unmetSocialCareNeed for x in household])
        
        self.costPublicSocialCare = self.publicSocialCare*self.p['priceSocialCare']
        self.publicCareProvision.append(self.publicSocialCare)
        totalSocialCareNeed = sum([x.hoursSocialCareDemand for x in self.pop.livingPeople if x.careNeedLevel > 0])
        totalResidualSocialCareNeed = sum([x.unmetSocialCareNeed for x in self.pop.livingPeople if x.careNeedLevel > 0])
        self.sharePublicSocialCare = 0
        if totalSocialCareNeed > 0:
            self.sharePublicSocialCare = 1.0 - float(totalResidualSocialCareNeed)/float(totalSocialCareNeed)
            
            
    def computeSocialCareNeeds_W(self):
        self.totalSocialCareNeed = 0
        self.publicSocialCare = 0
        for house in self.map.occupiedHouses:
            house.socialCareRecipients = []
            house.totalSocialCareNeed = 0
            household = list(house.occupants)
            for person in household:
                careNeed = self.p['careDemandInHours'][person.careNeedLevel]
                person.hoursSocialCareDemand = careNeed
                person.socialCareNeed = person.hoursSocialCareDemand
                person.privateSocialCareNeed = person.socialCareNeed
                person.unmetSocialCareNeed = person.hoursSocialCareDemand
                person.fixedNeedSchedule = [[0, 0], [0, 0], [0, 0], [0, 0]]
                person.flexibleNeed = 0
                if person.unmetSocialCareNeed > 0:
                    house.socialCareRecipients.append(person)
                    dailyHours = person.unmetSocialCareNeed/7
                    totHours = 0
                    selected = []
                    while totHours < dailyHours:
                        if person.flexibleNeed < dailyHours/2 and np.random.random() < self.p['probFlexibleNeed']:
                            person.flexibleNeed += 1
                        else:
                            j = 0
                            if np.random.random() < 0.5:
                                j = 1
                            remaining = [x for x in range(4) if x not in selected]
                            if len(remaining) == 0:
                                remaining = range(4)
                            i = np.random.choice(remaining)
                            selected.append(i)
                            person.fixedNeedSchedule[i][j] = 1
                        totHours = person.flexibleNeed
                        for n in range(4):
                            totHours += sum(person.fixedNeedSchedule[n])
                person.weelyFlexibleNeeds = [person.flexibleNeed]*7
                
                ## Add to the social need schedules of the household
                
                
                # person.weeklyNeeds = self.weeklySocialCareNeeds(careNeed)
                
                if person.unmetSocialCareNeed > 0:
                    person.wealthPV = person.financialWealth*math.pow(1.0 + self.p['pensionReturnRate'], person.lifeExpectancy)
                    
                    shareWealthForCare = 1.0 - 1.0/math.exp(self.p['wealthCareParam']*person.financialWealth)
                    person.wealthForCare = ((person.financialWealth/person.lifeExpectancy)*shareWealthForCare)/52.0
                    
                    # person.wealthForCare = person.financialWealth*shareWealthForCare
                
                preCareNeed = person.unmetSocialCareNeed
                
                # Compute probability of taking advantage of public social care
                # Depends on income (-) of household and level of unmet care need (+)
                
                if person.careNeedLevel >= self.p['publicCareNeedLevel'] and person.age >= self.p['publicCareAgeLimit'] and person.independentStatus == True:
                    socialCareCost = person.socialCareNeed*self.p['priceSocialCare']*(1.0 - self.p['socialCareTaxFreeRate'])
                    # The state pays for all the social care need that cannot be satisfied by the person with his income (leaving him a minimum income)
                    if socialCareCost > person.income - self.p['minimumIncomeGuarantee']:
                        if person.income > self.p['minimumIncomeGuarantee']:
                            stateContribution = 0
                            if person.financialWealth <= self.p['minWealthMeansTest']:
                                stateContribution = (socialCareCost - (person.income - self.p['minimumIncomeGuarantee']))
                            elif  person.financialWealth > self.p['minWealthMeansTest'] and person.financialWealth < self.p['maxWealthMeansTest']:
                                stateContribution = (socialCareCost - (person.income - self.p['minimumIncomeGuarantee']))
                                stateContribution -= int(person.financialWealth/self.p['wealthToPoundReduction'])
                                stateContribution = max(stateContribution, 0)
                            stateCare = stateContribution/(self.p['priceSocialCare']*(1.0 - self.p['socialCareTaxFreeRate']))
                            stateCare = int((stateCare+self.p['quantumCare']/2)/self.p['quantumCare'])*self.p['quantumCare']
                            # print 'State Care: ' + str(stateCare)
                            if stateCare < 0:
                                print 'Error: public care is negative!'
                                sys.exit()
                            self.publicSocialCare += stateCare
                            person.privateSocialCareNeed -= stateCare 
                            person.publicCareSupply = stateCare
                        else:
                            stateContribution = 0
                            if person.financialWealth <= self.p['minWealthMeansTest']:
                                stateContribution = socialCareCost
                            elif  person.financialWealth > self.p['minWealthMeansTest'] and person.financialWealth < self.p['maxWealthMeansTest']:
                                stateContribution = socialCareCost
                                stateContribution -= int(person.financialWealth/self.p['wealthToPoundReduction'])
                                stateContribution = max(stateContribution, 0)
                            stateCare = stateContribution/(self.p['priceSocialCare']*(1.0 - self.p['socialCareTaxFreeRate']))
                            stateCare = int((stateCare+self.p['quantumCare']/2)/self.p['quantumCare'])*self.p['quantumCare']
                            # print 'State Care: ' + str(stateCare)
                            if stateCare < 0:
                                print 'Error: public care is negative!'
                                sys.exit()
                            self.publicSocialCare += stateCare
                            person.publicCareSupply = stateCare
                            person.privateSocialCareNeed -= stateCare
                            
                        
                        postCareNeed = person.unmetSocialCareNeed
                        
                        if postCareNeed > preCareNeed or postCareNeed < 0:
                            print postCareNeed
                            print preCareNeed
                            print person.income
                            print stateContribution
                            print stateCare
                            # sys.exit()
                            
                        
            house.totalSocialCareNeed = sum([x.privateSocialCareNeed for x in household])
            house.totalUnmetSocialCareNeed = sum([x.unmetSocialCareNeed for x in household])
            self.totalSocialCareNeed += house.totalUnmetSocialCareNeed
            
        self.costPublicSocialCare = self.publicSocialCare*self.p['priceSocialCare']
        self.publicCareProvision.append(self.publicSocialCare)
        totalSocialCareNeed = sum([x.hoursSocialCareDemand for x in self.pop.livingPeople if x.careNeedLevel > 0])
        totalResidualSocialCareNeed = sum([x.unmetSocialCareNeed for x in self.pop.livingPeople if x.careNeedLevel > 0])
        self.sharePublicSocialCare = 0
        if totalSocialCareNeed > 0:
            self.sharePublicSocialCare = float(self.publicSocialCare)/float(totalSocialCareNeed)
     
    def weeklySocialCareNeeds(self, careNeed):
        print 'Work in progress....'
   
        # for house in self.map.occupiedHouses:
        
        
    def computeChildCareNeeds(self):
        self.totalChildCareNeed = 0
        self.publicChildCare = 0
        for house in self.map.occupiedHouses:
        
            household = list(house.occupants)
            
            parents = [x for x in household if x.independentStatus == True]
            house.gettingBenefits = False
            for parent in parents:
                if parent.ucBenefits == True or parent.guaranteeCredit == True:
                    house.gettingBenefits = True
            workingFamily = False
            if len(parents) ==  1 and parents[0].workingHours > 0:
                workingFamily = True
            elif len(parents) ==  2 and parents[0].workingHours > 0 and parents[1].workingHours > 0:
                workingFamily = True
            
            house.shiftTable = [['empty']*24, ['empty']*24, ['empty']*24, ['empty']*24, ['empty']*24, ['empty']*24, ['empty']*24]
            children = [x for x in household if x.age > 0 and x.age < self.p['ageTeenagers']]
            teenAgers = [x for x in household if x.age >= self.p['ageTeenagers'] and x.age < self.p['workingAge'][0]]
            recipients = children+teenAgers
            house.childCareRecipients = [x for x in recipients]
            house.childrenAges = list(set([x.age for x in recipients])).sort()
            newBorns = [x for x in household if x.age == 0]
            for child in newBorns:
                child.hoursChildCareDemand = self.p['zeroYearCare']
                child.netChildCareDemand = child.hoursChildCareDemand
                child.informalChildCareReceived = self.p['zeroYearCare']
                child.unmetChildCareNeed = 0
                child.mother.childWork = self.p['zeroYearCare']
            
            for child in children:
                # child.hoursChildCareDemand = max(0, self.p['childCareDemand'] - child.unmetSocialCareNeed)
                child.publicCareSupply = 0
                child.hoursChildCareDemand = max(self.p['childCareDemand'], child.unmetSocialCareNeed)
                child.unmetWeeklyNeeds = [[1]*24, [1]*24, [1]*24, [1]*24, [1]*24, [1]*24, [1]*24]
                child.residualChildcareNeed = 0
            
            for child in teenAgers:
                child.publicCareSupply = 0
                child.unmetWeeklyNeeds = [[0]*12+[1]*12, [0]*12+[1]*12, [0]*12+[1]*12, [0]*12+[1]*12, [0]*12+[1]*12, [0]*12+[1]*12, [0]*12+[1]*12]
                
            # Assign school hours (9-15) for children aged 5 to 12
            for agent in [x for x in recipients if x.age > 4]:
                for i in range(5):
                    agent.unmetWeeklyNeeds[i][1:7] = [0 for x in agent.unmetWeeklyNeeds[i][1:7]]
                    self.publicChildCare += 6 # Daily hours of school per child
            
            house.numChildcareReceivers = len(recipients)
#            householdCarers = [x for x in house.occupants if x.age >= self.p['ageTeenagers'] and x.maternityStatus == False]
#            employed = [x for x in householdCarers if x.status == 'worker']
#            householdIncome = 0
#            for worker in employed:
#                worker.income = worker.residualWorkingHours*worker.wage
            house.totalUnmetChildCareNeed = 0
            for child in recipients:
                child.unmetChildCareNeed = 0
                child.privateChildCareNeed_WNH = 0
                child.privateChildCareNeed_ONH = 0
                for i in range(7):
                    for j in range(24):
                        child.unmetChildCareNeed += child.unmetWeeklyNeeds[i][j]
                        child.totalChildCareNeed += child.unmetWeeklyNeeds[i][j]
                        if i < 5 and j < 10:
                            child.privateChildCareNeed_WNH += child.unmetWeeklyNeeds[i][j]
                        else:
                            child.privateChildCareNeed_ONH += child.unmetWeeklyNeeds[i][j]
                house.totalUnmetChildCareNeed += child.unmetChildCareNeed
            self.totalChildCareNeed += house.totalUnmetChildCareNeed
            # income = sum([x.income for x in household])
            if house.gettingBenefits == True:
                firstGroup = [x for x in children if x.age < 2]
                for child in firstGroup:
                    child.publicCareSupply = 0
                    child.totalChildCareNeed = max(child.unmetChildCareNeed-child.publicCareSupply, 0.0)
                    child.privateChildCareNeed_WNH = max(child.privateChildCareNeed_WNH-child.publicCareSupply, 0.0)
                secondGroup = [x for x in children if x.age  == 2]
                for child in secondGroup:
                    child.publicCareSupply = self.p['freeChildCareHoursToddlers']
                    child.totalChildCareNeed = max(child.unmetChildCareNeed-child.publicCareSupply, 0.0)
                    child.privateChildCareNeed_WNH = max(child.privateChildCareNeed_WNH-child.publicCareSupply, 0.0)
                    self.publicChildCare += self.p['freeChildCareHoursToddlers']
                thirdGroup = [x for x in children if x.age > 2 and x.age < 5]
                for child in thirdGroup:
                    if workingFamily == False:
                        child.publicCareSupply = self.p['freeChildCareHoursPreSchool_NWP']
                        self.publicChildCare += self.p['freeChildCareHoursPreSchool_NWP']
                    else:
                        child.publicCareSupply = self.p['freeChildCareHoursPreSchool_WF']
                        self.publicChildCare += self.p['freeChildCareHoursPreSchool_WF']
                    child.totalChildCareNeed = max(child.unmetChildCareNeed-child.publicCareSupply, 0.0)
                    child.privateChildCareNeed_WNH = max(child.privateChildCareNeed_WNH-child.publicCareSupply, 0.0)
            else:
                firstGroup = [x for x in children if x.age < 3]
                for child in firstGroup:
                    child.publicCareSupply = 0
                    child.totalChildCareNeed = max(child.unmetChildCareNeed-child.publicCareSupply, 0.0)
                    child.privateChildCareNeed_WNH = max(child.privateChildCareNeed_WNH-child.publicCareSupply, 0.0)
                secondGroup = [x for x in children if x.age > 2 and x.age < 5]
                for child in secondGroup:
                    if workingFamily == False:
                        child.publicCareSupply = self.p['freeChildCareHoursPreSchool_NWP']
                        self.publicChildCare += self.p['freeChildCareHoursPreSchool_NWP']
                    else:
                        child.publicCareSupply = self.p['freeChildCareHoursPreSchool_WF']
                        self.publicChildCare += self.p['freeChildCareHoursPreSchool_WF']
                    child.totalChildCareNeed = max(child.unmetChildCareNeed-child.publicCareSupply, 0.0)
                    child.privateChildCareNeed_WNH = max(child.privateChildCareNeed_WNH-child.publicCareSupply, 0.0)
            
            house.privateChildCareNeed_WNH = 0
            house.privateChildCareNeed_ONH = 0
            house.totalChildCareNeed = 0
            for child in recipients:
                # Net childcare needs according to periods of the day
                house.privateChildCareNeed_WNH += child.privateChildCareNeed_WNH
                house.privateChildCareNeed_ONH += child.privateChildCareNeed_ONH
                # Net childcare need unregarding of the period of the day
            house.totalChildCareNeed = house.privateChildCareNeed_WNH+house.privateChildCareNeed_ONH
            priorityChildren = [x for x in house.childCareRecipients if x.age < self.p['priorityAgeThreshold']]
            house.totalPriorityCareNeed = sum([(x.privateChildCareNeed_WNH+x.privateChildCareNeed_ONH) for x in priorityChildren])
        
            children.sort(key=operator.attrgetter("unmetChildCareNeed"))
            house.totalChilcareNeed_ONH = 0
            house.totalChilcareNeed_WNH = 0
            for i in range(7):
                for j in range(24): 
                    if i > 4 or (i < 5 and j > 9):
                        for agent in [x for x in recipients if x.privateChildCareNeed_ONH > 0]:
                            house.totalChilcareNeed_ONH += agent.unmetWeeklyNeeds[i][j]
                    elif i < 5 and j < 10:
                        for agent in [x for x in recipients if x.privateChildCareNeed_WNH > 0]:
                            house.totalChilcareNeed_WNH += agent.unmetWeeklyNeeds[i][j]
       
            receivers = children + teenAgers
            house.childrenCareNeedSchedule = []
            house.childrenInNeedByHour = []
            house.childMinAge = []
            for i in range(7):
                dayNeed = [] 
                hourReceivers = []
                receiversMinAge = []
                for j in range(24):
                    if i > 4 or (i < 5 and j > 9):
                        totalChildCareNeed = sum([x.unmetWeeklyNeeds[i][j] for x in receivers if x.privateChildCareNeed_ONH > 0])
                        hourReceivers.append([x for x in receivers if x.unmetWeeklyNeeds[i][j] == 1 and x.privateChildCareNeed_ONH > 0])
                    else:
                        totalChildCareNeed = sum([x.unmetWeeklyNeeds[i][j] for x in receivers if x.privateChildCareNeed_WNH > 0])
                        hourReceivers.append([x for x in receivers if x.unmetWeeklyNeeds[i][j] == 1 and x.privateChildCareNeed_WNH > 0])
                    dayNeed.append(totalChildCareNeed)
                    if len([x for x in receivers if x.unmetWeeklyNeeds[i][j] == 1 and x.totalChildCareNeed > 0]) > 0:
                        receiversMinAge.append(min([x.age for x in receivers if x.unmetWeeklyNeeds[i][j] == 1 and x.totalChildCareNeed > 0]))
                    else:
                        receiversMinAge.append(-1)
                house.childrenInNeedByHour.append(hourReceivers)
                house.childrenCareNeedSchedule.append(dayNeed)
                house.childMinAge.append(receiversMinAge)
            
            
#            totalNeed = sum([x.unmetChildCareNeed for x in children])
#            discountedNeed = sum([min(self.p['childcareTaxFreeCap'], x.unmetChildCareNeed) for x in children])
#            if totalNeed > 0:
#                ratio = discountedNeed/totalNeed
#            else:
#                ratio = 0.0
#            house.averageChildCarePrice = self.p['priceChildCare']*(1.0-ratio) + self.p['priceChildCare']*(1-self.p['childCareTaxFreeRate'])*ratio
#                
#            residualNeeds = [x.unmetChildCareNeed for x in children]
#            marginalNeeds = []
#            numbers = []
#            toSubtract = 0
#            for need in residualNeeds:
#                marginalNeed = need-toSubtract
#                if marginalNeed > 0:
#                    marginalNeeds.append(marginalNeed)
#                    num = len([x for x in residualNeeds if x >= need])
#                    numbers.append(num)                
#                    toSubtract = need
#            house.childCareNeeds = marginalNeeds
#            house.cumulatedChildren = numbers
#            
#            prices = []
#            residualCare = 0
#            cumulatedCare = 0
#            for i in range(len(numbers)):
#                cost = 0
#                residualCare = house.childCareNeeds[i]
#                for child in children[-numbers[i]:]:
#                    if cumulatedCare + residualCare + child.formalChildCareReceived <= self.p['childcareTaxFreeCap']:
#                        cost += self.p['priceChildCare']*(1-self.p['childCareTaxFreeRate'])*residualCare
#                    else:
#                        if child.formalChildCareReceived + cumulatedCare >= self.p['childcareTaxFreeCap']:
#                            cost += self.p['priceChildCare']*residualCare
#                        else:
#                            discountedCare = self.p['childcareTaxFreeCap'] - (child.formalChildCareReceived + cumulatedCare)
#                            cost1 = discountedCare*self.p['priceChildCare']*(1-self.p['childCareTaxFreeRate'])
#                            fullPriceCare = residualCare - discountedCare
#                            cost2 = fullPriceCare*self.p['priceChildCare']
#                            cost += (cost1 + cost2)
#                cumulatedCare += house.childCareNeeds[i]
#                prices.append(cost/house.childCareNeeds[i])
#            house.childCarePrices = prices
#            
#            # Compite high and low price chil care need
#            house.highPriceChildCare = 0
#            house.lowPriceChildCare = 0
#            for i in range(len(house.childCarePrices)):
#                if house.childCarePrices[i] >= self.p['priceSocialCare']*(1.0 - self.p['socialCareTaxFreeRate']):
#                    house.highPriceChildCare += house.childCareNeeds[i]
#                else:
#                    house.lowPriceChildCare += house.childCareNeeds[i]
#                    
#            if house.totalChildCareNeed > 0 and (house.highPriceChildCare+house.lowPriceChildCare) <= 0:
#                print 'Error: mismatch between total child care needs in computeChildCareNeeds'
#                print residualNeeds
#                print house.totalChildCareNeed
#                print house.childCareNeeds
#                print house.childCarePrices
#                print house.highPriceChildCare
#                print house.lowPriceChildCare
#                sys.exit()
        
        children = [x for x in self.pop.livingPeople if x.age > 0 and x.age < self.p['ageTeenagers']]
        totalChildCareNeed = sum([x.hoursChildCareDemand for x in children])
        totalUnmetChildCareNeed = sum([x.unmetChildCareNeed for x in children])
        
        self.costPublicChildCare = self.publicChildCare*self.p['priceChildCare']
        self.sharePublicChildCare = 0
        if totalChildCareNeed > 0:
            self.sharePublicChildCare = float(self.publicChildCare)/float(totalUnmetChildCareNeed)
            
    def householdCareSupply(self):
        self.aggregateSchedule = [0]*24
        print 'Doing householdCareSupply'
        
        for house in self.map.occupiedHouses:
        
            household = [x for x in house.occupants]
            householdCarers = [x for x in household if x.age >= self.p['ageTeenagers'] and x.careNeedLevel < 2 and x.maternityStatus == False]
           
            for member in householdCarers:
                member.freeWorkingHours = 0
                if member.status == 'teenager':
                    member.potentialCarer = True
                    member.daysOff = [6, 7]
                    member.maxDailySupplies = []
                    for i in range(1,8):
                        if i in member.daysOff:
                            member.maxDailySupplies.append(self.p['dailyTeenagerSupply'][1])
                        else:
                            member.maxDailySupplies.append(self.p['dailyTeenagerSupply'][0])
                    member.maxWeeklySupplies = [x for x in self.p['weeklyTeenagerSupply']]
                    # Member schedule
                    member.weeklyTime = [[0]*24, [0]*24, [0]*24, [0]*24, [0]*24, [0]*24, [0]*24]
                    # Set time of appointments to 0 (e.g. school time)
                    # Weekends: students have time between 8 and 20 (max 4 hours)
                    member.weeklyTime[5][:13] = [1 for x in member.weeklyTime[5][:13]]
                    member.weeklyTime[6][:13] = [1 for x in member.weeklyTime[6][:13]]
                    # In weekdays, teenager can supervise children from 17 to 20
                    for i in range(5):
                        member.weeklyTime[i][9:13] = [1 for x in member.weeklyTime[i][9:13]]
                    
                elif member.status == 'student' and member.outOfTownStudent == False:
                    member.potentialCarer = True
                    member.daysOff = [6, 7]
                    member.maxDailySupplies = []
                    for i in range(1,8):
                        if i in member.daysOff:
                            member.maxDailySupplies.append(self.p['dailyStudentSupply'][1])
                        else:
                            member.maxDailySupplies.append(self.p['dailyStudentSupply'][0])
                    member.maxWeeklySupplies = [x for x in self.p['weeklyStudentSupply']]
                    member.weeklyTime = [[1]*24, [1]*24, [1]*24, [1]*24, [1]*24, [1]*24, [1]*24]
                    # Set time of appointments to 0 (e.g. school time)
                    # Weekends: students have time between 8 and 20 (max 4 hours)
                    # In weekdays, teenager can supervise children from 17 to 20
                    for i in range(5):
                        member.weeklyTime[i][9:13] = [0 for x in member.weeklyTime[i][9:13]]
                        for i in range(5):
                            j = 1
                            while j < 11:
                                if member.weeklyTime[i][j] == 1:
                                    if np.random.random() < self.p['shareAppointmentsStudents']:
                                        # One or two-hour appointments 
                                        if np.random.random < 0.5 or j == 10:
                                            member.weeklyTime[i][j] = 0
                                        else:
                                            member.weeklyTime[i][j] = 0
                                            member.weeklyTime[i][j+1] = 0
                                            j += 1
                                j += 1
                    
                elif member.status == 'retired':
                    member.potentialCarer = True
                    member.daysOff = [6, 7]
                    member.maxDailySupplies = []
                    for i in range(1,8):
                        if i in member.daysOff:
                            member.maxDailySupplies.append(self.p['dailyRetiredSupply'][1])
                        else:
                            member.maxDailySupplies.append(self.p['dailyRetiredSupply'][0])
                    member.maxWeeklySupplies = [x for x in self.p['weeklyRetiredSupply']]
                    member.weeklyTime = [[1]*24, [1]*24, [1]*24, [1]*24, [1]*24, [1]*24, [1]*24]
                    # Add some time unavailable between 9 and 18 for personal appointments 
                    for i in range(5):
                        j = 1
                        while j < 11:
                            if np.random.random() < self.p['shareAppointmentsRetired']:
                                # One or two-hour appointments
                                if np.random.random < 0.5 or j == 10:
                                    member.weeklyTime[i][j] = 0
                                else:
                                    member.weeklyTime[i][j] = 0
                                    member.weeklyTime[i][j+1] = 0
                                    j += 1
                            j += 1

                elif member.status == 'unemployed':
                    member.potentialCarer = True
                    member.daysOff = [6, 7]
                    member.maxDailySupplies = []
                    for i in range(1,8):
                        if i in member.daysOff:
                            member.maxDailySupplies.append(self.p['dailyUnemployedSupply'][1])
                        else:
                            member.maxDailySupplies.append(self.p['dailyUnemployedSupply'][0])
                    member.maxWeeklySupplies = [x for x in self.p['weeklyUnemployedSupply']]
                    member.weeklyTime = [[1]*24, [1]*24, [1]*24, [1]*24, [1]*24, [1]*24, [1]*24]
                    # Add some time unavailable between 9 and 18 for personal appointments 
                    for i in range(5):
                        j = 1
                        while j < 11:
                            if np.random.random() < self.p['shareAppointmentsUnemployed']:
                                # One or two-hour appointments 
                                if np.random.random < 0.5 or j == 10:
                                    member.weeklyTime[i][j] = 0
                                else:
                                    member.weeklyTime[i][j] = 0
                                    member.weeklyTime[i][j+1] = 0
                                    j += 1
                            j += 1
                            
                elif member.status == 'worker':
                    member.potentialCarer = True
                    member.maxDailySupplies = []
                    for i in range(1,8):
                        if i in member.daysOff:
                            member.maxDailySupplies.append(self.p['dailyEmployedSupply'][1])
                        else:
                            member.maxDailySupplies.append(self.p['dailyEmployedSupply'][0])
                    member.maxWeeklySupplies = [x for x in self.p['weeklyEmployedSupply']]
                    member.weeklyTime = [[0]*24, [0]*24, [0]*24, [0]*24, [0]*24, [0]*24, [0]*24]
                    for i in range(7):
                        for j in range(24):
                            if member.jobSchedule[i][j] == 0:
                                member.weeklyTime[i][j] = 1
                                member.afterCareJS[i][j] = 0
                            else:
                                member.weeklyTime[i][j] = 0
                                member.afterCareJS[i][j] = 1
                    
                    # Check hours' frequencies
                            
                    for i in range(5):
                        j = 1
                        while j < 11:
                            if member.weeklyTime[i][j] == 1:
                                if np.random.random() < self.p['shareAppointmentsWorkers']:
                                    # One or two-hour appointments 
                                    if np.random.random < 0.5 or j == 10:
                                        member.weeklyTime[i][j] = 0
                                    else:
                                        member.weeklyTime[i][j] = 0
                                        member.weeklyTime[i][j+1] = 0
                                        j += 1
                            j += 1
                            
               
                # member.residualInformalSupplies = [max(x-member.hoursSocialCareDemand, 0) for x in member.residualInformalSupplies]
                # Making copies for child care provision process
                member.hoursInformalSupplies = [x for x in member.maxWeeklySupplies]
                member.residualWeeklySupplies = [x for x in member.maxWeeklySupplies]
                member.residualDailySupplies = [x for x in member.maxDailySupplies]
            
            for agent in householdCarers:
                if len(agent.residualWeeklySupplies) == 0:
                    print agent.age
                    print agent.status
                    print agent.careNeedLevel
                    
            house.carers = [x for x in householdCarers if x.residualWeeklySupplies[0] > 0]
            house.numberOfCarers = len(house.carers)
            
            
            house.householdInformalSupplySchedule = []
            house.householdInformalSuppliers = []
            for i in range(7):
                day = []
                suppliers = []
                for j in range(24):
                    careAvailabilityScore = sum([x.weeklyTime[i][j] for x in householdCarers])
                    day.append(careAvailabilityScore)
                    suppliers.append([x for x in householdCarers if x.weeklyTime[i][j] == 1])
                house.householdInformalSupplySchedule.append(day)
                house.householdInformalSuppliers.append(suppliers)

            
            house.householdInformalSupplies = []
            for i in range(4):
                kinSupply = 0
                for agent in householdCarers:
                    kinSupply += agent.residualWeeklySupplies[i]
                house.householdInformalSupplies.append(kinSupply)
        
            employed = [x for x in householdCarers if x.status == 'worker' and x.maternityStatus == False and x.careNeedLevel < 2]
            for worker in employed:
                worker.workingHours = self.p['weeklyHours'][worker.careNeedLevel]
                worker.availableWorkingHours = worker.workingHours
                worker.freeWorkingHours = worker.workingHours
                worker.potentialIncome = worker.workingHours*worker.wage
                worker.residualIncome = worker.potentialIncome  
            
            potentialIncomesFromWork = [x.potentialIncome for x in employed]
            potentialIncomesFromWelfare = [x.pension for x in household if x.status == 'retired']
            potentialIncome = sum(potentialIncomesFromWork+potentialIncomesFromWelfare)
            agentsInMaternityLeave = [x for x in household if x.maternityStatus == False]
            maternityIncomes = []
            for person in agentsInMaternityLeave:
                maternityIncome = self.p['maternityLeaveIncomeReduction']*person.previousIncome
                if person.monthsSinceBirth > 2:
                    maternityIncome = min(self.p['minStatutoryMaternityPay'], maternityIncome)
                    maternityIncomes.append(maternityIncome)
            potentialIncomesFromWelfare.extend([x.benefits for x in household])
            potentialIncomes = potentialIncomesFromWork + potentialIncomesFromWelfare + maternityIncomes
            house.potentialIncomeFromWork = sum(potentialIncomesFromWork)
            house.potentialIncomeFromWelfare = sum(potentialIncomesFromWelfare)
            house.totalPotentialIncome = sum(potentialIncomes)
            ## Add benefits
            
            house.residualIncomeForChildCare = house.totalPotentialIncome
            house.initialResidualIncomeForChildCare = house.residualIncomeForChildCare
            
            # The household's tax brackets are the sum of the individual income brackets.
            taxBands = len(self.p['taxBrackets'])
            house.incomeByTaxBand = [0]*taxBands
            house.incomeByTaxBand[-1] = potentialIncome
            for i in range(taxBands-1):
                for income in potentialIncomes:
                    if income > self.p['taxBrackets'][i]:
                        bracket = income-self.p['taxBrackets'][i]
                        house.incomeByTaxBand[i] += bracket
                        house.incomeByTaxBand[-1] -= bracket
                        potentialIncomes[potentialIncomes.index(income)] -= bracket
                        
    def updateNetworkSupplies(self):
        
        for house in self.map.occupiedHouses:
            house.d1CareSupply = 0
            house.d2CareSupply = 0
            for supplier in house.d1Households:
                house.d1CareSupply += house.householdInformalSupplies[1]
            for supplier in house.d2Households:
                house.d2CareSupply += house.householdInformalSupplies[2]

    def computeNetCareDemand(self):
        print 'Compute net care demand: work in progress....'
        
#        for house in self.map.occupiedHouses:
#            house.suppliers = [house]
#            house.suppliers.extend(list(house.careNetwork.neighbors(house)))
#            house.receivers = list(house.demandNetwork.neighbors(house))
#            totalDemand = house.totalUnmetSocialCareNeed + sum(house.childCareNeeds) # Total informal care need
#            totalSupply = house.householdInformalSupplies[0]# Total internal care supply
#            house.netCareDemand = totalDemand - totalSupply
            
                        
    def householdRelocation(self, policyFolder):
        shareRelocated = 0
        relocated = 0
        numHouseholds = len(self.map.occupiedHouses)
        for house in self.map.occupiedHouses:
            
            householdIncome = sum([x.income for x in house.occupants])
            
            perCapitaIncome = householdIncome/float(len(house.occupants))
            if house.netCareDemand > 0:
                # In this case, the household needs care. The importance of need is inversely related to income
                house.careAttractionFactor = house.netCareDemand/math.exp(self.p['careAttractionExp']*perCapitaIncome)
            else:
                # In this case, the household can supply care
                house.careAttractionFactor = house.netCareDemand
        
        for house in self.map.occupiedHouses:
            house.townAttractiveness = []
            if house.newOccupancy == True:
                continue
            
            houseRank = max([x.classRank for x in house.occupants])
            householdIncome = sum([x.income for x in house.occupants])
            perCapitaIncome = householdIncome/float(len(house.occupants))
            house.sizeIndex = self.computeHouseholdDimension(house) - 1
            
            for town in self.map.towns:
                # print town.id
                # First element: care-related factor (KNA)
                
                # If the household has positive net demand, the care attraction associated with a town depends on quantity of net supply within the 
                # household's care supply network.
                # Vice versa, if the household has positive net supply, the care attraction associated with a town depends on quantity of net supply within the
                # household's care demand network.
                
                if house.netCareDemand > 0:
                    # If the household is net receiver, the relevant relatives are those that are net suppliers.
                    neighbors = [x for x in house.suppliers if x != house and x.town == town and x.careAttractionFactor < 0]
                    distances = [house.careNetwork[house][x]['distance'] for x in neighbors]
                else:
                    # If the household is net supplier, the relevant relatives are those that are net receivers.
                    neighbors = [x for x in house.receivers if x != house and x.town == town and x.careAttractionFactor > 0]
                    distances = [house.demandNetwork[house][x]['distance'] for x in neighbors]
                    
                cares = [x.careAttractionFactor for x in neighbors]
                # The total care demand/supply is weighted by the kinship distance
                totalCare = sum([abs(x)/math.pow(self.p['networkDistanceParam'], distances[cares.index(x)]) for x in cares])
#                for care in cares:
#                    distance = distances[cares.index(care)]
#                    totalCareWeight += abs(care)/math.pow(self.p['networkDistanceParam'], distance)
                
                # The total attraction depends on the product of the house care the network care: 
                # if the household has not net demand, ther is no use for the network net supply, and vice versa.
                kinshipNetworkAttraction = abs(house.careAttractionFactor)*totalCare
                careFactor = math.exp(self.p['knaExp']*kinshipNetworkAttraction)
                
                
                # Second element: social factor
                sameSES = len([x for x in town.houses if len(x.occupants) > 0 and max([y.classRank for y in x.occupants]) >= houseRank])
                allHouses = len([x for x in town.houses if len(x.occupants) > 0])
                townSESShare = 0.0
                if allHouses > 0:
                    townSESShare = float(sameSES)/float(allHouses)
                sameSES = len([x for x in self.map.allHouses if len(x.occupants) > 0 and max([y.classRank for y in x.occupants]) == houseRank])
                allHouses = len([x for x in self.map.allHouses if len(x.occupants) > 0])
                mapSESShare = float(sameSES)/float(allHouses)
                deltaSES = townSESShare - mapSESShare
                sesFactor = math.exp(self.p['sesShareExp']*deltaSES)
                
                # Third element: economic factor
                # relRent = house.town.LHA[house.sizeIndex]/(house.town.LHA[house.sizeIndex]+math.exp(self.p['relativeRentExp']*perCapitaIncome))
                relRent = house.town.LHA[house.sizeIndex]/math.exp(self.p['relativeRentExp']*perCapitaIncome) #perCapitaIncome
                rentFactor = 1/math.exp(self.p['rentExp']*relRent)
                
#                townHouses = len([x for x in town.houses if len(x.occupants) == 0])
#                mapHouses = len([x for x in self.map.allHouses if len(x.occupants) == 0])
#                shareAvailableHouses = float(townHouses)/float(mapHouses)
                
                # Town's total attractiveness (TTA)
                townTotalAttractiveness = careFactor*sesFactor*rentFactor
                
                house.townAttractiveness.append(townTotalAttractiveness)
            
            # 1 - Sample a town other than the one where the family is living
            
            probTowns = []
            potentialTowns = []
            for town in self.map.towns:
                if town == house.town:
                    continue
                potentialTowns.append(town)
                indexTown = self.map.towns.index(town)
                townAttractiveness = house.townAttractiveness[indexTown]
                townHouses = len([x for x in town.houses if len(x.occupants) == 0])
                mapHouses = len([x for x in self.map.allHouses if len(x.occupants) == 0])
                shareAvailableHouses = float(townHouses)/float(mapHouses)
                probTowns.append(shareAvailableHouses*townAttractiveness)
            prob = [x/sum(probTowns) for x in probTowns]
            newTown = np.random.choice(potentialTowns, p = prob)
            
            # 2 - Decide whether to relocate to the new town or remain in the current one
            indexNewTown = self.map.towns.index(newTown)
            indexCurrentTown = self.map.towns.index(house.town)
            newTownAttractiveness = house.townAttractiveness[indexNewTown]
            currentTownAttractiveness = house.townAttractiveness[indexCurrentTown]
            attractivenessRatio = newTownAttractiveness/(newTownAttractiveness+currentTownAttractiveness)
            relocationCost = sum([math.pow(x.yearInTown, self.p['yearsInTownBeta']) for x in house.occupants])
            probRelocation = attractivenessRatio/math.exp(self.p['relocationCostBeta']*relocationCost)
            house.ownershipIndex = currentTownAttractiveness*relocationCost
            probRelocation *= self.p['scalingFactor']
            
            # print 'Prob Relocation: ' + str(probRelocation)
            
#                # Compute relocation probability
#                relocationCost = self.p['relocationCostParam']*sum([math.pow(x.yearInTown, self.p['yearsInTownBeta']) for x in household])
#                supportNetworkFactor = math.exp(self.p['supportNetworkBeta']*house.networkSupport)
#                relocationCostFactor = math.exp(self.p['relocationCostBeta']*relocationCost)
#                perCapitaIncome = self.computeHouseholdIncome(house)/float(len(household))
#                incomeFactor = math.exp(self.p['incomeRelocationBeta']*perCapitaIncome)
#                relativeRelocationFactor = (supportNetworkFactor*relocationCostFactor)/incomeFactor
#                probRelocation = self.p['baseRelocationRate']/relativeRelocationFactor
           
            if np.random.random() < probRelocation: #self.p['basicProbFamilyMove']*self.p['probFamilyMoveModifierByDecade'][int(ageClass)]:
                
                relocated += 1
                
                peopleToMove = [x for x in house.occupants]
                self.findNewHouseInNewTown(peopleToMove, newTown, policyFolder)
        
        shareRelocated = float(relocated)/float(numHouseholds)
        print shareRelocated
        
        # Update display house
        if len(self.displayHouse.occupants) < 1:
            self.displayHouse.display = False
            ## Nobody lives in the display house any more, choose another
            if self.nextDisplayHouse != None:
                self.displayHouse = self.nextDisplayHouse
                self.displayHouse.display = True
                self.nextDisplayHouse = None
            else:
                self.displayHouse = random.choice(self.pop.livingPeople).house
                self.displayHouse.display = True
                self.textUpdateList.append(str(self.year) + ": Display house empty, going to " + self.displayHouse.name + ".")
                messageString = "Residents: "
                for k in self.displayHouse.occupants:
                    messageString += "#" + str(k.id) + " "
                    self.textUpdateList.append(messageString)
                
    def minOwnershipShare(self, totHouses):
        a = 0
        for i in range(len(self.p['ageOwnershipShares'])):
            if i == 0:
                numHouse = len([x for x in totHouses if x.ageOccupants <= self.p['ageOwnershipShares'][i]])
            elif i == len(self.p['ageOwnershipShares'])-1:
                numHouse = len([x for x in totHouses if x.ageOccupants > self.p['ageOwnershipShares'][i]])
            else:
                numHouse = len([x for x in totHouses if x.ageOccupants > self.p['ageOwnershipShares'][i-1] and x.ageOccupants <= self.p['ageOwnershipShares'][i]])
            a += float(numHouse)*self.p['ageOwnershipShares'][i]/self.p['ageOwnershipShares'][0]
        if a > 0:
            minShare = float(len(totHouses))*self.p['incomeOwnershipShares'][0]/a
        else:
            minShare = 0
        return minShare
    
    def houseOwnership(self, year):
        
        print 'Doing home ownership'
        
        # Compute household's income decile
        households = list(self.map.occupiedHouses)
        households.sort(key=operator.attrgetter("householdIncome"))
        i = 10.0
        d = 1
        while len(households) > 0:
            decileNum = int(float(len(households))/i)
            decilePop = households[:decileNum]
            for house in decilePop:
                house.incomeDecile = d
            households = [x for x in households if x not in decilePop]
            i -= 1
            d += 1
        
        for house in self.map.occupiedHouses:
            
            independentHousehold = [x for x in house.occupants if x.independentStatus == True]
            
            if len(independentHousehold) < 1 or len(independentHousehold) > 2:
                print 'Error: wrong number of independet agents!'
                print 'There are ' + str(len(independentHousehold)) + ' independent agents.'
                print 'Independent agents: ' + str(independentHousehold)
                print 'All members: ' + str(len(house.occupants))
                print 'Member ages: ' + str([x.age for x in house.occupants])
                sys.exit()
            if len(independentHousehold) == 2:
                partners = [x for x in house.occupants if x.partner != None]
                if len(partners) > 2:
                    print 'Error: there is more than one couple!'
                    print 'Independent agents: ' + str(independentHousehold)
                    sys.exit()
            
            ageMean = np.mean([x.age for x in independentHousehold])
            house.ageOccupants = ageMean
           
        # Check number of owned houses in each income-age class
        for d in range(10):
            totHouses = [x for x in self.map.occupiedHouses if x.incomeDecile == d]
            minShare = self.minOwnershipShare(totHouses)
            for i in range(len(self.p['ageOwnershipShares'])):
                share = minShare*self.p['ageOwnershipShares'][i]/self.p['ageOwnershipShares'][0]
                if i == 0:
                    ageHouse = [x for x in totHouses if x.ageOccupants <= self.p['ageOwnershipShares'][i]]
                elif i == len(self.p['ageOwnershipShares'])-1:
                    ageHouse = [x for x in totHouses if x.ageOccupants > self.p['ageOwnershipShares'][i]]
                else:
                    ageHouse = [x for x in totHouses if x.ageOccupants > self.p['ageOwnershipShares'][i-1] and x.ageOccupants <= self.p['ageOwnershipShares'][i]]
                empiricalOwners = int(share*float(len(ageHouse)))
                actualOwners = [x for x in ageHouse if x.ownedByOccupants == True]
                rentedHouses = [x for x in ageHouse if x not in actualOwners]
                if empiricalOwners < len(actualOwners):
                    # In this case some house are sold
                    numHousesToSell = len(actualOwners)-empiricalOwners
                    sumWeights = sum([1.0/np.exp(self.p['ownershipProbExp']*x.ownershipIndex) for x in actualOwners])
                    probs = [(1.0/np.exp(self.p['ownershipProbExp']*x.ownershipIndex))/sumWeights for x in actualOwners]
                    houseToSell = np.random.choice(actualOwners, numHousesToSell, replace = False, p = probs)
                    for house in houseToSell:
                        house.ownedByOccupants = False
                if empiricalOwners > len(actualOwners):
                    # In this case, some renting agents by a house.
                    numHousesToBuy = empiricalOwners-len(actualOwners)
                    sumWeights = sum([np.exp(self.p['ownershipProbExp']*x.ownershipIndex) for x in rentedHouses])
                    probs = [np.exp(self.p['ownershipProbExp']*x.ownershipIndex)/sumWeights for x in rentedHouses]
                    houseToBuy = np.random.choice(rentedHouses, numHousesToBuy, replace = False, p = probs)
                    for house in houseToBuy:
                        house.ownedByOccupants = True
                
    def computeHouseholdDimension(self, house):
        # Compute number of rooms for housing benefit purposes
        adults = [x for x in house.occupants if x.age > 15]
        houseBenefitRoom = 0
        visited = []
        for person in adults:
            if person in visited:
                continue
            visited.append(person)
            if person.partner != None:
                visited.append(person.partner)
            houseBenefitRoom +=1
        rooms = []
        children = [x for x in house.occupants if x.age < 16]
        children.sort(key=operator.attrgetter("age"), reverse = True)
        allocated = []
        for child in children:
            roomMates = []
            if child in allocated:
                continue
            allocated.append(child)
            roomMates.append(child)
            if child.age > 9:
                # Only another child of same sex can go with him
                sameSexChildren = [x for x in children if x.sex == child.sex and x.id != child.id]
                if len(sameSexChildren) > 0:
                    allocated.append(sameSexChildren[0])
                    roomMates.append(sameSexChildren[0])
            else:
                # Any child can share the room
                otherChildren = [x for x in children if x.id != child.id]
                if len(otherChildren) > 0:
                    allocated.append(otherChildren[0])
                    roomMates.append(otherChildren[0])
            rooms.append(roomMates)
        houseBenefitRoom += len(rooms)
        houseBenefitRoom = min(houseBenefitRoom, 4)
        houseBenefitRoom -= 1
        return houseBenefitRoom
        
    def doAgeTransitions(self, policyFolder, month):
        
        for person in self.pop.livingPeople:
            if person.birthMonth == month:
                person.age += 1
            person.movedThisYear = False
            # Change this....
            person.yearInTown += 1
            if person.maternityStatus == True:
                person.monthsSinceBirth += 1
            if person.monthsSinceBirth == self.p['maternityLeaveDuration']:
                person.maternityStatus = False
                person.monthsSinceBirth = 0
        """Check whether people have moved on to a new status in life."""
        peopleNotYetRetired = [x for x in self.pop.livingPeople if x.status != 'retired']
        for person in peopleNotYetRetired:
            ## Do transitions to adulthood and retirement
            if person.age == self.p['ageTeenagers'] and person.status != 'teenager':
                person.status = 'teenager'
            if person.age == self.p['ageOfAdulthood'] and person.status != 'student':
                person.status = 'student'
                person.classRank = 0 # max(person.father.classRank, person.mother.classRank)
                if np.random.random() < self.p['probOutOfTownStudent']:
                    person.outOfTownStudent = True
                if person.house == self.displayHouse:
                    messageString = str(self.year) + ": #" + str(person.id) + " is now an adult."
                    self.textUpdateList.append(messageString)
                        
                    with open(os.path.join(policyFolder, "Log.csv"), "a") as file:
                        writer = csv.writer(file, delimiter = ",", lineterminator='\r')
                        writer.writerow([self.year, messageString])
                        
                        
            elif person.age == self.p['ageOfRetirement'] and person.status != 'retired':
                person.status = 'retired'
                person.jobSchedule = [[0]*24, [0]*24, [0]*24, [0]*24, [0]*24, [0]*24, [0]*24]
                person.wage = 0
                shareWorkingTime = person.workingPeriods/float(self.p['minContributionPeriods'])
                dK = np.random.normal(0, self.p['wageVar'])
                person.pension = person.lastIncome*shareWorkingTime*math.exp(dK)
                if person.house == self.displayHouse:
                    messageString = str(self.year) + ": #" + str(person.id) + " has now retired."
                    self.textUpdateList.append(messageString)
                        
                    with open(os.path.join(policyFolder, "Log.csv"), "a") as file:
                        writer = csv.writer(file, delimiter = ",", lineterminator='\r')
                        writer.writerow([self.year, messageString])
                    
    def startWorking(self, person):
        
        person.status = 'unemployed'
        person.outOfTownStudent = False
        
        dKi = np.random.normal(0, self.p['wageVar'])
        person.initialIncome = self.p['incomeInitialLevels'][person.classRank]*math.exp(dKi)
        dKf = np.random.normal(dKi, self.p['wageVar'])
        person.finalIncome = self.p['incomeFinalLevels'][person.classRank]*math.exp(dKf)
        
#        person.wage = person.initialIncome
#        person.income = person.wage*self.p['weeklyHours'][int(person.careNeedLevel)]
#        person.potentialIncome = person.income
    
    def doSocialTransition(self, policyFolder, month):
        
        if month == 1:
            for person in self.pop.livingPeople:
                if person.age == self.p['workingAge'][person.classRank] and person.status == 'student':
                # With a certain probability p the person enters the workforce, 
                # with a probability 1-p goes to the next educational level
                    if person.classRank == 4:
                        probStudy = 0.0
                    else:
                        probStudy = self.transitionProb(person) # Probability of keeping studying
                    
                    if np.random.random() > probStudy:
                        self.startWorking(person)
                        if person.house == self.displayHouse:
                            messageString = str(self.year) + ": #" + str(person.id) + " is now looking for a job."
                            self.textUpdateList.append(messageString)
                            
                            with open(os.path.join(policyFolder, "Log.csv"), "a") as file:
                                writer = csv.writer(file, delimiter = ",", lineterminator='\r')
                                writer.writerow([self.year, messageString])
                            
                    else:
                        person.classRank += 1
                        if person.house == self.displayHouse:
                            messageString = str(self.year) + ": #" + str(person.id) + " is now a student."
                            self.textUpdateList.append(messageString)
                            
                            with open(os.path.join(policyFolder, "Log.csv"), "a") as file:
                                writer = csv.writer(file, delimiter = ",", lineterminator='\r')
                                writer.writerow([self.year, messageString])
                        
            
    def transitionProb (self, person):
        household = [x for x in person.house.occupants]
        if person.father.dead + person.mother.dead != 2:
            disposableIncome = sum([x.income for x in household])
            perCapitaDisposableIncome = disposableIncome/len(household)
            # print('Per Capita Disposable Income: ' + str(perCapitaDisposableIncome))
            
            if perCapitaDisposableIncome > 0.0:
                
                forgoneSalary = self.p['incomeInitialLevels'][person.classRank]*self.p['weeklyHours'][person.careNeedLevel]
                educationCosts = self.p['educationCosts'][person.classRank]
                
                # relCost = (forgoneSalary+educationCosts)/perCapitaDisposableIncome
                
                relCost = forgoneSalary/perCapitaDisposableIncome
                
                # Check variable
#                if self.year == self.p['getCheckVariablesAtYear']:
#                    self.relativeEducationCost.append(relCost) # 0.2 - 5
                
                incomeEffect = (self.p['costantIncomeParam']+1)/(math.exp(self.p['eduWageSensitivity']*relCost) + self.p['costantIncomeParam']) # Min-Max: 0 - 10
                
                targetEL = max(person.father.classRank, person.mother.classRank)
                
                dE = float(targetEL - person.classRank)
                expEdu = math.exp(self.p['eduRankSensitivity']*dE)
                educationEffect = expEdu/(expEdu+self.p['costantEduParam'])
                
                careEffect = 1/math.exp(self.p['careEducationParam']*(person.socialWork+person.childWork))
                
                
                ### Fixing probability to keep studying   ######################
                
                pStudy = incomeEffect*educationEffect*careEffect
                
#                shareAdjustmentFactor = self.socialClassShares[person.classRank] - self.p['shareClasses'][person.classRank]
#                
#                pStudy *= math.exp(self.p['classAdjustmentBeta']*shareAdjustmentFactor)
                
                if person.classRank == 0 and self.socialClassShares[0] > 0.2:
                    pStudy *= 1.0/0.9
                
                if person.classRank == 0 and self.socialClassShares[0] < 0.2:
                    pStudy *= 0.85
                
                if person.classRank == 1 and self.socialClassShares[1] > 0.35:
                    pStudy *= 1.0/0.8
                    
                if person.classRank == 2 and self.socialClassShares[2] > 0.25:
                    pStudy *= 1.0/0.85
                    
                
                #####################################################################
                
                # pStudy = math.pow(incomeEffect, self.p['incEduExp'])*math.pow(educationEffect, 1-self.p['incEduExp'])
                if pStudy < 0:
                    pStudy = 0
                # Check
#                if self.year == self.p['getCheckVariablesAtYear']:
#                    self.probKeepStudying.append(pStudy)
#                    self.person.classRankStudent.append(person.classRank)
                
            else:
                # print('perCapitaDisposableIncome: ' + str(perCapitaDisposableIncome))
                pStudy = 0
        else:
            pStudy = 0
        # pWork = math.exp(-1*self.p['eduEduSensitivity']*dE1)
        # return (pStudy/(pStudy+pWork))
        #pStudy = 0.8
        return pStudy
    
    def assignJobs(self, hiredAgents, month):
        # Create a list of weekly shifts
        numHiredAgents = len(hiredAgents)
        hiredAgents.sort(key=operator.attrgetter("unemploymentIndex"))
        shifts = [x for x in list(np.random.choice(self.shiftsPool, numHiredAgents))]
        for person in hiredAgents:
            if month == -1:
                month = np.random.choice([x+1 for x in range(12)])
            person.status = 'worker'
            person.unemploymentMonths = 0
            person.monthHired = month
            person.wage = self.computeWage(person)
            weights = [x.socialIndex for x in shifts]
            probs = [x/sum(weights) for x in weights]
            negativeProbes = [x for x in probs if x < 0]
            if len(negativeProbes) > 0:
                print 'Error: a negative prob!'
                sys.exit()
            shift = np.random.choice(shifts, p = probs)
            person.jobShift = shift
            person.daysOff = [x for x in range(1, 8) if x not in shift.days]
            person.workingHours = self.p['weeklyHours'][person.careNeedLevel]
            person.jobSchedule = self.weeklySchedule(shift, person.workingHours)
            shifts.remove(shift)
            
    def weeklySchedule(self, shift, weeklyHours):
        dailyHours = int(weeklyHours/5)
        shiftHours = [x for x in shift.shiftHours]
        if dailyHours < len(shiftHours):
            if np.random.random < 0.5:
                shiftHours = shift.shiftHours[:4]
            else:
                shiftHours = shift.shiftHours[4:]
        weeklySchedule = [[0]*24, [0]*24, [0]*24, [0]*24, [0]*24, [0]*24, [0]*24]
        for day in shift.days:
            for hour in shiftHours:
                weeklySchedule[day-1][hour] = 1
        return weeklySchedule
        
    def dismissWorkers(self, newUnemployed):
        for person in newUnemployed:
            person.status = 'unemployed'
            person.workingHours = 0
            person.income = 0
            person.jobTenure = 0
            person.monthHired = 0
            person.jobShift = None
            person.jobSchedule = [[0]*24, [0]*24, [0]*24, [0]*24, [0]*24, [0]*24, [0]*24]
            # person.weeklyTime = [[1]*24, [1]*24, [1]*24, [1]*24, [1]*24, [1]*24, [1]*24]
            
        # Assign unemployment duration: sample number determined by share according to unemploymentIndex.
        unemployed = list(newUnemployed)
        men = [x for x in unemployed if x.sex == 'male']
        numMen = len(men)
        women = [x for x in unemployed if x.sex == 'female']
        numWomen = len(women)
        for i in ['male', 'female']:
            if i == 'male':
                durationShares = self.p['maleUDS']
                unemployed = list(men)
                totUnemployed = numMen
            else:
                durationShares = self.p['femaleUDS']
                unemployed = list(women)
                totUnemployed = numWomen
            durationIndex = 1
            for durationShare in durationShares:
                numUnemployed = min(int(float(totUnemployed)*durationShare), len(unemployed))
                if numUnemployed > 0:
                    weights = [1.0/np.exp(self.p['unemploymentBeta']*x.unemploymentIndex) for x in unemployed]
                    probs = [x/sum(weights) for x in weights]
                    assignedUnemployed = np.random.choice(unemployed, numUnemployed, p = probs)
                    for person in assignedUnemployed:
                        if durationIndex < 7:
                            person.unemploymentDuration = durationIndex
                        else:
                            if durationIndex == 7:
                                person.unemploymentDuration = np.random.choice(range(7,10))
                            elif durationIndex == 8:
                                person.unemploymentDuration = np.random.choice(range(10,13))
                            elif durationIndex == 9:
                                person.unemploymentDuration = np.random.choice(range(13,19))
                            elif durationIndex == 10:
                                person.unemploymentDuration = np.random.choice(range(19,25))
                    durationIndex += 1
                    unemployed = [x for x in unemployed if x not in assignedUnemployed]
                else:
                    break
            if len(unemployed) > 0:
                for person in unemployed:
                    person.unemploymentDuration = 25
    
    def computeIncome(self, month):
        # Compute income from work based on last period job market and informal care
        for person in self.pop.livingPeople:
            if month == 1:
                person.yearlyIncome = 0
                person.yearlyDisposableIncome = 0
                person.yearlyBenefits = 0
            if person.status == 'worker':
                person.income = person.wage*person.availableWorkingHours
                person.lastIncome = person.income
                # Detract taxes and 
            elif person.status == 'retired':
                person.income = person.pension
            else:
                person.income = 0
            person.yearlyIncome += (person.income*52.0)/12
            person.disposableIncome = person.income

        # Compute income quintiles original income
        for house in self.map.occupiedHouses:
            if month == 1:
                house.yearlyIncome = 0
                house.yearlyDisposableIncome = 0
                house.yearlyBenefits = 0
            house.householdIncome = sum([x.income for x in house.occupants])
            house.incomePerCapita = house.householdIncome/float(len(house.occupants))
            house.yearlyIncome += (house.householdIncome*52.0)/12
            
        households = [x for x in self.map.occupiedHouses]
        households.sort(key=operator.attrgetter("yearlyIncome"))
        for i in range(5):
            number = int(round(len(households)/(5.0-float(i))))
            quintile = households[:number]
            for j in quintile:
                j.incomeQuintile = i
            households = [x for x in households if x not in quintile]
        
        if month == 12:
            independentAgents = [x for x in self.pop.livingPeople if x.independentStatus == True]
            independentAgents.sort(key=operator.attrgetter("yearlyIncome"))
            for i in range(5):
                number = int(round(len(independentAgents)/(5.0-float(i))))
                quintile = independentAgents[:number]
                for j in quintile:
                    j.incomeQuintile = i
                independentAgents = [x for x in independentAgents if x not in quintile]

        # Now, compute disposable income (i..e after taxes and benefits)
        # First, reduce by tax
        earningPeople = [x for x in self.pop.livingPeople if x.income > 0]
        self.totalTaxRevenue = 0
        self.totalPensionRevenue = 0
        for person in earningPeople:
            employeePensionContribution = 0
            # Pension Contributions
            if person.disposableIncome > 162.0:
                if person.disposableIncome < 893.0:
                    employeePensionContribution = (person.disposableIncome - 162.0)*0.12
                else:
                    employeePensionContribution = (893.0 - 162.0)*0.12
                    employeePensionContribution += (person.disposableIncome - 893.0)*0.02
            person.disposableIncome -= employeePensionContribution
            self.totalPensionRevenue += employeePensionContribution
            
            # Tax Revenues
            tax = 0
            residualIncome = person.disposableIncome
            for i in range(len(self.p['taxBrackets'])):
                if residualIncome > self.p['taxBrackets'][i]:
                    taxable = residualIncome - self.p['taxBrackets'][i]
                    tax += taxable*self.p['taxationRates'][i]
                    residualIncome -= taxable
            person.disposableIncome -= tax
            self.totalTaxRevenue += tax
            
        self.statePensionRevenue.append(self.totalPensionRevenue)
        self.stateTaxRevenue.append(self.totalTaxRevenue)
        
        # ...then add benefits
        for person in self.pop.livingPeople:
            person.disposableIncome += person.benefits
            person.yearlyBenefits += (person.benefits*52.0)/12
            person.yearlyDisposableIncome += (person.disposableIncome*52.0)/12
            person.cumulativeIncome += person.disposableIncome
                # person.cumulativeIncome = max(person.cumulativeIncome, 0)
        # Compute income quintiles disposable income
        for house in self.map.occupiedHouses:
            house.householdDisposableIncome = sum([x.disposableIncome for x in house.occupants])
            house.benefits = sum([x.benefits for x in house.occupants])
            house.yearlyDisposableIncome += (house.householdDisposableIncome*52.0)/12
            house.yearlyBenefits += (house.benefits*52.0)/12
            house.disposableIncomePerCapita = house.householdIncome/float(len(house.occupants))
        households = [x for x in self.map.occupiedHouses]
        households.sort(key=operator.attrgetter("yearlyDisposableIncome"))
        for i in range(5):
            number = int(round(len(households)/(5.0-float(i))))
            quintile = households[:number]
            for j in quintile:
                j.disposableIncomeQuintile = i
            households = [x for x in households if x not in quintile]
            
        independentAgents = [x for x in self.pop.livingPeople if x.independentStatus == True]
        if month == 12:
            independentAgents.sort(key=operator.attrgetter("yearlyDisposableIncome"))
            for i in range(5):
                number = int(round(len(independentAgents)/(5.0-float(i))))
                quintile = independentAgents[:number]
                for j in quintile:
                    j.disposableIncomeQuintile = i
                independentAgents = [x for x in independentAgents if x not in quintile]
        
        # Then, from the household income subtract the cost of formal child and social care
        for house in self.map.occupiedHouses:
            house.householdNetIncome = house.householdDisposableIncome-house.costFormalCare
            house.netIncomePerCapita = house.householdNetIncome/float(len(house.occupants))
        # Compute net income distribution
        households = [x for x in self.map.occupiedHouses]
        households.sort(key=operator.attrgetter("householdNetIncome"))
        for i in range(5):
            number = int(round(len(households)/(5.0-float(i))))
            quintile = households[:number]
            for j in quintile:
                j.netIncomeQuintile = i
            households = [x for x in households if x not in quintile]  

        for house in self.map.occupiedHouses:
            house.totalIncome = sum([x.totalIncome for x in house.occupants])
            house.povertyLineIncome = 0
            independentMembers = [x for x in house.occupants if x.independentStatus == True]
            if len(independentMembers) == 1:
                independentPerson = [x for x in house.occupants if x.independentStatus == True][0]
                if independentPerson.status == 'worker':
                    house.povertyLineIncome = self.p['singleWorker']
                elif independentPerson.status == 'retired':
                    house.povertyLineIncome = self.p['singlePensioner']
            elif len(independentMembers) == 2:
                independentPerson_1 = [x for x in house.occupants if x.independentStatus == True][0]
                independentPerson_2 = [x for x in house.occupants if x.independentStatus == True][1]
                if independentPerson_1.status == 'worker' and independentPerson_2.status == 'worker':
                    house.povertyLineIncome = self.p['marriedCouple']
                elif (independentPerson_1.status == 'retired' and independentPerson_2.status == 'worker') or (independentPerson_2.status == 'retired' and independentPerson_1.status == 'worker'):
                    house.povertyLineIncome = self.p['mixedCouple']
                elif independentPerson_1.status == 'retired' and independentPerson_2.status == 'retired':
                    house.povertyLineIncome = self.p['couplePensioners']
            dependentMembers = [x for x in house.occupants if x.independentStatus == False]
            house.povertyLineIncome += len(dependentMembers)*self.p['additionalChild']
        
        # Update work experience and wage
#        for person in self.pop.livingPeople:
#            if person.status == 'worker':
#                # person.workingPeriods = 0
#                if person.workingHours > 0:
#                    person.workingPeriods += float(person.availableWorkingHours)/float(person.workingHours)
#                person.workExperience += float(person.availableWorkingHours)/self.p['weeklyHours'][0]
#                person.wage = self.computeWage(person)
    
    def computeIncomeQuintileShares(self):
        independentAgents = [x for x in self.pop.livingPeople if x.independentStatus == True]
        print 'Mean income IQ1: ' + str(np.mean([x.yearlyIncome for x in independentAgents if x.incomeQuintile == 0]))
        
#        if len(independentAgents_zeroIncome) > 0:
#            for agent in independentAgents_zeroIncome:
#                print 'Zero-income agent age: ' + str(agent.age)
#                print 'Zero-income agent status: ' + str(agent.status)
#                print 'Zero-income agent months unemployed: ' + str(agent.unemploymentMonths)
#                print 'Zero-income agent maternity status: ' + str(agent.maternityStatus)
#                print 'Zero-income agent care need: ' + str(agent.careNeedLevel)
#                print 'Zero-income agent class: ' + str(agent.classRank)
#                print 'Zero-income agent wealth: ' + str(agent.financialWealth)
#                print 'Zero-income agent cumulative Income: ' + str(agent.cumulativeIncome)
#                print 'Zero-income agent benefits: ' + str(agent.benefits)
#        
#            pdb.set_trace()
            
        origIQ1 = np.median([x.yearlyIncome for x in independentAgents if x.incomeQuintile == 0])
        origIQ2 = np.median([x.yearlyIncome for x in independentAgents if x.incomeQuintile == 1])
        origIQ3 = np.median([x.yearlyIncome for x in independentAgents if x.incomeQuintile == 2])
        origIQ4 = np.median([x.yearlyIncome for x in independentAgents if x.incomeQuintile == 3])
        origIQ5 = np.median([x.yearlyIncome for x in independentAgents if x.incomeQuintile == 4])
        print 'Gross incomes quintiles: ' + str([origIQ1, origIQ2, origIQ3, origIQ4, origIQ5])
        
        dispIQ1 = np.median([x.yearlyDisposableIncome for x in independentAgents if x.disposableIncomeQuintile == 0])
        dispIQ2 = np.median([x.yearlyDisposableIncome for x in independentAgents if x.disposableIncomeQuintile == 1])
        dispIQ3 = np.median([x.yearlyDisposableIncome for x in independentAgents if x.disposableIncomeQuintile == 2])
        dispIQ4 = np.median([x.yearlyDisposableIncome for x in independentAgents if x.disposableIncomeQuintile == 3])
        dispIQ5 = np.median([x.yearlyDisposableIncome for x in independentAgents if x.disposableIncomeQuintile == 4])
        print 'Disposable incomes quintiles: ' + str([dispIQ1, dispIQ2, dispIQ3, dispIQ4, dispIQ5])
        
        origIQ1 = np.median([x.yearlyIncome for x in self.map.occupiedHouses if x.incomeQuintile == 0])
        origIQ2 = np.median([x.yearlyIncome for x in self.map.occupiedHouses if x.incomeQuintile == 1])
        origIQ3 = np.median([x.yearlyIncome for x in self.map.occupiedHouses if x.incomeQuintile == 2])
        origIQ4 = np.median([x.yearlyIncome for x in self.map.occupiedHouses if x.incomeQuintile == 3])
        origIQ5 = np.median([x.yearlyIncome for x in self.map.occupiedHouses if x.incomeQuintile == 4])
        print 'Households Gross incomes quintiles: ' + str([origIQ1, origIQ2, origIQ3, origIQ4, origIQ5])
        
        benIQ1 = np.median([x.yearlyBenefits for x in self.map.occupiedHouses if x.incomeQuintile == 0])
        benIQ2 = np.median([x.yearlyBenefits for x in self.map.occupiedHouses if x.incomeQuintile == 1])
        benIQ3 = np.median([x.yearlyBenefits for x in self.map.occupiedHouses if x.incomeQuintile == 2])
        benIQ4 = np.median([x.yearlyBenefits for x in self.map.occupiedHouses if x.incomeQuintile == 3])
        benIQ5 = np.median([x.yearlyBenefits for x in self.map.occupiedHouses if x.incomeQuintile == 4])
        print 'Households benefits by income quintile: ' + str([benIQ1, benIQ2, benIQ3, benIQ4, benIQ5])
        
        dispIQ1 = np.median([x.yearlyDisposableIncome for x in self.map.occupiedHouses if x.disposableIncomeQuintile == 0])
        dispIQ2 = np.median([x.yearlyDisposableIncome for x in self.map.occupiedHouses if x.disposableIncomeQuintile == 1])
        dispIQ3 = np.median([x.yearlyDisposableIncome for x in self.map.occupiedHouses if x.disposableIncomeQuintile == 2])
        dispIQ4 = np.median([x.yearlyDisposableIncome for x in self.map.occupiedHouses if x.disposableIncomeQuintile == 3])
        dispIQ5 = np.median([x.yearlyDisposableIncome for x in self.map.occupiedHouses if x.disposableIncomeQuintile == 4])
        print 'Households Disposable incomes quintiles: ' + str([dispIQ1, dispIQ2, dispIQ3, dispIQ4, dispIQ5])
        
    def computeWage(self, person):
        c = np.math.log(person.initialIncome/person.finalIncome)
        wage = person.finalIncome*np.math.exp(c*np.math.exp(-1*self.p['incomeGrowthRate'][person.classRank]*person.workExperience))
        dK = np.random.normal(0, self.p['wageVar'])
        wage *= math.exp(dK)
        return wage
    
    def checkIncome(self, n):
        zeroIncomeHouseholds = [x for x in self.map.occupiedHouses if sum([y.income for y in x.occupants]) == 0]
        print 'Number of zero income households (' + str(n) + '): ' + str(len(zeroIncomeHouseholds))
    
    def jobMarket(self, year, month):
        self.hiredPeople = []
        self.newUnemployed = []
        activePop = [x for x in self.pop.livingPeople if (x.status == 'worker' or x.status == 'unemployed') and x.careNeedLevel < 2 and x.maternityStatus == False]
        
        unemployedNotInActive = [x for x in self.pop.livingPeople if x not in activePop and x.status == 'unemployed']
        

#        workingPop = [x for x in activePop if x.status == 'worker']
#        notChanged = [x for x in workingPop if x.jobTenure > self.p['minTenure']]
#        jobChangersNum = int(float(len(notChanged))*self.p['monthlyTurnOver'])
#        
#        weights = [np.exp(self.p['changeJobBeta']*(float(len(x.house.town.houses))*x.house.ownershipIndex*x.wage)) for x in notChanged]
#        probs = [x/sum(weights) for x in weights]
#        jobChangers = np.random.choice(workingPop, jobChangersNum, p = probs)
        
        workingPop = [x for x in activePop if x.status == 'worker']
        for person in workingPop:
            person.jobTenure += 1
            if person.workingHours > 0:
                person.workingPeriods += float(person.availableWorkingHours)/float(person.workingHours)
            person.workExperience += float(person.availableWorkingHours)/self.p['weeklyHours'][0]
            person.wage = self.computeWage(person)
            
        
        unemployed = [x for x in activePop if x.status == 'unemployed']
        for person in unemployed:
            person.unemploymentMonths += 1
            person.unemploymentDuration -= 1
        
        longTermUnemployed = [x for x in unemployed if x.unemploymentMonths >= 12]
        longTermUnemploymentRate = float(len(longTermUnemployed))/float(len(activePop))
        print 'Long-term unemployment rate: ' + str(longTermUnemploymentRate)
        
        unemploymentRate = self.unemployment_series[int(self.year-self.p['startYear'])]
        
        print 'Unemployment rate: ' + str(unemploymentRate)
        
        classShares = []
        for c in range(int(self.p['numberClasses'])):
            classPop = [x for x in activePop if x.classRank == c]
            classShares.append(float(len(classPop))/float(len(activePop)))

        for c in range(int(self.p['numberClasses'])):
            classPop = [x for x in activePop if x.classRank == c]
            ageBandShares = []
            for b in range(int(self.p['numberAgeBands'])):
                agePop = [x for x in classPop if self.ageBand(x.age) == b]
                if len(classPop) > 0:
                    ageBandShares.append(float(len(agePop))/float(len(classPop)))
                else:
                    ageBandShares.append(0)
                    
            for b in range(int(self.p['numberAgeBands'])):
                agePop = [x for x in activePop if x.classRank == c and self.ageBand(x.age) == b]
                if len(agePop) > 0:
                    ageSES_ur = self.computeUR(unemploymentRate, classShares, ageBandShares, self.p['unemploymentClassBias'], self.p['unemploymentAgeBias'], c, b)
                    workPop = [x for x in workingPop if x.classRank == c and self.ageBand(x.age) == b]
                    if len(workPop) > 0:
                        # Age and SES-specific unemployment rate 
                        layOffsRate = self.p['meanLayOffsRate']*ageSES_ur/unemploymentRate
                        dismissableWorkers = [x for x in workPop if x.jobTenure >= self.p['probationPeriod']]
                        numLayOffs = min(int(float(len(workPop))*layOffsRate), len(dismissableWorkers))
                        if numLayOffs > 0:
                            weights = [1.0/np.exp(self.p['layOffsBeta']*x.jobTenure) for x in dismissableWorkers]
                            probs = [x/sum(weights) for x in weights]
                            firedWorkers = np.random.choice(dismissableWorkers, numLayOffs, replace = False, p = probs)
                            self.dismissWorkers(firedWorkers)
                            # self.newUnemployed.extend(firedWorkers)
                            for person in firedWorkers:
                                person.unemploymentIndex = ageSES_ur
                    
                    # agePop = [x for x in activePop if x.classRank == c and self.ageBand(x.age) == b]
                    empiricalUnemployed = int(float(len(agePop))*ageSES_ur)
                    actualUnemployed = [x for x in agePop if x.status == 'unemployed']
                    employedWorkers = [x for x in agePop if x.status == 'worker']
                    if len(actualUnemployed) > empiricalUnemployed:
                        peopleToHire = len(actualUnemployed)-empiricalUnemployed
                        # The probability to be hired is iversely proportional to unemployment duration.
                        # Order workers from lower to higher duration, and hire from the top.
                        actualUnemployed.sort(key=operator.attrgetter("unemploymentDuration"))
                        peopleHired = actualUnemployed[:peopleToHire]
                        self.assignJobs(peopleHired, month)
                        
    #                    weights = [1.0/np.exp(self.p['hiringBeta']*x.unemploymentDuration) for x in actualUnemployed]
    #                    probs = [x/sum(weights) for x in weights]
    #                    peopleHired = np.random.choice(actualUnemployed, peopleToHire, replace = False, p = probs)
                        
                        for person in peopleHired:
                            person.unemploymentIndex = ageSES_ur
                    
                    elif empiricalUnemployed > len(actualUnemployed):
                        employedWorkers = [x for x in agePop if x.status == 'worker']
                        peopleToFire = min(empiricalUnemployed-len(actualUnemployed), len(employedWorkers))
                        weights = [1.0/np.exp(self.p['layOffsBeta']*x.jobTenure) for x in employedWorkers]
                        probs = [x/sum(weights) for x in weights]
                        firedWorkers = np.random.choice(employedWorkers, peopleToFire, replace = False, p = probs)
                        self.dismissWorkers(firedWorkers)
                        for person in firedWorkers:
                            person.unemploymentIndex = ageSES_ur
        
        # print 'Number hired people: ' + str(len(self.hiredPeople))
        unemployedPop = [x for x in self.pop.livingPeople if x.status == 'unemployed']
        print 'Numer unemployed: ' + str(len(unemployedPop))
        print 'Empirical unemployed: ' + str(int(float(len(activePop))*unemploymentRate))
        print 'Simulation unemployment rate: ' + str(float(len(unemployedPop))/float(len(activePop)))
        print 'Unemployed among not active: ' + str(len(unemployedNotInActive))
        # self.assignJobs(self.hiredPeople)
        
        tempJS = [0]*24
        for agent in self.hiredPeople:
            for i in range(7):
                if i+1 not in agent.daysOff:
                    for j in range(24):
                        tempJS[j] += agent.jobSchedule[i][j]
                    
        # hoursFrequencies = [x for x in self.aggregateSchedule]
        print 'Hours frequencies (temp): ' + str(tempJS)
        
        # self.dismissWorkers(self.newUnemployed)
        
    
    def computeUR(self, ur, classShares, ageShares, classBias, ageBias, classGroup, ageGroup):
        a = 0
        for i in range(int(self.p['numberClasses'])):
            a += classShares[i]*math.pow(classBias, i)
        lowClassRate = ur/a
        classRate = lowClassRate*math.pow(classBias, classGroup)
        a = 0
        for i in range(int(self.p['numberAgeBands'])):
            a += ageShares[i]*ageBias[i]
        if a > 0:
            lowerAgeBandRate = classRate/a 
        else:
            lowerAgeBandRate = 0
        unemploymentRate = lowerAgeBandRate*ageBias[ageGroup]
        return unemploymentRate
    
    def ageBand(self, age):
        if age <= 19:
            band = 0
        elif age >= 20 and age <= 24:
            band = 1
        elif age >= 25 and age <= 34:
            band = 2
        elif age >= 35 and age <= 44:
            band = 3
        elif age >= 45 and age <= 54:
            band = 4
        else: 
            band = 5
        return (band)
        
    
    
    def updateIncome(self, person):

        if person.status == 'worker' and person.careNeedLevel < 2:
            person.workExperience *= self.p['workDiscountingTime']
            if person.maternityStatus == False:
                if self.p['weeklyHours'][person.careNeedLevel] > 0:
                    person.workingPeriods += float(self.p['weeklyHours'][person.careNeedLevel])/40.0
                    person.workExperience += person.residualWorkingHours/40.0
                person.wage = self.computeWage(person)
                person.income = person.wage*person.residualWorkingHours   # self.p['weeklyHours'][int(person.careNeedLevel)]
                person.previousIncome = person.income
                person.lastIncome = person.income
            elif person.maternityStatus == True:
                person.wage = 0
                maternityIncome = self.p['maternityLeaveIncomeReduction']*person.previousIncome
                if person.monthsSinceBirth > 2:
                    maternityIncome = min(self.p['minStatutoryMaternityPay'], maternityIncome)
                person.income = maternityIncome
               
        elif person.age == self.p['ageOfRetirement'] or person.careNeedLevel > 1:
            person.wage = 0
            shareWorkingTime = person.workingPeriods/float(self.p['minContributionPeriods'])
            dK = np.random.normal(0, self.p['wageVar'])
#                averageIncome = 0
#                if person.workingPeriods > 0:
#                    averageIncome = person.cumulativeIncome/person.workingPeriods
            person.income = person.lastIncome*shareWorkingTime*math.exp(dK) #self.p['pensionWage'][person.classRank]*self.p['weeklyHours'][0]
            
#                if person.income < self.p['statePension']:
#                    person.income = self.p['statePension']
        person.cumulativeIncome += (person.income - person.incomeExpenses)
        person.cumulativeIncome = max(person.cumulativeIncome, 0)
        
    def computeTax(self):
        
        self.grossDomesticProduct = sum([x.income for x in self.pop.livingPeople if x.wage > 0])
        
        for house in self.map.occupiedHouses:
            house.outOfWorkSocialCare = sum([x.outOfWorkSocialCare for x in house.occupants])
            house.householdIncome = sum([x.income for x in house.occupants])
            house.incomePerCapita = house.householdIncome/float(len(house.occupants))
           
        households = [x for x in self.map.occupiedHouses]
        households.sort(key=operator.attrgetter("incomePerCapita"))
        for i in range(5):
            number = int(round(len(households)/(5.0-float(i))))
            quintile = households[:number]
            for j in quintile:
                j.incomeQuintile = i
            households = [x for x in households if x not in quintile]
 
        # Compute tax revenue and income after tax
        earningPeople = [x for x in self.pop.livingPeople if x.status == 'worker' and x.maternityStatus == False]
        self.totalTaxRevenue = 0
        self.totalPensionRevenue = 0
        for person in earningPeople:
            employeePensionContribution = 0
            # Pension Contributions
            if person.income > 162.0:
                if person.income < 893.0:
                    employeePensionContribution = (person.income - 162.0)*0.12
                else:
                    employeePensionContribution = (893.0 - 162.0)*0.12
                    employeePensionContribution += (person.income - 893.0)*0.02
            person.income -= employeePensionContribution
            self.totalPensionRevenue += employeePensionContribution
            
            # Tax Revenues
            tax = 0
            residualIncome = person.income
            for i in range(len(self.p['taxBrackets'])):
                if residualIncome > self.p['taxBrackets'][i]:
                    taxable = residualIncome - self.p['taxBrackets'][i]
                    tax += taxable*self.p['taxationRates'][i]
                    residualIncome -= taxable
            person.income -= tax
            self.totalTaxRevenue += tax
        self.statePensionRevenue.append(self.totalPensionRevenue)
        self.stateTaxRevenue.append(self.totalTaxRevenue)
        
        # Pensions Expenditure
        pensioners = [x for x in self.pop.livingPeople if x.status == 'retired']
        totalIncome = sum([x.income for x in earningPeople if x.status == 'worker'])
        self.pensionExpenditure = self.p['statePension']*len(pensioners) + totalIncome*self.p['statePensionContribution']
        self.statePensionExpenditure.append(self.pensionExpenditure)
    
    # Debugg benefit allocation process
    def computeBenefits(self):
        
        # Reset counters
        for agent in self.pop.livingPeople:
            agent.benefits = 0
            agent.highestDisabilityBenefits = False
            agent.ucBenefits = False
        
        
        self.childBenefits()
        
        self.disabilityBenefits()
        
        self.universalCredit()
        
        self.pensionCredit()
            
    def childBenefits(self):
        self.aggregateChildBenefits = 0
        parents = [x for x in self.pop.livingPeople if x.independentStatus == True]
        for parent in parents:
            dependentMembers = [x for x in parent.house.occupants if x.age < 16 or (x.age < 20 and x.status == 'student')]
            if len(dependentMembers) > 0:
                totChildBenefit = 0
                if parent.partner == None:
                    if parent.income < self.p['childBenefitIncomeThreshold']:
                        totChildBenefit = self.p['firstChildBenefit']
                        totChildBenefit += self.p['otherChildrenBenefit']*float(len(dependentMembers)-1)
                else:
                    if parent.income < self.p['childBenefitIncomeThreshold'] or parent.partner.income < self.p['childBenefitIncomeThreshold']:
                        totChildBenefit = self.p['firstChildBenefit']/2.0
                        totChildBenefit += self.p['otherChildrenBenefit']*float(len(dependentMembers)-1)/2.0
                parent.benefits += totChildBenefit
                self.aggregateChildBenefits += totChildBenefit
        print 'Total child benefits: ' + str(self.aggregateChildBenefits)
        
    
    def disabilityBenefits(self):
        
        self.aggregateDisabledChildrenBenefits = 0
        self.aggregatePIP = 0
        self.aggregateAttendanceAllowance = 0
        self.aggregateCarersAllowance = 0
        
        disabledChildren = [x for x in self.pop.livingPeople if x.age < 16 and x.careNeedLevel > 0]
        for child in disabledChildren:
            disabledChildBenefit = 0
            if child.careNeedLevel == 1:
                disabledChildBenefit = self.p['careDLA'][0]+self.p['mobilityDLA'][0]
            elif child.careNeedLevel == 2:
                disabledChildBenefit = self.p['careDLA'][1]+self.p['mobilityDLA'][0]
            elif child.careNeedLevel == 3:
                disabledChildBenefit = self.p['careDLA'][1]+self.p['mobilityDLA'][1]
            else:
                disabledChildBenefit = self.p['careDLA'][2]+self.p['mobilityDLA'][1]
                child.highestDisabilityBenefits = True
            child.benefits += disabledChildBenefit
            self.aggregateDisabledChildrenBenefits += disabledChildBenefit
            
        ## PIP
        disabledAdults = [x for x in self.pop.livingPeople if x.age >= 16 and x.age < self.p['ageOfRetirement'] and x.careNeedLevel > 0]
        for agent in disabledAdults:
            disabledAdultBenefit = 0
            if agent.careNeedLevel == 1:
                disabledAdultBenefit = self.p['carePIP'][0]
            elif agent.careNeedLevel == 2:
                disabledAdultBenefit = self.p['carePIP'][0]+self.p['mobilityPIP'][0]
            elif agent.careNeedLevel == 3:
                disabledAdultBenefit = self.p['carePIP'][1]+self.p['mobilityPIP'][0]
                agent.highestDisabilityBenefits = True
            else:
                disabledAdultBenefit = self.p['carePIP'][1]+self.p['mobilityPIP'][1]
                agent.highestDisabilityBenefits = True
            agent.benefits += disabledAdultBenefit
            self.aggregatePIP += disabledAdultBenefit
                
        ## Attendance Allowance
        disabledPensioners = [x for x in self.pop.livingPeople if x.age >= self.p['ageOfRetirement'] and x.careNeedLevel > 2]
        for agent in disabledPensioners:
            disabledPensionerBenefit = 0
            if agent.careNeedLevel == 3:
                disabledPensionerBenefit = self.p['careAA'][0]
            else:
                disabledPensionerBenefit = self.p['careAA'][1]
            agent.benefits += disabledPensionerBenefit
            self.aggregateAttendanceAllowance += disabledPensionerBenefit
            
        ## Carers' Allowance
        fullTimeCarers = [x for x in self.pop.livingPeople if x.socialWork >= 35]
        for agent in fullTimeCarers:
            agent.benefits += self.p['carersAllowance']
            self.aggregateCarersAllowance += self.p['carersAllowance']
        
        print 'Total disabled children benefits: ' + str(self.aggregateDisabledChildrenBenefits)
        print 'Total disabled adults benefits: ' + str(self.aggregatePIP)
        print 'Total disabled retired benefits: ' + str(self.aggregateAttendanceAllowance)
        print 'Total disabled carers benefits: ' + str(self.aggregateCarersAllowance)
        
    
    def universalCredit(self):
        print 'Work in progress....'
        self.aggregateUC = 0
        self.aggregateHousingElement = 0
        # Condition 1: age between 18 and 64
        # Condition 2: low income or unemployed
        # Condition 3: Savings less than 16000
        ucAgeBand = [x for x in self.pop.livingPeople if x.age >= 18 and x.age < self.p['ageOfRetirement']]
        ucPopulation = [x for x in ucAgeBand if x.status == 'worker' or x.status == 'unemployed']
        
        for agent in ucPopulation:
            self.computeUC(agent)
                    
        students = [x for x in ucAgeBand if x.status == 'student']
        studentWithChildren = [x for x in students if len([y for y in x.children if x.house == y.house]) > 0]
        pensionersStudents = [x for x in students if x.age >= self.p['ageOfRetirement'] and x not in studentWithChildren]
        allStudents = studentWithChildren+pensionersStudents
        studentsWithUCPartner = [x for x in students if x.partner != None and x.partner.ucBenefits == True and x not in allStudents]
        allStudents += studentsWithUCPartner
        disabledStudents = [x for x in students if x.careNeedLevel > 0 and x not in allStudents]
        allStudents += disabledStudents
        
        for student in allStudents:
            self.computeUC(student)
        
        under18s = [x for x in self.pop.livingPeople if x.age >= 16 and x.age < 18 and x not in allStudents]
        loneStudents = [x for x in under18s if x.status == 'student' and x.mother.dead == True and x.father.dead == True]
        caringUnder18s = [x for x in under18s if x.socialWork >= 35 and x not in loneStudents]
        allUnder18s = caringUnder18s+loneStudents
        under18sWitChild = [x for x in under18s if x.independentStatus == True and len([y for y in x.children if x.house == y.house]) > 0 and x not in allUnder18s]
        allUnder18s += under18sWitChild
        
        for under18 in allUnder18s:
            self.computeUC(under18)
        
        print 'Total Universal Credit: ' + str(self.aggregateUC)
        
        # Housing element (for renters): LHA rate based on household composition (number of rooms).
        # 1 room for each of the following:
        # The household's head and partner
        # Any other person over 16, as long as they aren't living with you as your tenant
        # Two children under 16 of the same gender
        # Two children under 10
        # Any other child under 16
        ucRecipients = [x for x in self.pop.livingPeople if x.ucBenefits == True]
        rentingRecipients = [x for x in ucRecipients if x.independentStatus == True and x.house.ownedByOccupants == False]
        for agent in rentingRecipients:
            if agent.partner == None or agent.partner.ucBenefits == False:
                agent.benefits += agent.house.town.LHA[self.computeMaxRooms([agent]) - 1]
                self.aggregateHousingElement += agent.house.town.LHA[self.computeMaxRooms([agent]) - 1]
            else:
                agent.benefits += agent.house.town.LHA[self.computeMaxRooms([agent, agent.partner]) - 1]/2.0
                self.aggregateHousingElement += agent.house.town.LHA[self.computeMaxRooms([agent, agent.partner]) - 1]/2.0
                
    
    def computeUC(self, agent):
        if agent.partner == None:
            if agent.financialWealth < self.p['capitalHighThreshold']:
                ucIncome = agent.income + max(math.floor((agent.financialWealth-self.p['capitalLowThreshold'])/self.p['savingUCRate']), 0.0)*self.p['capitalIncome']
                youngMembers = [x for x in agent.house.occupants if x.age < 16 or (x.age < 20 and x.status == 'student')]
                if (agent.independentStatus == True and len(youngMembers) > 0) or agent.careNeedLevel > 0:
                    if agent.house.ownedByOccupants == False: # Assuming the agent will get the Housing Cost element
                        ucIncome = max(ucIncome-self.p['workAllowanceHS'], 0.0)
                    else:
                        ucIncome = max(ucIncome-self.p['workAllowanceNoHS'], 0.0)
                ucReduction = ucIncome*self.p['incomeReduction']
                benefit = 0
                if agent.age < 25:
                    benefit = max(self.p['sigleBelow25']-ucReduction, 0.0)
                    if benefit > 0:
                        agent.ucBenefits = True
                else:
                    benefit = max(self.p['single25Plus']-ucReduction, 0.0)
                    if benefit > 0:
                        agent.ucBenefits = True
                agent.benefits += benefit
                self.aggregateUC += benefit
                
                # Extra for children
                dependentMembers = [x for x in agent.house.occupants if x.age < 16 or (x.age < 20 and x.status == 'student')]
                numChildBenefits = min(len(dependentMembers), 2)
                benefit = self.p['eaChildren']*numChildBenefits
                agent.benefits += benefit
                self.aggregateUC += benefit
                if benefit > 0:
                    agent.ucBenefits = True
                
                # Extra for disabled children
                mildlyDisabledDependent = [x for x in dependentMembers if x.careNeedLevel > 0 and x.highestDisabilityBenefits == False]
                totalDisabledChildBenefits = self.p['eaDisabledChildren'][0]*float(len(mildlyDisabledDependent))
                agent.benefits += totalDisabledChildBenefits
                self.aggregateUC += totalDisabledChildBenefits
                if totalDisabledChildBenefits > 0:
                    agent.ucBenefits = True
                    
                criticallyDisabledDependent = [x for x in dependentMembers if x.highestDisabilityBenefits == True]
                totalDisabledChildBenefits = self.p['eaDisabledChildren'][1]*float(len(criticallyDisabledDependent))
                agent.benefits += totalDisabledChildBenefits
                self.aggregateUC += totalDisabledChildBenefits
                if totalDisabledChildBenefits > 0:
                    agent.ucBenefits = True
                
                # Extra for disability
                if agent.careNeedLevel > 1:
                    agent.benefits += self.p['lcfwComponent'] # limited capability for work and work-related activity
                    self.aggregateUC += self.p['lcfwComponent']
                    agent.ucBenefits = True
                    
                # Extra for social work
                if agent.socialWork > 35:
                    agent.benefits += self.p['carersComponent']
                    self.aggregateUC += self.p['carersComponent']
                    agent.ucBenefits = True
        else:
            totalWealth = agent.financialWealth+agent.partner.financialWealth
            if totalWealth < self.p['capitalHighThreshold']:
                totalIncome = agent.income + agent.partner.income
                ucIncome = totalIncome + max(math.floor((totalWealth-self.p['capitalLowThreshold'])/self.p['savingUCRate']), 0.0)*self.p['capitalIncome']
                youngMembers = [x for x in agent.house.occupants if x.age < 16 or (x.age < 20 and x.status == 'student')]
                if (agent.independentStatus == True and len(youngMembers) > 0) or agent.careNeedLevel > 0:
                    if agent.house.ownedByOccupants == False: # Assuming the agent will get the Housing Cost element
                        ucIncome = max(ucIncome-self.p['workAllowanceHS'], 0.0)
                    else:
                        ucIncome = max(ucIncome-self.p['workAllowanceNoHS'], 0.0)
                ucReduction = ucIncome*self.p['incomeReduction']
                benefit = 0
                if agent.age < 25 and agent.partner.age < 25:
                    benefit = max(self.p['coupleBelow25']-ucReduction, 0.0)/2.0
                    if benefit > 0:
                        agent.ucBenefits = True
                else:
                    benefit = max(self.p['couple25Plus']-ucReduction, 0.0)/2.0
                    if benefit > 0:
                        agent.ucBenefits = True
                agent.benefits += benefit
                self.aggregateUC += benefit
                # Extra for children
                dependentMembers = [x for x in agent.house.occupants if x.age < 16 or (x.age < 20 and x.status == 'student')]
                numChildBenefits = min(len(dependentMembers), 2)
                benefit = self.p['eaChildren']*numChildBenefits
                agent.benefits += benefit/2.0
                self.aggregateUC += benefit/2.0
                if benefit > 0:
                    agent.ucBenefits = True
                
                # Extra for disabled children
                mildlyDisabledDependent = [x for x in dependentMembers if x.careNeedLevel > 0 and x.highestDisabilityBenefits == False]
                totalDisabledChildBenefits = self.p['eaDisabledChildren'][0]*float(len(mildlyDisabledDependent))
                agent.benefits += totalDisabledChildBenefits/2.0
                self.aggregateUC += totalDisabledChildBenefits/2.0
                if totalDisabledChildBenefits > 0:
                    agent.ucBenefits = True
                    
                criticallyDisabledDependent = [x for x in dependentMembers if x.highestDisabilityBenefits == True]
                totalDisabledChildBenefits = self.p['eaDisabledChildren'][1]*float(len(criticallyDisabledDependent))
                agent.benefits += totalDisabledChildBenefits/2.0
                self.aggregateUC += totalDisabledChildBenefits/2.0
                
                if totalDisabledChildBenefits > 0:
                    agent.ucBenefits = True
                
                # Extra for disability
                if agent.careNeedLevel > 1:
                    agent.benefits += self.p['lcfwComponent'] # limited capability for work and work-related activity
                    self.aggregateUC += self.p['lcfwComponent']
                    agent.ucBenefits = True
                    
                # Extra for social work
                if agent.socialWork > 35:
                    agent.benefits += self.p['carersComponent']
                    self.aggregateUC += self.p['carersComponent']
                    agent.ucBenefits = True
        
        
    def pensionCredit(self):
        print 'Work in progress....'
        self.aggregatePensionCredit = 0
        # Condition 1: 65 or older (both, if a couple)
        pensioners = [x for x in self.pop.livingPeople if x.age >= self.p['ageOfRetirement']]
        for agent in pensioners:
            agent.guaranteeCredit = False
            agent.houseBenefit = False
            if agent.partner == None:
                benefitIncome = agent.income + max(math.floor((agent.financialWealth-self.p['wealthAllowancePC'])/self.p['savingIncomeRatePC']), 0.0)
                agent.benefits += max(self.p['singlePC']-benefitIncome, 0)
                self.aggregatePensionCredit += max(self.p['singlePC']-benefitIncome, 0)
                if max(self.p['singlePC']-benefitIncome, 0) > 0:
                    agent.guaranteeCredit = True
            elif agent.partner.age >= self.p['ageOfRetirement']:
                totalIncome = agent.income+agent.partner.income
                totalWealth = agent.financialWealth+agent.partner.financialWealth
                aggregateBenefitIncome = totalIncome + max(math.floor((totalWealth-self.p['wealthAllowancePC'])/self.p['savingIncomeRatePC']), 0.0)
                agent.benefits += max(self.p['couplePC']-aggregateBenefitIncome, 0)/2.0
                self.aggregatePensionCredit += max(self.p['couplePC']-aggregateBenefitIncome, 0)/2.0
                if max(self.p['couplePC']-aggregateBenefitIncome, 0)/2.0 > 0:
                    agent.guaranteeCredit = True
            ## Severe disability extra
            if agent.careNeedLevel > 2:
                agent.benefits += self.p['disabilityComponentPC']
                self.aggregatePensionCredit += self.p['disabilityComponentPC']
                agent.guaranteeCredit = True
            if agent.socialWork >= 35:
                agent.benefits += self.p['caringComponentPC']
                self.aggregatePensionCredit += self.p['caringComponentPC']
                agent.guaranteeCredit = True
            if agent.independentStatus == True:
                dependentMembers = [x for x in agent.house.occupants if x.age < 16 or (x.age < 20 and x.status == 'student')]
                if len(dependentMembers) > 0:
                    totalChildBenefit = self.p['childComponentPC']*float(len(dependentMembers))
                    if agent.partner == None:
                        agent.benefits += totalChildBenefit
                        self.aggregatePensionCredit += totalChildBenefit
                        agent.guaranteeCredit = True
                    elif agent.partner.age >= self.p['ageOfRetirement']:
                        agent.benefits += totalChildBenefit/2.0
                        self.aggregatePensionCredit += totalChildBenefit/2.0
                        agent.guaranteeCredit = True
                    # Disabled children
                    mildlyDisabledDependent = [x for x in dependentMembers if x.careNeedLevel > 0 and x.highestDisabilityBenefits == False]
                    totalDisabledChildBenefits = self.p['disabledChildComponent'][0]*float(len(mildlyDisabledDependent))
                    if agent.partner == None:
                        agent.benefits += totalDisabledChildBenefits
                        self.aggregatePensionCredit += totalDisabledChildBenefits
                        agent.guaranteeCredit = True
                    elif agent.partner.age >= self.p['ageOfRetirement']:
                        agent.benefits += totalDisabledChildBenefits/2.0
                        self.aggregatePensionCredit += totalDisabledChildBenefits/2.0
                        agent.guaranteeCredit = True
                    criticallyDisabledDependent = [x for x in dependentMembers if x.highestDisabilityBenefits == True]
                    totalDisabledChildBenefits = self.p['disabledChildComponent'][1]*float(len(criticallyDisabledDependent))
                    if agent.partner == None:
                        agent.benefits += totalDisabledChildBenefits
                        self.aggregatePensionCredit += totalDisabledChildBenefits
                        agent.guaranteeCredit = True
                    elif agent.partner.age >= self.p['ageOfRetirement']:
                        agent.benefits += totalDisabledChildBenefits/2.0
                        self.aggregatePensionCredit += totalDisabledChildBenefits/2.0
                        agent.guaranteeCredit = True
        # Housing benefit (for renters): LHA rate based on household composition (number of rooms).
        # 1 room for each of the following:
        # The household's head and partner
        # Any other person over 16, as long as they aren't living with you as your tenant
        # Two children under 16 of the same gender
        # Two children under 10
        # Any other child under 16
        for agent in [x for x in pensioners if x.independentStatus == True and x.house.ownedByOccupants == False]:
            if agent.partner == None:
                if agent.financialWealth < self.p['housingBenefitWealthThreshold'] or agent.guaranteeCredit == True:
                    agent.benefits += agent.house.town.LHA[self.computeMaxRooms([agent]) - 1]
                    self.aggregateHousingElement += agent.house.town.LHA[self.computeMaxRooms([agent]) - 1]
            elif agent.partner.age >= self.p['ageOfRetirement']:
                totalWealth = agent.financialWealth+agent.partner.financialWealth
                if totalWealth < self.p['housingBenefitWealthThreshold'] or agent.guaranteeCredit == True:
                    agent.benefits += agent.house.town.LHA[self.computeMaxRooms([agent, agent.partner]) - 1]/2.0
                    self.aggregateHousingElement += agent.house.town.LHA[self.computeMaxRooms([agent, agent.partner]) - 1]/2.0
                    
        print 'Total pension credit: ' + str(self.aggregatePensionCredit)
        print 'Total housing element: ' + str(self.aggregateHousingElement)
        
        
    def computeMaxRooms(self, agents):
        allowedRooms = 1
        house = agents[0].house
        residualMembers = [x for x in house.occupants if x not in agents]
        over16 = [x for x in residualMembers if x.age >= 16]
        allowedRooms += len(over16)
        residualMembers = [x for x in residualMembers if x not in over16]
        maleTeenagers = [x for x in residualMembers if x.age >= 10 and x.age < 16 and x.sex == 'male']
        additionalRooms = int(float(len(maleTeenagers))/2.0)
        allowedRooms += additionalRooms
        allocatedMaleTeenagers = maleTeenagers[:additionalRooms*2]
        residualMembers = [x for x in residualMembers if x not in allocatedMaleTeenagers]
        femaleTeenagers = [x for x in residualMembers if x.age >= 10 and x.age < 16 and x.sex == 'female']
        additionalRooms = int(float(len(femaleTeenagers))/2.0)
        allowedRooms += additionalRooms
        allocatedFemaleTeenagers = femaleTeenagers[:additionalRooms*2]
        residualMembers = [x for x in residualMembers if x not in allocatedFemaleTeenagers]
        under10 = [x for x in residualMembers if x.age < 10]
        additionalRooms = int(float(len(under10))/2.0)
        allowedRooms += additionalRooms
        allocatedUnder10s = under10[:additionalRooms*2]
        residualMembers = [x for x in residualMembers if x not in allocatedUnder10s]
        allowedRooms += len(residualMembers)
        if allowedRooms > 4:
            allowedRooms = 4
        return allowedRooms
        
        
    def updateWealth_Ind(self):
        # Only workers: retired are assigned a wealth at the end of their working life (which they consume thereafter)
        earningPop = [x for x in self.pop.livingPeople if x.cumulativeIncome > 0]
        
        earningPop.sort(key=operator.attrgetter("cumulativeIncome"))
        
        peopleToAssign = list(earningPop)
        wealthPercentiles = []
        for i in range(100, 0, -1):
            groupNum = int(float(len(peopleToAssign))/float(i))
            peopleGroup = peopleToAssign[0:groupNum]
            wealthPercentiles.append(peopleGroup)
            peopleToAssign = peopleToAssign[groupNum:]
            
        for i in range(100):
            wealth = float(self.wealthPercentiles[i])
            for person in wealthPercentiles[i]:
                dK = np.random.normal(0, self.p['wageVar'])
                person.wealth = wealth*math.exp(dK)
                
        for person in self.pop.livingPeople:
            # Update financial wealth
            if person.wage > 0:
                person.financialWealth = person.wealth*self.p['shareFinancialWealth']
            else:
                person.financialWealth -= person.wealthSpentOnCare
            person.financialWealth = max(person.financialWealth, 0)
        
        notEarningPop = [x for x in self.pop.livingPeople if x.cumulativeIncome > 0 and x.wage == 0]
        for person in notEarningPop:
            person.financialWealth *= (1.0 + self.p['pensionReturnRate'])
            
    def updateWealth(self):
        households = [x for x in self.map.occupiedHouses]
        for h in households:
            h.householdCumulativeIncome = sum([x.cumulativeIncome for x in h.occupants])
        households.sort(key=operator.attrgetter("householdCumulativeIncome"))
        
        householdsToAssign = list(households)
        wealthPercentiles = []
        for i in range(100, 0, -1):
            groupNum = int(float(len(householdsToAssign))/float(i))
            householdGroup = householdsToAssign[0:groupNum]
            wealthPercentiles.append(householdGroup)
            householdsToAssign = householdsToAssign[groupNum:]
            
        for i in range(100):
            wealth = float(self.wealthPercentiles[i])
            for household in wealthPercentiles[i]:
                dK = np.random.normal(0, self.p['wageVar'])
                household.wealth = wealth*math.exp(dK)
        
        # Assign household wealth to single members
        for h in households:
            if h.householdCumulativeIncome > 0:
                earningMembers = [x for x in h.occupants if x.cumulativeIncome > 0]
                for m in earningMembers:
                    m.wealth = (m.cumulativeIncome/h.householdCumulativeIncome)*h.wealth
            else:
                independentMembers = [x for x in h.occupants if x.independentStatus == True]
                if len(independentMembers) > 0:
                    for m in independentMembers:
                        m.wealth = h.wealth/float(len(independentMembers))
    
    def computeBirthProb(self, fertilityBias, rawRate, womanRank):
        womenOfReproductiveAge = [x for x in self.pop.livingPeople
                                  if x.sex == 'female' and x.age >= self.p['minPregnancyAge']]
        womanClassShares = []
        womanClassShares.append(len([x for x in womenOfReproductiveAge if x.classRank == 0])/float(len(womenOfReproductiveAge)))
        womanClassShares.append(len([x for x in womenOfReproductiveAge if x.classRank == 1])/float(len(womenOfReproductiveAge)))
        womanClassShares.append(len([x for x in womenOfReproductiveAge if x.classRank == 2])/float(len(womenOfReproductiveAge)))
        womanClassShares.append(len([x for x in womenOfReproductiveAge if x.classRank == 3])/float(len(womenOfReproductiveAge)))
        womanClassShares.append(len([x for x in womenOfReproductiveAge if x.classRank == 4])/float(len(womenOfReproductiveAge)))
        a = 0
        for i in range(int(self.p['numberClasses'])):
            a += womanClassShares[i]*math.pow(self.p['fertilityBias'], i)
        baseRate = rawRate/a
        birthProb = baseRate*math.pow(self.p['fertilityBias'], womanRank)
        return birthProb
    
    def doBirths(self, policyFolder, month):
        
        preBirth = len(self.pop.livingPeople)
        
        marriedLadies = 0
        adultLadies = 0
        births = [0, 0, 0, 0, 0]
        marriedPercentage = []
        
        allFemales = [x for x in self.pop.livingPeople if x.sex == 'female']
        adultWomen = [x for x in self.pop.livingPeople if x.sex == 'female' and x.age >= self.p['minPregnancyAge']]
        notFertiledWomen = [x for x in adultWomen if x.age > self.p['maxPregnancyAge']]
        
        print 'Number of adult women: ' + str(len(allFemales))
        print 'Number of adult women: ' + str(len(adultWomen))
        print 'Not fertile women: ' + str(len(notFertiledWomen))
        
        womenOfReproductiveAgeButNotMarried = [x for x in self.pop.livingPeople
                                  if x.sex == 'female'
                                  and x.age >= self.p['minPregnancyAge']
                                  and x.age <= self.p['maxPregnancyAge']
                                  and x.partner == None]
        
        print 'Not married fertile women: ' + str(len(womenOfReproductiveAgeButNotMarried))
        
        womenOfReproductiveAge = [x for x in self.pop.livingPeople
                                  if x.sex == 'female'
                                  and x.age >= self.p['minPregnancyAge']
                                  and x.age <= self.p['maxPregnancyAge']
                                  and x.partner != None]
        
        adultLadies_1 = [x for x in adultWomen if x.classRank == 0]   
        marriedLadies_1 = len([x for x in adultLadies_1 if x.partner != None])
        if len(adultLadies_1) > 0:
            marriedPercentage.append(marriedLadies_1/float(len(adultLadies_1)))
        else:
            marriedPercentage.append(0)
        adultLadies_2 = [x for x in adultWomen if x.classRank == 1]    
        marriedLadies_2 = len([x for x in adultLadies_2 if x.partner != None])
        if len(adultLadies_2) > 0:
            marriedPercentage.append(marriedLadies_2/float(len(adultLadies_2)))
        else:
            marriedPercentage.append(0)
        adultLadies_3 = [x for x in adultWomen if x.classRank == 2]   
        marriedLadies_3 = len([x for x in adultLadies_3 if x.partner != None]) 
        if len(adultLadies_3) > 0:
            marriedPercentage.append(marriedLadies_3/float(len(adultLadies_3)))
        else:
            marriedPercentage.append(0)
        adultLadies_4 = [x for x in adultWomen if x.classRank == 3]  
        marriedLadies_4 = len([x for x in adultLadies_4 if x.partner != None])   
        if len(adultLadies_4) > 0:
            marriedPercentage.append(marriedLadies_4/float(len(adultLadies_4)))
        else:
            marriedPercentage.append(0)
        adultLadies_5 = [x for x in adultWomen if x.classRank == 4]   
        marriedLadies_5 = len([x for x in adultLadies_5 if x.partner != None]) 
        if len(adultLadies_5) > 0:
            marriedPercentage.append(marriedLadies_5/float(len(adultLadies_5)))
        else:
            marriedPercentage.append(0)
        
        # print(marriedPercentage)
        
#        for person in self.pop.livingPeople:
#           
#            if person.sex == 'female' and person.age >= self.p['minPregnancyAge']:
#                adultLadies += 1
#                if person.partner != None:
#                    marriedLadies += 1
#        marriedPercentage = float(marriedLadies)/float(adultLadies)
        
        print 'Number of reproductive women: ' + str(len(womenOfReproductiveAge))
        
        for woman in womenOfReproductiveAge:
            
            womanClassRank = woman.classRank
            if woman.status == 'student':
                womanClassRank = woman.parentsClassRank

            if self.year < 1951:
                rawRate = self.p['growingPopBirthProb']
                birthProb = self.computeBirthProb(self.p['fertilityBias'], rawRate, womanClassRank)
            else:
                rawRate = self.fert_data[(self.year - woman.birthdate)-16, self.year-1950]
                birthProb = self.computeBirthProb(self.p['fertilityBias'], rawRate, womanClassRank)/marriedPercentage[womanClassRank]
                
            # birthProb = self.computeBirthProb(self.p['fertilityBias'], rawRate, woman.classRank)
            
            #baseRate = self.baseRate(self.socialClassShares, self.p['fertilityBias'], rawRate)
            #fertilityCorrector = (self.socialClassShares[woman.classRank] - self.p['initialClassShares'][woman.classRank])/self.p['initialClassShares'][woman.classRank]
            #baseRate *= 1/math.exp(self.p['fertilityCorrector']*fertilityCorrector)
            #birthProb = baseRate*math.pow(self.p['fertilityBias'], woman.classRank)
            if birthProb <= 0.0:
                print 'Error: birth prob is zeo/negative!'
                sys.exit()
                
            if np.random.random() < birthProb and np.random.choice([x+1 for x in range(12)]) == month:
                # (self, mother, father, age, birthYear, sex, status, house,
                # classRank, sec, edu, wage, income, finalIncome):
                parentsClassRank = max([woman.classRank, woman.partner.classRank])
                baby = Person(woman, woman.partner, self.year, 0, 'random', woman.house, woman.sec, -1, parentsClassRank, 0, 0, 0, 0, 0, 0, 'child', False, 0, month)
                self.pop.allPeople.append(baby)
                self.pop.livingPeople.append(baby)
                woman.house.occupants.append(baby)
                woman.children.append(baby)
                woman.partner.children.append(baby)
                woman.maternityStatus = True
                # woman.weeklyTime = [[0]*12+[1]*12, [0]*12+[1]*12, [0]*12+[1]*12, [0]*12+[1]*12, [0]*12+[1]*12, [0]*12+[1]*12, [0]*12+[1]*12]
                woman.weeklyTime = [[1]*24, [1]*24, [1]*24, [1]*24, [1]*24, [1]*24, [1]*24]
                woman.workingHours = 0
                woman.maxWeeklySupplies = [0, 0, 0, 0]
                woman.residualDailySupplies = [0]*7
                woman.residualWeeklySupplies = [x for x in woman.maxWeeklySupplies]
                woman.residualWorkingHours = 0
                woman.availableWorkingHours = 0
                woman.potentialIncome = 0
                woman.income = 0
                if woman.house == self.displayHouse:
                    messageString = str(self.year) + ": #" + str(woman.id) + " had a baby, #" + str(baby.id) + "." 
                    self.textUpdateList.append(messageString)
                    
                    with open(os.path.join(policyFolder, "Log.csv"), "a") as file:
                        writer = csv.writer(file, delimiter = ",", lineterminator='\r')
                        writer.writerow([self.year, messageString])
                    
        postBirth = len(self.pop.livingPeople)
        numberBirths = postBirth - preBirth
        print 'The number of births is: ' + str(numberBirths)
        
    
    def computeSplitProb(self, rawRate, classRank):
        a = 0
        for i in range(int(self.p['numberClasses'])):
            a += self.socialClassShares[i]*math.pow(self.p['divorceBias'], i)
        baseRate = rawRate/a
        splitProb = baseRate*math.pow(self.p['divorceBias'], classRank)
        return splitProb
            
    def doDivorces(self, policyFolder, month):
        menInRelationships = [x for x in self.pop.livingPeople if x.sex == 'male' and x.partner != None ]
        for man in menInRelationships:
            
            age = self.year - man.birthdate 

            ## This is here to manage the sweeping through of this parameter
            ## but only for the years after 2012
            if self.year < self.p['thePresent']:
                rawRate = self.p['basicDivorceRate'] * self.p['divorceModifierByDecade'][int(age)/10]
            else:
                rawRate = self.p['variableDivorce'] * self.p['divorceModifierByDecade'][int(age)/10]
                
            splitProb = self.computeSplitProb(rawRate, man.classRank)
                
            if np.random.random() < splitProb and np.random.choice([x+1 for x in range(12)]) == month:
                # man.children = []
                wife = man.partner
                man.partner = None
                wife.partner = None
                man.yearDivorced.append(self.year)
                wife.yearDivorced.append(self.year)
                if wife.status == 'student':
                    wife.independentStatus = True
                    self.startWorking(wife)
                self.divorceTally += 1
                distance = random.choice(['near','far'])
                if man.house == self.displayHouse:
                    messageString = str(self.year) + ": #" + str(man.id) + " splits with #" + str(wife.id) + "."
                    self.textUpdateList.append(messageString)
                    
                    with open(os.path.join(policyFolder, "Log.csv"), "a") as file:
                        writer = csv.writer(file, delimiter = ",", lineterminator='\r')
                        writer.writerow([self.year, messageString])
                    
                # manChildren = [x for x in man.children if x.dead == False and x.house == man.house and x.father == man and x.mother != wife]
                
                manChildren = []
                children = [x for x in man.children if x.dead == False and x.house == man.house]
                for child in children:
                    if child.father == man and child.mother != wife:
                        manChildren.append(child)
                    else:
                        if np.random.random() < self.p['probChildrenWithFather']:
                            manChildren.append(child)
                
#                for x in manChildren:
#                    if x not in man.house.occupants:
#                        print 'Error in doDivorce: man children not in house'
#                        sys.exit()
                        
                peopleToMove = [man]
                peopleToMove += manChildren
                self.findNewHouse(peopleToMove,distance, policyFolder)
                
    def doMarriages(self, policyFolder, month):
        
        # eligibleMen = [x for x in self.pop.livingPeople if x.sex == 'male' and x.partner == None and x.status == 'worker']
        
        eligibleMen = [x for x in self.pop.livingPeople if x.sex == 'male' and x.partner == None and x.age >= self.p['ageOfAdulthood'] and x.careNeedLevel < 4]
        
        notEligibleMen = [x for x in self.pop.livingPeople if x.sex == 'male' and x.partner == None and x.status == 'unemployed']
        eligibleWomen = [x for x in self.pop.livingPeople if x.sex == 'female' and x.partner == None and x.age >= self.p['minPregnancyAge']]
        
        print 'Eligible men: ' + str(len(eligibleMen))
        print 'Not eligible men: ' + str(len(notEligibleMen))
        print 'Eligible women: ' + str(len(eligibleWomen))
        
        menMarried = []
        marriageProbs = []
        if len(eligibleMen) > 0 and len (eligibleWomen) > 0:
            np.random.shuffle(eligibleMen)
            np.random.shuffle(eligibleWomen)
            
#            interestedWomen = []
#            for w in eligibleWomen:
#                womanMarriageProb = self.p['basicFemaleMarriageProb']*self.p['femaleMarriageModifierByDecade'][w.age/10]
#                if np.random.random() < womanMarriageProb:
#                    interestedWomen.append(w)
        
            for man in eligibleMen:
                
                ageClass = int(man.age/10)
                manMarriageProb = self.p['basicMaleMarriageProb']*self.p['maleMarriageModifierByDecade'][ageClass]
                
                if man.status != 'worker' or man.careNeedLevel > 1:
                    manMarriageProb *= self.p['notWorkingMarriageBias']
                
                ageClassPop = [x for x in eligibleMen if int(x.age/10) == ageClass]
                noChildrenMen = [x for x in ageClassPop if len([y for y in x.children if y.dead == False and y.house == x.house]) == 0]
                shareNoChildren = float(len(noChildrenMen))/float(len(ageClassPop))
                den = shareNoChildren + (1-shareNoChildren)*self.p['manWithChildrenBias']
                baseRate = manMarriageProb/den
                if man in noChildrenMen:
                    manMarriageProb = baseRate
                else:
                    manMarriageProb = baseRate*self.p['manWithChildrenBias']
                
#                marriageProbs.append(manMarriageProb)
#                # Adjusting for number of children
#                numChildrenWithMan = len([x for x in man.children if x.house == man.house])
#                childrenFactor = 1/math.exp(self.p['numChildrenExp']*numChildrenWithMan)
#                manMarriageProb *= childrenFactor
                
#                 Adjusting to increase rate
#                 manMarriageProb *= self.p['maleMarriageMultiplier']
                
                
                if np.random.random() < manMarriageProb and np.random.choice(range(1, 13)) == month:
                    
                    menMarried.append(man)
                    
                    potentialBrides = []
                    for woman in eligibleWomen:
                        deltaAge = man.age - woman.age
                        if deltaAge < 10 and deltaAge > -5:
                            if woman.house != man.house:
                                if man.mother != None and woman.mother != None:
                                    if man.mother != woman.mother and man not in woman.children and woman not in man.children:
                                        potentialBrides.append(woman)
                                else:
                                    if man not in woman.children and woman not in man.children:
                                        potentialBrides.append(woman)
                    
                    if len(potentialBrides) > 0:
                        manTown = man.house.town
                        bridesWeights = []
                        for woman in potentialBrides:
                            
                            womanTown = woman.house.town
                            geoDistance = self.manhattanDistance(manTown, womanTown)/float(self.p['mapGridXDimension'] + self.p['mapGridYDimension'])
                            geoFactor = 1/math.exp(self.p['betaGeoExp']*geoDistance)
                            
                            womanRank = woman.classRank
                            studentFactor = 1.0
                            if woman.status == 'student':
                                studentFactor = self.p['studentFactorParam']
                                womanRank = max(woman.father.classRank, woman.mother.classRank)
                            statusDistance = float(abs(man.classRank-womanRank))/float((self.p['numberClasses']-1))
                            if man.classRank < womanRank:
                                betaExponent = self.p['betaSocExp']
                            else:
                                betaExponent = self.p['betaSocExp']*self.p['rankGenderBias']
                            socFactor = 1/math.exp(betaExponent*statusDistance)
                            
                            ageFactor = self.p['deltageProb'][self.deltaAge(man.age-woman.age)]
                            
                            numChildrenWithWoman = len([x for x in woman.children if x.house == woman.house])
                            
                            childrenFactor = 1/math.exp(self.p['bridesChildrenExp']*numChildrenWithWoman)
                            
                            marriageProb = geoFactor*socFactor*ageFactor*childrenFactor*studentFactor
                            
                            bridesWeights.append(marriageProb)
                            
                        if sum(bridesWeights) > 0:
                            bridesProb = [i/sum(bridesWeights) for i in bridesWeights]
                            woman = np.random.choice(potentialBrides, p = bridesProb)
                        else:
                            woman = np.random.choice(potentialBrides)
                        man.partner = woman
                        woman.partner = man
                        man.yearMarried.append(self.year)
                        woman.yearMarried.append(self.year)
                        eligibleWomen.remove(woman)
                        
                        self.marriageTally += 1
                        
                        self.joinCouple([man, woman], policyFolder)
    
                        if man.house == self.displayHouse or woman.house == self.displayHouse:
                            messageString = str(self.year) + ": #" + str(man.id) + " (age " + str(man.age) + ")"
                            messageString += " and #" + str(woman.id) + " (age " + str(woman.age)
                            messageString += ") marry."
                            self.textUpdateList.append(messageString)
                            
                            with open(os.path.join(policyFolder, "Log.csv"), "a") as file:
                                writer = csv.writer(file, delimiter = ",", lineterminator='\r')
                                writer.writerow([self.year, messageString])
                                
            print 'Men actually married: ' + str(len(menMarried))
            if len(marriageProbs) > 0:
                print 'Median probability of marriage: ' + str(np.median(marriageProbs))
        
    def deltaAge(self, dA):
        if dA <= -10 :
            cat = 0
        elif dA >= -9 and dA <= -3:
            cat = 1
        elif dA >= -2 and dA <= 0:
            cat = 2
        elif dA >= 1 and dA <= 4:
            cat = 3
        elif dA >= 5 and dA <= 9:
            cat = 4
        else:
            cat = 5
        return cat

    def joinCouple(self, couple, policyFolder):
        man = couple[0]
        woman = couple[1]
        if np.random.random() < self.p['probApartWillMoveTogether']:
            peopleToMove = couple
            if man.independentStatus == False:
                manChildren = self.bringTheKids(man)
                manChildrenToMove = [x for x in manChildren]
                peopleToMove += manChildrenToMove
            else:
                if len([x for x in man.house.occupants if x.independentStatus == True]) > 1:
                    print 'Error: an independent spouse is already living with an independent agent!'
                    sys.exit()
                peopleToMove += [x for x in man.house.occupants if x != man]
            if woman.independentStatus == False:
                womanChildren = self.bringTheKids(woman)
                womanChildrenToMove = [x for x in womanChildren]
                peopleToMove += [x for x in womanChildrenToMove if x not in manChildrenToMove]
            else:
                if len([x for x in woman.house.occupants if x.independentStatus == True]) > 1:
                    print 'Error: an independent spouse partner is already living with an independent agent!'
                    sys.exit()
                peopleToMove += [x for x in woman.house.occupants if x != woman]
            
            if np.random.random() < self.p['coupleMovesToExistingHousehold']:
                # Change this to make sure they house an agent moves to is NOT the house of the partner's parents
                myHousePop = len(man.house.occupants)
                yourHousePop = len(woman.house.occupants)
                if yourHousePop < myHousePop:
                    targetHouse = woman.house
                else:
                    targetHouse = man.house
                if man.house == self.displayHouse:
                    messageString = str(self.year) + ": #" + str(man.id) + " and #" + str(woman.id)
                    messageString += " move to existing household."
                    self.textUpdateList.append(messageString)
                    with open(os.path.join(policyFolder, "Log.csv"), "a") as file:
                        writer = csv.writer(file, delimiter = ",", lineterminator='\r')
                        writer.writerow([self.year, messageString])
                        
                self.movePeopleIntoChosenHouse(targetHouse, man.house,peopleToMove, 0, policyFolder)                        
            else:
                distance = random.choice(['here','near'])
                if man.house == self.displayHouse:
                    messageString = str(self.year) + ": #" + str(man.id) + " moves out to live with #" + str(woman.id)
                    if len(peopleToMove) > 2:
                        messageString += ", bringing the kids"
                    messageString += "."
                    self.textUpdateList.append(messageString)
                    
                    with open(os.path.join(policyFolder, "Log.csv"), "a") as file:
                        writer = csv.writer(file, delimiter = ",", lineterminator='\r')
                        writer.writerow([self.year, messageString])
                        
                self.findNewHouse(peopleToMove,distance, policyFolder)                        

            if man.independentStatus == False:
                man.independentStatus = True
                man.movedThisYear = True
            if woman.independentStatus == False:
                woman.independentStatus = True
                woman.movedThisYear = True

    
    def doMovingAround(self, policyFolder):
        """
        Various reasons why a person or family group might want to
        move around. People who are in partnerships but not living
        together are highly likely to find a place together. Adults
        still living at home might be ready to move out this year.
        Single people might want to move in order to find partners. A
        family might move at random for work reasons. Older people
        might move back in with their kids.
        """
        
        for person in self.pop.livingPeople:
            age = self.year - person.birthdate
            ageClass = age / 10
            
            if person.movedThisYear:
                continue
            
            elif person.status == 'worker' and person.independentStatus == False and person.partner == None:
                ## a single person who hasn't left home yet
                if np.random.random() < self.p['basicProbAdultMoveOut']*self.p['probAdultMoveOutModifierByDecade'][ageClass]:
                    peopleToMove = [person]
                    peopleToMove += self.bringTheKids(person)
                    distance = random.choice(['here','near'])
                    if person.house == self.displayHouse:
                        messageString = str(self.year) + ": #" + str(person.id) + " moves out, aged " + str(self.year-person.birthdate) + "."
                        self.textUpdateList.append(messageString)
                        with open(os.path.join(policyFolder, "Log.csv"), "a") as file:
                            writer = csv.writer(file, delimiter = ",", lineterminator='\r')
                            writer.writerow([self.year, messageString])
                            
                    self.findNewHouse(peopleToMove,distance, policyFolder)
                    person.independentStatus = True
                    

            elif person.independentStatus == True and person.partner == None:
                ## a young-ish person who has left home but is still (or newly) single
                if np.random.random() < self.p['basicProbSingleMove']*self.p['probSingleMoveModifierByDecade'][int(ageClass)]:
                    peopleToMove = [person]
                    peopleToMove += [x for x in person.house.occupants if x != person] # self.bringTheKids(person)
                    distance = random.choice(['here','near'])
                    if person.house == self.displayHouse:
                        messageString = str(self.year) + ": #" + str(person.id) + " moves to meet new people."
                        self.textUpdateList.append(messageString)
                        with open(os.path.join(policyFolder, "Log.csv"), "a") as file:
                            writer = csv.writer(file, delimiter = ",", lineterminator='\r')
                            writer.writerow([self.year, messageString])
                            
                    self.findNewHouse(peopleToMove,distance, policyFolder)

            elif person.status == 'retired' and len(person.house.occupants) == 1:
                ## a retired person who lives alone
                workingChildren = [x for x in person.children if x.status == 'worker']
                for c in workingChildren:
                    if c.dead == False:
                        distance = self.manhattanDistance(person.house.town,c.house.town)
                        distance += 1.0
                        if self.year < self.p['thePresent']:
                            mbRate = self.p['agingParentsMoveInWithKids']/distance
                        else:
                            mbRate = self.p['variableMoveBack']/distance
                        if np.random.random() < mbRate:
                            peopleToMove = [person]
                            if person.house == self.displayHouse:
                                messageString = str(self.year) + ": #" + str(person.id) + " is going to live with one of their children."
                                self.textUpdateList.append(messageString)
                                with open(os.path.join(policyFolder, "Log.csv"), "a") as file:
                                    writer = csv.writer(file, delimiter = ",", lineterminator='\r')
                                    writer.writerow([self.year, messageString])
                                
                            self.movePeopleIntoChosenHouse(c.house,person.house,peopleToMove, 0, policyFolder)
                            break
                        
        self.checkIndependentAgents(4.2)
            
#            elif person.partner != None and person.yearMarried[-1] != self.year:
#                ## any other kind of married person, e.g., a normal family with kids
#                house = person.house
#                household = [x for x in house.occupants]
#                
#                # Compute relocation probability
#                relocationCost = self.p['relocationCostParam']*sum([math.pow(x.yearInTown, self.p['yearsInTownBeta']) for x in household])
#                supportNetworkFactor = math.exp(self.p['supportNetworkBeta']*house.networkSupport)
#                relocationCostFactor = math.exp(self.p['relocationCostBeta']*relocationCost)
#                perCapitaIncome = self.computeHouseholdIncome(house)/float(len(household))
#                incomeFactor = math.exp(self.p['incomeRelocationBeta']*perCapitaIncome)
#                relativeRelocationFactor = (supportNetworkFactor*relocationCostFactor)/incomeFactor
#                probRelocation = self.p['baseRelocationRate']/relativeRelocationFactor
#               
#                if random.random() < probRelocation: #self.p['basicProbFamilyMove']*self.p['probFamilyMoveModifierByDecade'][int(ageClass)]:
#                    
#                    peopleToMove = [x for x in person.house.occupants]
##                    personChildren = self.bringTheKids(person)
##                    peopleToMove += personChildren
##                    partnerChildren = self.bringTheKids(person.partner)
##                    peopleToMove += [x for x in partnerChildren if x not in personChildren]
##                    stepChildrenPartner = [x for x in personChildren if x not in partnerChildren]
##                    stepChildrenPerson = [x for x in partnerChildren if x not in personChildren]
##                    person.children.extend(stepChildrenPerson)
##                    person.partner.children.extend(stepChildrenPartner)
#                    
#                    # Add a choice of town which depends on kinship network and available houses.
#                    
#                    distance = random.choice(['here,''near','far'])
#                    if person.house == self.displayHouse:
#                        messageString = str(self.year) + ": #" + str(person.id) + " and #" + str(person.partner.id) + " move house"
#                        if len(peopleToMove) > 2:
#                            messageString += " with kids"
#                        messageString += "."
#                        self.textUpdateList.append(messageString)
#                        with open(os.path.join(policyFolder, "Log.csv"), "a") as file:
#                            writer = csv.writer(file, delimiter = ",", lineterminator='\r')
#                            writer.writerow([self.year, messageString])
#                        
#                    self.findNewHouse(peopleToMove,distance, policyFolder)
                    
        
        # Update display house
        if len(self.displayHouse.occupants) < 1:
            self.displayHouse.display = False
            ## Nobody lives in the display house any more, choose another
            if self.nextDisplayHouse != None:
                self.displayHouse = self.nextDisplayHouse
                self.displayHouse.display = True
                self.nextDisplayHouse = None
            else:
                self.displayHouse = random.choice(self.pop.livingPeople).house
                self.displayHouse.display = True
                self.textUpdateList.append(str(self.year) + ": Display house empty, going to " + self.displayHouse.name + ".")
                messageString = "Residents: "
                for k in self.displayHouse.occupants:
                    messageString += "#" + str(k.id) + " "
                self.textUpdateList.append(messageString)
                
    def manhattanDistance(self,t1,t2):
        """Calculates the distance between two towns"""
        xDist = abs(t1.x - t2.x)
        yDist = abs(t1.y - t2.y)
        return xDist + yDist


    def bringTheKids(self,person):
        """Given a person, return a list of their dependent kids who live in the same house as them."""
        returnList = []
        for i in person.children:
            if i.house == person.house and i.independentStatus == False and i.dead == False:
                returnList.append(i)
        return returnList

    def findNewHouseInNewTown(self, personList, newTown, policyFolder):
        """Find an appropriate empty house for the named person and put them in it."""

        newHouse = None
        person = personList[0]
        departureHouse = person.house
        t = person.house.town
        availableHouses = [x for x in newTown.houses if len(x.occupants) == 0]
        newHouse = random.choice(availableHouses)

        ## Quit with an error message if we've run out of houses
        if newHouse in self.map.occupiedHouses:
            print 'Error in house selection: already occupied!'
            print newHouse.id
            
#        if newHouse == None:
#            print "No houses left for person of SEC " + str(person.sec)
#            sys.exit()

        ## Actually make the chosen move
        self.movePeopleIntoChosenHouse(newHouse, departureHouse, personList, 1, policyFolder)

    def findNewHouse(self, personList, preference, policyFolder):
        """Find an appropriate empty house for the named person and put them in it."""

        newHouse = None
        if len(personList) > 1 and personList[0].partner == personList[1]:
            person = np.random.choice([personList[0], personList[1]])
        else:
            person = personList[0]
        departureHouse = person.house
        t = person.house.town

        if ( preference == 'here' ):
            ## Anything empty in this town of the right size?
            localPossibilities = [x for x in t.houses
                                  if len(x.occupants) < 1
                                  and person.sec == x.size ]
            if localPossibilities:
                newHouse = random.choice(localPossibilities)

        if ( preference == 'near' or newHouse == None ):
            ## Neighbouring towns?
            if newHouse == None:
                nearbyTowns = [ k for k in self.map.towns
                                if abs(k.x - t.x) <= 1
                                and abs(k.y - t.y) <= 1 ]
                nearbyPossibilities = []
                for z in nearbyTowns:
                    for w in z.houses:
                        if len(w.occupants) < 1 and person.sec == w.size:
                            nearbyPossibilities.append(w)
                if nearbyPossibilities:
                    newHouse = random.choice(nearbyPossibilities)

        if ( preference == 'far' or newHouse == None ):
            ## Anywhere at all?
            if newHouse == None:
                allPossibilities = []
                for z in self.map.allHouses:
                    if len(z.occupants) < 1 and person.sec == z.size:
                        allPossibilities.append(z)
                if allPossibilities:
                    newHouse = random.choice(allPossibilities)

        ## Quit with an error message if we've run out of houses
        if newHouse in self.map.occupiedHouses:
            print 'Error in house selection: already occupied!'
            print newHouse.id
            
#        if newHouse == None:
#            print "No houses left for person of SEC " + str(person.sec)
#            sys.exit()

        ## Actually make the chosen move
        self.movePeopleIntoChosenHouse(newHouse,departureHouse,personList, 1, policyFolder)

    
    def addMember(self,newHouse,departureHouse,personList, case, policyFolder):
        ## Put the new house onto the list of occupied houses if it was empty
        newMembers = list(personList)
        
        if len(newMembers) != len(set(newMembers)):
            print 'Error in movePeopleIntoChosenHouse: double counting people'
            for member in newMembers:
                print member.id
            sys.exit()
        
        ## Move everyone on the list over from their former house to the new one
        for i in newMembers:
            if newHouse.town != departureHouse.town:
                i.yearInTown = 0
#            if i.house == newHouse:
#                print 'Error: new house is the old house!'
#                sys.exit()
                
            oldHouse = i.house
            
#            if i not in oldHouse.occupants:
#                print 'Error: person not in house.'
#                print i.house.id
#                print oldHouse.id
#                sys.exit()
                
            oldHouse.occupants.remove(i)
            
            if len(oldHouse.occupants) == 0:
                self.map.occupiedHouses.remove(oldHouse)
                ##print "This house is now empty: ", oldHouse
                if (self.p['interactiveGraphics']):
                    self.canvas.itemconfig(oldHouse.icon, state='hidden')
            
            newHouse.occupants.append(i)
            
            i.house = newHouse
            i.movedThisYear = True

        ## This next is sloppy and will lead to loads of duplicates in the
        ## occupiedHouses list, but we don't want to miss any -- that's
        ## much worse -- and the problem will be solved by a conversion
        ## to set and back to list int he stats method in a moment
        if case == 1:
            self.map.occupiedHouses.append(newHouse)
        
#        if len(self.map.occupiedHouses) != len(set(self.map.occupiedHouses)):
#            print 'Error: house appears twice in occupied houses!'
#            houses = []
#            for x in self.map.occupiedHouses:
#                if x in houses:
#                    print x.id
#                else:
#                    houses.append(x)
#            sys.exit()
        
        emptyOccupiedHouses = [x for x in self.map.occupiedHouses if len(x.occupants) == 0]
        
#        if len(emptyOccupiedHouses) > 0:
#            print 'Error: empty houses among occupied ones!'
#            for m in emptyOccupiedHouses:
#                print m.id
#            sys.exit()
        
        if (self.p['interactiveGraphics']):
            self.canvas.itemconfig(newHouse.icon, state='normal')

            
            
        ## Check whether we've moved into the display house
        if newHouse == self.displayHouse:
            messageString = str(self.year) + ": New people are moving into " + newHouse.name
            self.textUpdateList.append(messageString)
            with open(os.path.join(policyFolder, "Log.csv"), "a") as file:
                writer = csv.writer(file, delimiter = ",", lineterminator='\r')
                writer.writerow([self.year, messageString])
            
            messageString = ""
            for k in personList:
                messageString += "#" + str(k.id) + " "
            self.textUpdateList.append(messageString)
            with open(os.path.join(policyFolder, "Log.csv"), "a") as file:
                writer = csv.writer(file, delimiter = ",", lineterminator='\r')
                writer.writerow([self.year, messageString])
            
        ## or out of it...
        if departureHouse == self.displayHouse and len(departureHouse.occupants) < 1:
            self.nextDisplayHouse = newHouse
    
    def movePeopleIntoChosenHouse(self,newHouse,departureHouse,personList, case, policyFolder):

        ## Put the new house onto the list of occupied houses if it was empty
        household = list(personList)
        
        newHouse.newOccupancy = True
        
        if len(household) != len(set(household)):
            print 'Error in movePeopleIntoChosenHouse: double counting people'
            for member in household:
                print member.id
            sys.exit()
        
        
        ## Move everyone on the list over from their former house to the new one
        for i in household:
            if newHouse.town != departureHouse.town:
                i.yearInTown = 0
#            if i.house == newHouse:
#                print 'Error: new house is the old house!'
#                sys.exit()
                
            oldHouse = i.house
            
#            if i not in oldHouse.occupants:
#                print 'Error: person not in house.'
#                print i.house.id
#                print oldHouse.id
#                sys.exit()
                
            oldHouse.occupants.remove(i)
            
            if len(oldHouse.occupants) == 0:
                self.map.occupiedHouses.remove(oldHouse)
                ##print "This house is now empty: ", oldHouse
                if (self.p['interactiveGraphics']):
                    self.canvas.itemconfig(oldHouse.icon, state='hidden')
            
            newHouse.occupants.append(i)
            
            i.house = newHouse
            i.movedThisYear = True

        ## This next is sloppy and will lead to loads of duplicates in the
        ## occupiedHouses list, but we don't want to miss any -- that's
        ## much worse -- and the problem will be solved by a conversion
        ## to set and back to list int he stats method in a moment
        if case == 1:
            self.map.occupiedHouses.append(newHouse)
        
#        if len(self.map.occupiedHouses) != len(set(self.map.occupiedHouses)):
#            print 'Error: house appears twice in occupied houses!'
#            houses = []
#            for x in self.map.occupiedHouses:
#                if x in houses:
#                    print x.id
#                else:
#                    houses.append(x)
#            sys.exit()
        
        emptyOccupiedHouses = [x for x in self.map.occupiedHouses if len(x.occupants) == 0]
        
#        if len(emptyOccupiedHouses) > 0:
#            print 'Error: empty houses among occupied ones!'
#            for m in emptyOccupiedHouses:
#                print m.id
#            sys.exit()
        
        if (self.p['interactiveGraphics']):
            self.canvas.itemconfig(newHouse.icon, state='normal')

            
            
        ## Check whether we've moved into the display house
        if newHouse == self.displayHouse:
            messageString = str(self.year) + ": New people are moving into " + newHouse.name
            self.textUpdateList.append(messageString)
            with open(os.path.join(policyFolder, "Log.csv"), "a") as file:
                writer = csv.writer(file, delimiter = ",", lineterminator='\r')
                writer.writerow([self.year, messageString])
            
            messageString = ""
            for k in personList:
                messageString += "#" + str(k.id) + " "
            self.textUpdateList.append(messageString)
            with open(os.path.join(policyFolder, "Log.csv"), "a") as file:
                writer = csv.writer(file, delimiter = ",", lineterminator='\r')
                writer.writerow([self.year, messageString])
            
        ## or out of it...
        if departureHouse == self.displayHouse and len(departureHouse.occupants) < 1:
            self.nextDisplayHouse = newHouse
                

    def doStats(self, policyFolder, dataMapFolder, dataHouseholdFolder, period):
        """Calculate annual stats and store them appropriately."""

        self.times.append(self.year)

        currentPop = len(self.pop.livingPeople)
        everLivedPop = len(self.pop.allPeople)
        self.pops.append(currentPop)

        potentialWorkers = [x for x in self.pop.livingPeople if x.age >= self.p['ageOfAdulthood'] and x.age < self.p['ageOfRetirement']]
        employed = [x for x in potentialWorkers if x.status == 'worker' and x.residualWorkingHours > 0]
        potentialHours = sum([self.p['weeklyHours'][x.careNeedLevel] for x in employed])
        actualHours = sum([x.residualWorkingHours for x in employed])
        
        shareEmployed = 0
        if len(potentialWorkers) > 0:
            shareEmployed = float(len(employed))/float(len(potentialWorkers))
        shareWorkHours = 0
        if potentialHours > 0:
            shareWorkHours = float(actualHours)/float(potentialHours)
        self.employmentRate.append(shareEmployed)
        self.shareWorkingHours.append(shareWorkHours)

        ## Check for double-included houses by converting to a set and back again
        self.map.occupiedHouses = list(set(self.map.occupiedHouses))
        
        singleHousehold_UC = 0
        coupleHousehold_UC = 0
        incomePerCapita_Single = 0
        incomePerCapita_Couple = 0
        totalIncome_Single = 0
        totalIncome_Couple = 0
        totalMembers_Single = 0
        totalMembers_Couple = 0
        parents = []
        loneParents = []
        loneFemaleParents = []
        visitedPeople = []
        for person in [x for x in self.pop.livingPeople if x.independentStatus == True]:
            children = [x for x in person.house.occupants if x.age <= 15 or (x.age <= 18 and x.status == 'student')]
            if len(children) > 0:
                if person.partner != None and person not in visitedPeople:
                    visitedPeople.extend([person, person.partner])
                    parents.append([person, person.partner])
                    coupleHousehold_UC += sum([x.unmetChildCareNeed for x in person.house.occupants])
                    totalIncome_Couple += sum([x.income for x in person.house.occupants])
                    totalMembers_Couple += len([x for x in person.house.occupants])
                if person.partner == None and person not in visitedPeople:
                    visitedPeople.append(person)
                    parents.append([person])
                    loneParents.append(person)
                    singleHousehold_UC += sum([x.unmetChildCareNeed for x in person.house.occupants])
                    totalIncome_Single += sum([x.income for x in person.house.occupants])
                    totalMembers_Single += len([x for x in person.house.occupants])
                    if person.sex == 'female':
                        loneFemaleParents.append(person)
 
        numberCouples = float(len(parents))
        incomePerCapita_Single = 0
        if totalMembers_Single > 0:
            incomePerCapita_Single = totalIncome_Single/float(totalMembers_Single)
        incomePerCapita_Couple = 0
        if totalMembers_Couple > 0:
            incomePerCapita_Couple = totalIncome_Couple/float(totalMembers_Couple)
        print 'Number households with children: ' + str(numberCouples)
        numberLoneParents = float(len(loneParents))
        shareSingleParents = 0
        if numberCouples > 0:
            shareSingleParents = numberLoneParents/numberCouples
        shareFemaleSingleParent = 0
        if numberLoneParents > 0:
            shareFemaleSingleParent = float(len(loneFemaleParents))/numberLoneParents
        self.shareLoneParents.append(shareSingleParents)
        self.shareFemaleLoneParents.append(shareFemaleSingleParent)
        
        over64 = [x for x in self.pop.livingPeople if x.age >= 65]
        indipendentOver65 = [x for x in over64 if x.careNeedLevel == 0]
        lowDependencyOver65 = [x for x in over64 if x.careNeedLevel == 1]
        mediumDependencyOver65 = [x for x in over64 if x.careNeedLevel == 2 or x.careNeedLevel == 3]
        highDependencyOver65 = [x for x in over64 if x.careNeedLevel == 4]
        
#        if len(over64) > 0:
#            print 'independent Over 64: ' + str(float(len(indipendentOver65))/float(len(over64)))
#            print 'low dependency Over 64: ' + str(float(len(lowDependencyOver65))/float(len(over64)))
#            print 'medium dependency Over 64: ' + str(float(len(mediumDependencyOver65))/float(len(over64)))
#            print 'high dependency Over 64: ' + str(float(len(highDependencyOver65))/float(len(over64)))
#        
        if self.year == 2017:
            self.sesPops = []
            for i in range(int(self.p['numberClasses'])):
                self.sesPops.append(len([x for x in self.pop.livingPeople if x.age > 23 and x.classRank == i]))
            self.sesPopsShares = [float(x)/float(sum(self.sesPops)) for x in self.sesPops]
            lenFrequency = len(self.incomeDistribution)
            self.incomeFrequencies = [0]*lenFrequency
            households = [y.occupants for y in self.map.occupiedHouses]
            
            self.individualIncomes = [x.income*52 for x in self.pop.livingPeople if x.income > 0]
            
        
            self.householdIncomes = [sum([x.income*52 for x in y]) for y in households]
            
            for i in self.householdIncomes:
                ind = int(i/1000)
                if ind > -1 and ind < lenFrequency:
                    self.incomeFrequencies[ind] += 1

        ## Check for overlooked empty houses
        emptyHouses = [x for x in self.map.occupiedHouses if len(x.occupants) == 0]
        for h in emptyHouses:
            self.map.occupiedHouses.remove(h)
            if (self.p['interactiveGraphics']):
                self.canvas.itemconfig(h.icon, state='hidden')

        ## Avg household size (easily calculated by pop / occupied houses)
        numHouseholds = len(self.map.occupiedHouses)
        averageHouseholdSize = float(currentPop)/float(numHouseholds)
        self.avgHouseholdSize.append(averageHouseholdSize)

        self.numMarriages.append(self.marriageTally)
        self.numDivorces.append(self.divorceTally)            
        
        
        totalSocialCareNeed = sum([x.hoursSocialCareDemand for x in self.pop.livingPeople])
        totalInformalSocialCare = sum([x.informalSocialCareReceived for x in self.pop.livingPeople])
        totalFormalSocialCare = sum([x.formalSocialCareReceived for x in self.pop.livingPeople])
        totalSocialCare = totalInformalSocialCare + totalFormalSocialCare
        totalUnmetSocialCareNeed = sum([x.unmetSocialCareNeed for x in self.pop.livingPeople])
        
        totalInformalChildCare = sum([x.informalChildCareReceived for x in self.pop.livingPeople])
        totalFormalChildCare = sum([x.formalChildCareReceived for x in self.pop.livingPeople])
        totalChildCare = totalInformalChildCare + totalFormalChildCare
        totalUnmetChildCareNeed = sum([x.unmetChildCareNeed for x in self.pop.livingPeople])
        
        
        share_InformalSocialCare = 0
        if totalSocialCare > 0:
            share_InformalSocialCare = totalInformalSocialCare/totalSocialCare
        
        print share_InformalSocialCare
        
        share_UnmetSocialCareNeed = 0
        if totalSocialCareNeed > 0:
            share_UnmetSocialCareNeed = totalUnmetSocialCareNeed/totalSocialCareNeed
        
        
        for house in self.map.occupiedHouses:
            house.totalUnmetSocialCareNeed = sum([x.unmetSocialCareNeed for x in house.occupants])
#        print totalSocialCareNeed
#        if totalInformalSocialCare > 0:
#            print 'Share of in-house informal care: ' + str(float(self.inHouseInformalCare)/totalInformalSocialCare)
#        print share_UnmetSocialCareNeed
#        print ''
        
        outOfWorkSocialCare = [x.outOfWorkSocialCare for x in self.pop.livingPeople]
        totalOWSC = sum(outOfWorkSocialCare)
        shareOWSC = 0
        if totalInformalSocialCare > 0:
            shareOWSC = totalOWSC/totalInformalSocialCare
        totalCostOWSC = sum([x.outOfWorkSocialCare*x.wage for x in self.pop.livingPeople if x.outOfWorkSocialCare > 0])
        
        inactiveAgents = [x for x in potentialWorkers if x.status == 'worker' if x.residualWorkingHours == 0]
        print 'Number of inactive adults: ' + str(len(inactiveAgents))
        print 'Number of new mothers: ' + str(len([x for x in potentialWorkers if x.maternityStatus == True]))
        
        parttimeAgents = [x for x in potentialWorkers if x.status == 'worker' if x.residualWorkingHours < 25 and x not in inactiveAgents]
        print 'Number of part-time agents: ' + str(len(parttimeAgents))
        print 'Total adults: ' + str(len(potentialWorkers))
        
        medianPTIncome = [x.income for x in parttimeAgents]
        if len(medianPTIncome) > 0:
            print 'Median PT Income: ' + str(np.median(medianPTIncome))
        else:
            print 'No PT agents.'
        
        zeroIncomeHouseholds = [x for x in self.map.occupiedHouses if sum([y.income for y in x.occupants]) == 0]
        print 'Number of zero income households: ' + str(len(zeroIncomeHouseholds))
        
        # By income quintiles
        households = [x for x in self.map.occupiedHouses]
        print 'Number households: ' + str(len(households))
        q1_households = [x for x in households if x.incomeQuintile == 0]
        q1_socialCareNeed = sum([x.totalSocialCareNeed for x in q1_households])
        q2_households = [x for x in households if x.incomeQuintile == 1]
        q2_socialCareNeed = sum([x.totalSocialCareNeed for x in q2_households])
        q3_households = [x for x in households if x.incomeQuintile == 2]
        q3_socialCareNeed = sum([x.totalSocialCareNeed for x in q3_households])
        q4_households = [x for x in households if x.incomeQuintile == 3]
        q4_socialCareNeed = sum([x.totalSocialCareNeed for x in q4_households])
        q5_households = [x for x in households if x.incomeQuintile == 4]
        q5_socialCareNeed = sum([x.totalSocialCareNeed for x in q5_households])
        
        q1_informalSocialCare = sum([x.informalSocialCareReceived for x in q1_households])
        q2_informalSocialCare = sum([x.informalSocialCareReceived for x in q2_households])
        q3_informalSocialCare = sum([x.informalSocialCareReceived for x in q3_households])
        q4_informalSocialCare = sum([x.informalSocialCareReceived for x in q4_households])
        q5_informalSocialCare = sum([x.informalSocialCareReceived for x in q5_households])
        
        q1_outOfWorkSocialCare = sum([x.outOfWorkSocialCare for x in q1_households])
        q2_outOfWorkSocialCare = sum([x.outOfWorkSocialCare for x in q2_households])
        q3_outOfWorkSocialCare = sum([x.outOfWorkSocialCare for x in q3_households])
        q4_outOfWorkSocialCare = sum([x.outOfWorkSocialCare for x in q4_households])
        q5_outOfWorkSocialCare = sum([x.outOfWorkSocialCare for x in q5_households])
        
        q1_formalSocialCare = sum([x.formalSocialCareReceived for x in q1_households])
        q2_formalSocialCare = sum([x.formalSocialCareReceived for x in q2_households])
        q3_formalSocialCare = sum([x.formalSocialCareReceived for x in q3_households])
        q4_formalSocialCare = sum([x.formalSocialCareReceived for x in q4_households])
        q5_formalSocialCare = sum([x.formalSocialCareReceived for x in q5_households])
        
        q1_unmetSocialCareNeed = sum([x.totalUnmetSocialCareNeed for x in q1_households])
        q2_unmetSocialCareNeed = sum([x.totalUnmetSocialCareNeed for x in q2_households])
        q3_unmetSocialCareNeed = sum([x.totalUnmetSocialCareNeed for x in q3_households])
        q4_unmetSocialCareNeed = sum([x.totalUnmetSocialCareNeed for x in q4_households])
        q5_unmetSocialCareNeed = sum([x.totalUnmetSocialCareNeed for x in q5_households])
        
        taxPayers = len([x for x in self.pop.livingPeople if x.status == 'student' or x.status == 'worker'])
        
        
        print 'Number of working-age people (2): ' + str(len([x for x in self.pop.livingPeople if x.status == 'worker']))
        
        print 'Number of retired people (2): ' + str(len([x for x in self.pop.livingPeople if x.status == 'retired']))
        self.numTaxpayers.append(taxPayers)
        
        if totalSocialCareNeed == 0:
            familyCareRatio = 0.0
        else:
            familyCareRatio = (totalSocialCareNeed - totalUnmetSocialCareNeed)/totalSocialCareNeed

        ##familyCareRatio = ( totalCareDemandHours - unmetNeed ) / (1.0 * (totalCareDemandHours+0.01))
        self.totalFamilyCare.append(familyCareRatio)
        taxBurden = 0
        if taxPayers > 0:
            taxBurden = ( totalUnmetSocialCareNeed * self.p['hourlyCostOfCare'] * 52.18 ) / ( taxPayers * 1.0 )
        self.totalTaxBurden.append(taxBurden)
        
        ## Count the proportion of adult women who are married
        totalAdultWomen = 0
        totalMarriedAdultWomen = 0
        for person in self.pop.livingPeople:
            if person.sex == 'female' and person.age >= 18:
                totalAdultWomen += 1
                if person.partner != None:
                    totalMarriedAdultWomen += 1
        marriagePropNow = float(totalMarriedAdultWomen)/float(totalAdultWomen)
        self.marriageProp.append(marriagePropNow)
        print 'Share of married adult women: ' + str(marriagePropNow)

        formalChildCare = sum([x.formalChildCareReceived for x in self.pop.livingPeople])
        formalChildCareCost = formalChildCare*self.p['priceChildCare']
        householdsIncome = sum([x.householdIncome for x in self.map.occupiedHouses])
        householdsTotalIncome = sum([x.totalPotentialIncome for x in self.map.occupiedHouses])
        householdsTotalChildCareCost = sum([x.costFormalChildCare for x in self.map.occupiedHouses])
        totalDisposableIncome = sum([x.householdDisposableIncome for x in self.map.occupiedHouses])
        
        childcareIncomeShare = 0
        if totalDisposableIncome > 0:
            childcareIncomeShare = householdsTotalChildCareCost/totalDisposableIncome
      
        children = [x for x in self.pop.livingPeople if x.age < self.p['ageTeenagers']]
        totalChildCareNeed = sum([x.netChildCareDemand for x in children])
        unmetChildCareNeed = sum([x.unmetChildCareNeed for x in children])
        
#        print 'Total child care need: ' + str(totalChildCareNeed)
#        print 'Unmet child care need: ' + str(unmetChildCareNeed)
        
        totalInformalChildCare = sum([x.informalChildCareReceived for x in children])
        shareInformalChildCare = 0
        if totalChildCareNeed > 0:
            shareInformalChildCare = totalInformalChildCare/totalChildCareNeed
       
        # Social care stats
        over16Pop = [x for x in self.pop.livingPeople if x.age > 16]
        totalSuppliers = [x for x in over16Pop if x.socialWork > 0]
        shareCareGivers = float(len(totalSuppliers))/float(len(over16Pop))
        familyCarers = [x for x in over16Pop if x.careForFamily == True]
        
        
        malesOver16 = [x for x in over16Pop if x.sex == 'male']
        femalesOver16 = [x for x in over16Pop if x.sex == 'female']
        maleSuppliers = [x for x in malesOver16 if x.socialWork > 0]
        femaleSuppliers = [x for x in femalesOver16 if x.socialWork > 0]
        ratioFemaleMaleCarers = 0
        if len(totalSuppliers) > 0:
            ratioFemaleMaleCarers = float(len(femaleSuppliers))/float(len(totalSuppliers))
        shareMaleCarers = 0
        if len(malesOver16) > 0:
            shareMaleCarers = float(len(maleSuppliers))/float(len(malesOver16))
        shareFemaleCarers = 0
        if len(femalesOver16) > 0:
            shareFemaleCarers = float(len(femaleSuppliers))/float(len(femalesOver16))
        
        workers = [x for x in self.pop.livingPeople if x.status == 'worker' and x.careNeedLevel < 3]
        employedMales = [x for x in workers if x.sex == 'male']
        employedFemales = [x for x in workers if x.sex == 'female']
        
        meanMaleWage = np.mean([x.wage for x in employedMales])
        meanFemaleWage = np.mean([x.wage for x in employedFemales])
        ratioWage = 0
        if meanMaleWage > 0:
            ratioWage = meanFemaleWage/meanMaleWage
        
        meanMaleIncome = np.mean([x.income for x in employedMales])
        meanFemaleIncome = np.mean([x.income for x in employedFemales])
        ratioIncome = 0
        if meanMaleIncome > 0:
            ratioIncome = meanFemaleIncome/meanMaleIncome
        
        informalSocialCarers = [x for x in self.pop.livingPeople if x.socialWork > 0]
        informalSocialReceivers = [x for x in self.pop.livingPeople if x.informalSocialCareReceived > 0]
        informalCaresSupplied = [x.socialWork for x in informalSocialCarers]
        shareFamilyCarer = 0
        if len(informalSocialCarers) > 0:
            shareFamilyCarer = float(len(familyCarers))/float(len(informalSocialCarers))
        
        over20Hours_FamilyCarers = [x for x in familyCarers if x.socialWork > 20]
        share_over20Hours_FamilyCarers = 0
        if len(familyCarers) > 0:
            share_over20Hours_FamilyCarers = float(len(over20Hours_FamilyCarers))/float(len(familyCarers))
        numSocialCarers = len(informalSocialCarers)
        averageHoursOfCare = 0
        if numSocialCarers > 0:
            averageHoursOfCare = np.mean(informalCaresSupplied)
        carers_40to64 = [x for x in informalSocialCarers if x.age >= 40 and x.age <= 64]
        over65_carers = [x for x in informalSocialCarers if x.age >= 65]
        share_40to64_carers = 0
        if len(informalSocialCarers) > 0:
            share_40to64_carers = float(len(carers_40to64))/float(len(informalSocialCarers))
        share_over65_carers = 0
        if len(informalSocialCarers) > 0:
            share_over65_carers = float(len(over65_carers))/float(len(informalSocialCarers))
            
        over70_carers = [x for x in informalSocialCarers if x.age >= 70]  
        TenPlusHours_over70 = [x for x in over70_carers if x.age >= 70 if x.socialWork > 10]
        share_10PlusHours_over70 = 0
        if len(over70_carers) > 0:
            share_10PlusHours_over70 = float(len(TenPlusHours_over70))/float(len(over70_carers))
        
        self.costTaxFreeSocialCare = totalFormalSocialCare*self.p['priceSocialCare']*self.p['socialCareTaxFreeRate']
        
        publicCareToGDP = 0
        if self.grossDomesticProduct > 0:
            publicCareToGDP = self.costPublicSocialCare/self.grossDomesticProduct
            
        origIQ1 = np.median([x.householdIncome for x in self.map.occupiedHouses if x.incomeQuintile == 0])
        origIQ2 = np.median([x.householdIncome for x in self.map.occupiedHouses if x.incomeQuintile == 1])
        origIQ3 = np.median([x.householdIncome for x in self.map.occupiedHouses if x.incomeQuintile == 2])
        origIQ4 = np.median([x.householdIncome for x in self.map.occupiedHouses if x.incomeQuintile == 3])
        origIQ5 = np.median([x.householdIncome for x in self.map.occupiedHouses if x.incomeQuintile == 4])
        # print 'Gross incomes quintiles: ' + str([origIQ1, origIQ2, origIQ3, origIQ4, origIQ5])
        
        dispIQ1 = np.median([x.householdDisposableIncome for x in self.map.occupiedHouses if x.disposableIncomeQuintile == 0])
        dispIQ2 = np.median([x.householdDisposableIncome for x in self.map.occupiedHouses if x.disposableIncomeQuintile == 1])
        dispIQ3 = np.median([x.householdDisposableIncome for x in self.map.occupiedHouses if x.disposableIncomeQuintile == 2])
        dispIQ4 = np.median([x.householdDisposableIncome for x in self.map.occupiedHouses if x.disposableIncomeQuintile == 3])
        dispIQ5 = np.median([x.householdDisposableIncome for x in self.map.occupiedHouses if x.disposableIncomeQuintile == 4])
        
        independentAgents = [x for x in self.pop.livingPeople if x.independentStatus == True]
        indIQ1 = np.median([x.yearlyDisposableIncome for x in independentAgents if x.disposableIncomeQuintile == 0])
        indIQ2 = np.median([x.yearlyDisposableIncome for x in independentAgents if x.disposableIncomeQuintile == 1])
        indIQ3 = np.median([x.yearlyDisposableIncome for x in independentAgents if x.disposableIncomeQuintile == 2])
        indIQ4 = np.median([x.yearlyDisposableIncome for x in independentAgents if x.disposableIncomeQuintile == 3])
        indIQ5 = np.median([x.yearlyDisposableIncome for x in independentAgents if x.disposableIncomeQuintile == 4])
        
        netIQ1 = np.median([x.householdNetIncome for x in self.map.occupiedHouses if x.netIncomeQuintile == 0])
        netIQ2 = np.median([x.householdNetIncome for x in self.map.occupiedHouses if x.netIncomeQuintile == 1])
        netIQ3 = np.median([x.householdNetIncome for x in self.map.occupiedHouses if x.netIncomeQuintile == 2])
        netIQ4 = np.median([x.householdNetIncome for x in self.map.occupiedHouses if x.netIncomeQuintile == 3])
        netIQ5 = np.median([x.householdNetIncome for x in self.map.occupiedHouses if x.netIncomeQuintile == 4])
        
        shareInternalCare = 0
        totalCare = self.internalChildCare+self.internalSocialCare+self.externalChildCare+self.externalSocialCare
        if totalCare > 0:
            shareInternalCare = (self.internalChildCare+self.internalSocialCare)/totalCare
        
        self.previousTotalFormalCare = self.totalFormalCare
        self.totalFormalCare = totalFormalSocialCare+formalChildCare
        
        if self.totalFormalCare > 0:
            self.periodFormalCare = True
#            if self.previousTotalFormalCare > 0:
#                self.periodFormalCare = False
#                self.householdsWithFormalChildCare = []
        else:
            self.periodFormalCare = False
        
        print 'Formal child care: ' + str(formalChildCare)
        print 'Formal social care: ' + str(totalFormalSocialCare)
        
#        if self.previousTotalFormalCare > 0:
#            if self.totalFormalCare == 0:
#                sys.exit()
        totalBenefits = sum([self.aggregateChildBenefits, self.aggregateDisabledChildrenBenefits,
                   self.aggregatePIP, self.aggregateAttendanceAllowance, self.aggregateCarersAllowance, self.aggregateUC, 
                   self.aggregateHousingElement, self.aggregatePensionCredit])
        benefitsIncomeShare = 0
        if totalDisposableIncome > 0:
            benefitsIncomeShare = totalBenefits/totalDisposableIncome
        print 'Benefits as share of income: ' + str(benefitsIncomeShare)
        
        outputs = [self.year, self.month, period, currentPop, everLivedPop, numHouseholds, averageHouseholdSize, self.marriageTally, 
                   marriagePropNow, self.divorceTally, shareSingleParents, shareFemaleSingleParent, taxPayers, taxBurden, familyCareRatio, 
                   shareEmployed, shareWorkHours, self.publicSocialCare, self.costPublicSocialCare, self.sharePublicSocialCare, 
                   self.costTaxFreeSocialCare, self.publicChildCare, self.costPublicChildCare, self.sharePublicChildCare, 
                   self.costTaxFreeChildCare, self.totalTaxRevenue, self.totalPensionRevenue, self.pensionExpenditure, 
                   self.totalHospitalizationCost, self.socialClassShares[0], self.socialClassShares[1], self.socialClassShares[2], 
                   self.socialClassShares[3], self.socialClassShares[4], totalInformalChildCare, formalChildCare, totalUnmetChildCareNeed, 
                   childcareIncomeShare, shareInformalChildCare, shareCareGivers, ratioFemaleMaleCarers, shareMaleCarers, shareFemaleCarers, ratioWage, 
                   ratioIncome, shareFamilyCarer, share_over20Hours_FamilyCarers, numSocialCarers, averageHoursOfCare, share_40to64_carers, 
                   share_over65_carers, share_10PlusHours_over70, totalSocialCareNeed, totalInformalSocialCare, totalFormalSocialCare, 
                   totalUnmetSocialCareNeed, totalSocialCare, share_InformalSocialCare, share_UnmetSocialCareNeed, 
                   totalOWSC, shareOWSC, totalCostOWSC, singleHousehold_UC, coupleHousehold_UC, incomePerCapita_Single, incomePerCapita_Couple,
                   q1_socialCareNeed, q1_informalSocialCare, q1_formalSocialCare, q1_unmetSocialCareNeed, q1_outOfWorkSocialCare,
                   q2_socialCareNeed, q2_informalSocialCare, q2_formalSocialCare, q2_unmetSocialCareNeed, q2_outOfWorkSocialCare,
                   q3_socialCareNeed, q3_informalSocialCare, q3_formalSocialCare, q3_unmetSocialCareNeed, q3_outOfWorkSocialCare,
                   q4_socialCareNeed, q4_informalSocialCare, q4_formalSocialCare, q4_unmetSocialCareNeed, q4_outOfWorkSocialCare,
                   q5_socialCareNeed, q5_informalSocialCare, q5_formalSocialCare, q5_unmetSocialCareNeed, q5_outOfWorkSocialCare,
                   self.grossDomesticProduct, publicCareToGDP, self.onhUnmetChildcareNeed, self.medianChildCareNeedONH, self.totalHoursOffWork,
                   indIQ1, indIQ2, indIQ3, indIQ4, indIQ5, origIQ1, origIQ2, origIQ3, origIQ4, origIQ5, dispIQ1, dispIQ2, dispIQ3, dispIQ4, dispIQ5,
                   netIQ1, netIQ2, netIQ3, netIQ4, netIQ5, self.socialClassShares[0], self.socialClassShares[1], self.socialClassShares[2],
                   self.socialClassShares[3], self.socialClassShares[4], self.internalChildCare, self.internalSocialCare, self.externalChildCare, 
                   self.externalSocialCare, shareInternalCare, self.aggregateChildBenefits, self.aggregateDisabledChildrenBenefits,
                   self.aggregatePIP, self.aggregateAttendanceAllowance, self.aggregateCarersAllowance, self.aggregateUC, 
                   self.aggregateHousingElement, self.aggregatePensionCredit, totalBenefits, benefitsIncomeShare]
        
        
        dataMapFile = 'DataMap_' + str(self.year) + '.csv'
        if not os.path.exists(dataMapFolder):
            os.makedirs(dataMapFolder)
        with open(os.path.join(dataMapFolder, dataMapFile), "w") as file:
            writer = csv.writer(file, delimiter = ",", lineterminator='\r')
            writer.writerow((self.dataMap))
            for house in self.map.allHouses:
                data = [house.town.x, house.town.y, house.x, house.y, len(house.occupants), house.totalUnmetSocialCareNeed]
                writer.writerow(data)
                
        householdFile = 'DataHousehold_' + str(self.year) + '.csv'
        if not os.path.exists(dataHouseholdFolder):
            os.makedirs(dataHouseholdFolder)
        with open(os.path.join(dataHouseholdFolder, householdFile), "w") as file:
            writer = csv.writer(file, delimiter = ",", lineterminator='\r')
            writer.writerow((self.householdData))
            for member in self.displayHouse.occupants:
                data = [member.id, member.sex, member.age, member.careNeedLevel]
                writer.writerow(data)    
        
        houseData = [self.year, self.displayHouse.name, len(self.displayHouse.occupants)]
        with open(os.path.join(policyFolder, "HouseData.csv"), "a") as file:
            writer = csv.writer(file, delimiter = ",", lineterminator='\r')
            writer.writerow(houseData)
        
        malesByNeed = []
        for i in range(int(self.p['numCareLevels'])):
            malesByAge = []
            for j in range(25):
                subgroup = [x for x in self.pop.livingPeople if x.sex == 'male' and int(x.age/5) == j and x.careNeedLevel == i]
                malesByAge.append(len(subgroup))
            malesByNeed.append(malesByAge)
            
        femalesByNeed = []
        for i in range(int(self.p['numCareLevels'])):
            femalesByAge = []
            for j in range(25):
                subgroup = [x for x in self.pop.livingPeople if x.sex == 'female' and int(x.age/5) == j and x.careNeedLevel == i]
                femalesByAge.append(len(subgroup))
            femalesByNeed.append(femalesByAge)
        
        for i in range(int(self.p['numCareLevels'])):
            pyramidData = [self.year]
            pyramidData.extend(malesByNeed[i])
            fileName = 'Pyramid_Male_' + str(i) + '.csv'
            with open(os.path.join(policyFolder, fileName), "a") as file:
                writer = csv.writer(file, delimiter = ",", lineterminator='\r')
                writer.writerow(pyramidData)
            
        for i in range(int(self.p['numCareLevels'])):
            pyramidData = [self.year]
            pyramidData.extend(femalesByNeed[i])
            fileName = 'Pyramid_Female_' + str(i) + '.csv'
            with open(os.path.join(policyFolder, fileName), "a") as file:
                writer = csv.writer(file, delimiter = ",", lineterminator='\r')
                writer.writerow(pyramidData)
            
        houseData = [self.year, self.displayHouse.name, len(self.displayHouse.occupants)]
        with open(os.path.join(policyFolder, "HouseData.csv"), "a") as file:
            writer = csv.writer(file, delimiter = ",", lineterminator='\r')
            writer.writerow(houseData)
            
        if period == 1:
            if not os.path.exists(policyFolder):
                os.makedirs(policyFolder)
            with open(os.path.join(policyFolder, "Outputs.csv"), "w") as file:
                writer = csv.writer(file, delimiter = ",", lineterminator='\r')
                writer.writerow((self.Outputs))
                writer.writerow(outputs)
        else:
            with open(os.path.join(policyFolder, "Outputs.csv"), "a") as file:
                writer = csv.writer(file, delimiter = ",", lineterminator='\r')
                writer.writerow(outputs)
        
        self.marriageTally = 0
        self.divorceTally = 0
        
        ## Some extra debugging stuff just to check that all
        ## the lists are behaving themselves
        if self.p['verboseDebugging']:
            peopleCount = 0
            for i in self.pop.allPeople:
                if i.dead == False:
                    peopleCount += 1
            print "True pop counting non-dead people in allPeople list = ", peopleCount

            peopleCount = 0
            for h in self.map.occupiedHouses:
                peopleCount += len(h.occupants)
            print "True pop counting occupants of all occupied houses = ", peopleCount

            peopleCount = 0
            for h in self.map.allHouses:
                peopleCount += len(h.occupants)
            print "True pop counting occupants of ALL houses = ", peopleCount

            tally = [ 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
            for h in self.map.occupiedHouses:
                tally[len(h.occupants)] += 1
            for i in range(len(tally)):
                if tally[i] > 0:
                    print i, tally[i]
            print

            
    def healthCareCost(self):

        peopleWithUnmetNeed = [x for x in self.pop.livingPeople if x.careNeedLevel > 0]
        self.totalHospitalizationCost = 0
        for person in peopleWithUnmetNeed:
            needLevelFactor = math.pow(self.p['needLevelParam'], person.careNeedLevel)
            unmetSocialCareFactor = math.pow(self.p['unmetSocialCareParam'], person.averageShareUnmetNeed)
            averageHospitalization = self.p['hospitalizationParam']*needLevelFactor*unmetSocialCareFactor
            self.totalHospitalizationCost += averageHospitalization*self.p['costHospitalizationPerDay']
        self.hospitalizationCost.append(self.totalHospitalizationCost)
        
    def initializeCanvas(self):
        """Put up a TKInter canvas window to animate the simulation."""
        self.canvas.pack()

        ## Draw some numbers for the population pyramid that won't be redrawn each time
        for a in range(0,int(self.p['num5YearAgeClasses'])):
            self.canvas.create_text(170, 385 - (10 * a),
                                    text=str(5*a) + '-' + str(5*a+4),
                                    font='Helvetica 6',
                                    fill='white')

        ## Draw the overall map, including towns and houses (occupied houses only)
        for t in self.map.towns:
            xBasic = 580 + (t.x * self.p['pixelsPerTown'])
            yBasic = 15 + (t.y * self.p['pixelsPerTown'])
            self.canvas.create_rectangle(xBasic, yBasic,
                                         xBasic+self.p['pixelsPerTown'],
                                         yBasic+self.p['pixelsPerTown'],
                                         outline='grey',
                                         state = 'hidden' )

        for h in self.map.allHouses:
            t = h.town
            xBasic = 580 + (t.x * self.p['pixelsPerTown'])
            yBasic = 15 + (t.y * self.p['pixelsPerTown'])
            xOffset = xBasic + 2 + (h.x * 2)
            yOffset = yBasic + 2 + (h.y * 2)

            outlineColour = fillColour = self.p['houseSizeColour'][h.size]
            width = 1

            h.icon = self.canvas.create_rectangle(xOffset,yOffset,
                                                  xOffset + width, yOffset + width,
                                                  outline=outlineColour,
                                                  fill=fillColour,
                                                  state = 'normal' )

        self.canvas.update()
        time.sleep(0.5)
        self.canvas.update()

        for h in self.map.allHouses:
            self.canvas.itemconfig(h.icon, state='hidden')

        for h in self.map.occupiedHouses:
            self.canvas.itemconfig(h.icon, state='normal')

        self.canvas.update()
        self.updateCanvas()

    def updateCanvas(self):
        """Update the appearance of the graphics canvas."""

        ## First we clean the canvas off; some items are redrawn every time and others are not
        self.canvas.delete('redraw')

        ## Now post the current year and the current population size
        self.canvas.create_text(self.p['dateX'],
                                self.p['dateY'],
                                text='Year: ' + str(self.year),
                                font = self.p['mainFont'],
                                fill = self.p['fontColour'],
                                tags = 'redraw')
        self.canvas.create_text(self.p['popX'],
                                self.p['popY'],
                                text='Pop: ' + str(len(self.pop.livingPeople)),
                                font = self.p['mainFont'],
                                fill = self.p['fontColour'],
                                tags = 'redraw')

        self.canvas.create_text(self.p['popX'],
                                self.p['popY'] + 30,
                                text='Ever: ' + str(len(self.pop.allPeople)),
                                font = self.p['mainFont'],
                                fill = self.p['fontColour'],
                                tags = 'redraw')

        ## Also some other stats, but not on the first display
        if self.year > self.p['startYear']:
            self.canvas.create_text(350,20,
                                    text='Avg household: ' + str ( round ( self.avgHouseholdSize[-1] , 2 ) ),
                                    font = 'Helvetica 11',
                                    fill = 'white',
                                    tags = 'redraw')
            self.canvas.create_text(350,40,
                                    text='Marriages: ' + str(self.numMarriages[-1]),
                                    font = 'Helvetica 11',
                                    fill = 'white',
                                    tags = 'redraw')
            self.canvas.create_text(350,60,
                                    text='Divorces: ' + str(self.numDivorces[-1]),
                                    font = 'Helvetica 11',
                                    fill = 'white',
                                    tags = 'redraw')
            self.canvas.create_text(350,100,
                                    text='Total care demand: ' + str(round(self.totalCareDemand[-1], 0 ) ),
                                    font = 'Helvetica 11',
                                    fill = 'white',
                                    tags = 'redraw')
            self.canvas.create_text(350,120,
                                    text='Num taxpayers: ' + str(round(self.numTaxpayers[-1], 0 ) ),
                                    font = 'Helvetica 11',
                                    fill = 'white',
                                    tags = 'redraw')
            self.canvas.create_text(350,140,
                                    text='Family care ratio: ' + str(round(100.0 * self.totalFamilyCare[-1], 0 ) ) + "%",
                                    font = 'Helvetica 11',
                                    fill = 'white',
                                    tags = 'redraw')
            self.canvas.create_text(350,160,
                                    text='Tax burden: ' + str(round(self.totalTaxBurden[-1], 0 ) ),
                                    font = 'Helvetica 11',
                                    fill = 'white',
                                    tags = 'redraw')
            self.canvas.create_text(350,180,
                                    text='Marriage prop: ' + str(round(100.0 * self.marriageProp[-1], 0 ) ) + "%",
                                    font = 'Helvetica 11',
                                    fill = self.p['fontColour'],
                                    tags = 'redraw')

        

        ## Draw the population pyramid split by care categories
        for a in range(0,int(self.p['num5YearAgeClasses'])):
            malePixel = 153
            femalePixel = 187
            for c in range(0,self.p['numCareLevels']):
                mWidth = self.pyramid.maleData[a,c]
                fWidth = self.pyramid.femaleData[a,c]

                if mWidth > 0:
                    self.canvas.create_rectangle(malePixel, 380 - (10*a),
                                                 malePixel - mWidth, 380 - (10*a) + 9,
                                                 outline=self.p['careLevelColour'][c],
                                                 fill=self.p['careLevelColour'][c],
                                                 tags = 'redraw')
                malePixel -= mWidth
                
                if fWidth > 0:
                    self.canvas.create_rectangle(femalePixel, 380 - (10*a),
                                                 femalePixel + fWidth, 380 - (10*a) + 9,
                                                 outline=self.p['careLevelColour'][c],
                                                 fill=self.p['careLevelColour'][c],
                                                 tags = 'redraw')
                femalePixel += fWidth

        ## Draw in the display house and the people who live in it
        if len(self.displayHouse.occupants) < 1:
            ## Nobody lives in the display house any more, choose another
            if self.nextDisplayHouse != None:
                self.displayHouse = self.nextDisplayHouse
                self.nextDisplayHouse = None
            else:
                self.displayHouse = random.choice(self.pop.livingPeople).house
                self.textUpdateList.append(str(self.year) + ": Display house empty, going to " + self.displayHouse.name + ".")
                messageString = "Residents: "
                for k in self.displayHouse.occupants:
                    messageString += "#" + str(k.id) + " "
                self.textUpdateList.append(messageString)
            

        outlineColour = self.p['houseSizeColour'][self.displayHouse.size]
        self.canvas.create_rectangle( 50, 450, 300, 650,
                                      outline = outlineColour,
                                      tags = 'redraw' )
        self.canvas.create_text ( 60, 660,
                                  text="Display house " + self.displayHouse.name,
                                  font='Helvetica 10',
                                  fill='white',
                                  anchor='nw',
                                  tags='redraw')
                                  

        ageBracketCounter = [ 0, 0, 0, 0, 0 ]

        for i in self.displayHouse.occupants:
            age = self.year - i.birthdate
            ageBracket = age / 20
            if ageBracket > 4:
                ageBracket = 4
            careClass = i.careNeedLevel
            sex = i.sex
            idNumber = i.id
            self.drawPerson(age,ageBracket,ageBracketCounter[ageBracket],careClass,sex,idNumber)
            ageBracketCounter[ageBracket] += 1


        ## Draw in some text status updates on the right side of the map
        ## These need to scroll up the screen as time passes

        if len(self.textUpdateList) > self.p['maxTextUpdateList']:
            excess = len(self.textUpdateList) - self.p['maxTextUpdateList']
            self.textUpdateList = self.textUpdateList[excess:excess+self.p['maxTextUpdateList']]

        baseX = 1035
        baseY = 30
        for i in self.textUpdateList:
            self.canvas.create_text(baseX,baseY,
                                    text=i,
                                    anchor='nw',
                                    font='Helvetica 9',
                                    fill = 'white',
                                    width = 265,
                                    tags = 'redraw')
            baseY += 30

        ## Finish by updating the canvas and sleeping briefly in order to allow people to see it
        self.canvas.update()
        if self.p['delayTime'] > 0.0:
            time.sleep(self.p['delayTime'])


    def drawPerson(self, age, ageBracket, counter, careClass, sex, idNumber):
        baseX = 70 + ( counter * 30 )
        baseY = 620 - ( ageBracket * 30 )

        fillColour = self.p['careLevelColour'][careClass]

        self.canvas.create_oval(baseX,baseY,baseX+6,baseY+6,
                                fill=fillColour,
                                outline=fillColour,tags='redraw')
        if sex == 'male':
            self.canvas.create_rectangle(baseX-2,baseY+6,baseX+8,baseY+12,
                                fill=fillColour,outline=fillColour,tags='redraw')
        else:
            self.canvas.create_polygon(baseX+2,baseY+6,baseX-2,baseY+12,baseX+8,baseY+12,baseX+4,baseY+6,
                                fill=fillColour,outline=fillColour,tags='redraw')
        self.canvas.create_rectangle(baseX+1,baseY+13,baseX+5,baseY+20,
                                     fill=fillColour,outline=fillColour,tags='redraw')
            
            
            
        self.canvas.create_text(baseX+11,baseY,
                                text=str(age),
                                font='Helvetica 6',
                                fill='white',
                                anchor='nw',
                                tags='redraw')
        self.canvas.create_text(baseX+11,baseY+8,
                                text=str(idNumber),
                                font='Helvetica 6',
                                fill='grey',
                                anchor='nw',
                                tags='redraw')


    def doGraphs(self):
        """Plot the graphs needed at the end of one run."""
        
        

        p1, = pylab.plot(self.times,self.pops,color="red")
        p2, = pylab.plot(self.times,self.numTaxpayers,color="blue")
        pylab.legend([p1, p2], ['Total population', 'Taxpayers'],loc='lower right')
        pylab.xlim(xmin=self.p['statsCollectFrom'])
        pylab.ylabel('Number of people')
        pylab.xlabel('Year')
        pylab.savefig('popGrowth.pdf')
        pylab.show()
        pylab.close()

        pylab.plot(self.times,self.avgHouseholdSize,color="red")
        pylab.xlim(xmin=self.p['statsCollectFrom'])
        pylab.ylabel('Average household size')
        pylab.xlabel('Year')
        pylab.savefig('avgHousehold.pdf')
        pylab.show()
        pylab.close()

        p1, = pylab.plot(self.times,self.totalCareDemand,color="red")
        p2, = pylab.plot(self.times,self.totalCareSupply,color="blue")
        pylab.xlim(xmin=self.p['statsCollectFrom'])
        pylab.legend([p1, p2], ['Care demand', 'Total theoretical supply'],loc='lower right')
        pylab.ylabel('Total hours per week')
        pylab.xlabel('Year')
        pylab.savefig('totalCareSituation.pdf')
        pylab.show()

        pylab.plot(self.times,self.totalFamilyCare,color="red")
        pylab.xlim(xmin=self.p['statsCollectFrom'])
        pylab.ylabel('Proportion of informal social care')
        pylab.xlabel('Year')
        pylab.savefig('informalCare.pdf')
        pylab.show()

        pylab.plot(self.times,self.totalTaxBurden,color="red")
        pylab.xlim(xmin=self.p['statsCollectFrom'])
        pylab.ylabel('Care costs in pounds per taxpayer per year')
        pylab.xlabel('Year')
        pylab.savefig('taxBurden.pdf')
        pylab.show()

        pylab.plot(self.times,self.marriageProp,color="red")
        pylab.xlim(xmin=self.p['statsCollectFrom'])
        pylab.ylabel('Proportion of married adult women')
        pylab.xlabel('Year')
        pylab.savefig('marriageProp.pdf')
        pylab.savefig('marriageProp.png')
        pylab.show()
        
        pylab.plot(self.times,self.shareLoneParents,color="red")
        pylab.xlim(xmin=self.p['statsCollectFrom'])
        pylab.ylabel('Share of Lone Parents')
        pylab.xlabel('Year')
        pylab.savefig('shareLoneParents.pdf')
        pylab.savefig('shareLoneParents.png')
        pylab.show()
        
        pylab.plot(self.times, self.shareUnmetNeed, color="red")
        pylab.xlim(xmin=self.p['statsCollectFrom'])
        pylab.ylabel('Share of Unmet Care Need')
        pylab.xlabel('Year')
        pylab.savefig('shareUnmetCareNeed.pdf')
        pylab.savefig('shareUnmetCareNeed.png')
        pylab.show()
        
        pylab.plot(self.times, self.hospitalizationCost, color="red")
        pylab.xlim(xmin=self.p['statsCollectFrom'])
        pylab.ylabel('Hospitalisation Cost')
        pylab.xlabel('Year')
        pylab.savefig('hospitalisationCost.pdf')
        pylab.savefig('hospitalisationCost.png')
        pylab.show()
        
        pylab.plot(self.times, self.employmentRate, color="red")
        pylab.xlim(xmin=self.p['statsCollectFrom'])
        pylab.ylabel('Employment Rate')
        pylab.xlabel('Year')
        pylab.savefig('employmentRate.pdf')
        pylab.savefig('employmentRate.png')
        pylab.show()
        
        pylab.plot(self.times, self.publicCareProvision, color="red")
        pylab.xlim(xmin=self.p['statsCollectFrom'])
        pylab.ylabel('Public Care Provision')
        pylab.xlabel('Year')
        pylab.savefig('publicCareProvision.pdf')
        pylab.savefig('publicCareProvision.png')
        pylab.show()
        
        y_pos = np.arange(len(self.sesPopsShares))
        plt.bar(y_pos, self.sesPopsShares)
        plt.ylabel('SES Populations')
        plt.show()
        
        lenFrequency = len(self.incomeDistribution)
        individualIncomeFrequencies = [0]*lenFrequency

        dK = np.random.normal(0, self.p['wageVar'])
        indDist = np.random.choice(self.incomesPercentiles, len(self.individualIncomes))*math.exp(dK)
        for i in indDist:
            ind = int(i/1000)
            if ind > -1 and ind < lenFrequency:
                individualIncomeFrequencies[ind] += 1
                
        y_pos = np.arange(lenFrequency)
        plt.bar(y_pos, individualIncomeFrequencies)
        plt.ylabel('individual frequency (empirical)')
        plt.show()
        
        lenFrequency = len(self.incomeDistribution)
        individualIncomeFrequencies = [0]*lenFrequency
        for i in self.individualIncomes:
            ind = int(i/1000)
            if ind > -1 and ind < lenFrequency:
                individualIncomeFrequencies[ind] += 1
                
        y_pos = np.arange(lenFrequency)
        plt.bar(y_pos, individualIncomeFrequencies)
        plt.ylabel('individual frequency (simulated)')
        plt.show()
        
        df = pd.DataFrame()
        df[0] = self.individualIncomes
        df[1] = indDist
        fig, ax = plt.subplots(1,1)
        for s in df.columns:
            df[s].plot(kind='density')
        fig.show()
    

class PopPyramid:
    """Builds a data object for storing population pyramid data in."""
    def __init__ (self, ageClasses, careLevels):
        self.maleData = pylab.zeros((int(ageClasses), int(careLevels)),dtype=int)
        self.femaleData = pylab.zeros((int(ageClasses), int(careLevels)),dtype=int)

    def update(self, year, ageClasses, careLevels, pixelFactor, people):
        ## zero the two arrays
        for a in range (int(ageClasses)):
            for c in range (int(careLevels)):
                self.maleData[a,c] = 0
                self.femaleData[a,c] = 0
        ## tally up who belongs in which category
        for i in people:
            ageClass = ( year - i.birthdate ) / 5
            if ageClass > ageClasses - 1:
                ageClass = ageClasses - 1
            careClass = i.careNeedLevel
            if i.sex == 'male':
                self.maleData[int(ageClass), int(careClass)] += 1
            else:
                self.femaleData[int(ageClass), int(careClass)] += 1

        ## normalize the totals into pixels
        total = len(people)        
        for a in range (int(ageClasses)):
            for c in range (int(careLevels)):
                self.maleData[a,c] = pixelFactor * self.maleData[a,c] / total
                self.femaleData[a,c] = pixelFactor * self.femaleData[a,c] / total
