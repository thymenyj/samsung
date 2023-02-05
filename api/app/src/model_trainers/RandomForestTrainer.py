from sqlalchemy import text
from pandas import DataFrame


class RandomForestTrainer:
    
    def __init__(self, analytics_database):
        self._analytics_database = analytics_database
        
    def train(self):
        visitors_dataframe = self._get_visitors_dataframe()
        print(visitors_dataframe.iloc[:10])
    
    def _get_visitors_dataframe(self):
        try:
            sql_query = text("SELECT * FROM visitors")

            with self._analytics_database.engine.connect() as connection:
                visitors_data = connection.execute(sql_query).fetchall()
                visitors_dataframe = DataFrame(visitors_data)
                
                return visitors_dataframe
        
        except Exception as exc:
            print(exc)
            return