# Blackjack Game — Technical Documentation

**Project:** A Blackjack Game  
**Team:** Triple Threat — Nathaniel Payne, Hannah Portillo, Muhammad Numan  
**Course:** CIS-2790  

---

## Table of Contents

- [Code Documentation](#code-documentation)
- [Function Header Comments](#function-header-comments)
- [Product Documentation](#product-documentation)
- [Software Architecture Schemas](#software-architecture-schemas)
  - [Logical Architecture](#logical-architecture)
  - [Physical Architecture](#physical-architecture)
- [Database Schemas](#database-schemas)
- [Sequence Diagram](#sequence-diagram)
- [Technical Decision Log](#technical-decision-log)

---

## Code Documentation

To run the game, simply download the release zip, extract to a folder, and open run_blackjack.bat.

The program is split across two Python files and one batch launcher, all kept in the same folder:

- **`blackjack_logic.py`** — All game logic: dealing cards, managing the dealer, processing hits, determining winners, and adjusting money. This module has no knowledge of the GUI and imports only Python's built-in `random` library.
- **`blackjack_gui.py`** — The graphical frontend built with `customtkinter`. It imports all game functions from `blackjack_logic.py` and owns all game state as instance variables on the `BlackjackApp` class.
- **`run_blackjack.bat`** — A Windows batch script that installs `customtkinter` via pip and launches `blackjack_gui.py`.

The GUI imports `house`, `totals`, `player_money`, and `cash` directly from `blackjack_logic.py` and uses them as shared state between the two modules.

---

## Function Header Comments

### `blackjack_logic.py`

---

**`user(player_cards)`**
```
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
```

---

**`dict_list(dict_totals, names, p_money)`**
```
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
```

---

**`dealer(houses_cards)`**
```
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
```

---

**`hit(current_value)`**
```
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
```

---

**`check_winners(final_values)`**
```
# Function: check_winners
# Purpose:
#     Finds the player or players with the highest hand value.
#     This function separates the players into winners and losers
#     based on the highest final hand value after all turns are complete.
# Parameters:
#     final_values - dictionary storing each player's final hand value
# Returns:
#     winners - dictionary of players with the highest hand value
#     losers - dictionary of players who did not have the highest value
```

---

**`adjust_money(cash, winners, losers, p_money, dealer_value)`**
```
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
```

---

**`reset_round(name_and_totals, house_cards)`**
```
# Function: reset_round
# Purpose:
#     Resets state for a new round without full re-init.
# Parameters:
#     name_and_totals - dict of player hand totals to reset
#     house_cards     - list of dealer cards to clear
# Returns:
#     name_and_totals   - reset player totals
#     house_cards       - cleared dealer hand
#     player_cards_map  - new dealt cards per player
```

---

### `blackjack_gui.py`

---

**`BlackjackApp.__init__`**
```
# __init__
# Purpose:
#     Initializes the main window and all game state variables,
#     then launches the first screen.
```

---

**`BlackjackApp._swap(f)`**
```
# _swap
# Purpose:
#     Replaces the currently displayed frame with a new one.
#     Destroys the old frame first to avoid stacking screens.
# Parameters:
#     f - the new CTkFrame to display
```

---

**`BlackjackApp._input_screen(...)`**
```
# _input_screen
# Purpose:
#     Reusable helper that builds a simple input screen with a
#     title, a label, a text entry, and a Continue button.
#     Used for screens 1, 2, and 3 (players, names, bets).
# Parameters:
#     title     - large heading text
#     label     - prompt shown above the entry box
#     default   - pre-filled value in the entry box
#     on_submit - function called with the entry value when Continue is clicked
# Returns:
#     entry - the CTkEntry widget (in case the caller needs it)
```

---


**`BlackjackApp._show_num_players()`**
```
# _show_num_players  (Screen 1)
# Purpose:
#     Asks how many players will be playing.
#     Validates that the input is a positive integer,
#     then moves to the name-entry screen.
```

---


**`BlackjackApp._show_name()`**
```
# _show_name  (Screen 2)
# Purpose:
#     Collects each player's name one at a time.
#     Loops until all names are gathered, then initializes
#     game state (deals opening hands, sets starting balances)
#     and moves to the bet screen.
```

---


**`BlackjackApp._show_bet()`**
```
# _show_bet  (Screen 3)
# Purpose:
#     Collects each player's bet one at a time.
#     Validates the bet is between 1 and the player's balance.
#     Once all bets are placed, deals the dealer's hand and
#     moves to the play screen.
```

---


**`BlackjackApp._show_play()`**
```
# _show_play  (Screen 4)
# Purpose:
#     Displays the current player's hand and the dealer's
#     partially hidden hand, then lets them Hit or Stand.
#     Automatically advances to the next player's turn when
#     the current player busts, hits 21, or stands.
#     When all players are done, moves to the result screen
```

---

**`BlackjackApp._next_turn()`**
```
# _next_turn
# Purpose:
#     Advances _turn_idx to the next player and reloads the
#     play screen. Called after a bust, blackjack, or stand.
```

---

**`BlackjackApp._show_result()`**
```
# _show_result  (Screen 5)
# Purpose:
#     Reveals the dealer's full hand, determines winners and
#     losers, updates balances, and displays the outcome for
#     each player. Offers a Play Again button.
```

---

**`BlackjackApp._play_again()`**
```
# _play_again
# Purpose:
#     Resets the round for another game. Removes any players
#     who have run out of money. If no players remain, shows
#     a Game Over screen. Otherwise redeals hands and goes
#     back to the bet screen.
```

---

## Product Documentation

The Blackjack Game is a desktop card game application. It is designed to simulate a traditional Blackjack experience and uses a simple graphical user interface.
This application was developed for the CIS2790 Software Development Capstone course. The goal of this project is to showcase our understanding and apply system analysis and design concepts to create a prototype for a traditional Blackjack game.

- **Blackjack Project Features**
  - Classic rules for playing Blackjack
  - Allows player interaction through Hit or Stand options
  - Dealer follows standard Blackjack rules
  - Automatically determines outcomes of games
  - Designed to run locally without reliance on networks or internet connections

- **Technologies Used**
  - Python programming language
  - customtkinter is an external library that will need to be installed 
  - GitHub for project tracking

- **How to run the program**
  - Install Python3
  - Install the customtkinter library for GUI
  - Download repository and open src folder
  - Run the program: "blackjack_gui.py"
  - Make sure "blackjack_logic.py" is in the same folder/directory as "blackjack_gui.py"
  - Optionally: simply run "run_blackjack.bat" this is a more direct way to launch the game

- **Program Logic Flow**
  - Program starts and displays a welcome message
  - User enters the number of players
  - Each player is initialized with:
      - Name
      - Starting cards
      - Starting money ($50)
  - Dealer is dealt initial cards
  - Players place bets
  - Each player chooses:
      - Hit to draw another card
      - Stand to keep current total
  - Dealer draws cards until reaching 17 or higher
  - Winners and losers are determined
  - Player money is updated based on results
  - User chooses to play again or exit

- **Entry Point**
  - The main entry point of the program is the main() function.
  - This function controls the entire game flow including setup, gameplay, and replay logic.

- **Environmental Variables**
  - This program does not require any environmental variables.
  - All inputs are handled through user input via customtkinter GUI.

- **Error Handling**
  - Input validation is implemented for:
    - Hit/Stand choices (must be "hit" or "stand")
      - Keyboard shortcuts for: "H" and "h" = Hit or "S" and "s" = Stand)
    - Play again prompt (must be "yes" or "no")
  - Prevents invalid inputs from crashing the program

- **Code Conventions**
  - Uses snake_case naming convention
  - Functions are modular and separated by responsibility
  - Descriptive function names (ex. hit_or_stand, adjust_money)
  - Comments are included above functions to explain their purpose
  - Global dictionaries are used to track player data

- **User Guide**
  - Run the program
  - Enter the number of players when prompted
  - Enter each player's name
  - Let the game begin!

- **Gameplay Instructions**
  - Placing bets
    - Each player will be prompted to enter a bet amount at the start of each round
  - Player Turns
    - Each player will choose:
      - Hit: receive another card
      - Stand: keep current total
  - Goal
    - Get as close to 21 as possible without going over
    - Going over 21 results in a bust or automatic out/loss
  - Dealer Rules
    - Dealer draws cards until reaching a total of 17 or higher
    - Dealer busts if total exceeds 21
  - Winning and Losing
    - Players with the highest total win (highest total while still under 21)
    - Winners receive double their bet
    - Losers lose their bet amount
    - If tied with the dealer, the result is a wash (no gain or loss)
  - Play Again?
    - At the end of each round, you will be asked, "Play Again? (yes/no)"
    - Enter 'yes' to continue playing or 'no' to exit the game

- **Notes**
  - Each player starts with $50
  - Players are removed from the game if their balance reaches $0
  - All inputs must be entered exactly as prompted (ex. 'hit', 'stand', 'yes', 'no')

---

## Software Architecture Schemas

### Logical Architecture 

- **System Architecture**

  The application follows a two-layer architecture which consists of: a presentation layer and a gameplay logic layer.
The presentation layer is handled by blackjack_gui.py while the logic layer is handled by blackjack_logic.py

- **blackjack_gui.py** manages the following
  - user interaction
  - screen rendering
  - input validation
  - navigation between screens

- **blackjack_logic.py** manages the following
  - card generation
  - dealer logic
  - score calculations
  - winner determinations
  - money adjustments

The seperation of presentation and logic allows the game rules to operate independently of the GUI. It also makes maintenance and editing much easier. It also keeps the code more organized and easy to read/follow.

```
┌─────────────────────────────────────┐
│          Presentation Layer         │
│                                     │
│         blackjack_gui.py            │
│                                     │
│  - Handles GUI screens              │
│  - Processes player input           │
│  - Displays cards/results           │
│  - Controls game flow               │
└─────────────────┬───────────────────┘
                  │
                  │ Function Calls
                  ▼
┌─────────────────────────────────────┐
│            Logic Layer              │
│                                     │
│        blackjack_logic.py           │
│                                     │
│  - Deals cards                      │
│  - Controls dealer AI               │
│  - Calculates totals                │
│  - Determines winners               │
│  - Updates player money             │
└─────────────────────────────────────┘
```

### Physical Architecture

The application is a standalone offline desktop program. It requires no network connection, no database, and no server.

```
┌──────────────────────────────────┐
│         User's Computer          │
│                                  │
│  ┌────────────────────────────┐  │
│  │     Python 3.8+ Runtime    │  │
│  │                            │  │
│  │  blackjack_gui.py          │  │
│  │  blackjack_logic.py        │  │
│  │  random (stdlib)           │  │
│  │  customtkinter (library)   │  │
│  └────────────────────────────┘  │
│                                  │
│  OS: Windows / macOS / Linux     │
│  Hardware: Standard PC/laptop    │
│  Network: Not required           │
└──────────────────────────────────┘
```

---

## Sequence Diagram

The following describes the sequence of interactions for one complete round of play.

```
Player(s)          BlackjackApp (GUI)        blackjack_logic.py
   │                       │                          │
   │  Launch app           │                          │
   │──────────────────────►│                          │
   │  Enter # of players   │                          │
   │──────────────────────►│                          │
   │  Enter player names   │                          │
   │──────────────────────►│                          │
   │                       │── dict_list() ──────────►│
   │                       │◄── totals, money, cards ─│
   │  Place bets           │                          │
   │──────────────────────►│                          │
   │                       │── dealer() ─────────────►│
   │                       │◄── house_cards, value ───│
   │  Hit or Stand         │                          │
   │──────────────────────►│                          │
   │                       │── hit() ────────────────►│  (on Hit)
   │                       │◄── new_value, card, ─────│
   │                       │    busted, blackjack     │
   │  [Repeats per player] │                          │
   │                       │                          │
   │                       │── check_winners() ──────►│
   │                       │◄── winners, losers ──────│
   │                       │── adjust_money() ───────►│
   │                       │◄── updated money, ───────│
   │                       │    results               │
   │  View results         │                          │
   │◄──────────────────────│                          │
   │  Play Again / Exit    │                          │
   │──────────────────────►│                          │
   │                       │── reset_round() ────────►│  (on Play Again)
   │                       │◄── new hands ────────────│
```


## Technical Decision Log

| Decision             | Choice Made          | Rationale            |
|---                   |---                   |---                   |
| Programming language | Python               | Familiar coding language to team members; well-suited for rapid development of a 2D desktop game. |
| GUI library          | CustomTkinter        | Uses standard python GUI library `tkinter`, but expands for modern graphical elements. |
| Architecture         | Two-file separation (logic + GUI) | Keeps game rules independent of the interface, making each easier to read and modify. |
