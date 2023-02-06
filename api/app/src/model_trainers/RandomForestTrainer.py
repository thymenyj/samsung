from logging import error, info
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
        try:
            visitors_dataframe = self._get_visitors_dataframe()
            X_train, X_test, y_train, y_test = train_test_split(
                visitors_dataframe.drop(columns=["positive_revenue"]),
                visitors_dataframe["positive_revenue"],
                test_size = 0.2,
                random_state=1
            )

            random_forest = RandomForestClassifier(n_estimators=100, n_jobs=20, random_state=2, verbose=True)

            info("Start training random forest.")
            random_forest.fit(X_train, y_train.values.ravel())

            info("Start evaluating random forest.")
            self._evalute_random_forest(random_forest, X_test, y_test)

            feature_labels = visitors_dataframe.drop(columns=["positive_revenue"]).columns
            self._calculate_feature_importance(random_forest, feature_labels)

            self._save_random_forest(random_forest)

        except Exception as exc:
            error(f"Failed to train random forest. --> {exc}")

    def _get_visitors_dataframe(self):
        try:
            sql_query = text("SELECT * FROM visitors")

            with self._analytics_database.engine.connect() as connection:
                visitors_data = connection.execute(sql_query).fetchall()
                visitors_dataframe = DataFrame(visitors_data)

                return visitors_dataframe

        except Exception as exc:
            error(f"Failed to get visitors dataframe. --> {exc}")

    def _evalute_random_forest(self, random_forest, X_test, y_test):
        try:
            prediction = random_forest.predict(X_test)
            matrix = confusion_matrix(y_test, prediction)
            accuracy = accuracy_score(y_test, prediction)
            f1 = f1_score(y_test, prediction)
            
            print(f"accuracy: {accuracy}")
            print(f"f1_score: {f1}")
            print("Confusion Matrix")
            print(matrix)
        
        except Exception as exc:
            error(f"Failed to evaluate random forest. --> {exc}")

    def _calculate_feature_importance(self, random_forest, feature_labels):
        try:
            importances = random_forest.feature_importances_
            sorted_indices = argsort(importances)[::-1]

            print("Feature Importance Top 20")
            for f in range(20):
                print("%2d) %-*s %f" % (
                    f + 1, 30,
                    feature_labels[sorted_indices[f]],
                    importances[sorted_indices[f]])
                )

        except Exception as exc:
            error(f"Failed to calculate feature importance. {exc}")

    def _save_random_forest(self, random_forest):
        try:
            dump(random_forest, open("/app/ml_models/random_forest.pkl", 'wb'))

            info("Saved random forest successfully!")

        except Exception as exc:
            error(f"Failed to save random forest. --> {exc}")
