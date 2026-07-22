# Climate Chat Agent — Evaluation Report
**Generated:** 2026-07-22T10:24:18.247871  
**Random Seed:** 45862  
**Runs:** 1 × 4 test cases

## 📊 Aggregate Metrics
| Metric | Value |
|--- |--- |
| Template Accuracy | 100.0% ± 0.0% |
| Template Accuracy Range | 100.0% – 100.0% |
| Execution Success Rate | 100.0% |
| Avg Latency | 21.25s |
| Latency Range | 15.49s – 33.01s |
| **Overall Score** | **100.0%** |

## 📋 Per-Run Summary
| Run | Templ Acc | Exec Success | Avg Time |
|--- |--- |--- |--- |
| 1 | 100.0% | 100.0% | 21.25s |

## 🏷️ Category-wise Analysis
| Category | Tests | Templ Acc | Exec Success | Avg Time | Common Errors |
|--- |--- |--- |--- |--- |--- |
| overview | 3 | 100.0% | 100.0% | 17.33s |  |
| subsampling | 1 | 100.0% | 100.0% | 33.01s |  |

## 📐 Template-wise Analysis
| Template | Tested | Success | Rate | Avg Time | Common Errors |
|--- |--- |--- |--- |--- |--- |
| all_properties_summary | 1 | 1 | 100.0% | 20.72s |  |
| list_features_of_interest | 1 | 1 | 100.0% | 15.78s |  |
| list_properties | 1 | 1 | 100.0% | 15.49s |  |
| sample_observations | 1 | 1 | 100.0% | 33.01s |  |

## ❌ Error Analysis
| Error Category | Count |
|--- |--- |

## 🔀 Confusion Matrix
| Expected ↓ / Predicted → | all_properties_summary | list_features_of_interest | list_properties | sample_observations |
|---|---|---|---|---|
| all_properties_summary | 1 | 0 | 0 | 0 |
| list_features_of_interest | 0 | 1 | 0 | 0 |
| list_properties | 0 | 0 | 1 | 0 |
| sample_observations | 0 | 0 | 0 | 1 |

## 📝 Detailed Results (Run 1)
| ID | Cat | Question | Expected | Predicted | Match | Rows | Time |
|--- |--- |--- |--- |--- |--- |--- |--- |
| 1 | overview | Provide an overview of observation variables in the dataset | list_properties | list_properties | ✅ | 5 | 15.49s |
| 2 | overview | List all locations of observations available | list_features_of_interest | list_features_of_interest | ✅ | 10 | 15.78s |
| 3 | subsampling | Show me some sample observations | sample_observations | sample_observations | ✅ | 10 | 33.01s |
| 4 | overview | Show me climate data for 2000 | all_properties_summary | all_properties_summary | ✅ | 2 | 20.72s |