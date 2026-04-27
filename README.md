# CIS2790_Project_Blackjack
Project for CIS2790 

## Overview
This repository contains the design components for a Blackjack game program.
This game application is being developed for the CIS2790 Software Development Capstone course.
The goal of this project is to showcase our understanding and apply system analysis and design concepts
to create a prototype for a traditional Blackjack game.
This repository includes the documentation, project management plans, and source code used to 
build the Blackjack game.

---

## Blackjack Project Features
1. Classic rules for playing Blackjack
2. Allows player interaction through Hit or Stand options
3. Dealer follows standard Blackjack rules
4. Automatically determines outcomes of games
5. Designed to run locally without reliance on networks or internet connections

---

## Technologies Used
1. Python programming language
2. Tkinter for GUI
3. GitHub for project tracking

---

## How to run the program
1. Install Python3
2. Download this repository
3. Open src folder
4. Run the program: python "Blackjack Program.py"

---

## Program Logic Flow
1. Program starts and displays a welcome message
2. User enters the number of players
3. Each player is initialized with:
Name
Starting cards
Starting money ($50)
4. Dealer is dealt initial cards
5. Players place bets
6. Each player chooses:
Hit → draw another card
Stand → keep current total
7. Dealer draws cards until reaching 17 or higher
8. Winners and losers are determined
9. Player money is updated based on results
10. User chooses to play again or exit

---

## Entry Point
- The main entry point of the program is the main() function.
- This function controls the entire game flow including setup, gameplay, and replay logic.

---

## Environmental Variables
- This program does not require any environmental variables.
- All inputs are handled through user input via the console.

---

## Error Handling
- Input validation is implemented for:
- Hit/Stand choices (must be "hit" or "stand")
- Play again prompt (must be "yes" or "no")
- Prevents invalid inputs from crashing the program

---

## Code Conventions
- Uses snake_case naming convention
- Functions are modular and separated by responsibility
- Descriptive function names (ex. hit_or_stand, adjust_money)
- Comments are included above functions to explain their purpose
- Global dictionaries are used to track player data

---

## Repository structure
CIS2790_Project_Blackjack
- docs
- project-management
- src
  - Blackjack Program.py
- LICENSE
- README.md

---

## System Architecture
- main() controls game flow and coordinates all functions
- dict_list() initializes players and assigns starting values
- dealer() handles dealer card logic and rules
- hit_or_stand() processes player decisions
- check_winners() determines winners and losers
- adjust_money() updates player balances
- play_again() resets the game state for the next round

---

## User Guide
1. Run the program
2. Enter the number of players when prompted
3. Enter each player's name
4. Let the game begin!

## Gameplay Instructions
- Placing bets
  - Each player will be prompted to enter a bet amount at the start of each round
- Player Turns
  - Each player will choose:
    - Hit: recieve another card
    - Stand: keep current total
- Goal
  - Get as close to 21 as possible without going over
  - Going over 21 results in a bust or automatic out/loss
- Dealer Rules
  - Dealer draws cards until reaching a total of 17 or higher
  - Dealer busts if total exceeds 21
- Winning and Losing
  - Players with the highest total win (highest total while still under 21)
  - Winners recieve double their bet
  - Losers lose their bet amount
  - If tied with the dealer, the result is a wash (no gain or loss)
- Play Again?
  - At the end of each round, you will be asked, "Play Again? (yes/no)"
  - Enter 'yes' to continue playing or 'no' to exit the game

---

## Notes
- Each player starts with $50
- Player are removed from the game if their balance reaches $0
- All inputs must be entered exactly as prompted (ex. 'hit', 'stand', 'yes', 'no')
 
