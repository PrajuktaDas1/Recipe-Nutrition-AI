# charts.py

import matplotlib.pyplot as plt
from nutrition import extract_number


def create_macro_chart(nutrition):
    """
    Create a macronutrient pie chart.
    """

    protein = extract_number(nutrition.get("protein"))
    carbs = extract_number(nutrition.get("carbs"))
    fat = extract_number(nutrition.get("fat"))

    values = [protein, carbs, fat]
    labels = ["Protein", "Carbs", "Fat"]

    # Prevent empty chart errors
    if sum(values) <= 0:
        return None

    fig, ax = plt.subplots(figsize=(6, 5))

    ax.pie(
        values,
        labels=labels,
        autopct="%1.1f%%",
        startangle=90
    )

    ax.set_title("Macronutrient Breakdown")

    fig.tight_layout()

    return fig


def create_nutrition_bar_chart(nutrition):
    """
    Create a simple nutrition comparison bar chart.
    """

    labels = [
        "Protein",
        "Carbs",
        "Fat",
        "Fiber",
        "Sugar"
    ]

    values = [
        extract_number(nutrition.get("protein")),
        extract_number(nutrition.get("carbs")),
        extract_number(nutrition.get("fat")),
        extract_number(nutrition.get("fiber")),
        extract_number(nutrition.get("sugar"))
    ]

    if sum(values) <= 0:
        return None

    fig, ax = plt.subplots(figsize=(8, 4))

    ax.bar(labels, values)

    ax.set_ylabel("Amount")
    ax.set_title("Nutrition Overview")

    fig.tight_layout()

    return fig