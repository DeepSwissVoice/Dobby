#!/usr/bin/env bash
set -e

echo "# This file was generated by pipenv based on the Pipfile. DO NOT EDIT MANUALLY!"
OUTPUT=$(python.exe -m pipenv lock -r 2>&1)
while read -r line; do
    if [[ "$line" =~ .+==.+(;.+(=|<|>|!)=?.+)? ]]; then
        echo "$line"
    fi
done <<< "$OUTPUT"