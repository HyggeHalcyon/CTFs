import re
import subprocess
from string import printable as asci

alfa_num = re.compile(r'[a-zA-Z0-9]')
asci_regex = re.compile(rf'^[{re.escape(asci)}]*$')

while True:
    try:
        print("Get the flag with your command!!!")
        command = input("input>> ")
        command = str(command)
        
        if alfa_num.match(command):
            print("Permission denied!")
            print("Only accept special character")
            
        if not asci_regex.match(command):
            print("Permission denied!")
            print("Use only printable ascii")
        
        elif len(command) < 5000:
            print("Permission denied!")
            print("Minimum 5000 characters")
            
        else:
            subprocess.run(command, shell=True, executable="/bin/bash")
        
        print()
    except Exception as e:
        print(f"An error occurred: {e}")