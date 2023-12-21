# streamlit run ./cepro_fuel_app/cepro_fuel_app.py
from src.utils import filter_dataframe, info_type_enum, data_download
import streamlit as st
import pandas as pd
import requests as req
import copy
import leafmap.foliumap as leafmap
import os
import leafmap as lm
import argparse

parser = argparse.ArgumentParser()

parser.add_argument(
    "--dev",
    action="append",
    default=[],
    help="Start development mode",
)

try:
    args = parser.parse_args()
except SystemExit as e:
    os._exit(e.code)



data_download(info_type = info_type_enum.encyclopedia, development=True)
data_download(info_type = info_type_enum.stations, development=True)




# # for development
# all_gs = copy.deepcopy(response_gas_stations.json())
# encyclopedia_info = copy.deepcopy(response_encyclopedia.json())

# # check for errors in json files
# if all_gs['success'] is not True:
#     error_msg_all_gs = all_gs['Error']['errorText']
#     print(error_msg_all_gs)

# if encyclopedia_info['success'] is not True:
#     error_msg_encyclopedia_info = encyclopedia_info['Error']['errorText']
#     print(error_msg_encyclopedia_info)

# # gas stations
# data_gs = all_gs['Data']

# # product list
# products_list = pd.DataFrame(data_gs['cis_prod_list'])

# # fuel prices
# gs_prices = pd.concat([
#     pd.DataFrame(data_gs['cs_ceny']).explode('ceny').reset_index()
#     , pd.DataFrame(pd.DataFrame(data_gs['cs_ceny']).explode('ceny')['ceny'].tolist()).reset_index()
#     ]
#     , axis=1)[['kod_cs', 'cena', 'kod_produkt']]
# gs_prices = gs_prices.merge(products_list, how='inner', on='kod_produkt')



# # Product quality list
# product_quality_list = pd.DataFrame(data_gs['cis_kvalita_list'])

# # product quality
# gs_product_quality = pd.DataFrame()
# for gs_product in data_gs['cs_kvalita']:
#     gs_number = gs_product['kod_cs']
#     product_quality_gs = pd.DataFrame(pd.DataFrame(gs_product['produkty']).explode('parametry')['parametry'].to_list())
#     product_quality_gs['kod_cs'] = gs_number
#     gs_product_quality = pd.concat([gs_product_quality,product_quality_gs], axis='index')
# gs_product_quality = gs_product_quality.merge(product_quality_list, how='inner', on='kod_parametr')

# # gas station location
# gs_adress_wo_gps = pd.DataFrame(data_gs['cs_fix_list']).reset_index()
# gs_adress = pd.concat([gs_adress_wo_gps, pd.DataFrame(gs_adress_wo_gps['GPS'].tolist())], axis=1)
# del(gs_adress_wo_gps)

# # encyclopedia
# # info = encyclopedia_info['Encyklopedie']
# # for i in info['tree']:
# #     if i['parent'] == 'root':
# #         root = pd.DataFrame(i['children'])
# #     if i['parent'] == 'produkt':
# #         product = pd.DataFrame(i['children'])
# #     if i['parent'] == 'kvalita':
# #         quality = pd.DataFrame(i['children'])
# #     if i['parent'] == 'kvalita:natural95':
# #         quality_95 = pd.DataFrame(i['children'])
# #     if i['parent'] == 'kvalita:optimal_diesel':
# #         quality_diesel = pd.DataFrame(i['children'])




# st.set_page_config(layout="wide")

# st.sidebar.info(
#     """
#     - Web App URL: <https://streamlit.geemap.org>
#     - GitHub repository: <https://github.com/giswqs/streamlit-geospatial>
#     """
# )

# st.sidebar.title("Contact")
# st.sidebar.info(
#     """
#     Qiusheng Wu: <https://wetlands.io>
#     [GitHub](https://github.com/giswqs) | [Twitter](https://twitter.com/giswqs) | [YouTube](https://www.youtube.com/c/QiushengWu) | [LinkedIn](https://www.linkedin.com/in/qiushengwu)
#     """
# )

# st.title("EuroOil stanice")

# if "stations" not in st.session_state:
#     st.session_state["stations"] = None

# gs_filtered = filter_dataframe(gs_adress)
# st.session_state["stations"] = gs_filtered

# st.dataframe(gs_filtered[['kraj', 'obec', 'okres']].drop_duplicates())
# st.dataframe(gs_filtered)

# from folium import Map, Marker
# from streamlit_folium import st_folium

# st.title("Marker Cluster")

# map = Map(center=[50, 16], zoom_start=15)
# for i in range(len(gs_filtered)):
#     location = gs_filtered.iloc[i,12], gs_filtered.iloc[i,11]
#     Marker(location=location, tooltip=gs_filtered.iloc[i,9]).add_to(map)
# # https://python-visualization.github.io/folium/latest/user_guide/ui_elements/popups.html

# st_folium(map, width = 700)


