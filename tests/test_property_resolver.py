"""Test property resolver with common terms and typos."""
from property_resolver import property_resolver

print("=" * 60)
print("Testing Property Resolver - Common Terms & Typos")
print("=" * 60)

# Prefetch properties first
property_resolver.prefetch_properties()

test_cases = [
    # Correct terms
    ("temperature", "✅ Correct term"),
    ("rainfall", "✅ Common term"),
    ("humidity", "✅ Correct term"),
    
    # Simple synonyms
    ("rain", "✅ Simple synonym"),
    ("temp", "✅ Short form"),
    ("moisture", "✅ Synonym for humidity"),
    
    # Typos
    ("temprature", "⚠️ Common typo"),
    ("rainfalll", "⚠️ Extra letter"),
    ("precipitaion", "⚠️ Missing 't'"),
    ("humidty", "⚠️ Missing 'i'"),
    ("percipitation", "⚠️ Wrong first letter"),
    
    # Natural language
    ("heat", "✅ Natural term"),
    ("cold", "✅ Natural term"),
    ("rainy", "✅ Adjective form"),
    ("sunshine", "✅ Natural term"),
]

print("\nTest Results:")
print("-" * 60)

for query, description in test_cases:
    uri, confidence, candidates = property_resolver.resolve(query)
    
    if uri:
        # Extract property name from URI
        prop_name = uri.split('/')[-1].replace('_', ' ').title()
        status = "✅ RESOLVED"
        result = f"{prop_name}"
    else:
        status = "❌ FAILED"
        result = "Not found"
    
    print(f"{status} | {query:20s} | {description:20s} | {result}")

print("\n" + "=" * 60)
print("Property Resolver Test Complete!")
print("=" * 60)
