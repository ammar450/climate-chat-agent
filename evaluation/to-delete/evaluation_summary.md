# Climate Chat Agent — Evaluation Report
**Generated:** 2026-07-22T19:30:07.312594  
**Random Seed:** 10183  
**Runs:** 1 × 16 test cases

## 📊 Aggregate Metrics
| Metric | Value |
|--- |--- |
| Template Accuracy | 100.0% ± 0.0% |
| Template Accuracy Range | 100.0% – 100.0% |
| Success Rate - Query Execution | 100.0% |
| Success Rate - Query Creation | 100.0% |
| Avg Latency | 36.45s |
| Latency Range | 4.10s – 68.59s |
| **Overall Score** | **100.0%** |

## 📋 Per-Run Summary
| Run | Templ Acc | Exec Success | Avg Time |
|--- |--- |--- |--- |
| 1 | 100.0% | 100.0% | 36.45s |

## 🏷️ Category-wise Analysis
| Category | Tests | Templ Acc | Exec Success | Avg Time | Common Errors |
|--- |--- |--- |--- |--- |--- |
| aggregation | 4 | 100.0% | 100.0% | 34.23s |  |
| extreme-values | 1 | 100.0% | 100.0% | 42.83s |  |
| filtering | 2 | 100.0% | 100.0% | 43.37s |  |
| location-based | 3 | 100.0% | 100.0% | 22.33s |  |
| multi-year-comparison | 1 | 100.0% | 100.0% | 42.47s |  |
| nested-aggregation | 1 | 100.0% | 100.0% | 53.49s |  |
| overview | 3 | 100.0% | 100.0% | 30.73s |  |
| subsampling | 1 | 100.0% | 100.0% | 61.61s |  |

## 📐 Template-wise Analysis
| Template | Tested | Success | Rate | Avg Time | Common Errors |
|--- |--- |--- |--- |--- |--- |
| all_properties_summary | 1 | 1 | 100.0% | 56.26s |  |
| average_for_property_date_range | 1 | 1 | 100.0% | 5.32s |  |
| daily_aggregates | 1 | 1 | 100.0% | 7.61s |  |
| features_near_coordinates | 1 | 1 | 100.0% | 4.10s |  |
| filtered_timeseries | 2 | 2 | 100.0% | 43.37s |  |
| list_features_of_interest | 1 | 1 | 100.0% | 18.79s |  |
| list_properties | 1 | 1 | 100.0% | 17.14s |  |
| location_based_summary | 1 | 1 | 100.0% | 8.76s |  |
| monthly_aggregates | 1 | 1 | 100.0% | 55.41s |  |
| monthly_mean_from_daily | 1 | 1 | 100.0% | 53.49s |  |
| sample_observations | 1 | 1 | 100.0% | 61.61s |  |
| timeseries_statistics | 2 | 2 | 100.0% | 55.53s |  |
| timeseries_statistics_by_feature | 1 | 1 | 100.0% | 54.12s |  |
| top_extremes_for_property | 1 | 1 | 100.0% | 42.83s |  |

## ❌ Error Analysis
| Error Category | Count |
|--- |--- |

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

## 📝 Detailed Results (Run 1)
| ID | Cat | Question | Expected | Predicted | Match | Rows | Time |
|--- |--- |--- |--- |--- |--- |--- |--- |
| 1 | overview | What variables are available? | list_properties | list_properties | ✅ | 5 | 17.14s |
| 2 | overview | List all locations of observations available | list_features_of_interest | list_features_of_interest | ✅ | 10 | 18.79s |
| 3 | subsampling | Give me examples of observations in the dataset | sample_observations | sample_observations | ✅ | 0 | 61.61s |
| 4 | overview | Give me an overview of climate observations for 2024 | all_properties_summary | all_properties_summary | ✅ | 2 | 56.26s |
| 5 | aggregation | Calculate temperature statistics for 2024 | timeseries_statistics | timeseries_statistics | ✅ | 1 | 68.59s |
| 6 | aggregation | Show me average precipitation in March 1975 | average_for_property_date_range | average_for_property_date_range | ✅ | 1 | 5.32s |
| 7 | aggregation | Show monthly temperature averages for 2022 | monthly_aggregates | monthly_aggregates | ✅ | 10 | 55.41s |
| 8 | aggregation | Show daily temperature averages for January 2024 | daily_aggregates | daily_aggregates | ✅ | 10 | 7.61s |
| 9 | extreme-values | Show me the lowest precipitation amounts in 1955 | top_extremes_for_property | top_extremes_for_property | ✅ | 10 | 42.83s |
| 10 | filtering | Find precipitation values below 12 mm and above 10 mm in 200 | filtered_timeseries | filtered_timeseries | ✅ | 10 | 40.33s |
| 11 | filtering | Find temperature readings above 30 degrees in Summer 2024 | filtered_timeseries | filtered_timeseries | ✅ | 10 | 46.42s |
| 12 | location-based | What are grids near lat: 67.8, lon: 20.3 | features_near_coordinates | features_near_coordinates | ✅ | 10 | 4.10s |
| 13 | location-based | What was the weather like in Poland in 1970? | location_based_summary | location_based_summary | ✅ | 4 | 8.76s |
| 14 | nested-aggregation | What was the mean daily temperature in 2021? | monthly_mean_from_daily | monthly_mean_from_daily | ✅ | 1 | 53.49s |
| 15 | location-based | Compare temperature across different grid points in 2019 | timeseries_statistics_by_feature | timeseries_statistics_by_feature | ✅ | 10 | 54.12s |
| 16 | multi-year-comparison | Show me wind speed trends for the last 5 years | timeseries_statistics | timeseries_statistics | ✅ | 1 | 42.47s |