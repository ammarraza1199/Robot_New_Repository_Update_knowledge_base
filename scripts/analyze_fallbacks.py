import pandas as pd

df = pd.read_csv('tests/output/acoustic_test_results_20260222_012645_annotated.csv')
fallback_queries = df[df['id'].str.contains('fallback', case=False, na=False)]

print('\n--- FALLBACK QUERIES REASON COUNTS ---')
print(fallback_queries['evaluation_reason'].value_counts())

print('\n--- ALL FALLBACK QUERIES THAT FAILED ---')
failed_fallbacks = fallback_queries[~fallback_queries['evaluation_reason'].str.contains('Correct')]
for _, row in failed_fallbacks.iterrows():
    print(f"ID: {row['id']} | Lang: {row['heard_lang']}")
    print(f"Text: {str(row['heard_text']).encode('ascii', errors='replace').decode('ascii')}")
    print(f"Response: {str(row['robot_response']).encode('ascii', errors='replace').decode('ascii')}")
    print(f"Reason: {row['evaluation_reason']}")
    print('-'*50)
