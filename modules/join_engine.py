import pandas as pd


class JoinEngine:

    def auto_join(self, context):

        datasets = context.datasets
        dataset_names = context.dataset_names

        context.joins = []

        # Detect fact table
        fact_index = max(
            range(len(datasets)),
            key=lambda i: datasets[i].shape[0]
        )

        fact_df = datasets[fact_index].copy()

        context.transformation_history.append(
            f"Fact table detected: {dataset_names[fact_index]}"
        )

        for i, dim_df in enumerate(datasets):

            if i == fact_index:
                continue

            common_cols = set(fact_df.columns).intersection(dim_df.columns)

            if not common_cols:
                continue

            join_col = list(common_cols)[0]

            dim_df = dim_df.drop_duplicates(subset=[join_col])

            fact_df = fact_df.merge(
                dim_df,
                on=join_col,
                how="left"
            )

            # store join metadata
            context.joins.append({
                "left_table": dataset_names[fact_index],
                "right_table": dataset_names[i],
                "column": join_col
            })

            context.transformation_history.append(
                f"Joined {dataset_names[i]} on {join_col}"
            )

        context.cleaned_dataframe = fact_df

        return context