import pandas as pd
import plotly.express as px


class VisualizationEngine:


    # --------------------------------------
    # Detect column roles
    # --------------------------------------

    def detect_roles(self, df):

        numeric_cols = df.select_dtypes(
            include=["int64", "float64"]
        ).columns.tolist()

        categorical_cols = df.select_dtypes(
            include=["object"]
        ).columns.tolist()

        datetime_cols = df.select_dtypes(
            include=["datetime64"]
        ).columns.tolist()

        return numeric_cols, categorical_cols, datetime_cols


    # --------------------------------------
    # Remove identifiers
    # --------------------------------------

    def remove_identifiers(self, columns):

        filtered = []

        for col in columns:

            name = col.lower()

            if (
                name.endswith("_id")
                or name == "id"
                or "key" in name
                or "uuid" in name
                or "transaction" in name
                or "order_number" in name
            ):
                continue

            filtered.append(col)

        return filtered


    # --------------------------------------
    # Select top analytical columns
    # --------------------------------------

    def select_priority_columns(self, df, numeric_cols, categorical_cols):

        numeric_priority = []
        categorical_priority = []

        # numeric scoring

        for col in numeric_cols:

            variance = df[col].var()

            numeric_priority.append((variance, col))

        numeric_priority.sort(reverse=True)

        numeric_priority = [c for _, c in numeric_priority[:5]]

        # categorical scoring

        for col in categorical_cols:

            unique = df[col].nunique()

            if unique < 50 and unique > 1:

                categorical_priority.append((unique, col))

        categorical_priority.sort()

        categorical_priority = [c for _, c in categorical_priority[:5]]

        return numeric_priority, categorical_priority


    # --------------------------------------
    # Generate insight
    # --------------------------------------

    def generate_insight(self, df, dimension, measure):

        grouped = (
            df.groupby(dimension)[measure]
            .sum()
            .sort_values(ascending=False)
        )

        top = grouped.index[0]
        top_value = grouped.iloc[0]

        bottom = grouped.index[-1]
        bottom_value = grouped.iloc[-1]

        insight = (
            f"{top} contributes the most {measure} "
            f"({top_value:,.2f}), while {bottom} contributes the least "
            f"({bottom_value:,.2f})."
        )

        return insight


    # --------------------------------------
    # Main Engine
    # --------------------------------------

    def run(self, context):

        df = context.cleaned_dataframe

        numeric_cols, categorical_cols, datetime_cols = self.detect_roles(df)

        # remove identifiers

        numeric_cols = self.remove_identifiers(numeric_cols)

        categorical_cols = self.remove_identifiers(categorical_cols)

        # select top priority columns

        numeric_priority, categorical_priority = self.select_priority_columns(
            df,
            numeric_cols,
            categorical_cols
        )

        charts = []
        insights = []


        # ----------------------------------
        # Dimension vs Measure
        # ----------------------------------

        for dim in categorical_priority:

            for measure in numeric_priority:

                try:

                    grouped = df.groupby(dim)[measure].sum().reset_index()

                    chart = px.bar(
                        grouped,
                        x=dim,
                        y=measure,
                        title=f"{measure} by {dim}"
                    )

                    insight = self.generate_insight(
                        df,
                        dim,
                        measure
                    )

                    charts.append(chart)
                    insights.append(insight)

                except:
                    continue


        # ----------------------------------
        # Time series charts
        # ----------------------------------

        for date_col in datetime_cols[:2]:

            for measure in numeric_priority:

                try:

                    chart = px.line(
                        df,
                        x=date_col,
                        y=measure,
                        title=f"{measure} over time"
                    )

                    insight = (
                        f"{measure} trend over time shows how the metric evolves."
                    )

                    charts.append(chart)
                    insights.append(insight)

                except:
                    continue


        # ----------------------------------
        # Limit to top 10 charts
        # ----------------------------------

        context.visualizations = charts[:10]

        context.chart_insights = insights[:10]

        return context