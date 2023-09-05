import subprocess

def output():
    path = "/beacon/beacon/db/verifier.txt"
    #open text file in read mode
    text_file = open(path, "r")
    
    #read whole file to a string
    data = text_file.read()
    
    #close file
    text_file.close()
    

    command = 'beacon-verifier ' + data
    try:
        bash = subprocess.check_output(command, shell=True)
    except subprocess.CalledProcessError as e:
        bash = e.output
    return bash

output()