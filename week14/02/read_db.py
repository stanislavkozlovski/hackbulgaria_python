from model import Server, session

def calculate_server_occurences():
    web_servers = session.query(Server).all()

    server_occurences = {}
    for server in web_servers:
        if '/' in server.server_name:
            server_name = server.server_name[:server.server_name.index('/')]
        else:
            server_name = server.server_name
        if server_name not in server_occurences:
            server_occurences[server_name] = 0
        server_occurences[server_name] += server.occurences

    return server_occurences