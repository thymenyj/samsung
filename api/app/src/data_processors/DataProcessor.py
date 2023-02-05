from pandas import DataFrame, read_pickle
from kaggle.api.kaggle_api_extended import KaggleApi
from zipfile import ZipFile

from app.src.databases.AnalyticsDatabase import AnalyticsDatabase


class DataProcessor:

    def __init__(self, analytics_database: AnalyticsDatabase):
        self._analytics_database = analytics_database

    def process(self) -> None:
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

        X_train = data.get("X_train")
        y_train = data.get("y_train")
        feature_names = data.get("feature_names")

        visitor_dataframe = self._get_visitor_dataframe(X_train, y_train, feature_names)

        self._save_to_database(visitor_dataframe)

    def _save_to_database(self, visitor_dataframe) -> None:
        print("Save to database")
        with self._analytics_database.engine.connect() as connection:
            visitor_dataframe.to_sql("visitors", con=connection, if_exists="replace")

    def _get_visitor_dataframe(self, X_train, y_train, feature_names):
        visitor_dataframe = DataFrame(columns=feature_names, data=X_train)
        visitor_dataframe["totals_transaction_revenue"] = y_train

        visitor_dataframe = self._add_positive_revenue_column(visitor_dataframe)

        return visitor_dataframe

    def _add_positive_revenue_column(self, visitor_dataframe):
        visitor_dataframe["positive_revenue"] = visitor_dataframe["totals_transaction_revenue"] > 0
        visitor_dataframe["positive_revenue"] = visitor_dataframe["positive_revenue"].astype(
            "float")
        visitor_dataframe = visitor_dataframe.drop(
            columns=["totals_transaction_revenue"])

        return visitor_dataframe