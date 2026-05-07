# Blackjack GUI - customtkinter frontend
# Imports all game logic from blackjack_logic.py; this file only handles the UI.
import customtkinter as ctk
from blackjack_logic import (
    dict_list, dealer, hit, check_winners, adjust_money,
    reset_round, house, totals, player_money, cash, PlayerList
)

# Use light mode and the built-in blue color theme
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

# Aces (1 and 11) display as "A"; all other card values display as their number
FACE = {1: "A", 11: "A"}

def card_str(val):
    # Returns the display string for a card value
    return FACE.get(val, str(val))

def hand_text(cards, hide_first=False):
    # Builds a string like  [A]  [7]  [3]  from a list of card values.
    # If hide_first is True, the first card shows as [?] (dealer's hidden card).
    parts = []
    for i, c in enumerate(cards):
        parts.append("[?]" if hide_first and i == 0 else f"[{card_str(c)}]")
    return "  ".join(parts)


class BlackjackApp(ctk.CTk):
    # ------------------------------------------------------------
    # __init
    # Purpose:
    #     Initializes the main window and all game state variables,
    #     then launches the first screen.
    # ------------------------------------------------------------
    def __init__(self):
        super().__init__()
        self.title("Blackjack")
        self.geometry("800x600")
        self.resizable(False, False)

        # --- Game state ---
        self.num_players = 0           # Total number of players entered
        self.player_names = []         # Names collected during setup
        self.player_totals = totals    # dict: name -> current hand value
        self.player_cards_map = {}     # dict: name -> list of card values
        self.house_cards = house       # List of dealer's card values
        self.house_value = 0           # Dealer's final hand value
        self.bets = cash               # dict: name -> bet amount for this round
        self.money = player_money      # dict: name -> running balance

        # --- Turn tracking ---
        self._player_list = []         # Ordered list of active player names
        self._name_idx = 0             # Index of the player we're currently naming
        self._bet_idx = 0              # Index of the player we're currently betting
        self._turn_idx = 0             # Index of the player whose turn it is
        self._frame = None             # Reference to the currently displayed frame

        self._show_num_players()       # Start on the first screen

    # ------------------------------------------------------------
    # _swap
    # Purpose:
    #     Replaces the currently displayed frame with a new one.
    #     Destroys the old frame first to avoid stacking screens.
    # Parameters:
    #     f - the new CTkFrame to display
    # ------------------------------------------------------------
    def _swap(self, f):
        if self._frame:
            self._frame.destroy()
        self._frame = f
        f.pack(fill="both", expand=True, padx=40, pady=30)

    # ------------------------------------------------------------
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
    # ------------------------------------------------------------
    def _input_screen(self, title, label, default, on_submit):
        f = ctk.CTkFrame(self)
        ctk.CTkLabel(f, text=title, font=("", 26, "bold")).pack(pady=(20, 30))
        ctk.CTkLabel(f, text=label).pack()
        entry = ctk.CTkEntry(f, width=200, justify="center")
        entry.insert(0, default)
        entry.pack(pady=8)
        entry.focus()
        ctk.CTkButton(f, text="Continue", width=140,
                      command=lambda: on_submit(entry.get())).pack(pady=12)
        self._swap(f)
        return entry

    # ------------------------------------------------------------
    # _show_num_players  (Screen 1)
    # Purpose:
    #     Asks how many players will be playing.
    #     Validates that the input is a positive integer,
    #     then moves to the name-entry screen.
    # ------------------------------------------------------------
    def _show_num_players(self):
        def submit(val):
            try:
                n = int(val)
                assert n >= 1
            except:
                return   # Ignore invalid input; keep the screen open
            self.num_players = n
            self.player_names.clear()
            self._name_idx = 0
            self._show_name()
        self._input_screen("Welcome to Blackjack!", "Number of players:", "1", submit)

    # ------------------------------------------------------------
    # _show_name  (Screen 2)
    # Purpose:
    #     Collects each player's name one at a time.
    #     Loops until all names are gathered, then initializes
    #     game state (deals opening hands, sets starting balances)
    #     and moves to the bet screen.
    # ------------------------------------------------------------
    def _show_name(self):
        idx = self._name_idx
        def submit(val):
            name = val.strip()
            if not name:
                return   # Ignore blank names
            self.player_names.append(name)
            self._name_idx += 1
            if self._name_idx < self.num_players:
                # More players still need names
                self._show_name()
            else:
                # All names collected — initialize game state via logic module
                self.player_totals.clear()
                self.player_cards_map.clear()
                self.money.clear()
                self.bets.clear()
                t, m, cards = dict_list(self.player_totals, self.player_names, self.money)
                self.player_totals.update(t)
                self.money.update(m)
                self.player_cards_map.update(cards)
                self._player_list = list(self.player_names)
                self._bet_idx = 0
                self._show_bet()
        self._input_screen("Setup", f"Enter player {idx + 1} name:", "", submit)

    # ------------------------------------------------------------
    # _show_bet  (Screen 3)
    # Purpose:
    #     Collects each player's bet one at a time.
    #     Validates the bet is between 1 and the player's balance.
    #     Once all bets are placed, deals the dealer's hand and
    #     moves to the play screen.
    # ------------------------------------------------------------
    def _show_bet(self):
        name = self._player_list[self._bet_idx]
        bal = self.money.get(name, 50)
        def submit(val):
            try:
                bet = int(val)
                assert 1 <= bet <= bal   # Bet must be positive and within balance
            except:
                return   # Ignore invalid input
            self.bets[name] = bet
            self._bet_idx += 1
            if self._bet_idx < len(self._player_list):
                # More players still need to bet
                self._show_bet()
            else:
                # All bets placed — deal the dealer's hand
                self.house_cards.clear()
                _, self.house_value = dealer(self.house_cards)
                self._turn_idx = 0
                self._show_play()
        self._input_screen("Place Your Bet",
                           f"{name}'s bet  (balance: ${bal}):", "10", submit)

    # ------------------------------------------------------------
    # _show_play  (Screen 4)
    # Purpose:
    #     Displays the current player's hand and the dealer's
    #     partially hidden hand, then lets them Hit or Stand.
    #     Automatically advances to the next player's turn when
    #     the current player busts, hits 21, or stands.
    #     When all players are done, moves to the result screen.
    # ------------------------------------------------------------
    def _show_play(self):
        # If all players have taken their turn, show results
        if self._turn_idx >= len(self._player_list):
            self._show_result()
            return

        name = self._player_list[self._turn_idx]
        val  = self.player_totals[name]
        p_cards = self.player_cards_map.get(name, [])

        f = ctk.CTkFrame(self)

        # Show current player's hand
        ctk.CTkLabel(f, text=f"{name}  —  {val} total",
                     font=("", 18, "bold")).pack(pady=(20, 4))
        ctk.CTkLabel(f, text=hand_text(p_cards), font=("", 20)).pack()

        # Show dealer's hand with the first card hidden
        ctk.CTkLabel(f, text="Dealer", font=("", 14)).pack(pady=(20, 4))
        dealer_shown = self.house_cards[:2] if len(self.house_cards) >= 2 else self.house_cards
        ctk.CTkLabel(f, text=hand_text(dealer_shown, hide_first=True),
                     font=("", 20)).pack()

        # Status label — updated when the player busts, gets blackjack, or stands
        status = ctk.CTkLabel(f, text="", text_color="gray")
        status.pack(pady=10)

        btn_row = ctk.CTkFrame(f, fg_color="transparent")
        btn_row.pack()

        def do_hit():
            # Deal one card via the logic module and update state
            new_val, card, busted, blackjack = hit(val)
            self.player_totals[name] = new_val
            self.player_cards_map[name].append(card)
            if busted:
                # Player exceeded 21 — score set to 0 in logic, move on after delay
                status.configure(text=f"Bust!", text_color="red")
                hit_btn.configure(state="disabled")
                stand_btn.configure(state="disabled")
                self.after(1000, self._next_turn)
            elif blackjack:
                # Player hit exactly 21
                status.configure(text="Blackjack! 🎉", text_color="green")
                hit_btn.configure(state="disabled")
                stand_btn.configure(state="disabled")
                self.after(1000, self._next_turn)
            else:
                # Refresh the screen to show the new card
                self._show_play()

        def do_stand():
            # Player keeps their current total — no card drawn
            status.configure(text=f"{name} stands at {val}.")
            hit_btn.configure(state="disabled")
            stand_btn.configure(state="disabled")
            self.after(800, self._next_turn)

        hit_btn   = ctk.CTkButton(btn_row, text="Hit",   width=120, command=do_hit)
        stand_btn = ctk.CTkButton(btn_row, text="Stand", width=120, command=do_stand)
        hit_btn.pack(side="left", padx=12)
        stand_btn.pack(side="left", padx=12)

        self._swap(f)

    # ------------------------------------------------------------
    # _next_turn
    # Purpose:
    #     Advances _turn_idx to the next player and reloads the
    #     play screen. Called after a bust, blackjack, or stand.
    # ------------------------------------------------------------
    def _next_turn(self):
        self._turn_idx += 1
        self._show_play()

    # ------------------------------------------------------------
    # _show_result  (Screen 5)
    # Purpose:
    #     Reveals the dealer's full hand, determines winners and
    #     losers, updates balances, and displays the outcome for
    #     each player. Offers a Play Again button.
    # ------------------------------------------------------------
    def _show_result(self):
        final     = dict(self.player_totals)
        house_val = self.house_value
        result_lines = []    # General messages (e.g. "Dealer busted!")
        money_results = {}   # dict: name -> (amount, won) for per-player display

        if house_val > 0 and house_val > max(final.values(), default=0):
            # Dealer beats everyone — deduct bets manually (no adjust_money needed)
            for nm in self._player_list:
                self.money[nm] = self.money.get(nm, 50) - self.bets.get(nm, 0)
                money_results[nm] = (-self.bets.get(nm, 0), False)
            result_lines.append(f"Dealer wins with {house_val}.")
        else:
            if house_val == 0:
                # Dealer busted — all non-bust players win
                result_lines.append("Dealer busted!")
                winners = {k: v for k, v in final.items() if v > 0}
                losers  = {k: v for k, v in final.items() if v == 0}
            else:
                # Normal case — highest hand wins
                winners, losers = check_winners(final)
                # Remove players who tied with the dealer (a "wash" — no money changes)
                for k in [k for k, v in winners.items() if v == house_val]:
                    del winners[k]
            self.money, money_results = adjust_money(
                self.bets, winners, losers, self.money, house_val)

        f = ctk.CTkFrame(self)

        # Reveal dealer's full hand
        ctk.CTkLabel(f, text=f"Dealer  —  {house_val} total",
                     font=("", 16, "bold")).pack(pady=(20, 4))
        ctk.CTkLabel(f, text=hand_text(self.house_cards), font=("", 18)).pack()

        ctk.CTkLabel(f, text="─" * 36, text_color="gray").pack(pady=8)

        # General result messages
        for line in result_lines:
            ctk.CTkLabel(f, text=line, font=("", 13), text_color="gray").pack()

        # Per-player win/loss messages
        for nm, (amt, won) in money_results.items():
            color = "green" if won else "red"
            verb  = "won" if won else "lost"
            ctk.CTkLabel(f, text=f"{nm} {verb} ${abs(amt)}!",
                          font=("", 17, "bold"), text_color=color).pack(pady=2)

        # Show updated balances for all players
        bal_text = "   ".join(f"{nm}: ${self.money.get(nm, 0)}"
                               for nm in self._player_list)
        ctk.CTkLabel(f, text=bal_text, text_color="gray").pack(pady=(6, 0))

        ctk.CTkButton(f, text="Play Again", width=150,
                      command=self._play_again).pack(pady=16)

        self._swap(f)

    # ------------------------------------------------------------
    # _play_again
    # Purpose:
    #     Resets the round for another game. Removes any players
    #     who have run out of money. If no players remain, shows
    #     a Game Over screen. Otherwise redeals hands and goes
    #     back to the bet screen.
    # ------------------------------------------------------------
    def _play_again(self):
        # Remove players who can no longer afford to bet
        broke = [nm for nm in self._player_list if self.money.get(nm, 0) <= 0]
        for nm in broke:
            self._player_list.remove(nm)
            self.player_totals.pop(nm, None)
            self.player_cards_map.pop(nm, None)

        if not self._player_list:
            # No players left — show game over screen
            f = ctk.CTkFrame(self)
            ctk.CTkLabel(f, text="Game Over!", font=("", 24, "bold"),
                          text_color="red").pack(expand=True, pady=60)
            ctk.CTkLabel(f, text="All players are out of money.").pack()
            ctk.CTkButton(f, text="Exit", command=self.destroy).pack(pady=20)
            self._swap(f)
            return

        # Reset hands and clear bets for the new round
        self.player_totals, self.house_cards, self.player_cards_map = \
            reset_round(self.player_totals, self.house_cards)
        self.bets.clear()
        self._bet_idx = 0
        self._show_bet()


if __name__ == "__main__":
    app = BlackjackApp()
    app.mainloop()
