# Blackjack Program
import random
PlayerList = []
player_money = {}
house = []
totals = {}
cash = {}

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
    
    
def dict_list(dict_totals,total_players, player_money):
    for i in range(total_players):
        name = input(f"Enter player {i+1} name: ")
        total, player_cards = user(PlayerList)
        print(f"Cards: {player_cards}")
        print(f"Total: {total} ")
        dict_totals[name] = total
        player_money[name] = 50 
    return dict_totals, player_money

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

def check_winners(final_values):
    max_value = max(final_values.values())
    winners = {k: v for k, v in final_values.items() if v == max_value}
    losers = {k: v for k, v in final_values.items() if v != max_value}
    
    return winners, losers
    

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
