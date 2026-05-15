"""Compare evaluation results before and after agent improvements"""
import json
from pathlib import Path

def loadjson(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def print_comparison(before_file, after_file):
    print("=" * 80)
    print("AGENT IMPROVEMENT COMPARISON")
    print("=" * 80)
    print()
    
    before = load_json(before_file)
    after = load_json(after_file)
    
    # Overall Statistics
    print("### OVERALL STATISTICS")
    print()
    print("| Metric | Before | After | Change |")
    print("|--------|--------|-------|--------|")
    
    bs = before['summary']
    as_ = after['summary']
    
    # Template match rate
    btemplate = bs.get('template_match_rate', 0)
    atemplate = as_.get('template_match_rate', 0)
    print(f"| Template Match Rate | {btemplate:.1f}% | {atemplate:.1f}% | {atemplate-btemplate:+.1f}% |")
    
    # Success rate
    bsuccess = bs.get('success_rate', 0)
    asuccess = as_.get('success_rate', 0)
    print(f"| Execution Success | {bsuccess:.1f}% | {asuccess:.1f}% | {asuccess-bsuccess:+.1f}% |")
    
    # LLM Judge stats
    if 'llm_judge' in bs and 'llm_judge' in as_:
        blj = bs['llm_judge']
        alj = as_['llm_judge']
        
        bcorrect = blj.get('correct_count', 0)
        acorrect = alj.get('correct_count', 0)
        bpartial = blj.get('partially_correct_count', 0)
        apartial = alj.get('partially_correct_count', 0)
        bincorrect = blj.get('incorrect_count', 0)
        aincorrect = alj.get('incorrect_count', 0)
        bavg_score = blj.get('average_score', 0)
        aavg_score = alj.get('average_score', 0)
        
        total = bs.get('total_tests', 30)
        
        print(f"| Correct | {bcorrect} ({bcorrect/total*100:.1f}%) | {acorrect} ({acorrect/total*100:.1f}%) | {acorrect-bcorrect:+d} ({(acorrect-bcorrect)/total*100:+.1f}%) |")
        print(f"| Partial | {bpartial} ({bpartial/total*100:.1f}%) | {apartial} ({apartial/total*100:.1f}%) | {apartial-bpartial:+d} ({(apartial-bpartial)/total*100:+.1f}%) |")
        print(f"| Incorrect | {bincorrect} ({bincorrect/total*100:.1f}%) | {aincorrect} ({aincorrect/total*100:.1f}%) | {aincorrect-bincorrect:+d} ({(aincorrect-bincorrect)/total*100:+.1f}%) |")
        print(f"| Avg Score | {bavg_score:.3f} | {aavg_score:.3f} | {aavg_score-bavg_score:+.3f} |")
    
    print()
    print("### KEY IMPROVEMENTS")
    print()
    
    # Analyze which tests improved
    improved_tests = []
    degraded_tests = []
    
    b_results = {r['test_id']: r for r in before.get('detailed_results', [])}
    a_results = {r['test_id']: r for r in after.get('detailed_results', [])}
    
    for test_id in sorted(set(b_results.keys()) & set(a_results.keys())):
        br = b_results[test_id]
        ar = a_results[test_id]
        
        b_label = br.get('llm_judge_label', 'unknown')
        a_label = ar.get('llm_judge_label', 'unknown')
        
        # Score mapping
        score_map = {'correct': 2, 'partially_correct': 1, 'incorrect': 0, 'not_evaluated': -1}
        b_score = score_map.get(b_label, -1)
        a_score = score_map.get(a_label, -1)
        
        if a_score > b_score:
            improved_tests.append({
                'id': test_id,
                'question': br.get('question', '')[:50],
                'before': b_label,
                'after': a_label,
                'category': br.get('category', '')
            })
        elif a_score < b_score:
            degraded_tests.append({
                'id': test_id,
                'question': br.get('question', '')[:50],
                'before': b_label,
                'after': a_label,
                'category': br.get('category', '')
            })
    
    if improved_tests:
        print(f"✅ **{len(improved_tests)} Tests Improved:**")
        print()
        for t in improved_tests[:10]:  # Show first 10
            print(f"- Test #{t['id']} ({t['category']}): {t['before']} → {t['after']}")
            print(f"  \"{t['question']}...\"")
        print()
    
    if degraded_tests:
        print(f"⚠️  **{len(degraded_tests)} Tests Degraded:**")
        print()
        for t in degraded_tests[:5]:  # Show first 5
            print(f"- Test #{t['id']} ({t['category']}): {t['before']} → {t['after']}")
            print(f"  \"{t['question']}...\"")
        print()
    
    print("=" * 80)

if __name__ == "__main__":
    before = "evaluation/llm_judge_full_report.json"
    after = "evaluation/llm_judge_improved.json"
    
    if not Path(after).exists():
        print(f"⚠️  Waiting for {after} to be created...")
        print("   Evaluation still running. Please wait...")
    else:
        print_comparison(before, after)
