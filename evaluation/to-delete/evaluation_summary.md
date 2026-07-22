# Climate Chat Agent — Evaluation Report
**Generated:** 2026-07-22T14:27:33.647101  
**Random Seed:** 37590  
**Runs:** 1 × 3 test cases

## 📊 Aggregate Metrics
| Metric | Value |
|--- |--- |
| Template Accuracy | 100.0% ± 0.0% |
| Template Accuracy Range | 100.0% – 100.0% |
| Success Rate - Query Execution | 100.0% |
| Success Rate - Query Creation | 100.0% |
| Avg Latency | 26.30s |
| Latency Range | 15.94s – 46.24s |
| **Overall Score** | **100.0%** |

## 📋 Per-Run Summary
| Run | Templ Acc | Exec Success | Avg Time |
|--- |--- |--- |--- |
| 1 | 100.0% | 100.0% | 26.30s |

## 🏷️ Category-wise Analysis
| Category | Tests | Templ Acc | Exec Success | Avg Time | Common Errors |
|--- |--- |--- |--- |--- |--- |
| overview | 2 | 100.0% | 100.0% | 16.33s |  |
| subsampling | 1 | 100.0% | 100.0% | 46.24s |  |

## 📐 Template-wise Analysis
| Template | Tested | Success | Rate | Avg Time | Common Errors |
|--- |--- |--- |--- |--- |--- |
| list_features_of_interest | 1 | 1 | 100.0% | 16.72s |  |
| list_properties | 1 | 1 | 100.0% | 15.94s |  |
| sample_observations | 1 | 1 | 100.0% | 46.24s |  |

## ❌ Error Analysis
| Error Category | Count |
|--- |--- |

## 🔀 Confusion Matrix
| Expected ↓ / Predicted → | list_features_of_interest | list_properties | sample_observations |
|---|---|---|---|
| list_features_of_interest | 1 | 0 | 0 |
| list_properties | 0 | 1 | 0 |
| sample_observations | 0 | 0 | 1 |

## 📝 Detailed Results (Run 1)
| ID | Cat | Question | Expected | Predicted | Match | Rows | Time |
|--- |--- |--- |--- |--- |--- |--- |--- |
| 1 | overview | What variables are available? | list_properties | list_properties | ✅ | 5 | 15.94s |
| 2 | overview | What are grids available in the dataset? | list_features_of_interest | list_features_of_interest | ✅ | 10 | 16.72s |
| 3 | subsampling | Give me examples of observations in the dataset | sample_observations | sample_observations | ✅ | 10 | 46.24s |