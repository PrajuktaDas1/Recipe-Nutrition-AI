# pdf_report.py

from io import BytesIO

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)


def create_pdf(recipe, nutrition):
    """
    Generate a downloadable PDF nutrition report.
    """

    buffer = BytesIO()

    document = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "TitleCustom",
        parent=styles["Title"],
        alignment=TA_CENTER,
        fontSize=24,
        spaceAfter=20
    )

    heading_style = ParagraphStyle(
        "HeadingCustom",
        parent=styles["Heading2"],
        fontSize=16,
        spaceBefore=15,
        spaceAfter=10
    )

    normal_style = ParagraphStyle(
        "NormalCustom",
        parent=styles["BodyText"],
        fontSize=10,
        leading=15
    )

    story = []

    # Title
    story.append(
        Paragraph(
            "Recipe Nutrition AI",
            title_style
        )
    )

    story.append(
        Paragraph(
            f"<b>Recipe:</b> {recipe}",
            normal_style
        )
    )

    story.append(Spacer(1, 20))

    # Nutrition heading
    story.append(
        Paragraph(
            "Nutrition Information",
            heading_style
        )
    )

    table_data = [
        ["Nutrition", "Estimated Value"],

        ["Calories", nutrition.get("calories", "N/A")],

        ["Protein", nutrition.get("protein", "N/A")],

        ["Carbohydrates", nutrition.get("carbs", "N/A")],

        ["Fat", nutrition.get("fat", "N/A")],

        ["Fiber", nutrition.get("fiber", "N/A")],

        ["Sugar", nutrition.get("sugar", "N/A")],

        ["Sodium", nutrition.get("sodium", "N/A")],

        ["Vitamins", nutrition.get("vitamins", "N/A")],

        ["Health Score", nutrition.get("health_score", "N/A")]
    ]

    table = Table(
        table_data,
        colWidths=[180, 300]
    )

    table.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),

            ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),

            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),

            ("FONTNAME", (0, 1), (0, -1), "Helvetica-Bold"),

            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),

            ("VALIGN", (0, 0), (-1, -1), "TOP"),

            ("PADDING", (0, 0), (-1, -1), 8),
        ])
    )

    story.append(table)

    story.append(Spacer(1, 20))

    # Vitamins
    story.append(
        Paragraph(
            "<b>Vitamins:</b> "
            + str(nutrition.get("vitamins", "N/A")),
            normal_style
        )
    )

    story.append(Spacer(1, 10))

    # Allergens
    story.append(
        Paragraph(
            "<b>Possible Allergens:</b> "
            + str(nutrition.get("allergens", "N/A")),
            normal_style
        )
    )

    story.append(Spacer(1, 15))

    # Health tips
    story.append(
        Paragraph(
            "<b>Health Tips:</b> "
            + str(nutrition.get("tips", "N/A")),
            normal_style
        )
    )

    story.append(Spacer(1, 15))

    # Recommendation
    story.append(
        Paragraph(
            "<b>AI Recommendation:</b> "
            + str(nutrition.get("recommendation", "N/A")),
            normal_style
        )
    )

    document.build(story)

    buffer.seek(0)

    return buffer.getvalue()