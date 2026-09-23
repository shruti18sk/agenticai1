from dotenv import load_dotenv
import streamlit as st

from langchain_google_genai import ChatGoogleGenerativeAI


load_dotenv()


st.set_page_config(
    page_title="Blood Work Analyzer",
    page_icon="🩺",
    layout="wide"
)


# =========================================================
# MODEL
# =========================================================

llm = ChatGoogleGenerativeAI(
    model="gemma-4-31b-it",
    timeout=120,
    max_retries=0
)


# =========================================================
# CSS
# =========================================================

st.markdown("""
<style>

/* =====================================================
   MAIN BACKGROUND
===================================================== */

.stApp {
    background: #05070B;
    color: #EAF4FF;
    overflow-x: hidden;
}


/* =====================================================
   ANIMATED NEON BACKGROUND
===================================================== */

.stApp::before {

    content: "";

    position: fixed;

    width: 520px;
    height: 520px;

    left: -250px;
    top: 25%;

    border: 1px solid rgba(21, 151, 229, 0.35);

    border-radius: 50%;

    box-shadow:
        0 0 35px rgba(21, 151, 229, 0.16),
        0 0 90px rgba(21, 151, 229, 0.08);

    pointer-events: none;

    z-index: 0;

    animation:
        orbitLeft 7s ease-in-out infinite;
}


.stApp::after {

    content: "";

    position: fixed;

    width: 430px;
    height: 430px;

    right: -190px;
    bottom: 5%;

    border: 1px solid rgba(73, 185, 255, 0.30);

    border-radius: 50%;

    box-shadow:
        0 0 40px rgba(73, 185, 255, 0.15),
        0 0 100px rgba(73, 185, 255, 0.08);

    pointer-events: none;

    z-index: 0;

    animation:
        orbitRight 6s ease-in-out infinite;
}


@keyframes orbitLeft {

    0% {
        transform: translate(0px, -20px) scale(0.9);
        opacity: 0.45;
    }

    50% {
        transform: translate(80px, 20px) scale(1.12);
        opacity: 0.85;
    }

    100% {
        transform: translate(0px, -20px) scale(0.9);
        opacity: 0.45;
    }
}


@keyframes orbitRight {

    0% {
        transform: translate(0px, 20px) scale(0.9);
        opacity: 0.35;
    }

    50% {
        transform: translate(-70px, -30px) scale(1.15);
        opacity: 0.8;
    }

    100% {
        transform: translate(0px, 20px) scale(0.9);
        opacity: 0.35;
    }
}


/* =====================================================
   CONTENT ABOVE BACKGROUND
===================================================== */

.block-container {
    position: relative;
    z-index: 2;

    max-width: 1400px;

    padding-top: 38px;
    padding-bottom: 45px;
}


/* =====================================================
   HEADER
===================================================== */

.main-title {

    text-align: center;

    color: #F2F7FF;

    font-size: 46px;

    font-weight: 750;

    letter-spacing: -1.5px;

    margin-bottom: 7px;

    animation:
        titleEnter 0.8s ease-out;
}


.subtitle {

    text-align: center;

    color: #78C7FF;

    font-size: 17px;

    letter-spacing: 0.2px;

    margin-bottom: 45px;

    animation:
        subtitleEnter 1s ease-out;
}


@keyframes titleEnter {

    from {
        opacity: 0;
        transform: translateY(-25px) scale(0.96);
    }

    to {
        opacity: 1;
        transform: translateY(0) scale(1);
    }
}


@keyframes subtitleEnter {

    from {
        opacity: 0;
        transform: translateY(15px);
    }

    to {
        opacity: 1;
        transform: translateY(0);
    }
}


/* =====================================================
   SECTION TITLES
===================================================== */

.section-title {

    color: #EAF4FF;

    font-size: 21px;

    font-weight: 700;

    margin-bottom: 13px;

    letter-spacing: 0.2px;
}


/* =====================================================
   TEXT AREA
===================================================== */

div[data-testid="stTextArea"] textarea {

    background: #0B1220 !important;

    color: #EAF4FF !important;

    border: 1px solid #29496B !important;

    border-radius: 18px !important;

    padding: 18px !important;

    font-size: 15px !important;

    line-height: 1.6 !important;

    min-height: 420px !important;

    box-shadow:
        0 10px 35px rgba(0, 0, 0, 0.45),
        0 0 25px rgba(21, 151, 229, 0.04);

    transition:
        border-color 0.25s ease,
        box-shadow 0.25s ease,
        transform 0.25s ease;
}


div[data-testid="stTextArea"] textarea:hover {

    border-color: #3975A8 !important;

    box-shadow:
        0 0 25px rgba(21, 151, 229, 0.15),
        0 12px 40px rgba(0, 0, 0, 0.45);

    transform: translateY(-1px);
}


div[data-testid="stTextArea"] textarea:focus {

    border-color: #1597E5 !important;

    box-shadow:
        0 0 0 2px rgba(21, 151, 229, 0.12),
        0 0 35px rgba(21, 151, 229, 0.20) !important;
}


div[data-testid="stTextArea"] textarea::placeholder {
    color: #5D7895 !important;
}


/* =====================================================
   ANALYZE BUTTON
===================================================== */

div.stButton > button {

    width: 100%;

    height: 55px;

    margin-top: 13px;

    border-radius: 13px;

    background: #1597E5;

    color: #FFFFFF;

    border: 1px solid #49B9FF;

    font-size: 16px;

    font-weight: 700;

    letter-spacing: 0.2px;

    box-shadow:
        0 0 18px rgba(21, 151, 229, 0.25);

    transition:
        all 0.2s ease;
}


div.stButton > button:hover {

    background: #20A4F3;

    color: #FFFFFF;

    transform: translateY(-3px);

    box-shadow:
        0 0 25px rgba(21, 151, 229, 0.55),
        0 0 55px rgba(21, 151, 229, 0.20);
}


div.stButton > button:active {

    transform: translateY(1px);
}


/* =====================================================
   RESULT BOXES
===================================================== */

div[data-testid="stVerticalBlockBorderWrapper"] {

    background: #080E18 !important;

    border: 1px solid #243B5A !important;

    border-radius: 18px !important;

    box-shadow:
        0 10px 35px rgba(0, 0, 0, 0.45),
        inset 0 0 30px rgba(21, 151, 229, 0.025);

    transition:
        border-color 0.3s ease,
        box-shadow 0.3s ease,
        transform 0.3s ease;
}


div[data-testid="stVerticalBlockBorderWrapper"]:hover {

    border-color: #3975A8 !important;

    box-shadow:
        0 0 30px rgba(21, 151, 229, 0.12),
        0 15px 45px rgba(0, 0, 0, 0.5);
}


/* =====================================================
   RESULT TEXT
===================================================== */

div[data-testid="stVerticalBlockBorderWrapper"] p {

    color: #DCEBFA;

    line-height: 1.65;
}


div[data-testid="stVerticalBlockBorderWrapper"] strong {

    color: #F2F7FF;
}


div[data-testid="stVerticalBlockBorderWrapper"] h1,
div[data-testid="stVerticalBlockBorderWrapper"] h2,
div[data-testid="stVerticalBlockBorderWrapper"] h3 {

    color: #78C7FF;
}


/* =====================================================
   PLACEHOLDER
===================================================== */

.placeholder {

    height: 270px;

    display: flex;

    flex-direction: column;

    align-items: center;

    justify-content: center;

    text-align: center;

    color: #64748B;

    font-size: 15px;

    animation: placeholderPulse 2.5s ease-in-out infinite;
}


.placeholder-icon {

    font-size: 48px;

    margin-bottom: 16px;

    filter:
        drop-shadow(0 0 10px rgba(73, 185, 255, 0.35));
}


@keyframes placeholderPulse {

    0%, 100% {
        opacity: 0.55;
        transform: translateY(0) scale(1);
    }

    50% {
        opacity: 1;
        transform: translateY(-8px) scale(1.05);
    }
}


/* =====================================================
   ANALYSIS COMPLETE
===================================================== */

.analysis-result {

    background: #0B1220;

    border: 1px solid #1597E5;

    border-radius: 15px;

    padding: 18px 20px;

    margin-top: 18px;

    box-shadow:
        0 0 20px rgba(21, 151, 229, 0.10);

    animation:
        resultEnter 0.5s ease-out;
}


.analysis-title {

    color: #78C7FF;

    font-size: 17px;

    font-weight: 700;

    margin-bottom: 7px;
}


.analysis-text {

    color: #8FAAC2;

    font-size: 14px;

    line-height: 1.5;
}


@keyframes resultEnter {

    from {
        opacity: 0;
        transform: translateY(15px);
        box-shadow: 0 0 0 rgba(21, 151, 229, 0);
    }

    to {
        opacity: 1;
        transform: translateY(0);
        box-shadow: 0 0 20px rgba(21, 151, 229, 0.10);
    }
}


/* =====================================================
   SPINNER
===================================================== */

div[data-testid="stSpinner"] {

    color: #78C7FF !important;
}


/* =====================================================
   ALERTS
===================================================== */

div[data-testid="stAlert"] {

    background: #0B1220 !important;

    color: #DCEBFA !important;

    border: 1px solid #29496B !important;

    border-radius: 13px !important;
}


/* =====================================================
   SCROLLBAR
===================================================== */

::-webkit-scrollbar {
    width: 7px;
}


::-webkit-scrollbar-track {
    background: #05070B;
}


::-webkit-scrollbar-thumb {

    background: #243B5A;

    border-radius: 10px;
}


::-webkit-scrollbar-thumb:hover {
    background: #1597E5;
}


/* =====================================================
   FOOTER
===================================================== */

.footer {

    text-align: center;

    color: #4F6B85;

    font-size: 13px;

    margin-top: 35px;

    padding-bottom: 10px;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# SESSION STATE
# =========================================================

if "health_report" not in st.session_state:
    st.session_state.health_report = None

if "diet_plan" not in st.session_state:
    st.session_state.diet_plan = None

if "analyzed" not in st.session_state:
    st.session_state.analyzed = False


# =========================================================
# HEADER
# =========================================================

st.markdown(
    '<div class="main-title">🩺 Blood Work Analyzer</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Understand your blood report with AI-powered analysis and personalized dietary guidance</div>',
    unsafe_allow_html=True
)


# =========================================================
# COLUMNS
# =========================================================

left, right = st.columns(
    [1, 1],
    gap="large"
)


# =========================================================
# LEFT
# =========================================================

with left:

    st.markdown(
        '<div class="section-title">📄 Your Blood Report</div>',
        unsafe_allow_html=True
    )

    document = st.text_area(
        "Blood Report",
        height=420,
        label_visibility="collapsed",
        placeholder="""Paste your complete blood report here...

Example:

Hemoglobin: 15.1 g/dL
Reference Range: 13.5-17.5

WBC: 6.8 x10^3/uL
Reference Range: 4.5-11.0

Total Cholesterol: 238 mg/dL
Reference Range: <200

LDL Cholesterol: 162 mg/dL
Reference Range: <100

HDL Cholesterol: 36 mg/dL
Reference Range: >40

Paste your full report here..."""
    )

    analyze = st.button(
        "🔍  Analyze My Report",
        use_container_width=True
    )


    # -----------------------------------------------------
    # ANALYSIS STATUS
    # -----------------------------------------------------

    if st.session_state.analyzed:

        st.markdown(
            """
<div class="analysis-result">
    <div class="analysis-title">
        ✓ Analysis Complete
    </div>
    <div class="analysis-text">
        Your blood report has been analyzed successfully.
        Your health report and personalized diet plan are ready.
    </div>
</div>
""",
            unsafe_allow_html=True
        )


# =========================================================
# RIGHT
# =========================================================

with right:

    # =====================================================
    # HEALTH REPORT
    # =====================================================

    st.markdown(
        '<div class="section-title">📊 Health Report</div>',
        unsafe_allow_html=True
    )

    health_box = st.container(
        height=360,
        border=True
    )

    with health_box:

        if st.session_state.health_report:

            st.markdown(
                st.session_state.health_report
            )

        else:

            st.markdown(
                """
<div class="placeholder">
    <div class="placeholder-icon">🧪</div>
    <div>Your blood analysis will appear here</div>
</div>
""",
                unsafe_allow_html=True
            )


    # =====================================================
    # DIET PLAN
    # =====================================================

    st.markdown(
        '<div class="section-title">🥗 Diet Plan</div>',
        unsafe_allow_html=True
    )

    diet_box = st.container(
        height=360,
        border=True
    )

    with diet_box:

        if st.session_state.diet_plan:

            st.markdown(
                st.session_state.diet_plan
            )

        else:

            st.markdown(
                """
<div class="placeholder">
    <div class="placeholder-icon">🥗</div>
    <div>Your personalized diet plan will appear here</div>
</div>
""",
                unsafe_allow_html=True
            )


# =========================================================
# LLM ANALYSIS
# =========================================================

if analyze:

    if not document.strip():

        st.warning(
            "Please paste your blood report first."
        )

    else:

        extraction_report = f"""
You are a medical laboratory data extraction assistant.

Extract EVERY laboratory test and result from the blood report below.

For each test, provide:
- Test Name
- Value
- Unit
- Reference Range
- Status: HIGH, LOW, or NORMAL

Rules:
- Extract every test; do not skip normal results.
- Use ONLY the reference range printed in the report.
- Below range = LOW, above range = HIGH, within range = NORMAL.
- Do not invent reference ranges.
- Preserve the exact value and unit as reported.
- Include qualitative results such as Positive, Negative, Reactive, Non-reactive, etc.
- Do not diagnose or give treatment advice.
- If a value or reference range cannot be determined, write "Unable to determine".

Format:

### Laboratory Results

- Test Name: [value] [unit] | Status: [HIGH/LOW/NORMAL] | Reference: [range]

### Summary

Total tests: [number]
High: [number]
Low: [number]
Normal: [number]
Unable to classify: [number]

### Abnormal Results Only

- Test Name: [value] [unit] — [HIGH/LOW] | Reference: [range]

Blood Report:

{document}
"""


        with st.spinner("🧬 Analyzing your blood report..."):

            try:

                # STAGE 1
                response = llm.invoke(
                    extraction_report
                )

                model_output_report = response.text


                # STAGE 2
                diet_prompt = f"""
You are a clinical nutritionist specializing in Indian dietary habits.

Based on the blood work analysis below, write:

1. A short health summary in 4-5 lines explaining the patient's condition in simple language.

2. A short, practical Indian diet plan having only two sections:

(1) Foods to avoid

(2) Foods to eat more of.

Do not include any other sections in the diet plan.

Blood Work Analysis:

{model_output_report}
"""


                diet_response = llm.invoke(
                    diet_prompt
                )

                model_output_diet = diet_response.text


                # SAVE
                st.session_state.health_report = model_output_report
                st.session_state.diet_plan = model_output_diet
                st.session_state.analyzed = True


                # REFRESH
                st.rerun()


            except Exception as e:

                st.error(
                    f"Something went wrong: {e}"
                )


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
<div class="footer">
    AI-powered blood work analysis • For informational purposes only
</div>
""",
    unsafe_allow_html=True
)