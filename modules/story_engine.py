import pandas as pd


class StoryEngine:


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
    # Dataset overview
    # ----------------------------------------

    def dataset_summary(self, df):

        rows = df.shape[0]
        cols = df.shape[1]

        return f"The dataset contains {rows:,} records and {cols} columns."


    # ----------------------------------------
    # Top contributor insight
    # ----------------------------------------

    def top_contributor(self, df, dimension, kpi):

        grouped = (
            df.groupby(dimension)[kpi]
            .sum()
            .sort_values(ascending=False)
        )

        top = grouped.index[0]
        value = grouped.iloc[0]

        return f"{top} contributes the highest {kpi} ({value:,.2f})."


    # ----------------------------------------
    # Lowest contributor
    # ----------------------------------------

    def lowest_contributor(self, df, dimension, kpi):

        grouped = (
            df.groupby(dimension)[kpi]
            .sum()
            .sort_values()
        )

        bottom = grouped.index[0]
        value = grouped.iloc[0]

        return f"{bottom} contributes the lowest {kpi} ({value:,.2f})."


    # ----------------------------------------
    # Trend detection
    # ----------------------------------------

    def detect_trend(self, df, date_col, kpi):

        trend = df.groupby(date_col)[kpi].sum()

        if trend.iloc[-1] > trend.iloc[0]:

            return f"{kpi} shows an overall increasing trend over time."

        else:

            return f"{kpi} shows a declining trend over time."


    # ----------------------------------------
    # Main story generator
    # ----------------------------------------

    def generate_story(self, df):

        story = []

        kpi = self.detect_kpi(df)

        if not kpi:
            return ["Unable to detect KPI for storytelling."]

        story.append(self.dataset_summary(df))

        total = df[kpi].sum()

        story.append(f"Total {kpi} across the dataset is {total:,.2f}.")

        categorical_cols = df.select_dtypes(include=["object"]).columns.tolist()

        datetime_cols = df.select_dtypes(include=["datetime64"]).columns.tolist()

        if categorical_cols:

            dim = categorical_cols[0]

            story.append(self.top_contributor(df, dim, kpi))

            story.append(self.lowest_contributor(df, dim, kpi))

        if datetime_cols:

            story.append(self.detect_trend(df, datetime_cols[0], kpi))

        return story