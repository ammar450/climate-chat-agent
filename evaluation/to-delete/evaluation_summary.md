# Climate Chat Agent — Evaluation Report
**Generated:** 2026-07-24T22:16:11.838129  
**Random Seed:** 42  
**Runs:** 1 × 2 test cases

---
# Statistics across all 1 runs
## 📊 Aggregate Metrics
| Metric | Value |
|--- |--- |
| Template Accuracy | 100.0% ± 0.0% |
| Template Accuracy Range | 100.0% – 100.0% |
| Success Rate - Query Creation | 100.0% |
| Success Rate - Query Execution | 100.0% |
| Avg Latency | 16.32s |
| Latency Range | 15.49s – 17.15s |
| **Overall Score** | **100.0%** |

## 🏷️ Category-wise Analysis
| Category | Tests | Templ Acc | Exec Success | Avg Time | 
|--- |--- |--- |--- |--- |
| overview | 2 | 100.0% | 100.0% | 16.32s |

## 📐 Template-wise Analysis
| Template | Tested | Success | Rate | Avg Time | 
|--- |--- |--- |--- |--- |
| list_features_of_interest | 1 | 1 | 100.0% | 17.15s | 
| list_properties | 1 | 1 | 100.0% | 15.49s | 

## ❌ Error Analysis
| Template | Count | Top failure reasons (count) | Topics |
|----------|-------|-----------------------------|--------|
| n/a      | n/a   | n/a                         | n/a    |

| Category | Count | Top failure reasons (count) | Topics |
|----------|-------|-----------------------------|--------|
| n/a      | n/a   | n/a                         | n/a    |

## 🔀 Confusion Matrix
| Expected ↓ / Predicted → | list_features_of_interest | list_properties |
|---|---|---|
| list_features_of_interest | 1 | 0 |
| list_properties | 0 | 1 |

---
# Statistics per run
## 📋 Per-Run Summary
| Run | Templ Acc | Generation Success | Execution Success | Avg Time |
|--- |--- |--- |--- |--- |
| 1 | 100.0% | 100.0% | 100.0% | 16.32s |

## 📝 Detailed Results (Run 1)
| ID | Cat | Question | Expected | Predicted | Match | Rows | Time |
|--- |--- |--- |--- |--- |--- |--- |--- |
| 1 | overview | Provide an overview of observation variables in the dataset | list_properties | list_properties | ✅ | 5 | 15.49s |
| 2 | overview | List all locations of observations available | list_features_of_interest | list_features_of_interest | ✅ | 10 | 17.15s |