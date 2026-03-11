class DataProfiler:

    def run(self, context):

        profiles = []

        for df in context.datasets:

            profile = {
                "rows": df.shape[0],
                "columns": df.shape[1],
                "missing_values": {k: int(v) for k, v in df.isnull().sum().to_dict().items()},
                "duplicates": int(df.duplicated().sum())
            }

            # Detect column types
            numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns.tolist()
            categorical_cols = df.select_dtypes(include=["object"]).columns.tolist()

            profile["numeric_columns"] = numeric_cols
            profile["categorical_columns"] = categorical_cols

            # Missing value percentages
            profile["missing_percentage"] = {
                k: round(v, 2)
                for k, v in (df.isnull().mean() * 100).to_dict().items()
            }

            # Numeric statistics
            if numeric_cols:
                profile["numeric_summary"] = df[numeric_cols].describe().to_dict()

            # Correlation matrix
            if len(numeric_cols) >= 2:

                corr_matrix = df[numeric_cols].corr()

                profile["correlations"] = corr_matrix.to_dict()

                strong_corr = []

                for col1 in numeric_cols:
                    for col2 in numeric_cols:

                        if col1 != col2:

                            corr_value = corr_matrix.loc[col1, col2]

                            if abs(corr_value) > 0.7:

                                strong_corr.append({
                                    "feature_1": col1,
                                    "feature_2": col2,
                                    "correlation": round(float(corr_value), 2)
                                })

                profile["strong_correlations"] = strong_corr

            # Categorical summaries
            categorical_summary = {}

            for col in categorical_cols:

                categorical_summary[col] = (
                    df[col]
                    .value_counts()
                    .head(10)
                    .to_dict()
                )

            profile["categorical_summary"] = categorical_summary

            profiles.append(profile)

        context.dataset_profile = profiles

        context.transformation_history.append("Data profiling completed")

        return context