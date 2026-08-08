# ============================================================
# agent.py
# Recipe Nutrition AI
# ============================================================

import os
import json

from dotenv import load_dotenv
from google import genai

from nutrition import normalize_nutrition


# ============================================================
# LOAD .ENV
# ============================================================

load_dotenv()


API_KEY = os.getenv("GEMINI_API_KEY")


if not API_KEY:
    raise RuntimeError(
        "GEMINI_API_KEY not found. "
        "Please check your .env file."
    )


# ============================================================
# GEMINI CLIENT
# ============================================================

client = genai.Client(
    api_key=API_KEY
)


# ============================================================
# CURRENT GEMINI MODEL
# ============================================================

MODEL_NAME = "gemini-3.6-flash"


# ============================================================
# NUTRITION ANALYSIS
# ============================================================

def analyze_nutrition(recipe):

    recipe = str(recipe).strip()

    if not recipe:

        return normalize_nutrition({
            "recommendation": "Please enter a recipe."
        })


    prompt = f"""
You are an expert nutritionist and food analysis AI.

Analyze the following recipe:

{recipe}

Assume the recipe represents ONE normal serving.

Estimate the following:

1. Calories
2. Protein
3. Carbohydrates
4. Fat
5. Fiber
6. Sugar
7. Sodium
8. Vitamins
9. Health Score
10. Health Tips
11. Personalized Recommendation
12. Possible Allergens

IMPORTANT:

Return ONLY valid JSON.

Use exactly this structure:

{{
    "calories": "500 kcal",
    "protein": "25 g",
    "carbs": "60 g",
    "fat": "18 g",
    "fiber": "6 g",
    "sugar": "5 g",
    "sodium": "700 mg",
    "vitamins": "Vitamin A, Vitamin C, Vitamin B6",
    "health_score": "85/100",
    "tips": "Short practical health advice.",
    "recommendation": "Short personalized recommendation.",
    "allergens": "Milk, nuts, gluten or None"
}}

Rules:

- Give realistic estimated nutrition.
- Always provide every field.
- Health score must be between 0 and 100.
- Keep health tips concise.
- Keep recommendation concise.
- Mention important vitamins.
- Mention possible common allergens.
- Do NOT use markdown.
- Do NOT put ``` around the JSON.
- Do NOT write anything outside the JSON.
"""


    try:

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )


        # ----------------------------------------------------
        # GET AI TEXT
        # ----------------------------------------------------

        text = response.text.strip()


        if not text:

            return normalize_nutrition({
                "recommendation":
                "AI returned an empty response."
            })


        # ----------------------------------------------------
        # CLEAN MARKDOWN JSON
        # ----------------------------------------------------

        text = text.replace("```json", "")
        text = text.replace("```", "")
        text = text.strip()


        # ----------------------------------------------------
        # PARSE JSON
        # ----------------------------------------------------

        data = json.loads(text)


        return normalize_nutrition(data)


    except json.JSONDecodeError:

        # AI returned text instead of JSON
        return parse_text_response(text)


    except Exception as error:

        # ----------------------------------------------------
        # SHOW ACTUAL ERROR IN RESULT
        # ----------------------------------------------------

        return normalize_nutrition({

            "recommendation":
            f"AI Error: {str(error)}"

        })


# ============================================================
# FALLBACK TEXT PARSER
# ============================================================

def parse_text_response(text):

    result = {

        "calories": "N/A",

        "protein": "N/A",

        "carbs": "N/A",

        "fat": "N/A",

        "fiber": "N/A",

        "sugar": "N/A",

        "sodium": "N/A",

        "vitamins": "N/A",

        "health_score": "N/A",

        "tips": "N/A",

        "recommendation": "N/A",

        "allergens": "N/A"

    }


    if not text:
        return normalize_nutrition(result)


    for line in text.splitlines():

        if ":" not in line:
            continue


        key, value = line.split(":", 1)


        key = key.lower().strip()

        value = value.strip()


        if "calories" in key:

            result["calories"] = value


        elif "protein" in key:

            result["protein"] = value


        elif "carb" in key:

            result["carbs"] = value


        elif "fat" in key:

            result["fat"] = value


        elif "fiber" in key:

            result["fiber"] = value


        elif "sugar" in key:

            result["sugar"] = value


        elif "sodium" in key:

            result["sodium"] = value


        elif "vitamin" in key:

            result["vitamins"] = value


        elif "health score" in key:

            result["health_score"] = value


        elif "health tip" in key:

            result["tips"] = value


        elif "recommendation" in key:

            result["recommendation"] = value


        elif "allergen" in key:

            result["allergens"] = value


    return normalize_nutrition(result)


# ============================================================
# COMPATIBILITY FUNCTION
# ============================================================

def get_recipe_response(recipe):

    nutrition = analyze_nutrition(recipe)


    return (

        f"Calories: {nutrition['calories']}\n"

        f"Protein: {nutrition['protein']}\n"

        f"Carbs: {nutrition['carbs']}\n"

        f"Fat: {nutrition['fat']}\n"

        f"Fiber: {nutrition['fiber']}\n"

        f"Sugar: {nutrition['sugar']}\n"

        f"Sodium: {nutrition['sodium']}\n"

        f"Vitamins: {nutrition['vitamins']}\n"

        f"Health Score: {nutrition['health_score']}\n"

        f"Health Tips: {nutrition['tips']}\n"

        f"Recommendation: {nutrition['recommendation']}\n"

        f"Allergens: {nutrition['allergens']}"

    )