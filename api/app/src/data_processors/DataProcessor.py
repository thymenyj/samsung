from logging import error, info
from pandas import DataFrame, read_pickle, concat
from kaggle.api.kaggle_api_extended import KaggleApi
from zipfile import ZipFile

from app.src.databases.AnalyticsDatabase import AnalyticsDatabase


class DataProcessor:

    def __init__(self, analytics_database: AnalyticsDatabase):
        self._analytics_database = analytics_database

    def process(self):
        data = self._get_data_from_kaggle()

        X_train = data.get("X_train")
        y_train = data.get("y_train")
        feature_names = data.get("feature_names")

        visitor_dataframe = self._get_visitor_dataframe(X_train, y_train, feature_names)

        balanced_dataframe = self._get_balanced_dataframe(visitor_dataframe)

        self._save_to_database(balanced_dataframe)

    def _get_data_from_kaggle(self):
        try:
            kaggle_api = KaggleApi()
            kaggle_api.authenticate()
            kaggle_api.dataset_download_file(
                dataset="lipann/prepaired-data-of-customer-revenue-prediction",
                file_name="data_all_features.pkl",
                path="/app/data"
            )

            with ZipFile("/app/data/data_all_features.pkl.zip") as zip_file:
                zip_file.extractall("/app/data")

            data = read_pickle("app/data/data_all_features.pkl")

            info("Got data from kaggle successfully!")
            return data

        except Exception as exc:
            error(f"Failed to get data from kaggle. --> {exc}")

    def _save_to_database(self, visitor_dataframe) -> None:
        try:
            with self._analytics_database.engine.begin() as connection:
                visitor_dataframe.to_sql("visitors", con=connection, if_exists="replace", index=False)
                
                info("Saved data to database successfully!")

        except Exception as exc:
            error(f"Failed to save data to database. --> {exc}")

    def _get_visitor_dataframe(self, X_train, y_train, feature_names):
        try:
            visitor_dataframe = DataFrame(columns=feature_names, data=X_train)
            visitor_dataframe["totals_transaction_revenue"] = y_train

            visitor_dataframe = self._add_positive_revenue_column(visitor_dataframe)

            return visitor_dataframe

        except Exception as exc:
            error(f"Failed to get visitor dataframe. --> {exc}")

    def _add_positive_revenue_column(self, visitor_dataframe):
        try:
            visitor_dataframe["positive_revenue"] = visitor_dataframe["totals_transaction_revenue"] > 0
            visitor_dataframe["positive_revenue"] = visitor_dataframe["positive_revenue"].astype("float")
            visitor_dataframe = visitor_dataframe.drop(columns=["totals_transaction_revenue"])

            return visitor_dataframe

        except Exception as exc:
            error(f"Failed to add positive revenue column. --> {exc}")


    def _get_balanced_dataframe(self, visitor_dataframe):
        try:
            paying_visitor_dataframe = visitor_dataframe[visitor_dataframe["positive_revenue"] == 1]
            number_of_rows = len(paying_visitor_dataframe)
            non_paying_visitor_dataframe = visitor_dataframe[visitor_dataframe["positive_revenue"] == 0][:number_of_rows]

            balanced_dataframe = concat([paying_visitor_dataframe, non_paying_visitor_dataframe])

            info("Balanced dataframe successfully!")
            return balanced_dataframe

        except Exception as exc:
            error(f"Failed to get balanced dataframe. -> {exc}")
