import sys

from termcolor import *
def printOutput(value,color):
    output_string=">>> "+value
    print(colored(output_string, color))

def debugOutput(value,color):
    output_string = "<<< " + value
    print(colored(output_string, color))

def printMsg(msg_sender,value):
    output_string = msg_sender+"<<< " + value
    cprint(output_string,'blue')
    # print(colored(output_string, 'blue'))
