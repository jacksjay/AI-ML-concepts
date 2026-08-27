import json
import os

# Read a file
file_path = 'sample.txt'

# Check if file exists first to avoid crashing
if os.path.exists(file_path):
    with open(file_path, 'r') as file:
        text = file.read()
    
    # Process data (Convert to lowercase and split into a list of words)
    words = text.lower().split()
    
    # Count frequencies using a Dictionary
    word_counts = {}
    for word in words:
        if word in word_counts:
            word_counts[word] += 1
        else:
            word_counts[word] = 1
            
    print("Word counting complete!")
    
    # Save to JSON
    with open('results.json', 'w') as json_file:
        # indent=4 makes the JSON file readable (pretty print)
        json.dump(word_counts, json_file, indent=4)
        print("Results saved to results.json")
else:
    print(f"Error: Could not find {file_path}")