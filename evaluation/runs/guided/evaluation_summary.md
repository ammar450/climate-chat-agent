# Climate Chat Agent — Evaluation Report
**Generated:** 2026-07-04T17:58:28.903995  
**Random Seed:** 42  
**Runs:** 5 × 16 test cases

## 📊 Aggregate Metrics
| Metric | Value |
|--- |--- |
| Template Accuracy | 90.0% ± 3.4% |
| Template Accuracy Range | 87.5% – 93.8% |
| Execution Success Rate | 100.0% |
| Answer Correct | 0 / run |
| Answer Partial | 2 / run |
| Answer Incorrect | 14 / run |
| **LLM Judge Score** | **0.432** |
| Judge Correct | 7 / run |
| Judge Partial | 0 / run |
| Judge Incorrect | 9 / run |
| Judge Errors | 0 / run |
| Avg Latency | 10.27s |
| Latency Range | 8.15s – 28.50s |
| **Overall Score** | **73.8%** |

## 📋 Per-Run Summary
| Run | Templ Acc | Exec Success | Correct | Partial | Incorrect | Judge Score | Judge C/P/I | Avg Time |
|--- |--- |--- |--- |--- |--- |--- |--- |--- |
| 1 | 93.8% | 100.0% | 0 | 2 | 14 | 0.438 | 7/0/9 | 11.33s |
| 2 | 93.8% | 100.0% | 0 | 1 | 15 | 0.412 | 6/1/9 | 10.39s |
| 3 | 87.5% | 100.0% | 0 | 3 | 13 | 0.438 | 7/0/9 | 10.20s |
| 4 | 87.5% | 100.0% | 0 | 1 | 15 | 0.438 | 7/0/9 | 9.63s |
| 5 | 87.5% | 100.0% | 0 | 3 | 13 | 0.438 | 7/0/9 | 9.79s |

## 🏷️ Category-wise Analysis
| Category | Tests | Templ Acc | Exec Success | Avg Time | Common Errors |
|--- |--- |--- |--- |--- |--- |
| aggregation | 20 | 100.0% | 100.0% | 9.91s | SPARQL generation failure(15), Unknown failure(2) |
| extreme-values | 5 | 100.0% | 100.0% | 9.59s | SPARQL generation failure(5) |
| filtering | 10 | 100.0% | 100.0% | 11.14s | Empty SPARQL results(10) |
| location-based | 15 | 100.0% | 100.0% | 11.35s | Empty SPARQL results(12), SPARQL generation failure(1) |
| multi-year-comparison | 5 | 40.0% | 100.0% | 10.08s | SPARQL generation failure(4), Empty SPARQL results(1) |
| nested-aggregation | 5 | 0.0% | 100.0% | 11.90s | Empty SPARQL results(5) |
| overview | 15 | 100.0% | 100.0% | 8.93s | Empty SPARQL results(11), Formatting failure(4) |
| subsampling | 5 | 100.0% | 100.0% | 9.98s | Empty SPARQL results(4), SPARQL generation failure(1) |

## 📐 Template-wise Analysis
| Template | Tested | Success | Rate | Avg Time | Common Errors |
|--- |--- |--- |--- |--- |--- |
| all_properties_summary | 5 | 5 | 100.0% | 10.38s | Formatting failure(4), Empty SPARQL results(1) |
| average_for_property_date_range | 5 | 5 | 100.0% | 10.95s | Unknown failure(2) |
| daily_aggregates | 5 | 5 | 100.0% | 9.61s | SPARQL generation failure(5) |
| features_near_coordinates | 5 | 5 | 100.0% | 9.79s | Empty SPARQL results(5) |
| filtered_timeseries | 10 | 10 | 100.0% | 11.14s | Empty SPARQL results(10) |
| list_features_of_interest | 5 | 5 | 100.0% | 8.18s | Empty SPARQL results(5) |
| list_properties | 5 | 5 | 100.0% | 8.22s | Empty SPARQL results(5) |
| location_based_summary | 5 | 5 | 100.0% | 13.46s | Empty SPARQL results(3) |
| monthly_aggregates | 5 | 5 | 100.0% | 9.60s | SPARQL generation failure(5) |
| monthly_mean_from_daily | 5 | 0 | 0.0% | 11.90s | Empty SPARQL results(5) |
| sample_observations | 5 | 5 | 100.0% | 9.98s | Empty SPARQL results(4), SPARQL generation failure(1) |
| timeseries_statistics | 10 | 7 | 70.0% | 9.78s | SPARQL generation failure(9), Empty SPARQL results(1) |
| timeseries_statistics_by_feature | 5 | 5 | 100.0% | 10.79s | Empty SPARQL results(4), SPARQL generation failure(1) |
| top_extremes_for_property | 5 | 5 | 100.0% | 9.59s | SPARQL generation failure(5) |

## ❌ Error Analysis
| Error Category | Count |
|--- |--- |
| Empty SPARQL results | 43 |
| SPARQL generation failure | 26 |
| Formatting failure | 4 |
| Unknown failure | 2 |

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
| monthly_mean_from_daily | 0 | 0 | 5 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| sample_observations | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 5 | 0 | 0 | 0 |
| timeseries_statistics | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 7 | 1 | 0 |
| timeseries_statistics_by_feature | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 5 | 0 |
| top_extremes_for_property | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 5 |

## 📝 Detailed Results (Run 1)
| ID | Cat | Question | Expected | Predicted | Match | Rows | Rule | Judge | Score | Time |
|--- |--- |--- |--- |--- |--- |--- |--- |--- |--- |--- |
| 1 | overview | Provide an overview of observation variables in the dat | list_properties | list_properties | ✅ | 0 | incorrect | correct | 1.00 | 8.26s |
| 2 | overview | What are grids available in the dataset? | list_features_of_interest | list_features_of_interest | ✅ | 0 | incorrect | correct | 1.00 | 8.15s |
| 3 | subsampling | Show me some sample observations | sample_observations | sample_observations | ✅ | 0 | incorrect | incorrect | 0.00 | 10.65s |
| 4 | overview | Give me an overview of climate observations for 2024 | all_properties_summary | all_properties_summary | ✅ | 0 | incorrect | correct | 1.00 | 8.99s |
| 5 | aggregation | What are statistics about relative humidity for 1960? | timeseries_statistics | timeseries_statistics | ✅ | 0 | incorrect | incorrect | 0.00 | 9.61s |
| 6 | aggregation | Show me average precipitation in March 1975 | average_for_property_date_range | average_for_property_date_range | ✅ | 1 | partially_correct | incorrect | 0.00 | 11.41s |
| 7 | aggregation | Calculate monthly precipitation totals for 1965 | monthly_aggregates | monthly_aggregates | ✅ | 0 | incorrect | incorrect | 0.00 | 9.63s |
| 8 | aggregation | Give me daily precipitation statistics for June 1970 | daily_aggregates | daily_aggregates | ✅ | 0 | incorrect | incorrect | 0.00 | 9.77s |
| 9 | extreme-values | What were the highest temperature values in 2023? | top_extremes_for_property | top_extremes_for_property | ✅ | 0 | incorrect | incorrect | 0.00 | 9.70s |
| 10 | filtering | Show me humidity values between 30 and 40 percent in 20 | filtered_timeseries | filtered_timeseries | ✅ | 0 | incorrect | correct | 1.00 | 12.14s |
| 11 | filtering | Find precipitation values above 30 mm in 2000 | filtered_timeseries | filtered_timeseries | ✅ | 0 | incorrect | incorrect | 0.00 | 11.18s |
| 12 | location-based | What are grids near lat: 67.8, lon: 20.3 | features_near_coordinates | features_near_coordinates | ✅ | 0 | incorrect | incorrect | 0.00 | 9.88s |
| 13 | location-based | What was the weather in France during 1985? | location_based_summary | location_based_summary | ✅ | 0 | incorrect | correct | 1.00 | 28.50s |
| 14 | nested-aggregation | What was the mean daily temperature in 2011? | monthly_mean_from_daily | daily_aggregates | ❌ | 0 | partially_correct | correct | 1.00 | 13.28s |
| 15 | location-based | Compare humidity across different grid points in 2019 | timeseries_statistics_by_feature | timeseries_statistics_by_feature | ✅ | 0 | incorrect | correct | 1.00 | 10.74s |
| 16 | multi-year-comparison | Show me wind speed trends for the last 5 years | timeseries_statistics | timeseries_statistics | ✅ | 0 | incorrect | incorrect | 0.00 | 9.41s |