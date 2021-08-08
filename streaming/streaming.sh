#!/bin/sh

echo "Preparing."

input="/data/input/adult.data"
output="/data/output/output.data"

sleep_time_milliseconds=0.004

echo "Cleaning environment."

# If the output file exists, delete it.
if test -f "$output"; then
    rm -rf $output
fi

echo "Processing."

# Writes one line of the input file to the output file, every sleep_time_seconds seconds.
while IFS= read -r line
do
    echo "$line" >> $output
    sleep $sleep_time_milliseconds
done < "$input"

echo "Success."