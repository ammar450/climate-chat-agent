# Climate Chat Agent — Evaluation Report
**Generated:** 2026-07-23T10:26:31.424526  
**Random Seed:** 37964  
**Runs:** 2 × 2 test cases

## 📊 Aggregate Metrics
| Metric | Value |
|--- |--- |
| Template Accuracy | 100.0% ± 0.0% |
| Template Accuracy Range | 100.0% – 100.0% |
| Success Rate - Query Creation | 100.0% |
| Success Rate - Query Execution | 100.0% |
| Avg Latency | 17.25s |
| Latency Range | 15.80s – 18.62s |
| **Overall Score** | **100.0%** |

## 📋 Per-Run Summary
| Run | Templ Acc | Generation Success | Execution Success | Avg Time |
|--- |--- |--- |--- |--- |
| 1 | 100.0% | 100.0% | 100.0% | 17.29s |
| 2 | 100.0% | 100.0% | 100.0% | 17.21s |

## 🏷️ Category-wise Analysis
| Category | Tests | Templ Acc | Exec Success | Avg Time | Common Errors |
|--- |--- |--- |--- |--- |--- |
| overview | 4 | 100.0% | 100.0% | 17.25s |  |

## 📐 Template-wise Analysis
| Template | Tested | Success | Rate | Avg Time | Common Errors |
|--- |--- |--- |--- |--- |--- |
| list_features_of_interest | 2 | 2 | 100.0% | 18.59s |  |
| list_properties | 2 | 2 | 100.0% | 15.91s |  |

## ❌ Error Analysis




## 🔀 Confusion Matrix
| Expected ↓ / Predicted → | list_features_of_interest | list_properties |
|---|---|---|
| list_features_of_interest | 2 | 0 |
| list_properties | 0 | 2 |

## 📝 Detailed Results (Run 1)
| ID | Cat | Question | Expected | Predicted | Match | Rows | Time |
|--- |--- |--- |--- |--- |--- |--- |--- |
| 1 | overview | Which variables can be queried? | list_properties | list_properties | ✅ | 5 | 16.01s |
| 2 | overview | What are grids available in the dataset? | list_features_of_interest | list_features_of_interest | ✅ | 10 | 18.57s |