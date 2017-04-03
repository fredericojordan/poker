'''
Created on 31 de mar de 2017

@author: fvj
'''
from random import shuffle
from time import time

# Royal flush       0.0032%
# Straight flush    0.0279%
# Four of a kind    0.168%
# Full house        2.60%
# Flush             3.03%
# Straight          4.62%
# Three of a kind   4.83%
# Two pair         23.5%
# One pair         43.8%
# High card        17.4%

CARD_RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
CARD_SUITS = ['♦', '♠', '♥', '♣']

class Card:
    def __init__(self, value, suit):
        self.rank = value
        self.suit = suit
    def __repr__(self):
        return str(self.rank) + str(self.suit)
    def __gt__(self, Card):
        return CARD_RANKS.index(self.rank) > CARD_RANKS.index(Card.rank)
    def __ge__(self, Card):
        return CARD_RANKS.index(self.rank) >= CARD_RANKS.index(Card.rank)
    def __lt__(self, Card):
        return CARD_RANKS.index(self.rank) < CARD_RANKS.index(Card.rank)
    def __le__(self, Card):
        return CARD_RANKS.index(self.rank) <= CARD_RANKS.index(Card.rank)
    def __eq__(self, Card):
        return CARD_RANKS.index(self.rank) == CARD_RANKS.index(Card.rank)
    def __ne__(self, Card):
        return CARD_RANKS.index(self.rank) != CARD_RANKS.index(Card.rank)
    def __sub__(self, Card):
        return CARD_RANKS.index(self.rank) - CARD_RANKS.index(Card.rank)  
    
FULL_DECK = [Card(value,suit) for suit in CARD_SUITS for value in CARD_RANKS]

def getRandomDeck():
    deck = list(FULL_DECK)
    shuffle(deck)
    return deck

def getSuited(cards, suit):
    suited = []
    for c in cards:
        if c.suit == suit:
            suited.append(c)
    return suited

def hasPair(cards):
    for card in cards:
        if countSameRank(card, cards) == 2:
            return True
    return False

def hasTwoPairs(cards):
    pairedCards = 0
    for card in cards:
        if countSameRank(card, cards) == 2:
            pairedCards += 1
    return pairedCards >= 4 # 2 pairs = 4 cards

def hasThreeOfAKind(cards):
    for card in cards:
        if countSameRank(card, cards) == 3:
            return True
    return False

def hasFourOfAKind(cards):
    for card in cards:
        if countSameRank(card, cards) == 4:
            return True
    return False

def hasFullHouse(cards):
    return hasPair(cards) and hasThreeOfAKind(cards)

def hasFlush(cards):
    for card in cards:
        if countSameSuit(card, cards) >= 5:
            return True
    return False

def hasStraight(cards):
    ordered = order(cards)
    
    for c in cards:
        if c == Card('A', ''):
            ordered.append(c)
            
    diff = [i-j for i, j in zip(ordered[:-1], ordered[1:])]
    
    if 0 in diff:
        diff.remove(0)
        
    count = 0
    for i in diff:
        if i == 1 or i == -12:
            count += 1
            if count == 4:
                return True
        else:
            count = 0
    return False

def hasStraightFlush(cards):
    for suit in CARD_SUITS:
        suited = getSuited(cards, suit)
        if hasStraight(suited):
            return True
    return False

def hasRoyalStraightFlush(cards):
    for suit in CARD_SUITS:
        suited = getSuited(cards, suit)
        if sameOrHigherCount(Card('10',''), suited) >= 5:
            return True
    return False

def getHighCard(cards):
    high = cards[0]
    for c in cards:
        if c > high:
            high = c
    return high

def order(cards):
    tempCards = list(cards)
    ordered = []
    while tempCards:
        high = getHighCard(tempCards)
        tempCards.remove(high)
        ordered.append(high)
    return ordered

def countSameRank(card, cards):
    count = 0
    for c in cards:
        if c == card:
            count += 1
    return count

def countSameSuit(card, cards):
    count = 0
    for c in cards:
        if c.suit == card.suit:
            count += 1
    return count

def getProbability(occurences, total):
    if occurences == 0:
        return ' 0.000%'
    return '{:7.3%} (1 in {:.1f})'.format(occurences/games, games/occurences)

def sameOrHigherCount(card, cards):
    count = 0
    for c in cards:
        if c >= card:
            count += 1
    return count

games = 1000000

pocketPair = 0
pocketFaces = 0

royalFlush = 0
straightFlush = 0
fourOfAKind = 0
fullHouse = 0
flush = 0
straight = 0
threeOfAKind = 0
twoPairs = 0
pairedCards = 0
noShit = 0

print('Gathering statistics on {} games...'.format(games))

start = time()
for _ in range(games):
    newDeck = getRandomDeck()
    
    myHand = [newDeck.pop(), newDeck.pop()]
    newDeck.pop() # burn
    flop = [newDeck.pop(), newDeck.pop(), newDeck.pop()]
    newDeck.pop() # burn
    turn = [newDeck.pop()]
    newDeck.pop() # burn
    river = [newDeck.pop()]
    
    availableCards = myHand+flop+turn+river
    
    if hasPair(myHand):
        pocketPair += 1
    
    if sameOrHigherCount(Card('J', ''), myHand) == 2:
        pocketFaces += 1
    
    if hasRoyalStraightFlush(availableCards):
        royalFlush += 1
    elif hasStraightFlush(availableCards):
        straightFlush += 1
    elif hasFourOfAKind(availableCards):
        fourOfAKind += 1
    elif hasFullHouse(availableCards):
        fullHouse += 1
    elif hasFlush(availableCards):
        flush += 1
    elif hasStraight(availableCards):
        straight += 1
    elif hasThreeOfAKind(availableCards):
        threeOfAKind += 1
    elif hasTwoPairs(availableCards):
        twoPairs += 1
    elif hasPair(availableCards):
        pairedCards += 1
    else:
        noShit += 1

print("Took {:.1f} seconds".format(time()-start))
print("---- Results ----")
print("Royal flush:     " + getProbability(royalFlush, games))
print("Straight flush:  " + getProbability(straightFlush, games))
print("Four of a Kind:  " + getProbability(fourOfAKind, games))
print("Full House:      " + getProbability(fullHouse, games))
print("Flush:           " + getProbability(flush, games))
print("Straight:        " + getProbability(straight, games))
print("Three of a Kind: " + getProbability(threeOfAKind, games))
print("Two Pairs:       " + getProbability(twoPairs, games))
print("Pair:            " + getProbability(pairedCards, games))
print("Fucking nothing: " + getProbability(noShit, games))
print("---")
print("TOTAL:          " + getProbability(royalFlush+straightFlush+fourOfAKind+fullHouse+flush+straight+threeOfAKind+twoPairs+pairedCards+noShit, games))
print()
print("Pocket Pairs:    " + getProbability(pocketPair, games))
print("Pocket faces:    " + getProbability(pocketFaces, games))