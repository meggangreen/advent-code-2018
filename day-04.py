"""Part One"""
import re

timestamp_re = re.compile(r"\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2})\]")
guard_re = re.compile(r"Guard #(\d{1,5}) ")
sleeps_re = re.compile(r"(falls asleep)")
wakes_re = re.compile(r"(wakes up)")

class Guard(object):
    def __init__(self, idn):
        self.idn = idn
        self.history = []
        self.total_sleep = 0


    def get_history(self):
        schedule = get_schedule()
        guard_idn = None
        for entry in schedule:
            if guard_re.search(entry):
                guard_idn = int(guard_re.search(entry).groups()[0])
            if guard_idn == self.idn:
                self.history.append(entry)


    def calc_total_sleep(self):
        total = 0
        for i in range(len(self.history)):
            if sleeps_re.search(self.history[i]):
                start = int(self.history[i][15:17])
                if i+1 != len(self.history) and wakes_re.search(self.history[i+1]):
                    end = int(self.history[i+1][15:17])
                else:
                    end = 60
                total += end - start
            else:
                start, end = None, None
        self.total_sleep = total
        return self.total_sleep


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
