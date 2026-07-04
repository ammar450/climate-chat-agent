"""Compare baseline vs LLM-judge evaluation results."""
import json, sys

base_path  = sys.argv[1] if len(sys.argv) > 1 else "evaluation/baseline_run/evaluation_results.json"
judge_path = sys.argv[2] if len(sys.argv) > 2 else "evaluation/judge_run2/evaluation_results.json"

with open(base_path)  as f: B = json.load(f)
with open(judge_path) as f: J = json.load(f)

btr = B["per_run_results"][0]["test_results"]
jtr = J["per_run_results"][0]["test_results"]
bm  = B["aggregate_metrics"]["aggregate_metrics"]
jm  = J["aggregate_metrics"]["aggregate_metrics"]

print("=" * 75)
print("AGGREGATE COMPARISON  (seed=42, 1 run, 16 tests)")
print("=" * 75)
print(f"{'Metric':<35} {'Baseline':<14} {'LLM-Judge':<14} Delta")
print("-" * 75)

def row(label, bv, jv):
    delta = round(jv - bv, 4) if isinstance(bv, float) and isinstance(jv, float) else ""
    bs = f"{bv:.4f}" if isinstance(bv, float) else str(bv)
    js = f"{jv:.4f}" if isinstance(jv, float) else str(jv)
    ds = f"{delta:+.4f}" if isinstance(delta, float) else str(delta)
    print(f"{label:<35} {bs:<14} {js:<14} {ds}")

row("Template Accuracy",      bm["avg_template_accuracy"],      jm["avg_template_accuracy"])
row("Execution Success Rate", bm["avg_execution_success_rate"], jm["avg_execution_success_rate"])
row("Rule Correct (avg)",     float(bm["avg_answer_correct"]),  float(jm["avg_answer_correct"]))
row("Rule Partial (avg)",     float(bm["avg_answer_partial"]),  float(jm["avg_answer_partial"]))
row("Rule Incorrect (avg)",   float(bm["avg_answer_incorrect"]),float(jm["avg_answer_incorrect"]))
row("Avg Latency (s)",        bm["avg_latency"],                jm["avg_latency"])
row("Overall Score",          float(B["aggregate_metrics"]["overall_score"]),
                              float(J["aggregate_metrics"]["overall_score"]))

print()
print(f"{'Judge Correct (avg)':<35} {'N/A':<14} {str(jm.get('avg_judge_correct','N/A')):<14}")
print(f"{'Judge Partial (avg)':<35} {'N/A':<14} {str(jm.get('avg_judge_partial','N/A')):<14}")
print(f"{'Judge Incorrect (avg)':<35} {'N/A':<14} {str(jm.get('avg_judge_incorrect','N/A')):<14}")
print(f"{'Avg Judge Score':<35} {'N/A':<14} {str(jm.get('avg_judge_score','N/A')):<14}")

print()
print("=" * 110)
print(f"{'ID':<4} {'Question':<50} {'Rows':<5} {'Rule':<18} {'Judge':<18} {'Score':<7} Agreement")
print("-" * 110)

for b, j in zip(btr, jtr):
    rule   = b["answer_correctness"]
    jd     = j.get("llm_judge", {})
    jlabel = jd.get("label", "-")
    jscore = jd.get("score", 0.0)
    rows_j = j["returned_rows"]
    if rule == jlabel:
        agree = "SAME"
    elif jlabel in ("incorrect",) and rule != "incorrect":
        agree = "MORE STRICT"
    elif jlabel in ("correct", "partially_correct") and rule == "incorrect":
        agree = "LESS STRICT"
    else:
        agree = "DIFF"
    q = b["selected_question"][:49]
    print(f"{b['test_id']:<4} {q:<50} {rows_j:<5} {rule:<18} {jlabel:<18} {jscore:<7.2f} {agree}")

print()
print("=" * 110)
print("JUDGE REASONS FOR DISAGREEMENTS:")
print("-" * 110)
for b, j in zip(btr, jtr):
    rule   = b["answer_correctness"]
    jd     = j.get("llm_judge", {})
    jlabel = jd.get("label", "-")
    if rule != jlabel:
        reason = jd.get("reason", "")
        miss   = jd.get("missing_coverage", [])
        wrong  = jd.get("incorrect_claims", [])
        print(f"  Test {b['test_id']}: rule={rule}  judge={jlabel}")
        print(f"    Reason : {reason}")
        if miss:  print(f"    Missing: {miss}")
        if wrong: print(f"    Wrong  : {wrong}")
        print()
