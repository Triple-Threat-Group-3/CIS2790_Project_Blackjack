# Blackjack Program - Logic
import random

SUITS = ["clubs", "diamonds", "hearts", "spades"]

def _rand_card():
    """Return (value, suit) where value is 2-11."""
    return random.randint(2, 11), random.choice(SUITS)

PlayerList = []
player_money = {}
house = []
totals = {}
cash = {}

# ------------------------------------------------------------
# Function: user
# Purpose:
#     Deals two random starting cards to a player.
#     The card values are randomly generated between 2 and 11.
#     If an Ace is counted as 11 and causes the player to go over 21,
#     the Ace is changed to 1 to prevent an automatic bust.
# Parameters:
#     player_cards - list used to store the player's cards
# Returns:
#     total - total value of the player's hand
#     player_cards - list of cards dealt to the player
# ------------------------------------------------------------
def user(player_cards):
    # Cards are now (value, suit) tuples
    c1_val, c1_suit = _rand_card()
    c2_val, c2_suit = _rand_card()
    
    player_cards = [(c1_val, c1_suit), (c2_val, c2_suit)]
    total = c1_val + c2_val
    if c1_val == 11 and total > 21:
        player_cards[0] = (1, c1_suit)
        total -= 10
    elif c2_val == 11 and total > 21:
        player_cards[1] = (1, c2_suit)
        total -= 10
        
    return total, player_cards


# ------------------------------------------------------------
# Function: dict_list
# Purpose:
#     Creates the starting player information for the game.
#     This function asks for each player's name, deals each player
#     an opening hand, stores their hand total, and gives each player
#     a starting money amount of $50.
# Parameters:
#     dict_totals - dictionary storing each player's hand total
#     names       - list of player name strings
#     p_money     - dictionary storing each player's money balance
# Returns:
#     dict_totals - updated dictionary of player hand totals
#     p_money     - updated dictionary of player money balances
#     player_cards_map - dict of name -> list of cards
# ------------------------------------------------------------
def dict_list(dict_totals, names, p_money):
    player_cards_map = {}                             
    for name in names:   
        total, player_cards = user(PlayerList)
        dict_totals[name] = total
        p_money[name] = 50
        player_cards_map[name] = player_cards
    return dict_totals, p_money, player_cards_map

# ------------------------------------------------------------
# Function: dealer
# Purpose:
#     Controls the dealer's hand for the round.
#     The dealer starts with two random cards and continues drawing
#     cards while the hand value is less than 17. If the dealer has
#     an Ace valued at 11 and the total goes over 21, the Ace is
#     changed to 1. If the dealer still goes over 21, the dealer busts.
# Parameters:
#     houses_cards - list storing the dealer's cards
# Returns:
#     houses_cards - list of cards in the dealer's hand
#     hand_value   - final value of the dealer's hand
# ------------------------------------------------------------
def dealer(houses_cards):
    c1_val, c1_suit = _rand_card()
    c2_val, c2_suit = _rand_card()
    houses_cards.append((c1_val, c1_suit))
    houses_cards.append((c2_val, c2_suit))
    hand_value = c1_val + c2_val

    if hand_value > 21 and (c1_val == 11 or c2_val == 11):
        hand_value -= 10
        if c1_val == 11:
            houses_cards[0] = (1, c1_suit)
        elif c2_val == 11:
            houses_cards[1] = (1, c2_suit)

    while hand_value < 17:
        val, suit = _rand_card()
        houses_cards.append((val, suit))
        hand_value += val
        # Convert aces (11) to 1 if over 21
        while hand_value > 21 and any(v == 11 for v, _ in houses_cards):
            for i, (v, s) in enumerate(houses_cards):
                if v == 11:
                    houses_cards[i] = (1, s)
                    hand_value -= 10
                    break
        if hand_value > 21:
            hand_value = 0
            break

    return houses_cards, hand_value

# ------------------------------------------------------------
# Function: hit
# Purpose:
#     Deals one card to a player. If the player goes over 21,
#     their score is set to 0 because they busted.
# Parameters:
#     current_value - player's current hand total
# Returns:
#     new_value   - updated hand total
#     card        - the card that was dealt
#     busted      - True if player went over 21
#     blackjack   - True if player hit exactly 21
# ------------------------------------------------------------
def hit(current_value):
    val, suit = _rand_card()
    new_value = current_value + val
    busted = False
    blackjack = False

    if new_value > 21 and val == 11:
        new_value -= 10
        val = 1   # treat ace as 1 for display

    if new_value > 21:
        busted = True
        new_value = 0
    elif new_value == 21:
        blackjack = True

    return new_value, (val, suit), busted, blackjack

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
# Parameters:
#     cash - dictionary storing each player's bet
#     winners - dictionary of winning players
#     losers - dictionary of losing players
#     p_money - dictionary storing each player's current money
#     dealer_value - dealer's final hand value
# Returns:
#     player_money - updated dictionary of player money balances
#     results      - dict of name -> (amount, won) for GUI
# ------------------------------------------------------------
def adjust_money(cash, winners, losers, p_money, dealer_value):
    results = {}
    for name in winners:
        bet = cash[name]
        payout = bet * 2
        p_money[name] += payout
        results[name] = (payout, True)
    for name in losers:
        bet = cash[name]
        p_money[name] -= bet
        results[name] = (bet, False)
    for name in list(p_money):
        if p_money[name] == 0:
            del p_money[name]
    return p_money, results


# ------------------------------------------------------------
# Function: reset_round
# Purpose:
#     Resets state for a new round without full re-init (NEW).
# Parameters:
#     name_and_totals - dict of player hand totals to reset
#     house_cards     - list of dealer cards to clear
# Returns:
#     name_and_totals   - reset player totals
#     house_cards       - cleared dealer hand
#     player_cards_map  - new dealt cards per player
# ------------------------------------------------------------
def reset_round(name_and_totals, house_cards):
    house_cards.clear()
    player_cards_map = {}
    for name in name_and_totals:
        total, player_cards = user(PlayerList)
        name_and_totals[name] = total
        player_cards_map[name] = player_cards
    return name_and_totals, house_cards, player_cards_map
