import folium
import pandas as pd
import altair as alt
from folium import plugins

from tralard.models.ward import Ward
from tralard.constants import MAP_LAYER_CHOICES
from tralard.models.sub_project import SubProject
from tralard.models.beneficiary import Beneficiary


def prepare_marker_data():
    wards = Ward.objects.all()
    data = {}
    for ward_data in wards:
        if ward_data.location is not None:
            data[ward_data] = [ward_data.location.x, ward_data.location.y]

    return data


def circle_marker(ward_name, lat, lng, source):
    chart = alt.Chart(source).mark_bar().encode(x="subprojects", y="Beneficiary Count")
    visual_graph = chart.to_json()
    marker = folium.CircleMarker(
        location=[lat, lng],
        radius=10,
        color="darkgreen",
        fill=True,
        fill_color="lightblue",
        fillOpacity=1.0,
        opacity=0.5,
        tooltip=ward_name,
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

    wards = prepare_marker_data()

    subproject_names = []
    beneficiary_count = []
    for ward, lat_lng in wards.items():
        subprojects = SubProject.objects.filter(
            ward__slug=ward.slug
        )
        for subproject in  subprojects:
            beneficiary_counter = Beneficiary.objects.filter(
                    ward__slug=ward.slug,
                    sub_project__slug=subproject.slug
                ).count()
            beneficiary_count.append(beneficiary_counter)
            subproject_names.append(subproject.name.capitalize())

        source = pd.DataFrame(
            {
                "subprojects": subproject_names, 
                "Beneficiary Count": beneficiary_count
            }
        )

        ward_name_verbose = (
            f"{ward.name} Ward <br/>{ward.district.name.capitalize()} District <br/>{ward.district.province.name}"
        )
        marker = circle_marker(ward_name_verbose, lat_lng[0], lat_lng[1], source)
        marker.add_to(marker_cluster)

    folium.LayerControl().add_to(map)
    map = map._repr_html_()

    return map
