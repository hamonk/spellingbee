import sys
from gtts import gTTS
import argparse
import json
from playsound import playsound
import random
import csv
import colorama
from colorama import Fore, Style

def say_word(word):
    """
    Use gTTS to say a word.
    """
    tts = gTTS(text=word, lang='es')
    tts.save("word.mp3")
    playsound("word.mp3")

def read(filename="words.csv"):
    data = {}
    with open(filename) as f:
        for row in csv.reader(f):
            data[row[0]] = {'definition': row[1], 'example': row[2]}
    return data

def play(word, data, instruction=True):
    
    if instruction:
        say_word(word)
        say_word("como se escribe?")
    
    user_input = input(Fore.BLUE + "Please type and spell the word you just heard. You can also write " + Fore.RED + "'r'" + Fore.BLUE + "for repeat," + Fore.RED + "'d'" + Fore.BLUE + " for definition and " + Fore.RED + "'e'" + Fore.BLUE + " for example.\n" + Fore.BLACK)
    
    if user_input == word:
        say_word("Muy bien!")
        _ = input("Type any key to continue...\n")

        return 1

    else:
        
        if user_input == 'd':
            definition = data[word]['definition']
            say_word(definition)
            play(word, data, instruction=False)

        elif user_input == 'e':
            example = data[word]['example']
            say_word(example)
            play(word, data, instruction=False)

        elif user_input == 'r':
            example = data[word]['example']
            say_word(word)
            play(word, data, instruction=False)            

        else:
            texto = f"No es correcto. La respuesta era "
            say_word(texto)
            print(f"{word}## You: ##{user_input}##")

            _ = input("Type any key to continue...\n")
            return 0

def main():

    data = read()

    args = parse_args()

    words = list(data.keys())

    stat = {}
    for x in [len(word) for word in words]:
        if x in stat:
            stat[x] += 1
        else:
            stat[x] = 1
    options = list(stat.keys())
    options.sort()
    for x in options:
        print(f"Number of words with {x} letters: {stat[x]}")

    # for x in words:
    #     print(f"{len(x)}: {x}")

    # sys.exit(0)

    if args.len > -1:
        print(f"Before reduction: {len(words)}")
        words = [x for x in words if len(x) == args.len]
        print(f"After reduction: {len(words)}")

    characters = list(set(''.join(words)))
    characters.sort()
    print(f"Letters are from this list: {''.join(characters)}")



    with open("memory.json", "r") as f:
        memory = json.load(f)
    
    if 'good' not in memory:
        memory['good'] = []
    if 'bad' not in memory:
        memory['bad'] = []
       
    
    
    if args.verbose:
        say_word("Bienvenido al spelling bee juego en español!")
        say_word(f"Tengo {len(words)} palabras en mi vocabulario")    

    if args.random:
        challenge = [words[random.randint(0,len(words)-1)] for _ in range(args.num)]
        if args.len == -1:
            say_word(f"Te voy a preguntar {args.num} de la lista completa")
        else:
            say_word(f"Te voy a preguntar {args.num} con {args.len} lettras")
    else:
        n = min(len(memory['bad']), args.num)
        print(f"min between request ({args.num}) and bad words ({len(memory['bad'])}) in: {n}")
        bad_words = memory['bad']
        random.shuffle(bad_words)
        challenge = bad_words[:n]
        say_word(f"Te voy a preguntar {n} de la lista de las palabras que te equivocaste en el pasado")

    ok = []
    ko = []

    for word in challenge:

        res = play(word, data)

        if res == 1:
            ok.append(word)
            if word not in memory['good']:
                memory['good'].append(word)
        else:
            ko.append(word)
            if word not in memory['bad']:
                memory['bad'].append(word)

    with open("memory.json", "w") as f:
        json.dump(memory, f)

    say_word(f"Tuviste {len(ok)} buenas palabras")
    say_word(f"Tuviste {len(ko)} not so buenas palabras")

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--verbose", action="store_true", required=False, default=False)
    parser.add_argument("--random", action="store_true", required=False, default=False)
    parser.add_argument("--num", type=int, dest="num", required=False, default=10)
    parser.add_argument("--len", type=int, dest="len", required=False, default=-1)
    return parser.parse_args()

if __name__ == "__main__":

    main()