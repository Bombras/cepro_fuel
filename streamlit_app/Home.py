import streamlit as st
from cepro_fuel.utils import (data_download
                              , check_for_errors_in_response
                              , info_type_enum)
from cepro_fuel.encyclopedia import test

st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)

st.write("### Welcome to Streamlit app that shows ČEPRO fuel stations and products! 👋")

st.sidebar.success("Select a page to display.")

st.markdown(
    """

    Lorem ipsum vole


"""
)

development = True # or False

st.session_state.encyclopedia_response = data_download(info_type = info_type_enum.encyclopedia, dev_mode=development)
st.session_state.stations_response = data_download(info_type = info_type_enum.stations, dev_mode=development)

st.markdown("#### Responses")

st.write(check_for_errors_in_response(response_json = st.session_state.encyclopedia_response))
st.write(check_for_errors_in_response(response_json = st.session_state.stations_response))