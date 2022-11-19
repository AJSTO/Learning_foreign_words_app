# Importing all needed libraries.
import os
import random
import sys
import time

import pandas as pd
import requests
from numpy import zeros


class Application:
    """
    Simple game created for learning foreign languages.
    Allow to choose target language from: EN|FR|DE.
    Version 1.0.
    Future updates?:
    - letting choose a language source not only target.
    - adding more languages.
    - finding way to allow ASCII latin-2 with Google Translate API.
    - creating SQLserwer to connect for bigger base of words (now words are captured from xlsx file).
    - allow to choose categories, now category is randomly choosen from given 4.
    """
    HEADER = """                          
                            /\            \n
                           /::\           \n
                          /::::\          \n
            ,a_a         /\::::/\         \n
           {/ ''\_      /\ \::/\ \        \n
           {\ ,_oo)    /\ \ \/\ \ \       \n
           {/  (_^____/  \ \ \ \ \ \      \n
 .=.      {/ \___)))*)    \ \ \ \ \/      \n
(.=.`\   {/   /=;  ~/      \ \ \ \/       \n
    \ `\{/(   \/\  /        \ \ \/        \n
     \  `. `\  ) )           \ \/         \n
      \    // /_/_            \/          \n
       '==''---))))                       \n
Witamy w aplikacji do nauki słówek.
"""

    def __init__(self):
        df = pd.read_excel('./dictionary.xlsx', header=1)  # reading from xlsx.
        self.dictionary = df.drop('Unnamed: 0', axis=1)  # dropping unnecessary column.

    # Cleaning window method.
    def cls(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    # Checking if player want to start a game.
    def check_y(self):
        print(self.HEADER)
        user_input = input('Czy chcesz zacząć? t/n')
        if user_input.lower() == 'n':
            print('Dziękuję za skorzystanie z aplikacji :)')
            time.sleep(5)
            return sys.exit()
        elif user_input.lower() != 't':
            self.cls()
            print("Przepraszam nie rozumiem, czy możemy jeszcze raz?")
            return self.check_y()
        self.cls()

    # Choosing language
    def take_language(self):
        lang = ['en', 'fr', 'de']
        print('Proszę wybrać język')
        self.language = input('EN|FR|DE?')
        if self.language.lower() not in lang:
            self.cls()
            print("Przepraszam nie rozumiem, czy możemy jeszcze raz?")
            self.take_language()
        self.cls()
        self.chosen_language = self.language.lower()

    # Random choice of category and words.
    def suffle_category_and_words(self):
        self.category = random.choice(self.dictionary.columns)  # choosing random category.
        self.sample = random.sample(list(self.dictionary.index), k=1)  # k is for number of chosen words.

    # Method for translate word.
    def get_translate(self, word, language):
        url = "https://google-translate1.p.rapidapi.com/language/translate/v2"  # copied from API page.
        headers = {
            # RapidAPI Google Translate:
            # link: https://rapidapi.com/googlecloud/api/google-translate1
            "content-type": "application/x-www-form-urlencoded",  # copied from API page.
            "Accept-Encoding": "application/gzip",  # copied from API page.
            "X-RapidAPI-Key": "62d4a1e54emsh8383b0b77225583p1a8a90jsn30c27e399d2e",  # API key from API endpoint
            "X-RapidAPI-Host": "google-translate1.p.rapidapi.com"  # API host from google translate API endpoint
        }
        payload = f"q={word}&target={language}&source=pl"  # payload to API based on chosen word and language.

        response = requests.request("POST", url, data=payload, headers=headers)
        try:
            return response.json()['data']['translations'][0]['translatedText']  # get from json translated word.
        except KeyError:
            return 'KeyError'

    # Translating shuffled 5 words.
    def translated(self):
        translated_words = {}
        for index in self.sample:
            element = self.dictionary.at[index, self.category]
            translated = self.get_translate(element, self.chosen_language)
            translated_words[element] = translated.lower()
        if bool('keyerror' in translated_words.values()):
            print('Przepraszamy awaria API :(, domyślny język to EN.')
            time.sleep(2)
            self.cls()
            self.translated_words = {
                'widelec': 'fork',
                'telefon': 'telephone',
                'biurko': 'desk',
                'rower': 'bike',
                'lampa': 'lamp', }
        else:
            print(f'Wylosowana kategoria to: {self.category}')
            time.sleep(2)
            self.cls()
            self.translated_words = translated_words  # dict with words in pl and foreign lang.
        self.translated_words_C = self.translated_words.copy()  # making a copy for future pd.df of failures.

    # Parameters for starting game.
    def start_guess_game(self):
        self.SCORE = 0  # Starting score =0.
        self.failures = dict(zip(list(self.translated_words.values()), zeros(5, dtype=int)))  # dict for capt failures.
        self.points = {0: 20, 1: 10, 2: 5}  # ranking of points.

    # Method for running guessing a translated word.
    def guess_game(self):
        while self.translated_words and not bool(3 in list(self.failures.values())):
            word_pl = random.choice(list(self.translated_words.keys()))  # polish word.
            clue = self.translated_words[word_pl]  # translated word.
            now = time.time()
            guess = input(f'Proszę przetłumacz słowo {word_pl}:')
            later = time.time()
            q_time = later - now  # time to take a answer.
            if clue == guess.lower() and q_time < 20:
                print(f'Brawo! + {self.points[self.failures[clue]]}!')
                del self.translated_words[word_pl]  # deleting guessed k,v from dict.
                self.SCORE += self.points[self.failures[clue]]
                time.sleep(2)
                self.cls()
                return self.guess_game()
            if q_time > 20:
                print('Próba nieudana :(\nczas odpowiedzi +20s')
                self.failures[clue] += 1  # +1 to failure dict.
                time.sleep(2)
                self.cls()
                return self.guess_game()
            else:
                print('Próba nieudana :(')
                self.failures[clue] += 1  # +1 to failure dict.
                time.sleep(2)
                self.cls()
                return self.guess_game()
        fail_table = pd.DataFrame(  # setting pandas df for number of failed attempts
            {
                'Słówko': list(self.translated_words_C.keys()),
                'Przetłumaczone': list(self.translated_words_C.values()),
                'Błędy': list(self.failures.values())
            }
        )
        if not any(self.failures.values()):
            print(f'Twój wynik to {self.SCORE}!\n'
                  '5/5 dobrych odpowiedzi!')
            return None
        elif self.SCORE < 100:
            print(f'Ukończono test, twój wynik to: {self.SCORE})')
            print('Słowa które sprawiły Ci trudność:\n')
            print(fail_table[fail_table['Błędy'] > 0].reindex())
            return None

    # Method for running application.
    def run(self):
        self.check_y()
        self.take_language()
        self.suffle_category_and_words()
        self.translated()
        self.start_guess_game()
        self.guess_game()
        question = input('Czy chcesz zacząć jeszcze raz? t/n')
        if question == 't':
            time.sleep(1)
            self.cls()
            return self.run()
        self.cls()
        print('Dziękujemy za skorzystanie z gry.')
        time.sleep(1)
        return sys.exit()


# Enabling running if opened strictly from file in shell.
if __name__ == '__main__':
    app = Application()
    app.run()
