import random
import string

def RandomWord():
    #Pick a random word from Mots.txt
    with open("Mots.txt", "r") as f:
        words = f.readlines()
        return random.choice(words).strip()
    
print(RandomWord())