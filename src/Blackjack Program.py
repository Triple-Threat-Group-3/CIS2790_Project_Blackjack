# Blackjack Program
import random
PlayerList = []
player_money = {}
house = []
totals = {}
cash = {}

# ------------------------------------------------------------
# Function: main
# Purpose:
#     Controls the overall flow of the Blackjack program.
#     This function starts the game, gets the number of players,
#     initializes player hands and money, runs each round, collects
#     bets, calls the dealer and player turn functions, determines
#     winners, updates money, and asks if the players want to play again.
# ------------------------------------------------------------
def main():
    PlayAgain = True
    house_win = False
    bet = None
    print("Welcome to blackjack!")
    players = int(input("Enter # of players: "))
    name_and_totals, total_player_money  = dict_list(totals, players, player_money)
    while PlayAgain:
        house_cards, house_value = dealer(house)
        for name in name_and_totals:
            bet = int(input(f"Enter {name}'s bet: "))
            cash[name] = bet
        print("Player Bets: ")
        print(cash,"\n")
        print("Player Cards: ")
        print(name_and_totals)
        FinalValues = hit_or_stand(name_and_totals)
        print(FinalValues)
        
        
        print("Dealers cards: ")
        print(house_cards)
        print(f"The house has a hand value of: {house_value}")
        if house_value > max(FinalValues.values()):
            for name in cash:
                total_player_money[name] -= cash[name]
                print(f"{name} has lost ${cash[name]}")
            print(f"The house has the highest hand value of {house_value} ")
            print("The house wins! ")
            house_win = True
        elif house_value == max(FinalValues.values()):
            tied_players = [n for n,v in FinalValues.items() if v == house_value]
            print(f"It's a wash between the house and {', '.join(tied_players)}")
        
            
        if house_win != True:    
            winners, losers = check_winners(FinalValues)
            winner_names = list(winners.keys())
            for name in winners:
                if len(winners) > 1:
                    tied_players = [other for other in winners if other != name]
                    tied_list = ', '.join(tied_players)
                    if winners[name] == 0:
                        print("Nobody wins")
                        break
                    print(f"{name} {tied_list} are tied with a hand value of {winners[name]}")
                    total_player_money = adjust_money(cash,winners,losers, player_money, house_value)
                elif len(winners) == 1:
                     print(f"{name} wins with a hand value of {winners[name]}")
                     total_player_money = adjust_money(cash,winners, losers, player_money, house_value)
        print(f"Total player money: {total_player_money}")
        PlayAgain, house_value = play_again(name_and_totals,house_cards,house_value)
        
    print(f"Total player money: {total_player_money}")
    print(cash)

# ------------------------------------------------------------
# Function: play_again
# Purpose:
#     Asks the user if they want to play another round.
#     If the user chooses yes, this function clears the dealer's hand,
#     resets the dealer value, resets each player's hand total, and
#     deals new starting cards to each player.
#
# Parameters:
#     finalvalues - dictionary storing each player's current hand total
#     house_cards - list storing the dealer's cards
#     house_value - integer storing the dealer's hand value
#
# Returns:
#     play_again - True if the game should continue, False if not
#     house_value - reset dealer hand value
# ------------------------------------------------------------
def play_again(finalvalues,house_cards,house_value):
    play_again = True
    question = input(f"Play again ? Enter yes/no ").lower()
    while question not in ['yes','no']:
            print(f"Invalid, must enter (yes/no)")
            question = input("Try again: ").lower()
    if question == 'yes':
        house_cards.clear()
        house_value = 0
        for name in finalvalues:
            finalvalues[name] = 0
        for name in finalvalues:
            total, player_cards = user(PlayerList)
            finalvalues[name] = total
            print(f"{name} Cards: {player_cards} ")
            print(f"{name} Total: {total} \n")
        play_again = True
    else:
        play_again = False
    return play_again, house_value
        
    
# ------------------------------------------------------------
# Function: user
# Purpose:
#     Deals two random starting cards to a player.
#     The card values are randomly generated between 2 and 11.
#     If an Ace is counted as 11 and causes the player to go over 21,
#     the Ace is changed to 1 to prevent an automatic bust.
#
# Parameters:
#     player_cards - list used to store the player's cards
#
# Returns:
#     total - total value of the player's hand
#     player_cards - list of cards dealt to the player
# ------------------------------------------------------------
def user(player_cards):
    random_card = random.randint(2,11)
    random_card2 = random.randint(2,11)
        
    player_cards = []
    player_cards.append(random_card)
    player_cards.append(random_card2)
    total = sum(player_cards)
    if random_card == 11 and total > 21:
        player_cards.remove(random_card)
        ace = 1
        player_cards.append(ace)
        total -= 10
    elif random_card2 == 11 and total > 21:
        player_cards.remove(random_card2)
        ace = 1
        player_cards.append(ace)
        total -= 10
    
    return total, player_cards
    
# ------------------------------------------------------------
# Function: dict_list
# Purpose:
#     Creates the starting player information for the game.
#     This function asks for each player's name, deals each player
#     an opening hand, stores their hand total, and gives each player
#     a starting money amount of $50.
#
# Parameters:
#     dict_totals - dictionary storing each player's hand total
#     total_players - number of players in the game
#     player_money - dictionary storing each player's money balance
#
# Returns:
#     dict_totals - updated dictionary of player hand totals
#     player_money - updated dictionary of player money balances
# ------------------------------------------------------------
def dict_list(dict_totals,total_players, player_money):
    for i in range(total_players):
        name = input(f"Enter player {i+1} name: ")
        total, player_cards = user(PlayerList)
        print(f"Cards: {player_cards}")
        print(f"Total: {total} ")
        dict_totals[name] = total
        player_money[name] = 50 
    return dict_totals, player_money

# ------------------------------------------------------------
# Function: dealer
# Purpose:
#     Controls the dealer's hand for the round.
#     The dealer starts with two random cards and continues drawing
#     cards while the hand value is less than 17. If the dealer has
#     an Ace valued at 11 and the total goes over 21, the Ace is
#     changed to 1. If the dealer still goes over 21, the dealer busts.
#
# Parameters:
#     houses_cards - list storing the dealer's cards
#
# Returns:
#     houses_cards - list of cards in the dealer's hand
#     hand_value - final value of the dealer's hand
# ------------------------------------------------------------
def dealer(houses_cards):
    random_card = random.randint(2,11)
    random_card2 = random.randint(2,11)
    houses_cards.append(random_card)
    houses_cards.append(random_card2)
    
    
    hand_value = sum(houses_cards)
    print("Dealers showing a",houses_cards[0])
    
    if hand_value == 21:
        print(houses_cards[1])
        print("Dealers showing a blackjack!")
        
    elif hand_value > 21 and (random_card == 11 or random_card2 == 11):
        hand_value -= 10
        if random_card == 11:
            print("Dealers showing an ace")
            houses_cards.pop(0)
            random_card -= 10
            houses_cards.append(random_card)
        elif random_card2 == 11:
            houses_cards.pop(1)
            random_card2 -= 10
            houses_cards.append(random_card2)
    
    while hand_value < 17:
        random_card = random.randint(2,11)
        houses_cards.append(random_card)
        hand_value += random_card
        while hand_value > 21 and 11 in houses_cards:
            houses_cards[houses_cards.index(11)] = 1
            hand_value -= 10
        if hand_value > 21:
            hand_value = 0
            break
        
    return houses_cards, hand_value

# ------------------------------------------------------------
# Function: hit_or_stand
# Purpose:
#     Handles each player's turn during the round.
#     Each active player is asked whether they want to hit or stand.
#     If the player hits, a new random card is added to their total.
#     If the player goes over 21, their score is set to 0 because
#     they busted. If the player stands, their current total is kept.
#
# Parameters:
#     DictTotals - dictionary storing each player's current hand total
#
# Returns:
#     DictTotals - updated dictionary after all players finish turns
# ------------------------------------------------------------
def hit_or_stand(DictTotals):
    
    active_players = set(DictTotals.keys()) 
    finished_players = set()
    
    while active_players:
        for name in list(active_players):
            value = DictTotals[name]
            new_value = DictTotals[name]
            print(f"{name} has a hand value of {value}")
            
            prompt = input(f"Does {name} want to hit or stand ? ").lower()
            while prompt not in ['hit','stand']:
                print(f"Invalid, {name} must enter (hit/stand)")
                prompt = input("Try again: ").lower()
            while True:
                if prompt == 'hit':
                    random_card = random.randint(2,11)
                    new_value += random_card
                    
                    if new_value > 21 and random_card == 11:
                        new_value -= 10
                        print(f"{name} received an ace giving them a total of {new_value}")
                        
                    if new_value > 21:
                        print(f"{name} received a {random_card} giving them a total of {new_value}, they have gone bust! ")
                        DictTotals[name] = 0
                        active_players.remove(name)
                        break
                        
                    elif new_value == 21:
                        print(f"{name} received a {random_card} and hit Blackjack!")
                        DictTotals[name] = 21
                        active_players.remove(name)
                        break
                    
                    
                    else:
                        print(f"{name} hits and now has a total of {new_value}")
                        DictTotals[name] = new_value
                        break
                else:
                    print(f"{name} is standing with a total of {new_value}")
                    DictTotals[name] = new_value
                    active_players.remove(name)
                    break
                    
    return DictTotals

# ------------------------------------------------------------
# Function: check_winners
# Purpose:
#     Finds the player or players with the highest hand value.
#     This function separates the players into winners and losers
#     based on the highest final hand value after all turns are complete.
#
# Parameters:
#     final_values - dictionary storing each player's final hand value
#
# Returns:
#     winners - dictionary of players with the highest hand value
#     losers - dictionary of players who did not have the highest value
# ------------------------------------------------------------
def check_winners(final_values):
    max_value = max(final_values.values())
    winners = {k: v for k, v in final_values.items() if v == max_value}
    losers = {k: v for k, v in final_values.items() if v != max_value}
    
    return winners, losers
    
# ------------------------------------------------------------
# Function: adjust_money
# Purpose:
#     Updates each player's money after the round.
#     Winners receive double their bet as a payout. Losers lose the
#     amount they bet. Any player whose money reaches $0 is removed
#     from the player money dictionary.
#
# Parameters:
#     cash - dictionary storing each player's bet
#     winners - dictionary of winning players
#     losers - dictionary of losing players
#     player_money - dictionary storing each player's current money
#     dealer_value - dealer's final hand value
#
# Returns:
#     player_money - updated dictionary of player money balances
# ------------------------------------------------------------
def adjust_money(cash, winners, losers, player_money, dealer_value):

    
    for name in winners:
        bet = cash[name]
        payout = bet * 2
        player_money[name] += payout
        print(f"{name} has won ${payout}!")
    for name in losers:
        bet = cash[name]
        player_money[name] -= bet
        print(f"{name} has lost ${bet}")
        
    for name in list(player_money):
        if player_money[name] == 0:
            del player_money[name]
            print(f"{name} has been removed due to insufficient funds")
            
        
    return player_money
    
                               
main()
