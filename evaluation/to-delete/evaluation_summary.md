# Climate Chat Agent — Evaluation Report
**Generated:** 2026-07-22T20:01:37.853693  
**Random Seed:** 29227  
**Runs:** 1 × 16 test cases

## 📊 Aggregate Metrics
| Metric | Value |
|--- |--- |
| Template Accuracy | 100.0% ± 0.0% |
| Template Accuracy Range | 100.0% – 100.0% |
| Success Rate - Query Execution | 31.2% |
| Success Rate - Query Creation | 93.8% |
| Avg Latency | 27.06s |
| Latency Range | 1.60s – 60.80s |
| **Overall Score** | **65.6%** |

## 📋 Per-Run Summary
| Run | Templ Acc | Exec Success | Avg Time |
|--- |--- |--- |--- |
| 1 | 100.0% | 31.2% | 27.06s |

## 🏷️ Category-wise Analysis
| Category | Tests | Templ Acc | Exec Success | Avg Time | Common Errors |
|--- |--- |--- |--- |--- |--- |
| aggregation | 4 | 100.0% | 25.0% | 17.35s |  |
| extreme-values | 1 | 100.0% | 0.0% | 32.66s |  |
| filtering | 2 | 100.0% | 50.0% | 33.34s |  |
| location-based | 3 | 100.0% | 0.0% | 18.59s |  |
| multi-year-comparison | 1 | 100.0% | 0.0% | 60.80s |  |
| nested-aggregation | 1 | 100.0% | 100.0% | 50.76s |  |
| overview | 3 | 100.0% | 33.3% | 21.18s |  |
| subsampling | 1 | 100.0% | 100.0% | 33.27s |  |

## 📐 Template-wise Analysis
| Template | Tested | Success | Rate | Avg Time | Common Errors |
|--- |--- |--- |--- |--- |--- |
| all_properties_summary | 1 | 0 | 0.0% | 29.17s |  |
| average_for_property_date_range | 1 | 0 | 0.0% | 12.26s |  |
| daily_aggregates | 1 | 0 | 0.0% | 6.55s |  |
| features_near_coordinates | 1 | 0 | 0.0% | 2.27s |  |
| filtered_timeseries | 2 | 1 | 50.0% | 33.34s |  |
| list_features_of_interest | 1 | 1 | 100.0% | 18.50s |  |
| list_properties | 1 | 0 | 0.0% | 15.86s |  |
| location_based_summary | 1 | 0 | 0.0% | 2.94s |  |
| monthly_aggregates | 1 | 0 | 0.0% | 1.60s |  |
| monthly_mean_from_daily | 1 | 1 | 100.0% | 50.76s |  |
| sample_observations | 1 | 1 | 100.0% | 33.27s |  |
| timeseries_statistics | 2 | 1 | 50.0% | 54.90s |  |
| timeseries_statistics_by_feature | 1 | 0 | 0.0% | 50.57s |  |
| top_extremes_for_property | 1 | 0 | 0.0% | 32.66s |  |

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
| 1 | overview | What variables are available? | list_properties | list_properties | ✅ | 5 | 15.86s |
| 2 | overview | What are locations of observations available in the dataset? | list_features_of_interest | list_features_of_interest | ✅ | 10 | 18.50s |
| 3 | subsampling | Give me examples of observations in the dataset | sample_observations | sample_observations | ✅ | 10 | 33.27s |
| 4 | overview | Give me an overview of climate observations for 2024 | all_properties_summary | all_properties_summary | ✅ | 2 | 29.17s |
| 5 | aggregation | What are statistics about relative humidity for 1960? | timeseries_statistics | timeseries_statistics | ✅ | 1 | 49.00s |
| 6 | aggregation | Show me average precipitation in March 1975 | average_for_property_date_range | average_for_property_date_range | ✅ | 1 | 12.26s |
| 7 | aggregation | What was the wettest month in 2023? | monthly_aggregates | monthly_aggregates | ✅ | 0 | 1.60s |
| 8 | aggregation | Show daily temperature averages for January 2024 | daily_aggregates | daily_aggregates | ✅ | 10 | 6.55s |
| 9 | extreme-values | What were the highest humidity values in 1970 | top_extremes_for_property | top_extremes_for_property | ✅ | 2 | 32.66s |
| 10 | filtering | Show me humidity values between 30 and 40 percent in 2022 | filtered_timeseries | filtered_timeseries | ✅ | 10 | 31.80s |
| 11 | filtering | Find precipitation values above 30 mm in 2000 | filtered_timeseries | filtered_timeseries | ✅ | 10 | 34.88s |
| 12 | location-based | What are grids near lat: 67.8, lon: 20.3 | features_near_coordinates | features_near_coordinates | ✅ | 10 | 2.27s |
| 13 | location-based | What was the weather like in Poland in 1970? | location_based_summary | location_based_summary | ✅ | 4 | 2.94s |
| 14 | nested-aggregation | What was the mean daily temperature in 2021? | monthly_mean_from_daily | monthly_mean_from_daily | ✅ | 1 | 50.76s |
| 15 | location-based | Compare temperature across different grid points in 2019 | timeseries_statistics_by_feature | timeseries_statistics_by_feature | ✅ | 10 | 50.57s |
| 16 | multi-year-comparison | Show temperature patterns decade by decade from 1950 to 2024 | timeseries_statistics | timeseries_statistics | ✅ | 0 | 60.80s |