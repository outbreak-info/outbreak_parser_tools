import functools
import json

from collections import defaultdict

CATS_FILE     = '/opt/home/outbreak/topic_classifier/results/topicCats.json'
PREPRINT_FILE = '/opt/home/outbreak/outbreak_preprint_matcher/results/update dumps/update_file.json'

def add_addendum(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        addendums = get_addendums()
        for document in func(*args, **kwargs):
            document_with_addendums = addendums.get(document['_id'])

            if document_with_addendums:
                # prefers existing values for keys without overwriting anything
                document_with_addendums.update(document)
                yield document_with_addendums
            else:
                yield document

    return wrapper

def get_topic_categories(topic_categories_file, addendums):
    with open(topic_categories_file, 'r') as categories_file:
        categories_list = json.load(categories_file)

    for category in categories_list:
        addendums[category['_id']]['topicCategory'] = category['topicCategory']
    return categories

def get_preprint(preprint_file, addendums):
    with open(preprint_file, 'r') as preprint_file:
        preprint_list = json.load(preprint_file)

    for preprint in preprint_list:
        addendums[preprint['_id']]['correction'] = preprint['correction']
    return categories

def get_addendums():
    addendums = defaultdict(dict)
    get_topic_categories(CATS_FILE, addendums)
    get_preprint_match(PREPRINTS_FILE, addendums)

    return dict(addendums)
