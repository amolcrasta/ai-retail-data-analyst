import io
import tempfile

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch


class PDFReportGenerator:

    def generate_report(self, context):

        buffer = io.BytesIO()

        styles = getSampleStyleSheet()

        elements = []

        # ---------------------------------------------------
        # Title
        # ---------------------------------------------------

        elements.append(
            Paragraph(
                "Automated Data Quality & Analysis Report",
                styles["Title"]
            )
        )

        elements.append(Spacer(1, 20))

        # ---------------------------------------------------
        # Dataset Summary
        # ---------------------------------------------------

        if hasattr(context, "cleaned_dataframe") and context.cleaned_dataframe is not None:

            df = context.cleaned_dataframe

            elements.append(
                Paragraph(
                    f"<b>Dataset Size:</b> {df.shape[0]} rows × {df.shape[1]} columns",
                    styles["Normal"]
                )
            )

            elements.append(Spacer(1, 10))

            elements.append(
                Paragraph("<b>Columns</b>", styles["Heading2"])
            )

            for col in df.columns[:30]:

                elements.append(
                    Paragraph(f"- {col}", styles["Normal"])
                )

            elements.append(Spacer(1, 20))

        # ---------------------------------------------------
        # Cleaning Actions
        # ---------------------------------------------------

        if hasattr(context, "transformation_history"):

            elements.append(
                Paragraph(
                    "<b>Data Cleaning Actions</b>",
                    styles["Heading2"]
                )
            )

            for step in context.transformation_history:

                elements.append(
                    Paragraph(f"- {step}", styles["Normal"])
                )

            elements.append(Spacer(1, 20))

        # ---------------------------------------------------
        # Insights
        # ---------------------------------------------------

        if hasattr(context, "chart_insights") and context.chart_insights:

            elements.append(
                Paragraph(
                    "<b>AI Generated Insights</b>",
                    styles["Heading2"]
                )
            )

            for insight in context.chart_insights[:10]:

                elements.append(
                    Paragraph(f"- {insight}", styles["Normal"])
                )

            elements.append(Spacer(1, 20))

        # ---------------------------------------------------
        # Charts
        # ---------------------------------------------------

        if hasattr(context, "visualizations") and context.visualizations:

            elements.append(
                Paragraph(
                    "<b>Key Visual Insights</b>",
                    styles["Heading2"]
                )
            )

            elements.append(Spacer(1, 15))

            # Plotly default color palette
            palette = [
                "#636EFA",
                "#EF553B",
                "#00CC96",
                "#AB63FA",
                "#FFA15A",
                "#19D3F3",
                "#FF6692",
                "#B6E880"
            ]

            for fig in context.visualizations[:6]:

                tmp = tempfile.NamedTemporaryFile(
                    delete=False,
                    suffix=".png"
                )

                # ------------------------------------------------
                # FORCE COLOR ON EVERY TRACE
                # ------------------------------------------------

                for i, trace in enumerate(fig.data):

                    color = palette[i % len(palette)]

                    if hasattr(trace, "marker"):
                        trace.marker.color = color

                    if hasattr(trace, "line"):
                        trace.line.color = color

                # Clean layout
                fig.update_layout(
                    template="plotly_white",
                    font=dict(size=14),
                    title_font=dict(size=18)
                )

                # Export chart
                fig.write_image(
                    tmp.name,
                    scale=3,
                    width=1200,
                    height=700
                )

                elements.append(
                    Image(
                        tmp.name,
                        width=6.5 * inch,
                        height=3.8 * inch
                    )
                )

                elements.append(Spacer(1, 20))

        # ---------------------------------------------------
        # Build PDF
        # ---------------------------------------------------

        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter
        )

        doc.build(elements)

        buffer.seek(0)

        return buffer