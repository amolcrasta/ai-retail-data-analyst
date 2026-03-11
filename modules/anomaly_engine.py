import pandas as pd
import numpy as np


class AnomalyEngine:


    # ----------------------------------------
    # Detect KPI
    # ----------------------------------------

    def detect_kpi(self, df):

        numeric_cols = df.select_dtypes(
            include=["int64", "float64"]
        ).columns.tolist()

        for col in numeric_cols:

            name = col.lower()

            if (
                "revenue" in name
                or "sales" in name
                or "amount" in name
                or "profit" in name
            ):
                return col

        if numeric_cols:
            return numeric_cols[0]

        return None


    # ----------------------------------------
    # Detect anomalies using Z-score
    # ----------------------------------------

    def detect_anomalies(self, df, date_col, kpi):

        series = df.groupby(date_col)[kpi].sum()

        mean = series.mean()
        std = series.std()

        anomalies = []

        for date, value in series.items():

            z = (value - mean) / std if std != 0 else 0

            if abs(z) > 2:

                anomalies.append((date, value, z))

        return anomalies


    # ----------------------------------------
    # Main engine
    # ----------------------------------------

    def run(self, df):

        insights = []

        kpi = self.detect_kpi(df)

        if not kpi:

            return ["Unable to detect KPI for anomaly analysis."]

        datetime_cols = df.select_dtypes(
            include=["datetime64"]
        ).columns.tolist()

        if not datetime_cols:

            return ["No time column detected for anomaly analysis."]

        date_col = datetime_cols[0]

        anomalies = self.detect_anomalies(
            df,
            date_col,
            kpi
        )

        if not anomalies:

            insights.append(
                f"No major anomalies detected in {kpi} over time."
            )

        else:

            for date, value, z in anomalies:

                direction = "spike" if z > 0 else "drop"

                insights.append(
                    f"Anomaly detected: {kpi} shows a significant {direction} "
                    f"on {date.date()} (value {value:,.2f})."
                )

        return insights