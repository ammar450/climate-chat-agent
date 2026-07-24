# Climate Chat Agent — Evaluation Report
**Generated:** 2026-07-24T15:22:06.266875  
**Random Seed:** 42  
**Runs:** 5 × 2 test cases

---
# Statistics across all 5 runs
## 📊 Aggregate Metrics
| Metric | Value |
|--- |--- |
| Template Accuracy | 100.0% ± 0.0% |
| Template Accuracy Range | 100.0% – 100.0% |
| Success Rate - Query Creation | 100.0% |
| Success Rate - Query Execution | 100.0% |
| Avg Latency | 16.57s |
| Latency Range | 15.08s – 19.10s |
| **Overall Score** | **100.0%** |

## 🏷️ Category-wise Analysis
| Category | Tests | Templ Acc | Exec Success | Avg Time | 
|--- |--- |--- |--- |--- |
| overview | 10 | 100.0% | 100.0% | 16.57s |

## 📐 Template-wise Analysis
| Template | Tested | Success | Rate | Avg Time | 
|--- |--- |--- |--- |--- |
| list_features_of_interest | 5 | 5 | 100.0% | 17.66s | 
| list_properties | 5 | 5 | 100.0% | 15.49s | 

## ❌ Error Analysis
| Category | Count | Top failure reasons (count) | Topics |
|---------|-------|---------------------------|-------|
| n/a     | n/a   | n/a                       | n/a   |

| Template | Count | Top failure reasons (count) | Topics |
|---------|-------|---------------------------|-------|
| n/a     | n/a   | n/a                       | n/a   |

## 🔀 Confusion Matrix
| Expected ↓ / Predicted → | list_features_of_interest | list_properties |
|---|---|---|
| list_features_of_interest | 5 | 0 |
| list_properties | 0 | 5 |

---
# Statistics per run
## 📋 Per-Run Summary
| Run | Templ Acc | Generation Success | Execution Success | Avg Time |
|--- |--- |--- |--- |--- |
| 1 | 100.0% | 100.0% | 100.0% | 17.89s |
| 2 | 100.0% | 100.0% | 100.0% | 16.30s |
| 3 | 100.0% | 100.0% | 100.0% | 16.37s |
| 4 | 100.0% | 100.0% | 100.0% | 16.32s |
| 5 | 100.0% | 100.0% | 100.0% | 15.99s |

## 📝 Detailed Results (Run 1)
| ID | Cat | Question | Expected | Predicted | Match | Rows | Time |
|--- |--- |--- |--- |--- |--- |--- |--- |
| 1 | overview | Provide an overview of observation variables in the dataset | list_properties | list_properties | ✅ | 5 | 16.68s |
| 2 | overview | List all locations of observations available | list_features_of_interest | list_features_of_interest | ✅ | 10 | 19.10s |
## 📝 Detailed Results (Run 2)
| ID | Cat | Question | Expected | Predicted | Match | Rows | Time |
|--- |--- |--- |--- |--- |--- |--- |--- |
| 1 | overview | What variables are available? | list_properties | list_properties | ✅ | 5 | 15.08s |
| 2 | overview | What are grids available in the dataset? | list_features_of_interest | list_features_of_interest | ✅ | 10 | 17.51s |
## 📝 Detailed Results (Run 3)
| ID | Cat | Question | Expected | Predicted | Match | Rows | Time |
|--- |--- |--- |--- |--- |--- |--- |--- |
| 1 | overview | Which variables can be queried? | list_properties | list_properties | ✅ | 5 | 15.27s |
| 2 | overview | List all locations of observations available | list_features_of_interest | list_features_of_interest | ✅ | 10 | 17.47s |
## 📝 Detailed Results (Run 4)
| ID | Cat | Question | Expected | Predicted | Match | Rows | Time |
|--- |--- |--- |--- |--- |--- |--- |--- |
| 1 | overview | What variables are available? | list_properties | list_properties | ✅ | 5 | 15.25s |
| 2 | overview | List all locations of observations available | list_features_of_interest | list_features_of_interest | ✅ | 10 | 17.39s |
## 📝 Detailed Results (Run 5)
| ID | Cat | Question | Expected | Predicted | Match | Rows | Time |
|--- |--- |--- |--- |--- |--- |--- |--- |
| 1 | overview | Provide an overview of observation variables in the dataset | list_properties | list_properties | ✅ | 5 | 15.17s |
| 2 | overview | List all locations of observations available | list_features_of_interest | list_features_of_interest | ✅ | 10 | 16.81s |