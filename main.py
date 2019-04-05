import curses
from time import sleep


def draw(canvas):
    curses.curs_set(False)
    canvas.border()
    canvas.refresh()

    row, column = (5, 20)
    symbol = "*"

    while True:
        canvas.addstr(row, column, symbol, curses.A_DIM)
        canvas.refresh()
        sleep(2)

        canvas.addstr(row, column, symbol)
        canvas.refresh()
        sleep(0.3)

        canvas.addstr(row, column, symbol, curses.A_BOLD)
        canvas.refresh()
        sleep(2)

        canvas.addstr(row, column, symbol)
        canvas.refresh()
        sleep(0.3)


def main():
    curses.update_lines_cols()
    curses.wrapper(draw)
    sleep(3)


if __name__ == "__main__":
    main()
