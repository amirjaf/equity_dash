import pandas as pd
from shapely.geometry import shape
import fiona
import os

# Read shapefile using Fiona
cw = os.getcwd()
with fiona.open(
    os.path.join(cw, "src", "assets", "maz_shapefile", "l_poi_surface.shp")
) as src:
    records = []
    for feature in src:
        geometry = shape(feature["geometry"])
        record = feature["properties"]
        record["geometry"] = geometry
        records.append(record)

# Convert to DataFrame
df = pd.DataFrame(records)
print(df)
