#!/bin/bash

# File Size Report Generator
# Usage: ./file_size_report.sh <directory_path> [output_file]

# Function to display usage
usage() {
    echo "Usage: $0 <directory_path> [output_file]"
    echo "  directory_path: The directory to scan recursively"
    echo "  output_file: Optional output file (default: file_size_report.txt)"
    echo ""
    echo "Example: $0 /home/user my_report.txt"
    exit 1
}

# Function to convert bytes to kilobytes with proper formatting
bytes_to_kb() {
    local bytes=$1
    if [ "$bytes" -eq 0 ]; then
        echo "0kb"
    elif [ "$bytes" -lt 1024 ]; then
        echo ".$(echo "scale=1; $bytes * 10 / 1024" | bc | cut -d. -f1)kb"
    else
        local kb=$(echo "scale=1; $bytes / 1024" | bc)
        # Remove trailing .0 if it's a whole number
        if [[ $kb == *.0 ]]; then
            kb=${kb%.0}
        fi
        echo "${kb}kb"
    fi
}

# Check if directory argument is provided
if [ $# -lt 1 ]; then
    echo "Error: Directory path is required."
    usage
fi

# Get the directory path from command line argument
TARGET_DIR="$1"

# Set output file (default or user-specified)
if [ $# -ge 2 ]; then
    OUTPUT_FILE="$2"
else
    OUTPUT_FILE="file_size_report.txt"
fi

# Check if the directory exists
if [ ! -d "$TARGET_DIR" ]; then
    echo "Error: Directory '$TARGET_DIR' does not exist."
    exit 1
fi

# Check if bc is available (needed for decimal calculations)
if ! command -v bc &> /dev/null; then
    echo "Error: 'bc' calculator is required but not installed."
    echo "Please install bc: sudo apt-get install bc (on Debian/Ubuntu)"
    exit 1
fi

# Get the absolute path and clean it up
TARGET_DIR=$(realpath "$TARGET_DIR")

# Create or clear the output file
> "$OUTPUT_FILE"

# Add header to output file
echo "Contents of $TARGET_DIR:" >> "$OUTPUT_FILE"

# Counter for files processed
file_count=0

# Find all files recursively and process them
while IFS= read -r -d '' file; do
    # Get file size in bytes
    file_size=$(stat -f%z "$file" 2>/dev/null || stat -c%s "$file" 2>/dev/null)
    
    # Skip if we couldn't get the file size
    if [ -z "$file_size" ]; then
        continue
    fi
    
    # Get relative path from target directory
    relative_path="${file#$TARGET_DIR/}"
    
    # Convert bytes to kilobytes
    size_kb=$(bytes_to_kb "$file_size")
    
    # Output to file in the format: filename, size
    echo "$relative_path, $size_kb" >> "$OUTPUT_FILE"
    
    # Increment counter
    ((file_count++))
    
done < <(find "$TARGET_DIR" -type f -print0)

# Add summary at the end
echo "" >> "$OUTPUT_FILE"
echo "Total files processed: $file_count" >> "$OUTPUT_FILE"

echo "File size report generated successfully!"
echo "Output file: $OUTPUT_FILE"
echo "Total files processed: $file_count"
echo "Target directory: $TARGET_DIR"
