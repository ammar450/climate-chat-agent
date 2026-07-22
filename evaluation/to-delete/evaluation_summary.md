# Climate Chat Agent — Evaluation Report
**Generated:** 2026-07-22T08:38:38.617268  
**Random Seed:** 40192  
**Runs:** 1 × 4 test cases

## 📊 Aggregate Metrics
| Metric | Value |
|--- |--- |
| Template Accuracy | 100.0% ± 0.0% |
| Template Accuracy Range | 100.0% – 100.0% |
| Execution Success Rate | 100.0% |
| Avg Latency | 23.20s |
| Latency Range | 15.41s – 33.19s |
| **Overall Score** | **100.0%** |

## 📋 Per-Run Summary
| Run | Templ Acc | Exec Success | Avg Time |
|--- |--- |--- |--- |
| 1 | 100.0% | 100.0% | 23.20s |

## 🏷️ Category-wise Analysis
| Category | Tests | Templ Acc | Exec Success | Avg Time | Common Errors |
|--- |--- |--- |--- |--- |--- |
| overview | 3 | 100.0% | 100.0% | 19.87s |  |
| subsampling | 1 | 100.0% | 100.0% | 33.19s |  |

## 📐 Template-wise Analysis
| Template | Tested | Success | Rate | Avg Time | Common Errors |
|--- |--- |--- |--- |--- |--- |
| all_properties_summary | 1 | 1 | 100.0% | 28.72s |  |
| list_features_of_interest | 1 | 1 | 100.0% | 15.41s |  |
| list_properties | 1 | 1 | 100.0% | 15.49s |  |
| sample_observations | 1 | 1 | 100.0% | 33.19s |  |

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
| 1 | overview | What variables are available? | list_properties | list_properties | ✅ | 5 | 15.49s |
| 2 | overview | What are grids available in the dataset? | list_features_of_interest | list_features_of_interest | ✅ | 10 | 15.41s |
| 3 | subsampling | Show me some sample observations | sample_observations | sample_observations | ✅ | 10 | 33.19s |
| 4 | overview | Give me an overview of climate observations for 2024 | all_properties_summary | all_properties_summary | ✅ | 2 | 28.72s |