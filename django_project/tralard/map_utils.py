import json
import random

import folium
from folium import plugins

from tralard.models.ward import Ward
from tralard.models.district import District
from tralard.models.beneficiary import Beneficiary


def prepare_marker_data():
    district_details = District.objects.all()

    # Prepare this data from a queryset either for
    # District or wards or both + Provincial coordinates - from model_name
    # https://latitude.to/articles-by-country/zm/zambia/page/5
    # i.e: record = District.objects.all() - when model_name=District ...

    data = {}
    # work in progress
    for geo_data in district_details:
        data[f"{geo_data.name}"] = [
            geo_data.location.x,
            geo_data.location.y,
            random.choice(["business-firm", "cooperative"]),
        ]

    return data


def prepare_map_layers():
    # intitiate default layers or custom shapefiles to load as onto the map
    # Note: these are default to folium and we just initiate them,
    # it would need more processing to prepare custom shapefiles from QGIS
    map_layers = [
        "CartoDB Positron",
        "Open Street Map",
        "Stamen Terrain",
        "Stamen Toner",
        "Stamen Watercolor",
        "CartoDB Dark_Matter",
    ]

    return map_layers


def build_map_context():

    # add base map
    map = folium.Map(
        # bounding box for map of zambia
        location=[-13.1519165, 27.852537499999983],
        tiles="cartodbpositron",
        zoom_start=6.5,
        # max_bounds=True
    )

    map_layers = prepare_map_layers()
    for map_layer in map_layers:
        folium.raster_layers.TileLayer(map_layer).add_to(map)

    mini_map = plugins.MiniMap(toggle_display=True)

    # clustering
    marker_cluster = plugins.MarkerCluster().add_to(map)

    # Search widget
    search = plugins.Search(
        marker_cluster,
        search_label=None,
        search_zoom=None,
        geom_type="Point",
        position="topleft",
        placeholder="Search district",
        collapsed=False,
    )

    search.add_to(map)

    # Draw tools
    draw = plugins.Draw(export=False)

    draw.add_to(map)

    # search.add_to(map)

    locate = plugins.LocateControl(auto_start=False)
    locate.add_to(map)

    # add minimap to main map
    map.add_child(mini_map)

    # add scroll zoom toggler to main map
    plugins.Fullscreen(position="topright").add_to(map)

    data = prepare_marker_data()

    for district, lat_lng in data.items():
        if lat_lng[2] == "coorperative" and lat_lng[2] is not None:
            color = "darkred"

        elif lat_lng[2] == "business-firm" and lat_lng[2] is not None:
            color = "darkgreen"

        else:
            color = "lightblue"

        folium.Marker(
            location=[lat_lng[0], lat_lng[1]],
            popup=district.capitalize(),
            icon=folium.Icon(color=color, icon="fa-users", prefix="fa"),
        ).add_to(marker_cluster)

    # # add map layer toggle, intentionally to be initiated after rendering map widget
    folium.LayerControl().add_to(map)

    # render map onto html
    map = map._repr_html_()

    return map
