import asyncio
import curses
from time import sleep


async def blink(canvas, row, column, symbol="*"):
    while True:
        canvas.addstr(row, column, symbol, curses.A_DIM)
        await asyncio.sleep(0)

        canvas.addstr(row, column, symbol)
        await asyncio.sleep(0)

        canvas.addstr(row, column, symbol, curses.A_BOLD)
        await asyncio.sleep(0)

        canvas.addstr(row, column, symbol)
        await asyncio.sleep(0)


def draw(canvas):
    curses.curs_set(False)
    canvas.border()
    canvas.refresh()

    row, column = (1, 1)

    coroutines = [blink(canvas, row, column + i) for i in range(5)]

    while True:
        if len(coroutines) == 0:
            break

        for cor in coroutines:
            try:
                _ = cor.send(None)
            except StopIteration:
                coroutines.remove(cor)

        canvas.refresh()
        sleep(1)



def main():
    curses.update_lines_cols()
    curses.wrapper(draw)
    sleep(1)


if __name__ == "__main__":
    main()
