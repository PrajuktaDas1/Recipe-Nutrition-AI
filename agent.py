import os
import json
import streamlit as st
from dotenv import load_dotenv
from google import genai

from nutrition import normalize_nutrition

# ============================================================
# LOAD ENVIRONMENT
# ============================================================

load_dotenv()

# Local computer
API_KEY = os.getenv("GEMINI_API_KEY")

# Streamlit Cloud
if not API_KEY:
    try:
        API_KEY = st.secrets["GEMINI_API_KEY"]
    except Exception:
        API_KEY = None

# ============================================================
# CHECK API KEY
# ============================================================

if not API_KEY:
    raise RuntimeError(
        "GEMINI_API_KEY is missing. "
        "Add it in Streamlit Cloud → Manage app → Settings → Secrets."
    )

# ============================================================
# GEMINI
# ============================================================

client = genai.Client(api_key=API_KEY)

MODEL_NAME = "gemini-2.5-flash"


# ============================================================
# NUTRITION ANALYSIS
# ============================================================

def analyze_nutrition(recipe):

    recipe = str(recipe).strip()

    if not recipe:
        return normalize_nutrition({})

    prompt = f"""
You are an expert nutritionist.

Analyze this food/recipe:

{recipe}

Assume one normal serving.

Return ONLY valid JSON.

Use exactly this format:

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
  "tips": "Eat this in a balanced portion.",
  "recommendation": "A good option when eaten in moderation.",
  "allergens": "None"
}}

Rules:
- Always provide every field.
- Give realistic estimated values.
- Health score must be between 0 and 100.
- Do not use markdown.
- Do not use ```json.
- Return JSON only.
"""

    try:

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )

        text = response.text.strip()

        # Remove accidental markdown
        if text.startswith("```"):
            text = text.replace("```json", "")
            text = text.replace("```", "")
            text = text.strip()

        data = json.loads(text)

        return normalize_nutrition(data)

    except Exception as e:

        # IMPORTANT:
        # Show the real error instead of silently showing N/A
        return normalize_nutrition({
            "recommendation": f"AI Error: {str(e)}"
        })


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
import json
import streamlit as st
from dotenv import load_dotenv
from google import genai

from nutrition import normalize_nutrition

# --------------------------------------------------
# LOAD LOCAL .env
# --------------------------------------------------

load_dotenv()

# --------------------------------------------------
# GET GEMINI API KEY
# Works both locally and on Streamlit Cloud
# --------------------------------------------------

API_KEY = os.getenv("GEMINI_API_KEY")

# Streamlit Cloud Secrets
if not API_KEY:
    try:
        API_KEY = st.secrets["GEMINI_API_KEY"]
    except Exception:
        API_KEY = None

# --------------------------------------------------
# CHECK API KEY
# --------------------------------------------------

if not API_KEY:
    raise RuntimeError(
        "GEMINI_API_KEY is missing. "
        "Add GEMINI_API_KEY in Streamlit Cloud → Manage app → Settings → Secrets."
    )

# --------------------------------------------------
# GEMINI CLIENT
# --------------------------------------------------

client = genai.Client(api_key=API_KEY)

MODEL_NAME = "gemini-2.5-flash"


# ==================================================
# MAIN NUTRITION FUNCTION
# ==================================================

def analyze_nutrition(recipe):

    recipe = str(recipe).strip()

    if not recipe:
        return normalize_nutrition({
            "recommendation": "Please enter a recipe."
        })

    prompt = f"""
You are an expert nutritionist and food analysis AI.

Analyze this recipe:

{recipe}

Assume this represents ONE normal serving.

Estimate:

- Calories
- Protein
- Carbohydrates
- Fat
- Fiber
- Sugar
- Sodium
- Vitamins
- Health Score
- Health Tips
- Personalized Recommendation
- Possible Allergens

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

1. Give realistic estimated nutrition.
2. Always provide every field.
3. Health score must be between 0 and 100.
4. Keep health tips concise.
5. Keep recommendation concise.
6. Mention important vitamins.
7. Mention possible common allergens.
8. Do not use Markdown.
9. Do not use code blocks.
10. Do not write anything outside the JSON.
"""

    try:

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )

        text = (response.text or "").strip()

        if not text:
            return normalize_nutrition({
                "recommendation": "AI returned an empty response."
            })

        # Remove accidental Markdown code fences
        text = text.replace("```json", "")
        text = text.replace("```", "")
        text = text.strip()

        # Convert JSON text to dictionary
        data = json.loads(text)

        return normalize_nutrition(data)

    except json.JSONDecodeError:

        return parse_text_response(text)

    except Exception as error:

        return normalize_nutrition({
            "recommendation": f"AI Error: {error}"
        })


# ==================================================
# FALLBACK TEXT PARSER
# ==================================================

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


# ==================================================
# COMPATIBILITY FUNCTION
# ==================================================

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