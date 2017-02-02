PUBLIC_TEAMS_URL = 'https://hackbulgaria.com/hackfmi/api/public-teams/'
MENTORS_URL = 'https://hackbulgaria.com/hackfmi/api/mentors/'
TECHNOLOGIES_URL = 'https://hackbulgaria.com/hackfmi/api/skills/'


class Error(Exception):
    pass


class InvalidMentor(Error):
    pass
