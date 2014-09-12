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

    def get_data_file(self, filename):
        words = []
        word_file = os.path.join(sublime.packages_path(), "Random Everything", filename)
        with open(word_file) as f:
            words = f.read().splitlines()
        return words

    def get_words(self):
        return self.get_data_file("words.txt")

    def get_first_names(self):
        return self.get_data_file("first_names.txt")

    def get_last_names(self):
        return self.get_data_file("last_names.txt")

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
        words = self.get_words()
        return random.choice(words)

    def run(self, view, **kwargs):
        self.insert(view, self.generate_word)


class RandomTextCommand(RandomText):

    def generate_text(self):
        words = self.get_words()
        return " ".join([random.choice(words) for i in range(0,24)])

    def run(self, view, **kwargs):
        self.insert(view, self.generate_text)


class RandomFirstNameCommand(RandomText):

    def generate_first_name(self):
        first_names = self.get_first_names()
        return random.choice(first_names)

    def run(self, view, **kwargs):
        self.insert(view, self.generate_first_name)


class RandomLastNameCommand(RandomText):

    def generate_last_name(self):
        last_names  = self.get_last_names()
        return random.choice(last_names)

    def run(self, view, **kwargs):
        self.insert(view, self.generate_last_name)


class RandomFullNameCommand(RandomText):

    def generate_full_name(self):
        first_names = self.get_first_names()
        last_names  = self.get_last_names()
        return "%s %s" % (random.choice(first_names), random.choice(last_names))

    def run(self, view, **kwargs):
        self.insert(view, self.generate_full_name)


class RandomUrlCommand(RandomText):

    def generate_url(self):
        r_words  = [random.choice(self.get_words()) for i in range(0,7)]
        scheme   = random.choice(['http', 'https'])
        domain   = r_words[0]
        path     = "/".join(r_words[1:3])
        query    = "a=%s&b=%s" % (r_words[4], r_words[5])
        fragment = r_words[6]
        url      = "%s://%s.com/%s?%s#%s" % (scheme, domain, path, query, fragment)
        return url.lower()

    def run(self, view, **kwargs):
        self.insert(view, self.generate_url)

'''
END Text commands
'''
