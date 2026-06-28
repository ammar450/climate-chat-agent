"""Quick evaluation of all 16 test cases."""
import sys, json
sys.path.insert(0, '.')
from src.agent.graph_agent import run_agent

with open('evaluation/test_questions.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

passed = 0
failed = 0
nodata = 0
errors = 0

for tc in data['test_cases']:
    qid = tc['id']
    expected = tc['expected_template']
    q = tc['question'][0]
    
    print(f"\n[{qid}] [{tc['category']}] {q[:80]}")
    print(f"    Expected: {expected}")
    
    try:
        r = run_agent(f'ev-{qid}', q, model='openai:gpt-4o-mini')
        tmpl = r.get('used_template', '?')
        ans = r.get('answer', '')
        rows = r.get('results', [])
        
        no_data = any(p in ans.lower() for p in [
            'no data found', 'no data available',
            "i don't have enough", "i'm sorry"
        ])
        
        match = 'MATCH' if tmpl == expected else 'WRONG'
        status = 'NO_DATA' if no_data else 'OK'
        
        if tmpl == expected and not no_data:
            passed += 1
            print(f"    {match} | {status} | rows={len(rows)}")
        elif no_data:
            nodata += 1
            print(f"    [FAIL-NODATA] tmpl={tmpl}")
            print(f"    Answer: {ans[:150]}")
        else:
            failed += 1
            print(f"    [FAIL-WRONG-TMPL] got={tmpl} exp={expected}")
            print(f"    Answer: {ans[:150]}")
    except Exception as e:
        errors += 1
        print(f"    [ERROR] {str(e)[:150]}")

print("\n" + "=" * 60)
print(f"Results: {passed} passed, {failed} wrong-template, {nodata} no-data, {errors} errors")
print("=" * 60)
