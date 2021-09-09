import sublime
import sublime_plugin
import random as r
import datetime
import string
import os
import uuid
import logging

PACKAGES_PATH = os.path.dirname(os.path.realpath(__file__))

def get_settings():
    return sublime.load_settings('Random.sublime-settings')

"""
Base class for the Random generator. Extends the WindowCommand and adds helper methods
"""
class RandomWindow(sublime_plugin.WindowCommand):

    def default_range(self):
        """
        This should be persisted somehow
        """
        return '1,100'

    def get_range(self, input_text):
        try:
            input_text = input_text.replace(' ', '')
            start, stop = input_text.split(',')
            start = int(start)
            stop = int(stop)

            if start > stop:
                raise ValueError('Invalid format. Maybe you meant: {},{}?'.format(stop, start))

            self.insert({'start': start, 'stop': stop})
        except Exception as e:
            logging.exception(e)
            sublime.error_message('Must be two comma separated integers')

    def insert(self, kwargs):
        view = self.window.active_view()
        view.run_command(self.text_command, kwargs)

"""
Base class for the Random generator. Extends the window and adds helper methods
"""
class RandomText(sublime_plugin.TextCommand):
    def insert(self, view, generator):
        sels = self.view.sel()

        for region in sels:
            output = generator()
            self.view.insert(view, region.begin(), output)

    def get_data_file(self, filename):
        words = []
        word_file = os.path.join(PACKAGES_PATH + '/assets', filename)
        with open(word_file) as f:
            words = f.read().splitlines()
        return words

    def get_words(self):
        return self.get_data_file('words.txt')

    def get_first_names(self):
        return self.get_data_file('first_names.txt')

    def get_last_names(self):
        return self.get_data_file('last_names.txt')

    def get_countries(self):
        return self.get_data_file('countries.txt')
        
    def get_blast_first_names(self):
        return self.get_data_file('blast_first_names.txt')
        
    def get_blast_second_names(self):
        return self.get_data_file('blast_second_names.txt')
        
    def get_blast_third_names(self):
        return self.get_data_file('blast_third_names.txt')

    
        
    
"""
Window commands
"""
class RandomIntWindowCommand(RandomWindow):
    def run(self):
        self.text_command = 'random_int'
        self.window.show_input_panel('Random integer from-to',self.default_range(), self.get_range, None, None)


class RandomFloatWindowCommand(RandomWindow):
    def run(self):
        self.text_command = 'random_float'
        self.window.show_input_panel('Random float from-to',self.default_range(), self.get_range, None, None)

"""
END Window commands
"""

"""
Text commands
"""
class RandomIntCommand(RandomText):
    def generate_int(self):
        output = r.randint(self.start, self.stop)
        return str(output)

    def run(self, view, **kwargs):
        self.start = kwargs['start']
        self.stop = kwargs['stop']
        self.insert(view, self.generate_int)

class RandomFloatCommand(RandomText):

    def generate_float(self):
        output = r.uniform(self.start, self.stop)
        output = '{0:g}'.format(output)
        return str(output)

    def run(self, view, **kwargs):
        self.start = kwargs['start']
        self.stop = kwargs['stop']
        self.insert(view, self.generate_float)

class RandomLetterCommand(RandomText):

    def generate_letters(self):
        upper_range = r.randint(3, 20)
        output = ''
        for letter in range(0, upper_range):
            output += r.choice(string.ascii_letters)

        return output

    def run(self, view, **kwargs):
        self.insert(view, self.generate_letters)

class RandomLetterAndNumberCommand(RandomText):

    def generate_letters_and_numbers(self):
        upper_range = r.randint(3, 20)
        output = ''
        for letter in range(0, upper_range):
            output += r.choice(string.ascii_letters + string.digits)

        return output

    def run(self, view, **kwargs):
        self.insert(view, self.generate_letters_and_numbers)

class RandomWordCommand(RandomText):

    def generate_word(self):
        words = self.get_words()
        return r.choice(words)

    def run(self, view, **kwargs):
        self.insert(view, self.generate_word)

class RandomTextCommand(RandomText):

    def generate_text(self):
        words = self.get_words()
        return ' '.join([r.choice(words) for i in range(0,24)])

    def run(self, view, **kwargs):
        self.insert(view, self.generate_text)

class RandomUuidCommand(RandomText):

    def generate_uuid(self):
        return str(uuid.uuid4())

    def run(self, view, **kwargs):
        self.insert(view, self.generate_uuid)


class RandomFirstNameCommand(RandomText):

    def generate_first_name(self):
        first_names = self.get_first_names()
        return r.choice(first_names)

    def run(self, view, **kwargs):
        self.insert(view, self.generate_first_name)

class RandomLastNameCommand(RandomText):

    def generate_last_name(self):
        last_names  = self.get_last_names()
        return r.choice(last_names)

    def run(self, view, **kwargs):
        self.insert(view, self.generate_last_name)


class RandomFullNameCommand(RandomText):

    def generate_full_name(self):
        first_names = self.get_first_names()
        last_names  = self.get_last_names()
        return '%s %s' % (r.choice(first_names), r.choice(last_names))

    def run(self, view, **kwargs):
        self.insert(view, self.generate_full_name)


class RandomBlastNameCommand(RandomText):

    def generate_full_name(self):
        first_names = self.get_blast_first_names()
        second_names = self.get_blast_second_names()
        third_names = self.get_blast_third_names()
        return '%s %s%s' % (r.choice(first_names), r.choice(second_names),
                            r.choice(third_names))

    def run(self, view, **kwargs):
        self.insert(view, self.generate_full_name)


class RandomUrlCommand(RandomText):

    def generate_url(self):
        r_words  = [r.choice(self.get_words()) for i in range(0,7)]
        scheme   = r.choice(['http', 'https'])
        domain   = r_words[0]
        path     = '/'.join(r_words[1:3])
        query    = 'a=%s&b=%s' % (r_words[4], r_words[5])
        fragment = r_words[6]
        url      = '%s://%s.com/%s?%s#%s' % (scheme, domain, path, query, fragment)
        return url.lower()

    def run(self, view, **kwargs):
        self.insert(view, self.generate_url)

class RandomEmailCommand(RandomText):

    def generate_email(self):
        settings = get_settings()
        u_name = self.get_words()
        u_name = r.choice(u_name)
        domain = settings.get('random_email_main_domain_override',self.get_words())
        domain = r.choice(domain)
        seq = settings.get('random_email_top_level_domain_override',['com', 'net', 'edu'])
        top_domain = r.choice(seq)
        email = '%s@%s.%s' %(u_name, domain, top_domain)
        return email.lower()

    def run(self, view, **kwargs):
        self.insert(view, self.generate_email)

class RandomHexColorCommand(RandomText):

    def generate_hex_color(self):
        return '#%06x' % r.randint(0,0xFFFFFF)

    def run(self, view, **kwargs):
        self.insert(view, self.generate_hex_color)

class RandomDateCommand(RandomText):

    def generate_random_date(self):
        year = r.randint(datetime.datetime.now().year - 10, datetime.datetime.now().year + 10)
        month = r.randint(1, 12)
        day = r.randint(1, 28)
        date = datetime.date(year, month, day)
        return date.isoformat()

    def run(self, view, **kwargs):
        self.insert(view, self.generate_random_date)

class RandomTimeCommand(RandomText):

    def generate_random_time(self):
        hour = r.randint(0, 23)
        minute = r.randint(0, 59)
        second = r.randint(0, 59)
        time = datetime.time(hour, minute, second)
        return time.isoformat()

    def run(self, view, **kwargs):
        self.insert(view, self.generate_random_time)

class RandomDatetimeRfc3339Command(RandomText):

    def generate_random_datetime_rfc3339(self):
        year = r.randint(datetime.datetime.now().year - 10, datetime.datetime.now().year + 10)
        month = r.randint(1, 12)
        day = r.randint(1, 28)
        date = datetime.date(year, month, day)
        hour = r.randint(0, 23)
        minute = r.randint(0, 59)
        second = r.randint(0, 59)
        time = datetime.time(hour, minute, second)
        timezone = r.randint(0, 24) - 12
        if timezone == 0:
            return "%sT%sZ" % (date.isoformat(), time.isoformat())
        return "%sT%s%+03d:00" % (date.isoformat(), time.isoformat(), timezone)

    def run(self, view, **kwargs):
        self.insert(view, self.generate_random_datetime_rfc3339)

class RandomIpv4AddressCommand(RandomText):
    def generate_ipv4_address(self):
        return "%s.%s.%s.%s" % (r.randint(0,255), r.randint(0,255), r.randint(0,255), r.randint(0,255))

    def run(self, view, **kwargs):
        self.insert(view, self.generate_ipv4_address)

class RandomIpv6AddressCommand(RandomText):
    def generate_hexbyte(self):
        choice = "0123456789ABCDEF"
        return "%s%s" % (r.choice(choice), r.choice(choice))

    def generate_ipv6_address(self):
        address = ""
        for x in range(0,8):
            address += self.generate_hexbyte()
            address += self.generate_hexbyte()
            if x < 7:
                address += ":"
        return address

    def run(self, view, **kwargs):
        self.insert(view, self.generate_ipv6_address)

class RandomCountryCommand(RandomText):

    def generate_country(self):
        countries = self.get_countries()
        return r.choice(countries)

    def run(self, view, **kwargs):
        self.insert(view, self.generate_country)

"""
END Text commands
"""
