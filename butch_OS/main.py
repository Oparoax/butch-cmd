import json
import sys
import webbrowser

from random import choice as random_choice
from time import sleep, time

from progress.bar import ShadyBar
from progress.spinner import Spinner


class ConsoleHandler:
    def __init__(self):
        self.importer = FileImporter()
        self.progress_display = ProgressDisplay()

        self.butch_phrases = self.importer.phrases
        self.progress_msgs = self.importer.progress_msgs
        self.music_links = self.importer.links

        self.butch = Butch(self.butch_phrases)
        self.kioshi = Kioshi(self.music_links)

    def play_intro(self):
        self.progress_display.spinner('Welcome to ..', 2, "")

        print('\n')

        sleep(1)

        print(f"{self.importer.get_file_content('Assets/title.txt')} \n")

        for msg in self.progress_msgs["progress_msgs"]:
            self.progress_display.loading_bar(msg['name'], msg['delay'], msg['complete'])

        sleep(2)

        print(self.importer.get_file_content('Assets/butch-portrait.txt'))

        sleep(1)

        print(self.importer.get_file_content('Assets/complete.txt'))

    def listen_for_input(self):
        input_str = input()

        input_str.strip()
        keywords = input_str.split(" ")

        for keyword in keywords:
            keyword = keyword.lower()
            keyword = keyword.strip()

        match keywords[0]:
            case 'butch':
                self.butch_commands(keywords)
                return
            case 'kioshi':
                self.kioshi_commands(keywords)
            case 'help':
                return
            case 'exit':
                sys.exit()
            case _:
                print("Command not recognised")

    def butch_commands(self, commands):

        match commands[1]:
            case 'version':
                self.butch.get_version()
            case 'speak':
                print(f"butch says: {self.butch.get_butch_phrase()}")
            case 'takeaway':
                print(
                    "Two Number 9's,"
                    "\n a number 9 large,"
                    "\n number 6 with extra dip,"
                    "\n number 7,"
                    "\n 2 number 45's, one with cheese,"
                    "\n and a large soda")
            case _:
                print("Command not recognised")

    def kioshi_commands(self, commands):

        match commands[1]:
            case 'version':
                self.kioshi.get_version()
            case 'play':
                self.kioshi.play_yt_playlist()
            case 'radio':
                self.kioshi.play_yt_radio()
            case _:
                print("Command not recognised")


class Butch:
    def __init__(self, phrases):
        self.phrases = phrases
        self.version = "0.9.2"

    def get_version(self):
        return print(f"Version: {self.version}")

    def get_butch_phrase(self):
        return random_choice(self.phrases['phrases'])


class Kioshi:
    def __init__(self, links):
        self.links = links
        self.version = "v1.2.1"

    def get_version(self):
        return print(f"Version: {self.version}")

    def play_yt_playlist(self):
        self.play_yt(self.links['playlist'])

    def play_yt_radio(self):
        self.play_yt(self.links['radio'])
        
    def play_yt(self, link):
        print("Loading up ...")
        webbrowser.open(link[0])


class ProgressDisplay:
    def __init__(self):
        self.bar_max = 100
        self.funk_print = FunkyPrint()

    def loading_bar(self, process_name, delay, is_completed=True):
        if is_completed:
            bar_max = self.bar_max
        else:
            bar_max = self.bar_max - random_choice([20, 15, 10, 5])

        if delay > 0.2:
            self.funk_print.pr_red("WTF that delay is too long")
            return

        with ShadyBar(process_name, max=self.bar_max) as bar:
            for i in range(bar_max):
                # Do some work
                sleep(delay)
                bar.next()
            bar.finish()
            self.funk_print.pr_status_msg(is_completed)

    def spinner(self, process_name, delay, complete_msg):
        spinner = Spinner(process_name)
        time_elapsed = 0

        start = time()

        if delay > 5:
            self.funk_print.pr_red("WTF that delay is too long")
            return

        while time_elapsed < delay:
            time_elapsed = time() - start
            spinner.next()

        spinner.finish()

        if complete_msg is not None:
            print(complete_msg)


class FileImporter:
    def __init__(self):
        self.phrases = self.load_json_phrases()
        self.progress_msgs = self.load_json_intro_progress()
        self.links = self.load_json_kioshi_links()

    def get_file_content(self, filepath):
        text_file = open(filepath, 'r')
        text = text_file.read()
        text_file.close()

        if text is not None:
            return text
        else:
            print(f"File not found: {filepath}")

    def get_json_content(self, filepath):
        text_file = open(filepath, 'r')
        text = json.load(text_file)

        return text

    def load_json_phrases(self):
        phrases = self.get_json_content('JSON/butch_text.json')

        if phrases is not None:
            return phrases
        else:
            print('No phrases could be loaded for butch')

    def load_json_intro_progress(self):
        progress_msgs = self.get_json_content('JSON/butch_loading_text.json')

        if progress_msgs is not None:
            return progress_msgs
        else:
            print('No progress msgs could be loaded for butch')

    def load_json_kioshi_links(self):
        links = self.get_json_content('JSON/kioshi_links.json')

        if links is not None:
            return links
        else:
            print('No links could be loaded for kioshi')


class FunkyPrint:

    def pr_status_msg(self, result):
        if result:
            self.pr_green('Complete')
        else:
            self.pr_red('Failed')

    def pr_red(self, txt):
        print("\033[91m {}\033[00m".format(txt))

    def pr_green(self, txt):
        print("\033[92m {}\033[00m".format(txt))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    console = ConsoleHandler()
    debug_mode = False

    if len(sys.argv) > 1:
        if sys.argv[1] == "-d":
            debug_mode = True
    else:
        console.play_intro()

    print("----------------------------")
    print('= Welcome to butch-os v1.0 =')
    print("----------------------------")

    is_finished = False

    while not is_finished:
        console.listen_for_input()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
