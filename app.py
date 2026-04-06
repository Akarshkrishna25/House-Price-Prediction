import streamlit as st
import pandas as pd
import joblib

# -------------------- CONFIG (FIRST LINE) --------------------
st.set_page_config(
    page_title="🏠 House Price Predictor | ML App",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# -------------------- CSS --------------------
st.markdown("""
<style>
.stButton > button {
    background: linear-gradient(135deg, #ff4b4b, #ff914d);
    color: white;
    font-size: 18px;
    font-weight: bold;
    border-radius: 12px;
    padding: 12px;
    border: none;
    width: 100%;
    transition: 0.3s ease;
}
.stButton > button:hover {
    transform: scale(1.05);
    background: linear-gradient(135deg, #ff2e2e, #ff7a1a);
}
.result-box {
    background: #1c1f26;
    padding: 20px;
    border-radius: 15px;
    text-align: center;
    font-size: 26px;
    color: #00FFAA;
    font-weight: bold;
    margin-top: 20px;
}
</style>
""", unsafe_allow_html=True)

# -------------------- LOAD --------------------
with open("Rf_model.joblib","rb") as file:
    model = joblib.load(file)

df = pd.read_csv("cleaned_df.csv")

# -------------------- HEADER --------------------
st.markdown("<h1 style='text-align:center;'>🏠 House Price Prediction</h1>", unsafe_allow_html=True)

col_img, col_title = st.columns([1,2])

with col_img:
    st.image("house.png", width=250)

with col_title:
    st.markdown("### Predict house prices instantly using ML")

# -------------------- INPUT --------------------
with st.container(border=True):

    col1, col2 = st.columns(2)

    with col1:
        location = st.selectbox("📍 Location", df["location"].unique())
        sqft = st.number_input("📐 Square Feet", min_value=300)

    with col2:
        bath = st.selectbox("🛁 Bathrooms", sorted(df["bath"].unique()))
        bhk = st.selectbox("🛏 Bedrooms", sorted(df["bhk"].unique()))

# -------------------- ENCODING --------------------
def get_encoded_loc(location):
    return df[df["location"] == location]["encoded_loc"].values[0]

encode = get_encoded_loc(location)

# -------------------- BUTTON CENTER --------------------
col1, col2, col3 = st.columns([1,2,1])

with col2:
    clicked = st.button("🚀 Predict Price")

# -------------------- PREDICTION --------------------
if clicked:
    input_data = [[sqft, bath, bhk, encode]]
    pred = model.predict(input_data)[0]

    price = round(pred * 100000, 2)

    st.markdown(f"""
        <div class="result-box">
            💰 Predicted Price: ₹ {price:,.0f}
        </div>
    """, unsafe_allow_html=True)