# Climate Chat Agent — Evaluation Report
**Generated:** 2026-07-23T14:43:25.007125  
**Random Seed:** 98529  
**Runs:** 2 × 2 test cases

## 📊 Aggregate Metrics
| Metric | Value |
|--- |--- |
| Template Accuracy | 100.0% ± 0.0% |
| Template Accuracy Range | 100.0% – 100.0% |
| Success Rate - Query Creation | 100.0% |
| Success Rate - Query Execution | 100.0% |
| Avg Latency | 17.04s |
| Latency Range | 15.50s – 18.61s |
| **Overall Score** | **100.0%** |

## 📋 Per-Run Summary
| Run | Templ Acc | Generation Success | Execution Success | Avg Time |
|--- |--- |--- |--- |--- |
| 1 | 100.0% | 100.0% | 100.0% | 17.02s |
| 2 | 100.0% | 100.0% | 100.0% | 17.06s |

## 🏷️ Category-wise Analysis
| Category | Tests | Templ Acc | Exec Success | Avg Time | 
|--- |--- |--- |--- |--- |
| overview | 4 | 100.0% | 100.0% | 17.04s |

## 📐 Template-wise Analysis
| Template | Tested | Success | Rate | Avg Time | 
|--- |--- |--- |--- |--- |
| list_features_of_interest | 2 | 2 | 100.0% | 18.55s | 
| list_properties | 2 | 2 | 100.0% | 15.53s | 

## ❌ Error Analysis
| Category | Count | Top failure reasons (count) | Topics |
| n/a | n/a | n/a | n/a |


| Template | Count | Top failure reasons (count) | Topics |
| n/a | n/a | n/a | n/a |


## 🔀 Confusion Matrix
| Expected ↓ / Predicted → | list_features_of_interest | list_properties |
|---|---|---|
| list_features_of_interest | 2 | 0 |
| list_properties | 0 | 2 |

## 📝 Detailed Results (Run 1)
| ID | Cat | Question | Expected | Predicted | Match | Rows | Time |
|--- |--- |--- |--- |--- |--- |--- |--- |
| 1 | overview | What variables are available? | list_properties | list_properties | ✅ | 5 | 15.57s |
| 2 | overview | What are grids available in the dataset? | list_features_of_interest | list_features_of_interest | ✅ | 10 | 18.48s |
## 📝 Detailed Results (Run 2)
| ID | Cat | Question | Expected | Predicted | Match | Rows | Time |
|--- |--- |--- |--- |--- |--- |--- |--- |
| 1 | overview | Which variables can be queried? | list_properties | list_properties | ✅ | 5 | 15.50s |
| 2 | overview | What are locations of observations available in the dataset? | list_features_of_interest | list_features_of_interest | ✅ | 10 | 18.61s |