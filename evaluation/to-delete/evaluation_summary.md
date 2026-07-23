# Climate Chat Agent — Evaluation Report
**Generated:** 2026-07-23T10:50:50.407337  
**Random Seed:** 78497  
**Runs:** 2 × 2 test cases

## 📊 Aggregate Metrics
| Metric | Value |
|--- |--- |
| Template Accuracy | 100.0% ± 0.0% |
| Template Accuracy Range | 100.0% – 100.0% |
| Success Rate - Query Creation | 100.0% |
| Success Rate - Query Execution | 100.0% |
| Avg Latency | 17.44s |
| Latency Range | 15.75s – 18.77s |
| **Overall Score** | **100.0%** |

## 📋 Per-Run Summary
| Run | Templ Acc | Generation Success | Execution Success | Avg Time |
|--- |--- |--- |--- |--- |
| 1 | 100.0% | 100.0% | 100.0% | 17.66s |
| 2 | 100.0% | 100.0% | 100.0% | 17.21s |

## 🏷️ Category-wise Analysis
| Category | Tests | Templ Acc | Exec Success | Avg Time | 
|--- |--- |--- |--- |--- |--- |
| overview | 4 | 100.0% | 100.0% | 17.44s |

## 📐 Template-wise Analysis
| Template | Tested | Success | Rate | Avg Time | 
|--- |--- |--- |--- |--- |--- |
| list_features_of_interest | 2 | 2 | 100.0% | 18.72s | 
| list_properties | 2 | 2 | 100.0% | 16.16s | 

## ❌ Error Analysis




## 🔀 Confusion Matrix
| Expected ↓ / Predicted → | list_features_of_interest | list_properties |
|---|---|---|
| list_features_of_interest | 2 | 0 |
| list_properties | 0 | 2 |

## 📝 Detailed Results (Run 1)
| ID | Cat | Question | Expected | Predicted | Match | Rows | Time |
|--- |--- |--- |--- |--- |--- |--- |--- |
| 1 | overview | Which variables can be queried? | list_properties | list_properties | ✅ | 5 | 16.56s |
| 2 | overview | List all locations of observations available | list_features_of_interest | list_features_of_interest | ✅ | 10 | 18.77s |
## 📝 Detailed Results (Run 2)
| ID | Cat | Question | Expected | Predicted | Match | Rows | Time |
|--- |--- |--- |--- |--- |--- |--- |--- |
| 1 | overview | Provide an overview of observation variables in the dataset | list_properties | list_properties | ✅ | 5 | 15.75s |
| 2 | overview | What are grids available in the dataset? | list_features_of_interest | list_features_of_interest | ✅ | 10 | 18.67s |