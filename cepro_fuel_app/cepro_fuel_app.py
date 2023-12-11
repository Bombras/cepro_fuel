import streamlit as st
import pandas as pd
import requests as req
import copy
import leafmap.foliumap as leafmap
import os
import leafmap as lm


req_url = 'https://einfo.ceproas.cz/cepro_portal_ws/rest/common/prox/mobileData'
req_header = {'authorization': 'Basic bW9iYXA6RVdpa0Ey',
              'content-type': 'application/json; charset=UTF-8',
              'accept-encoding': 'gzip',
              'user-agent': 'okhttp/4.9.0'}
json_body_encyclopedia = '{"encyklopedie": {"full": true}, "version": 5}'
json_body_stations = '{"search": {"exclude_cs_ceny": false,"exclude_cs_kvalita": false},"version": 5}'

# try:
#     response_gas_stations = req.post(url=req_url, headers=req_header, data=json_body_stations, timeout = 10)
#     response_encyclopedia = req.post(url=req_url, headers=req_header, data=json_body_encyclopedia, timeout = 10)
#     response_gas_stations.raise_for_status()
#     response_encyclopedia.raise_for_status()
# except req.exceptions.Timeout as errrt:
#     print("ERROR : ceproas.cz API - Request Time out. CEPRO server is down.")
# except req.exceptions.RequestException:
#     print('ERROR : Something went wrong.')


response_gas_stations = pd.read_pickle('notebooks/_data/response_gas_stations.pickle')
response_encyclopedia = pd.read_pickle('notebooks/_data/response_encyclopedia.pickle')


# for development
all_gs = copy.deepcopy(response_gas_stations.json())
encyclopedia_info = copy.deepcopy(response_encyclopedia.json())

# check for errors in json files
if all_gs['success'] is not True:
    error_msg_all_gs = all_gs['Error']['errorText']
    print(error_msg_all_gs)

if encyclopedia_info['success'] is not True:
    error_msg_encyclopedia_info = encyclopedia_info['Error']['errorText']
    print(error_msg_encyclopedia_info)

# gas stations
data_gs = all_gs['Data']

# fuel prices
gs_prices = pd.concat([
    pd.DataFrame(data_gs['cs_ceny']).explode('ceny').reset_index()
    , pd.DataFrame(pd.DataFrame(data_gs['cs_ceny']).explode('ceny')['ceny'].tolist()).reset_index()
    ]
    , axis=1)[['kod_cs', 'cena', 'kod_produkt']]

# product list
products_list = pd.DataFrame(data_gs['cis_prod_list'])

# product quality
gs_product_quality = pd.DataFrame()
for gs_product in data_gs['cs_kvalita']:
    gs_number = gs_product['kod_cs']
    product_quality_gs = pd.DataFrame(pd.DataFrame(gs_product['produkty']).explode('parametry')['parametry'].to_list())
    product_quality_gs['kod_cs'] = gs_number
    gs_product_quality = pd.concat([gs_product_quality,product_quality_gs], axis='index')

# gas station location
gs_adress_wo_gps = pd.DataFrame(data_gs['cs_fix_list']).reset_index()
gs_adress = pd.concat([gs_adress_wo_gps, pd.DataFrame(gs_adress_wo_gps['GPS'].tolist())], axis=1)
del(gs_adress_wo_gps)

# Pruct quality list
product_quality_list = data_gs['cis_kvalita_list']


# encyclopedia
# info = encyclopedia_info['Encyklopedie']
# for i in info['tree']:
#     if i['parent'] == 'root':
#         root = pd.DataFrame(i['children'])
#     if i['parent'] == 'produkt':
#         product = pd.DataFrame(i['children'])
#     if i['parent'] == 'kvalita':
#         quality = pd.DataFrame(i['children'])
#     if i['parent'] == 'kvalita:natural95':
#         quality_95 = pd.DataFrame(i['children'])
#     if i['parent'] == 'kvalita:optimal_diesel':
#         quality_diesel = pd.DataFrame(i['children'])




st.set_page_config(layout="wide")

st.sidebar.info(
    """
    - Web App URL: <https://streamlit.geemap.org>
    - GitHub repository: <https://github.com/giswqs/streamlit-geospatial>
    """
)

st.sidebar.title("Contact")
st.sidebar.info(
    """
    Qiusheng Wu: <https://wetlands.io>
    [GitHub](https://github.com/giswqs) | [Twitter](https://twitter.com/giswqs) | [YouTube](https://www.youtube.com/c/QiushengWu) | [LinkedIn](https://www.linkedin.com/in/qiushengwu)
    """
)

st.title("Marker Cluster")

st.filter_dataframe(data=gs_adress)

m = lm.Map(center=[50, 16], zoom=7, )

m.add_points_from_xy(
    gs_adress,
    x="long_dec",
    y="lat_dec",
    # color_column='region',
    # icon_names=['gear', 'map', 'leaf', 'globe'],
    spin=True,
    add_legend=True,
    )

m.to_streamlit(height=550)