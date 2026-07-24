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
# ERROR ANALYSIS - LLM-based
# ──────────────────────────────────────────────

SUMMARIZATION_PROMPT = """
You are AI assistant specialized in summarizing the input data, which is about some errors. 

You need to provide two summaries as nicely formatted markdown tables: One according to the most frequent errors according to the template, 
and the other according to the most frequent errors according to the category. These are two views on the data. 
Where appropriate, you can categorize them according to the unique topic that they touch.

Columns for the 'summary_per_template': 'Template | Count | Top failure reasons (count) | Topics
Columns for the 'summary_per_category': 'Category | Count | Top failure reasons (count) | Topics

If there are no errors at all, return a table with the columns plus one line. The line should be 
visible to users. Add n/a in each cell of the line. Do not add placeholder information in the tables.

<output_format>

The result must have exactly this structure:

" <table 1> \n <table 2> "

</output_format>

"""


NEW_PROMPT = """
You are an AI assistant specialized in summarizing input data about errors.

You need to produce two summaries as structured data: one grouped by template, 
and one grouped by category. Where appropriate, group rows further by unique topic.

Return ONLY a valid JSON object with exactly this structure (double quotes only, 
no trailing commas, no markdown fences, no text before or after):

{{
  "summary_per_template": [
    {{"template": "string", "count": number, "top_failure_reasons": "string", "topics": "string"}}
  ],
  "summary_per_category": [
    {{"category": "string", "count": number, "top_failure_reasons": "string", "topics": "string"}}
  ]
}}

Rules:
- If there are no errors at all, return exactly one row per list with all fields set to "n/a".
- Do not invent or add placeholder data otherwise.
- "top_failure_reasons" should list the most frequent reasons with their counts in parentheses, 
  e.g. "timeout (5), invalid_input (3)".
- Every string value must be a single line — do not include literal newlines inside any string.
- Output must be parseable by a standard JSON parser. Double-check quoting and escaping before responding.
"""

def analyze_errors(
    results: List[Dict],
    model: Optional[str] = None) -> str:
    """
    Use an LLM to analyze the errors that occured during the execution (across all runs)
    """

    all_runs = results['per_run_results']
    # extract errors from the set of results
    errors = []

    for run in all_runs: 
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

    print(errors_str)

    # Parse model spec "provider:model_name"
    provider, model_name = None, None
    if model and ":" in model:
        provider, model_name = model.split(":", 1)

    messages = [{"role": "system", "content": SUMMARIZATION_PROMPT.strip()},
                {"role": "user", "content": f"Errors: \n{errors_str}"}]

    # Run error analysis
    error_analysis = llm_chat(messages, provider=provider, model=model_name, temperature=0.0, max_tokens=500)

    return error_analysis


def aggregate(data, group_key):
    groups = defaultdict(lambda: {"count": 0, "reason_counts": Counter()})
    
    for entry in data:
        key = entry[group_key]
        groups[key]["count"] += 1
        for reason in entry["execution_failure_reasons"]:
            groups[key]["reason_counts"][reason] += 1
    
    # Convert to a clean list, sorted by count desc
    result = []
    for key, info in sorted(groups.items(), key=lambda x: -x[1]["count"]):
        top_reasons = info["reason_counts"].most_common(5)  # cap so it can't grow unbounded
        result.append({
            "key": key,
            "count": info["count"],
            "top_failure_reasons": [{"reason": r, "count": c} for r, c in top_reasons]
        })
    return result




def generate_markdown_report(input_dir: str, model: str, output_dir: str):
    
    print(os.path.join(os.path.dirname(__file__)))

    os.makedirs(input_dir, exist_ok=True)

    input_file = os.path.join(input_dir, "evaluation_results.json")
    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)
   
    all_runs = data #['per_run_results']
    
    L = []

    L.append("## ❌ Error Analysis")
    
    print(f"[EVAL] Model used for the error analysis {model}")
    test = analyze_errors(all_runs, model)
    print(type(test))
    print(test)

    L.append(test)
    L.append("")

    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "evaluation_summary.md")    

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(L))
    print(f"[REPORT] MD -> {output_path}")



generate_markdown_report("evaluation/to-delete/", "gpt-5.4-nano", "evaluation/to-delete2/")

