'''
Created on 31 de mar de 2017

@author: fvj
'''
from random import shuffle

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
        if countSuit(card, cards) >= 5:
            return True
    return False

def hasStraight(cards):
    ordered = order(cards)
    diff = [i-j for i, j in zip(ordered[:-1], ordered[1:])]
    if 0 in diff:
        diff.remove(0)
    count = 0
    for i in diff:
        if i == 1:
            count += 1
            if count == 4:
                return True
        else:
            count = 0
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

def countSuit(card, cards):
    count = 0
    for c in cards:
        if c.suit == card.suit:
            count += 1
    return count

def getProbability(occurences, total):
    if occurences == 0:
        return ' 0.00%'
    return '{:6.2%} (1 in {:.1f})'.format(occurences/games, games/occurences)

games = 10000

pocketPair = 0

fourOfAKind = 0
fullHouse = 0
flush = 0
straight = 0
threeOfAKind = 0
twoPairs = 0
pairedCards = 0
noShit = 0

print('Gathering statistics on {} games...'.format(games))

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
        
    if hasFourOfAKind(availableCards):
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

print("---- Results ----")        
print("Four of a Kind:  " + getProbability(fourOfAKind, games))
print("Full House:      " + getProbability(fullHouse, games))
print("Flush:           " + getProbability(flush, games))
print("Straight:        " + getProbability(straight, games))
print("Three of a Kind: " + getProbability(threeOfAKind, games))
print("Two Pairs:       " + getProbability(twoPairs, games))
print("Pair:            " + getProbability(pairedCards, games))
print("Fucking nothing: " + getProbability(noShit, games))
print("---")
print("TOTAL:          " + getProbability(fourOfAKind+fullHouse+flush+straight+threeOfAKind+twoPairs+pairedCards+noShit, games))
print()
print("Pocket Pairs:    " + getProbability(pocketPair, games))






