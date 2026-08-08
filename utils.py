# utils.py

import re


def is_valid_recipe(recipe):
    """
    Check whether user entered a reasonable recipe name.
    """

    if recipe is None:
        return False

    recipe = recipe.strip()

    if len(recipe) < 2:
        return False

    return True


def safe_text(text):
    """
    Safely convert text to string.
    """

    if text is None:
        return ""

    return str(text).strip()


def clean_recipe_name(recipe):
    """
    Clean unnecessary spaces.
    """

    recipe = safe_text(recipe)

    recipe = re.sub(r"\s+", " ", recipe)

    return recipe.strip()


def health_label(score):
    """
    Convert health score into a label.
    """

    try:
        score = float(score)
    except (ValueError, TypeError):
        return "Unknown"

    if score >= 80:
        return "Excellent"

    if score >= 60:
        return "Good"

    if score >= 40:
        return "Moderate"

    return "Needs Improvement"