from pickle import dump
from sqlalchemy import text
from pandas import DataFrame
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
        
from sklearn.metrics import confusion_matrix, f1_score, accuracy_score
from numpy import argsort


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

        random_forest = RandomForestClassifier(n_estimators=100, n_jobs=20, random_state=2, verbose=True)

        print("Start training random forest...")
        random_forest.fit(X_train, y_train.values.ravel())

        print("Evaluating random forest...")
        prediction = random_forest.predict(X_test)
        matrix = confusion_matrix(y_test, prediction)
        accuracy = accuracy_score(y_test, prediction)
        f1 = f1_score(y_test, prediction)
        print(f"accuracy: {accuracy}")
        print(f"f1_score: {f1}")
        print(matrix)

        importances = random_forest.feature_importances_
        sorted_indices = argsort(importances)[::-1]
        feat_labels = visitors_dataframe.drop(columns=["positive_revenue"]).columns

        for f in range(X_train.shape[1]):
            print("%2d) %-*s %f" % (f + 1, 30,
                                    feat_labels[sorted_indices[f]],
                                    importances[sorted_indices[f]]))
            
        dump(random_forest, open("/app/models/random_forest.pkl", 'wb'))
        print("Saved Random Forest")

    def _get_visitors_dataframe(self):
        try:
            sql_query = text("SELECT * FROM visitors")

            with self._analytics_database.engine.connect() as connection:
                visitors_data = connection.execute(sql_query).fetchall()
                visitors_dataframe = DataFrame(visitors_data)
                print(visitors_dataframe.iloc[:10])
                return visitors_dataframe
        
        except Exception as exc:
            print(exc)
            return