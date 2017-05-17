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

HAND_DESCRIPTION = ["No Pair:        ", \
                    "Pair:           ", \
                    "Two Pairs:      ", \
                    "Three of a Kind:", \
                    "Straight:       ", \
                    "Flush:          ", \
                    "Full House:     ", \
                    "Four of a Kind: ", \
                    "Straight Flush: ", \
                    "Royal Flush:    "]

DEFAULT_MAX_GAME_COUNT = 100000

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
    def __add__(self, Card):
        return CARD_RANKS.index(self.rank) + CARD_RANKS.index(Card.rank)  
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
    return order(trips)

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
        return ordered[start:end]

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

def hasFullHouse(cards): #FIXME
    return (hasThreeOfAKind(cards) and hasPair(cards)) or \
        (len(getThreeOfAKind(cards)) > 3)

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
        return '  0.000%'
    return '{:8.3%} (1 in {:.1f})'.format(occurences/total, total/occurences)

def sameOrHigherCount(card, cards):
    count = 0
    for c in cards:
        if c >= card:
            count += 1
    return count

def getHandCode(cards):
    code = 0
    
    if hasRoyalStraightFlush(cards):
        code = 9
    elif hasStraightFlush(cards):
        code = 8
    elif hasFourOfAKind(cards):
        code = 7
    elif hasFullHouse(cards):
        code = 6
    elif hasFlush(cards):
        code = 5
    elif hasStraight(cards):
        code = 4
    elif hasThreeOfAKind(cards):
        code = 3
    elif hasTwoPairs(cards):
        code = 2
    elif hasPair(cards):
        code = 1
    
    return code << 5*4

def getHandDescription(score):
    code = score & (0xf<<5*4)
    code = code >> 5*4
    return HAND_DESCRIPTION[code].strip().rstrip(':')

def getKickersValue(cards):
    if hasRoyalStraightFlush(cards):
        return 0
    elif hasStraightFlush(cards):
        return CARD_RANKS.index(getStraightFlush(cards)[0].rank) << 4*4
    elif hasFourOfAKind(cards):
        ordCards = order(cards)
        value = CARD_RANKS.index(getFourOfAKind(cards)[0].rank) << 4*4    
        for card in getFourOfAKind(cards):
            ordCards.remove(card)
        return value + (CARD_RANKS.index(ordCards[0].rank) << 3*4)
    elif hasFullHouse(cards):
        return (CARD_RANKS.index(getFullHouse(cards)[0].rank) << 4*4) + (CARD_RANKS.index(getFullHouse(cards)[3].rank) << 3*4)
    elif hasFlush(cards):
        return (CARD_RANKS.index(getFlush(cards)[0].rank) << 4*4) + \
            (CARD_RANKS.index(getFlush(cards)[1].rank) << 3*4) + \
            (CARD_RANKS.index(getFlush(cards)[2].rank) << 2*4) + \
            (CARD_RANKS.index(getFlush(cards)[3].rank) << 1*4) + \
            CARD_RANKS.index(getFlush(cards)[4].rank)
    elif hasStraight(cards):
        return CARD_RANKS.index(getStraight(cards)[0].rank) << 4*4 
    elif hasThreeOfAKind(cards):
        ordCards = order(cards)
        value = CARD_RANKS.index(getThreeOfAKind(cards)[0].rank) << 4*4
        for card in getThreeOfAKind(cards):
            ordCards.remove(card)
        return value + (CARD_RANKS.index(ordCards[0].rank) << 3*4) + (CARD_RANKS.index(ordCards[1].rank) << 2*4) 
    elif hasTwoPairs(cards):
        ordCards = order(cards)
        value = (CARD_RANKS.index(getPairs(cards)[0].rank) << 4*4) + (CARD_RANKS.index(getPairs(cards)[2].rank) << 3*4)  
        for card in getPairs(cards)[:4]:
            ordCards.remove(card)
        return value + (CARD_RANKS.index(ordCards[0].rank) << 2*4)
    elif hasPair(cards):
        ordCards = order(cards)
        value = CARD_RANKS.index(getPairs(cards)[0].rank) << 4*4 
        for card in getPairs(cards):
            ordCards.remove(card)
        return value + (CARD_RANKS.index(ordCards[0].rank) << 3*4) + \
            (CARD_RANKS.index(ordCards[1].rank) << 2*4) + \
            (CARD_RANKS.index(ordCards[2].rank) << 1*4) + \
            CARD_RANKS.index(ordCards[3].rank)
    else:
        ordCards = order(cards)
        return (CARD_RANKS.index(ordCards[0].rank) << 4*4) + \
            (CARD_RANKS.index(ordCards[1].rank) << 3*4) + \
            (CARD_RANKS.index(ordCards[2].rank) << 2*4) + \
            (CARD_RANKS.index(ordCards[3].rank) << 1*4) + \
            CARD_RANKS.index(ordCards[4].rank) 

def getHandValue(cards):
    return getHandCode(cards) + getKickersValue(cards)

def playHand(players):
    newDeck = getRandomDeck()
    hands = {}
    for player in players:
        hands[player] = [newDeck.pop(), newDeck.pop()]

    flop = [newDeck.pop(), newDeck.pop(), newDeck.pop()]
    turn = [newDeck.pop()]
    river = [newDeck.pop()]
    
#     print(order(flop+turn+river))
    
    best_score = 0
    best_player = []
    best_hand = []
        
    for player, hand in hands.items():
        availableCards = hand+flop+turn+river
        player_score = getHandValue(availableCards)
        
#         print(str(player) + ': 0x' + str(format(player_score, '06x')) + ' ' + str(order(hand)))
         
        if player_score > best_score:
            best_player = [player]
            best_score = player_score
            best_hand = [availableCards]
        elif player_score == best_score:
            best_player.append(player)
            best_hand.append(availableCards)
        
    return [best_player, best_score, best_hand]  
    
def handDealtTest(games):
    pocketPair = 0
    pocketFaces = 0
    pocketSuitedFaces = 0
    
    handOccurrences = [0 for _ in range(10)]
    
    print('Gathering statistics on {} games...'.format(games))
    
    start = time()
    for i in range(games):
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
            
        if sameOrHigherCount(Card('J', ''), myHand) == 2 and countSameSuit(myHand[0], myHand) == 2:
            pocketSuitedFaces += 1
        
        if hasRoyalStraightFlush(availableCards):
            handOccurrences[9] += 1
        elif hasStraightFlush(availableCards):
            handOccurrences[8] += 1
        elif hasFourOfAKind(availableCards):
            handOccurrences[7] += 1
        elif hasFullHouse(availableCards):
            handOccurrences[6] += 1
        elif hasFlush(availableCards):
            handOccurrences[5] += 1
        elif hasStraight(availableCards):
            handOccurrences[4] += 1
        elif hasThreeOfAKind(availableCards):
            handOccurrences[3] += 1
        elif hasTwoPairs(availableCards):
            handOccurrences[2] += 1
        elif hasPair(availableCards):
            handOccurrences[1] += 1
        else:
            handOccurrences[0] += 1
            
        print('\n'.join('{:7d} | {:4.1f} % | {}'.format(score, 100*score/games, '#'*int(score/(games/100))) for score in handOccurrences))
        print('{:7d} | {:4.1f} %'.format(i, 100*i/games))
        print()
    
    print("Took {:.1f} seconds".format(time()-start))
    print("\n---- Results ----")
    print('\n'.join('{} {:7d} | {}'.format(HAND_DESCRIPTION[i], handOccurrences[i], getProbability(handOccurrences[i], games)) for i in range(10)))
    print("--- TOTAL --- {:10d} | {}\n".format(games, getProbability(sum(handOccurrences), games)))
    print("---- Pocket ----")
    print("Pairs:                    | " + getProbability(pocketPair, games))
    print("Faces:                    | " + getProbability(pocketFaces, games))
    print("Suited faces:             | " + getProbability(pocketSuitedFaces, games))
    
def handPlayedTest(games):
    start = time()
    players = ['Fred', 'Flavio', 'Marcelo', 'Amauri', 'Apse', 'Henrique']
    winning_hands = [0 for _ in range(10)]
    scores = []
    for i in range(games):
        winner = playHand(players)
        winning_hands[winner[1]>>5*4] += 1
        scores.append(winner[1])
        print('\n'.join('{:7d} | {:5.1f} % | {}'.format(score, 100*score/games, '#'*int(score/(games/150))) for score in winning_hands))
        print('{:7d} | {:5.1f} %\n'.format(i, 100*i/games))
    print("Took {:.1f} seconds\n".format(time()-start))
    print('\n'.join('{} {:7d} | {}'.format(HAND_DESCRIPTION[i], winning_hands[i], getProbability(winning_hands[i], games)) for i in range(10)))
    print('--- TOTAL --- {:10d} | {}\n'.format(sum(winning_hands), getProbability(sum(winning_hands), games)))
    scores.sort(reverse=True)
    filename = '{}players.txt'.format(len(players))
    r = open(filename, 'a')
    for score in scores:
        r.write('0x' + format(score, '06x') + '\n')
    r.close()
    
if __name__ == '__main__':
    print('Starting...')
    handPlayedTest(888900)
#     handDealtTest(DEFAULT_MAX_GAME_COUNT)
    print('Done!')