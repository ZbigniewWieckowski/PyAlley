import random

class Strategy:
    def __init__(self,name):
        self.name = name
        

class Player:
    def __init__(self,name,nationality,playerType='',strategy=''):
        print('Starting player initialization ...')
        # Initialize player
        self.name = name
        self.nationality = nationality
        self.playerType = playerType
        self.strategy = strategy
        print('Finished player initialization ...')
    def getName(self):
        return self.name
    def setName(self,name):
        self.name = name
    def getNationality(self):
        return self.nationality
    def setNationality(self,nationality):
        self.nationality = nationality
    def getPlayerType(self):
        return self.playerType
    def setPlayerType(self,type):
        self.playerType = playerType
    def __str__(self):
        return '{0} is a {1} {2}'.format(self.name, self.nationality, self.playerType)
    def move(self,board):
        # TBD - implement player move
        print('Player:move() - TBD')
    def printResources(self, board, revealAll=0):
        print('')
        pRes = board.getPlayersResources(self)
        print('            ', end='')
        for nat in board.getAllAvailableNationalities():
            print(' ' + nat[0], end='')
        print('')
        
        resType = 'Password'
        print(resType + '   :', end='')
        for nat in board.getAllAvailableNationalities():
            print(' ' + str(pRes[nat][resType]), end='')
        print('')

        resType = 'Disguise'
        print(resType + '   :', end='')
        for nat in board.getAllAvailableNationalities():
            print(' ' + str(pRes[nat][resType]), end='')
        print('')

        resType = 'CodeBook'
        print(resType + '   :', end='')
        for nat in board.getAllAvailableNationalities():
            print(' ' + str(pRes[nat][resType]), end='')
        print('')

        resType = 'Key'
        print(resType + '        :', end='')
        for nat in board.getAllAvailableNationalities():
            print(' ' + str(pRes[nat][resType]), end='')
        print('')

        print('')
        print('Move Cards : ' + str(len(board.getPlayersMoveCards(self))) + (' ' + str(board.getPlayersMoveCards(self)) if 1 == revealAll else ''))
        print('Money      : $' + str(board.getPlayersMoney(self)))
        print('Wild Cards : ' + str(board.getPlayersWildCards(self)))
        print('')
    def hasAllResourcesOfType(self,board,resType):
        pRes = board.getPlayersResources(self)
        hasAll = 1
        for nat in board.getAllAvailableNationalities():
            if 0 == pRes[nat][resType]:
                hasAll = 0
                break
        return hasAll
    def checkWinningCriteria(self,board):
        numberOfWildcards = board.getPlayersWildCards(self)
        pRes = board.getPlayersResources(self)
        numberOfNatResources = 0
        for resType in board.getPlayersResourceTypes():
            numberOfNatResources = numberOfNatResources + pRes[self.nationality][resType]
            if numberOfNatResources + numberOfWildcards >= 4:
                board.recordExitThroughEmbassy(self)
                print('Player ' + self.name + ' collected all item and exited through embassy !!!')


class ComputerPlayer(Player):
    def __init__(self,name,nationality,playerType='Computer'):
        print('Starting computer player initialization ...')
        # Initialize computer player        
        self.name = name
        self.nationality = nationality
        self.playerType = playerType
        print('Finished computer player initialization ...')
    def move(self,board,printResources='yes'):
        print('')
        print('Starting move of ' + self.name)
        # Challenge phase
        if (random.random() > 0.9):
            # Only challenge part of the time
            print('Challenge random player for random nationality ...')
            plist = board.getActivePlayers()
            foundPlayer = 0
            while (foundPlayer == 0):
                p = plist[round(random.random()*len(plist)+0.5)-1]
                if (p != self):
                    foundPlayer = 1
            nlist = list(board.getAllAvailableNationalities())
            nlist.remove(self.getNationality())
            n = nlist[round(random.random()*len(nlist)+0.5)-1]
            print('')
            print('!!! Challenging player ' + p.getName())
            if (p.getPlayerType() == 'Human'):
                input('Summon human player ' + p.getName() + ', press [Enter] when ready ...')
                print('')
                print('Guessing s/he is a ' + n)
                input(p.getName() + ' - Please confirm by pressing [Enter] ...')
                for i in range(1,100):
                    print('')
            print('')
            if (n == p.getNationality()):
                print('Challenge successful - player ' + p.getName() + ' is out!')
                board.deactivatePlayer(p)
                board.transferResources(p,self)
                # Switch nationality 50% of the time
                if random.random() > 0.5:
                    board.switchNationalities(p,self)
            else:
                print('Challenge was not successful, current player is out!')
                board.deactivatePlayer(self)
                board.transferResources(self,p)
                if 'Human' == p.getPlayerType():
                    completedSwitch = 0
                    while 0 == completedSwitch:
                        switchAnswer = input('Question for ' + p.getName() + ' - do you want to switch nationalities with ' + self.getName() + ' and become ' + self.getNationality() + '? (y/n): ')
                        if 'y' == switchAnswer or 'Y' == switchAnswer:
                            print('Switched nationality to ' + self.getNationality())
                            board.switchNationalities(p, self)
                            input('Acknowledge switching to new nationality. Press [Enter]')
                            for i in range(1,100):
                                print('')
                            completedSwitch = 1
                        elif 'n' == switchAnswer or 'N' == switchAnswer:
                            completedSwitch = 1
                        else:
                            print('Unrecognized answer, please try again ...')
                else:
                    # Switch nationalities 50% of the time
                    if random.random() > 0.5:
                        board.switchNationalities(p, self)
        else:
            print('Did not challenge')
        # Advance phase
        if board.isPlayerActive(self) and len(board.getActivePlayers()) > 1:
            moveCards = board.getPlayersMoveCards(self)
            isMoveCardUsed = 0
            moveCardCount = len(moveCards)
            if moveCardCount > 0:
                # Use move card 20% of the time, if available
                if random.random() > 0.8:
                    pick = round(random.random() * moveCardCount - 0.5)
                    moveCardValue = moveCards[pick]
                    isMoveCardUsed = 1
            if 0 == isMoveCardUsed:
                diceRoll = round(random.random()*6+0.5)
                print('Bot advance phase - rolled ' + str(diceRoll))
            else:
                diceRoll = moveCardValue
                board.discardMoveCard(self, moveCardValue)
                print('Bot advance phase - used move card of value ' + str(moveCardValue))
            pos = board.getPlayersPosition(self)
            for i in range(1, diceRoll+1):
                if i == 1 and pos == 'SpyAlleyEntrance':
                    pos = 'Collect$20'
                else:
                    nextPos = board.nextSpace(pos)
                    if (len(nextPos) == 1):
                        pos = nextPos[0]
                    else:
                        # Pick each path 50% of the time
                        if (random.random() > 0.5):
                            pos = nextPos[0]
                        else:
                            pos = nextPos[1]
                        print('Decided to enter ' + pos)
                    if pos == 'Start':
                        board.passingStart(self)
            board.setPlayersPosition(self, pos)
            print('Ended up on ' + pos)
            # Check for winning criteria
            if pos == self.nationality + 'Embassy':
                self.checkWinningCriteria(board)
            # Action for current position
            if len(board.getActivePlayers()) > 1:                   
                # Handle landing on password space
                if pos in board.getAllAvailableNationalities():
                    if 0 == board.getPlayersResources(self)[pos]['Password']:
                        # Buy password 90% of time, if funds are available
                        if (random.random() > 0.1):
                            if board.getPlayersMoney(self) > 0:
                                board.assignPassword(self, pos)
                        else:
                            print('Did not buy password')
                # Handle landing on move card space
                if pos[0:8] == 'MoveCard':
                    board.assignMoveCard(self)
                # Handle landing on resource space
                if 'Disguises' == pos or 'CodeBooks' == pos or 'Keys' == pos:
                    resType = pos[0:len(pos)-1]
                    if 0 == self.hasAllResourcesOfType(board,resType):
                        # Spend 50% of funds on resources
                        availableFunds = board.getPlayersMoney(self)
                        amountToSpend = round(availableFunds/2)
                        amountPerResource = board.getAmountPerResourceType(resType)
                        unfilledNationalities = []
                        for nat in board.getAllAvailableNationalities():
                            if 0 == board.getPlayersResources(self)[nat][resType]:
                                unfilledNationalities.append(nat)
                        while len(unfilledNationalities) > 0 and amountToSpend >= amountPerResource:
                            pick = round(random.random() * len(unfilledNationalities) - 0.5)
                            pickedNationality = unfilledNationalities[pick]
                            board.assignResource(self, pickedNationality, resType)
                            unfilledNationalities.remove(pickedNationality)
                            amountToSpend = amountToSpend - amountPerResource
                # Handle landing on collect $10 space
                if 'Collect$10' == pos:
                    board.updateFunds(self,10)
                # Handle landing on collect $20 space
                if 'Collect$20' == pos:
                    board.updateFunds(self,20)
                # Handle landing on border crossing space
                if 'BorderCrossing' == pos:
                    if board.getPlayersMoney(self) < 5:
                        print('Not enough funds for crossing the border - landing on Spy Alley Entrance instead.')
                        board.setPlayersPosition(self, 'SpyAlleyEntrance')
                    else:
                        print('Collecting $5 for border crossing')
                        board.updateFunds(self,-5)
                # Handle landing on move back 2 spaces space
                if 'MoveBack2Spaces' == pos:
                    print('Moving back 2 spaces to Spy Alley Entrance')
                    board.setPlayersPosition(self, 'SpyAlleyEntrance')
                # Handle landing on black market space
                if pos[0:11] == 'BlackMarket':
                    # Buy resource at random
                    pRes = board.getPlayersResources(self)
                    availableFunds = board.getPlayersMoney(self)
                    notBoughtYet = []
                    for resType in board.getPlayersResourceTypes():
                        if availableFunds >= board.getAmountPerResourceType(resType):
                            for nat in board.getAllAvailableNationalities():
                                if 0 == pRes[nat][resType]:
                                    notBoughtYet.append([nat, resType])
                    # Randomly select nat /resType combination
                    pick = round(random.random()*len(notBoughtYet)-0.5)
                    pickNat = notBoughtYet[pick][0]
                    pickResType = notBoughtYet[pick][1]
                    board.assignResource(self, pickNat, pickResType)
                    print('Bought ' + pickNat + ' ' + pickResType)
                # Handle landing on spy eliminator space
                if 'SpyEliminator' == pos:
                    # challenge all active players in Spy Alley spaces
                    for p in board.getActivePlayers():
                        if p != self and board.isSpaceInSpyAlley(board.getPlayersPosition(p)):                            
                            nlist = list(board.getAllAvailableNationalities())
                            nlist.remove(self.getNationality())
                            n = nlist[round(random.random()*len(nlist)-0.5)]
                            print('')
                            print('!!! Challenging player ' + p.getName())
                            if (p.getPlayerType() == 'Human'):
                                input('Summon human player ' + p.getName() + ', press [Enter] when ready ...')
                                print('')
                                print('Guessing s/he is a ' + n)
                                input(p.getName() + ' - Please confirm by pressing [Enter] ...')
                                for i in range(1,100):
                                    print('')
                                print('')
                            if (n == p.getNationality()):
                                print('Challenge successful - player ' + p.getName() + ' is out!')
                                board.deactivatePlayer(p)
                                board.transferResources(p,self)
                                # Switch nationality 50% of the time
                                if random.random() > 0.5:
                                    board.switchNationalities(p,self)
                            else:
                                print('Challenge was not successful')
                # Handle landing on free gift space
                if 'FreeGift' == pos[0:8]:
                    gc = board.getRandomGiftCard()
                    if 'WildCard' == gc[0]:
                        board.assignWildCard(self,'no')
                    else:
                        if 0 == board.getPlayersResources(self)[gc[0]][gc[1]]:
                            board.assignResource(self,gc[0],gc[1],'no')
                        else:
                            print('Already had ' + gc[0] + ' ' + gc[1])
                    board.discardGiftCard(gc)
                # Handle landing on confiscate materials space
                if 'ConfiscateMaterials' == pos:
                    availableFunds = board.getPlayersMoney(self)
                    if board.hasAllResources(self):
                        # Check for wild cards
                        playersWithWildCards = []
                        for p in board.getActivePlayers():
                            if board.getPlayersWildCards(p) > 0:
                               playersWithWildCards.append(p)
                        if len(playersWithWildCards) > 0:
                            amountPerResource = board.getConfiscateMaterialsPrices('WildCard')
                            if availableFunds >= amountPerResource:
                                pick = round(random.random()*len(playersWithWildCards)-0.5)
                                if board.getPlayersWildCards(playersWithWildCards[pick]) > 0:
                                    board.confiscateWildCard(playersWithWildCards[pick])
                                    board.updateFunds(self, -amountPerResource)
                                    board.assignWildCard(self,'no')
                                    print('Confiscated Wild Card from ' + playersWithWildCards[pick].getName())
                    else:
                        # Pick at random
                        activePlayers = board.getActivePlayers()
                        resourceTypes = []
                        for rt in board.getPlayersResourceTypes():
                            resourceTypes.append(rt)
                        resourceTypes.append('WildCard')
                        nationalities = board.getAllAvailableNationalities()
                        transferDone = 0
                        while 0 == transferDone:
                            playerPick = round(random.random()*len(activePlayers)-0.5)
                            p = activePlayers[playerPick]
                            resourcePick = round(random.random()*len(resourceTypes)-0.5)
                            resType = resourceTypes[resourcePick]
                            amountPerResource = board.getConfiscateMaterialsPrices(resType)
                            if availableFunds >= amountPerResource:
                                if 'WildCard' == resType:
                                    if board.getPlayersWildCards(p) > 0:
                                        board.confiscateWildCard(p)
                                        board.updateFunds(self, -amountPerResource)
                                        board.assignWildCard(self,'no')
                                        transferDone = 1
                                        print('Confiscated Wild Card from ' + p.getName())
                                else:
                                    nationalityPick = round(random.random()*len(nationalities)-0.5)
                                    nat = nationalities[nationalityPick]
                                    if 0 == board.getPlayersResources(self)[nat][resType]:
                                        if 1 == board.getPlayersResources(p)[nat][resType]:
                                            board.confiscateMaterial(p, nat, resType)
                                            board.updateFunds(self, -amountPerResource)
                                            board.assignResource(self, nat, resType, 'no')
                                            transferDone = 1
                                            print('Confiscated ' + nat + ' ' + resType + ' from ' + p.getName())
                # Handle landing on take another turn space
                if 'TakeAnotherTurn' == pos:
                    print('Taking another turn...')
                    self.move(board,'no')
                if printResources == 'yes':
                    self.printResources(board)
                    print('Finished move of ' + self.name)


class DummyComputerPlayer(ComputerPlayer):
    def __init__(self):
        setName('Dummy')


class JoshBot(ComputerPlayer):
    def __init__(self):
        setName('JoshBot')


class DadBot(ComputerPlayer):
    def __init__(self):
        setName('DadBot')


class HumanPlayer(Player):
    def __init__(self,name,nationality,playerType='Human'):
        print('Starting computer player initialization ...')
        # Initialize computer player        
        self.name = name
        self.nationality = nationality
        self.playerType = playerType
        print('Finished computer player initialization ...')
    def move(self,board,printResources='yes'):
        print('')
        print('Starting move of ' + self.name)
        # Challenge phase
        challengeInProgress = 1
        while (challengeInProgress == 1):
            isChallenge = input('Challenge phase - do you want to challenge? (y/n)?')
            if isChallenge == 'n' or isChallenge == 'N':
                challengeInProgress = 0
                print('Skipped the challenge phase')
            elif isChallenge == 'y' or isChallenge == 'Y':
                foundPlayer = 0
                challengedName = input('Name player to be challenged: ')
                for p in board.getActivePlayers():
                    if (challengedName == p.getName()):
                        if (p == self):
                            print('Sorry, you cannot challenge yourself')
                        else:
                            foundPlayer = 1
                            playerToBeChallenged = p
                            break
                if (foundPlayer == 0):
                    print('Name is not one of the active players'' names ...')
                else:
                    challengedNationality = input('What are you guessing the players nationality is? : ')
                    foundNationality = 0
                    for n in board.getAllAvailableNationalities():
                        if (challengedNationality == n):
                            foundNationality = 1
                    challengeInProgress = 0
                    if (foundNationality == 0):
                        print('Not one of the nationalities in the game: ')
                    else:
                        print('')
                        print('!!! Challenging player ' + playerToBeChallenged.getName() + ', guessing s/he is a ' + challengedNationality)
                        print('')
                        if (challengedNationality == playerToBeChallenged.getNationality()):
                            print('Challenge successful - player ' + playerToBeChallenged.getName() + ' is out!')
                            board.deactivatePlayer(playerToBeChallenged)
                            board.transferResources(playerToBeChallenged,self)
                            completedSwitch = 0
                            while 0 == completedSwitch:
                                switchAnswer = input('Do you want to switch nationalities with ' + challengedOpponent.getName() + ' and become ' + challengedNationality + '? (y/n): ')
                                if 'y' == switchAnswer or 'Y' == switchAnswer:
                                    board.switchNationalities(playerToBeChallenged, self)
                                    completedSwitch = 1
                                elif 'n' == switchAnswer or 'N' == switchAnswer:
                                    completedSwitch = 1
                                else:
                                    print('Unrecognized answer, please try again ...')
                        else:
                            print('Challenge was not successful, current player is out!')
                            board.deactivatePlayer(self)
                            board.transferResources(self, playerToBeChallenged)
                            if 'Human' == playerToBeChallenged.getPlayerType():
                                completedSwitch = 0
                                while 0 == completedSwitch:
                                    switchAnswer = input('Question for ' + playerToBeChallenged.getName() + ' - do you want to switch nationalities with ' + challengedOpponent.getName() + ' and become ' + challengedNationality + '? (y/n): ')
                                    if 'y' == switchAnswer or 'Y' == switchAnswer:
                                        board.switchNationalities(playerToBeChallenged, self)
                                        print('Switched nationality to ' + self.getNationality())
                                        input('Acknowledge switching to new nationality. Press [Enter]')
                                        for i in range(1,100):
                                            print('')
                                        completedSwitch = 1
                                    elif 'n' == switchAnswer or 'N' == switchAnswer:
                                        completedSwitch = 1
                                    else:
                                        print('Unrecognized answer, please try again ...')
                            else:
                                # Switch nationalities 50% of the time
                                if random.random() > 0.5:
                                    board.switchNationalities(playerToBeChallenged, self)
            else:
                print('Unrecognized answer - please try again ...')
        # Advance stage
        if board.isPlayerActive(self) and len(board.getActivePlayers()) > 1:
            moveCards = board.getPlayersMoveCards(self)
            isMoveCardUsed = 0
            moveCardCount = len(moveCards)
            if moveCardCount > 0:
                print('You have the following move cards: ' + str(moveCards))
                gotUseMoveCardDecision = 0
                while 0 == gotUseMoveCardDecision:
                    useMoveCard = input('Your position is ' + board.getPlayersPosition(self) + '. Use move card? (y/n)')
                    if useMoveCard == 'Y' or useMoveCard == 'y':
                        isMoveCardUsed = 1
                        gotUseMoveCardDecision = 1
                    elif useMoveCard == 'N' or useMoveCard == 'n':
                        gotUseMoveCardDecision = 1
                    else:
                        print('Incorrect answer - please try again ...')
                if 1 == isMoveCardUsed:
                    allSame = 1
                    firstCard = moveCards[0]
                    for ix in range(1, moveCardCount):
                        if moveCards[ix] != firstCard:
                            allSame = 0
                            break
                    if 1 == allSame:
                        moveCardValue = moveCards[0]
                    else:
                        gotMoveCardValue = 0
                        while 0 == gotMoveCardValue:
                            moveCardValue = eval(input('Which move card to use?'))
                            foundValue = 0
                            for ix in range(0, moveCardCount):
                                if moveCards[ix] == moveCardValue:
                                    foundValue = 1
                                    break
                            if 1 == foundValue:
                                gotMoveCardValue = 1
            if 1 == isMoveCardUsed:
                diceRoll = moveCardValue
                board.discardMoveCard(self, moveCardValue)
                print('Used move card of value ' + str(moveCardValue))
            else:   
                diceRoll = round(random.random()*6+0.5)
                print('Human advance phase - rolled ' + str(diceRoll))
            posList = []
            posList.append(board.getPlayersPosition(self))
            for i in range(1, diceRoll+1):
                if i == 1 and posList[0] == 'SpyAlleyEntrance':
                    posList = ['Collect$20']
                else:
                    # print('posList = ' + str(posList))
                    nextPos = []
                    for pos in posList:
                        for next in board.nextSpace(pos):
                            nextPos.append(next)
                    posList = nextPos
                    if posList[0] == 'Start':
                        board.passingStart(self)
            # print('posList = ' + str(posList))
            if (len(posList) == 1):
                pos = posList[0]
            else:
                gotDecision = 0
                while (gotDecision == 0):
                    moveDecision = input('(1) move to ' + str(posList[0]) + ' or (2) move to ' + str(posList[1]) + ' ? : ')
                    if (moveDecision == '1' or moveDecision == '2'):
                          gotDecision = 1
                    else:
                          print('Invalid choice: ' + moveDecision + ', try again')
                pos = posList[eval(moveDecision)-1]
                print('Decided to move to ' + pos)
            board.setPlayersPosition(self, pos)
            print('Ended up on ' + pos)
            # Check for winning criteria
            if pos == self.nationality + 'Embassy':
                self.checkWinningCriteria(board)
            # Action for current position
            if len(board.getActivePlayers()) > 1:                   
                # Handle landing on password space
                if pos in board.getAllAvailableNationalities():
                    if 0 == board.getPlayersResources(self)[pos]['Password']:
                        self.buyingPassword(board,pos)
                # Handle landing on move card space
                if 'MoveCard' == pos[0:8]:
                    board.assignMoveCard(self)
                # Handle landing on resource space
                if 'Disguises' == pos or 'CodeBooks' == pos or 'Keys' == pos:
                    resType = pos[0:len(pos)-1]                
                    if 0 == self.hasAllResourcesOfType(board, resType):
                        amountPerResource = board.getAmountPerResourceType(resType)
                        if board.getPlayersMoney(self) < amountPerResource:
                            print('Not enough money to buy ' + resType + ' at this time.')
                        else:
                            self.buyingResource(board, resType)
                    else:
                        print('Already have all ' + resType + 's. Moving on')
                # Handle landing on collect $10 space
                if 'Collect$10' == pos:
                    board.updateFunds(self,10)
                # Handle landing on collect $20 space
                if 'Collect$20' == pos:
                    board.updateFunds(self,20)
                # Handle landing on border crossing space
                if 'BorderCrossing' == pos:
                    if board.getPlayersMoney(self) < 5:
                        print('Not enough funds for crossing the border - landing on Spy Alley Entrance instead.')
                        board.setPlayersPosition(self, 'SpyAlleyEntrance')
                    else:
                        print('Collecting $5 for border crossing')
                        board.updateFunds(self,-5)
                # Handle landing on move back 2 spaces space
                if 'MoveBack2Spaces' == pos:
                    print('Moving back 2 spaces to Spy Alley Entrance')
                    board.setPlayersPosition(self, 'SpyAlleyEntrance')
                # Handle landing on black market space
                if 'BlackMarket' == pos[0:11]:
                    # Buy resource at random\
                    self.buyResourceOnBlackMarket(board)
                # Handle landing on spy eliminator space
                if 'SpyEliminator' == pos:
                    for p in board.getActivePlayers():
                        if p != self and board.isSpaceInSpyAlley(board.getPlayersPosition(p)):                            
                            self.freeChallenge(board, p);
                # Handle landing on free gift space
                if 'FreeGift' == pos[0:8]:
                    gc = board.getRandomGiftCard()
                    if 'WildCard' == gc[0]:
                        board.assignWildCard(self,'no')
                    else:
                        if 0 == board.getPlayersResources(self)[gc[0]][gc[1]]:
                            board.assignResource(self,gc[0],gc[1],'no')
                        else:
                            print('Already had ' + gc[0] + ' ' + gc[1])
                    board.discardGiftCard(gc)
                # Handle landing on confiscate materials space
                if 'ConfiscateMaterials' == pos:
                    self.confiscateMaterials(board)
                # Handle landing on take another turn space
                if 'TakeAnotherTurn' == pos:
                    print('Taking another turn...')
                    self.move(board,'no')
                if printResources == 'yes':
                    self.printResources(board)
                    print('Finished move of ' + self.name)
    def buyingPassword(self,board,nat):               
        buyPasswordInProgress = 1
        while (buyPasswordInProgress == 1):
            buyPassword = input('Do you want to buy ' + nat + ' password? (y/n)?')
            if buyPassword == 'n' or buyPassword == 'N':
                buyPasswordInProgress = 0
                print('Skipped buying password')
            elif buyPassword == 'y' or buyPassword == 'Y':
                board.assignPassword(self, nat)
                buyPasswordInProgress = 0
            else:
                print('Unrecognized answer - please try again ...')
    def buyingResource(self,board,resType):
        pRes = board.getPlayersResources(self)
        amountPerResource = board.getAmountPerResourceType(resType)
        print('Available funds: $' + str(board.getPlayersMoney(self)))
        print('You have the following ' + resType + 's:')
        print('')
        print('            ', end='')
        for nat in board.getAllAvailableNationalities():
            print(' ' + nat[0], end='')
        print('')
        print(resType + ('        :' if 'Key' == resType else '   :'), end='')
        for nat in board.getAllAvailableNationalities():
            print(' ' + str(pRes[nat][resType]), end='')
        print('')
        buyResourceInProgress = 1
        another = ''
        while (buyResourceInProgress == 1):
            buyResource = input('Do you want to buy ' + another + resType + '? (y/n)?')
            if buyResource == 'n' or buyResource == 'N':
                buyResourceInProgress = 0
                print('Done buying ' + resType + 's')
            elif buyResource == 'y' or buyResource == 'Y':
                # Check if only one missing
                numberMissing = 0
                lastNatMissing = ''
                for nat in board.getAllAvailableNationalities():
                    if 0 == pRes[nat][resType]:
                        numberMissing += 1
                        lastNatMissing = nat
                        if numberMissing > 1:
                            break
                if 1 == numberMissing:
                    if board.getPlayersMoney(self) >= amountPerResource:
                        board.assignResource(self, lastNatMissing, resType)
                    else:
                        print('Not enough funds for buying another ' + resType)
                else:
                    gotResourceNationality = 0
                    while 0 == gotResourceNationality:
                        nat = input('Enter nationality for ' + resType + ' , first letters, or qQ:')
                        if 'q' == nat or 'Q' == nat:
                            buyResourceInProgress = 0
                            break
                        elif nat in board.getAllAvailableNationalities():
                            if 0 == pRes[nat][resType]:
                                board.assignResource(self, nat, resType)
                                gotResourceNationality = 1
                                another = 'another '
                            else:
                                print('You already have ' + nat + ' ' + resType)
                        else:
                            natList = []
                            error = 0
                            for n in list(nat.upper()):
                                if n in ['A', 'F', 'G', 'I', 'R', 'S']:
                                    n1 = board.lookupNationality(n)
                                    if not n1 in natList:
                                        natList.append(n1)
                                else:
                                    error = 1
                                    break
                            if 1 == error:
                                print('Incorrectly entered nationality. Try again:')
                            else:
                                if board.getPlayersMoney(self) >= len(natList) * amountPerResource:
                                    for n in natList:
                                        board.assignResource(self, n, resType)
                                    buyResourceInProgress = 0
                                    break
                                else:
                                    print('Not enough funds for buying + nat ' + resType)
                    if buyResourceInProgress and board.getPlayersMoney(self) < amountPerResource:
                        print('Not enough funds for buying another ' + resType)
                        buyResourceInProgress = 0
            else:
                print('Unrecognized answer - please try again ...')
    def buyResourceOnBlackMarket(self,board):
        pRes = board.getPlayersResources(self)
        availableFunds = board.getPlayersMoney(self)
        buyResourceInProgress = 1
        while (buyResourceInProgress == 1):
            buyResource = input('You have $' + str(availableFunds) + '. Do you want to buy resource on black market? (y/n)?')
            if buyResource == 'n' or buyResource == 'N':
                buyResourceInProgress = 0
                print('Done buying resource on black market')
            elif buyResource == 'y' or buyResource == 'Y':
                gotResourceType = 0
                while 0 == gotResourceType:
                    resTypeAnswer = input('Enter resource type (1) Password, (2) Disguise, (3) Code Book, (4) Key:')
                    resType = 'Password' if '1' == resTypeAnswer else ('Disguise' if '2' == resTypeAnswer else ('CodeBook' if '3' == resTypeAnswer else ('Key' if '4' == resTypeAnswer else 'Error')))
                    if 'Error' == resType:
                        print('Incorrect response, please retry')
                    else:
                       gotResourceType = 1
                amountPerResource = board.getAmountPerResourceType(resType)
                if 'WildCard' == resType:
                    if availableFunds >= amountPerResource:
                        board.assignWildCard(self)
                        break
                gotResourceNationality = 0
                while 0 == gotResourceNationality:
                    nat = input('Enter nationality , first letter, or qQ:')
                    if 'q' == nat or 'Q' == nat:
                        buyResourceInProgress = 0
                        break
                    elif nat in board.getAllAvailableNationalities():
                        if 0 == pRes[nat][resType]:
                            board.assignResource(self, nat, resType)
                            gotResourceNationality = 1
                            another = 'another '
                        else:
                            print('You already have ' + nat + ' ' + resType)
                    else:
                        error = 1 != len(nat)
                        if 0 == error:
                            natList = []
                            error = 0
                            for n in list(nat.upper()):
                                if n in ['A', 'F', 'G', 'I', 'R', 'S']:
                                    n1 = board.lookupNationality(n)
                                    if not n1 in natList:
                                        natList.append(n1)
                                else:
                                    error = 1
                                    break
                        if 1 == error:
                            print('Incorrectly entered nationality. Try again:')
                        else:
                            if availableFunds >= amountPerResource:
                                for n in natList:
                                    board.assignResource(self, n, resType)
                                buyResourceInProgress = 0
                                break
                            else:
                                print('Not enough funds for buying + nat ' + resType)
            else:
                print('Unrecognized answer - please try again ...')
    def freeChallenge(self,board,challengedOpponent):
        completedChallenge = 0
        while 0 == completedChallenge:
            print('Freely challenging ' + challengedOpponent.getName())
            challengedNationality = input('What are you guessing the players nationality is, or first letter? : ')
            foundNationality = 0
            if 1 == len(challengedNationality):
                challengedNationality = board.lookupNationality(challengedNationality)
            for n in board.getAllAvailableNationalities():
                if (challengedNationality == n):
                    foundNationality = 1
            if (foundNationality == 0):
                    print('Not one of the nationalities in the game: ')
            else:
                print('')
                print('!!! Challenging player ' + challengedOpponent.getName() + ', guessing s/he is a ' + challengedNationality)
                print('')
                if (challengedNationality == challengedOpponent.getNationality()):
                    print('Challenge successful - player ' + challengedOpponent.getName() + ' is out!')
                    board.deactivatePlayer(challengedOpponent)
                    board.transferResources(challengedOpponent, self)
                    completedSwitch = 0
                    while 0 == completedSwitch:
                        switchAnswer = input('Do you want to switch nationalities with ' + challengedOpponent.getName() + ' and become ' + challengedNationality + '? (y/n): ')
                        if 'y' == switchAnswer or 'Y' == switchAnswer:
                            board.switchNationalities(challengedOpponent, self)
                            completedSwitch = 1
                            print('Switched nationality to ' + self.getNationality())
                            input('Acknowledge switching to new nationality. Press [Enter]')
                            for i in range(1,100):
                                print('')
                        elif 'n' == switchAnswer or 'N' == switchAnswer:
                            completedSwitch = 1
                        else:
                            print('Unrecognized answer, please try again ...')
                else:
                    print('Challenge was not successful')
                completedChallenge = 1
    def confiscateMaterials(self,board):
        availableFunds = board.getPlayersMoney(self)
        transferDone = 0
        while 0 == transferDone:
            pickedPlayer = 0
            while 0 == pickedPlayer:
                confMatPlayer = input('Which player to confiscate materials from, or Qq?: ')
                if 'q' == confMatPlayer or 'Q' == confMatPlayer:
                    transferDone = 1
                    break
                else:
                    foundPlayer = 0
                    for p in board.getActivePlayers():
                        if p.getName() == confMatPlayer:
                            foundPlayer = 1
                            break
                    if 0 == foundPlayer:
                        print('Invalid player, try again ...')
                    else:
                        pickedPlayer = 1 
                        gotResourceType = 0
                        while 0 == gotResourceType:
                            resTypeAnswer = input('Enter resource type (1) Password, (2) Disguise, (3) Code Book, (4) Key, (5) WildCard :')
                            resType = 'Password' if '1' == resTypeAnswer else ('Disguise' if '2' == resTypeAnswer else ('CodeBook' if '3' == resTypeAnswer else ('Key' if '4' == resTypeAnswer else ('WildCard' if '5' == resType else 'Error'))))
                            if 'Error' == resType:
                                print('Incorrect response, please retry')
                            else:
                               gotResourceType = 1
                        amountPerResource = board.getConfiscateMaterialsPrices(resType)
                        if 'WildCard' == resType:
                            if availableFunds >= amountPerResource:
                                if board.getPlayersWildCards(p) > 0:
                                    board.confiscateWildCard(p)
                                    board.updateFunds(self, -amountPerResource)
                                    board.assignWildCard(self,'no')
                                    transferDone = 1
                                    print('Confiscated Wild Card from ' + p.getName())
                        else:
                            pickedNationality = 0
                            while 0 == pickedNationality:
                                nat = input('Pick nationality, first letter, or Qq:')
                                if 'q' == nat or 'Q' == nat:
                                    pickedPlayer = 1
                                    transferDone = 1
                                    break
                                elif nat.upper() in ['A', 'F', 'G', 'I', 'R', 'S']:
                                    nat = board.lookupNationality(nat)
                                    pickedNationality = 1
                                elif nat in board.getAllAvailableNationalities():
                                    pickedNationality = 1
                                else:
                                    print('Invalid nationality, try again ...')
                                if 1 == pickedNationality:
                                    if 1 == board.getPlayersResources(self)[nat][resType]:
                                          print('You already have ' + nat + ' ' + resType)
                                    else:
                                          if 0 == board.getPlayersResources(p)[nat][resType]:
                                              print(p.getName() + ' does not have ' + nat + ' ' + resType)
                                          else:
                                              board.confiscateMaterial(p, nat, resType)
                                              board.updateFunds(self, -amountPerResource)
                                              board.assignResource(self, nat, resType, 'no')
                                              transferDone = 1
                                              print('Confiscated ' + nat + ' ' + resType + ' from ' + p.getName())


class SpyAlleyBoard:
    def __init__(self):
        print('Starting game board initialization ...')
        # Initialize game board
        self.players = []
        self.activePlayers = []
        self.allAvailableNationalities = ['American', 'French', 'German', 'Italian', 'Russian', 'Spanish']
        self.nationalityLookup = { 'A':'American', 'F':'French', 'G':'German', 'I':'Italian', 'R':'Russian', 'S':'Spanish' }
        self.nextSpaceLookup = {
              'Start'               : ['Russian'],
              'Russian'             : ['MoveCard#1'],
              'MoveCard#1'          : ['Disguises'],
              'Disguises'           : ['American'],
              'American'            : ['MoveCard#2'],
              'MoveCard#2'          : ['TakeAnotherTurn'],
              'TakeAnotherTurn'     : ['FreeGift#1'],
              'FreeGift#1'          : ['Collect$10'],
              'Collect$10'          : ['Italian'],
              'Italian'             : ['Keys'],
              'Keys'                : ['Spanish'],
              'Spanish'             : ['MoveCard#3'],
              'MoveCard#3'          : ['BlackMarket#1'],
              'BlackMarket#1'       : ['SpyAlleyEntrance'],
              'SpyAlleyEntrance'    : ['Collect$20', 'BorderCrossing'],
              'Collect$20'          : ['SpyEliminator'],
              'SpyEliminator'       : ['FrenchEmbassy'],
              'FrenchEmbassy'       : ['GermanEmbassy'],
              'GermanEmbassy'       : ['ConfiscateMaterials'],
              'ConfiscateMaterials' : ['SpanishEmbassy'],
              'SpanishEmbassy'      : ['ItalianEmbassy'],
              'ItalianEmbassy'      : ['AmericanEmbassy'],
              'AmericanEmbassy'     : ['RussianEmbassy'],
              'RussianEmbassy'      : ['MoveCard#5'],
              'BorderCrossing'      : ['MoveBack2Spaces'],
              'MoveBack2Spaces'     : ['German'],
              'German'              : ['CodeBooks'],
              'CodeBooks'           : ['MoveCard#4'],
              'MoveCard#4'          : ['FreeGift#2'],
              'FreeGift#2'          : ['French'],
              'French'              : ['MoveCard#5'],
              'MoveCard#5'          : ['BlackMarket#2'],
              'BlackMarket#2'       : ['Start']
            }
        self.moveCards = [ 5, 4, 5, 2, 3, 4, 2, 1, 4, 3, 2, 6, 1, 6, 2, 6, 2, 1, 3, 5, 5, 3, 3, 1, 4, 6, 5, 4, 5, 1, 3, 2, 6, 1, 4, 6 ]
        self.moveCardsDiscardPile = []
        self.giftCards = [
            ['American', 'Disguise'],
            ['Russian',  'CodeBook'],
            ['Spanish',  'Disguise'],
            ['French',   'Disguise'],
            ['Italian',  'CodeBook'],
            ['French',   'CodeBook'],
            ['Russian',  'CodeBook'],
            ['Italian',  'Disguise'],
            ['German',   'Disguise'],
            ['Russian',  'Disguise'],
            ['Spanish',  'CodeBook'],
            ['Italian',  'Disguise'],
            ['German',   'Key'],
            ['Spanish',  'Key'],
            ['Italian',  'Disguise'],
            ['Russian',  'Key'],
            ['Russian',  'Disguise'],
            ['Italian',  'CodeBook'],
            ['French',   'Disguise'],
            ['Spanish',  'CodeBook'],
            ['French',   'Key'],
            ['Russian',  'Disguise'],
            ['German',   'CodeBook'],
            ['Spanish',  'Disguise'],
            ['American', 'Disguise'],
            ['WildCard'],
            ['WildCard'],
            ['Spanish',  'Disguise'],
            ['German',   'Disguise'],
            ['French',   'Disguise'],
            ['WildCard'],
            ['Italian',  'Key'],
            ['American', 'CodeBook'],
            ['German',   'Disguise'],
            ['German',   'CodeBook'],
            ['French',   'CodeBook'],
            ['American', 'Disguise'],
            ['American', 'Key'],
            ['WildCard'],
            ['American', 'CodeBook'],
          ]     
        self.giftCardsDiscardPile = []
        self.positions = {}
        self.playersResourceTypes = [ 'Password', 'Disguise', 'CodeBook', 'Key' ]
        self.playersResources = {}
        self.playersMoney = {}
        self.playersMoveCards = {}
        self.playersWildCards = {}
        print('Finished game board initialization ...')
    def getAmountPerResourceType(self,resType):
        return 1 if 'Password' == resType else (5 if 'Disguise' == resType else (15 if 'CodeBook' == resType else (30 if 'Key' == resType else 10000)))
    def getConfiscateMaterialsPrices(self,resType):
        return 5 if 'Password' == resType else (5 if 'Disguise' == resType else (10 if 'CodeBook' == resType else (25 if 'Key' == resType else (50 if 'WildCard' == resType else 10000))))
    def lookupNationality(self,firstLetter):
        return self.nationalityLookup[firstLetter.upper()]
    def initializeFunds(self):
        startingFunds = 10*len(self.getPlayers())
        for p in self.getPlayers():
            self.playersMoney[p] = startingFunds
    def getPlayers(self):
        return self.players
    def getActivePlayers(self):
        return self.activePlayers
    def addPlayer(self,player):
        self.players.append(player)
        self.activePlayers.append(player)
        self.positions[player] = 'Start'
        self.playersResources[player] = {}
        for nat in self.allAvailableNationalities:
            self.playersResources[player][nat] = {}
            for resType in self.playersResourceTypes:
                self.playersResources[player][nat][resType] = 0
        self.playersMoveCards[player] = [ ]
        self.playersWildCards[player] = 0
    def deactivatePlayer(self,player):
        self.activePlayers.remove(player)
        print('Deactivating player ' + player.getName() + ', remaining are', end='')
        sep = ''
        for p in self.activePlayers:
            print(sep + ' ' + p.getName(), end='')
            sep = ','
        print('')
    def isPlayerActive(self,player):
        # Uncomment the next two lines, if debugging is needed
        # print('player = ' + player.getName())
        # print('active players = ' + str(self.activePlayers))
        return self.activePlayers.count(player) == 1
    def getPlayersPosition(self,player):
        return self.positions[player]
    def getPlayersResourceTypes(self):
        return self.playersResourceTypes
    def getPlayersMoney(self,player):
        return self.playersMoney[player]
    def getPlayersResources(self,player):
        return self.playersResources[player]
    def getPlayersMoveCards(self,player):
        return self.playersMoveCards[player]
    def getPlayersWildCards(self,player):
        return self.playersWildCards[player]
    def getMoveCardsDiscardPile(self):
        return self.moveCardsDiscardPile
    def getGiftCardsDiscardPile(self):
        return self.giftCardsDiscardPile
    def setPlayersPosition(self,player,space):
        self.positions[player] = space
    def getAllAvailableNationalities(self):
        return self.allAvailableNationalities
    def nextSpace(self,space):
        return self.nextSpaceLookup.get(space)
    def setPlayersPositionadvancePlayer(self,player,space):
        self.positions[player] = space
    def passingStart(self,player):
        self.playersMoney[player] += 15
        print(player.getName() + ' received $15 for passing Start')
    def assignPassword(self,player,nat):
        self.playersResources[player][nat]['Password'] = 1
        self.playersMoney[player] -= 1
        print(player.getName() + ' received ' + nat + ' Password')
    def assignResource(self,player,nat,resType,charge='yes'):
        self.playersResources[player][nat][resType] = 1
        if charge == 'yes':
            self.playersMoney[player] = self.playersMoney[player] - self.getAmountPerResourceType(resType)
        print(player.getName() + ' received ' + nat + ' ' + resType)
    def assignMoveCard(self,player):
        if 0 == len(self.moveCards):
            self.moveCards = self.moveCardsDiscardPile
            self.moveCardsDiscardPile = { }
        pick = round(len(self.moveCards) * random.random() - 0.5)
        mc = self.moveCards[pick]
        self.moveCards.remove(mc)
        self.playersMoveCards[player].append(mc)
        print(player.getName() + ' received Move Card')
    def discardMoveCard(self, player, moveCardValue):
        self.playersMoveCards[player].remove(moveCardValue)
        self.moveCardsDiscardPile.append(moveCardValue)
    def assignWildCard(self,player,charge='yes'):
        self.playersWildCards[player] += 1
        if charge == 'yes':
            self.playersMoney[player] -= 50
        print(player.getName() + ' received Wild Card')
    def recordExitThroughEmbassy(self,winningPlayer):
        for p in self.activePlayers:
            if p != winningPlayer:
                self.deactivatePlayer(p)
    def updateFunds(self,player,amount):
        self.playersMoney[player] += amount
    def isSpaceInSpyAlley(self,pos):
        return 'Collect$20' == pos or 'SpyEliminator' == pos or 'FrenchEmbassy' == pos or 'GermanEmbassy' == pos or 'ConfiscateMaterials' == pos or 'SpanishEmbassy' == pos or 'ItalianEmbassy' == pos or 'AmericanEmbassy' == pos or 'RussianEmbassy' == pos
    def getRandomGiftCard(self):
        if 0 == len(self.giftCards):
            self.giftCards = self.giftCardsDiscardPile
            self.giftCardsDiscardPile = []
        pick = round(random.random()*len(self.giftCards)-0.5)
        gc = self.giftCards[pick]
        self.giftCards.remove(gc)
        return gc
    def discardGiftCard(self,gc):
        self.giftCardsDiscardPile.append(gc)
    def confiscateWildCard(self,player):
        amountPerResource = board.getConfiscateMaterialsPrices('WildCard')
        self.wildCards[player] -= 1
        self.playersMoney[player] += amountPerResource
    def confiscateMaterial(self,player,nat,resType):
        amountPerResource = self.getConfiscateMaterialsPrices(resType)
        self.playersResources[player][nat][resType] = 0
        self.playersMoney[player] += amountPerResource
    def transferResources(self,p1,p2):
        for nat in self.allAvailableNationalities:
            for resType in self.playersResourceTypes:
                if 1 == self.playersResources[p1][nat][resType]:
                    self.playersResources[p2][nat][resType] = 1
                    self.playersResources[p1][nat][resType] = 0
        for mc in self.playersMoveCards[p1]:
            self.playersMoveCards[p2].append(mc)
        self.playersMoveCards[p1] = []
        self.playersMoney[p2] += self.playersMoney[p1]
        self.playersMoney[p1] = 0
        self.playersWildCards[p2] += self.playersWildCards[p1]
        self.playersWildCards[p1] = 0
        print('Transferred resources from ' + p1.getName() + ' to ' + p2.getName())
    def switchNationalities(self,p1,p2):
        temp = p1.getNationality()
        p1.setNationality(p2.getNationality())
        p2.setNationality(temp)
    def hasAllResources(self,player):
        hasAll = 1
        for nat in self.allAvailableNationalities:
            if 0 == hasAll:
                break
            for resType in self.playersResourceTypes:
                if 0 == self.playersResources[player][nat][resType]:
                    hasAll = 0
                    break
        return hasAll


class SpyAlleyGame:
    def __init__(self):
        print('In SpyAlleyGame __init__')
    def getBoard(self):
        return self.board
    def getActivePlayers(self):
        return self.ActivePlayers
    def play(self):
        # TBD - implement game play
        print('Starting game initialization ...')
        self.board = SpyAlleyBoard()
        # Initialize human players - ask them for names and secretly inform
        #    them of their nationality
        self.humanCount = eval(input('Enter number of human players: '))
        availableNationalities = list(self.board.getAllAvailableNationalities())
        for pn in range(1, self.humanCount+1):
            name = input('Name the human player #' + str(pn) + ": ")
            # Randomly select nationality
            pos = round(random.random()*len(availableNationalities)+0.5)
            #print('pos = ' + str(pos))
            nat = availableNationalities[pos-1]
            player = HumanPlayer(name, nat)
            self.board.addPlayer(player)
            print(name + "'s position is " + self.board.getPlayersPosition(player))
            print(name + "'s nationality is " + nat)
            availableNationalities.remove(nat)
            input('Confirm receiving nationality. Press [Enter]')
            for i in range(1,100):
                print('')
        # Remaining players are computers
        for pn in range(1,6-self.humanCount+1):
            name = 'Robot #' + str(pn)
            # Randomly select nationality
            pos = round(random.random()*len(availableNationalities)+0.5)
            #print("pos = " + str(pos))
            nat = availableNationalities[pos-1]
            player = ComputerPlayer(name, nat)
            self.board.addPlayer(player)
            # Uncomment the next line for debug, otherwise nationalities are secret
            # print(name + "'s nationality is " + nat)
            availableNationalities.remove(nat)
            print(name + "'s position is " + self.board.getPlayersPosition(player))
        print('Finished game initialization ...')
        # Game loop
        self.getBoard().initializeFunds()
        gameInProgress = 1
        while (gameInProgress == 1):
            for p in self.getBoard().getPlayers():
                if (self.getBoard().isPlayerActive(p)):
                    p.move(self.getBoard())
                    if (len(self.getBoard().getActivePlayers()) == 1):
                        gameInProgress = 0
                        break
                    print('')
                    input('Paused ... - press {Enter]')
        print('')
        print('!!! The winner is ' + self.getBoard().getActivePlayers()[0].getName())
        print('')
        input('Paused ... - press {Enter]')

g=SpyAlleyGame()
g.play()
print('')

b=g.getBoard()
# Get players
for p in b.getPlayers():
    print("# Get player's name")
    print('p.getName():')
    print(p.getName())
    print("# Get player's nationality")
    print('p.getNationality():')
    print(p.getNationality())    
    print("# Get player's last position")
    print('b.getPlayersPosition(p):')
    print(b.getPlayersPosition(p))
    print('')
    print(p.getName() + "'s Resources:")
    p.printResources(b,1)
print('Move card discard pile: ' + str(b.getMoveCardsDiscardPile()))
print('Gift card discard pile: ' + str(b.getGiftCardsDiscardPile()))
