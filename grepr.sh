#!/bin/bash
directory=$1
shift

# Check if the directory exists
if [ ! -d "$directory" ]; then
    echo "Error: Directory '$directory' does not exist."
    exit 1
fi

# Loop through each dictionary file
for dictionary_file in "$@"; do
    while IFS= read -r word; do
        grep_output=$(grep -r --color=always -w "$word" "$directory" 2>/dev/null | grep -v "Binary file")
        echo "$grep_output"
    done < "$dictionary_file"
done