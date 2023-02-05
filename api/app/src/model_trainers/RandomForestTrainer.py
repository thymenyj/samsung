from sqlalchemy import text
from pandas import DataFrame
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
        
from sklearn.metrics import confusion_matrix, f1_score, accuracy_score
class RandomForestTrainer:
    
    def __init__(self, analytics_database):
        self._analytics_database = analytics_database
        
    def train(self):
        visitors_dataframe = self._get_visitors_dataframe()
        X_train, X_test, y_train, y_test = train_test_split(
            visitors_dataframe.drop(columns=["positive_revenue"]),
            visitors_dataframe["positive_revenue"],
            test_size = 0.2,
            random_state=1
        )

        forest = RandomForestClassifier(n_estimators=100, n_jobs=20, random_state=2, verbose=True)
        
        print("Start training random forest...")
        forest.fit(X_train, y_train.values.ravel())
        
        print("Evaluating random forest...")
        prediction = forest.predict(X_test)
        matrix = confusion_matrix(y_test, prediction)
        accuracy = accuracy_score(y_test, prediction)
        f1 = f1_score(y_test, prediction)
        print(f"accuracy: {accuracy}")
        print(f"f1_score: {f1}")
        print(matrix)

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