from enum import Enum

class Ruleset(Enum):
    DEFAULT = 0

class Mancala():
    def __init__(self):
        self.pits = [
            [4] * 6,
            [4] * 6
        ]
        self.banks = [0, 0]
        self.curr_player = 0

    @property
    def next_player(self):
        return (self.curr_player + 1) % 2

    def is_game_over(self):
        '''
        Return (game_is_over, winner)
        where game_is_over is a bool representing if the game is over,
        and winner is either None (if game_is_over == False), or the number of the player who won, or -1 if tie.
        '''
        if sum(self.pits[self.curr_player]) > 0:
            return False, None
        else:
            scores = self.banks
            scores[self.next_player] += sum(self.pits[self.next_player]) # other player gets all the seeds in their pits
            winner = -1 # default to a tie
            if scores[0] > scores[1]:
                winner = 0
            elif scores[0] < scores[1]:
                winner = 1
            return True, winner

    def make_move(self, pit_no):
        if not (0 <= pit_no <= 5):
            print("invalid move")
            return
        
        seeds = self.pits[self.curr_player][pit_no]
        if seeds == 0:
            print("empty pit")
            return

        self.pits[self.curr_player][pit_no] = 0

        ptr = pit_no
        while seeds:
            ptr += 1
            if ptr == 6: # self-bank
                self.banks[self.curr_player] += 1
            elif ptr == 13: # opponent-bank
                ptr = 0
                continue
            else:
                side = (self.curr_player + (ptr // 6)) % 2
                self.pits[side][ptr%6-(1 if ptr > 6 else 0)] += 1
            seeds -= 1
        
        if ptr < 6 and self.pits[self.curr_player][ptr] == 1: # if move ended in an empty on our side, capture!
            # TODO: other rule-sets have this at even OR empty
            captured = self.pits[self.curr_player][ptr]
            captured += self.pits[self.next_player][5-ptr]
            self.banks[self.curr_player] += captured

            self.pits[self.curr_player][ptr] = 0
            self.pits[self.next_player][5-ptr] = 0

        if not ptr == 6: # if move didn't end in self-bank, turn moves to the next player
            self.curr_player = self.next_player

    def __str__(self): # string representation of the board from the perspective of P0
        # TODO improve padding for the banks
        # TODO represent the current player
        string = ""

        string += "|" + "|".join([str(x) for x in self.pits[1][::-1]]) + "|"
        string += "\n"
        string += str(self.banks[1]) + "-"*11 + str(self.banks[0])
        string += "\n"
        string += "|" + "|".join([str(x) for x in self.pits[0]]) + "|"
        string += "\n"

        return string
        
m = Mancala()

m.make_move(5)
m.make_move(1)
m.make_move(0)
m.make_move(1)

print(m)