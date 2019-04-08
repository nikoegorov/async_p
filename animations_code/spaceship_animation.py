import asyncio
from typing import List

from itertools import cycle

from curses_tools import draw_frame, get_frame_size, read_controls


async def animate_spaceship(
    canvas,
    start_row: int,
    start_column: int,
    border_limit_top: int,
    border_limit_bottom: int,
    border_limit_left: int,
    border_limit_right: int,
    animations: List[str]
):
    animations_cycle = cycle(animations)

    row_shift = 0
    column_shift = 0

    while True:
        # rows_direction, columns_direction, _ = read_controls(canvas)
        #
        # filename, frame = next(animations_cycle)
        # frame_height, frame_width = get_frame_size(frame)
        #
        # shift_frame_rows_to_center = -int(frame_height / 2)
        # shift_frame_columns_to_center = -int(frame_width / 2)
        #
        # old_frame_top_row = start_row + row_shift
        # old_frame_left_column = start_column + column_shift
        #
        # new_position_top_row = old_frame_top_row + rows_direction
        # new_position_left_column = old_frame_left_column + columns_direction
        #
        # new_frame_top_row = new_position_top_row + shift_frame_rows_to_center
        # new_frame_bottom_row = new_position_top_row - shift_frame_rows_to_center
        #
        # new_frame_left_column = new_position_left_column + shift_frame_columns_to_center
        # new_frame_right_column = new_position_left_column - shift_frame_columns_to_center
        #
        # if new_frame_top_row < border_limit_top:
        #     rows_direction = 0
        #
        # if new_frame_bottom_row > border_limit_bottom:
        #     rows_direction = 0
        #
        # if new_frame_left_column < border_limit_left:
        #     columns_direction = 0
        #
        # if new_frame_right_column > border_limit_right:
        #     columns_direction = 0
        #
        # row_shift += rows_direction
        # column_shift += columns_direction
        #
        # spaceship_center_row = start_row + row_shift + shift_frame_rows_to_center
        # spaceship_center_column = start_column + column_shift + shift_frame_columns_to_center
        #
        # draw_frame(canvas, spaceship_center_row, spaceship_center_column, frame)
        # canvas.refresh()
        # for i in range(2):
        #     await asyncio.sleep(0)
        # draw_frame(canvas, spaceship_center_row, spaceship_center_column, frame,
        #            negative=True)
        # canvas.refresh()


        rows_direction, columns_direction, _ = read_controls(canvas)

        filename, frame = next(animations_cycle)
        frame_height, frame_width = get_frame_size(frame)

        frame_center_rows = int(frame_height / 2)
        frame_center_columns = int(frame_width / 2)

        old_frame_top_row = start_row + row_shift
        new_frame_top_row = old_frame_top_row + rows_direction
        new_frame_bottom_row = new_frame_top_row + frame_height

        if any([
            new_frame_top_row < border_limit_top + frame_center_rows,
            new_frame_bottom_row > border_limit_bottom + frame_center_rows,
        ]):
            rows_direction = 0

        old_frame_left_column = start_column + column_shift
        new_frame_left_column = old_frame_left_column + columns_direction
        new_frame_right_column = new_frame_left_column + frame_width

        if any([
            new_frame_left_column < border_limit_left + frame_center_columns,
            new_frame_right_column > border_limit_right + frame_center_columns,
        ]):
            columns_direction = 0

        new_frame_top_row = old_frame_top_row + rows_direction
        new_frame_left_column = old_frame_left_column + columns_direction

        ship_center_position_row = new_frame_top_row - frame_center_rows
        ship_center_position_column = new_frame_left_column - frame_center_columns

        draw_frame(canvas, ship_center_position_row, ship_center_position_column, frame)
        canvas.refresh()
        for i in range(2):
            await asyncio.sleep(0)
        draw_frame(canvas, ship_center_position_row, ship_center_position_column, frame,
                   negative=True)
        canvas.refresh()

        row_shift += rows_direction
        column_shift += columns_direction