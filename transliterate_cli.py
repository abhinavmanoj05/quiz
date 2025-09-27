from datasets import load_dataset
import argparse
from typing import Dict, List

def load_data():
    """Load the transliteration dataset"""
    print("Loading Bhasha-Abhijnaanam dataset...")
    dataset = load_dataset("ai4bharat/Bhasha-Abhijnaanam", split="train")
    print(f"Loaded {len(dataset)} examples")
    return dataset

def explore_dataset(dataset, limit=10):
    """Explore the dataset structure"""
    print(f"\nExploring first {limit} examples:")
    print("=" * 50)
    
    for i, example in enumerate(dataset.select(range(min(limit, len(dataset))))):
        print(f"\nExample {i+1}:")
        for key, value in example.items():
            print(f"  {key}: {value}")

def search_dataset(dataset, query: str, limit=5):
    """Search for text in the dataset"""
    print(f"\nSearching for '{query}'...")
    matches = []
    
    for i, example in enumerate(dataset):
        if query.lower() in str(example).lower():
            matches.append((i, example))
            if len(matches) >= limit:
                break
    
    if matches:
        print(f"Found {len(matches)} matches:")
        for idx, match in matches:
            print(f"\nMatch {idx+1}:")
            for key, value in match.items():
                print(f"  {key}: {value}")
    else:
        print("No matches found.")

def main():
    parser = argparse.ArgumentParser(description="Indian Language Transliteration Tool")
    parser.add_argument("--explore", action="store_true", help="Explore dataset structure")
    parser.add_argument("--search", type=str, help="Search for text in dataset")
    parser.add_argument("--limit", type=int, default=10, help="Limit number of results")
    
    args = parser.parse_args()
    
    # Load dataset
    dataset = load_data()
    
    if args.explore:
        explore_dataset(dataset, args.limit)
    elif args.search:
        search_dataset(dataset, args.search, args.limit)
    else:
        print("\nUsage:")
        print("  python transliterate_cli.py --explore          # Explore dataset")
        print("  python transliterate_cli.py --search 'text'    # Search dataset")
        print("  python transliterate_cli.py --help             # Show help")

if __name__ == "__main__":
    main()
