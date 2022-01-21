import folium
import pandas as pd
import altair as alt
from folium import plugins

from tralard.models.ward import Ward
from tralard.models.district import District
from tralard.constants import MAP_LAYER_CHOICES
from tralard.models.beneficiary import Beneficiary


def prepare_marker_data():
    districts = District.objects.all()
    data = {}
    for district_data in districts:
        data[district_data] = [district_data.location.x, district_data.location.y]

    return data


def circle_marker(district_name, lat, lng, source):
    chart = alt.Chart(source).mark_bar().encode(x="Wards", y="Beneficiary Count")
    visual_graph = chart.to_json()
    marker = folium.CircleMarker(
        location=[lat, lng],
        radius=10,
        color="darkgreen",
        fill=True,
        fill_color="lightblue",
        fillOpacity=1.0,
        opacity=0.5,
        tooltip=district_name,
        popup=folium.Popup(max_width=500).add_child(
            folium.VegaLite(visual_graph, height=300)
        ),
    )
    return marker


def build_map_context():

    # add base map
    map = folium.Map(
        # bounding box for map of zambia
        location=[-13.1519165, 27.852537499999983],
        tiles="cartodbpositron",
        control_scale=True,
        max_zoom=8,
        zoom_start=6.4,
        width="100%",
        height="80%",
    )

    map_layers = MAP_LAYER_CHOICES
    for map_layer in map_layers:
        folium.raster_layers.TileLayer(map_layer).add_to(map)

    mini_map = plugins.MiniMap(toggle_display=True)
    marker_cluster = plugins.MarkerCluster().add_to(map)

    # Search widget
    search = plugins.Search(
        marker_cluster,
        geom_type="Point",
        search_label=None,
        search_zoom=None,
        position="topleft",
        placeholder="Search district",
        collapsed=False,
    )
    search.add_to(map)

    # Draw tools
    draw = plugins.Draw(export=True)
    locate = plugins.LocateControl(auto_start=False)
    draw.add_to(map)
    locate.add_to(map)
    map.add_child(mini_map)
    plugins.Fullscreen(position="topright").add_to(map)

    districts = prepare_marker_data()

    start_coords = []
    ward_names = []
    beneficiary_count = []
    for district, lat_lng in districts.items():
        start_coords.append((lat_lng[0], lat_lng[1]))

        for ward in Ward.objects.filter(district__name=district.name):
            beneficiary_counter = Beneficiary.objects.filter(
                ward__name=ward.name
            ).count()
            beneficiary_count.append(beneficiary_counter)
            ward_names.append(ward.name.capitalize())

        source = pd.DataFrame(
            {"Wards": ward_names, "Beneficiary Count": beneficiary_count}
        )

        district_name_verbose = (
            f"{district.name.capitalize()} District - {district.province.name}"
        )
        marker = circle_marker(district_name_verbose, lat_lng[0], lat_lng[1], source)
        marker.add_to(marker_cluster)

    folium.LayerControl().add_to(map)
    map = map._repr_html_()

    return map
