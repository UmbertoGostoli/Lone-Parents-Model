
import random
import numpy as np
import networkx as nx

class House:
    counter = 1
    """The house class stores information about a distinct house in the sim."""
    def __init__ (self, town, cdfHouseClasses, classBias, hx, hy):
        r = random.random()
        i = 0
        c = cdfHouseClasses[i] - classBias
        while r > c:
            i += 1
            c = cdfHouseClasses[i] - classBias
        self.size = i
        self.sizeIndex = -1
        self.wealth = 0
        self.occupants = []
        self.occupantsID = []  # For pickle
        self.newOccupancy = False
        self.town = town
        self.x = hx
        self.y = hy
        self.icon = None
        self.display = False
        self.wealthForCare = 0
        self.householdCumulativeIncome = 0
        self.householdIncome = 0
        self.householdDisposableIncome = 0
        self.householdNetIncome = 0
        self.costFormalCare = 0
        self.incomePerCapita = 0
        self.disposableIncomePerCapita = 0
        self.netIncomePerCapita = 0
        self.incomeQuintile = 0
        self.disposableIncomeQuintile = 0
        self.netIncomeQuintile = 0
        self.yearlyIncome = 0
        self.yearlyDisposableIncome = 0
        self.benefits = 0
        self.yearlyBenefits = 0
        self.totalIncome = 0
        self.totalPotentialIncome = 0
        self.potentialIncomeFromWork = 0
        self.potentialIncomeFromWelfare = 0
        self.povertyLineIncome = 0
        self.name = self.town.name + "-" + str(hx) + "-" + str(hy)
        self.sizeIndex = -1
        self.id = House.counter
        
        # House care variables
        self.careNetwork = nx.DiGraph()
        self.demandNetwork = nx.Graph()
        self.townAttractiveness = []
        self.availableWeeklySupplies = []
        self.needAfterHouseholdCare = 0
        
        self.residualCareNeed_PreFormal = 0
        self.residualCareNeed_PostFormal = 0
        self.unmetChildCareNeed_Pre = 0
        self.totalCareNeed_Pre = 0
        self.totalPriorityCareSlots_Pre = 0
        self.totalChildCareSlots_Pre = 0
        self.totalOutOfWorkChildCare_Pre = 0
        self.totalOutOfWorkChildCare_Post = 0
        self.onhSlots_Pre = 0
        self.wnhSlots_Pre = 0
        self.slotWithCareSuppliers_ONH = 0
        self.slotWithCareSuppliers_WNH = 0
        self.numCostGreaterThanWage = 0
        self.numNoSuppliers = 0
        self.numCostSmallerThanWage = 0
        
        
        self.netCareDemand = 0
        self.careAttractionFactor = 0
        self.totalUnmetSocialCareNeed = 0
        self.totalUnmetChildCareNeed = 0
        self.privateChildCareNeed_ONH = 0
        self.privateChildCareNeed_WNH = 0
        self.totalChildCareNeed = 0
        self.totalSocialCareNeed = 0
        self.totalCareNeed = 0
        self.numChildcareReceivers = 0
        self.childCareNeeds = []
        self.childCarePrices = []
        self.cumulatedChildren = []
        self.highPriceChildCare = 0
        self.lowPriceChildCare = 0
        self.residualIncomeForChildCare = 0
        self.initialResidualIncomeForChildCare = 0
        self.residualIncomeForSocialCare = []
        self.carers = []
        self.childCareRecipients = []
        self.socialCareRecipients = []
        self.shiftTable = []
        self.d1WeeklySupplyData = []
        self.totalD1Supply = []
        self.totalD1Supply_ONH = []
        self.totalD1Supply_WNH = []
        self.d1SuppliesSchedule = []
        self.d1WeeklySuppliers = []
        self.carriedOverCost = 0
        self.d1Households = []
        self.d2Households = []
        self.d1CareSupply = 0
        self.d2CareSupply = 0
        
        
        self.d2WeeklySupplyData = []
        self.totalD2Supply = []
        self.totalD2Supply_ONH = []
        self.totalD2Supply_WNH = []
        self.d2SuppliesSchedule = []
        self.d2WeeklySuppliers = []
        
        self.careSlots = []
        self.priorityCareSlots = []
        self.maxHourSuppliers = []
        self.totalChilcareNeed = 0
        self.totalChilcareNeed_ONH = 0
        self.totalChilcareNeed_WNH = 0
        self.totalSocialCareNeed = 0
        self.totalPriorityCareNeed = 0
        self.numberOfCarers = 0
        self.householdInformalSupplies = []
        self.householdInformalSupplySchedule = []
        self.householdInformalSuppliers = []
        self.childrenCareNeedSchedule = []
        self.childMinAge = []
        self.childrenAges = []
        self.weeklyChildCareCosts = []
        self.costUnits = []
        self.childrenInNeedByHour = []
        self.householdFormalSupply = []
        self.networkSupply = 0
        self.suppliers = []
        self.receivers = []
        self.networkSupport = 0
        self.networkTotalSupplies = []
        self.totalSupplies = []
        self.netCareSupply = 0
        self.networkInformalSupplies = []
        self.formalChildCareSupply = 0
        self.formalSocialCare = 0
        self.formalChildCare = 0
        self.costFormalSocialCare = 0
        self.costFormalChildCare = 0
        self.networkFormalSocialCareSupplies = []
        self.childCareWeights = []
        self.formalCaresRatios = []
        self.informalChildCareReceived = 0
        self.informalSocialCareReceived = 0
        self.formalChildCareReceived = 0
        self.formalChildCareCost = 0
        self.formalSocialCareReceived = 0
        self.householdFormalSupplyCost = 0
        self.outOfWorkSocialCare = 0
        self.incomeByTaxBand = []
        self.ownershipIndex = 0
        self.ownedByOccupants = False
        self.ageOccupants = -1
        self.incomeDecile = -1
        self.averageChildCarePrice = 0
        self.gettingUC = False
        self.gettingPC = False
        self.gettingDB = False
        self.gettingBenefits = False
        
        House.counter += 1
                            
class Town:
    counter = 1
    """Contains a collection of houses."""
    def __init__ (self, townGridDimension, tx, ty,
                  cdfHouseClasses, density, classBias, densityModifier,
                  lha1, lha2, lha3, lha4):
        self.x = tx
        self.y = ty
        self.houses = []
        self.name = str(tx) + "-" + str(ty)
        self.LHA = [lha1, lha2, lha3, lha4]
        self.id = Town.counter
        Town.counter += 1
        if density > 0.0:
            adjustedDensity = density * densityModifier
            for hy in range(int(townGridDimension)):
                for hx in range(int(townGridDimension)):
                    if random.random() < adjustedDensity:
                        newHouse = House(self,cdfHouseClasses,
                                         classBias,hx,hy)
                        self.houses.append(newHouse)

class Map:
    """Contains a collection of towns to make up the whole country being simulated."""
    def __init__ (self, gridXDimension, gridYDimension,
                  townGridDimension, cdfHouseClasses,
                  ukMap, ukClassBias, densityModifier,
                  lha1, lha2, lha3, lha4):
        self.towns = []
        self.allHouses = []
        self.occupiedHouses = []
        ukMap = np.array(ukMap)
        ukMap.resize(int(gridYDimension), int(gridXDimension))
        ukClassBias = np.array(ukClassBias)
        ukClassBias.resize(int(gridYDimension), int(gridXDimension))
        lha1 = np.array(lha1)
        lha1.resize(int(gridYDimension), int(gridXDimension))
        lha2 = np.array(lha1)
        lha2.resize(int(gridYDimension), int(gridXDimension))
        lha3 = np.array(lha1)
        lha3.resize(int(gridYDimension), int(gridXDimension))
        lha4 = np.array(lha1)
        lha4.resize(int(gridYDimension), int(gridXDimension))
        for y in range(int(gridYDimension)):
            for x in range(int(gridXDimension)):
                newTown = Town(townGridDimension, x, y,
                               cdfHouseClasses, ukMap[y][x],
                               ukClassBias[y][x], densityModifier,
                               lha1[y][x], lha2[y][x], lha3[y][x], lha4[y][x])
                self.towns.append(newTown)

        for t in self.towns:
            for h in t.houses:
                self.allHouses.append(h)




