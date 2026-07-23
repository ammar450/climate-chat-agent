# Climate Chat Agent — Evaluation Report
**Generated:** 2026-07-23T15:17:47.780381  
**Random Seed:** 25110  
**Runs:** 2 × 2 test cases

---
# Statistics across all 2 runs
## 📊 Aggregate Metrics
| Metric | Value |
|--- |--- |
| Template Accuracy | 100.0% ± 0.0% |
| Template Accuracy Range | 100.0% – 100.0% |
| Success Rate - Query Creation | 100.0% |
| Success Rate - Query Execution | 100.0% |
| Avg Latency | 16.86s |
| Latency Range | 15.24s – 18.38s |
| **Overall Score** | **100.0%** |

## 🏷️ Category-wise Analysis
| Category | Tests | Templ Acc | Exec Success | Avg Time | 
|--- |--- |--- |--- |--- |
| overview | 4 | 100.0% | 100.0% | 16.86s |

## 📐 Template-wise Analysis
| Template | Tested | Success | Rate | Avg Time | 
|--- |--- |--- |--- |--- |
| list_features_of_interest | 2 | 2 | 100.0% | 18.34s | 
| list_properties | 2 | 2 | 100.0% | 15.39s | 

## ❌ Error Analysis
| Category | Count | Top failure reasons (count) | Topics |
|---------|-------|---------------------------|--------|
| n/a     | n/a   | n/a                       | n/a    |

| Template | Count | Top failure reasons (count) | Topics |
|---------|-------|---------------------------|--------|
| n/a     | n/a   | n/a                       | n/a    |

## 🔀 Confusion Matrix
| Expected ↓ / Predicted → | list_features_of_interest | list_properties |
|---|---|---|
| list_features_of_interest | 2 | 0 |
| list_properties | 0 | 2 |

---
# Statistics per run
## 📋 Per-Run Summary
| Run | Templ Acc | Generation Success | Execution Success | Avg Time |
|--- |--- |--- |--- |--- |
| 1 | 100.0% | 100.0% | 100.0% | 16.92s |
| 2 | 100.0% | 100.0% | 100.0% | 16.81s |

## 📝 Detailed Results (Run 1)
| ID | Cat | Question | Expected | Predicted | Match | Rows | Time |
|--- |--- |--- |--- |--- |--- |--- |--- |
| 1 | overview | Which variables can be queried? | list_properties | list_properties | ✅ | 5 | 15.54s |
| 2 | overview | What are locations of observations available in the dataset? | list_features_of_interest | list_features_of_interest | ✅ | 10 | 18.30s |
## 📝 Detailed Results (Run 2)
| ID | Cat | Question | Expected | Predicted | Match | Rows | Time |
|--- |--- |--- |--- |--- |--- |--- |--- |
| 1 | overview | Which variables can be queried? | list_properties | list_properties | ✅ | 5 | 15.24s |
| 2 | overview | What are grids available in the dataset? | list_features_of_interest | list_features_of_interest | ✅ | 10 | 18.38s |