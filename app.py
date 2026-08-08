import streamlit as st
import agent

from nutrition import get_health_score
from charts import create_macro_chart, create_nutrition_bar_chart
from pdf_report import create_pdf
from utils import is_valid_recipe, clean_recipe_name, health_label


st.set_page_config(
    page_title="Recipe Nutrition AI",
    page_icon="🥗",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at 10% 10%, rgba(90, 220, 150, 0.18), transparent 30%),
        radial-gradient(circle at 90% 90%, rgba(80, 190, 220, 0.12), transparent 30%),
        linear-gradient(135deg, #f7fffa 0%, #edfff5 50%, #f7fffc 100%);
}

/* Main container */
.block-container {
    max-width: 1200px;
    padding-top: 35px;
    padding-bottom: 50px;
}


/* # ============================================================
# HERO
# ============================================================ */

/* =========================================================
   INPUT CARD
   ========================================================= */

.input-card {
    background: rgba(255, 255, 255, 0.9);
    border-radius: 24px;
    padding: 28px;
    box-shadow: 0 15px 45px rgba(30, 100, 70, 0.10);
    border: 1px solid rgba(255, 255, 255, 0.9);
}


/* =========================================================
   INPUT
   ========================================================= */

.stTextInput > div > div > input {
    height: 52px;
    border-radius: 14px;
    border: 1px solid #d5e8dd;
    background: #ffffff;
    font-size: 16px;
    padding: 10px 16px;
}


/* =========================================================
   BUTTON
   ========================================================= */

.stButton > button {
    width: 100%;
    height: 52px;
    border-radius: 15px;
    border: none;
    background: linear-gradient(135deg, #18a558, #0d8748);
    color: white;
    font-size: 16px;
    font-weight: 700;
    box-shadow: 0 10px 25px rgba(24, 165, 88, 0.25);
    transition: 0.25s ease;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 15px 30px rgba(24, 165, 88, 0.35);
}


/* =========================================================
   METRIC CARDS
   ========================================================= */

.metric-card {
    background: rgba(255, 255, 255, 0.92);
    border-radius: 22px;
    padding: 25px 15px;
    text-align: center;
    min-height: 140px;
    box-shadow: 0 12px 35px rgba(20, 100, 60, 0.09);
    border: 1px solid rgba(24, 165, 88, 0.08);
    transition: 0.25s ease;
}

.metric-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 18px 45px rgba(20, 100, 60, 0.15);
}

.metric-icon {
    font-size: 30px;
    margin-bottom: 8px;
}

.metric-label {
    color: #75847c;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 0.8px;
}

.metric-value {
    color: #12372a;
    font-size: 25px;
    font-weight: 800;
    margin-top: 6px;
}


/* =========================================================
   HEALTH SCORE
   ========================================================= */

.health-card {
    background: linear-gradient(135deg, #12372a, #17784d);
    color: white;
    border-radius: 26px;
    padding: 30px;
    margin-top: 30px;
    text-align: center;
    box-shadow: 0 18px 45px rgba(18, 55, 42, 0.20);
}

.health-score {
    font-size: 48px;
    font-weight: 800;
}

.health-label {
    font-size: 20px;
    font-weight: 700;
    margin-top: 5px;
}

.health-text {
    opacity: 0.85;
    margin-top: 8px;
}


/* =========================================================
   INFO CARDS
   ========================================================= */

.info-card {
    background: rgba(255, 255, 255, 0.92);
    border-radius: 22px;
    padding: 25px;
    margin-top: 22px;
    box-shadow: 0 12px 35px rgba(20, 100, 60, 0.08);
    border-left: 5px solid #18a558;
}

.info-title {
    color: #12372a;
    font-size: 19px;
    font-weight: 800;
    margin-bottom: 10px;
}

.info-text {
    color: #53665d;
    line-height: 1.7;
}


/* =========================================================
   FOOTER
   ========================================================= */

.footer {
    text-align: center;
    color: #72827a;
    font-size: 13px;
    margin-top: 55px;
    padding: 25px;
}


/* =========================================================
   MOBILE
   ========================================================= */

@media (max-width: 768px) {

    .hero {
        padding: 30px 22px;
    }

    .hero-title {
        font-size: 36px;
    }

    .hero-subtitle {
        font-size: 16px;
    }

}

</style>
""", unsafe_allow_html=True)


st.markdown(
    """
<div class="hero">
    <div class="hero-title">
        🥗 Recipe <span>Nutrition AI</span>
    </div>

    <div class="hero-subtitle">
        Discover calories, protein, carbohydrates, fats,
        vitamins, health score and personalized health insights
        from your favorite recipes — powered by AI.
    </div>
</div>
""",
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-title">🍽️ Analyze Your Recipe</div>',
    unsafe_allow_html=True
)

left, right = st.columns([1.45, 1], gap="large")


with left:

    st.markdown(
        '<div class="input-card">',
        unsafe_allow_html=True
    )

    recipe = st.text_input(
        "Recipe Name",
        placeholder="Example: Chicken Biryani, Pasta, Paneer Tikka..."
    )

    analyze_button = st.button(
        "✨ Analyze Nutrition"
    )

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )


with right:

    st.image(
        "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=900",
        use_container_width=True
    )


if analyze_button:

    recipe = clean_recipe_name(recipe)

    if not is_valid_recipe(recipe):

        st.warning("⚠️ Please enter a recipe first.")

        st.stop()


    with st.spinner("🤖 AI is analyzing your recipe..."):

        try:

            nutrition = agent.analyze_nutrition(recipe)

        except Exception as error:

            st.error(
                f"❌ AI Error: {error}"
            )

            st.stop()


    if not isinstance(nutrition, dict):

        st.error(
            "❌ AI returned an invalid result."
        )

        st.stop()


    st.markdown(
        '<div class="section-title">📊 Nutrition Analysis</div>',
        unsafe_allow_html=True
    )

    c1, c2, c3, c4 = st.columns(4)


    with c1:

        st.markdown(
            f"""
<div class="metric-card">
    <div class="metric-icon">🔥</div>
    <div class="metric-label">CALORIES</div>
    <div class="metric-value">{nutrition.get("calories", "N/A")}</div>
</div>
""",
            unsafe_allow_html=True
        )


    with c2:

        st.markdown(
            f"""
<div class="metric-card">
    <div class="metric-icon">💪</div>
    <div class="metric-label">PROTEIN</div>
    <div class="metric-value">{nutrition.get("protein", "N/A")}</div>
</div>
""",
            unsafe_allow_html=True
        )


    with c3:

        st.markdown(
            f"""
<div class="metric-card">
    <div class="metric-icon">🌾</div>
    <div class="metric-label">CARBS</div>
    <div class="metric-value">{nutrition.get("carbs", "N/A")}</div>
</div>
""",
            unsafe_allow_html=True
        )


    with c4:

        st.markdown(
            f"""
<div class="metric-card">
    <div class="metric-icon">🥑</div>
    <div class="metric-label">FAT</div>
    <div class="metric-value">{nutrition.get("fat", "N/A")}</div>
</div>
""",
            unsafe_allow_html=True
        )


    score = get_health_score(
        nutrition.get("health_score", 0)
    )

    label = health_label(score)


    st.markdown(
        f"""
<div class="health-card">
    <div class="health-score">❤️ {score}/100</div>
    <div class="health-label">{label}</div>
    <div class="health-text">Estimated Recipe Health Score</div>
</div>
""",
        unsafe_allow_html=True
    )


    st.markdown(
        '<div class="section-title">🌱 Additional Nutrition</div>',
        unsafe_allow_html=True
    )

    e1, e2, e3 = st.columns(3)


    with e1:
        st.metric(
            "🌱 Fiber",
            nutrition.get("fiber", "N/A")
        )


    with e2:
        st.metric(
            "🍬 Sugar",
            nutrition.get("sugar", "N/A")
        )


    with e3:
        st.metric(
            "🧂 Sodium",
            nutrition.get("sodium", "N/A")
        )


    v1, v2 = st.columns(2)


    with v1:

        st.markdown(
            f"""
<div class="info-card">
    <div class="info-title">💊 Vitamins</div>
    <div class="info-text">
        {nutrition.get("vitamins", "N/A")}
    </div>
</div>
""",
            unsafe_allow_html=True
        )


    with v2:

        st.markdown(
            f"""
<div class="info-card">
    <div class="info-title">⚠️ Possible Allergens</div>
    <div class="info-text">
        {nutrition.get("allergens", "N/A")}
    </div>
</div>
""",
            unsafe_allow_html=True
        )


    st.markdown(
        '<div class="section-title">📈 Nutrition Charts</div>',
        unsafe_allow_html=True
    )

    chart1, chart2 = st.columns(2)


    with chart1:

        try:

            fig = create_macro_chart(nutrition)

            if fig is not None:
                st.pyplot(fig)

        except Exception as error:

            st.info(
                f"Macro chart unavailable: {error}"
            )


    with chart2:

        try:

            fig2 = create_nutrition_bar_chart(nutrition)

            if fig2 is not None:
                st.pyplot(fig2)

        except Exception as error:

            st.info(
                f"Nutrition chart unavailable: {error}"
            )


    st.markdown(
        f"""
<div class="info-card">
    <div class="info-title">🥦 AI Health Tips</div>
    <div class="info-text">
        {nutrition.get("tips", "N/A")}
    </div>
</div>
""",
        unsafe_allow_html=True
    )


    st.markdown(
        f"""
<div class="info-card">
    <div class="info-title">🤖 AI Recommendation</div>
    <div class="info-text">
        {nutrition.get("recommendation", "N/A")}
    </div>
</div>
""",
        unsafe_allow_html=True
    )


    st.markdown(
        '<div class="section-title">📄 Your Nutrition Report</div>',
        unsafe_allow_html=True
    )


    try:

        pdf_data = create_pdf(
            recipe,
            nutrition
        )

        st.download_button(
            "📥 Download Nutrition Report",
            data=pdf_data,
            file_name="recipe_nutrition_report.pdf",
            mime="application/pdf"
        )

    except Exception as error:

        st.warning(
            f"PDF generation unavailable: {error}"
        )


    st.success(
        "✅ Analysis completed successfully!"
    )


st.markdown(
    """
<div class="footer">
    🥗 Recipe Nutrition AI
    <br><br>
    Powered by AI • Eat Smart • Stay Healthy 💚
</div>
""",
    unsafe_allow_html=True
)