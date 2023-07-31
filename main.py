import folium
import numpy as np
import pandas as pd
import streamlit as st
import geopandas as gpd
from datetime import date
from streamlit_folium import st_folium

GEOJSON_PATH = "./data/japan.geojson"
DATASETS_PATH = "./data/japan_covid_19_cases_daily.csv"
STYLE_FUNC = lambda x: {'fillColor': '#ffffff', 
                            'color':'#000000', 
                            'fillOpacity': 0.1, 
                            'weight': 0.1}
HIGHLIGHT_FUNC = lambda x: {'fillColor': '#000000', 
                                'color':'#000000', 
                                'fillOpacity': 0.50, 
                                'weight': 0.1}


@st.cache_data
def get_geojson():
    gpd_df = gpd.read_file(GEOJSON_PATH)
    return gpd_df

@st.cache_data
def get_datasets():
    df = pd.read_csv(DATASETS_PATH)
    df["Date"] = pd.to_datetime(df["Date"]).dt.date
    return df

st.set_page_config(
    page_title="指定期間の都道府県別の新型コロナ感染割合",
    page_icon="🗾",
    layout="wide"
)

map = folium.Map(
    location=(36.56583, 139.88361),
    tiles="cartodbpositron",
    zoom_start=5
)

geojson = get_geojson()
df = get_datasets()

placeholder = st.empty()
map_col, menu_col = placeholder.columns([4, 1])

with menu_col:
    st.header("絞り込み")
    start_date = st.date_input(
        '開始日',
        min_value=df["Date"].min(),
        max_value=df["Date"].max(),
        value=df["Date"].min(),
        key="start_date"
    )
    end_date = st.date_input(
        '終了日',
        min_value=df["Date"].min(),
        max_value=df["Date"].max(),
        value=df["Date"].max(),
        key="end_date"
    )

with map_col:
    if st.session_state["start_date"] and st.session_state["end_date"]:
        start_date = st.session_state["start_date"]
        end_date = st.session_state["end_date"]
        df = df[(df["Date"] >= start_date) & (df["Date"] <= end_date)]

    if len(df) <= 0:
        st.markdown("# 該当データなし")
    else:
        df_group = df.groupby(["Prefecture_name", "Prefecture_code"], as_index=False)
        df_group = df_group.agg({
            'Infections': 'sum'
        })
        df_group.sort_values("Infections", inplace=True, ascending=False)
        df_group["Infections_logarithm"] = np.log(df_group["Infections"])
        df_group[df_group["Infections_logarithm"] == -np.inf] = 0
        df_group["Infections_Percentage"] = 100 * df_group["Infections"] / df_group["Infections"].sum()

        folium.Choropleth(
            geo_data=geojson,
            data=df_group,
            columns=["Prefecture_code", "Infections_logarithm"],
            key_on="feature.properties.id",
            fill_color='YlOrRd',
            nan_fill_color='darkgray',
            fill_opacity=0.8,
            nan_fill_opacity=0.8,
            line_opacity=0.2,
        ).add_to(map)

        df_geojson = pd.merge(
            geojson.loc[:,['id', 'nam_ja', 'geometry']], df_group,
            right_on="Prefecture_code",
            left_on="id",
        )

        choropleth_info = folium.GeoJson(
            data=df_geojson,
            style_function=STYLE_FUNC,
            highlight_function=HIGHLIGHT_FUNC,
            control=False,
            tooltip=folium.GeoJsonTooltip(
                fields=["nam_ja", "Infections", "Infections_Percentage", "Infections_logarithm"],
                aliases=['都道府県名: ', '感染者数: ', '全国の割合: ', '対数スケール: '],
                labels=True,
                sticky=True,
                style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;"), 
            )
        )
        map.add_child(choropleth_info)
        map.keep_in_front(choropleth_info)

        st_folium(map, use_container_width=True, height=720, returned_objects=[])
