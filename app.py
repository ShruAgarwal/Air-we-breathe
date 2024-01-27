import streamlit as st
from country_pollutants import pie_plot, observations
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
import plotly.io as pio
pio.templates.default = "plotly_dark"

# PAGE CONFIG
st.set_page_config(
    page_title="Air We Breathe",
    page_icon="🍃")

# =========================
# SIDEBAR

st.sidebar.title("About 👀")
st.sidebar.markdown("""This app displays the levels of air pollution across the world
                    by using interactive maps and charts to showcase the
                    Air Quality Index (AQI) and different pollutants like NO2, CO, and others.
                    Discover the invisible threat to our environment and better understand
                    the air we breathe.""")

st.sidebar.markdown("**Made by** [Shruti Agarwal](https://www.linkedin.com/in/shruti-agarwal-bb7889237)")
st.sidebar.divider()

# Finishing up with info panels 
st.sidebar.header("Resources ✨")
st.sidebar.info(
    """The raw data is taken from [Kaggle](https://www.kaggle.com/datasets/hasibalmuzdadid/global-air-pollution-dataset) and 
    originally scraped from [here](https://www.elichens.com/)!"""
    )

st.sidebar.info(
    """
    Image icon is from [here](https://icons8.com/icon/BIlYIKuOI6sm/air-pollution)
    """
    )

# =========================
# APP TITLE
c1, c2 = st.columns([0.2, 3.5], gap="large")

with c1:
    st.image(
        'icon.png',
        width=80,
    )

with c2:
    st.title("The Air We Breathe")
    st.markdown("*Visualizing Global Air Pollution Levels*")

# =========================
# Load the data
df = pd.read_csv('air-pollution.csv', encoding='latin-1', index_col=0)


# ============== PLOTS ==============

with st.expander("About Air Pollution"):
    st.write("""Air Pollution is contamination of the indoor or outdoor environment by any chemical,
             physical, or biological agent that modifies the natural characteristics of the atmosphere.""")

# ---- AQI on World Map ----
st.subheader("Global Air Quality Index (AQI) ☁")
st.info("""The below world map shows how polluted the air currently is or
        how polluted it is forecast to become. As air pollution levels rise,
        so does the AQI, along with the associated public health risk.""")

world_aqi = pd.DataFrame(df.groupby("country")["aqi_value"].max())

fig = go.Figure(data=go.Choropleth(
    locations = df['country_code'].values.tolist(),
    z = world_aqi['aqi_value'].values.tolist(),
    text = df.index,
    colorscale = 'matter',  #Color_options: magenta, Agsunset, Tealgrn
    autocolorscale=False,
    marker_line_color='darkgray',
    marker_line_width=1,
    colorbar_title = 'AQI<br>Value',
))

fig.update_layout(
    geo=dict(
        showframe=True,
        showcoastlines=False,
        projection_type='natural earth'
    ),
    height=450,
    margin={"r":10,"t":0,"l":10,"b":50}
)

st.plotly_chart(fig)


# =========================
# ---- Exploring countries with diff. air pollutants' levels  ----

st.divider()
st.subheader("Countries with air pollutants' levels 🏭")
tab1, tab2, tab3, tab4 = st.tabs(["CO", "O3", "NO2", "PM2.5"])

with tab1:
    st.info("""Carbon Monoxide is a colorless and odorless gas.
            Outdoor, it is emitted in the air above all by cars, trucks and
            other vehicles or machineries that burn fossil fuels.
            Such items like kerosene and gas space heaters, gas stoves also
            release CO affecting indoor air quality.""")
    
    st.markdown('#### Explore the air quality of CO for different countries to know more!')
    choose_catg = st.selectbox('Select an air quality type 👇',
    ('Good', 'Moderate', 'Unhealthy for Sensitive Groups'))

    pie_plot(category='co_aqi_category', catg_type=choose_catg,
             catg_aqi='co_aqi_value', aqi_label='CO',
             title='CO Levels Globally')

with tab2:
    st.info("""The Ozone molecule is harmful for outdoor air quality (if outside of the ozone layer).
            Ground level ozone can provoke several health problems like chest pain,
            coughing, throat irritation and airway inflammation.""")
    
    st.markdown('#### Explore the air quality of O3 for different countries to know more!')
    choose_catg = st.selectbox('Select an air quality type 👇',
    ('Good', 'Moderate', 'Unhealthy for Sensitive Groups', 'Unhealthy', 'Very Unhealthy'))

    pie_plot(category='ozone_aqi_category', catg_type=choose_catg,
             catg_aqi='ozone_aqi_value', aqi_label='O3',
             title='Ozone O3 Levels Globally', color=px.colors.sequential.haline)
    
with tab3:
    st.info("""Nitrogen Dioxide is introduced into the air by natural phenomena
            like entry from stratosphere or lighting. At the surface level, however,
            NO2 forms from cars, trucks and buses emissions, power plants and
            off-road equipment. Exposure over short periods can aggravate
            respiratory diseases, like asthma.""")
    
    st.markdown('#### Explore the air quality of NO2 for different countries to know more!')
    choose_catg = st.selectbox('Select an air quality type 👇',
    ('Good', 'Moderate'))

    pie_plot(category='no2_aqi_category', catg_type=choose_catg,
             catg_aqi='no2_aqi_value', aqi_label='NO2',
             title='NO2 Levels Globally', color=px.colors.sequential.haline)

with tab4:
    st.info("""Atmospheric Particulate Matter, also known as atmospheric aerosol particles,
            are complex mixtures of small solid and liquid matter that get into the air.
            If inhaled they can cause serious heart and lungs problem.""")
    
    st.markdown('#### Explore the air quality of PM2.5 for different countries to know more!')
    choose_catg = st.selectbox('Select an air quality type 👇',
    ('Good', 'Moderate', 'Unhealthy for Sensitive Groups', 'Unhealthy', 'Very Unhealthy', 'Hazardous'))

    pie_plot(category='pm2_5_aqi_category', catg_type=choose_catg,
             catg_aqi='pm2_5_aqi_value', aqi_label='PM2.5',
             title='PM2.5 Levels Globally')

# Insights for above pie plots
observations()

# =========================
# ---- 8 Countries whose top 15 cities shows diff. air pollutants' levels  ----

def plot_bar(coc='', aqi=''):
    """Plots a Seaborn barplot for ."""

    # Filter data for specific country
    df_coc = df[df['country_code'] == coc]

    # Filter data for pollutant values
    cont_plot = pd.DataFrame(df_coc.groupby("city")[aqi].max())

    sns.set_theme(style='dark')
    plt.style.use('dark_background')
    sns_fig = plt.figure(figsize=(40, 20))
    
    sns.barplot(x=cont_plot.index,
                y=cont_plot[aqi].values,
                order=cont_plot.sort_values(aqi,ascending=False).index[:15],
                palette=("cool"))
    st.pyplot(sns_fig)

st.divider()
st.subheader('Represents Maximum Values from 8 Countries📊')

choose_coc = st.selectbox('Select a Country Code 👇',
    ('USA', 'IND', 'CHN', 'MYS', 'IDN', 'ZAF', 'RUS', 'BRA'))

st.success("""📌 USA: United States, IND: India, CHN: China,
           MYS: Malaysia, IDN: Indonesia, ZAF: South Africa,
           RUS: Russia, BRA: Brazil""")

col1, col2 = st.columns(2, gap='medium')

with col1:
    st.markdown(':blue[Top 15 Cities with max values of **CO**]')
    plot_bar(coc=choose_coc, aqi='co_aqi_value')

with col2:
    st.markdown('Top 15 Cities with max values of **O3**')
    plot_bar(coc=choose_coc, aqi='ozone_aqi_value')


col3, col4 = st.columns(2, gap='medium')

with col3:
    plot_bar(coc=choose_coc, aqi='no2_aqi_value')
    st.markdown('Top 15 Cities with max values of **NO2**')

with col4:
    plot_bar(coc=choose_coc, aqi='pm2_5_aqi_value')
    st.markdown(':blue[Top 15 Cities with max values of **PM2.5**]')