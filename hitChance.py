


deck = {}
for i in range(1, 10):
    deck[i] = 4

deck[10] = 16

def handSum(hand):
    #TODO sort better, maybe
    hand.sort(reverse = True)
    valSum = 0
    for card in hand:
        if card != 1:
            valSum += card
        else:
            if valSum + 11 > 21:
                valSum += 1
            else:
                valSum += 11
    
    return valSum

def stand(userHand, dealerHand, deck):
    return dealerScore(userHand, dealerHand, deck)

def hitHelper(userHand, dealerHand, deck, memoVal=None, numHits=1):
    if memoVal is None:
        memoVal = {}

    userVal = handSum(userHand)
    dealerVal = handSum(dealerHand)

    key = (userVal, dealerVal, numHits)
    if key in memoVal:
        return memoVal[key]
    
    if userVal > 21:
        ev = -1
        memoVal[key] = ev
        return ev 
    
    if userVal == 21 or numHits == 0:
        ev = stand(userHand, dealerHand, deck)
        memoVal[key] = ev
        return ev
    
    ev = 0
    totalCards = sum(deck[card] for card in deck)

    if totalCards == 0:
        print("No cards")
        totalCards = 1
    for card in deck:
        if deck[card]:            
            userHandNew = userHand.copy()
            userHandNew.append(card)

            weight = deck[card] / totalCards
            ev += hitHelper(userHandNew, dealerHand, deck, memoVal, numHits - 1) * weight
    
    memoVal[key] = ev
    return ev

def hit(userHand, dealerHand, deck, memoVal={}):

    userVal = handSum(userHand)
    evList = []

    hitHeuristic = 1
    if userVal < 9:
        hitHeuristic = 5
    elif userVal < 11:
        hitHeuristic = 3
    elif userVal < 16:
        hitHeuristic = 2
    
    for numHits in range(1, hitHeuristic + 1):
        evList.append(hitHelper(userHand, dealerHand, deck, memoVal, numHits))

    return max(evList)


def doubleDown(userHand, dealerHand, deck):
    return 2 * hitHelper(userHand, dealerHand, deck)

def dealerScore(userHand, dealerHand, deck):
    dealerVal = handSum(dealerHand)

    ev = 0
    totalCards = sum(deck[card] for card in deck)
    if totalCards == 0:
        print("No cards")
        totalCards = 1
    
    if dealerVal < 17:
        for card in deck:
            if deck[card]:            
                dealerHandNew = dealerHand.copy()
                dealerHandNew.append(card)

                weight = deck[card] / totalCards
                ev += dealerScore(userHand, dealerHandNew, deck) * weight

        return ev
            
    userVal = handSum(userHand)

    if userVal > 21:
        return -1
    if dealerVal > 21:
        return 1
    if userVal > dealerVal:
        return 1
    if userVal < dealerVal:
        return -1
    else:
        return 0


userHand = [2, 3]
dealerHand = [10]
print(hit(userHand, dealerHand, deck))
print(stand(userHand, dealerHand, deck))