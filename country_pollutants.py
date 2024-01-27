import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.io as pio
pio.templates.default = "plotly_dark"

df = pd.read_csv('air-pollution.csv', encoding='latin-1')

def pie_plot(category='', catg_type='', catg_aqi='', aqi_label='', title='', color=px.colors.sequential.Plotly3):

    # Filter by pollutant_category_type like Good or Moderate
    top_catg = df[df[category]==catg_type]

    # Sort by pollutant_aqi_value
    top_catg = top_catg.sort_values(catg_aqi, ascending=False)

    # Create the pie chart
    fig = px.pie(top_catg, values=catg_aqi, names='country',
                 title=title,
                 hover_data=[catg_aqi], labels={catg_aqi:aqi_label},
                 color_discrete_sequence=color)

    # Update the traces
    fig.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig)


def observations():
    with st.expander("OBSERVATIONS 🧐"):
        st.write(":blue[*Carbon Monoxide*]")
        st.write('''
            - None of the countries has their locations marked as belonging to one of the risky categories.
            - With a :green[**Good**] performance in all the countries, only the United States holds a
              bit larger percentage for the :orange[**Unhealthy for Sensitive Groups category.**]
            ''')
    
        st.divider()
        st.write(":blue[*Ozone*]")
        st.write('''
            - China demonstrated the worst conditions showing less than 40 percent; of the areas here
              are labeled from :orange[**Unhealthy for Sensitive Groups to Very Unhealthy**]. 
            - At the same time, more than 60 percent of the areas were described as within normal limits
              :green[**(Good to Moderate)**], so the situation is not so dramatic compared to the "Indian AQI".
            - Speaking of India, within this category, over 70 percent have :green[**Good O3**] conditions.
            ''')
    
        st.divider()
        st.write(':blue[*Nitrogen Dioxide*]')
        st.write('''
            - Relatively worse conditions with less :green[**Good NO2 levels (between 47 - 49)**] can be found
              in countries such as Indonesia, China, United States, and Brazil.
            - A minor percentage of :green[**Moderate NO2**] levels can be found in areas of the United States.
            ''')
    
        st.divider()
        st.write(':blue[*Atmospheric Particulate Matter*]')
        st.write('''
            - The worst conditions can be found in India, China, Indonesia, Mexico, and Pakistan where
              most of their areas are marked from :orange[**Unhealthy for Sensitive Groups to Very Unhealthy**]
              categories.
            - A very small percentage of areas have :green[**Moderate PM2.5**] levels for the above-mentioned
              countries.
            - Countries such as India, South Africa, Russia, Pakistan, and South Korea are marked with
              high PM2.5 levels for the :red[**Hazardous**] category. This warns the public to avoid all outdoor
              physical activities.
            ''')