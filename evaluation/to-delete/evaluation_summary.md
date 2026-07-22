# Climate Chat Agent — Evaluation Report
**Generated:** 2026-07-22T19:44:41.538234  
**Random Seed:** 36343  
**Runs:** 1 × 16 test cases

## 📊 Aggregate Metrics
| Metric | Value |
|--- |--- |
| Template Accuracy | 100.0% ± 0.0% |
| Template Accuracy Range | 100.0% – 100.0% |
| Success Rate - Query Execution | 18.8% |
| Success Rate - Query Creation | 93.8% |
| Avg Latency | 28.42s |
| Latency Range | 2.15s – 60.71s |
| **Overall Score** | **59.4%** |

## 📋 Per-Run Summary
| Run | Templ Acc | Exec Success | Avg Time |
|--- |--- |--- |--- |
| 1 | 100.0% | 18.8% | 28.42s |

## 🏷️ Category-wise Analysis
| Category | Tests | Templ Acc | Exec Success | Avg Time | Common Errors |
|--- |--- |--- |--- |--- |--- |
| aggregation | 4 | 100.0% | 25.0% | 24.16s |  |
| extreme-values | 1 | 100.0% | 0.0% | 37.34s |  |
| filtering | 2 | 100.0% | 0.0% | 37.89s |  |
| location-based | 3 | 100.0% | 0.0% | 14.72s |  |
| multi-year-comparison | 1 | 100.0% | 0.0% | 60.71s |  |
| nested-aggregation | 1 | 100.0% | 0.0% | 54.00s |  |
| overview | 3 | 100.0% | 33.3% | 15.68s |  |
| subsampling | 1 | 100.0% | 100.0% | 39.00s |  |

## 📐 Template-wise Analysis
| Template | Tested | Success | Rate | Avg Time | Common Errors |
|--- |--- |--- |--- |--- |--- |
| all_properties_summary | 1 | 0 | 0.0% | 12.25s |  |
| average_for_property_date_range | 1 | 1 | 100.0% | 37.21s |  |
| daily_aggregates | 1 | 0 | 0.0% | 4.62s |  |
| features_near_coordinates | 1 | 0 | 0.0% | 2.42s |  |
| filtered_timeseries | 2 | 0 | 0.0% | 37.89s |  |
| list_features_of_interest | 1 | 1 | 100.0% | 18.76s |  |
| list_properties | 1 | 0 | 0.0% | 16.04s |  |
| location_based_summary | 1 | 0 | 0.0% | 7.13s |  |
| monthly_aggregates | 1 | 0 | 0.0% | 2.15s |  |
| monthly_mean_from_daily | 1 | 0 | 0.0% | 54.00s |  |
| sample_observations | 1 | 1 | 100.0% | 39.00s |  |
| timeseries_statistics | 2 | 0 | 0.0% | 56.70s |  |
| timeseries_statistics_by_feature | 1 | 0 | 0.0% | 34.60s |  |
| top_extremes_for_property | 1 | 0 | 0.0% | 37.34s |  |

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
| 1 | overview | What variables are available? | list_properties | list_properties | ✅ | 5 | 16.04s |
| 2 | overview | What are grids available in the dataset? | list_features_of_interest | list_features_of_interest | ✅ | 10 | 18.76s |
| 3 | subsampling | Show me some sample observations | sample_observations | sample_observations | ✅ | 10 | 39.00s |
| 4 | overview | What was the climate like in 1950? | all_properties_summary | all_properties_summary | ✅ | 3 | 12.25s |
| 5 | aggregation | What are statistics about relative humidity for 1960? | timeseries_statistics | timeseries_statistics | ✅ | 1 | 52.69s |
| 6 | aggregation | What is the average humidity for 2010? | average_for_property_date_range | average_for_property_date_range | ✅ | 1 | 37.21s |
| 7 | aggregation | What was the wettest month in 2023? | monthly_aggregates | monthly_aggregates | ✅ | 0 | 2.15s |
| 8 | aggregation | Give me daily precipitation statistics for June 1970 | daily_aggregates | daily_aggregates | ✅ | 10 | 4.62s |
| 9 | extreme-values | Show me the lowest precipitation amounts in 1955 | top_extremes_for_property | top_extremes_for_property | ✅ | 10 | 37.34s |
| 10 | filtering | Show me humidity values between 30 and 40 percent in 2022 | filtered_timeseries | filtered_timeseries | ✅ | 10 | 32.86s |
| 11 | filtering | Find temperature readings above 30 degrees in Summer 2024 | filtered_timeseries | filtered_timeseries | ✅ | 10 | 42.91s |
| 12 | location-based | Find observation points around lat: 52.5, lon: 13.4 | features_near_coordinates | features_near_coordinates | ✅ | 10 | 2.42s |
| 13 | location-based | Show me climate data in Germany during 2024 | location_based_summary | location_based_summary | ✅ | 4 | 7.13s |
| 14 | nested-aggregation | What was the mean daily temperature in 2001? | monthly_mean_from_daily | monthly_mean_from_daily | ✅ | 1 | 54.00s |
| 15 | location-based | Compare humidity across different grid points in 2019 | timeseries_statistics_by_feature | timeseries_statistics_by_feature | ✅ | 10 | 34.60s |
| 16 | multi-year-comparison | Compare humidity between 1950 and 2024 | timeseries_statistics | timeseries_statistics | ✅ | 0 | 60.71s |