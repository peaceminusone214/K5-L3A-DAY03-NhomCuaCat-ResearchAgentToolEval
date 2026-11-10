---
name: dedupe_items
track: core
kind: local_formatter
requires_env: []
inputs: [items, key]
outputs: [items, input_count, removed_count]
side_effect: false
---
# dedupe_items

Removes duplicate research items locally, preserving first-seen order. It does
not search the web and should only be used when the user supplies items or URLs.
