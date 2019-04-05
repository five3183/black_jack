import random

#Global variables 
SUITS = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
RANKS = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
VALUES = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10,
         'Queen':10, 'King':10, 'Ace':11}

GAME = True
PLAYING = True

class Card():
    # Set up card class
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        # Return string for a single card
        return self.rank + ' of ' + self.suit

class Deck():

    def __init__(self):
        # Create a deck list from the suits and ranks vsariables

        self.deck = []
        for suit in SUITS:
            for rank in RANKS:
                self.deck.append(Card(suit, rank))

    def __str__(self):
        # Return string for cards in the deck
        deck_contains=''
        for card in self.deck:
            deck_contains += '\n'+card.__str__()
        return 'Cards in deck:' + deck_contains
    
    def shuffle(self):
        # Shuffle deck
        random.shuffle(self.deck)
    
    def deal(self):
        # Remove top card from deck list
        one_card = self.deck.pop(0)
        return one_card

class Hand():
    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0
    
    def add_card(self,card):
        # Get a card from the deal method in the Deck class and add it to the hand
        self.cards.append(card)
        # Get the value of the card from the VALUES dictionary so that it can be added to the hand value
        self.value += VALUES[card.rank]

        if card.rank == 'Ace':
            self.aces += 1

    def adjust_for_ace(self):
        # Check to see if the hand value is > than 21 and has an ace then reduce the value for by 10 and ace count by 1
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1

class Chips():
    def __init__(self, total=100):
        self.total = total
        self.bet = 0
    
    def win_bet(self):
        self.total += self.bet

    def lose_bet(self):
        self.total -= self.bet

def take_bet(chips):
    while True:
        try:
            chips.bet = int(input('How many chips would you like to bet? '))
        except ValueError:
            print('Bet must be an integer greater than zero ')
        else:
            if chips.bet > chips.total:
                print(f'You have {chips.total} chips \nYou do not have enough chips to cover that bet ')
            else:
                break

def hit(deck, hand):
    hand.add_card(deck.deal())
    hand.adjust_for_ace()

def hit_or_stand(deck, hand):
    global PLAYING
    while True:
        x = input('\nHit or Stand?  Enter H or S ')

        if x.lower() == 'h':
            hit(deck,hand)
            show_some(player_hand, dealer_hand)
            if player_hand.value > 21:
                player_busts(player_hand, dealer_hand, player_chips)
                show_all(player_hand, dealer_hand)
                break
            else:
                continue

        elif x.lower() =='s':
            print('Player stands! \nDealer\'s Turn!')
            PLAYING = False
            break
        else:
            print('Please enter h or s ')
            continue

def show_some(player,dealer):
    print("\nDealer's Hand:")
    print(" <card hidden>")
    print('',dealer.cards[1])  
    print("\nPlayer's Hand:", *player.cards, sep='\n ')
    
def show_all(player,dealer):
    print("\nDealer's Hand:", *dealer.cards, sep='\n ')
    print("Dealer's Hand =",dealer.value)
    print("\nPlayer's Hand:", *player.cards, sep='\n ')
    print("Player's Hand =",player.value)

def player_busts(player, dealer, chips):
    print('Player BUSTS!')
    chips.lose_bet()

def player_wins(player, dealer, chips):
    print('Player Wins!')
    chips.win_bet()

def dealer_wins(player, dealer, chips):
    print('Dealer Wins!')
    chips.lose_bet()

def dealer_busts(player, dealer, chips):
    print('Player Wins!')
    chips.win_bet()

def push(player, dealer):
    print('PUSH!')

while GAME:
    print('Welcome to BLACKJACK')
    player_chips = Chips()

    while PLAYING:
        deck = Deck()
        deck.shuffle()

        player_hand = Hand()
        player_hand.add_card(deck.deal())
        player_hand.add_card(deck.deal())

        dealer_hand = Hand()
        dealer_hand.add_card(deck.deal())
        dealer_hand.add_card(deck.deal())

        take_bet(player_chips)

        show_some(player_hand, dealer_hand)

        hit_or_stand(deck, player_hand)

        if player_hand.value <= 21:

            while dealer_hand.value < player_hand.value:
                hit(deck, dealer_hand)
            
            show_all(player_hand, dealer_hand)

            if dealer_hand.value > 21:
                dealer_busts(player_hand, dealer_hand, player_chips)

            elif dealer_hand.value > player_hand.value:
                dealer_wins(player_hand, dealer_hand, player_chips)

            elif dealer_hand.value < player_hand.value:
                player_wins(player_hand, dealer_hand, player_chips)
            
            else:
                push(player_hand, dealer_hand)
        
        print(f'\nPlayer total chips are:  {player_chips.total}')


        new_game = input('Do you want to play another hand? y/n ')

        if new_game[0].lower() =='y':
            PLAYING = True
            continue
        else:
            print('Thanks for playing! ')
            PLAYING = False
            GAME = False
            break