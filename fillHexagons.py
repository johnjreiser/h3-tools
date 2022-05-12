import h3
import argparse
from geojson import load, Feature, FeatureCollection
from shapely.geometry import Polygon, shape, mapping
import logging

logging.basicConfig(level=logging.DEBUG)


def featureToHexagons(input_geojson, resolution=8):
    for feature in input_geojson.features:
        hex_ids = h3.polyfill(
            dict(feature.geometry), resolution, geo_json_conformant=True
        )
        for hex in hex_ids:
            hexpoly = Feature(properties=feature.properties)
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
    p.add_argument(
        "-b",
        "--buffer",
        help="Buffer the input GeoJSON by twice a hexagon's edge length",
        default=False,
        action="store_true",
    )

    args = p.parse_args()

    with open(args.boundary, "rb") as fh:
        input_geojson = load(fh)

    if args.buffer:
        logging.info(
            "Buffering input by ~{} meters".format(
                h3.edge_length(args.resolution, unit="m")
            )
        )
        buff_degrees = h3.edge_length(args.resolution, unit="m") / 111111 * 2
        for feature in input_geojson.features:
            sg = Polygon(shape(feature.geometry)).buffer(buff_degrees)
            feature.geometry = mapping(sg)

    if args.output == "geojson":
        features = []
        for polygon in featureToHexagons(input_geojson, args.resolution):
            features.append(polygon)
        print(FeatureCollection(features))
