# Climate Chat Agent — Evaluation Report
**Generated:** 2026-07-22T13:16:41.079497  
**Random Seed:** 72184  
**Runs:** 1 × 16 test cases

## 📊 Aggregate Metrics
| Metric | Value |
|--- |--- |
| Template Accuracy | 100.0% ± 0.0% |
| Template Accuracy Range | 100.0% – 100.0% |
| Success Rate - Query Execution | 100.0% |
| Success Rate - Query Creation | 100.0% |
| Avg Latency | 34.66s |
| Latency Range | 3.16s – 65.93s |
| **Overall Score** | **100.0%** |

## 📋 Per-Run Summary
| Run | Templ Acc | Exec Success | Avg Time |
|--- |--- |--- |--- |
| 1 | 100.0% | 100.0% | 34.66s |

## 🏷️ Category-wise Analysis
| Category | Tests | Templ Acc | Exec Success | Avg Time | Common Errors |
|--- |--- |--- |--- |--- |--- |
| aggregation | 4 | 100.0% | 100.0% | 32.34s |  |
| extreme-values | 1 | 100.0% | 100.0% | 46.50s |  |
| filtering | 2 | 100.0% | 100.0% | 39.58s |  |
| location-based | 3 | 100.0% | 100.0% | 19.36s |  |
| multi-year-comparison | 1 | 100.0% | 100.0% | 60.71s |  |
| nested-aggregation | 1 | 100.0% | 100.0% | 51.95s |  |
| overview | 3 | 100.0% | 100.0% | 20.97s |  |
| subsampling | 1 | 100.0% | 100.0% | 65.93s |  |

## 📐 Template-wise Analysis
| Template | Tested | Success | Rate | Avg Time | Common Errors |
|--- |--- |--- |--- |--- |--- |
| all_properties_summary | 1 | 1 | 100.0% | 29.80s |  |
| average_for_property_date_range | 1 | 1 | 100.0% | 33.98s |  |
| daily_aggregates | 1 | 1 | 100.0% | 9.30s |  |
| features_near_coordinates | 1 | 1 | 100.0% | 3.47s |  |
| filtered_timeseries | 2 | 2 | 100.0% | 39.58s |  |
| list_features_of_interest | 1 | 1 | 100.0% | 17.24s |  |
| list_properties | 1 | 1 | 100.0% | 15.86s |  |
| location_based_summary | 1 | 1 | 100.0% | 3.16s |  |
| monthly_aggregates | 1 | 1 | 100.0% | 38.51s |  |
| monthly_mean_from_daily | 1 | 1 | 100.0% | 51.95s |  |
| sample_observations | 1 | 1 | 100.0% | 65.93s |  |
| timeseries_statistics | 2 | 2 | 100.0% | 54.14s |  |
| timeseries_statistics_by_feature | 1 | 1 | 100.0% | 51.45s |  |
| top_extremes_for_property | 1 | 1 | 100.0% | 46.50s |  |

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
| 1 | overview | Provide an overview of observation variables in the dataset | list_properties | list_properties | ✅ | 5 | 15.86s |
| 2 | overview | What are locations of observations available in the dataset? | list_features_of_interest | list_features_of_interest | ✅ | 10 | 17.24s |
| 3 | subsampling | What are examples of observations from the current dataset | sample_observations | sample_observations | ✅ | 10 | 65.93s |
| 4 | overview | Give me an overview of climate observations for 2024 | all_properties_summary | all_properties_summary | ✅ | 2 | 29.80s |
| 5 | aggregation | Show me wind speed statistics for 2010 | timeseries_statistics | timeseries_statistics | ✅ | 1 | 47.56s |
| 6 | aggregation | What is the average humidity for 2010? | average_for_property_date_range | average_for_property_date_range | ✅ | 1 | 33.98s |
| 7 | aggregation | Calculate monthly precipitation totals for 1965 | monthly_aggregates | monthly_aggregates | ✅ | 10 | 38.51s |
| 8 | aggregation | Show daily temperature averages for January 2024 | daily_aggregates | daily_aggregates | ✅ | 10 | 9.30s |
| 9 | extreme-values | What were the highest temperature values in 2023? | top_extremes_for_property | top_extremes_for_property | ✅ | 1 | 46.50s |
| 10 | filtering | Show me humidity values between 30 and 40 percent in 2022 | filtered_timeseries | filtered_timeseries | ✅ | 10 | 35.74s |
| 11 | filtering | Find temperature readings above 30 degrees in Summer 2024 | filtered_timeseries | filtered_timeseries | ✅ | 10 | 43.41s |
| 12 | location-based | What locations are near coordinates 48.5, 9.0? | features_near_coordinates | features_near_coordinates | ✅ | 10 | 3.47s |
| 13 | location-based | What was the weather in France during 1985? | location_based_summary | location_based_summary | ✅ | 4 | 3.16s |
| 14 | nested-aggregation | What was the mean daily temperature in 2021? | monthly_mean_from_daily | monthly_mean_from_daily | ✅ | 1 | 51.95s |
| 15 | location-based | Compare temperature across different grid points in 2019 | timeseries_statistics_by_feature | timeseries_statistics_by_feature | ✅ | 10 | 51.45s |
| 16 | multi-year-comparison | Show temperature patterns decade by decade from 1950 to 2024 | timeseries_statistics | timeseries_statistics | ✅ | 0 | 60.71s |