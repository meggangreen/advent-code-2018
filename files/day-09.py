""" Part One """
# puzzle data: 424 players; last marble is worth 71482 points

# make circle
# make player hash
# keep track of who is playing on turn 23 - player counter
# keep track of index - index counter
# marble++

class Game(object):
    def __init__(self, num_players, valuablest_marble):
        self.circle = []
        self.players = {i: 0 for i in range(1, num_players+1)}
        self.marbles = [m for m in range(valuablest_marble,-1,-1)]
        self.c_index = None                          # int
        self.c_player = None                         # int
        self.c_marble = None                         # int


    def start(self):
        self.circle.append(0)
        self.c_index = 0
        self.c_player = 0
        self.c_marble = self.marbles.pop()
        self.play()


    def end(self):
        winners = sorted(self.players.items(), key=lambda kv: kv[1], reverse=True)
        print("GAME OVER")
        print(winners[0])


    def play(self):
        if not self.marbles:
            print("I've lost my marbles ...")
            return

        while self.marbles:
            # player and marble selection
            self.c_marble = self.marbles.pop()
            self.advance_player()

            # marble evaluation
            if self.c_marble % 23 == 0:
                # player gets points
                p_index = self.rotate_circle(-7)
                self.add_points(self.c_marble + self.circle[p_index])
                # marble removal
                del self.circle[p_index]
                # reset c_index and max_index
                self.c_index = p_index
            else:
                self.c_index = self.rotate_circle(2)
                self.circle.insert(self.c_index, self.c_marble)

        self.end()


    def advance_player(self):
        if self.c_player + 1 > len(self.players):
            self.c_player = 1
        else:
            self.c_player += 1


    def rotate_circle(self, num):
        if len(self.circle) == 2:
            return 1

        if len(self.circle) == 1:
            return 1

        if self.c_index + num > len(self.circle):
            return self.c_index + num - len(self.circle)
        elif self.c_index + num < 0:
            return self.c_index + num + len(self.circle)
        else:
            return self.c_index + num


    def add_points(self, points, player=None):
        if not player:
            player = self.c_player
        if self.players.get(player) is None:
            self.players[player] = 0
        self.players[player] += points


""" Part Two """
# copied again from the interwebs
# I assumed that rotating a deck would be O(n), which would give it the same
# runtime as my P1 solution (I think lol), but it's obviously faster.
# I like my score-keeping better, but max is obviously better than sorted =)

# From reddit marcusandrews
from collections import deque

def play_game(num_players, valuablest_marble):
    scores = players = {i: 0 for i in range(1, num_players+1)}
    circle = deque([0])

    for marble in range(1, valuablest_marble + 1):
        if marble % 23 == 0:
            circle.rotate(7)
            scores[marble % num_players + 1] += marble + circle.pop()
            circle.rotate(-1)
        else:
            circle.rotate(-1)
            circle.append(marble)

    return max(scores.values()) if scores else 0