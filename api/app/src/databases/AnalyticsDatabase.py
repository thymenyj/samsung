from sqlalchemy import create_engine


class AnalyticsDatabase:
    
    def __init__(self, connection_string):
        self.engine = create_engine(connection_string)
