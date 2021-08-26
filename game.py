from copy import deepcopy as dcopy

class Mancala():
    def __init__(self, pits = None, banks = None, player = 0):
        if not pits:
            self.pits = [
                [4] * 6,
                [4] * 6
            ]
        else:
            self.pits = pits
        
        if not banks:
            self.banks = [0, 0]
        else:
            self.banks = banks
        self.curr_player = player

    @property
    def next_player(self):
        return (self.curr_player + 1) % 2

    @property
    def playerJustMoved(self):
        '''
        Integration w/ MCTS script from mcts.ai
        '''
        return self.curr_player + 1

    def clone(self):
        copy = Mancala(dcopy(self.pits), dcopy(self.banks), dcopy(self.curr_player))
        return copy

    def check_game_end(self):
        '''
        Integration w/ MCTS script from mcts.ai
        '''
        _, player = self.is_game_over()
        if player == -1: # tie
            return 0.5
        elif player == self.curr_player:
            return 0.0
        else:
            return 1.0

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
            scores[self.curr_player] += sum(self.pits[self.next_player]) # curr player gets all the seeds in their opponents pits
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
            #print("empty pit")
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

    def get_possible_moves(self):
        moves = []
        for i in range(6):
            if self.pits[self.curr_player][i] > 0:
                moves.append(i)
        return moves
        
    @classmethod
    def PvP(self):
        m = Mancala()

        while not m.is_game_over()[0]:
            print(m)
            inp = int(input("What is the next move? "))
            m.make_move(inp)
        
        print(m.is_game_over()[1] + "wins")

    @classmethod
    def EvE(self):
        import mcts_bot
        m = Mancala()
        p1 = mcts_bot.MancalaPlayer(1)
        p2 = mcts_bot.MancalaPlayer(2)
        c = 1
        ps = [p2, p1]
        while not m.is_game_over()[0]:
            move = ps[c%2].next_move(m)
            m.make_move(move)
            print(move)
            print(m)
    
        print(m.is_game_over())
            
m = Mancala()

#m.make_move(5)
#m.make_move(1)
#m.make_move(0)
#m.make_move(1)
#print(m)

#Mancala.PvP()

m.EvE()