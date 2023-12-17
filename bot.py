import random
import pokersim


class bot(): #maybe move into pokersim later
  def __init__(self, currentHand, risk, difficulty):
    self.__currentHand = currentHand
    self.risk = risk  #0-1 the probability threshold for a card to appear which would be accepted 
    self.difficulty = difficulty  #easy, med, hard - how genuinely smart the bot is
    #chance of fold/check/bet in ranges of probabilities
    #get and use highest_bet to determine next action
    #replace player objects in player_dict with bot() objects
    #use same GetAction() functions as player() class in order to implement later

  def Calculate(self, stage): # more vars
    pass
    #calculate if next is a pair, a 
    #for every card not in currently known, calculate next card achieving that combination
    #therefore probability of each combination with the current hand
    #consider integration with pokersim findCombination() functions which will require importing

  def StartingHand(self): 
    suit1, value1 = self.__currentHand[0].split(".")
    suit2, value2 = self.__currentHand[1].split(".")
    
    if suit1 == suit2:
      print("onsuit")
    elif value1 == value2:
      print("pair")
      # a face value card A-J
      # is consecutive
    pass #rating

  def GetChoice(self):
    pass

  def RollRisk(self, probability):
    pass  #change

  def Strategy1(self):
    pass



hand = ["hearts.14", "spades.14"]
bot1 = bot(hand, 1, "easy")
bot1.StartingHand()