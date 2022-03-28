# -*- coding: utf-8 -*-
"""
Created on Mon Oct 25 21:18:38 2021

@author: Umberto Gostoli
"""

class Shift:
    def __init__ (self, days, hour, hourIndex, shiftHours, socInd):
        self.days = days
        self.start = hour
        self.startIndex = hourIndex
        self.shiftHours = shiftHours
        self.finish = self.start+8
        self.socialIndex = socInd

class CostUnit:
    def __init__ (self, day, hour, cost, children, numSuppliers, suppliers):
        self.day = day
        self.hour = hour
        self.cost = cost
        self.children = children
        self.numSuppliers = numSuppliers
        self.suppliers = suppliers
        
class CareSlot:
    counter = 1
    def __init__ (self, house, day, hour, isChildcare, careWeight, probIndex, cost, receivers, suppliers):
        self.house = house
        self.day = day
        self.hour = hour
        self.childCare = isChildcare
        self.careWeight = careWeight
        self.probIndex = probIndex
        self.cost = cost
        self.receivers = receivers
        self.suppliers = suppliers
        self.numReceivers = len(receivers)
        self.numSuppliers = len(suppliers)
        self.ageReceivers = [x.age for x in receivers]
        self.minAge = min(self.ageReceivers)
        self.id = CareSlot.counter
        CareSlot.counter += 1