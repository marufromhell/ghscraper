#!/bin/bash

# Check if the correct number of arguments is provided
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <directory> <dictionary_file>"
    exit 1
fi

# Assign arguments to variables
directory=$1
dictionary_file=$2

# Check if the directory exists
if [ ! -d "$directory" ]; then
    echo "Error: Directory '$directory' does not exist."
    exit 1
fi

# Check if the dictionary file exists
if [ ! -f "$dictionary_file" ]; then
    echo "Error: Dictionary file '$dictionary_file' does not exist."
    exit 1
fi

# Loop through each word in the dictionary file
while IFS= read -r word; do
    # Use grep to search for the word recursively in the directory
    # Suppress output if no matches are found and filter out binary file matches
    grep_output=$(grep -r --color=always -w "$word" "$directory" 2>/dev/null | grep -v "Binary file")
    if [ -n "$grep_output" ]; then
        echo "Searching for word: $word"
        echo "$grep_output"
    fi
done < "$dictionary_file"