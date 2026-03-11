class IssueDetector:

    def run(self, context):

        all_issues = []

        for df in context.datasets:

            issues = []

            # Missing values
            missing = df.isnull().sum()

            for col, val in missing.items():

                if val > 0:
                    issues.append({
                        "column": col,
                        "issue": "missing_values",
                        "count": int(val)
                    })

            # Duplicate rows
            duplicates = df.duplicated().sum()

            if duplicates > 0:

                issues.append({
                    "issue": "duplicate_rows",
                    "count": int(duplicates)
                })

            # Potential ID columns with duplicates
            for col in df.columns:

                if "id" in col.lower():

                    duplicate_ids = df[col].duplicated().sum()

                    if duplicate_ids > 0:

                        issues.append({
                            "column": col,
                            "issue": "duplicate_identifier",
                            "count": int(duplicate_ids)
                        })

            all_issues.append(issues)

        context.issues = all_issues

        context.transformation_history.append("Issue detection completed")

        return context