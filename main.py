import curses
from time import sleep


def draw_symbol_and_sleep(canvas, row, column, symbol, state=0, sleep_time=0.00):
    canvas.addstr(row, column, symbol, state)
    canvas.refresh()
    sleep(sleep_time)


def draw_background(canvas):
    curses.curs_set(False)
    canvas.border()
    canvas.refresh()

def draw_background_animations(canvas):
    row, column = (5, 20)
    symbol = "*"

    while True:
        draw_symbol_and_sleep(canvas, row, column, symbol, curses.A_DIM, 2)
        draw_symbol_and_sleep(canvas, row, column, symbol, sleep_time=0.3)
        draw_symbol_and_sleep(canvas, row, column, symbol, curses.A_BOLD, sleep_time=2)
        draw_symbol_and_sleep(canvas, row, column, symbol, sleep_time=0.3)


def main():
    curses.update_lines_cols()
    curses.wrapper(draw_background)
    curses.wrapper(draw_background_animations)


if __name__ == "__main__":
    main()

