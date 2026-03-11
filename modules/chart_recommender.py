
class ChartRecommender:

    def recommend(self, df, roles):

        measures = []
        dimensions = []
        time_cols = []

        rows = len(df)

        # ------------------------------------
        # Separate column roles
        # ------------------------------------
        for col, role in roles.items():

            if role == "identifier":
                continue

            if role == "measure":
                measures.append(col)

            if role == "dimension":

                unique_ratio = df[col].nunique() / rows

                # avoid extremely high-cardinality dimensions
                if unique_ratio < 0.3:
                    dimensions.append(col)

            if role == "time":
                time_cols.append(col)

        suggestions = []

        # ------------------------------------
        # 1️⃣ Measure by Dimension (BAR)
        # ------------------------------------
        for measure in measures:

            for dim in dimensions:

                suggestions.append({
                    "type": "bar",
                    "x": dim,
                    "y": measure,
                    "title": f"{measure} by {dim}"
                })

        # ------------------------------------
        # 2️⃣ Time Series (LINE)
        # ------------------------------------
        for measure in measures:

            for time_col in time_cols:

                suggestions.append({
                    "type": "line",
                    "x": time_col,
                    "y": measure,
                    "title": f"{measure} over time"
                })

        # ------------------------------------
        # 3️⃣ Measure Distribution
        # ------------------------------------
        for measure in measures:

            suggestions.append({
                "type": "histogram",
                "x": measure,
                "title": f"Distribution of {measure}"
            })

        # ------------------------------------
        # 4️⃣ Measure vs Measure (SCATTER)
        # ------------------------------------
        if len(measures) >= 2:

            for i in range(len(measures)):

                for j in range(i + 1, len(measures)):

                    suggestions.append({
                        "type": "scatter",
                        "x": measures[i],
                        "y": measures[j],
                        "title": f"{measures[i]} vs {measures[j]}"
                    })

        # ------------------------------------
        # Limit suggestions
        # ------------------------------------
        return suggestions[:10]