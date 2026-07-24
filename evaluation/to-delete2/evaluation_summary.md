## ❌ Error Analysis
| Template                     | Count | Top failure reasons (count)                                      | Topics                       |
|------------------------------|-------|------------------------------------------------------------------|------------------------------|
| filtered_timeseries           | 5     | All returned wind speed values are below 5 m/s or above 15 m/s. (2), No values found in the specified range of 10 mm to 12 mm. (1), All returned wind speed values are below 15 m/s. (1) | filtering                    |
| features_near_coordinates     | 2     | Returned grids do not match the specified latitude and longitude criteria. (1), Returned grids do not correspond to the specified latitude and longitude. (1) | location-based               |
| timeseries_statistics         | 3     | No data available for the specified years (3)                   | multi-year-comparison        |
| all_properties_summary        | 2     | Data does not specify the year 2024 (2)                         | overview                     |
| monthly_aggregates           | 2     | No data available for the specified year (2)                    | aggregation                  |
| top_extremes_for_property     | 1     | All returned precipitation values are zero, indicating no recorded precipitation for the queried year. (1) | extreme-values               |

| Category                     | Count | Top failure reasons (count)                                      | Topics                       |
|------------------------------|-------|------------------------------------------------------------------|------------------------------|
| filtering                    | 5     | All returned wind speed values are below 5 m/s or above 15 m/s. (2), No values found in the specified range of 10 mm to 12 mm. (1), All returned wind speed values are below 15 m/s. (1) | filtered_timeseries          |
| location-based               | 3     | Returned grids do not match the specified latitude and longitude criteria. (1), Returned grids do not correspond to the specified latitude and longitude. (1) | features_near_coordinates    |
| multi-year-comparison        | 3     | No data available for the specified years (3)                   | timeseries_statistics        |
| overview                     | 2     | Data does not specify the year 2024 (2)                         | all_properties_summary       |
| aggregation                  | 2     | No data available for the specified year (2)                    | monthly_aggregates          |
| extreme-values               | 1     | All returned precipitation values
