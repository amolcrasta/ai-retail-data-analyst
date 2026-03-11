import pandas as pd


class RootCauseEngine:

    # ----------------------------------------
    # Detect main KPI
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
    # Remove identifiers
    # ----------------------------------------

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
            ):
                continue

            filtered.append(col)

        return filtered


    # ----------------------------------------
    # Find drivers of KPI
    # ----------------------------------------

    def analyze_dimension(self, df, dimension, kpi):

        grouped = (
            df.groupby(dimension)[kpi]
            .sum()
            .sort_values(ascending=False)
        )

        top = grouped.index[0]
        bottom = grouped.index[-1]

        top_value = grouped.iloc[0]
        bottom_value = grouped.iloc[-1]

        insight = (
            f"{dimension}: {top} drives the highest {kpi} "
            f"({top_value:,.2f}), while {bottom} contributes the least "
            f"({bottom_value:,.2f})."
        )

        return insight


    # ----------------------------------------
    # Main RCA logic
    # ----------------------------------------

    def run(self, df):

        insights = []

        kpi = self.detect_kpi(df)

        if not kpi:
            return ["Unable to determine KPI for analysis."]

        categorical_cols = df.select_dtypes(
            include=["object"]
        ).columns.tolist()

        categorical_cols = self.remove_identifiers(categorical_cols)

        # analyze top 3 dimensions
        for col in categorical_cols[:3]:

            try:

                insight = self.analyze_dimension(
                    df,
                    col,
                    kpi
                )

                insights.append(insight)

            except:
                continue

        if not insights:

            insights.append(
                "No strong root cause patterns detected."
            )

        return insights