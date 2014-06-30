import sublime, sublime_plugin, random, string, os

'''
Base class for the Random generator. Extends the WindowCommand and adds helper methods
'''
class RandomWindow(sublime_plugin.WindowCommand):

    def get_range(self, input):
        try:
            start, stop = input.split('-')
            start = int(start)
            stop = int(stop)
            self.insert({'start': start, 'stop': stop})
        except:
            sublime.error_message('Must be two integers, separated by: - ')

    def insert(self, kwargs):
        view = self.window.active_view()
        view.run_command(self.text_command, kwargs)

'''
Base class for the Random generator. Extends the window and adds helper methods
'''
class RandomText(sublime_plugin.TextCommand):
    def insert(self, view, generator):
        sels = self.view.sel()

        for region in sels:
            output = generator()
            self.view.insert(view, region.begin(), output)

'''
Window commands
'''
class RandomIntWindowCommand(RandomWindow):
    def run(self):
        self.text_command = 'random_int'
        self.window.show_input_panel('Random integer from-to','1-100', self.get_range, None, None)


class RandomFloatWindowCommand(RandomWindow):
    def run(self):
        self.text_command = 'random_float'
        self.window.show_input_panel('Random float from-to','1-100', self.get_range, None, None)

'''
END Window commands
'''

'''
Text commands
'''
class RandomIntCommand(RandomText):
    def generate_int(self):
        output = random.randint(self.start, self.stop)
        return str(output)

    def run(self, view, **kwargs):
        self.start = kwargs['start']
        self.stop = kwargs['stop']
        self.insert(view, self.generate_int)

class RandomFloatCommand(RandomText):

    def generate_float(self):
        output = random.uniform(self.start, self.stop)
        output = '{0:g}'.format(output)
        return str(output)

    def run(self, view, **kwargs):
        self.start = kwargs['start']
        self.stop = kwargs['stop']
        self.insert(view, self.generate_float)

class RandomLetterCommand(RandomText):

    def generate_letters(self):
        upper_range = random.randint(3, 20)
        output = ''
        for letter in range(0, upper_range):
            output += random.choice(string.ascii_letters)

        return output


    def run(self, view, **kwargs):
        self.insert(view, self.generate_letters)


class RandomLetterAndNumberCommand(RandomText):

    def generate_letters_and_numbers(self):
        upper_range = random.randint(3, 20)
        output = ''
        for letter in range(0, upper_range):
            output += random.choice(string.ascii_letters + string.digits)

        return output


    def run(self, view, **kwargs):
        self.insert(view, self.generate_letters_and_numbers)

class RandomWordCommand(RandomText):

    def generate_word(self):
        words = []
        word_file = os.path.join(sublime.packages_path(), "Random Everything", "words.txt")
        with open(word_file) as f:
            words = f.read().splitlines()

        return random.choice(words)


    def run(self, view, **kwargs):
        self.insert(view, self.generate_word)

'''
END Text commands
'''
