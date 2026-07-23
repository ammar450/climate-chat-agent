# Climate Chat Agent — Evaluation Report
**Generated:** 2026-07-23T10:00:22.864012  
**Random Seed:** 7849  
**Runs:** 1 × 2 test cases

## 📊 Aggregate Metrics
| Metric | Value |
|--- |--- |
| Template Accuracy | 100.0% ± 0.0% |
| Template Accuracy Range | 100.0% – 100.0% |
| Success Rate - Query Creation | 100.0% |
| Success Rate - Query Execution | 100.0% |
| Avg Latency | 17.50s |
| Latency Range | 15.76s – 19.24s |
| **Overall Score** | **100.0%** |

## 📋 Per-Run Summary
| Run | Templ Acc | Generation Success | Execution Success | Avg Time |
|--- |--- |--- |--- |--- |
| 1 | 100.0% | 100.0% | 100.0% | 17.50s |

## 🏷️ Category-wise Analysis
| Category | Tests | Templ Acc | Exec Success | Avg Time | Common Errors |
|--- |--- |--- |--- |--- |--- |
| overview | 2 | 100.0% | 100.0% | 17.50s |  |

## 📐 Template-wise Analysis
| Template | Tested | Success | Rate | Avg Time | Common Errors |
|--- |--- |--- |--- |--- |--- |
| list_features_of_interest | 1 | 1 | 100.0% | 19.24s |  |
| list_properties | 1 | 1 | 100.0% | 15.76s |  |

## ❌ Error Analysis
| Category         | Count | Top failure reasons (count) | Topics               |
|------------------|-------|---------------------------|----------------------|
| Category 1      | 15    | Reason 1 (5), Reason 2 (3)| Topic 1, Topic 2    |
| Category 2      | 8     | Reason 3 (4)              | Topic 3              |
| Category 3      | 5     | Reason 5 (3)              | Topic 4              |
| Template         | Count | Top failure reasons (count) | Topics               |
|------------------|-------|---------------------------|----------------------|
| Template A      | 10    | Reason 1 (5), Reason 2 (3)| Topic 1, Topic 2    |
| Template B      | 8     | Reason 3 (4), Reason 4 (2)| Topic 3              |
| Template C      | 5     | Reason 5 (3)              | Topic 4              |

## 🔀 Confusion Matrix
| Expected ↓ / Predicted → | list_features_of_interest | list_properties |
|---|---|---|
| list_features_of_interest | 1 | 0 |
| list_properties | 0 | 1 |

## 📝 Detailed Results (Run 1)
| ID | Cat | Question | Expected | Predicted | Match | Rows | Time |
|--- |--- |--- |--- |--- |--- |--- |--- |
| 1 | overview | Provide an overview of observation variables in the dataset | list_properties | list_properties | ✅ | 5 | 15.76s |
| 2 | overview | What are locations of observations available in the dataset? | list_features_of_interest | list_features_of_interest | ✅ | 10 | 19.24s |