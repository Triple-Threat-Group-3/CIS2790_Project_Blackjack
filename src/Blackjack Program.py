# A Blackjack Game
import random
PlayerList = []
PlayerMoney = {}
house = []
totals = {}
cash = {}

def main():
    play_again = True
    house_cards = dealer(house)
    print(house_cards)
    print("Welcome to blackjack!")
    players = int(input("Enter # of players: "))
    name_and_totals = dict_list(totals, players)
    while play_again is True:
        for name in name_and_totals:
            bet = int(input(f"Enter {name}'s bet: "))
            cash[name] = bet
        print("Player Bets: ")
        print(cash,"\n")
        print("Player Cards: ")
        print(name_and_totals)
        FinalValues = hit_or_stand(name_and_totals)
        print(FinalValues)
        winners = check_winners(FinalValues)
        winner_names = list(winners.keys())
        for name in winners:
            if len(winners) > 1:
                tied_players = [other for other in winners if other != name]
                tied_list = ', '.join(tied_players)
                if winners[name] == 0:
                    print("Nobody wins")
                    break
                print(f"{name} {tied_list} are tied with a hand value of {winners[name]}")
                cashout, total_player_money = pay_winner(cash,winners,PlayerMoney)
                print(f"{name} has won ${cashout}!")
            elif len(winners) == 1:
                 print(f"{name} wins with a hand value of {winners[name]}")
                 cashout, total_player_money = pay_winner(cash,winners, PlayerMoney)
                 print(f"{name} has won ${cashout}!")
        question = input(f"Play again ? Enter yes/no ").lower()
        while question not in ['yes','no']:
                print(f"Invalid, must enter (yes/no)")
                question = input("Try again: ").lower()
        if question == 'yes':
            for name in FinalValues:
                FinalValues[name] = 0
            for name in FinalValues:
                total, player_cards = user(PlayerList)
                FinalValues[name] = total
                print(f"{name} Cards: {player_cards} ")
                print(f"{name} Total: {total} \n")
            play_again = True
        else:
            play_again = False
            
    print(cash)
    print(total_player_money)

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
    
    
def dict_list(dict_totals,total_players):
    for i in range(total_players):
        name = input(f"Enter player {i+1} name: ")
        total, player_cards = user(PlayerList)
        print(f"Cards: {player_cards}")
        print(f"Total: {total} ")
        dict_totals[name] = total
    return dict_totals

def dealer(houses_cards):
    random_card = random.randint(10,11)
    random_card2 = random.randint(10,11)
    houses_cards.append(random_card)
    houses_cards.append(random_card2)
    
    
    total = sum(houses_cards)
    print("Dealers showing a",houses_cards[0])
    
    if total == 21:
        print(houses_cards[1])
        print("Dealers showing a blackjack!")
        
    elif total > 21 and (random_card == 11 or random_card2 == 11):
        total -= 10
        if random_card == 11:
            print("Dealers showing an ace")
            houses_cards.pop(0)
            random_card -= 10
            houses_cards.append(random_card)
        elif random_card2 == 11:
            houses_cards.pop(1)
            random_card2 -= 10
            houses_cards.append(random_card2)
            
    print(total)
        
    return houses_cards
    
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
    return {key: value for key, value in final_values.items() if value == max_value}

def pay_winner(cash, winners, player_money):
    total_payout = 0
    
    
    for name, money in winners.items():
        winners_bet = cash[name]
        payout = winners_bet * 2
        total_payout += payout

        
    return total_payout, player_money
        
                               
main()

 


    


