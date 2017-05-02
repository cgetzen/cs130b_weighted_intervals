#!/usr/bin/env python3
""" Weighted interval scheduling """

from bisect import bisect_right
from itertools import islice
from collections import namedtuple

def main():
    # Create a list of triples
    triples = process_input()

    # Sort the list based on end time.
    triples.sort()

    # Create a structure to interact with the set of triples
    collection = Collection(triples)

    # Calculate the nearest possible previous triple for each triple.
    collection.next_previous_possibility()

    collection.solve()

    print(collection)

class Collection():

    def __init__(self, col):
        self.collection = col
        self.sol = []
        self.max_payoff = 0

    def next_previous_possibility(self):
        """
        Calculates the p-list for each triple.
        bisect is of O(log n), so nested in a list comprehension, this
        function is of O(n log n)
        """
        end = [triple.f for triple in self.collection]
        find_location = lambda i: bisect_right(end, self.collection[i].s) - 1
        self.p = [find_location(i) for i in range(len(self.collection))]

    def solve(self):
        """
        Assigns self.sol and self.max_payoff using pre-caching DP.
        Python's max recursion is 1000, so the recursive function was
        transformed into a hard to read for loop (probably should have
        implemented in a tail-recursion-friendly language). This algorithm
        is of O( n )
        """
        # + 1 because we need to append a 0 to the end when the index is -1
        maximum =  [0] * (len(self.collection) + 1)
        for i, triple in enumerate(self.collection):
            # "p-list with weights". Calculates the largets possible max output
            maximum[i] = max(triple.p + maximum[self.p[i]], maximum[i-1])

        iterator = iter(reversed(range(len(self.collection))))
        for i in iterator:
            # In order to tune solution: replace maximum[i] with i - 1 and:
            # >= : smallest set of schedules
            # >  : largest set of schedules
            if self.collection[i].p + maximum[self.p[i]] == maximum[i]:
                self.sol.append(self.collection[i])
                self.max_payoff += self.collection[i].p
                # skip to the next appropriate value
                next(islice(iterator, i-self.p[i]-1, i-self.p[i]-1), None)

    def __repr__(self):
        list_of_elements = "\n".join([str(triple) for triple in reversed(self.sol)])
        return "Maximum Payoff: {}\n{}".format(self.max_payoff, list_of_elements)

class Triple(namedtuple('Triple', 's f p')):

    def __init__(self, start, finish, payoff):
        if start >= finish:
            raise ValueError('Required: start < finish')
        if payoff <= 0:
            raise ValueError('Required: payoff > 0')

    def __repr__(self):
        return "{} {} {}".format(self.s, self.f, self.p)

    def __lt__(self, triple):  # Needed for sorting
        return self.f < triple.f

def process_input():
    collection = []
    try:  # Breaks on <CTRL-D>
        while(True):
            try:  # Breaks on non-integer input
                ints = map(int, input().split())
            except ValueError as ve:
                print(ve)
            try: # Breaks on wrong amount of arguments
                collection.append(Triple(*ints))
            except TypeError:
                print('Input must be 3 integers')
    except:
        return collection

if __name__ == '__main__':
    main()
