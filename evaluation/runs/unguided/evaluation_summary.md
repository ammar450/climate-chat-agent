# Climate Chat Agent — Evaluation Report
**Generated:** 2026-07-04T17:35:42.625960  
**Random Seed:** 42  
**Runs:** 5 × 16 test cases

## 📊 Aggregate Metrics
| Metric | Value |
|--- |--- |
| Template Accuracy | 100.0% ± 0.0% |
| Template Accuracy Range | 100.0% – 100.0% |
| Execution Success Rate | 100.0% |
| Answer Correct | 0 / run |
| Answer Partial | 4 / run |
| Answer Incorrect | 12 / run |
| Avg Latency | 19.69s |
| Latency Range | 8.20s – 77.12s |
| **Overall Score** | **60.0%** |

## 📋 Per-Run Summary
| Run | Templ Acc | Exec Success | Correct | Partial | Incorrect | Avg Time |
|--- |--- |--- |--- |--- |--- |--- |
| 1 | 100.0% | 100.0% | 0 | 4 | 12 | 19.05s |
| 2 | 100.0% | 100.0% | 0 | 4 | 12 | 19.58s |
| 3 | 100.0% | 100.0% | 0 | 4 | 12 | 25.04s |
| 4 | 100.0% | 100.0% | 0 | 3 | 13 | 24.14s |
| 5 | 100.0% | 100.0% | 0 | 3 | 13 | 10.64s |

## 🏷️ Category-wise Analysis
| Category | Tests | Templ Acc | Exec Success | Avg Time | Common Errors |
|--- |--- |--- |--- |--- |--- |
| aggregation | 20 | 100.0% | 100.0% | 16.93s | Unknown failure(7), Empty SPARQL results(3), SPARQL generation failure(2) |
| extreme-values | 5 | 100.0% | 100.0% | 21.09s | Unknown failure(3), Empty SPARQL results(2) |
| filtering | 10 | 100.0% | 100.0% | 11.77s | Unknown failure(6), Empty SPARQL results(4) |
| location-based | 15 | 100.0% | 100.0% | 17.20s | Unknown failure(8), Empty SPARQL results(5) |
| multi-year-comparison | 5 | 100.0% | 100.0% | 30.47s | Empty SPARQL results(1) |
| nested-aggregation | 5 | 100.0% | 100.0% | 24.16s | Unknown failure(5) |
| overview | 15 | 100.0% | 100.0% | 23.82s | Unknown failure(11), Empty SPARQL results(3), Formatting failure(1) |
| subsampling | 5 | 100.0% | 100.0% | 24.99s | Empty SPARQL results(1) |

## 📐 Template-wise Analysis
| Template | Tested | Success | Rate | Avg Time | Common Errors |
|--- |--- |--- |--- |--- |--- |
| all_properties_summary | 5 | 5 | 100.0% | 34.50s | Unknown failure(3), Empty SPARQL results(1), Formatting failure(1) |
| average_for_property_date_range | 5 | 5 | 100.0% | 12.03s | Unknown failure(1) |
| daily_aggregates | 5 | 5 | 100.0% | 11.33s | Unknown failure(3), Empty SPARQL results(2) |
| features_near_coordinates | 5 | 5 | 100.0% | 10.86s | Unknown failure(3), Empty SPARQL results(2) |
| filtered_timeseries | 10 | 10 | 100.0% | 11.77s | Unknown failure(6), Empty SPARQL results(4) |
| list_features_of_interest | 5 | 5 | 100.0% | 17.76s | Unknown failure(4), Empty SPARQL results(1) |
| list_properties | 5 | 5 | 100.0% | 19.20s | Unknown failure(4), Empty SPARQL results(1) |
| location_based_summary | 5 | 5 | 100.0% | 22.21s | Unknown failure(2), Empty SPARQL results(1) |
| monthly_aggregates | 5 | 5 | 100.0% | 21.00s | SPARQL generation failure(2), Empty SPARQL results(1) |
| monthly_mean_from_daily | 5 | 5 | 100.0% | 24.16s | Unknown failure(5) |
| sample_observations | 5 | 5 | 100.0% | 24.99s | Empty SPARQL results(1) |
| timeseries_statistics | 10 | 10 | 100.0% | 26.91s | Unknown failure(3), Empty SPARQL results(1) |
| timeseries_statistics_by_feature | 5 | 5 | 100.0% | 18.54s | Unknown failure(3), Empty SPARQL results(2) |
| top_extremes_for_property | 5 | 5 | 100.0% | 21.09s | Unknown failure(3), Empty SPARQL results(2) |

## ❌ Error Analysis
| Error Category | Count |
|--- |--- |
| Unknown failure | 40 |
| Empty SPARQL results | 19 |
| SPARQL generation failure | 2 |
| Formatting failure | 1 |

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

## 📝 Detailed Results (Run 1)
| ID | Cat | Question | Expected | Predicted | Match | Rows | Correct | Time |
|--- |--- |--- |--- |--- |--- |--- |--- |--- |
| 1 | overview | Provide an overview of observation variables in the dataset | list_properties | list_properties | ✅ | 5 | incorrect | 17.24s |
| 2 | overview | What are grids available in the dataset? | list_features_of_interest | list_features_of_interest | ✅ | 10 | incorrect | 17.02s |
| 3 | subsampling | Show me some sample observations | sample_observations | sample_observations | ✅ | 10 | partially_correct | 22.57s |
| 4 | overview | Give me an overview of climate observations for 2024 | all_properties_summary | all_properties_summary | ✅ | 5 | incorrect | 38.73s |
| 5 | aggregation | What are statistics about relative humidity for 1960? | timeseries_statistics | timeseries_statistics | ✅ | 1 | incorrect | 25.18s |
| 6 | aggregation | Show me average precipitation in March 1975 | average_for_property_date_range | average_for_property_date_range | ✅ | 1 | partially_correct | 11.28s |
| 7 | aggregation | Calculate monthly precipitation totals for 1965 | monthly_aggregates | monthly_aggregates | ✅ | 10 | partially_correct | 19.33s |
| 8 | aggregation | Give me daily precipitation statistics for June 1970 | daily_aggregates | daily_aggregates | ✅ | 10 | incorrect | 10.32s |
| 9 | extreme-values | What were the highest temperature values in 2023? | top_extremes_for_property | top_extremes_for_property | ✅ | 1 | incorrect | 15.58s |
| 10 | filtering | Show me humidity values between 30 and 40 percent in 2022 | filtered_timeseries | filtered_timeseries | ✅ | 10 | incorrect | 10.71s |
| 11 | filtering | Find precipitation values above 30 mm in 2000 | filtered_timeseries | filtered_timeseries | ✅ | 10 | incorrect | 11.32s |
| 12 | location-based | What are grids near lat: 67.8, lon: 20.3 | features_near_coordinates | features_near_coordinates | ✅ | 10 | incorrect | 10.66s |
| 13 | location-based | What was the weather in France during 1985? | location_based_summary | location_based_summary | ✅ | 5 | incorrect | 24.07s |
| 14 | nested-aggregation | What was the mean daily temperature in 2011? | monthly_mean_from_daily | monthly_mean_from_daily | ✅ | 1 | incorrect | 32.20s |
| 15 | location-based | Compare humidity across different grid points in 2019 | timeseries_statistics_by_feature | timeseries_statistics_by_feature | ✅ | 10 | incorrect | 17.73s |
| 16 | multi-year-comparison | Show me wind speed trends for the last 5 years | timeseries_statistics | timeseries_statistics | ✅ | 1 | partially_correct | 20.93s |