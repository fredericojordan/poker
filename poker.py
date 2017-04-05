'''
Created on 31 de mar de 2017

@author: fvj
'''
from random import shuffle
from time import time, sleep

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

class Player:
    def __init__(self, pot):
        self.hand = []
        self.pot = pot

def getRandomDeck():
    deck = list(FULL_DECK)
    shuffle(deck)
    return deck

def getSameSuit(suit, cards):
    suited = []
    for c in cards:
        if c.suit == suit:
            suited.append(c)
    return suited

def getSameRank(rank, cards):
    sameRankCards = []
    for c in cards:
        if c.rank == rank:
            sameRankCards.append(c)
    return sameRankCards

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
    return len(getSameRank(card.rank, cards))

def countSameSuit(card, cards):
    return len(getSameSuit(card.suit, cards))

###############################################################################

def getPairs(cards):
    pairs = []
    for card in cards:
        if countSameRank(card, cards) == 2:
            pairs.append(card)
    return order(pairs)

def getThreeOfAKind(cards):
    trips = []
    for card in cards:
        if countSameRank(card, cards) == 3:
            trips.append(card)
    return trips

def getStraight(cards):
    ordered = order(cards)
    
    for c in cards:
        if c == Card('A', ''):
            ordered.append(c)
            
    diff = [i-j for i, j in zip(ordered[:-1], ordered[1:])]
    
    dupes = 0
    count = 0
    start = -1
    for i in range(len(diff)):
        if diff[i] == 1 or diff[i] == -12:
            count += 1
            if count == 4:
                start = i-3-dupes
                end = i+2
        elif diff[i] == 0:
            dupes += 1
        else:
            count = 0
            dupes = 0
            
    if start == -1:
        return []
    else:
        return ordered[start:end]  # FIXME: remove duplicates

def getFlush(cards):
    for suit in CARD_SUITS:
        suited = getSameSuit(suit, cards)
        if len(suited) >= 5:
            return order(suited)
    return []

def getFullHouse(cards):
    return getThreeOfAKind(cards) + getPairs(cards)

def getFourOfAKind(cards):
    quads = []
    for card in cards:
        if countSameRank(card, cards) == 4:
            quads.append(card)
    return quads

def getStraightFlush(cards):
    for suit in CARD_SUITS:
        suited = getSameSuit(suit, cards)
        if hasStraight(suited):
            return getStraight(suited)
    return []

def getRoyalStraightFlush(cards):
    if hasRoyalStraightFlush(cards):
        return getStraightFlush(cards)
    else:
        return []

###############################################################################

def hasPair(cards):
    return len(getPairs(cards)) > 0

def hasTwoPairs(cards):
    return len(getPairs(cards)) > 2

def hasThreeOfAKind(cards):
    return len(getThreeOfAKind(cards)) > 0

def hasFourOfAKind(cards):
    return len(getFourOfAKind(cards)) > 0

def hasFullHouse(cards):
    return hasPair(cards) and hasThreeOfAKind(cards)

def hasFlush(cards):
    return len(getFlush(cards)) > 0

def hasStraight(cards):
    return len(getStraight(cards)) > 0

def hasStraightFlush(cards):
    return len(getStraightFlush(cards)) > 0

def hasRoyalStraightFlush(cards):
    for suit in CARD_SUITS:
        suited = getSameSuit(suit, cards)
        if sameOrHigherCount(Card('10',''), suited) >= 5:
            return True
    return False

###############################################################################

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

def getHandCode(cards):
    if hasRoyalStraightFlush(cards):
        return 9
    elif hasStraightFlush(cards):
        return 8
    elif hasFourOfAKind(cards):
        return 7
    elif hasFullHouse(cards):
        return 6
    elif hasFlush(cards):
        return 5
    elif hasStraight(cards):
        return 4
    elif hasThreeOfAKind(cards):
        return 3
    elif hasTwoPairs(cards):
        return 2
    elif hasPair(cards):
        return 1
    else:
        return 0

def getKickerValue(cards):
    if hasRoyalStraightFlush(cards):
        return 0
    elif hasStraightFlush(cards):
        return CARD_RANKS.index(getStraightFlush(cards)[0].rank)
    elif hasFourOfAKind(cards):
        return CARD_RANKS.index(getFourOfAKind(cards)[0].rank)
    elif hasFullHouse(cards):
        return CARD_RANKS.index(getFullHouse(cards)[0].rank)
    elif hasFlush(cards):
        return CARD_RANKS.index(getFlush(cards)[0].rank)
    elif hasStraight(cards):
        return CARD_RANKS.index(getStraight(cards)[0].rank)
    elif hasThreeOfAKind(cards):
        return CARD_RANKS.index(getThreeOfAKind(cards)[0].rank)
    elif hasTwoPairs(cards):
        return CARD_RANKS.index(getPairs(cards)[0].rank)
    elif hasPair(cards):
        return CARD_RANKS.index(getPairs(cards)[0].rank)
    else:
        return CARD_RANKS.index(getHighCard(cards).rank)

def getHandValue(cards): # FIXME: differentiate between same hands and kicker
    hand = getHandCode(cards) << 5*4
    kicker = getKickerValue(cards) << 4*4
    return hand + kicker

games = 1000000

pocketPair = 0
pocketFaces = 0
pocketSuitedFaces = 0

royalFlush = 0
straightFlush = 0
fourOfAKind = 0
fullHouse = 0
flush = 0
straight = 0
threeOfAKind = 0
twoPairs = 0
pairedCards = 0
noPair = 0

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
    
#     print(format(getHandValue(availableCards), '#08x') + ' ' + str(order(availableCards)))
    
    if hasPair(myHand):
        pocketPair += 1
    
    if sameOrHigherCount(Card('J', ''), myHand) == 2:
        pocketFaces += 1
        
    if sameOrHigherCount(Card('J', ''), myHand) == 2 and countSameSuit(myHand[0], myHand) == 2:
        pocketSuitedFaces += 1
    
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
        noPair += 1

print("Took {:.1f} seconds".format(time()-start))
print()
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
print("No pair:         " + getProbability(noPair, games))
print("---")
print("TOTAL:          " + getProbability(royalFlush+straightFlush+fourOfAKind+fullHouse+flush+straight+threeOfAKind+twoPairs+pairedCards+noPair, games))
print()
print("---- Pocket ----")
print("Pairs:           " + getProbability(pocketPair, games))
print("Faces:           " + getProbability(pocketFaces, games))
print("Suited faces:    " + getProbability(pocketSuitedFaces, games))