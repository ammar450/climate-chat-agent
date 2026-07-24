# Climate Chat Agent — Evaluation Report
**Generated:** 2026-07-24T16:09:07.724815  
**Random Seed:** 42  
**Runs:** 5 × 16 test cases

---
# Statistics across all 5 runs
## 📊 Aggregate Metrics
| Metric | Value |
|--- |--- |
| Template Accuracy | 100.0% ± 0.0% |
| Template Accuracy Range | 100.0% – 100.0% |
| Success Rate - Query Creation | 97.5% |
| Success Rate - Query Execution | 76.2% |
| Avg Latency | 30.24s |
| Latency Range | 1.66s – 62.46s |
| **Overall Score** | **88.1%** |

## 🏷️ Category-wise Analysis
| Category | Tests | Templ Acc | Exec Success | Avg Time | 
|--- |--- |--- |--- |--- |
| aggregation | 20 | 100.0% | 75.0% | 31.60s |
| extreme-values | 5 | 100.0% | 80.0% | 41.74s |
| filtering | 10 | 100.0% | 50.0% | 35.67s |
| location-based | 15 | 100.0% | 86.7% | 13.86s |
| multi-year-comparison | 5 | 100.0% | 40.0% | 52.12s |
| nested-aggregation | 5 | 100.0% | 100.0% | 54.82s |
| overview | 15 | 100.0% | 86.7% | 19.07s |
| subsampling | 5 | 100.0% | 80.0% | 38.58s |

## 📐 Template-wise Analysis
| Template | Tested | Success | Rate | Avg Time | 
|--- |--- |--- |--- |--- |
| all_properties_summary | 5 | 3 | 60.0% | 24.32s | 
| average_for_property_date_range | 5 | 5 | 100.0% | 36.98s | 
| daily_aggregates | 5 | 5 | 100.0% | 10.92s | 
| features_near_coordinates | 5 | 4 | 80.0% | 2.58s | 
| filtered_timeseries | 10 | 5 | 50.0% | 35.67s | 
| list_features_of_interest | 5 | 5 | 100.0% | 17.39s | 
| list_properties | 5 | 5 | 100.0% | 15.51s | 
| location_based_summary | 5 | 4 | 80.0% | 3.92s | 
| monthly_aggregates | 5 | 3 | 60.0% | 30.09s | 
| monthly_mean_from_daily | 5 | 5 | 100.0% | 54.82s | 
| sample_observations | 5 | 4 | 80.0% | 38.58s | 
| timeseries_statistics | 10 | 4 | 40.0% | 50.27s | 
| timeseries_statistics_by_feature | 5 | 5 | 100.0% | 35.08s | 
| top_extremes_for_property | 5 | 4 | 80.0% | 41.74s | 

## ❌ Error Analysis
| Category | Count | Top failure reasons (count) | Topics |
|---------|-------|---------------------------|--------|
| n/a     | n/a   | n/a                       | n/a    |

| Template | Count | Top failure reasons (count) | Topics |
|---------|-------|---------------------------|--------|
| n/a     | n/a   | n/a                       | n/a    |

## 🔀 Confusion Matrix
| Expected ↓ / Predicted → | all_properties_summary | average_for_property_date_range | daily_aggregates | features_near_coordinates | filtered_timeseries | list_features_of_interest | list_properties | location_based_summary | monthly_aggregates | monthly_mean_from_daily | sample_observations | timeseries_statistics | timeseries_statistics_by_feature | top_extremes_for_property |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all_properties_summary | 5 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| average_for_property_date_range | 0 | 5 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| daily_aggregates | 0 | 0 | 5 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| features_near_coordinates | 0 | 0 | 0 | 5 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| filtered_timeseries | 0 | 0 | 0 | 0 | 10 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| list_features_of_interest | 0 | 0 | 0 | 0 | 0 | 5 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| list_properties | 0 | 0 | 0 | 0 | 0 | 0 | 5 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| location_based_summary | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 5 | 0 | 0 | 0 | 0 | 0 | 0 |
| monthly_aggregates | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 5 | 0 | 0 | 0 | 0 | 0 |
| monthly_mean_from_daily | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 5 | 0 | 0 | 0 | 0 |
| sample_observations | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 5 | 0 | 0 | 0 |
| timeseries_statistics | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 10 | 0 | 0 |
| timeseries_statistics_by_feature | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 5 | 0 |
| top_extremes_for_property | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 5 |

---
# Statistics per run
## 📋 Per-Run Summary
| Run | Templ Acc | Generation Success | Execution Success | Avg Time |
|--- |--- |--- |--- |--- |
| 1 | 100.0% | 100.0% | 75.0% | 34.12s |
| 2 | 100.0% | 100.0% | 87.5% | 28.57s |
| 3 | 100.0% | 93.8% | 62.5% | 26.72s |
| 4 | 100.0% | 93.8% | 75.0% | 29.89s |
| 5 | 100.0% | 100.0% | 81.2% | 31.89s |

## 📝 Detailed Results (Run 1)
| ID | Cat | Question | Expected | Predicted | Match | Rows | Time |
|--- |--- |--- |--- |--- |--- |--- |--- |
| 1 | overview | Provide an overview of observation variables in the dataset | list_properties | list_properties | ✅ | 5 | 15.60s |
| 2 | overview | List all locations of observations available | list_features_of_interest | list_features_of_interest | ✅ | 10 | 17.52s |
| 3 | subsampling | Show me some sample observations | sample_observations | sample_observations | ✅ | 0 | 62.46s |
| 4 | overview | Show me climate data for 2000 | all_properties_summary | all_properties_summary | ✅ | 2 | 21.98s |
| 5 | aggregation | Show me wind speed statistics for 2010 | timeseries_statistics | timeseries_statistics | ✅ | 1 | 50.33s |
| 6 | aggregation | What was the average temperature in 2020? | average_for_property_date_range | average_for_property_date_range | ✅ | 1 | 52.32s |
| 7 | aggregation | Show monthly temperature averages for 2022 | monthly_aggregates | monthly_aggregates | ✅ | 10 | 54.78s |
| 8 | aggregation | Show daily temperature averages for January 2024 | daily_aggregates | daily_aggregates | ✅ | 10 | 7.08s |
| 9 | extreme-values | What were the highest humidity values in 1970 | top_extremes_for_property | top_extremes_for_property | ✅ | 2 | 40.26s |
| 10 | filtering | Show me wind speed between 5 and 15 m/s in 2020 | filtered_timeseries | filtered_timeseries | ✅ | 10 | 31.66s |
| 11 | filtering | Find precipitation values above 30 mm in 2000 | filtered_timeseries | filtered_timeseries | ✅ | 10 | 35.07s |
| 12 | location-based | What are grids near lat: 67.8, lon: 20.3 | features_near_coordinates | features_near_coordinates | ✅ | 10 | 2.80s |
| 13 | location-based | What was the weather like in Poland in 1970? | location_based_summary | location_based_summary | ✅ | 4 | 3.08s |
| 14 | nested-aggregation | What was the mean daily temperature in 2021? | monthly_mean_from_daily | monthly_mean_from_daily | ✅ | 1 | 53.63s |
| 15 | location-based | Compare wind speed across different grid points in 2019 | timeseries_statistics_by_feature | timeseries_statistics_by_feature | ✅ | 10 | 36.78s |
| 16 | multi-year-comparison | Compare humidity between 1950 and 2024 | timeseries_statistics | timeseries_statistics | ✅ | 0 | 60.59s |
## 📝 Detailed Results (Run 2)
| ID | Cat | Question | Expected | Predicted | Match | Rows | Time |
|--- |--- |--- |--- |--- |--- |--- |--- |
| 1 | overview | What variables are available? | list_properties | list_properties | ✅ | 5 | 15.55s |
| 2 | overview | List all locations of observations available | list_features_of_interest | list_features_of_interest | ✅ | 10 | 17.36s |
| 3 | subsampling | Show me some sample observations | sample_observations | sample_observations | ✅ | 10 | 33.01s |
| 4 | overview | Give me an overview of climate observations for 2024 | all_properties_summary | all_properties_summary | ✅ | 2 | 29.30s |
| 5 | aggregation | Calculate temperature statistics for 2024 | timeseries_statistics | timeseries_statistics | ✅ | 1 | 47.62s |
| 6 | aggregation | What is the average humidity for 2010? | average_for_property_date_range | average_for_property_date_range | ✅ | 1 | 33.59s |
| 7 | aggregation | Calculate monthly precipitation totals for 1965 | monthly_aggregates | monthly_aggregates | ✅ | 10 | 40.88s |
| 8 | aggregation | Show daily temperature averages for January 2024 | daily_aggregates | daily_aggregates | ✅ | 10 | 5.96s |
| 9 | extreme-values | What were the highest humidity values in 1970 | top_extremes_for_property | top_extremes_for_property | ✅ | 2 | 32.75s |
| 10 | filtering | Show me wind speed between 5 and 15 m/s in 2020 | filtered_timeseries | filtered_timeseries | ✅ | 10 | 30.38s |
| 11 | filtering | Find precipitation values above 30 mm in 2000 | filtered_timeseries | filtered_timeseries | ✅ | 10 | 33.51s |
| 12 | location-based | What are grids near lat: 67.8, lon: 20.3 | features_near_coordinates | features_near_coordinates | ✅ | 10 | 2.39s |
| 13 | location-based | What was the weather like in Poland in 1970? | location_based_summary | location_based_summary | ✅ | 4 | 2.75s |
| 14 | nested-aggregation | What was the mean daily temperature in 2001? | monthly_mean_from_daily | monthly_mean_from_daily | ✅ | 1 | 57.51s |
| 15 | location-based | Compare humidity across different grid points in 2019 | timeseries_statistics_by_feature | timeseries_statistics_by_feature | ✅ | 10 | 35.26s |
| 16 | multi-year-comparison | Show me wind speed trends for the last 5 years | timeseries_statistics | timeseries_statistics | ✅ | 1 | 39.30s |
## 📝 Detailed Results (Run 3)
| ID | Cat | Question | Expected | Predicted | Match | Rows | Time |
|--- |--- |--- |--- |--- |--- |--- |--- |
| 1 | overview | Which variables can be queried? | list_properties | list_properties | ✅ | 5 | 15.48s |
| 2 | overview | What are grids available in the dataset? | list_features_of_interest | list_features_of_interest | ✅ | 10 | 17.38s |
| 3 | subsampling | Give me examples of observations in the dataset | sample_observations | sample_observations | ✅ | 10 | 32.78s |
| 4 | overview | Give me an overview of climate observations for 2024 | all_properties_summary | all_properties_summary | ✅ | 2 | 29.09s |
| 5 | aggregation | Calculate temperature statistics for 2024 | timeseries_statistics | timeseries_statistics | ✅ | 1 | 48.17s |
| 6 | aggregation | What is the average humidity for 2010? | average_for_property_date_range | average_for_property_date_range | ✅ | 1 | 33.04s |
| 7 | aggregation | What was the wettest month in 2023? | monthly_aggregates | monthly_aggregates | ✅ | 0 | 1.66s |
| 8 | aggregation | Give me daily precipitation statistics for June 1970 | daily_aggregates | daily_aggregates | ✅ | 10 | 4.53s |
| 9 | extreme-values | Show me the lowest precipitation amounts in 1955 | top_extremes_for_property | top_extremes_for_property | ✅ | 10 | 40.58s |
| 10 | filtering | Show me wind speed between 5 and 15 m/s in 2020 | filtered_timeseries | filtered_timeseries | ✅ | 10 | 30.07s |
| 11 | filtering | Find temperature readings above 30 degrees in Summer 2024 | filtered_timeseries | filtered_timeseries | ✅ | 10 | 45.43s |
| 12 | location-based | Find observation points around lat: 52.5, lon: 13.4 | features_near_coordinates | features_near_coordinates | ✅ | 10 | 2.11s |
| 13 | location-based | Show me climate data in Germany during 2024 | location_based_summary | location_based_summary | ✅ | 4 | 3.40s |
| 14 | nested-aggregation | What was the mean daily temperature in 2021? | monthly_mean_from_daily | monthly_mean_from_daily | ✅ | 1 | 50.94s |
| 15 | location-based | Compare humidity across different grid points in 2019 | timeseries_statistics_by_feature | timeseries_statistics_by_feature | ✅ | 10 | 34.98s |
| 16 | multi-year-comparison | Show me wind speed trends for the last 5 years | timeseries_statistics | timeseries_statistics | ✅ | 1 | 37.88s |
## 📝 Detailed Results (Run 4)
| ID | Cat | Question | Expected | Predicted | Match | Rows | Time |
|--- |--- |--- |--- |--- |--- |--- |--- |
| 1 | overview | Which variables can be queried? | list_properties | list_properties | ✅ | 5 | 15.59s |
| 2 | overview | What are locations of observations available in the dataset? | list_features_of_interest | list_features_of_interest | ✅ | 10 | 17.21s |
| 3 | subsampling | What are examples of observations from the current dataset | sample_observations | sample_observations | ✅ | 10 | 32.24s |
| 4 | overview | What was the climate like in 1950? | all_properties_summary | all_properties_summary | ✅ | 3 | 12.18s |
| 5 | aggregation | Calculate temperature statistics for 2024 | timeseries_statistics | timeseries_statistics | ✅ | 1 | 48.12s |
| 6 | aggregation | What is the average humidity for 2010? | average_for_property_date_range | average_for_property_date_range | ✅ | 1 | 32.98s |
| 7 | aggregation | What was the wettest month in 2023? | monthly_aggregates | monthly_aggregates | ✅ | 0 | 1.82s |
| 8 | aggregation | What are daily humidity averages for March 2000 | daily_aggregates | daily_aggregates | ✅ | 10 | 33.92s |
| 9 | extreme-values | What were the highest temperature values in 2023? | top_extremes_for_property | top_extremes_for_property | ✅ | 1 | 49.24s |
| 10 | filtering | Find precipitation values below 12 mm and above 10 mm in 200 | filtered_timeseries | filtered_timeseries | ✅ | 10 | 34.14s |
| 11 | filtering | Find temperature readings above 30 degrees in Summer 2024 | filtered_timeseries | filtered_timeseries | ✅ | 10 | 42.68s |
| 12 | location-based | What are grids near lat: 67.8, lon: 20.3 | features_near_coordinates | features_near_coordinates | ✅ | 10 | 2.78s |
| 13 | location-based | What was the weather in France during 1985? | location_based_summary | location_based_summary | ✅ | 4 | 7.34s |
| 14 | nested-aggregation | What was the mean daily temperature in 2001? | monthly_mean_from_daily | monthly_mean_from_daily | ✅ | 1 | 52.74s |
| 15 | location-based | Compare wind speed across different grid points in 2019 | timeseries_statistics_by_feature | timeseries_statistics_by_feature | ✅ | 10 | 34.46s |
| 16 | multi-year-comparison | Compare humidity between 1950 and 2024 | timeseries_statistics | timeseries_statistics | ✅ | 0 | 60.84s |
## 📝 Detailed Results (Run 5)
| ID | Cat | Question | Expected | Predicted | Match | Rows | Time |
|--- |--- |--- |--- |--- |--- |--- |--- |
| 1 | overview | Provide an overview of observation variables in the dataset | list_properties | list_properties | ✅ | 5 | 15.35s |
| 2 | overview | List all locations of observations available | list_features_of_interest | list_features_of_interest | ✅ | 10 | 17.45s |
| 3 | subsampling | What are examples of observations from the current dataset | sample_observations | sample_observations | ✅ | 10 | 32.41s |
| 4 | overview | Give me an overview of climate observations for 2024 | all_properties_summary | all_properties_summary | ✅ | 2 | 29.07s |
| 5 | aggregation | Calculate temperature statistics for 2024 | timeseries_statistics | timeseries_statistics | ✅ | 1 | 47.89s |
| 6 | aggregation | What is the average humidity for 2010? | average_for_property_date_range | average_for_property_date_range | ✅ | 1 | 32.98s |
| 7 | aggregation | Show monthly temperature averages for 2022 | monthly_aggregates | monthly_aggregates | ✅ | 10 | 51.31s |
| 8 | aggregation | Give me daily precipitation statistics for June 1970 | daily_aggregates | daily_aggregates | ✅ | 10 | 3.10s |
| 9 | extreme-values | What were the highest temperature values in 2023? | top_extremes_for_property | top_extremes_for_property | ✅ | 1 | 45.87s |
| 10 | filtering | Show me wind speed between 5 and 15 m/s in 2020 | filtered_timeseries | filtered_timeseries | ✅ | 10 | 30.55s |
| 11 | filtering | Find temperature readings above 30 degrees in Summer 2024 | filtered_timeseries | filtered_timeseries | ✅ | 10 | 43.21s |
| 12 | location-based | Find observation points around lat: 52.5, lon: 13.4 | features_near_coordinates | features_near_coordinates | ✅ | 10 | 2.81s |
| 13 | location-based | What was the weather in France during 1985? | location_based_summary | location_based_summary | ✅ | 4 | 3.01s |
| 14 | nested-aggregation | What was the mean daily temperature in 2011? | monthly_mean_from_daily | monthly_mean_from_daily | ✅ | 1 | 59.26s |
| 15 | location-based | Compare wind speed across different grid points in 2019 | timeseries_statistics_by_feature | timeseries_statistics_by_feature | ✅ | 10 | 33.91s |
| 16 | multi-year-comparison | Compare humidity between 1950 and 2024 | timeseries_statistics | timeseries_statistics | ✅ | 0 | 62.01s |