import pandas as pd
import duckdb


class FileLoader:

    # --------------------------------------------------
    # Standalone file loading function
    # --------------------------------------------------
    def load_files(self, uploaded_files):

        datasets = []
        dataset_names = []

        for file in uploaded_files:

            filename = file.name.lower()

            try:

                # --------------------------------------------------
                # CSV FILES
                # --------------------------------------------------
                if filename.endswith(".csv"):

                    try:
                        df = pd.read_csv(file)

                    except Exception:

                        file.seek(0)

                        try:
                            df = pd.read_csv(file, encoding="latin1")

                        except Exception:

                            file.seek(0)

                            con = duckdb.connect()

                            df = con.execute(
                                "SELECT * FROM read_csv_auto(?)",
                                [file]
                            ).df()

                # --------------------------------------------------
                # EXCEL FILES
                # --------------------------------------------------
                elif filename.endswith(".xlsx") or filename.endswith(".xls"):

                    df = pd.read_excel(file)

                else:

                    raise ValueError(
                        f"Unsupported file type: {file.name}"
                    )

                # --------------------------------------------------
                # Normalize column names
                # --------------------------------------------------
                df.columns = (
                    df.columns
                    .str.strip()
                    .str.replace(" ", "_")
                    .str.lower()
                )

                datasets.append(df)
                dataset_names.append(file.name)

            except Exception as e:

                raise RuntimeError(
                    f"Error loading {file.name}: {str(e)}"
                )

        return datasets, dataset_names


    # --------------------------------------------------
    # Pipeline-compatible method
    # --------------------------------------------------
    def run(self, context):

        # Nothing to load here because files were already loaded
        # using load_files() inside app.py

        context.transformation_history.append("Files loaded")

        return context