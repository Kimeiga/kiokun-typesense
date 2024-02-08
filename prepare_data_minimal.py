# The idea here is that we are going to create the jsonl data that typesense will scan over
# But instead of trying to combine the data sources at all, we will just minify each entry from each one and
# add them to the same jsonl object

# When we make the entry page where we have just an entry with /word, then we will try to combine the data then
# Also we will have to have a key for each entry so that when you click on one of these you know which page you
# will go to.

# This means that in order for the interop to work, on every chinese object, we have to have a japanese character
# and on every japanese object we have to have a chinese character. That will make it a bit strange when they get
# matched though...
