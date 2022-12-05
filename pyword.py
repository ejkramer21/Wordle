"""
Wordle

Description:
    Player guesses secret word.  After each guess, reveal which letters are in
    the secret word in the correct position, wrong position, or not in the word.
    Have a main menu.  Invalid choice displays error message and try again.
    End if player chooses to exit.  Game has 3 round, each with a different
    five letter word. Player has 6 chances per word.  Invalid guesses
    DO NOT count as a turn.
"""

import random as rand
import math as ma
from os.path import exists

#display menu that shows all options
#options must be the number in order to be valid
#invalid responses get error message
def display_menu():
    invalid = True
    while (invalid):
        invalid = False
        print('----- Main Menu -----')
        print('1. New Game')
        print('2. See Hall of Fame')
        print('3. Quit')
        choice = input('\nWhat would you like to do? ')
        if (choice == '1' or choice=='2' or choice =='3'):
            return choice
        else:
            invalid=True
            print('\nInvalid choice. Please try again.\n')


#code for playing game
#provides all prompts for input and calls helper functions
#invalid responses are processed accordingly            
def new_game(list_of_words,scores):
    to_break = False
    total = 0
    words = pick_game_words(list_of_words)
    player = input('Enter your player name: ')
    print('')
    for i in range(3):
        curr_round_sum = []
        guessed =[]
        for j in range(26):
            guessed.append(' ')
        current_word = words[i]
        print(f'Round {i+1}:')
        for j in range(6):
            valid = False
            while(not valid):
                guess = input(f'{j+1}? ')
                if(len(guess) != 5):
                    valid=False
                    print('\nInvalid guess. Please enter exactly 5 characters.\n')
                elif (not guess.isalpha()):
                    valid=False
                    print('\nInvalid guess. Please only enter letters.\n')
                else:
                    valid=True
            guess=guess.lower()
            guessed,round=process_guess(current_word,guess,guessed)
            curr_round_sum.append(round)
            to_break,total = check_guess(guess, current_word,curr_round_sum,i,j,total)
            if(to_break):
                break               
    return player,total
        
    
#checks for correct answer in valid guesses
#returns specified accolade if correct and returns order to break
#loop for current round (only returns true if correct answer guessed)
def check_guess(guess, current_word,curr_round_sum, i, j,total):
    if(guess==current_word.strip()):
        points = ma.pow(2,6-j-1)
        total+=points
        accolade = get_accolade(points)
        print(f'{accolade}! You earned {points:.0f} points this round.')
        round_summary(curr_round_sum,i)
        to_break = True        
    elif(j==5):
        print('You ran out of tries.')
        print(f'The word was {current_word[:5]}.')
        round_summary(curr_round_sum,i)
        to_break = False
    else:
        to_break = False
    return to_break,total

#prints out the summary of the round that shows the
#validity of guesses after each round
def round_summary(curr_round_sum,i):
    print(f'Round {i+1} summary:')
    for j in curr_round_sum:
        print(f'   ',end='')
        for l in j:
            print(f'{l}',end='')
        print('')
    print('')

#switch statements to determine accolade
#called in new game
def get_accolade(points):
    if(points==64):
        return 'Impossible'
    if(points==32):
        return 'Genius'
    if(points==16):
        return 'Magnificent'
    if(points==8):
        return 'Impressive'
    if(points==4):
        return 'Splendid'
    if(points==2):
        return 'Great'
    return 'Phew'

#gives the helpful output info on the guess to show
#player if there guessed in the right position or letter
#keeps track of progress across the alphabet
def process_guess(current_word,guess,guessed):
    round = []
    letters='abcdefghijklmnopqrstuvwxyz'
    print('   ',end='')
    length = len(guess)
    i=0
    for letter in guess:
        index = letters.index(letter)
        if (letter in current_word):
            if(letter in current_word[i:length] and guess.index(letter,i,length) == current_word.index(letter,i,length)):
                print('!',end='')
                guessed[letters.index(letter)] = '!'
                round.append('!')
            else:
                print('?',end='')
                if (not guessed[letters.index(letter)] == '!'):
                    guessed[letters.index(letter)] = '?'
                round.append('?')
        else:
            print('X',end='')
            guessed[letters.index(letter)] = 'X'
            round.append('X')
        i+=1
    print(f'     ',end='')
    for i in guessed:
        print(f'{i}',end='')
    print(f'\n   {guess}     {letters}')
    return guessed,round
    
            
#randomly pick three words from list in words.txt        
def pick_game_words(list_of_words):
    words = []
    words = rand.choices(list_of_words, k=3)
    return words

#check if player's score will be entered into hall of fame
#if will be entered, returns true, false otherwise
def check_fame(players, scores, total):
    sort = sorted(scores)
    num = len(sort)
    if (num>0 and num < 10):
        return True
    elif (num>=10):
        tenth = scores[num-11]
        if (total>tenth):
            return True
    return False

#print congratulatory message if will be entered in hall of fame
def deliver_fame(fame, player, total, scores, players):
    if (fame):
        print(f'Way to go {player}!')
        print(f'You earned a total of {total:.0f} points and made it into the Hall of Fame!')
        hall_of_fame(players,scores)
        
def hof_file(players,scores):
    if (not exists('hall_of_fame.txt')):
        file2 = open('hall_of_fame.txt','a')
    else:
        file2 = open('hall_of_fame.txt','r')
        prev_plays = file2.readlines()
        for line in prev_plays:
            data = line.split(',')
            scores.append(int(data[0]))
            data[1] = data[1].lstrip()
            data[1] = data[1].rstrip()
            players.append(data[1])
        file2.close()
        file2 = open('hall_of_fame.txt','a')
        return file2

def main():
    players = []
    scores = []
    file2 = hof_file(players,scores)
    file = open('words.txt','r')
    list_of_words = file.readlines()
    choice = 0
    print('Welcome to PyWord.\n')
    while (choice !='3'):
        choice = display_menu()
        if (choice=='1'):
            player,total=new_game(list_of_words,scores)
            players.append(player)
            scores.append(total)
            fame = check_fame(scores,players,total)
            deliver_fame(fame, player,total,scores,players)
            file2.write(f'{total:.0f}, {player}\n')
        elif (choice=='2'):
            hall_of_fame(players,scores)
    print('Goodbye.')
    file.close()
    file2.close()

#code for hall of fame
#accounts for the same score received by multiple players
#stable st players that play first get listed    
def hall_of_fame(players, scores):
    print('\n--- Hall of Fame ---')
    print(' ## : Score : Player')
    sorted_scores = sorted(scores)
    num = len(sorted_scores)
    cur = num-1
    j = 0
    for i in range(10): 
        i = j
        place = i+1
        if (cur<0):
            break
        curr_score = sorted_scores[cur]
        if (scores.count(curr_score)>1):
            j=i
            prev_index = int(-1)
            for k in range(scores.count(curr_score)):
                place = j+1
                if (j>=10 or cur<0):
                    break
                print(f' {place:2d} : {curr_score:5.0f} : {players[scores.index(curr_score,int(prev_index)+1,num)]}')
                j+=1
                cur-=1
                prev_index = scores.index(curr_score,prev_index+1,num)
        else:
            j+=1
            print(f' {place:2d} : {curr_score:5.0f} : {players[scores.index(curr_score)]}')
            cur-=1
    print('')


"""Do not change anything below this line."""
if __name__ == "__main__":
    main()
