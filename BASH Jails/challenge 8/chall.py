#!/usr/local/bin/python3 -u
import subprocess
import re


def restrict_input(command):
    pattern = re.compile(r'[a-zA-Z*^\,,;\\!@/#?%`"\'&()-+]|[^\x00-\x7F]')
    if pattern.search(command):
        raise ValueError("that's not nice!")
    return command


def execute_command(command):
    safe = restrict_input(command)
    result = subprocess.run(safe, stdout=True, shell=True)
    return result.stdout


print("Welcome to Baby PyBash!\n")
cmd = input("Enter a bash command: ")
output = execute_command(cmd)
print(output)


'''
Solution: $0 
The reason this works is it calls /bin/bash which now calls a new session which cannot be checked by the jail
code (it is running in subprocess, so it's now it's own process blocking the python main code thread.)


Discord:
Explaining why $0 works for Baby Pybash

$ is a special character, and called Expansion character.
You use it when referencing variables, command substitution and etc

When you add a 0 behind it, you reference the first part of the command.
Which in this case is /bin/bash, so you then execute bash again when you give it $0 as a command to the python program

The input is no longer checked by python, so you are allowed to write whatever command.
So to get flag, you write 
cat flag.txt

'''