#!/usr/bin/env python3

from simple_term_menu import TerminalMenu


def main():
    terminal_menu = TerminalMenu(
        ["dog", "cat", "mouse", "squirrel"],
        multi_select=True,
        show_multi_select_hint=True,
    )
    menu_entry_indices = terminal_menu.show()
    print(menu_entry_indices)
    print(terminal_menu.chosen_menu_entries)


if __name__ == "__main__":
    main()