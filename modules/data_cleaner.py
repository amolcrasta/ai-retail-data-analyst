import pandas as pd
import numpy as np


class DataCleaner:

    # -----------------------------------
    # Column semantic detection
    # -----------------------------------
    def detect_column_type(self, column):

        name = column.lower()

        if "id" in name or "key" in name:
            return "identifier"

        if "price" in name or "amount" in name or "cost" in name:
            return "price"

        if "qty" in name or "quantity" in name:
            return "quantity"

        if "date" in name or "time" in name:
            return "datetime"

        return "unknown"


    # -----------------------------------
    # Normalize categorical text
    # -----------------------------------
    def normalize_text(self, series):

        series = series.astype(str)

        series = series.str.strip()

        series = series.replace(
            ["", "nan", "None", "null", "NaN"],
            np.nan
        )

        return series


    # -----------------------------------
    # Outlier handling (IQR)
    # -----------------------------------
    def handle_outliers(self, df, column):

        q1 = df[column].quantile(0.25)
        q3 = df[column].quantile(0.75)

        iqr = q3 - q1

        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr

        df[column] = df[column].clip(lower, upper)

        return df


    # -----------------------------------
    # Fill numeric values intelligently
    # -----------------------------------
    def fill_numeric(self, df, column):

        missing_before = df[column].isna().sum()

        if missing_before == 0:
            return df

        if abs(df[column].skew()) > 1:
            df[column] = df[column].fillna(df[column].median())
        else:
            df[column] = df[column].fillna(df[column].mean())

        return df


    # -----------------------------------
    # Group-based filling
    # -----------------------------------
    def group_fill(self, df, value_col, group_col):

        if group_col not in df.columns:
            return df

        df[value_col] = df.groupby(group_col)[value_col].transform(
            lambda x: x.fillna(x.median())
        )

        return df


    # -----------------------------------
    # Main pipeline
    # -----------------------------------
    def run(self, context):

        cleaned_datasets = []

        for df in context.datasets:

            df = df.copy()

            # -------------------------------
            # Standardize column names
            # -------------------------------

            df.columns = (
                df.columns
                .str.strip()
                .str.replace(" ", "_")
                .str.lower()
            )

            # -------------------------------
            # Remove duplicates
            # -------------------------------

            duplicates = df.duplicated().sum()

            if duplicates > 0:

                df = df.drop_duplicates()

                context.transformation_history.append(
                    f"Removed {duplicates} duplicate rows"
                )

            # -------------------------------
            # Drop low quality rows
            # -------------------------------

            threshold = int(len(df.columns) * 0.5)

            before = len(df)

            df = df.dropna(thresh=threshold)

            dropped = before - len(df)

            if dropped > 0:

                context.transformation_history.append(
                    f"Dropped {dropped} low-quality rows"
                )

            # -------------------------------
            # Normalize text columns
            # -------------------------------

            for col in df.select_dtypes(include="object").columns:

                df[col] = self.normalize_text(df[col])

            # -------------------------------
            # Remove empty columns
            # -------------------------------

            empty_columns = df.columns[df.isna().all()]

            if len(empty_columns) > 0:

                df = df.drop(columns=empty_columns)

                context.transformation_history.append(
                    f"Removed empty columns: {list(empty_columns)}"
                )

            # -------------------------------
            # Detect column types
            # -------------------------------

            column_types = {}

            for col in df.columns:
                column_types[col] = self.detect_column_type(col)

            # -------------------------------
            # Convert datetime
            # -------------------------------

            for col, ctype in column_types.items():

                if ctype == "datetime":

                    try:

                        df[col] = pd.to_datetime(df[col])

                        context.transformation_history.append(
                            f"Converted {col} to datetime"
                        )

                    except:
                        pass

            # -------------------------------
            # Numeric processing
            # -------------------------------

            numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns

            for col in numeric_cols:

                semantic = column_types.get(col)

                if semantic == "price":

                    for group_col in df.columns:

                        if "product" in group_col:

                            df = self.group_fill(df, col, group_col)

                df = self.fill_numeric(df, col)

                df = self.handle_outliers(df, col)

            # -------------------------------
            # Categorical filling
            # -------------------------------

            for col in df.select_dtypes(include="object").columns:

                if df[col].isna().sum() > 0:

                    mode = df[col].mode()

                    if len(mode) > 0:
                        df[col] = df[col].fillna(mode[0])
                    else:
                        df[col] = df[col].fillna("Unknown")

                    context.transformation_history.append(
                        f"Filled categorical values in {col}"
                    )

            cleaned_datasets.append(df)

        context.datasets = cleaned_datasets

        context.transformation_history.append(
            "Advanced AI cleaning completed"
        )

        return context