'''
Created on 31 de mar de 2017

@author: fvj
'''

import random, time

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
# CARD_SUITS = ['D', 'S', 'H', 'C']

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
    random.shuffle(deck)
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
        if len(ordCards) > 0:
            value += (CARD_RANKS.index(ordCards[0].rank) << 3*4)
        if len(ordCards) > 1:
            value += (CARD_RANKS.index(ordCards[1].rank) << 2*4)
        return value
    
    elif hasTwoPairs(cards):
        ordCards = order(cards)
        value = (CARD_RANKS.index(getPairs(cards)[0].rank) << 4*4) + (CARD_RANKS.index(getPairs(cards)[2].rank) << 3*4)  
        for card in getPairs(cards)[:4]:
            ordCards.remove(card)
        if len(ordCards) > 0:
            value += (CARD_RANKS.index(ordCards[0].rank) << 2*4)
        return value
    
    elif hasPair(cards):
        ordCards = order(cards)
        value = CARD_RANKS.index(getPairs(cards)[0].rank) << 4*4 
        for card in getPairs(cards):
            ordCards.remove(card)
        if len(ordCards) > 0:
            value += (CARD_RANKS.index(ordCards[0].rank) << 3*4)
        if len(ordCards) > 1:
            value += (CARD_RANKS.index(ordCards[1].rank) << 2*4)
        if len(ordCards) > 2:
            value += (CARD_RANKS.index(ordCards[2].rank) << 1*4)
        if len(ordCards) > 3:
            value += CARD_RANKS.index(ordCards[3].rank)
        return value
    
    else:
        ordCards = order(cards)
        value = (CARD_RANKS.index(ordCards[0].rank) << 4*4)
        if len(ordCards) > 1:
            value += (CARD_RANKS.index(ordCards[1].rank) << 3*4)
        if len(ordCards) > 2:
            value += (CARD_RANKS.index(ordCards[2].rank) << 2*4)
        if len(ordCards) > 3:
            value += (CARD_RANKS.index(ordCards[3].rank) << 1*4)
        if len(ordCards) > 4:
            value += CARD_RANKS.index(ordCards[4].rank) 
        return value

def getHandScore(cards):
    return getHandCode(cards) + getKickersValue(cards)

def dealHand(players):
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
        player_score = getHandScore(availableCards)
        
#         print(str(player) + ': 0x' + str(format(player_score, '06x')) + ' ' + str(order(hand)))
         
        if player_score > best_score:
            best_player = [player]
            best_score = player_score
            best_hand = [availableCards]
        elif player_score == best_score:
            best_player.append(player)
            best_hand.append(availableCards)
        
    return [best_player, best_score, best_hand]  
    
def handDealtStats(games):
    pocketPair = 0
    pocketFaces = 0
    pocketSuitedFaces = 0
    
    handOccurrences = [0 for _ in range(10)]
    
    print('Gathering statistics on {} games...'.format(games))
    
    start = time.time()
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
    
    print("Took {:.1f} seconds".format(time.time()-start))
    print("\n---- Results ----")
    print('\n'.join('{} {:7d} | {}'.format(HAND_DESCRIPTION[i], handOccurrences[i], getProbability(handOccurrences[i], games)) for i in range(10)))
    print("--- TOTAL --- {:10d} | {}\n".format(games, getProbability(sum(handOccurrences), games)))
    print("---- Pocket ----")
    print("Pairs:                    | " + getProbability(pocketPair, games))
    print("Faces:                    | " + getProbability(pocketFaces, games))
    print("Suited faces:             | " + getProbability(pocketSuitedFaces, games))
    
def winningHandStats(games):
    start = time.time()
    players = ['Fred', 'Flavio', 'Marcelo', 'Amauri', 'Apse', 'Henrique']
    winning_hands = [0 for _ in range(10)]
    scores = []
    for i in range(games):
        winner = dealHand(players)
        winning_hands[winner[1]>>5*4] += 1
        scores.append(winner[1])
        print('\n'.join('{:7d} | {:5.1f} % | {}'.format(score, 100*score/games, '#'*int(score/(games/150))) for score in winning_hands))
        print('{:7d} | {:5.1f} %\n'.format(i, 100*i/games))
    print("Took {:.1f} seconds\n".format(time.time()-start))
    print('\n'.join('{} {:7d} | {}'.format(HAND_DESCRIPTION[i], winning_hands[i], getProbability(winning_hands[i], games)) for i in range(10)))
    print('--- TOTAL --- {:10d} | {}\n'.format(sum(winning_hands), getProbability(sum(winning_hands), games)))
#     scores.sort(reverse=True)
    scores.sort()
    filename = '{}players.txt'.format(len(players))
    r = open(filename, 'a')
    for score in scores:
        r.write('0x' + format(score, '06x') + '\n')
    r.close()
    
def get6PlayersHandPercentage(score):
    statsFile = open('6players.txt', 'r')
    totalLines = 0
    equalLine = 0
    done = False
    
    for line in statsFile.readlines():
        totalLines += 1
        if not done and int(line, 16) >= score:
            equalLine = totalLines
            done = True
            
    statsFile.close() 
    return equalLine/totalLines
    
def getAIdecision(myself, myHand, allPlayers, foldPlayers, cash, pot, tableCards): # TODO: better decisions
    activePlayers = [player for player in allPlayers if player not in foldPlayers]
    
    if not len(activePlayers) > 1:
        return 0
    
    myScore = getHandScore(myHand+tableCards)
#     print('{}: {:.2f} %'.format(myself, 100*get6PlayersHandPercentage(myScore)))

    raiseFactor = 1 + random.random() 
    
    if myScore >= 0x627000: # ~90%
        return cash[myself]+pot[myself]
    elif myScore >= 0x2a1b00: # ~30%
        if random.random() > 0.8:
            return 10*int((raiseFactor*pot[myself])/10)
    
    if random.random() < 0.05: # bluff
        return 10*int((raiseFactor*pot[myself])/10)
    
    if getHighCard(myHand) < Card('8', ''):
        return -1
    
    return 0
    
def bidRound(activePlayers, humanPlayers, cash, pot, hands, tableCards):
    foldPlayers = []
    
    for player in activePlayers:
        if player in foldPlayers:
            continue
        
        if player in humanPlayers:
            print(str(player) + ' playing.')
            print('Your hand: {} ({})'.format(order(hands[player]), getHandDescription(getHandScore(tableCards+hands[player]))))
            print('You currently have {:.0f} invested on a {:.0f} pot.'.format(pot[player], sum(list(pot.values()))))
            print('You still have {:.0f} available of a total of {:.0f}.'.format(cash[player], cash[player]+pot[player] ))
            print('Would you like to fold [-1], check [0] (default), or raise to amount n [n]?')
            try:
                command = int(input())
            except:
                command = 0
        else:
            command = getAIdecision(player, hands[player], activePlayers, foldPlayers, cash, pot, tableCards)

        if command > 0 and command < max(list(pot.values())):
            command = 0
                                
        if command == 0: # check
            bid = max(list(pot.values()))
            raise_bid = bid-pot[player]
            if raise_bid > 0:
                print(player + ' covers pot.')
            else:
                print(player + ' checks.')
            if cash[player] > raise_bid:
                cash[player] -= raise_bid
                pot[player] += raise_bid
            else:
                pot[player] += cash[player]
                cash[player] = 0
        elif command < 0: # fold
            print(player + ' folds.')
            foldPlayers.append(player)
        else: # raise
            command = min(command, cash[player]+pot[player])
            print('{} raises to {:.0f}!'.format(player, command))
            raise_bid = command-pot[player]
            cash[player] -= raise_bid
            pot[player] += raise_bid
        
        if cash[player] == 0:
            print(player + ' is ALL IN!')
    
    currentBid = max(list(pot.values()))
    remainingPlayers = [player for player in activePlayers if pot[player] < currentBid and player not in foldPlayers and cash[player] > 0]
    for player in remainingPlayers:
        if player in humanPlayers:
            print('Would you like to cover raise to {:.0f}?'.format(currentBid))
            print('No [-1], Yes [0] (default)?')
            try:
                command = int(input())
            except:
                command = 0
        else:
            command = getAIdecision(player, hands[player], activePlayers, foldPlayers, cash, pot, tableCards)
    
        if command < 0: # fold
            print(player + ' folds.')
            foldPlayers.append(player)
        elif cash[player] > 0:
            print(player + ' covers raise.')
            bid = max(list(pot.values()))
            raise_bid = bid-pot[player]
            if cash[player] > raise_bid:
                cash[player] -= raise_bid
                pot[player] += raise_bid
            else:
                pot[player] += cash[player]
                cash[player] = 0
        
        if cash[player] == 0:
            print(player + ' is ALL IN!')
                            
    for out in foldPlayers:
        activePlayers.remove(out)
    
def playHand(players, humanPlayers, cash, bigBlind, smallBlind):
    pot = {player:0 for player in players}
    activePlayers = [player for player in players if cash[player] > 0]
    
    for player in activePlayers:
        if activePlayers.index(player) == 0:
            cash[player] -= smallBlind
            pot[player] += smallBlind 
        if activePlayers.index(player) == 1:
            cash[player] -= bigBlind
            pot[player] += bigBlind
            
    deck = getRandomDeck()
    hands = {}
        
    for player in activePlayers:
        hands[player] = [deck.pop(), deck.pop()]
        
    deck.pop() # burn
    flop = [deck.pop(), deck.pop(), deck.pop()]
    deck.pop() # burn
    turn = [deck.pop()]
    deck.pop() # burn
    river = [deck.pop()]
    
    tableCards = []
    bidRound(activePlayers, humanPlayers, cash, pot, hands, tableCards)
    
    if len(activePlayers) > 1:
        tableCards = flop
        print('\nFlop:  ' + str(tableCards))
        bidRound(activePlayers, humanPlayers, cash, pot, hands, tableCards)
    
    if len(activePlayers) > 1:
        tableCards = flop+turn
        print('\nTurn:  ' + str(tableCards))
        bidRound(activePlayers, humanPlayers, cash, pot, hands, tableCards)
    
    if len(activePlayers) > 1:
        tableCards = flop+turn+river
        print('\nRiver: ' + str(tableCards))
        bidRound(activePlayers, humanPlayers, cash, pot, hands, tableCards)
    
    if not len(activePlayers) > 1:
        print('\n\t{} has won!'.format(activePlayers[0]))
        best_players = activePlayers
        share = sum(list(pot.values()))
    else: # SHOWDOWN
        print('Table Cards: {}\nHands:'.format(str(flop+turn+river)))
        best_score = 0
        for player in activePlayers:
            score = getHandScore(flop+turn+river+hands[player])
            print('- {:20s}: {} ({})'.format(player[:20], order(hands[player]), getHandDescription(score)))
            if score > best_score:
                best_players = [player]
                best_score = score
            elif score == best_score:
                best_players.append(player)
                
        if len(best_players) == 1:
            print('\n\t{} has won with {}!'.format(best_players[0], getHandDescription(best_score)))
            share = sum(list(pot.values()))
        else:
            print('\n\tDraw with {}! Winning players: {}'.format(getHandDescription(best_score), ', '.join(best_players)))
            share = sum(list(pot.values()))/len(best_players)
            
    for winner in best_players:
        cash[winner] += share
    
def playGame(players, humanPlayers, initialCash=1000, bigBlind=100, smallBlind=50):
    cash = {player:initialCash for player in players}
    while(len(players) > 1):
        print('\nPots:')
        for player in players:
            print('{:20s}: {:5.0f}'.format(player[:20], cash[player]))
        print()
        playHand(players, humanPlayers, cash, bigBlind, smallBlind)
        print('\n'.join('{} has dropped out!'.format(player) for player in players if cash[player] <= 0))
        players.append(players.pop(0))
        players = [player for player in players if cash[player] > 0]
        time.sleep(2)
    print('Game has ended! {} has won!'.format(players[0]))
    
if __name__ == '__main__':
    print('Starting...')
    players = ['Amaurixa', 'Flavio do Posto', 'Fredelicia', 'Marcelonha', 'Henriqueta']
    random.shuffle(players)
    playGame(players, ['Fredelicia'])
    print('Done!')