import sys
from paraphrase import Paraphrase
from lyrics import Lyrics, setup_config, get_text
from song import Song


class WrongOptionTypeError(Exception):
    """
    This class is an exception. It appears when wrong option is chosen.

    It inherits from Exception class.
    """
    def __init__(self):
        super().__init__("Input is not an available option!")


class Interface:
    """
    This class gives access to console UI enabling generating texts and
    paraphrasing them.

    :param option: stores current paraphrase option
    :type option: str


    :param text: stores current generated text
    :type text: lyrics

    :param paraphrase: stores converted paraphrase text
    :type text: str

    :param config: configuration file object
    :type text: json
    """
    def __init__(self, config):
        self.option = None
        self.title = None
        self.text = None
        self.paraphrase = None
        self.paraphrases_database = {}
        self.config = setup_config(config)

    def start(self):
        """
        Infinite loop returning to main menu.
        """
        while True:
            self.choose_option()

    def get_option(self, limit=0):
        """
        Gets menu option chosen by user/if help is true serves as a brief stop.

        Raises WrongOptionTypeError if option is not an available choice.
        It is intercepted and launches wrong_option function.
        """
        try:
            self.option = None
            option = input("Select option: ")
            option = str(option)
            option = option.strip(" ()-.")
            if int(option) not in range(1, limit+1):
                raise WrongOptionTypeError
            self.option = option
        except WrongOptionTypeError:
            self.wrong_option()
        except ValueError:
            self.wrong_option()

    def wrong_option(self):
        """
        Prints wrong option and returns to main menu.
        """
        print("Wrong option!")
        self.choose_option()

    def choose_option(self):
        """
        Prints main menu on the screen and checks which option was chosen.
        """
        print(self)
        self.get_option(6)
        option = self.option
        if option == "1":
            self.help()
        elif option == "2":
            self.generate_random_text()
        elif option == "3":
            self.choose_paraphrase()
        elif option == "4":
            self.add_to_database()
        elif option == "5":
            self.search_in_database()
        elif option == "6":
            self.end_program()
        else:
            self.choose_option()

    def add_to_database(self):
        """
        Adds current paraphrased text to dictionary with title as key.
        """
        if self.title in self.paraphrases_database.keys():
            self.text_in_paraphrase()
        if self.paraphrase:
            self.title = self.title.lower()
            self.paraphrases_database[self.title] = self.paraphrase
            print("Text added to database.")
        else:
            self.empty_paraphrase()

    def text_in_paraphrase(self):
        """
        Prints an error message when text is already in the dictionary.
        """
        print("Text already in database!")
        self.choose_option()

    def empty_paraphrase(self):
        """
        Prints an error message when text paraphrase param is empty.
        """
        print("There isn't any paraphrase to save!")
        self.choose_option()

    def search_in_database(self):
        """
        Prints paraphrase from dictionary after inputing its title.
        """
        title = input("Enter title of saved paraphrase you want to print: ")
        try:
            title = title.lower()
            if title in self.paraphrases_database.keys():
                self.print_text(self.paraphrases_database[title])
            else:
                self.not_in_database()
        except TypeError:
            self.not_in_database()

    def not_in_database(self):
        """
        Prints an error message when searched title isn't in the database.
        """
        print("Can't find this title in database!")
        self.choose_option()

    def __str__(self):
        """
        Returns the main menu options as a string.
        """
        description = """
        1. Help
        2. Generate text
        3. Paraphrase the text
        4. Save current paraphrase to database
        5. Search for paraphrase in database
        6. Quit\n """
        return description

    def help(self):
        """
        Prints the general help message.

        Allows the user to choose to see more specific help messages
        or return to main menu.
        """
        general_help = self.config["help"]["help_general"]
        general_help = "\n".join(general_help)
        print(general_help)
        self.get_option(3)
        option = self.option
        if option == "2":
            self.generate_text_help()
        elif option == "3":
            self.paraphrase_help()
        else:
            self.choose_option()

    def paraphrase_help(self):
        """
        Prints the help message for the paraphrase option.

        Allows the user to choose to see more specific help messages
        or return to main menu.
        """
        paraphrase_help = self.config["help"]["help_paraphrase"]
        paraphrase_help = "\n".join(paraphrase_help)
        print(paraphrase_help)
        self.get_option(2)
        option = self.option
        if option == "1":
            self.words_to_modify_help()
        else:
            self.choose_option()

    def words_to_modify_help(self):
        """
        Prints the help message for the words_to_modify option.

        Allows the user to choose to see more specific help messages
        or return to main menu.
        """
        words_to_modify_help = self.config["help"]["help_words_to_modify"]
        words_to_modify_help = "\n".join(words_to_modify_help)
        print(words_to_modify_help)
        self.get_option(2)
        option = self.option
        if option == "1":
            self.accuracy_help()
        else:
            self.choose_option()

    def accuracy_help(self):
        """
        Prints the help message for the accuracy option.

        Allows the user to return to the main menu.
        """
        accuracy_help = self.config["help"]["help_accuracy"]
        accuracy_help = "\n".join(accuracy_help)
        print(accuracy_help)
        self.get_option(1)
        self.choose_option()

    def generate_text_help(self):
        """
        Prints the help message for the generate text option.

        Allows the user to return to the main menu.
        """
        generate_text_help = self.config["help"]["help_generate_text"]
        generate_text_help = "\n".join(generate_text_help)
        print(generate_text_help)
        self.get_option(1)
        self.choose_option()

    def generate_random_text(self):
        """
        Allows the user to search for a song or generate random poem.


        generate a random poem or go back to the main menu
        """
        print("""
        1. Search for a song
        2. Generate random poem
        3. Back to menu\n""")
        self.get_option(3)
        option = self.option
        if option == "1":
            self.search_for_song()
        elif option == "2":
            self.generate_random_poem()
        else:
            self.choose_option()

    def generate_random_poem(self):
        """
        Generates a random poem and sets it as the current text.
        """
        self.text = Lyrics(get_text(self.config["urls"], "random_poem"))
        self.title = self.text.title()
        print("\n")
        print(self.title)
        print("\n")
        print(self.text)

    def search_for_song(self):
        """
        Allows the user to search for a song lyrics by artist and title.

        Fetches song from genius API using Song class and prints it in the
        console. If song is not found return not_found method.
        """
        artist = input("Enter the name or nickname of the artist: ")
        title = input("Enter the song title: ")
        song = Song(self.config["urls"]["song"], artist, title)
        text = song.get_text()
        if not text:
            self.not_found()
        else:
            lyrics = Lyrics(text, "song")
            self.text = lyrics
            self.title = self.text.title()
            print("\n")
            print(self.title)
            print("\n")
            print(self.text)
            self.choose_option()

    def not_found(self):
        """
        Prints an error message when a song is not found.
        """
        print("Sorry, couldn't find your song\nPress 1 to continue")
        self.get_option(1)

    def choose_paraphrase(self):
        """
        Allows the user to choose a paraphrase option.

        Calls the create_paraphrase method with the appropriate argument.
        If text attribute is empty, it prints an error message and returns to
        the main menu.
        """
        if not self.text:
            self.no_lyrics()
        print("""
        1. Switch rhymes
        2. Use synonyms
        3. Add adjectives
        4. Back to menu\n""")
        self.get_option(4)
        option = self.option
        if option == "1":
            self.create_paraphrase("rhyme")
        elif option == "2":
            self.create_paraphrase("synonym")
        elif option == "3":
            self.create_paraphrase("adjective")
        else:
            self.choose_option()

    def no_lyrics(self):
        print("There is no text to paraphrase!")
        self.choose_option()

    def choose_accuracy(self):
        """
        Allows the user to choose the accuracy level for the paraphrase.

        Returns the corresponding number of words to modify.
        """
        print("""
        1. High accuracy - low variety
        2. Medium accuracy - medium variety
        3. Low accuracy - high variety
        4. Back to words menu\n""")
        self.get_option(4)
        option = self.option
        if option == "1":
            return 1
        elif option == "2":
            return 4
        elif option == "3":
            return 10
        else:
            self.choose_words_to_modify()

    def choose_words_to_modify(self):
        """
        Allows the user to choose which words in the text to modify.

        Checks which option was chosen and returns the corresponding option.
        """
        print("""
        1. Modify last word in every verse
        2. Modify first word in every verse
        3. Modify random word in every verse
        4. Modify every word in every verse(VERY slow)
        5. Back to paraphrase menu\n""")
        self.get_option(5)
        option = self.option
        if option == "1":
            return "last"
        elif option == "2":
            return "first"
        elif option == "3":
            return "random"
        elif option == "4":
            return "all"
        else:
            self.choose_paraphrase()

    def create_paraphrase(self, form):
        """
        Creates and prints a paraphrase of the text.

        Using the Paraphrase class and according to the chosen options
        a paraphrase is generated.

        :param form: type of paraphrase to use
        :type form: str
        """
        change = self.choose_words_to_modify()
        accuracy = self.choose_accuracy()
        print("Generating paraphrase... ")
        paraphrase = Paraphrase(self.config["urls"], self.text,
                                form, change, accuracy)
        self.paraphrase = paraphrase.create_lyrics()
        self.print_text(self.paraphrase)
        self.choose_option()

    @staticmethod
    def print_text(text):
        """
        Prints text
        """
        print("\n")
        print(text)

    @staticmethod
    def end_program():
        """
        Ends the program.
        """
        sys.exit()


if __name__ == "__main__":
    UI = Interface("config.json")
    UI.start()
