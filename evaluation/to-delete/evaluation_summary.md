# Climate Chat Agent — Evaluation Report
**Generated:** 2026-07-22T11:31:00.810656  
**Random Seed:** 83307  
**Runs:** 1 × 16 test cases

## 📊 Aggregate Metrics
| Metric | Value |
|--- |--- |
| Template Accuracy | 100.0% ± 0.0% |
| Template Accuracy Range | 100.0% – 100.0% |
| Execution Success Rate | 100.0% |
| Avg Latency | 31.05s |
| Latency Range | 1.97s – 60.66s |
| **Overall Score** | **100.0%** |

## 📋 Per-Run Summary
| Run | Templ Acc | Exec Success | Avg Time |
|--- |--- |--- |--- |
| 1 | 100.0% | 100.0% | 31.05s |

## 🏷️ Category-wise Analysis
| Category | Tests | Templ Acc | Exec Success | Avg Time | Common Errors |
|--- |--- |--- |--- |--- |--- |
| aggregation | 4 | 100.0% | 100.0% | 29.99s |  |
| extreme-values | 1 | 100.0% | 100.0% | 36.67s |  |
| filtering | 2 | 100.0% | 100.0% | 42.91s |  |
| location-based | 3 | 100.0% | 100.0% | 14.66s |  |
| multi-year-comparison | 1 | 100.0% | 100.0% | 60.66s |  |
| nested-aggregation | 1 | 100.0% | 100.0% | 55.06s |  |
| overview | 3 | 100.0% | 100.0% | 20.21s |  |
| subsampling | 1 | 100.0% | 100.0% | 34.09s |  |

## 📐 Template-wise Analysis
| Template | Tested | Success | Rate | Avg Time | Common Errors |
|--- |--- |--- |--- |--- |--- |
| all_properties_summary | 1 | 1 | 100.0% | 29.34s |  |
| average_for_property_date_range | 1 | 1 | 100.0% | 36.25s |  |
| daily_aggregates | 1 | 1 | 100.0% | 32.82s |  |
| features_near_coordinates | 1 | 1 | 100.0% | 2.15s |  |
| filtered_timeseries | 2 | 2 | 100.0% | 42.91s |  |
| list_features_of_interest | 1 | 1 | 100.0% | 15.50s |  |
| list_properties | 1 | 1 | 100.0% | 15.79s |  |
| location_based_summary | 1 | 1 | 100.0% | 3.58s |  |
| monthly_aggregates | 1 | 1 | 100.0% | 1.97s |  |
| monthly_mean_from_daily | 1 | 1 | 100.0% | 55.06s |  |
| sample_observations | 1 | 1 | 100.0% | 34.09s |  |
| timeseries_statistics | 2 | 2 | 100.0% | 54.79s |  |
| timeseries_statistics_by_feature | 1 | 1 | 100.0% | 38.25s |  |
| top_extremes_for_property | 1 | 1 | 100.0% | 36.67s |  |

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
| 1 | overview | Which variables can be queried? | list_properties | list_properties | ✅ | 5 | 15.79s |
| 2 | overview | What are grids available in the dataset? | list_features_of_interest | list_features_of_interest | ✅ | 10 | 15.50s |
| 3 | subsampling | Give me examples of observations in the dataset | sample_observations | sample_observations | ✅ | 10 | 34.09s |
| 4 | overview | Give me an overview of climate observations for 2024 | all_properties_summary | all_properties_summary | ✅ | 2 | 29.34s |
| 5 | aggregation | What are statistics about relative humidity for 1960? | timeseries_statistics | timeseries_statistics | ✅ | 1 | 48.92s |
| 6 | aggregation | What is the average humidity for 2010? | average_for_property_date_range | average_for_property_date_range | ✅ | 1 | 36.25s |
| 7 | aggregation | What was the wettest month in 2023? | monthly_aggregates | monthly_aggregates | ✅ | 0 | 1.97s |
| 8 | aggregation | What are daily humidity averages for March 2000 | daily_aggregates | daily_aggregates | ✅ | 10 | 32.82s |
| 9 | extreme-values | What were the highest humidity values in 1970 | top_extremes_for_property | top_extremes_for_property | ✅ | 2 | 36.67s |
| 10 | filtering | Find precipitation values below 12 mm and above 10 mm in 200 | filtered_timeseries | filtered_timeseries | ✅ | 10 | 38.67s |
| 11 | filtering | Find temperature readings above 30 degrees in Summer 2024 | filtered_timeseries | filtered_timeseries | ✅ | 10 | 47.14s |
| 12 | location-based | What locations are near coordinates 48.5, 9.0? | features_near_coordinates | features_near_coordinates | ✅ | 10 | 2.15s |
| 13 | location-based | Show me climate data in Germany during 2024 | location_based_summary | location_based_summary | ✅ | 4 | 3.58s |
| 14 | nested-aggregation | What was the mean daily temperature in 2021? | monthly_mean_from_daily | monthly_mean_from_daily | ✅ | 1 | 55.06s |
| 15 | location-based | Compare humidity across different grid points in 2019 | timeseries_statistics_by_feature | timeseries_statistics_by_feature | ✅ | 10 | 38.25s |
| 16 | multi-year-comparison | Show temperature patterns decade by decade from 1950 to 2024 | timeseries_statistics | timeseries_statistics | ✅ | 0 | 60.66s |