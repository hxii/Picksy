import curses
import re
from typing import Union


class Picksy:

    __options = None
    __filtered_options = None
    __filter = ""
    __current_selection = 1
    __screen = None
    __message = None

    def __init__(self, options: Union[list, dict], message: str = ""):
        """Picksy. Python picker module with a simple search.

        Args:
            options (Union[list, dict]): A dictionary of options the user can choose from. {'id': 'text'}
            message (str, optional): Header message to show above menu. Defaults to "".
        """
        if options:
            if type(options) == list:
                self.__options = self.__convert_list(options)
            else:
                self.__options = options
            self.__filtered_options = self.__options
            self.__screen = curses.initscr()
            self.__message = message
            curses.wrapper(self.main)

    def __convert_list(self, list_to_convert: list) -> dict:
        """Convert a list into a dictionary following {'item': 'item'}

        Args:
            list_to_convert (list): The list we want to convert to a dict

        Returns:
            dict: Dictionary
        """
        dictionary = {}
        for item in list_to_convert:
            dictionary[item] = item
        return dictionary

    def get_choice(self) -> Union[str, bool]:
        """Get selected menu choice.

        Returns:
            Union[str, bool]: The selected choice if available, False otherwise
        """
        if self.__current_selection and len(self.__filtered_options.keys()) > 0:
            return list(self.__filtered_options.keys())[self.__current_selection - 1]
        else:
            return False

    def main(self, stdscr):
        try:
            curses.start_color()
            curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
            stdscr.keypad(True)
            self.__print_options(stdscr)
            while True:
                key = stdscr.getkey()
                if key == "KEY_UP":
                    self.__move_selection_up()
                elif key == "KEY_DOWN":
                    self.__move_selection_down()
                elif ord(key) == 10:
                    return
                else:
                    self.__filter_options(key)
                stdscr.clear()
                self.__print_options(stdscr)
                stdscr.refresh()
        except KeyboardInterrupt:
            self.__current_selection = False
            return False

    def __print_options(self, stdscr):
        """Print each option in the list

        Args:
            stdscr (_type_): curses screen
        """
        self.__screen.addstr(f"{self.__message}")
        for index, option in enumerate(self.__filtered_options.keys(), 1):
            if self.__current_selection == index:
                self.__highlight(f"{index}. {self.__filtered_options[option]}")
            else:
                stdscr.addstr(f"{index}. {self.__filtered_options[option]}\n")
        stdscr.addstr(f"Search: {self.__filter}")

    def __reset_current_selection(self):
        """Make sure the selection is always reset when the filter string changes"""
        self.__current_selection = 1

    def __move_selection_down(self):
        """Move selection down"""
        if self.__current_selection == len(self.__filtered_options):
            self.__current_selection = 1
        else:
            self.__current_selection += 1

    def __move_selection_up(self):
        """Move selection up"""
        if self.__current_selection == 1:
            self.__current_selection = len(self.__filtered_options)
        else:
            self.__current_selection -= 1

    def __filter_options(self, key: str):
        """Filter the list of available options based on regex i.e. .*word.*

        Args:
            f (str): key passed from curses
        """
        if ord(key) == 127:  # Detect backspace and make it work as intended
            self.__filter = (
                self.__filter[:-1] if len(self.__filter) > 0 else self.__filter
            )
        else:
            self.__filter = self.__filter + key
        self.__filtered_options = dict(
            filter(
                lambda item: re.match(rf"^.*{re.escape(self.__filter)}.*", item[1]),
                self.__options.items(),
            )
        )
        self.__reset_current_selection()

    def __highlight(self, text: str):
        """Highlight currently selected item in list

        Args:
            text (str): The text of the item to highlight
        """
        self.__screen.attron(curses.color_pair(1))
        self.__screen.addstr(f"{text}\n")
        self.__screen.attroff(curses.color_pair(1))
