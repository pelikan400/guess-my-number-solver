#!/usr/local/bin/python3

import random
import curses

digits = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
curses_key_map = {
    '0': ( 0, 0 ),
    '1': ( 1, 0 ),
    '2': ( 2, 0 ),
    '3': ( 3, 0 ),
    '4': ( 4, 0 ),
    '5': ( 1, 1 ),
    '6': ( 2, 1 ),
    '7': ( 3, 1 ),
    '8': ( 4, 1 ),
    '9': ( 2, 2 ),
    'a': ( 3, 2 ),
    'b': ( 4, 2 ),
    'c': ( 3, 3 ),
    'd': ( 4, 3 ),
    'e': ( 4, 4 )
}

class GuessMyNumberSolver:
    def __init__(self):
        ( self.permutationsMap, self.combinationMap ) = self.generate_permutations_of_four(digits)
        # print( "Initialized GuessMyNumberSolver. Number of active permutations: ", self.count_active_permutations() )

    def generate_permutations_of_four( self, digits):
        permutationsMap = {}
        combinationsMap = {}
        count = 0
        for i in digits:
            for j in digits:
                if i == j:
                    continue
                for k in digits:
                    if i == k or j == k:
                        continue 
                    for l in digits:
                        if i == l or j == l or k == l:
                            continue
                        permutation = i + j + k + l
                        permutationsMap[ permutation ] = True
                        count += 1
                        normalized_permutation = self.get_normalized_permutation( permutation )
                        if normalized_permutation in combinationsMap:
                            combinationsMap[ normalized_permutation ] += 1
                        else:
                            combinationsMap[ normalized_permutation ] = 1
        return ( permutationsMap, combinationsMap )

    def calculate_matches( self, permutation1, permutation2 ):
        number_of_right_digits = 0
        number_of_right_positions = 0
        for i in range(0, 4):
            if permutation1[i] == permutation2[i]:
                number_of_right_positions += 1
            for j in range(0, 4):
                if permutation1[i] in permutation2[j]:
                    number_of_right_digits += 1
        return (number_of_right_digits, number_of_right_positions)
    
    def get_normalized_permutation( self, permutation ):
        return ''.join( sorted( permutation ) )

    def delete_impossible_permutations( self, permutation, number_of_right_digits, number_of_right_positions ):
        for key in self.permutationsMap:
            if self.permutationsMap[key] == False:
                continue
            (right_digits, right_positions) = self.calculate_matches( key, permutation )
            if right_digits != number_of_right_digits or right_positions != number_of_right_positions:
                normalized_permutation = self.get_normalized_permutation( key )
                self.combinationMap[ normalized_permutation ] -= 1
                self.permutationsMap[key] = False

    
    def get_combination_with_maximum_matches( self ):
        max_matches = 0
        max_matches_combination = ""
        for combination in self.combinationMap:
            matches = self.combinationMap[combination]
            if matches > max_matches:
                max_matches = self.combinationMap[combination]
                max_matches_combination = combination
            elif matches == max_matches and random.choice([True, False]):
                max_matches_combination = combination
        return max_matches_combination

    def select_permutation( self, combination ):
        for key in self.permutationsMap:
            if self.permutationsMap[key] == False:
                continue
            if self.get_normalized_permutation( key ) == combination:
                return key
        return ""
    
    def print_permutations( self ):
        for key in self.permutationsMap:
            if self.permutationsMap[key] == True:
                print( key, end = " " )
        print()

    def count_active_permutations( self ):
        count = 0
        for key in self.permutationsMap:
            if self.permutationsMap[key] == True:
                count += 1
        return count
    
    def print_cmbination_map( self ):
        count = 0
        for key in self.combinationMap:
            if self.combinationMap[key] != 0:
                count += 1
                print( key, " : ", self.combinationMap[key] )
        print( "Number of combinations: ", count )
    
    def play_one_round( self, permutation, number_of_right_digits, number_of_right_positions ):
        self.delete_impossible_permutations( permutation, number_of_right_digits, number_of_right_positions )
        # print( "Active permutations: ", end="" )
        # self.print_permutations()
        # print( "Number of active permutations: ", self.count_active_permutations() )
        combination = self.get_combination_with_maximum_matches()
        permutation = self.select_permutation( combination )
        # print( "Combination with maximum matches: ",  permutation )
        # self.print_cmbination_map()
        # print()
        return permutation
    
    def get_starting_permutation( self ):
        return random.choice( list( self.permutationsMap.keys() ) )


stdscr = None

def init():
    global stdscr
    stdscr = curses.initscr()
    curses.noecho()  # turn off automatic echoing of key presses

def cleanup():
    global stdscr
    curses.nocbreak()
    stdscr.keypad(False)
    curses.echo()
    curses.endwin()

def get_input():
    global stdscr
    ch1 = stdscr.getch()
    ( number_of_right_digits, number_of_right_positions ) = curses_key_map[ chr( ch1 ) ]
    return ( number_of_right_digits, number_of_right_positions )

def print_help():
    global stdscr
    stdscr.addstr( 1, 20, "     0  1  2  3  4" )
    stdscr.addstr( 3, 20, "0    0" )
    stdscr.addstr( 4, 20, "1    1  5" )
    stdscr.addstr( 5, 20, "2    2  6  9" )
    stdscr.addstr( 6, 20, "3    3  7  A  C" )
    stdscr.addstr( 7, 20, "4    4  8  B  D  E" )

def main():
    global stdscr
    init()
    print_help()
    solver = GuessMyNumberSolver()

    # permutation = "1234"
    permutation = "1987"
    # permutation = solver.get_starting_permutation()

    text_row = 0

    while True:
        # print( "Combination with maximum matches: ",  permutation )
        stdscr.addstr( text_row, 1, "%s " % permutation )
        # guessString = input("")
        # guess = guessString.split()
        # ( number_of_right_digits, number_of_right_positions ) = ( int( guess[0] ), int( guess[1] ) )
        ( number_of_right_digits, number_of_right_positions ) = get_input()
        stdscr.addstr( text_row, 1, "%s %s%s" % ( permutation, number_of_right_digits, number_of_right_positions ) )
        if number_of_right_digits == 4 and number_of_right_positions == 4:
            print( "I won!" )
            break
        permutation = solver.play_one_round( permutation, number_of_right_digits, number_of_right_positions )
        text_row += 1
    cleanup()

if __name__ == "__main__":
    main()