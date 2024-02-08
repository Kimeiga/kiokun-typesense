#!/bin/bash

# Set Typesense API Key and Host
TYPESENSE_API_KEY="GSV3UjDj0By3HYzmgWSiCsprcn7khNRY3EVyVfHcOXOMaV3y"
TYPESENSE_HOST="http://localhost:8108"

# # Define Collection Schema
# SCHEMA='{
#   "name": "dictionary",
#   "enable_nested_fields": true,
#   "fields": [
#     { "name": "w_s", "type": "string", "infix": true, "optional": true },
#     { "name": "w_t", "type": "string", "infix": true, "optional": true },
#     { "name": "w_p", "type": "string[]", "infix": true, "optional": true },
#     { "name": "w_d", "type": "string[]", "infix": true, "optional": true },
#     { "name": "c_t", "type": "string", "infix": true, "optional": true },
#     { "name": "c_s", "type": "string[]", "infix": true, "optional": true },
#     { "name": "c_g", "type": "string[]", "infix": true, "optional": true },
#     { "name": "c_p", "type": "string[]", "infix": true, "optional": true },
#     { "name": "c_v", "type": "string[]", "infix": true, "optional": true },
#     { "name": "j", "type": "object[]", "infix": true, "optional": true },
#     { "name": "n", "type": "object[]", "infix": true, "optional": true },
#     { "name": "k", "type": "object[]", "infix": true, "optional": true }
#   ]
# }'
# Define Collection Schema
SCHEMA='{
  "name": "dictionary",
  "enable_nested_fields": true,
  "fields": [
    { "name": "w_s", "type": "string", "infix": true, "optional": true },
    { "name": "w_t", "type": "string", "infix": true, "optional": true },
    { "name": "w_p", "type": "string[]", "infix": true, "optional": true },
    { "name": "w_d", "type": "string[]", "infix": true, "optional": true },
    { "name": "c_t", "type": "string", "infix": true, "optional": true },
    { "name": "c_s", "type": "string[]", "infix": true, "optional": true },
    { "name": "c_g", "type": "string", "infix": true, "optional": true },
    { "name": "c_p", "type": "string", "infix": true, "optional": true },
    { "name": "c_v", "type": "string", "infix": true, "optional": true },
    { "name": "j", "type": "object[]", "infix": true, "optional": true },
    { "name": "n", "type": "object[]", "infix": true, "optional": true },
    { "name": "k", "type": "object", "infix": true, "optional": true },
    { "name": "v", "type": "object[]", "infix": true, "optional": true }
  ]
}'

# Delete existing collection (if needed)
curl -X DELETE \
     -H "X-TYPESENSE-API-KEY: $TYPESENSE_API_KEY" \
     "$TYPESENSE_HOST/collections/dictionary"

# Create a new collection
echo "Creating a new collection..."
curl -X POST \
     -H "Content-Type: application/json" \
     -H "X-TYPESENSE-API-KEY: $TYPESENSE_API_KEY" \
     -d "$SCHEMA" \
     "$TYPESENSE_HOST/collections"

# Import documents into the collection
echo "Importing documents..."
curl -X POST \
     -H "X-TYPESENSE-API-KEY: $TYPESENSE_API_KEY" \
     --data-binary @all_data.jsonl \
     "$TYPESENSE_HOST/collections/dictionary/documents/import"

echo "Import complete."
