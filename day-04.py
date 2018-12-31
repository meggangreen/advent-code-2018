"""Part One"""

class Guard(object):
    def __init__(self, idn):
        self.idn = idn
        self.history = []
        self.total_sleep = 0

    def get_most_slept_minute(self):
        if not self.history or total_sleep <= 0:
            print ("Unable to calculate:", "history: {}", "sleep: {}".
                   format(self.history, self.total_sleep), '\n')
            return None

        # code

def get_schedule():
    with open('day-04.txt') as file:
        schedule = sorted([entry.strip() for entry in file.readlines()])

    return schedule

def get_sleepiest_guard():
    pass


def get_most_slept_minute(guard):
    pass
