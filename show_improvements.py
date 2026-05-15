import json

before = json.load(open('evaluation/llm_judge_full_report.json'))
after = json.load(open('evaluation/llm_judge_report.json'))

print("=" * 80)
print("AGENT IMPROVEMENTS - BEFORE vs AFTER")
print("=" * 80)
print()

bs = before['summary']
as_ = after['summary']

print("### TEMPLATE MATCHING")
print(f"Before: {bs['template_match_rate']:.1f}% ({bs['template_matches']}/30)")
print(f"After:  {as_['template_match_rate']:.1f}% ({as_['template_matches']}/30)")
print(f"Change: {as_['template_match_rate'] - bs['template_match_rate']:+.1f}% ({as_['template_matches'] - bs['template_matches']:+d} tests)")
print()

print("### LLM JUDGE EVALUATION")
blj = bs['llm_judge']
alj = as_['llm_judge']

print(f"Correct:")
print(f"  Before: {blj['correct_count']} (33.3%)")
print(f"  After:  {alj['correct_count']} ({alj['correct_count']/30*100:.1f}%)")
print(f"  Change: {alj['correct_count'] - blj['correct_count']:+d}")
print()

print(f"Partial:")
print(f"  Before: {blj['partially_correct_count']} (53.3%)")
print(f"  After:  {alj['partially_correct_count']} ({alj['partially_correct_count']/30*100:.1f}%)")
print(f"  Change: {alj['partially_correct_count'] - blj['partially_correct_count']:+d}")
print()

print(f"Incorrect:")
print(f"  Before: {blj['incorrect_count']} (10.0%)")
print(f"  After:  {alj['incorrect_count']} ({alj['incorrect_count']/30*100:.1f}%)")
print(f"  Change: {alj['incorrect_count'] - blj['incorrect_count']:+d}")
print()

print(f"Average Score:")
print(f"  Before: {blj['average_score']:.3f}")
print(f"  After:  {alj['average_score']:.3f}")
print(f"  Change: {alj['average_score'] - blj['average_score']:+.3f}")
print()

print("=" * 80)
