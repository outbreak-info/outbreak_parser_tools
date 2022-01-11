import os
import json

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
        with open(source_file,'r') as infile:
            self.annotations = json.load(infile)

    def relevant_annotations(self, documents):
        d_ids = set([i['_id'] for i in documents])
        return [i for i in self.annotations if i['_id'] in d_ids]

    def get_annotation(self, document, annotations):
        return [a for a in annotations if a['_id']==document['_id']]

class Correction(Annotation):
    ## preprint matcher correction
    def update(self, documents):
        annotations = self.relevant_annotations(documents)

        for document in documents:
            correction = self.get_annotation(document, annotations)
            if not correction:
                continue

            if document.get('correction'):
                # not sure this branch is used at all
                if isinstance(document['correction'], list):
                    document['correction'].append(correction['correction'][0])
            else:
                # document does not yet have a correction
                document['correction'] = correction
                #print(f'{document["_id"]} correction {document["correction"]}')

class Topic(Annotation):
    def update(self, documents):
        annotations = self.relevant_annotations(documents)

        for document in documents:
            topic = self.get_annotation(document, annotations)
            if not topic:
                continue

            topicslist = topic[0]['topicCategory'].replace("'","").strip("[").strip("]").split(",")
            document['topicCategory'] = [x.strip(" ") for x in topicslist]
            #print(f"{document['_id']} topic {document['topicCategory']}")

class Metric(Annotation):
    def update(self, documents):
        annotations = self.relevant_annotations(documents)

        for document in documents:
            alt_info = self.get_annotation(document, annotations)
            if not alt_info:
                continue
            alt_metric = alt_info[0]

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
    def biorxiv_corrector(self):
        return Correction(ANNOTATION_PATHS['preprint_updates'])

    def topic_adder(self):
        return Topic(ANNOTATION_PATHS['topics_file'])

    def altmetric_adder(self):
        return Metric(ANNOTATION_PATHS['altmetrics_file'])
