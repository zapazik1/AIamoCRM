import json
import statistics
import random
from collections import Counter, defaultdict
import hashlib

# Statistics to track
chunk_count = 0
chunk_lengths = []
char_lengths = []
token_approx = []  # Rough token approximation (chars/4 for English, chars/3 for Russian/mixed)
metadata_keys = set()
metadata_counts = Counter()
key_terms_counts = []
source_counts = Counter()
doc_type_counts = Counter()
entities_counts = Counter()
image_counts = 0
encoding_issues = 0
length_distribution = {
    "very_short (0-50)": 0,
    "short (51-100)": 0,
    "medium (101-200)": 0,
    "target (201-400)": 0,
    "long (401-600)": 0,
    "very_long (601+)": 0
}

token_distribution = {
    "small (<250)": 0,
    "good (250-750)": 0,
    "large (751-1000)": 0,
    "xl (1001-1500)": 0,
    "xxl (>1500)": 0
}

# Duplication check
content_hashes = defaultdict(int)
exact_duplicates = 0
content_samples = []
large_samples = []
all_chunks = []

# Process each chunk
with open('database/chunks/chunks_balanced.jsonl', 'r', encoding='utf-8') as f:
    for line in f:
        try:
            chunk = json.loads(line)
            chunk_count += 1
            all_chunks.append(chunk)
            
            # Text analysis
            text = chunk['text']
            word_count = len(text.split())
            chunk_lengths.append(word_count)  # Word count
            char_count = len(text)
            char_lengths.append(char_count)  # Character count
            
            # Rough token approximation - Russian text typically has 3-4 chars per token
            # Mixed Russian/English/code would be somewhere between 3.5-4 chars per token
            approx_tokens = char_count / 3.5
            token_approx.append(approx_tokens)
            
            # Token size distribution
            if approx_tokens <= 250:
                token_distribution["small (<250)"] += 1
            elif approx_tokens <= 750:
                token_distribution["good (250-750)"] += 1
            elif approx_tokens <= 1000:
                token_distribution["large (751-1000)"] += 1
            elif approx_tokens <= 1500:
                token_distribution["xl (1001-1500)"] += 1
            else:
                token_distribution["xxl (>1500)"] += 1
                # Add to large samples for review
                large_samples.append({
                    "approx_tokens": approx_tokens,
                    "words": word_count,
                    "chars": char_count,
                    "metadata": chunk['metadata'],
                    "text_snippet": text[:200] + "...",
                })
            
            # Check for duplicates using content hash
            content_hash = hashlib.md5(text.encode('utf-8')).hexdigest()
            content_hashes[content_hash] += 1
            if content_hashes[content_hash] > 1:
                exact_duplicates += 1
            
            # Categorize by length (words as approximate for tokens)
            if word_count <= 50:
                length_distribution["very_short (0-50)"] += 1
            elif word_count <= 100:
                length_distribution["short (51-100)"] += 1
            elif word_count <= 200:
                length_distribution["medium (101-200)"] += 1
            elif word_count <= 400:
                length_distribution["target (201-400)"] += 1
            elif word_count <= 600:
                length_distribution["long (401-600)"] += 1
            else:
                length_distribution["very_long (601+)"] += 1
            
            # Check for encoding issues - look for replacement character
            if '\ufffd' in text:
                encoding_issues += 1
                
            # Check for images
            if '![' in text:
                image_counts += 1
                
            # Metadata analysis
            metadata = chunk['metadata']
            for key in metadata:
                metadata_keys.add(key)
                metadata_counts[key] += 1
                
            # Source and doc type counts
            if 'source' in metadata:
                source_counts[metadata['source']] += 1
            if 'doc_type' in metadata:
                doc_type_counts[metadata['doc_type']] += 1
                
            # Key terms analysis
            if 'key_terms' in metadata:
                key_terms_counts.append(len(metadata['key_terms']))
                
            # Entities analysis
            if 'entities' in metadata:
                for entity in metadata['entities']:
                    entities_counts[entity] += 1
                    
        except Exception as e:
            print(f"Error processing line: {e}")

# Sample random chunks for review
if all_chunks:
    samples = random.sample(all_chunks, min(5, len(all_chunks)))
    for i, sample in enumerate(samples, 1):
        content_samples.append({
            "sample_id": i,
            "text": sample['text'][:300] + "..." if len(sample['text']) > 300 else sample['text'],
            "approx_tokens": len(sample['text']) / 3.5,
            "word_count": len(sample['text'].split()),
            "char_count": len(sample['text']),
            "metadata": sample['metadata']
        })

# Calculate unique content hashes
unique_hashes = len(content_hashes)

print(f"Total chunks: {chunk_count}")
print(f"Text statistics:")
print(f"  Average words per chunk: {statistics.mean(chunk_lengths):.1f}")
print(f"  Min words: {min(chunk_lengths)}")
print(f"  Max words: {max(chunk_lengths)}")
print(f"  Median words: {statistics.median(chunk_lengths)}")
print(f"  Average characters per chunk: {statistics.mean(char_lengths):.1f}")
print(f"  Estimated average tokens per chunk: {statistics.mean(token_approx):.1f}")
print(f"  Estimated max tokens: {max(token_approx):.1f}")
print(f"  Chunks with encoding issues: {encoding_issues} ({encoding_issues/chunk_count*100:.1f}%)")
print(f"  Chunks with images: {image_counts} ({image_counts/chunk_count*100:.1f}%)")

print(f"\nToken size distribution (estimated):")
for size_range, count in token_distribution.items():
    print(f"  {size_range}: {count} chunks ({count/chunk_count*100:.1f}%)")

print(f"\nDuplication analysis:")
print(f"  Unique content chunks: {unique_hashes}")
print(f"  Duplicate content chunks: {exact_duplicates}")
print(f"  Duplication rate: {exact_duplicates/chunk_count*100:.1f}%")

print(f"\nChunk length distribution (words):")
for length_range, count in length_distribution.items():
    print(f"  {length_range}: {count} chunks ({count/chunk_count*100:.1f}%)")

print(f"\nMetadata keys: {', '.join(sorted(metadata_keys))}")
print(f"Metadata completeness:")
for key in sorted(metadata_keys):
    print(f"  {key}: {metadata_counts[key]} chunks ({metadata_counts[key]/chunk_count*100:.1f}%)")

if key_terms_counts:
    print(f"\nKey terms statistics:")
    print(f"  Average key terms per chunk: {statistics.mean(key_terms_counts):.1f}")
    print(f"  Min key terms: {min(key_terms_counts)}")
    print(f"  Max key terms: {max(key_terms_counts)}")

print(f"\nTop document types:")
for doc_type, count in doc_type_counts.most_common(5):
    print(f"  {doc_type}: {count} chunks ({count/chunk_count*100:.1f}%)")

print(f"\nTop entities:")
for entity, count in entities_counts.most_common(10):
    print(f"  {entity}: {count} chunks ({count/chunk_count*100:.1f}%)")

print("\nSample chunks for quality review:")
for sample in content_samples:
    print(f"\nSample {sample['sample_id']} ({sample['word_count']} words, ~{sample['approx_tokens']:.0f} tokens):")
    print(f"  Metadata: {sample['metadata']}")
    print(f"  Text: {sample['text']}")

print("\nLargest chunks by token count:")
for i, sample in enumerate(sorted(large_samples, key=lambda x: x['approx_tokens'], reverse=True)[:3], 1):
    print(f"\nLarge sample {i} (~{sample['approx_tokens']:.0f} tokens, {sample['words']} words):")
    print(f"  Source: {sample['metadata'].get('source', 'Unknown')}")
    print(f"  Doc type: {sample['metadata'].get('doc_type', 'Unknown')}")
    print(f"  Snippet: {sample['text_snippet']}") 