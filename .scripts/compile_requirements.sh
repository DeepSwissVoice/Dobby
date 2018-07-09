#!/usr/bin/env bash

OUTPUT=$(python.exe -m pipenv lock -r 2>/dev/null)
while read -r line; do
    if [[ "$line" =~ .+==.+(;.+(=|<|>|!)=?.+)? ]]; then
        echo "$line"
    fi
done <<< "$OUTPUT"