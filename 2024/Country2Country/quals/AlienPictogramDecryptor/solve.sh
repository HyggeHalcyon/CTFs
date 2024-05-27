#!/bin/bash

# Initialize an empty string to hold all comments
all_comments=""

# Loop through each file from 1.jpg to 38.jpg
for i in {1..37}
do
  # Extract the comment using exiftool
  comment=$(exiftool -Comment "$i.jpg" | awk -F': ' '{print $2}')
  
  # Append the comment to the all_comments string
  all_comments+="$comment"
done

# Print all concatenated comments
echo "$all_comments"
