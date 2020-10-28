from random import choice
from typing import List


def hangman_pics(mistakes: List[str]) -> List[str]:
    """Načte soubor s obrázky, automaticky jej po práci uzavře.
    Pokud hráč udělal alespoň jednu chybu, vrátí daný obrázek"""
    with open("obrazky.txt", encoding="utf-8") as file:
        all_lines = file.readlines()
    if len(mistakes) != 0:
        first_index = 8 * (len(mistakes) - 1) + 1
        second_index = 8 * len(mistakes) + 1
        return all_lines[first_index:second_index]
    else:
        return [""]


def game_status(missed_letters: List[str]) -> None:
    """Funkce vypíše stav hry, pokud hráč udělal alespoň jednu chybu"""
    if len(missed_letters) != 0:
        picture = (hangman_pics(missed_letters))
        print(*picture)
        print("Špatně hádaná písmena:")
        print(*missed_letters, end=" ")
        print()
    else:
        print()


def choose_word() -> str:
    """Náhodně vybere jedno slovo ze seznamu"""
    with open("ceska_podstatna_jmena.txt", encoding="utf-8") as file:
        words = file.readlines()
        new_words = []
        for word in words:
            word = word.replace("\n", "")
            new_words.append(word)
    return choice(new_words).lower()


def get_index_position(chosen_word: str, letter: str) -> List[int]:
    """Funkce zjišťuje indexy písmen v daném slově"""
    index_pos_list = []
    for i in range(len(chosen_word)):
        if letter in chosen_word[i]:
            index_pos_list.append(i)
    return index_pos_list


def move(field: str, position: int, letter: str) -> str:
    """Vrátí herní pole s umístěným daným písmenem"""
    return field[:position] + letter + field[position + 1:]


def guessing(already_guessed: List[str], chosen_word: str) -> str:
    """Funkce se ptá hráče na písmeno. Pokud nezadá jedno písmeno, nepustí
    ho funkce dále. Pokud zadá již zkoušené písmeno, taktéž se dále
    nedostane"""
    while True:
        answer = input("Hádej písmeno: ").lower()
        if answer.isalpha():
            if len(answer) > 1:
                print("Zadej pouze jedno písmeno.")
            elif answer in already_guessed:
                print("Toto písmeno jsi již zkoušel. Vyber jiné.")
            else:
                return answer
        else:
            print("Zadej písmeno, nikoli jiný znak.")


def play_again() -> bool:
    """Funkce zjišťuje, zda chce hráč pokračovat ve hře"""
    while True:
        answer = input("Chceš hrát znovu? ano/ne ").lower()
        if answer == "ano" or answer == "a":
            return True
        elif answer == "ne" or answer == "n":
            return False
        else:
            print("Nerozumím. Zadej ano nebo ne.")


def hangman() -> None:
    """Vlastní funkce hry. Načte slovo k uhádnutí, vytvoří pro něj hrací pole.
    Následuje funkce pro hádání písmena. Po každém hádání se odpověď a hra
    vyhodnotí"""
    print("Vítej ve hře šibenice.")
    game_is_done = False
    missed_letters: List[str] = []
    correct_letters: List[str] = []
    random_word = choose_word()
    print("Uhádni slovo. Dané slovo má", len(random_word), "písmen/a.")
    game_field = len(random_word) * "-"
    print(game_field)
    while not game_is_done:
        game_status(missed_letters)
        already_guessed = missed_letters + correct_letters
        guess = guessing(already_guessed, random_word)
        if guess not in random_word:
            missed_letters.append(guess)
            print("Dané písmeno ve slově není.")
            print(game_field)
        else:
            indexes = get_index_position(random_word, guess)
            for i in indexes:
                correct_letters.append(guess)
                game_field = (move(game_field, i, guess))
            print(game_field)
        if len(correct_letters) == len(random_word):
            print("Gratuluji Vyhrál jsi.")
            game_is_done = True
        if len(missed_letters) == 10:
            game_status(missed_letters)
            print("Hledané slovo bylo:", random_word)
            print("Je mi líto. Prohrál jsi.")
            game_is_done = True
        if game_is_done:
            if play_again():
                missed_letters = []
                correct_letters = []
                game_is_done = False
                random_word = choose_word()
                print("Uhádni slovo. Má", len(random_word), "písmen/a.")
                game_field = len(random_word) * "-"
                print(game_field)


hangman()
