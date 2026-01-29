import streamlit as st
import pandas as pd
import pickle

st.set_page_config(initial_sidebar_state="collapsed", layout = "centered")

st.markdown(
    """
    <style>
    .block-container {
        padding-top: 1.9rem; 
        padding-bottom: 0rem;
    }
    .centered-title {
        text-align: center;
        font-size: 38px;
        font-weight: 600;
        color: white;
        margin-top: 0px;
        margin-bottom: 30px;
    }
    </style>
    """,
    unsafe_allow_html=True
)
st.markdown('<div class="centered-title">US House Price Prediction</div>', unsafe_allow_html=True)


@st.cache_resource
def load_data():
    return pd.read_csv("zillow_house_price_dataset.csv")

df = load_data()

df["zipcode"] = df["zipcode"].astype(str)

@st.cache_resource
def load_model():
    with open("model/model.pkl", "rb") as m:
        return pickle.load(m)

model = load_model()

beds_options = sorted(df["beds"].dropna().unique())
baths_options = sorted(df["baths"].dropna().unique())
zip_options = sorted(df["zipcode"].dropna().unique())
state_options = sorted(df["state"].dropna().unique())
city_options = sorted(df["city"].dropna().unique())

#Zipcode - city,state map 
zip_map = df[["zipcode", "city", "state"]].dropna().drop_duplicates()
zip_city_map = zip_map.set_index("zipcode")["city"].to_dict()
zip_state_map = zip_map.set_index("zipcode")["state"].to_dict()

city_state_map = df[["city", "state"]].dropna().drop_duplicates().set_index("city")["state"].to_dict()


living_area = st.number_input("Enter Living Area (sq.ft)", min_value=1, value=1000)
beds = st.selectbox("Select Bedroom(s)", beds_options)
baths = st.selectbox("Select Bathroom(s)", baths_options)
zipcode = st.selectbox("Select Zipcode", zip_options)

#Auto fill based on zip
auto_state = zip_state_map.get(zipcode)
auto_city = zip_city_map.get(zipcode)

st.text_input("City (Auto-filled)", value=auto_city, disabled=True)
st.text_input("State (Auto-filled)", value=auto_state, disabled=True)

if st.button("Predict Price"):

    #error checking
    if living_area <= 0:
        st.error("Living area must be greater than 0.")
    elif beds is None:
        st.error(" Please select the number of beds.")
    elif baths is None:
        st.error(" Please select the number of beds.")
    elif zipcode is None:
        st.error(" Please select the number of beds.")
    else:
        input_df = pd.DataFrame({
            "livingArea in sq.ft": [living_area],
            "beds": [beds],
            "baths": [baths],
            "state": [auto_state],
            "city": [auto_city]
        })

        try:
            prediction = model.predict(input_df)
            price = prediction[0]
            st.success(f"Predicted Price: $ {price:,.0f}")
        except Exception as e:
            st.error(f"Prediction failed: {e}")


st.markdown("<br>", unsafe_allow_html=True)
left_col, right_col = st.columns([4, 1])

with right_col:
    if st.button("Next", use_container_width=True):
        st.switch_page("pages/tableau1.py")