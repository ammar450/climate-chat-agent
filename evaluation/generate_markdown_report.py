"""
Fall-back solution, if the markdown generation fails. 
It can be run just on the json output from the experiments to see which errors were occuring most frequently.

Usage:
    python evaluation/generate_markdown_report.py                

"""

import os
import sys
import re
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

The result must have exactly this structure: " <table 1> \n <table 2> "

Return only the raw markdown content as a plain string. 
Do not wrap it in code fences or backticks. Do not add any commentary before or after.

</output_format>

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

def strip_markdown_fence(text):
    text = text.strip()
    return re.sub(r"^```(?:markdown)?\s*\n?|\n?```$", "", text).strip()


def generate_markdown_report(input_dir: str, model: str, output_dir: str):
    
    print(os.path.join(os.path.dirname(__file__)))

    os.makedirs(input_dir, exist_ok=True)

    input_file = os.path.join(input_dir, "evaluation_results.json")
    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)
   
    all_runs = data 
    
    L = []

    L.append("## ❌ Error Analysis")
    
    print(f"[EVAL] Model used for the error analysis {model}")

    raw_output = analyze_errors(all_runs, model)
    clean_output = strip_markdown_fence(raw_output)

    L.append(clean_output)
    L.append("")

    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "evaluation_summary.md")    

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(L))
    print(f"[REPORT] MD -> {output_path}")


generate_markdown_report("evaluation/to-delete/", "gpt-5.4-nano", "evaluation/to-delete2/")

