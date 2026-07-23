# Climate Chat Agent — Evaluation Report
**Generated:** 2026-07-23T10:21:21.451695  
**Random Seed:** 71484  
**Runs:** 1 × 2 test cases

## 📊 Aggregate Metrics
| Metric | Value |
|--- |--- |
| Template Accuracy | 100.0% ± 0.0% |
| Template Accuracy Range | 100.0% – 100.0% |
| Success Rate - Query Creation | 100.0% |
| Success Rate - Query Execution | 100.0% |
| Avg Latency | 17.27s |
| Latency Range | 15.91s – 18.62s |
| **Overall Score** | **100.0%** |

## 📋 Per-Run Summary
| Run | Templ Acc | Generation Success | Execution Success | Avg Time |
|--- |--- |--- |--- |--- |
| 1 | 100.0% | 100.0% | 100.0% | 17.27s |

## 🏷️ Category-wise Analysis
| Category | Tests | Templ Acc | Exec Success | Avg Time | Common Errors |
|--- |--- |--- |--- |--- |--- |
| overview | 2 | 100.0% | 100.0% | 17.27s |  |

## 📐 Template-wise Analysis
| Template | Tested | Success | Rate | Avg Time | Common Errors |
|--- |--- |--- |--- |--- |--- |
| list_features_of_interest | 1 | 1 | 100.0% | 18.62s |  |
| list_properties | 1 | 1 | 100.0% | 15.91s |  |

## ❌ Error Analysis




## 🔀 Confusion Matrix
| Expected ↓ / Predicted → | list_features_of_interest | list_properties |
|---|---|---|
| list_features_of_interest | 1 | 0 |
| list_properties | 0 | 1 |

## 📝 Detailed Results (Run 1)
| ID | Cat | Question | Expected | Predicted | Match | Rows | Time |
|--- |--- |--- |--- |--- |--- |--- |--- |
| 1 | overview | What variables are available? | list_properties | list_properties | ✅ | 5 | 15.91s |
| 2 | overview | List all locations of observations available | list_features_of_interest | list_features_of_interest | ✅ | 10 | 18.62s |