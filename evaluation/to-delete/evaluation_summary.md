# Climate Chat Agent — Evaluation Report
**Generated:** 2026-07-24T22:08:36.553075  
**Random Seed:** 42  
**Runs:** 1 × 16 test cases

---
# Statistics across all 1 runs
## 📊 Aggregate Metrics
| Metric | Value |
|--- |--- |
| Template Accuracy | 100.0% ± 0.0% |
| Template Accuracy Range | 100.0% – 100.0% |
| Success Rate - Query Creation | 100.0% |
| Success Rate - Query Execution | 81.2% |
| Avg Latency | 30.87s |
| Latency Range | 2.29s – 60.62s |
| **Overall Score** | **90.6%** |

## 🏷️ Category-wise Analysis
| Category | Tests | Templ Acc | Exec Success | Avg Time | 
|--- |--- |--- |--- |--- |
| aggregation | 4 | 100.0% | 100.0% | 39.40s |
| extreme-values | 1 | 100.0% | 100.0% | 33.24s |
| filtering | 2 | 100.0% | 50.0% | 31.87s |
| location-based | 3 | 100.0% | 66.7% | 13.29s |
| multi-year-comparison | 1 | 100.0% | 0.0% | 60.62s |
| nested-aggregation | 1 | 100.0% | 100.0% | 51.56s |
| overview | 3 | 100.0% | 100.0% | 17.97s |
| subsampling | 1 | 100.0% | 100.0% | 33.38s |

## 📐 Template-wise Analysis
| Template | Tested | Success | Rate | Avg Time | 
|--- |--- |--- |--- |--- |
| all_properties_summary | 1 | 1 | 100.0% | 20.61s | 
| average_for_property_date_range | 1 | 1 | 100.0% | 48.78s | 
| daily_aggregates | 1 | 1 | 100.0% | 7.25s | 
| features_near_coordinates | 1 | 0 | 0.0% | 2.29s | 
| filtered_timeseries | 2 | 1 | 50.0% | 31.87s | 
| list_features_of_interest | 1 | 1 | 100.0% | 17.56s | 
| list_properties | 1 | 1 | 100.0% | 15.74s | 
| location_based_summary | 1 | 1 | 100.0% | 3.37s | 
| monthly_aggregates | 1 | 1 | 100.0% | 52.44s | 
| monthly_mean_from_daily | 1 | 1 | 100.0% | 51.56s | 
| sample_observations | 1 | 1 | 100.0% | 33.38s | 
| timeseries_statistics | 2 | 1 | 50.0% | 54.87s | 
| timeseries_statistics_by_feature | 1 | 1 | 100.0% | 34.19s | 
| top_extremes_for_property | 1 | 1 | 100.0% | 33.24s | 

## ❌ Error Analysis
| Template                   | Count | Top failure reasons (count)                                         | Topics                     |
|----------------------------|-------|--------------------------------------------------------------------|----------------------------|
| filtered_timeseries        | 1     | All returned wind speed values are below 5 m/s or above 15 m/s.   | filtering                   |
| features_near_coordinates  | 1     | Returned grids do not match the specified latitude and longitude criteria. (1), The grid URIs do not indicate proximity to the given coordinates. (1) | location-based             |
| timeseries_statistics       | 1     | No data available for the specified years (1), Query may not have matched any records in the dataset (1) | multi-year-comparison      |

| Category                   | Count | Top failure reasons (count)                                         | Topics                     |
|----------------------------|-------|--------------------------------------------------------------------|----------------------------|
| filtering                  | 1     | All returned wind speed values are below 5 m/s or above 15 m/s.   | filtered_timeseries        |
| location-based             | 1     | Returned grids do not match the specified latitude and longitude criteria. (1), The grid URIs do not indicate proximity to the given coordinates. (1) | features_near_coordinates  |
| multi-year-comparison      | 1     | No data available for the specified years (1), Query may not have matched any records in the dataset (1) | timeseries_statistics      |

## 🔀 Confusion Matrix
| Expected ↓ / Predicted → | all_properties_summary | average_for_property_date_range | daily_aggregates | features_near_coordinates | filtered_timeseries | list_features_of_interest | list_properties | location_based_summary | monthly_aggregates | monthly_mean_from_daily | sample_observations | timeseries_statistics | timeseries_statistics_by_feature | top_extremes_for_property |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all_properties_summary | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| average_for_property_date_range | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| daily_aggregates | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| features_near_coordinates | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| filtered_timeseries | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| list_features_of_interest | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| list_properties | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| location_based_summary | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| monthly_aggregates | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| monthly_mean_from_daily | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 |
| sample_observations | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| timeseries_statistics | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 |
| timeseries_statistics_by_feature | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 |
| top_extremes_for_property | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 |

---
# Statistics per run
## 📋 Per-Run Summary
| Run | Templ Acc | Generation Success | Execution Success | Avg Time |
|--- |--- |--- |--- |--- |
| 1 | 100.0% | 100.0% | 81.2% | 30.87s |

## 📝 Detailed Results (Run 1)
| ID | Cat | Question | Expected | Predicted | Match | Rows | Time |
|--- |--- |--- |--- |--- |--- |--- |--- |
| 1 | overview | Provide an overview of observation variables in the dataset | list_properties | list_properties | ✅ | 5 | 15.74s |
| 2 | overview | List all locations of observations available | list_features_of_interest | list_features_of_interest | ✅ | 10 | 17.56s |
| 3 | subsampling | Show me some sample observations | sample_observations | sample_observations | ✅ | 10 | 33.38s |
| 4 | overview | Show me climate data for 2000 | all_properties_summary | all_properties_summary | ✅ | 2 | 20.61s |
| 5 | aggregation | Show me wind speed statistics for 2010 | timeseries_statistics | timeseries_statistics | ✅ | 1 | 49.13s |
| 6 | aggregation | What was the average temperature in 2020? | average_for_property_date_range | average_for_property_date_range | ✅ | 1 | 48.78s |
| 7 | aggregation | Show monthly temperature averages for 2022 | monthly_aggregates | monthly_aggregates | ✅ | 10 | 52.44s |
| 8 | aggregation | Show daily temperature averages for January 2024 | daily_aggregates | daily_aggregates | ✅ | 10 | 7.25s |
| 9 | extreme-values | What were the highest humidity values in 1970 | top_extremes_for_property | top_extremes_for_property | ✅ | 2 | 33.24s |
| 10 | filtering | Show me wind speed between 5 and 15 m/s in 2020 | filtered_timeseries | filtered_timeseries | ✅ | 10 | 30.09s |
| 11 | filtering | Find precipitation values above 30 mm in 2000 | filtered_timeseries | filtered_timeseries | ✅ | 10 | 33.65s |
| 12 | location-based | What are grids near lat: 67.8, lon: 20.3 | features_near_coordinates | features_near_coordinates | ✅ | 10 | 2.29s |
| 13 | location-based | What was the weather like in Poland in 1970? | location_based_summary | location_based_summary | ✅ | 4 | 3.37s |
| 14 | nested-aggregation | What was the mean daily temperature in 2021? | monthly_mean_from_daily | monthly_mean_from_daily | ✅ | 1 | 51.56s |
| 15 | location-based | Compare wind speed across different grid points in 2019 | timeseries_statistics_by_feature | timeseries_statistics_by_feature | ✅ | 10 | 34.19s |
| 16 | multi-year-comparison | Compare humidity between 1950 and 2024 | timeseries_statistics | timeseries_statistics | ✅ | 0 | 60.62s |