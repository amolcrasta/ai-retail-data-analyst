import numpy as np


class ColumnSemanticEngine:

    def detect_roles(self, df):

        roles = {}

        rows = len(df)

        for col in df.columns:

            col_lower = col.lower()

            unique_ratio = df[col].nunique() / rows

            # -----------------------------
            # Strong name indicators
            # -----------------------------
            if any(x in col_lower for x in [
                "id", "key", "code", "number", "guid"
            ]):

                roles[col] = "identifier"
                continue

            # -----------------------------
            # High uniqueness detection
            # -----------------------------
            if unique_ratio > 0.9:

                roles[col] = "identifier"
                continue

            # -----------------------------
            # Datetime detection
            # -----------------------------
            if "date" in col_lower or "time" in col_lower:

                roles[col] = "time"
                continue

            # -----------------------------
            # Numeric measure detection
            # -----------------------------
            if df[col].dtype in ["int64", "float64"]:

                # Avoid numeric identifiers
                if unique_ratio < 0.5:

                    roles[col] = "measure"

                else:

                    roles[col] = "identifier"

                continue

            # -----------------------------
            # Default dimension
            # -----------------------------
            roles[col] = "dimension"

        return roles