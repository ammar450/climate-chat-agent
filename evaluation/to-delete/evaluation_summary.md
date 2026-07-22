# Climate Chat Agent — Evaluation Report
**Generated:** 2026-07-22T22:34:19.687629  
**Random Seed:** 87281  
**Runs:** 1 × 16 test cases

## 📊 Aggregate Metrics
| Metric | Value |
|--- |--- |
| Template Accuracy | 100.0% ± 0.0% |
| Template Accuracy Range | 100.0% – 100.0% |
| Success Rate - Query Creation | 100.0% |
| Success Rate - Query Execution | 81.2% |
| Avg Latency | 31.12s |
| Latency Range | 1.86s – 60.72s |
| **Overall Score** | **90.6%** |

## 📋 Per-Run Summary
| Run | Templ Acc | Generation Success | Execution Success | Avg Time |
|--- |--- |--- |--- |--- |
| 1 | 100.0% | 100.0% | 81.2% | 31.12s |

## 🏷️ Category-wise Analysis
| Category | Tests | Templ Acc | Exec Success | Avg Time | Common Errors |
|--- |--- |--- |--- |--- |--- |
| aggregation | 4 | 100.0% | 100.0% | 38.49s |  |
| extreme-values | 1 | 100.0% | 100.0% | 33.35s |  |
| filtering | 2 | 100.0% | 50.0% | 34.20s |  |
| location-based | 3 | 100.0% | 66.7% | 13.02s |  |
| multi-year-comparison | 1 | 100.0% | 0.0% | 60.72s |  |
| nested-aggregation | 1 | 100.0% | 100.0% | 53.92s |  |
| overview | 3 | 100.0% | 100.0% | 18.16s |  |
| subsampling | 1 | 100.0% | 100.0% | 33.98s |  |

## 📐 Template-wise Analysis
| Template | Tested | Success | Rate | Avg Time | Common Errors |
|--- |--- |--- |--- |--- |--- |
| all_properties_summary | 1 | 1 | 100.0% | 21.02s |  |
| average_for_property_date_range | 1 | 1 | 100.0% | 48.74s |  |
| daily_aggregates | 1 | 1 | 100.0% | 3.50s |  |
| features_near_coordinates | 1 | 1 | 100.0% | 1.86s |  |
| filtered_timeseries | 2 | 1 | 50.0% | 34.20s |  |
| list_features_of_interest | 1 | 1 | 100.0% | 17.97s |  |
| list_properties | 1 | 1 | 100.0% | 15.49s |  |
| location_based_summary | 1 | 0 | 0.0% | 2.99s |  |
| monthly_aggregates | 1 | 1 | 100.0% | 52.46s |  |
| monthly_mean_from_daily | 1 | 1 | 100.0% | 53.92s |  |
| sample_observations | 1 | 1 | 100.0% | 33.98s |  |
| timeseries_statistics | 2 | 1 | 50.0% | 54.99s |  |
| timeseries_statistics_by_feature | 1 | 1 | 100.0% | 34.20s |  |
| top_extremes_for_property | 1 | 1 | 100.0% | 33.35s |  |

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
| 1 | overview | Which variables can be queried? | list_properties | list_properties | ✅ | 5 | 15.49s |
| 2 | overview | What are grids available in the dataset? | list_features_of_interest | list_features_of_interest | ✅ | 10 | 17.97s |
| 3 | subsampling | What are examples of observations from the current dataset | sample_observations | sample_observations | ✅ | 10 | 33.98s |
| 4 | overview | Show me climate data for 2000 | all_properties_summary | all_properties_summary | ✅ | 2 | 21.02s |
| 5 | aggregation | What are statistics about relative humidity for 1960? | timeseries_statistics | timeseries_statistics | ✅ | 1 | 49.26s |
| 6 | aggregation | What was the average temperature in 2020? | average_for_property_date_range | average_for_property_date_range | ✅ | 1 | 48.74s |
| 7 | aggregation | Show monthly temperature averages for 2022 | monthly_aggregates | monthly_aggregates | ✅ | 10 | 52.46s |
| 8 | aggregation | Give me daily precipitation statistics for June 1970 | daily_aggregates | daily_aggregates | ✅ | 10 | 3.50s |
| 9 | extreme-values | What were the highest humidity values in 1970 | top_extremes_for_property | top_extremes_for_property | ✅ | 2 | 33.35s |
| 10 | filtering | Find precipitation values below 12 mm and above 10 mm in 200 | filtered_timeseries | filtered_timeseries | ✅ | 10 | 34.32s |
| 11 | filtering | Find precipitation values above 30 mm in 2000 | filtered_timeseries | filtered_timeseries | ✅ | 10 | 34.08s |
| 12 | location-based | Find observation points around lat: 52.5, lon: 13.4 | features_near_coordinates | features_near_coordinates | ✅ | 10 | 1.86s |
| 13 | location-based | Show me climate data in Germany during 2024 | location_based_summary | location_based_summary | ✅ | 4 | 2.99s |
| 14 | nested-aggregation | What was the mean daily temperature in 2001? | monthly_mean_from_daily | monthly_mean_from_daily | ✅ | 1 | 53.92s |
| 15 | location-based | Compare wind speed across different grid points in 2019 | timeseries_statistics_by_feature | timeseries_statistics_by_feature | ✅ | 10 | 34.20s |
| 16 | multi-year-comparison | Show temperature patterns decade by decade from 1950 to 2024 | timeseries_statistics | timeseries_statistics | ✅ | 0 | 60.72s |