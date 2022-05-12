# H3 Tools

Collection of code to work with the [Uber H3 hierarchical hexagon](https://github.com/uber/h3) index system.

## Tools

### fillHexagons.py


    usage: Fills a given GeoJSON with H3 hexagons

    positional arguments:
    boundary              GeoJSON boundary of the area to be hexagon-filled
    resolution            h3 resolution of the hexagon fill

    optional arguments:
    -b, --buffer          Buffer the input GeoJSON by twice a hexagon's edge length
    -h, --help            show this help message and exit


For a provided GeoJSON file, generates a new GeoJSON file containing the H3 hexagons within each input feature. Properties of the input feature are retained in the hexagons, and the `id` field of the hexagon is set to the H3 index value. 

#### Example

Provided the following `input.json` file:

    {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {},
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [
                        [
                            [
                                -74.922,
                                38.929
                            ],
                            [
                                -74.904,
                                38.929
                            ],
                            [
                                -74.904,
                                38.943
                            ],
                            [
                                -74.922,
                                38.943
                            ],
                            [
                                -74.922,
                                38.929
                            ]
                        ]
                    ]
                }
            }
        ]
    }

`python3 ./fillHexagons.py input.json 8 > hex.json` will produce the following (with pretty JSON formatting applied):

    {
    "features": [
        {
        "geometry": {
            "coordinates": [
            [
                [
                -74.9122067,
                38.9420844
                ],
                [
                -74.9183302,
                38.9410020
                ],
                [
                -74.9201375,
                38.9366299
                ],
                [
                -74.9158223,
                38.9333404
                ],
                [
                -74.9096998,
                38.9344226
                ],
                [
                -74.9078916,
                38.9387944
                ],
                [
                -74.9122067,
                38.9420844
                ]
            ]
            ],
            "type": "Polygon"
        },
        "id": "882aada961fffff",
        "properties": {},
        "type": "Feature"
        },
        {
        "geometry": {
            "coordinates": [
            [
                [
                -74.9201375,
                38.9366299
                ],
                [
                -74.9262601,
                38.9355471
                ],
                [
                -74.9280665,
                38.9311752
                ],
                [
                -74.9237512,
                38.9278862
                ],
                [
                -74.9176295,
                38.9289687
                ],
                [
                -74.9158223,
                38.9333404
                ],
                [
                -74.9201375,
                38.9366299
                ]
            ]
            ],
            "type": "Polygon"
        },
        "id": "882aada967fffff",
        "properties": {},
        "type": "Feature"
        },
        {
        "geometry": {
            "coordinates": [
            [
                [
                -74.9096998,
                38.9344226
                ],
                [
                -74.9158223,
                38.9333404
                ],
                [
                -74.9176295,
                38.9289687
                ],
                [
                -74.9133152,
                38.9256796
                ],
                [
                -74.9071936,
                38.9267615
                ],
                [
                -74.9053854,
                38.9311328
                ],
                [
                -74.9096998,
                38.9344226
                ]
            ]
            ],
            "type": "Polygon"
        },
        "id": "882aada963fffff",
        "properties": {},
        "type": "Feature"
        }
    ],
    "type": "FeatureCollection"
    }



#### Converting to SQL

Converting the resultant GeoJSON to a database or other format is easy using the [GDAL/OGR toolset](https://gdal.org/). 

    python3 ./fillHexagons.py input.geojson 8 > hex.json 
    ogr2ogr -f PGDUMP -select id -lco geometry_name=shape output.sql hex.json


## References

- [ogr2ogr](https://gdal.org/programs/ogr2ogr.html) - Convert from GeoJSON
- [jq](https://stedolan.github.io/jq/) - Parse and format JSON

