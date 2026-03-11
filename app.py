import streamlit as st
import pandas as pd
import plotly.io as pio
import subprocess
import sys

# Ensure Kaleido has Chrome available
try:
    pio.kaleido.scope.chromium_executable
except:
    subprocess.run([sys.executable, "-m", "plotly_get_chrome"], check=False)

from models.dataset_context import DatasetContext

from modules.file_loader import FileLoader
from modules.data_profiler import DataProfiler
from modules.issue_detector import IssueDetector
from modules.data_cleaner import DataCleaner
from modules.relationship_detector import RelationshipDetector
from modules.join_engine import JoinEngine
from modules.visualization_engine import VisualizationEngine
from modules.pipeline_engine import PipelineEngine
from modules.column_logic_engine import ColumnLogicEngine
from modules.story_engine import StoryEngine
from modules.root_cause_engine import RootCauseEngine
from modules.anomaly_engine import AnomalyEngine
from modules.pdf_report_generator import PDFReportGenerator


# -----------------------------------------------------
# Page Configuration
# -----------------------------------------------------

st.set_page_config(
    page_title="Automated Data Quality & Analysis Engine",
    page_icon="🧠",
    layout="wide"
)

st.title("🧠 Automated Data Quality & Analysis Engine")

st.markdown(
"""
Upload retail datasets and automatically generate insights using AI-powered
data cleaning, relationship detection, KPI discovery, automated analytics,
and downloadable AI-generated reports.
"""
)

# -----------------------------------------------------
# Sidebar Header
# -----------------------------------------------------

st.sidebar.markdown("## Navigation")
st.sidebar.markdown("---")

st.sidebar.markdown(
"""
### Automated Data Quality & Analysis Engine

Automated analytics assistant for retail datasets.
"""
)

# -----------------------------------------------------
# Session State
# -----------------------------------------------------

if "context" not in st.session_state:
    st.session_state.context = None


# -----------------------------------------------------
# Upload Protection
# -----------------------------------------------------

MAX_ROWS = 500000

def validate_dataset(df):

    if len(df) > MAX_ROWS:

        st.error(
            f"Dataset has {len(df):,} rows. Maximum allowed is {MAX_ROWS:,}."
        )

        return False

    return True


# -----------------------------------------------------
# Sidebar Navigation
# -----------------------------------------------------

menu = st.sidebar.radio(
    "",
    [
        "Upload Data",
        "Dataset Explorer",
        "Chart Builder and Insights"
    ]
)

if st.sidebar.button("Reset Application"):
    st.session_state.clear()
    st.rerun()


# -----------------------------------------------------
# KPI Detection
# -----------------------------------------------------

def detect_kpis(df):

    numeric_cols = df.select_dtypes(
        include=["int64", "float64"]
    ).columns.tolist()

    kpis = []

    for col in numeric_cols:

        name = col.lower()

        if (
            "revenue" in name
            or "sales" in name
            or "profit" in name
            or "amount" in name
            or "price" in name
        ):
            kpis.append(col)

    if not kpis and numeric_cols:
        kpis = numeric_cols[:2]

    return kpis


# =====================================================
# Upload Data
# =====================================================

if menu == "Upload Data":

    with st.expander("📂 Upload Retail Datasets", expanded=True):

        uploaded_files = st.file_uploader(
            "Upload CSV or Excel files",
            type=["csv", "xlsx", "xls"],
            accept_multiple_files=True
        )

        if uploaded_files:

            loader = FileLoader()

            datasets, dataset_names = loader.load_files(uploaded_files)

            valid_datasets = []
            valid_names = []

            for df, name in zip(datasets, dataset_names):

                if validate_dataset(df):

                    valid_datasets.append(df)
                    valid_names.append(name)

            if valid_datasets:

                context = DatasetContext()

                context.datasets = valid_datasets
                context.dataset_names = valid_names
                context.transformation_history = []

                st.session_state.context = context

                st.success("Datasets uploaded successfully")


# =====================================================
# Dataset Explorer
# =====================================================

elif menu == "Dataset Explorer":

    context = st.session_state.get("context")

    if context is None:

        st.warning("Upload datasets first")

    else:

        with st.expander("📊 Dataset Preview", expanded=True):

            for i, df in enumerate(context.datasets):

                st.subheader(context.dataset_names[i])

                preview_rows = st.selectbox(
                    "Preview rows",
                    [10, 50, 100, 500],
                    key=f"preview_{i}"
                )

                st.dataframe(df.head(preview_rows), use_container_width=True)


        with st.expander("🤖 Run AI Processing Pipeline"):

            if st.button("Process Data"):

                pipeline_modules = [
                    DataProfiler(),
                    IssueDetector(),
                    DataCleaner()
                ]

                pipeline = PipelineEngine(pipeline_modules)

                context = pipeline.run(context)

                detector = RelationshipDetector()

                context.detected_relationships = detector.detect(
                    context.datasets,
                    context.dataset_names
                )

                join_engine = JoinEngine()

                context = join_engine.auto_join(context)

                st.session_state.context = context

                st.success("AI processing completed")


        if hasattr(context, "cleaned_dataframe") and context.cleaned_dataframe is not None:

            df = context.cleaned_dataframe

            with st.expander("📦 Joined Dataset Preview", expanded=True):

                st.write(f"Rows: {df.shape[0]}")
                st.write(f"Columns: {df.shape[1]}")

                st.dataframe(df.head(200), use_container_width=True)


            with st.expander("🧮 Create Calculated Column"):

                logic_engine = ColumnLogicEngine()

                new_col_name = st.text_input("New Column Name")

                expression = st.text_input("Formula")

                if st.button("Create Column"):

                    try:

                        df = logic_engine.apply_logic(
                            df,
                            new_col_name,
                            expression
                        )

                        context.cleaned_dataframe = df

                        context.transformation_history.append(
                            f"User created column '{new_col_name}' using logic: {expression}"
                        )

                        st.success("Column created successfully")

                        st.rerun()

                    except:
                        st.error("Invalid formula")


            with st.expander("🛠 Remove Column"):

                remove_col = st.selectbox(
                    "Select column to remove",
                    ["None"] + list(df.columns)
                )

                if remove_col != "None":

                    if st.button("Remove Selected Column"):

                        df = df.drop(columns=[remove_col])

                        context.cleaned_dataframe = df

                        context.transformation_history.append(
                            f"User removed column: {remove_col}"
                        )

                        st.success(
                            f"Column '{remove_col}' removed"
                        )

                        st.rerun()


            with st.expander("🧹 AI Cleaning Summary"):

                for step in context.transformation_history:
                    st.write("•", step)


            with st.expander("📈 Detected KPIs"):

                kpis = detect_kpis(df)

                for k in kpis:
                    st.success(f"KPI detected: {k}")


# =====================================================
# Chart Builder and Insights
# =====================================================

elif menu == "Chart Builder and Insights":

    context = st.session_state.get("context")

    if context is None or not hasattr(context, "cleaned_dataframe") or context.cleaned_dataframe is None:

        st.warning("Process datasets first in Dataset Explorer")

    else:

        df = context.cleaned_dataframe

        st.info(
            f"Dataset ready for visualization: {df.shape[0]} rows | {df.shape[1]} columns"
        )


        with st.expander("📖 AI Data Story", expanded=True):

            story_engine = StoryEngine()

            story = story_engine.generate_story(df)

            for line in story:
                st.write("•", line)


        with st.expander("🔍 Root Cause Analysis"):

            rca_engine = RootCauseEngine()

            rca = rca_engine.run(df)

            for insight in rca:
                st.write("•", insight)


        with st.expander("⚠️ Anomaly Detection"):

            anomaly_engine = AnomalyEngine()

            anomalies = anomaly_engine.run(df)

            for insight in anomalies:
                st.write("•", insight)


        with st.expander("📊 Top 10 Most Relevant Charts", expanded=True):

            viz_engine = VisualizationEngine()

            context = viz_engine.run(context)

            charts = context.visualizations
            insights = context.chart_insights

            for i, chart in enumerate(charts):

                st.plotly_chart(
                    chart,
                    use_container_width=True,
                    key=f"chart_{i}"
                )

                st.info(insights[i])


# =====================================================
# REPORT DOWNLOAD
# =====================================================

context = st.session_state.get("context")

st.sidebar.markdown("---")
st.sidebar.markdown("### Reports")

if (
    context is not None
    and hasattr(context, "cleaned_dataframe")
    and context.cleaned_dataframe is not None
):

    try:

        if not hasattr(context, "visualizations") or context.visualizations is None:

            viz_engine = VisualizationEngine()
            context = viz_engine.run(context)

        pdf_generator = PDFReportGenerator()

        pdf_buffer = pdf_generator.generate_report(context)

        st.sidebar.download_button(
            label="📄 Download Analytics Report",
            data=pdf_buffer,
            file_name="analytics_report.pdf",
            mime="application/pdf"
        )

    except Exception as e:

        st.sidebar.error(e)

else:

    st.sidebar.info("Process dataset to enable report download")