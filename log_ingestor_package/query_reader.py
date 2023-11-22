import re

# List of keys to search for
keys = [
    "level",
    "message",
    "resourceId",
    "timestamp",
    "traceId",
    "spanId",
    "commit",
    "metadata.parentResourceId",
]


def get_keys_values(text):
    # Regular expression pattern to find key-value pairs
    # This pattern is more general and looks for any of the keys followed by any text (as minimal as possible),
    # then a quote, the value, and a closing quote.

    pattern = f'({"|".join(keys)})[^"]*"([^"]*)'
    # pattern = f"({'|'.join(keys)})[^']*'([^']*)"

    # Find all matches
    matches = re.findall(pattern, text)

    return matches
