from models.cinema import Cinema
from models.ticket import Ticket
from settings.utils import get_free_spots_for_a_projection, get_free_spot_count_for_a_projection, print_movie_hall
from settings.decorators import authenticate, authenticate_user
from settings.validator import is_valid_ticket_count, is_valid_row_or_col
from settings.constants import (DB_ID_KEY, DB_PROJECTIONS_DATE_KEY, DB_PROJECTIONS_HOUR_KEY,
                                DB_MOVIE_NAME_KEY, DB_PROJECTIONS_MOVIE_TYPE_KEY)
from controllers.projections import get_movie_projections, show_movie_projections
from controllers.movie import show_movies
from queries.inserter import create_reservations
from queries.loader import get_movie_by_id
from queries.deleter import delete_reservations_from_user


@authenticate
def make_reservation(cinema: Cinema):
    print('Choose the amount of tickets you want:')
    ticket_count = input(">Ticket count: ")
    while not is_valid_ticket_count(ticket_count):
        print('Invalid ticket count! The ticket count should be between 1-10 inclusive.')
        ticket_count = input(">Ticket count: ")
    ticket_count = int(ticket_count)

    # show the movies and let the user choose one
    movie, to_give_up = movie_choice_prompt()
    if to_give_up:
        return
    movie_id = movie[DB_ID_KEY]
    # show the projections for the movie
    movie, projections = get_movie_projections(movie_id)
    if len(projections) == 0:
        print('There are no projections for that movie, we apologize for the inconvenience.')
        return

    # let the user choose a projection and get the movie hall (seats) for the projection
    projection, movie_hall, to_give_up = projection_choice_prompt(movie, projections, ticket_count)
    if to_give_up:
        return

    tickets, to_give_up = ticket_choice_prompt(cinema, movie, projection, movie_hall, ticket_count)
    if to_give_up:
        return

    # finalize order
    print(
        'You have chosen to create {reservation_count} reservations for the movie {movie_name} on {date}{time}'.format(
            reservation_count=ticket_count, movie_name=movie[DB_MOVIE_NAME_KEY],
            date=projection[DB_PROJECTIONS_DATE_KEY], time=projection[DB_PROJECTIONS_HOUR_KEY]
        ))
    for idx, ticket in tickets.items():
        print("#{} {}".format(str(idx), ticket))

    choice = input('Do you confirm your order? (y/n): ')
    if choice in ['y', 'Y', 'yes', 'YES', 'Yes']:
        create_reservations(tickets.values())


def projection_choice_prompt(movie, projections: list, ticket_count: int):
    """
    This function presents the user with the available projections for the given movie and lets him choose
    the one he wants to make a reservation for.
    :param movie: A sqlite3 row object for a Movie from the DB tables movies
    :param projections: A list ot sqlite3 row objects for projections from the DB table projections
    :param ticket_count: The number of tickets the user wants to buy
    :return:
            the projection,
            the movie hall for the given projection,
            a boolean indicating if he has given up on his choice
    """
    to_give_up = False
    projections_by_id = {str(projection[DB_ID_KEY]): projection for projection in projections}
    while True:
        show_movie_projections(movie, projections)
        projection_id = input(">Choose a projection: ")
        if projection_id == 'give up':
            to_give_up = True
            return None, None, to_give_up
        if projection_id in projections_by_id:
            # see if there are enough free spots
            free_spots_count = get_free_spot_count_for_a_projection(projection_id)

            if free_spots_count < ticket_count:
                print('There are not enough free spots for {} tickets!'.format(ticket_count))
                print('Please choose another projection')
                continue

            break
        print('Invalid projection id!')
    projection = projections_by_id[projection_id]
    movie_hall = get_free_spots_for_a_projection(projection_id)
    return projection, movie_hall, to_give_up


def movie_choice_prompt():
    """
    Shows the movies to the user and prompts him for a choice using the movie's id
    """
    to_give_up = False
    show_movies()
    movie_id = input(">Choose a movie: ")
    movie = get_movie_by_id(movie_id)
    while not movie:
        print("Invalid movie id!")
        movie_id = input(">Choose a movie: ")
        if movie_id == "give up":
            to_give_up = True
            break
        movie = get_movie_by_id(movie_id)

    return movie, to_give_up


def ticket_choice_prompt(cinema, movie, projection, movie_hall, ticket_count: int):
    """
    Prompt the user to choose the seats for each ticket he wants to buy
    :param cinema: An object of class Cinema
    :param movie: A sqlite3 Row object for a movie from the Movie DB table
    :param projection: A sqlite3 Row object for a projection from the Projections DB table
    :param movie_hall: A 11x11 matrix representing the free seats in the movie hall
    :param ticket_count: The count of tickets the user wants to buy
    :return: A dictionary type: {ticket_idx:a Ticket object}
    """
    to_give_up = False
    tickets = {}  # type: {int:Ticket}
    for i in range(ticket_count):
        # loop until the user chooses a valid ticket
        while True:
            print("Please pick a spot for ticket #{}".format(i + 1))
            print_movie_hall(movie_hall)

            # Get the row/col for a seat and validate them
            row = input("Choose a row: (1-10): ")
            while not is_valid_row_or_col(row):
                if row == 'give up':
                    to_give_up = True
                    return None, to_give_up
                print('The row you entered is invalid.')
                row = input("Choose a row: (1-10): ")
            row = int(row)

            col = input("Choose a cow: (1-10): ")
            while not is_valid_row_or_col(col):
                if col == 'give up':
                    to_give_up = True
                    return None, to_give_up
                print('The col you entered is invalid.')
                col = input("Choose a col: (1-10): ")
            col = int(col)

            if movie_hall[row][col] == 'X':
                print('The spot you chose is taken!')
            else:
                # take the seat and add the ticket
                movie_hall[row][col] = 'X'
                ticket = Ticket(row, col, movie_name=movie[DB_MOVIE_NAME_KEY], projection_id=projection[DB_ID_KEY],
                                proj_type=projection[DB_PROJECTIONS_MOVIE_TYPE_KEY],
                                date=projection[DB_PROJECTIONS_DATE_KEY], hour=projection[DB_PROJECTIONS_HOUR_KEY],
                                owner_id=cinema.user[DB_ID_KEY])
                tickets[i + 1] = ticket
                break

    return tickets, to_give_up


@authenticate_user
def cancel_reservation(cinema: Cinema, username: str):
    user = cinema.user
    delete_reservations_from_user(user[DB_ID_KEY])
    print('You have successfully cancelled all your reservations!')