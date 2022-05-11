import h3
import argparse
import geojson


def featureToHexagons(input_geojson, resolution=8):
    for feature in input_geojson.features:
        hex_ids = h3.polyfill(
            dict(feature.geometry), resolution, geo_json_conformant=True
        )
        for hex in hex_ids:
            hexpoly = geojson.Feature(properties=feature.properties)
            hexpoly["id"] = hex
            hexpoly.geometry = {"type": "Polygon"}
            hexpoly.geometry["coordinates"] = [
                h3.h3_to_geo_boundary(hex, geo_json=True)
            ]
            yield (hexpoly)


if __name__ == "__main__":
    p = argparse.ArgumentParser(usage="Fills a given GeoJSON with H3 hexagons")
    p.add_argument("boundary", help="GeoJSON boundary of the area to be hexagon-filled")
    p.add_argument("resolution", type=int, help="h3 resolution of the hexagon fill")
    p.add_argument(
        "-o",
        "--output",
        default="geojson",
        choices=["geojson"],
        help="Specify output format",
    )

    args = p.parse_args()

    with open(args.boundary, "rb") as fh:
        input_geojson = geojson.load(fh)

    if args.output == "geojson":
        features = []
        for polygon in featureToHexagons(input_geojson, args.resolution):
            features.append(polygon)
        print(geojson.FeatureCollection(features))
