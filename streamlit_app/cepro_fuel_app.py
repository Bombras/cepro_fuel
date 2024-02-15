# streamlit run ./cepro_fuel_app/cepro_fuel_app.py
from cepro_fuel.utils import filter_dataframe, info_type_enum, data_download, check_for_errors_in_response
import streamlit as st
import pandas as pd
import leafmap.foliumap as leafmap
import leafmap as lm

development = True # or False

encyclopedia_response = data_download(info_type = info_type_enum.encyclopedia, dev_mode=development)
stations_response = data_download(info_type = info_type_enum.stations, dev_mode=development)

check_for_errors_in_response(response_json = encyclopedia_response)
check_for_errors_in_response(response_json = stations_response)

"""
Data from stations
"""
stations_data = stations_response['Data']

products_list = pd.DataFrame(stations_data['cis_prod_list'])[['nazev_produkt', 'kod_produkt']]
gs_prices = pd.concat([
    pd.DataFrame(stations_data['cs_ceny']).explode('ceny').reset_index()
    , pd.DataFrame(pd.DataFrame(stations_data['cs_ceny']).explode('ceny')['ceny'].tolist()).reset_index()
    ]
    , axis=1)[['kod_cs', 'cena', 'kod_produkt']]
gs_prices = gs_prices.merge(products_list, how='inner', on='kod_produkt').drop('county_name', axis='columns', inplace=True)



product_quality_list = pd.DataFrame(stations_data['cis_kvalita_list'])[['jednotka_parametr', 'kod_parametr', 'nazev_parametr']]
gs_product_quality = pd.DataFrame()
for gs_product in stations_data['cs_kvalita']:
    gs_number = gs_product['kod_cs']
    product_quality_gs = pd.DataFrame(pd.DataFrame(gs_product['produkty']).explode('parametry')['parametry'].to_list())
    product_quality_gs['kod_cs'] = gs_number
    gs_product_quality = pd.concat([gs_product_quality,product_quality_gs], axis='index')
gs_product_quality = gs_product_quality.merge(product_quality_list, how='inner', on='kod_parametr')


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


