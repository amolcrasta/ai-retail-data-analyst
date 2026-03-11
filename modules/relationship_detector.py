class RelationshipDetector:

    def detect(self, datasets, dataset_names):

        relationships = []

        for i, df1 in enumerate(datasets):

            for j, df2 in enumerate(datasets):

                if i >= j:
                    continue

                common_columns = set(df1.columns).intersection(df2.columns)

                for col in common_columns:

                    relationships.append({
                        "table1_index": i,
                        "table2_index": j,
                        "table1_name": dataset_names[i],
                        "table2_name": dataset_names[j],
                        "column": col
                    })

        return relationships