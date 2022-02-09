import os
import json
import logging

HOME_DIR = '/opt/home/outbreak'

ANNOTATION_PATHS = {
    'topics_file':      os.path.join(HOME_DIR, 'topic_classifier',          'results', 'topicCats.json'),
    'altmetrics_file':  os.path.join(HOME_DIR, 'covid_altmetrics',          'results', 'altmetric_annotations.json'),
    'litcovid_updates': os.path.join(HOME_DIR, 'outbreak_preprint_matcher', 'results', 'update dumps', 'litcovid_update_file.json'),
    'preprint_updates': os.path.join(HOME_DIR, 'outbreak_preprint_matcher', 'results', 'update dumps', 'preprint_update_file.json'),
    'loe_annotations':  os.path.join(HOME_DIR, 'covid19_LST_annotations',   'results', 'loe_annotations.json')
}

class Annotation:
    def __init__(self, source_file):
        logging.warning(f'adding {self.__class__}')
        with open(source_file,'r') as infile:
            self.annotations = json.load(infile)

    def relevant_annotation_dict(self, documents):
        doc_ids = set([i['_id'] for i in documents])
        logging.warning(f'{len(doc_ids)} relevant ids')
        return {i['_id']: i for i in self.annotations if i['_id'] in doc_ids}

class Correction(Annotation):
    def update(self, documents):
        annotations = self.relevant_annotation_dict(documents)

        for document in documents:
            correction = annotations.get(document['_id'])
            if correction and correction.get('correction')
                correction = correction.get('correction')
            else:
                continue

            if document.get('correction'):
                # not sure this branch is used at all
                if isinstance(document['correction'], list):
                    document['correction'].append(correction)
            else:
                # document does not yet have a correction
                document['correction'] = [correction]
                #print(f'{document["_id"]} correction {document["correction"]}')

class Topic(Annotation):
    def update(self, documents):
        annotations = self.relevant_annotation_dict(documents)

        for document in documents:
            topic = annotations.get(document['_id'])
            if not topic:
                continue

            topicslist = topic['topicCategory'].replace("'","").strip("[").strip("]").split(",")
            document['topicCategory'] = [x.strip(" ") for x in topicslist]
            #print(f"{document['_id']} topic {document['topicCategory']}")

class Metric(Annotation):
    def update(self, documents):
        annotations = self.relevant_annotation_dict(documents)

        for document in documents:
            alt_metric = annotations.get(document['_id'])
            if not alt_metric:
                continue

            if document.get('evaluations'):
                try:
                    document['evaluations'].append(alt_metric['evaluations'][0])
                except:
                    eval_object = document['evaluations']
                    document['evaluations']=[eval_object,alt_metric['evaluations'][0]]
            else:
                document['evaluations'] = alt_metric['evaluations']       
                #print(f'{document["_id"]} evaluation {document["evaluations"]}')
                
class Addendum:
    def biorxiv_corrector():
        return Correction(ANNOTATION_PATHS['preprint_updates'])

    def topic_adder():
        return Topic(ANNOTATION_PATHS['topics_file'])

    def altmetric_adder():
        return Metric(ANNOTATION_PATHS['altmetrics_file'])
