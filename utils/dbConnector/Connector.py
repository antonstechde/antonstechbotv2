import psycopg2


class Connector:
    def __init__(self, host: str, user: str, database: str, password: str, port: str):
        self.host = host
        self.user = user
        self.database = database
        self.password = password
        self.port = port

        self.connection: psycopg2 = None

    def connect(self):
        self.connection = psycopg2.connect(
            host=self.host,
            user=self.user,
            database=self.database,
            password=self.password,
            port=self.port
        )

    def get_new_cursor(self):
        return self.connection.cursor()
