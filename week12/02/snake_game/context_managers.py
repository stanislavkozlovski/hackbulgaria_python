from datetime import datetime
from contextlib import contextmanager


@contextmanager
def error_logger():
    with open('game_errors.txt', 'a') as g_errors:
        yield g_errors
        g_errors.write(f'\tat {datetime.now()}\n\n')


@contextmanager
def step_logger():
    with open('snake_steps.txt', 'a') as step_loggr:
        yield step_loggr
        step_loggr.write(f'\tat {datetime.now()}\n\n')


@contextmanager
def food_logger():
    with open('snake_meals.txt', 'a') as food_loggr:
        yield food_loggr
        food_loggr.write(f'\tat {datetime.now()}\n\n')


