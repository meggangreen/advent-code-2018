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
        self.minutes = {}


    def get_history(self):
        schedule = get_schedule()
        guard_idn = None
        for entry in schedule:
            if guard_re.search(entry):
                guard_idn = int(guard_re.search(entry).groups()[0])
            if guard_idn == self.idn:
                self.history.append(entry)


    def calc_sleep(self):
        total = 0
        minutes = {}
        for i in range(len(self.history)):
            if sleeps_re.search(self.history[i]):
                start = int(self.history[i][15:17])
                if i+1 != len(self.history) and wakes_re.search(self.history[i+1]):
                    end = int(self.history[i+1][15:17])
                else:
                    end = 60
                total += end - start
                minutes = input_minutes(minutes, start, end)
            else:
                start, end = None, None
        self.total_sleep = total
        self.minutes = minutes
        return self.total_sleep, self.minutes


    def get_most_slept_minute(self):
        if self.total_sleep <= 0:
            print ("Total sleep is zero")
            return None
        else:
            return sorted(self.minutes.items(), key = lambda kv: kv[1])[-1]


    def input_minutes(self, minutes={}, start=0, end=60):
        for m in range(start, end):
            minutes[m] = minutes.get(m, 0) + 1

        return minutes


def get_schedule():
    with open('day-04.txt') as file:
        schedule = sorted([entry.strip() for entry in file.readlines()])

    return schedule

def get_sleepiest_guard():
    idns = get_guard_idns()
    sleepy = Guard(-1)
    for n in idns:
        guard = Guard(n)
        guard.get_history()
        guard.calc_sleep()
        if guard.total_sleep > sleepy.total_sleep:
            sleepy = guard

    return sleepy


def get_guard_idns():
    schedule = get_schedule()
    guards = []
    for entry in schedule:
        if guard_re.search(entry):
            guards.append(int(guard_re.search(entry).groups()[0]))

    return guards
