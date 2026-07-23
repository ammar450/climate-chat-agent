# Climate Chat Agent — Evaluation Report
**Generated:** 2026-07-23T10:13:09.374391  
**Random Seed:** 36353  
**Runs:** 1 × 2 test cases

## 📊 Aggregate Metrics
| Metric | Value |
|--- |--- |
| Template Accuracy | 100.0% ± 0.0% |
| Template Accuracy Range | 100.0% – 100.0% |
| Success Rate - Query Creation | 100.0% |
| Success Rate - Query Execution | 100.0% |
| Avg Latency | 17.27s |
| Latency Range | 15.80s – 18.74s |
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
| list_features_of_interest | 1 | 1 | 100.0% | 18.74s |  |
| list_properties | 1 | 1 | 100.0% | 15.80s |  |

## ❌ Error Analysis
| Category         | Count | Top failure reasons (count) | Topics               |
|------------------|-------|---------------------------|----------------------|
| Category 1      | 15    | Reason 1 (5), Reason 2 (3)| Topic 1, Topic 2    |
| Category 2      | 8     | Reason 3 (4), Reason 4 (2)| Topic 3              |
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
| 1 | overview | What variables are available? | list_properties | list_properties | ✅ | 5 | 15.80s |
| 2 | overview | List all locations of observations available | list_features_of_interest | list_features_of_interest | ✅ | 10 | 18.74s |