# Climate Chat Agent — Evaluation Report
**Generated:** 2026-07-22T10:18:44.262406  
**Random Seed:** 39491  
**Runs:** 1 × 4 test cases

## 📊 Aggregate Metrics
| Metric | Value |
|--- |--- |
| Template Accuracy | 100.0% ± 0.0% |
| Template Accuracy Range | 100.0% – 100.0% |
| Execution Success Rate | 100.0% |
| Avg Latency | 17.88s |
| Latency Range | 6.21s – 34.21s |
| **Overall Score** | **100.0%** |

## 📋 Per-Run Summary
| Run | Templ Acc | Exec Success | Avg Time |
|--- |--- |--- |--- |
| 1 | 100.0% | 100.0% | 17.88s |

## 🏷️ Category-wise Analysis
| Category | Tests | Templ Acc | Exec Success | Avg Time | Common Errors |
|--- |--- |--- |--- |--- |--- |
| overview | 3 | 100.0% | 100.0% | 12.44s |  |
| subsampling | 1 | 100.0% | 100.0% | 34.21s |  |

## 📐 Template-wise Analysis
| Template | Tested | Success | Rate | Avg Time | Common Errors |
|--- |--- |--- |--- |--- |--- |
| all_properties_summary | 1 | 1 | 100.0% | 6.21s |  |
| list_features_of_interest | 1 | 1 | 100.0% | 15.44s |  |
| list_properties | 1 | 1 | 100.0% | 15.68s |  |
| sample_observations | 1 | 1 | 100.0% | 34.21s |  |

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
| 1 | overview | Provide an overview of observation variables in the dataset | list_properties | list_properties | ✅ | 5 | 15.68s |
| 2 | overview | List all locations of observations available | list_features_of_interest | list_features_of_interest | ✅ | 10 | 15.44s |
| 3 | subsampling | Show me some sample observations | sample_observations | sample_observations | ✅ | 10 | 34.21s |
| 4 | overview | What was the climate like in 1950? | all_properties_summary | all_properties_summary | ✅ | 3 | 6.21s |