import asyncio
from typing import List

from itertools import cycle

from curses_tools import draw_frame, get_frame_size, read_controls


async def animate_spaceship(
    canvas,
    start_row: int,
    start_column: int,
    border_limit_rows_top: int,
    border_limit_rows_bottom: int,
    border_limit_columns_left: int,
    border_limit_columns_right: int,
    animations: List[str]
):
    animations_cycle = cycle(animations)

    row_shift = 0
    column_shift = 0

    while True:
        rows_direction, columns_direction, _ = read_controls(canvas)
        row_shift += rows_direction
        column_shift += columns_direction

        filename, frame = next(animations_cycle)
        frame_height, frame_width = get_frame_size(frame)

        frame_top_row = start_row + row_shift
        frame_bottom_row = frame_top_row + frame_height
        frame_left_column = start_column + column_shift
        frame_right_column = frame_left_column + frame_width

        # print(
        #     '\t'.join([
        #     str(('frame_top_row', frame_top_row)),
        #     str(('frame_bottom_row  ', frame_bottom_row)),
        #     str(('frame_left_column  ', frame_left_column)),
        #     str(('frame_right_column  ', frame_right_column))
        # ])
        # )
        canvas.addstr(2, 3, str(('frame_top_row', frame_top_row)) )
        canvas.addstr(3, 3, str(('frame_bottom_row  ', frame_bottom_row)) )
        canvas.addstr(4, 3, str(('frame_left_column  ', frame_left_column)) )
        canvas.addstr(5, 3, str(('frame_right_column  ', frame_right_column)) )
        canvas.addstr(6, 3, str(('row_shift  ', row_shift)))
        canvas.addstr(7, 3, str(('column_shift  ', column_shift)))
        canvas.addstr(8, 3, str((filename, 'w', frame_width)))
        canvas.addstr(9, 3, str((filename, 'h', frame_height)))
        # canvas.addstr(10, 3, str(('border_limit_rows  ', border_limit_rows)))
        # canvas.addstr(11, 3, str(('border_limit_columns  ', border_limit_columns)))

        # print('frame_top_row  ', frame_top_row)
        # print('frame_bottom_row  ', frame_bottom_row)
        # print('frame_left_column  ', frame_left_column)
        # print('frame_right_column  ', frame_right_column)

        spaceship_center_row = frame_top_row - int(frame_height / 2)
        spaceship_center_column = frame_left_column - int(frame_width / 2)


        draw_frame(canvas, spaceship_center_row, spaceship_center_column, frame)
        canvas.refresh()
        for i in range(2):
            await asyncio.sleep(0)
        draw_frame(canvas, spaceship_center_row, spaceship_center_column, frame,
                   negative=True)
        canvas.refresh()
