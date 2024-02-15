import pandas as pd
import streamlit as st
from enum import Enum, unique
import requests as req


@unique
class info_type_enum(Enum):
    encyclopedia = 'encyclopedia'
    stations = 'stations'

@unique
class request_body_enum(Enum):
    encyclopedia = '{"encyklopedie": {"full": true}, "version": 5}'
    stations = '{"search": {"exclude_cs_ceny": false,"exclude_cs_kvalita": false},"version": 5}'

@st.cache_data
def data_download(info_type: info_type_enum, dev_mode: bool):
    req_url = 'https://einfo.ceproas.cz/cepro_portal_ws/rest/common/prox/mobileData'
    req_header = {'authorization': 'Basic bW9iYXA6RVdpa0Ey',
              'content-type': 'application/json; charset=UTF-8',
              'accept-encoding': 'gzip',
              'user-agent': 'okhttp/4.9.0'}
    if dev_mode == True:
        # For development, load files from project
        response = pd.read_pickle(f'_data/{info_type.value}.pickle')
        return response.json()
    else:
        try:
            response = req.post(url=req_url, headers=req_header, data=request_body_enum[info_type.value].value, timeout = 10)
            response.raise_for_status()
            return response.json()
        except req.exceptions.Timeout as errrt:
            st.error("ERROR : ceproas.cz API - Request Time out. CEPRO server is down.")
            st.stop()
        except req.exceptions.RequestException:
            st.error('ERROR : Something went wrong.')
            st.stop()

def check_for_errors_in_response(response_json):
    #  check for errors in json files
    if response_json['success'] is not True:
        print(response_json['Error']['errorText'])
        return response_json['Error']['errorText']
    else:
        print("Response from Cepro success: ", response_json['success'])
        return str("Response from CEPRO server OK")
