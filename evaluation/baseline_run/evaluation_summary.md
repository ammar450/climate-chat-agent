# Climate Chat Agent — Evaluation Report
**Generated:** 2026-07-04T16:34:49.354702  
**Random Seed:** 42  
**Runs:** 1 × 16 test cases

## 📊 Aggregate Metrics
| Metric | Value |
|--- |--- |
| Template Accuracy | 100.0% ± 0.0% |
| Template Accuracy Range | 100.0% – 100.0% |
| Execution Success Rate | 100.0% |
| Answer Correct | 0 / run |
| Answer Partial | 4 / run |
| Answer Incorrect | 12 / run |
| Avg Latency | 19.34s |
| Latency Range | 10.92s – 38.14s |
| **Overall Score** | **60.0%** |

## 📋 Per-Run Summary
| Run | Templ Acc | Exec Success | Correct | Partial | Incorrect | Avg Time |
|--- |--- |--- |--- |--- |--- |--- |
| 1 | 100.0% | 100.0% | 0 | 4 | 12 | 19.34s |

## 🏷️ Category-wise Analysis
| Category | Tests | Templ Acc | Exec Success | Avg Time | Common Errors |
|--- |--- |--- |--- |--- |--- |
| aggregation | 4 | 100.0% | 100.0% | 17.59s | Unknown failure(2) |
| extreme-values | 1 | 100.0% | 100.0% | 15.67s | Unknown failure(1) |
| filtering | 2 | 100.0% | 100.0% | 11.23s | Unknown failure(2) |
| location-based | 3 | 100.0% | 100.0% | 17.98s | Unknown failure(3) |
| multi-year-comparison | 1 | 100.0% | 100.0% | 19.73s |  |
| nested-aggregation | 1 | 100.0% | 100.0% | 32.71s | Unknown failure(1) |
| overview | 3 | 100.0% | 100.0% | 24.31s | Unknown failure(3) |
| subsampling | 1 | 100.0% | 100.0% | 21.65s |  |

## 📐 Template-wise Analysis
| Template | Tested | Success | Rate | Avg Time | Common Errors |
|--- |--- |--- |--- |--- |--- |
| all_properties_summary | 1 | 1 | 100.0% | 38.14s | Unknown failure(1) |
| average_for_property_date_range | 1 | 1 | 100.0% | 10.93s |  |
| daily_aggregates | 1 | 1 | 100.0% | 11.24s | Unknown failure(1) |
| features_near_coordinates | 1 | 1 | 100.0% | 11.08s | Unknown failure(1) |
| filtered_timeseries | 2 | 2 | 100.0% | 11.23s | Unknown failure(2) |
| list_features_of_interest | 1 | 1 | 100.0% | 17.50s | Unknown failure(1) |
| list_properties | 1 | 1 | 100.0% | 17.29s | Unknown failure(1) |
| location_based_summary | 1 | 1 | 100.0% | 24.83s | Unknown failure(1) |
| monthly_aggregates | 1 | 1 | 100.0% | 23.38s |  |
| monthly_mean_from_daily | 1 | 1 | 100.0% | 32.71s | Unknown failure(1) |
| sample_observations | 1 | 1 | 100.0% | 21.65s |  |
| timeseries_statistics | 2 | 2 | 100.0% | 22.27s | Unknown failure(1) |
| timeseries_statistics_by_feature | 1 | 1 | 100.0% | 18.03s | Unknown failure(1) |
| top_extremes_for_property | 1 | 1 | 100.0% | 15.67s | Unknown failure(1) |

## ❌ Error Analysis
| Error Category | Count |
|--- |--- |
| Unknown failure | 12 |

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
| ID | Cat | Question | Expected | Predicted | Match | Rows | Correct | Time |
|--- |--- |--- |--- |--- |--- |--- |--- |--- |
| 1 | overview | Provide an overview of observation variables in the dataset | list_properties | list_properties | ✅ | 5 | incorrect | 17.29s |
| 2 | overview | What are grids available in the dataset? | list_features_of_interest | list_features_of_interest | ✅ | 10 | incorrect | 17.50s |
| 3 | subsampling | Show me some sample observations | sample_observations | sample_observations | ✅ | 10 | partially_correct | 21.65s |
| 4 | overview | Give me an overview of climate observations for 2024 | all_properties_summary | all_properties_summary | ✅ | 5 | incorrect | 38.14s |
| 5 | aggregation | What are statistics about relative humidity for 1960? | timeseries_statistics | timeseries_statistics | ✅ | 1 | incorrect | 24.82s |
| 6 | aggregation | Show me average precipitation in March 1975 | average_for_property_date_range | average_for_property_date_range | ✅ | 1 | partially_correct | 10.93s |
| 7 | aggregation | Calculate monthly precipitation totals for 1965 | monthly_aggregates | monthly_aggregates | ✅ | 10 | partially_correct | 23.38s |
| 8 | aggregation | Give me daily precipitation statistics for June 1970 | daily_aggregates | daily_aggregates | ✅ | 10 | incorrect | 11.24s |
| 9 | extreme-values | What were the highest temperature values in 2023? | top_extremes_for_property | top_extremes_for_property | ✅ | 1 | incorrect | 15.67s |
| 10 | filtering | Show me humidity values between 30 and 40 percent in 2022 | filtered_timeseries | filtered_timeseries | ✅ | 10 | incorrect | 10.92s |
| 11 | filtering | Find precipitation values above 30 mm in 2000 | filtered_timeseries | filtered_timeseries | ✅ | 10 | incorrect | 11.53s |
| 12 | location-based | What are grids near lat: 67.8, lon: 20.3 | features_near_coordinates | features_near_coordinates | ✅ | 10 | incorrect | 11.08s |
| 13 | location-based | What was the weather in France during 1985? | location_based_summary | location_based_summary | ✅ | 5 | incorrect | 24.83s |
| 14 | nested-aggregation | What was the mean daily temperature in 2011? | monthly_mean_from_daily | monthly_mean_from_daily | ✅ | 1 | incorrect | 32.71s |
| 15 | location-based | Compare humidity across different grid points in 2019 | timeseries_statistics_by_feature | timeseries_statistics_by_feature | ✅ | 10 | incorrect | 18.03s |
| 16 | multi-year-comparison | Show me wind speed trends for the last 5 years | timeseries_statistics | timeseries_statistics | ✅ | 1 | partially_correct | 19.73s |