""" Solutions from reddit posts """

######
# luckily marcusandrews and I had the same puzzle input

lines = open("day-19.txt", "r").readlines()
a, b = int(lines[22].split()[2]), int(lines[24].split()[2])
n1 = 893  # 836 + 22 * a + b  # where did they get 836 and 22?
n2 = 10551293  # n1 + 10550400  # why not just hard code in the correct values if they hard code in the math?

for n in (n1, n2):
    sqn = int(n ** .5)
    print(sum(d + n // d for d in range(1, sqn + 1) if n % d == 0))  # - sqn * (sqn ** 2 == n))  <-- always evals to 0


######
# asger_blahimmel did a generic solve for Part Two only,
# but neglects to explain how he arrived at 10551236 (sqrt of runtime n?)

import re
import collections

a, b = instructions[21].data[2], instructions[23].data[2]  # instructions as they are from my prog
number_to_factorize = 10551236 + a * 22 + b

factors = collections.defaultdict(lambda: 0)
possible_prime_divisor = 2
while possible_prime_divisor ** 2 <= number_to_factorize:
  while number_to_factorize % possible_prime_divisor == 0:
    number_to_factorize /= possible_prime_divisor
    factors[possible_prime_divisor] += 1
  possible_prime_divisor += 1
if number_to_factorize > 1:
  factors[number_to_factorize] += 1

sum_of_divisors = 1
for prime_factor in factors:
  sum_of_divisors *= (prime_factor ** (factors[prime_factor] + 1) - 1) / (prime_factor - 1)

print(sum_of_divisors)


######
# TellowKrinkle said the magic words "My code summed factors of the number in R4"

# Stan-It showed his disassembly that I think would help me in mine
# https://www.reddit.com/r/adventofcode/comments/a7j9zc/2018_day_19_solutions/ec3v5ud/?context=3

# Apparently jonathan_paulson made a great video how-to; I haven't watched it
# https://www.reddit.com/r/adventofcode/comments/a7j9zc/2018_day_19_solutions/ec3i5og/