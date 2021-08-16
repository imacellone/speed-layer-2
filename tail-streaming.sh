#!/bin/bash

output="streaming/output/output.data"

while [ ! -f $output ]
do
    echo "streaming has not started yet. sleeping."
    sleep 10
done

tail -f $output
