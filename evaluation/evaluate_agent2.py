"""
Climate Chat Agent — Comprehensive Evaluation Framework v2.0

Evaluates agent performance across 5 randomized runs with:
- Per-run and aggregate metrics
- Template accuracy, execution success, answer correctness
- Category-wise and template-wise breakdown
- Confusion matrix, error classification
- JSON, CSV, and Markdown report generation

Usage:
    python evaluation/evaluate_agent.py                    # 5 runs, random seed
    python evaluation/evaluate_agent.py --seed 42           # reproducible
    python evaluation/evaluate_agent.py --runs 3            # fewer runs
    python evaluation/evaluate_agent.py --model openai:gpt-4o-mini
"""

import os
import sys
import json
import time
import random
import statistics
import argparse
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from collections import defaultdict, Counter


# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.agent.graph_agent import run_agent
from src.llm.llm_client import chat as llm_chat, LLMError


# ──────────────────────────────────────────────
# LLM-AS-JUDGE
# ──────────────────────────────────────────────

JUDGE_SYSTEM_PROMPT = """
You are a judge to assess whether the execution of a SPARQL query has been successful. 
You will receive a question and a set of rows. Your role is to make an assessment. 
If you think that the query has been successful, return TRUE. If not, return FALSE. 
In each case, provide a short explanation. Also, if the query has not been successful, provide likely reasons for the failure, only based on what you see in the rows.

Return ONLY a valid JSON object.

The JSON object must have exactly this structure:

{
  "success": true | false,
  "explanation": "<short explanation>",
  "failure_reasons": ["<reason1>", "<reason2>", ...]
}

Rules:
- Do not wrap the JSON in markdown.
- Do not include any extra text before or after the JSON.
- If success is TRUE, failure_reasons must be an empty array
"""

def run_llm_judge(
    question: str,
    sparql_bindings: str,
    model: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Use an LLM to assess if the execution of the SPARQL query has been successful.
    """

    user_content = f"""Question: {question}

Evidence (raw SPARQL results):
{sparql_bindings}

"""

    messages = [
        {"role": "system", "content": JUDGE_SYSTEM_PROMPT.strip()},
        {"role": "user", "content": user_content},
    ]

    # Parse model spec "provider:model_name"
    provider, model_name = None, None
    if model and ":" in model:
        provider, model_name = model.split(":", 1)

    try:
        raw = llm_chat(messages, provider=provider, model=model_name, temperature=0.0, max_tokens=500)
        # Strip markdown code fences if present
        raw = raw.strip()
        if raw.startswith("```"):
            raw = raw.split("\n", 1)[-1]
            raw = raw.rsplit("```", 1)[0].strip()
        parsed = json.loads(raw)
        return {
            "success": parsed['success'],
            "explanation": parsed['explanation'],
            "failure_reasons": parsed['failure_reasons']
        }
    except (LLMError, json.JSONDecodeError, Exception) as exc:
        return {
            "success": None,
            "explanation": None,
            "failure_reasons": str(exc)[:200]
        }



# ──────────────────────────────────────────────
# ERROR ANALYSIS - LLM-based
# ──────────────────────────────────────────────

SUMMARIZATION_PROMPT = """
You are AI assistant specialized in summarizing the input data, which is about some errors. 

You need to provide two summaries as nicely formatted markdown tables: One according to the most frequent errors according to the template, 
and the other according to the most frequent errors according to the category. These are two views on the data. 
Where appropriate, you can categorize them according to the unique topic that they touch.

Columns for the 'summary_per_template': 'Template | Count | Top failure reasons (count) | Topics
Columns for the 'summary_per_category': 'Category | Count | Top failure reasons (count) | Topics

If there are no errors at all, return a table with the columns plus one blank line. The blank line should be 
visible to users. Add : n/a in each cell of the line. Do not add placeholder information in the tables.

Return ONLY a valid JSON object.

The JSON object must have exactly this structure:

{{
  "summary_per_template": '<summary>',
  "summary_per_category": '<summary>'
}}

Rules:
- Do not wrap the JSON in markdown.
- Do not include any extra text before or after the JSON.
"""

def analyze_errors(
    results: List[Dict],
    model: Optional[str] = None) -> str:
    """
    Use an LLM to analyze the errors that occured during the execution (across all runs)
    """
    # extract errors from the set of results
    errors = []

    for run in results: 
        test_results = run['test_results']

        for r in test_results: 
            error_entry = {
                "test_id": "",
                "category": "",
                "expected_template": "",
                "execution_failure_reasons": None }
            #print(r)
            if r['execution_failure_reasons'] != [] :
                error_entry["test_id"] = r['test_id']
                error_entry["category"] = r['category']
                error_entry["expected_template"] = r['expected_template']
                error_entry["execution_failure_reasons"] = r['execution_failure_reasons']
                errors.append(error_entry)

    errors_str = json.dumps(errors, indent=2)

    # Parse model spec "provider:model_name"
    provider, model_name = None, None
    if model and ":" in model:
        provider, model_name = model.split(":", 1)

    messages = [{"role": "system", "content": SUMMARIZATION_PROMPT.strip()},
                {"role": "user", "content": "Errors: \n{errors}"}]

    # Run error analysis
    error_analysis = llm_chat(messages, provider=provider, model=model_name, temperature=0.0, max_tokens=500)

    return error_analysis
# ──────────────────────────────────────────────
# SINGLE RUN EVALUATOR
# ──────────────────────────────────────────────

def run_single_evaluation(
    test_cases: List[Dict],
    model: str = None,
    run_number: int = 1,
) -> Dict[str, Any]:
    """Run one evaluation pass over all test cases with random question selection."""
    
    run_results = {
        "run_number": run_number,
        "timestamp": datetime.now().isoformat(),
        "total_tests": len(test_cases),
        "test_results": [],
        "summary": {},
    }

    i = 0  
    for tc in test_cases:
        qid = tc["id"]
        category = tc.get("category", "unknown")
        expected_template = tc["expected_template"]
        difficulty = tc.get("difficulty", "medium")

        questions = tc.get("question", [])
        selected_question = random.choice(questions) if questions else ""

        result_entry = {
            "test_id": qid,
            "category": category,
            "difficulty": difficulty,
            "selected_question": selected_question,
            "expected_template": expected_template,
            "predicted_template": None,
            "template_match": False,
            "execution_success": False,
            "execution_explanation": "",
            "execution_failure_reasons": None,
            "execution_time_seconds": 0,
            "sparql_query": "",
            "sparql_success": False,
            "returned_rows": 0,
            "answer": "",
            "notes": "",
        }

        try:
            session_id = f"eval-r{run_number}-t{qid}"
            start = time.time()
            result = run_agent(session_id, selected_question, model=model)
            elapsed = time.time() - start

            predicted = result.get("used_template", "error")
            sparql_query = result.get("sparql").replace("\n", " ")
            answer = result.get("answer", "")
            rows = result.get("rows", [])
            exec_assessment = run_llm_judge(selected_question, rows, model=model)
            #print("PARSED2", exec_assessment)
            result_entry["predicted_template"] = predicted
            result_entry["template_match"] = (predicted == expected_template)
            result_entry["execution_success"] = exec_assessment['success'] # compare bindings and question to see if the question has likely been a success          
            result_entry["execution_time_seconds"] = round(elapsed, 3)
            result_entry["execution_explanation"] = exec_assessment['explanation']
            result_entry["sparql_query"] = sparql_query # sparql query generated
            result_entry["sparql_success"] = bool(sparql_query) # check if there is a SPARQL query generated
            result_entry["returned_rows"] = len(rows) if rows else 0
            result_entry["answer"] = answer[:500]
            result_entry["execution_failure_reasons"] = exec_assessment['failure_reasons']

        except Exception as e:
            elapsed = time.time() - start if 'start' in dir() else 0
            result_entry["execution_success"] = False
            result_entry["execution_time_seconds"] = round(elapsed, 3)
            result_entry["execution_failure_reasons"] = exec_assessment['failure_reasons'] 
            result_entry["notes"] = str(e)[:200]

        run_results["test_results"].append(result_entry)
        i = i+1
        if i == 2: 
           break

    # Compute summary
    total = len(run_results["test_results"])
    template_matches = sum(1 for r in run_results["test_results"] if r["template_match"])
    exec_successes = sum(1 for r in run_results["test_results"] if r["execution_success"])
    sparql_successes = sum(1 for r in run_results["test_results"] if r["sparql_success"])
    times = [r["execution_time_seconds"] for r in run_results["test_results"]]

    run_results["summary"] = {
        "total": total,
        "template_accuracy": round(template_matches / total, 4) if total else 0,
        "execution_success_rate": round(exec_successes / total, 4) if total else 0,
        "sparql_success_rate": round(sparql_successes / total, 4) if total else 0,
        "avg_execution_time": round(statistics.mean(times), 3) if times else 0,
        "min_execution_time": round(min(times), 3) if times else 0,
        "max_execution_time": round(max(times), 3) if times else 0,
        "std_execution_time": round(statistics.stdev(times), 3) if len(times) > 1 else 0,
    }

    return run_results


# ──────────────────────────────────────────────
# AGGREGATE OVER MULTIPLE RUNS
# ──────────────────────────────────────────────

def aggregate_runs(all_runs: List[Dict[str, Any]], test_cases: List[Dict]) -> Dict[str, Any]:
    """Aggregate metrics across multiple evaluation runs."""
    num_runs = len(all_runs)
    summaries = [r["summary"] for r in all_runs]

    agg = {
        "num_runs": num_runs,
        "total_tests_per_run": summaries[0]["total"],
        "aggregate_metrics": {
            "avg_template_accuracy": round(statistics.mean([s["template_accuracy"] for s in summaries]), 4),
            "std_template_accuracy": round(statistics.stdev([s["template_accuracy"] for s in summaries]), 4) if num_runs > 1 else 0,
            "min_template_accuracy": round(min(s["template_accuracy"] for s in summaries), 4),
            "max_template_accuracy": round(max(s["template_accuracy"] for s in summaries), 4),
            "avg_execution_success_rate": round(statistics.mean([s["execution_success_rate"] for s in summaries]), 4),
            "avg_sparql_success_rate": round(statistics.mean([s["sparql_success_rate"] for s in summaries]), 4),
            "avg_latency": round(statistics.mean([s["avg_execution_time"] for s in summaries]), 3),
            "min_latency": round(min(s["min_execution_time"] for s in summaries), 3),
            "max_latency": round(max(s["max_execution_time"] for s in summaries), 3),
            "std_latency": round(statistics.stdev([s["avg_execution_time"] for s in summaries]), 3) if num_runs > 1 else 0,
        },
        "overall_score": round(
            statistics.mean([ s["template_accuracy"] * 0.5 + s["execution_success_rate"] * 0.5 for s in summaries ]), 4
        ),
    }

    # Confusion matrix
    confusion = defaultdict(lambda: defaultdict(int))
    for run in all_runs:
        for tr in run["test_results"]:
            expected = tr["expected_template"]
            predicted = tr["predicted_template"] or "error"
            confusion[expected][predicted] += 1
    agg["confusion_matrix"] = {k: dict(v) for k, v in confusion.items()}

    # Category-wise
    cat_stats = defaultdict(lambda: {"total": 0, "template_match": 0, "exec_success": 0, "times": [], "errors": Counter()})
    for run in all_runs:
        for tr in run["test_results"]:
            cat = tr["category"]
            cat_stats[cat]["total"] += 1
            if tr["template_match"]: cat_stats[cat]["template_match"] += 1
            if tr["execution_success"]: cat_stats[cat]["exec_success"] += 1
            cat_stats[cat]["times"].append(tr["execution_time_seconds"])
            #if tr["error_category"]: cat_stats[cat]["errors"][tr["error_category"]] += 1

    agg["category_analysis"] = {}
    for cat, stats in sorted(cat_stats.items()):
        t = stats["total"]
        agg["category_analysis"][cat] = {
            "total": t,
            "template_accuracy": round(stats["template_match"] / t, 4) if t else 0,
            "execution_success_rate": round(stats["exec_success"] / t, 4) if t else 0,
            "avg_execution_time": round(statistics.mean(stats["times"]), 3) if stats["times"] else 0,
        }

    # Template-wise
    tpl_stats = defaultdict(lambda: {"total": 0, "success": 0, "times": [], "errors": Counter()})
    for run in all_runs:
        for tr in run["test_results"]:
            tpl = tr["expected_template"]
            tpl_stats[tpl]["total"] += 1
            if tr["execution_success"] and tr["template_match"]: tpl_stats[tpl]["success"] += 1
            tpl_stats[tpl]["times"].append(tr["execution_time_seconds"])
            #if tr["error_category"]: tpl_stats[tpl]["errors"][tr["error_category"]] += 1

    agg["template_analysis"] = {}
    for tpl, stats in sorted(tpl_stats.items()):
        t = stats["total"]
        agg["template_analysis"][tpl] = {
            "total_tested": t, "successful": stats["success"],
            "success_rate": round(stats["success"] / t, 4) if t else 0,
            "avg_response_time": round(statistics.mean(stats["times"]), 3) if stats["times"] else 0,
        }

    return agg


# ──────────────────────────────────────────────
# REPORT GENERATION
# ──────────────────────────────────────────────

def generate_json_report(all_runs: List[Dict], aggregate: Dict, seed: int, output_path: str):
    report = {
        "metadata": {"evaluation_timestamp": datetime.now().isoformat(), "random_seed": seed,
                      "num_runs": len(all_runs), "test_questions_file": "evaluation/test_questions.json"},
        "aggregate_metrics": aggregate,
        "per_run_results": all_runs,
        "per_run_summaries": [r["summary"] for r in all_runs],
    }
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    print(f"[REPORT] JSON -> {output_path}")


def generate_csv_report(aggregate: Dict, output_path: str):
    import csv
    m = aggregate.get("aggregate_metrics", {})
    rows = [
        ["Metric", "Value"],
        ["avg_template_accuracy", m.get("avg_template_accuracy", 0)],
        ["std_template_accuracy", m.get("std_template_accuracy", 0)],
        ["min_template_accuracy", m.get("min_template_accuracy", 0)],
        ["max_template_accuracy", m.get("max_template_accuracy", 0)],
        ["avg_execution_success_rate", m.get("avg_execution_success_rate", 0)],
        ["avg_sparql_success_rate", m.get("avg_sparql_success_rate", 0)],
        ["avg_latency", m.get("avg_latency", 0)],
        ["min_latency", m.get("min_latency", 0)],
        ["max_latency", m.get("max_latency", 0)],
        ["std_latency", m.get("std_latency", 0)],
        ["overall_score", aggregate.get("overall_score", 0)],
        [], ["Category", "Total", "TemplateAccuracy", "ExecSuccessRate", "AvgTime"],
    ]
    for cat, stats in aggregate.get("category_analysis", {}).items():
        rows.append([cat, stats["total"], stats["template_accuracy"], stats["execution_success_rate"], stats["avg_execution_time"]])
    rows.append([])
    rows.append(["ErrorCategory", "Count"])
    for err, count in aggregate.get("error_analysis", {}).items():
        rows.append([err, count])
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        csv.writer(f).writerows(rows)
    print(f"[REPORT] CSV -> {output_path}")


def generate_markdown_report(all_runs: List[Dict], aggregate: Dict, seed: int, model: str, output_path: str):
    m = aggregate.get("aggregate_metrics", {})
    L = []
    L.append("# Climate Chat Agent — Evaluation Report")
    L.append(f"**Generated:** {datetime.now().isoformat()}  ")
    L.append(f"**Random Seed:** {seed}  ")
    L.append(f"**Runs:** {len(all_runs)} × {aggregate.get('total_tests_per_run', 0)} test cases")
    L.append("")
    L.append("## 📊 Aggregate Metrics")
    L.append("| Metric | Value |")
    L.append("|--- |--- |")
    L.append(f"| Template Accuracy | {m.get('avg_template_accuracy', 0):.1%} ± {m.get('std_template_accuracy', 0):.1%} |")
    L.append(f"| Template Accuracy Range | {m.get('min_template_accuracy', 0):.1%} – {m.get('max_template_accuracy', 0):.1%} |")
    L.append(f"| Success Rate - Query Creation | {m.get('avg_sparql_success_rate', 0):.1%} |")
    L.append(f"| Success Rate - Query Execution | {m.get('avg_execution_success_rate', 0):.1%} |")
    L.append(f"| Avg Latency | {m.get('avg_latency', 0):.2f}s |")
    L.append(f"| Latency Range | {m.get('min_latency', 0):.2f}s – {m.get('max_latency', 0):.2f}s |")
    L.append(f"| **Overall Score** | **{aggregate.get('overall_score', 0):.1%}** |")
    L.append("")
    L.append("## 📋 Per-Run Summary")
    L.append("| Run | Templ Acc | Generation Success | Execution Success | Avg Time |")
    L.append("|--- |--- |--- |--- |--- |")
    for run in all_runs:
        s = run["summary"]
        L.append(f"| {run['run_number']} | {s['template_accuracy']:.1%} | {s['sparql_success_rate']:.1%} | {s['execution_success_rate']:.1%} | {s['avg_execution_time']:.2f}s |")
    L.append("")
    L.append("## 🏷️ Category-wise Analysis")
    L.append("| Category | Tests | Templ Acc | Exec Success | Avg Time | ")
    L.append("|--- |--- |--- |--- |--- |")
    for cat, stats in aggregate.get("category_analysis", {}).items():
        L.append(f"| {cat} | {stats['total']} | {stats['template_accuracy']:.1%} | {stats['execution_success_rate']:.1%} | {stats['avg_execution_time']:.2f}s |")
    L.append("")
    L.append("## 📐 Template-wise Analysis")
    L.append("| Template | Tested | Success | Rate | Avg Time | ")
    L.append("|--- |--- |--- |--- |--- |")
    for tpl, stats in aggregate.get("template_analysis", {}).items():
        L.append(f"| {tpl} | {stats['total_tested']} | {stats['successful']} | {stats['success_rate']:.1%} | {stats['avg_response_time']:.2f}s | ")
    L.append("")
    
    L.append("## ❌ Error Analysis")
    
    print(f"[EVAL] Model used for the error analysis {model}")

    error_summaries = json.loads(analyze_errors(all_runs, model))
    print(type(error_summaries), error_summaries)
    L.append(error_summaries['summary_per_category'])
    L.append("")

    L.append(error_summaries['summary_per_template'])
    L.append("")

    L.append("## 🔀 Confusion Matrix")
    cm = aggregate.get("confusion_matrix", {})
    all_tpl = sorted(set(cm.keys()) | {p for v in cm.values() for p in v})
    L.append("| Expected ↓ / Predicted → | " + " | ".join(all_tpl) + " |")
    L.append("|" + "|".join(["---"] * (len(all_tpl) + 1)) + "|")
    for exp in sorted(cm.keys()):
        row = f"| {exp} | " + " | ".join(str(cm[exp].get(p, 0)) for p in all_tpl) + " |"
        L.append(row)
    L.append("")

    for i in range(len(all_runs)): 
        L.append(f"## 📝 Detailed Results (Run {i+1})")
        L.append("| ID | Cat | Question | Expected | Predicted | Match | Rows | Time |")
        L.append("|--- |--- |--- |--- |--- |--- |--- |--- |")
        for tr in all_runs[i]["test_results"]:
            q = tr["selected_question"][:60]
            mch = "✅" if tr["template_match"] else "❌"
            L.append(f"| {tr['test_id']} | {tr['category']} | {q} | {tr['expected_template']} | {tr['predicted_template']} | {mch} | {tr['returned_rows']} | {tr['execution_time_seconds']:.2f}s |")
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(L))
    print(f"[REPORT] MD -> {output_path}")


# ──────────────────────────────────────────────
# MAIN
# ──────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Climate Chat Agent — Comprehensive Evaluation v2")
    parser.add_argument("--runs", type=int, default=5, help="Number of evaluation runs")
    parser.add_argument("--seed", type=int, default=None, help="Random seed for reproducibility")
    parser.add_argument("--model", type=str, default="gpt-5.4-nano", help="LLM model")
    parser.add_argument("--test-file", type=str, default="evaluation/test_questions.json")
    parser.add_argument("--output-dir", type=str, default="evaluation/to-delete")
    args = parser.parse_args()

    seed = args.seed if args.seed is not None else random.randint(1, 99999)
    random.seed(seed)

    test_file = os.path.join(os.path.dirname(__file__), "test_questions.json")
    with open(test_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    test_cases = data["test_cases"]
    print(f"[EVAL] Loaded {len(test_cases)} test cases")
    print(f"[EVAL] Model used for the evaluation {args.model}")

    all_runs = []
    for rn in range(1, args.runs + 1):
        print(f"\n[EVAL] === Run {rn}/{args.runs} ===")

        rr = run_single_evaluation(test_cases, model=args.model, run_number=rn)
        s = rr["summary"]

        print(f"[EVAL] Run {rn}: acc={s['template_accuracy']:.1%} ok={s['execution_success_rate']:.1%} "
              f"t={s['avg_execution_time']:.2f}")
        all_runs.append(rr)

    print(f"\n[EVAL] Aggregating...")
    agg = aggregate_runs(all_runs, test_cases)

    od = args.output_dir
    os.makedirs(od, exist_ok=True)
    generate_json_report(all_runs, agg, seed, os.path.join(od, "evaluation_results.json"))
    generate_csv_report(agg, os.path.join(od, "evaluation_summary.csv"))
    generate_markdown_report(all_runs, agg, seed, args.model, os.path.join(od, "evaluation_summary.md"))

    m = agg["aggregate_metrics"]
    print("\n" + "=" * 60)
    print("FINAL SUMMARY")
    print("=" * 60)
    print(f"  Template Accuracy:  {m['avg_template_accuracy']:.1%} +/- {m['std_template_accuracy']:.1%}")
    print(f"  Success - Query Execution:  {m['avg_execution_success_rate']:.1%}")
    print(f"  Success - Query Creation:  {m['avg_sparql_success_rate']:.1%}")
    print(f"  Avg Latency:        {m['avg_latency']:.2f}s")
    print(f"  Overall Score:      {agg['overall_score']:.1%}")
    print("=" * 60)


if __name__ == "__main__":
    main()
