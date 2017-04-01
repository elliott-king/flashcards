# import argparse
import textwrap
import os
import random
import yaml


MAX_WIDTH = 70
MIN_CONTENT_HEIGHT = 6
BORDER = '*'


class Flashcard:
    """Representation of a flashcard.

    It has two states, which are handled by the variable hide_content, as the name suggests,
    it will display a message in the placeholder of the content, telling the user to press a key
    to continue, and next, it will show the content.
    """

    def __init__(self, topic, content, keywords=None, max_card_width=MAX_WIDTH,
                 min_content_height=MIN_CONTENT_HEIGHT):
        self.max_card_width = max_card_width
        self.min_content_height = min_content_height
        self.topic = topic
        self.content = content
        self.keywords = keywords
        self.hide_content = True

    def format_data(self, line, max_length):
        """Processes raw data.

        :param line: contains the raw data which may include tabs, new lines, etc.
        :type line: str
        :param max_length: max length of each element of the array generated.
        :type max_length: int
        :returns: formated data.
        :rtype: list
        """

        line = ' '.join(line.split())
        words_in_line = line.replace('\n', ' ').replace('\t', ' ')

        return textwrap.wrap(words_in_line, max_length - 5)

    def style_on_line(self, line, max_length, border=BORDER):
        """Add border and center a given line.

        :param line: the pre formatted string.
        :type line: str
        :param max_length: used to calculate extra whitespaces and borders.
        :type max_length: int
        :param border: representation of the border.
        :type border: str

        :returns: styled string
        :rtype: str
        """

        return line.center(max_length - 2, ' ').center(max_length, border)

    def clean(self):
        """Clear the terminal on which the flashcard is gonna be displayed."""

        if os.name == 'posix':
            os.system('clear')
        else:
            os.system('cls')

    def get_topic(self):
        """Generate the topic lines ready to be displayed.

        :returns: lines ready to be shown.
        :rtype: list
        """

        topic_lines = ['']
        topic_lines += self.format_data(self.topic, self.max_card_width)
        topic_lines += ['']
        return [self.style_on_line(l, self.max_card_width) for l in topic_lines]

    def get_content(self):
        """Generate the content lines ready to be displayed.

        :returns: lines ready to be shown.
        :rtype: list
        """

        content_lines = ['']
        formatted_content = self.format_data(self.content, self.max_card_width)

        if self.hide_content:
            initial_content = 'Press [Enter] to show content'
            content_lines += self.format_data(initial_content, self.max_card_width)
        else:
            content_lines += formatted_content

        content_lines += ['']

        current_height = len(content_lines)
        expected_height = len(formatted_content)
        min_height = self.min_content_height
        height = 0
        if expected_height > min_height:
            height = expected_height
        else:
            height = min_height

        if current_height > height:
            height = current_height

        content_lines += [''] * (height - current_height)

        return [self.style_on_line(l, self.max_card_width) for l in content_lines]

    def get_keywords(self):
        """Generate the keywords lines ready to be displayed.

        :returns: lines ready to be shown.
        :rtype: list
        """

        topic_lines = ['']
        topic_lines += self.format_data(self.keywords, self.max_card_width)
        topic_lines += ['']
        return [self.style_on_line(l, self.max_card_width) for l in topic_lines]

    def get_lines_to_draw(self, border=BORDER):
        """Central connection where all the lines generated are unified.

        :returns: lines to be shown
        :rtype: list
        """

        lines = ['\n']  # starts with a new line

        # generate border line
        horizontal_border = border * self.max_card_width

        lines.append(horizontal_border)

        lines += self.get_topic()

        lines.append(horizontal_border)
        lines.append(horizontal_border)

        lines += self.get_content()

        if self.keywords:
            lines.append(horizontal_border)
            lines.append(horizontal_border)
            lines += self.get_keywords()

        lines.append(horizontal_border)
        return lines

    def draw(self):
        """Draw the generated lines."""
        lines = self.get_lines_to_draw()
        for line in lines:
            print(line)

        self.hide_content = not self.hide_content

    def run(self):
        """Execute the flashcard.

        It will transition between this states:
        1) Content is hidden and will request the user to press a key to continue.
        2) Content is shown.
        """
        self.clean()
        self.draw()


def run_flashcards(flashcards, ordered):
    if not ordered:
        random.shuffle(flashcards)
    for fc in flashcards:
        for _ in range(2):
            fc.run()
            input()


def start(args):
    # args = get_arguments()
    file_name = args.file_name
    ordered = args.ordered

    flashcards = []

    with open(file_name) as stream:
        # no exception handling here, let yaml exceptions do their job
        parsed_file = yaml.load(stream)
        for data in parsed_file:
            fc = Flashcard(**data)
            flashcards.append(fc)
    run_flashcards(flashcards, ordered)