# nutrition.py

def clean_value(value, default="N/A"):
    """Safely convert any value to a displayable string."""

    if value is None:
        return default

    value = str(value).strip()

    if not value:
        return default

    return value


def normalize_nutrition(data):
    """
    Make sure all required nutrition fields exist.
    """

    if not isinstance(data, dict):
        data = {}

    result = {
        "calories": clean_value(data.get("calories")),
        "protein": clean_value(data.get("protein")),
        "carbs": clean_value(data.get("carbs")),
        "fat": clean_value(data.get("fat")),
        "fiber": clean_value(data.get("fiber")),
        "sugar": clean_value(data.get("sugar")),
        "sodium": clean_value(data.get("sodium")),
        "vitamins": clean_value(data.get("vitamins")),
        "health_score": clean_value(data.get("health_score")),
        "tips": clean_value(data.get("tips")),
        "recommendation": clean_value(data.get("recommendation")),
        "allergens": clean_value(data.get("allergens")),
    }

    return result


def extract_number(value):
    """
    Extract the first number from text.

    Example:
    '520 kcal' -> 520.0
    '25 g' -> 25.0
    '85/100' -> 85.0
    """

    if value is None:
        return 0.0

    text = str(value)

    number = ""

    decimal_found = False

    for char in text:

        if char.isdigit():
            number += char

        elif char == "." and not decimal_found:
            number += char
            decimal_found = True

        elif number:
            break

    try:
        return float(number)

    except ValueError:
        return 0.0


def get_health_score(value):
    """Return a safe health score between 0 and 100."""

    score = extract_number(value)

    score = max(0, min(100, score))

    return int(score)