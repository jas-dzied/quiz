#!/usr/bin/env python3

import sys
sys.path.append("/home/jas/Documents/Programming/Projects/quiz/runtime/")
import user_input

fname = './qz.qz'#input('Where would you like to save your quiz? ')
with open(fname, 'w') as file:

    running = True
    while running:

        name = input('What would you like to name your quiz? ')
        file.write(name+'\n'+'~~~'+'\n')

        questions = True
        while questions:

            question_type = user_input.choose_menu('What type of question would you like?', [
                'multiple choice',
                'single answer',
                'options'
            ], 1)
            file.write(question_type+'\n')
            file.write(input('What is the question? ')+'\n')

            if question_type == 'multiple choice':
                file.write(input('What is the correct answer? ')+'\n')
                run = True
                while run:
                    print('Enter the options in the order they appear:')
                    print('(Leave it blank to stop adding options)')
                    choice = input(' :: ')
                    if choice == '':
                        run = False
                    else:
                        file.write(choice+'\n')
            elif question_type == 'single answer':
                file.write(input('What is the correct answer? ')+'\n')
            elif question_type == 'options':
                run = True
                while run:
                    choice = input('Enter a possible answer: ')
                    if choice == '':
                        run = False
                    else:
                        file.write(choice+'\n')
            else:
                assert False, "Impossible case, user input error."

            choice = input('Would you like to add more questions? ')
            if choice.lower() in ['no', 'n', '']:
                questions = False
            else:
                file.write('~~~'+'\n')

        choice = input('Would you like to add another quiz? ')
        if choice.lower() in ['no', 'n', '']:
            running = False
        else:
            file.write('###'+'\n')
