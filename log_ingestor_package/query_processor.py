import spacy
from spacy.matcher import Matcher

nlp = spacy.load("en_core_web_sm")
matcher = Matcher(nlp.vocab)

# Define patterns for matching entities in the query
level_pattern = [
    {"LOWER": "level"},
    {"LOWER": "set"},
    {"LOWER": "to"},
    {"TEXT": {"REGEX": r"\"[^\"]+\""}},
]
matcher.add("LEVEL_PATTERN", [level_pattern])

message_pattern = [
    {"LOWER": "message"},
    {"LOWER": "containing"},
    {"LOWER": "the"},
    {"LOWER": "term"},
    {"TEXT": {"REGEX": r"\"[^\"]+\""}},
]
matcher.add("MESSAGE_PATTERN", [message_pattern])

resource_id_pattern = [
    {"LOWER": {"IN": ["related", "resource", "resourceid"]}},
    {"IS_PUNCT": True, "OP": "?"},
    {"LOWER": "to"},
    {"TEXT": {"REGEX": r"\"[^\"]+\""}},
]
matcher.add("RESOURCE_ID_PATTERN", [resource_id_pattern])


def parse_query(query):
    doc = nlp(query)
    matches = matcher(doc)
    parsed_params = {}
    for match_id, start, end in matches:
        string_id = nlp.vocab.strings[match_id]
        span = doc[start:end]

        if string_id == "LEVEL_PATTERN":
            parsed_params["level"] = span[-1].text.strip('"')
        elif string_id == "MESSAGE_PATTERN":
            parsed_params["message"] = span[-1].text.strip('"')
        elif string_id == "RESOURCE_ID_PATTERN":
            parsed_params["resourceId"] = span[-1].text.strip('"')

    return parsed_params


def construct_es_query(params):
    query = {"bool": {"must": [], "filter": []}}

    if "level" in params:
        query["bool"]["filter"].append({"term": {"level": params["level"]}})
    if "message" in params:
        query["bool"]["must"].append({"match": {"message": params["message"]}})
    if "resourceId" in params:
        query["bool"]["filter"].append({"term": {"resourceId": params["resourceId"]}})
    # Add more conditions based on parsed parameters
    # ...

    return query
