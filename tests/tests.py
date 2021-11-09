import unittest

from unittest.mock import patch

from collections   import defaultdict

import addendum

def mock_addendums():
    addendums = defaultdict(dict)
    adds_fixture = [{"_id": "pmid32525881", "correction": [{"@type": "Correction", "identifier": "2020.03.31.20048876", "correctionType": 'NaN', "url": "https://doi.org/10.1101/2020.03.31.20048876"}]}, {"_id": "pmid32485157", "correction": [{"@type": "Correction", "identifier": "2020.05.22.20106328", "correctionType": 'NaN', "url": "https://doi.org/10.1101/2020.05.22.20106328"}]}, {"_id":"199059","topicCategory":"['Mechanism', 'Treatment']"},{"_id":"2020.01.19.911669","topicCategory":"['Transmission', 'Prevention', 'Forecasting']"},{"_id":"2020.01.20.913368","topicCategory":"['Mechanism', 'Transmission', 'Treatment']"},{"_id":"2020.01.21.914044","topicCategory":"['Mechanism', 'Transmission']"},{"_id":"2020.01.21.914929","topicCategory":"['Mechanism', 'Treatment']"}]
    for addendum in adds_fixture:
        addendums[addendum['_id']].update(addendum)
    return dict(addendums)

class TestAddendums(unittest.TestCase):
    @patch('addendum.get_addendums')
    def test_addendums(self, get_adds):
        get_adds.return_value = mock_addendums()
        @addendum.add_addendum
        def load_annotations():
            yield {"@context": {"outbreak": "https://discovery.biothings.io/view/outbreak/", "schema": "http://schema.org/"}, "@type": "Publication", "_id": "pmid32525881", "_score": 1.0, "abstract": "The Japanese government instituted countermeasures against COVID-19"}
            yield {"@context": {"outbreak": "https://discovery.biothings.io/view/outbreak/", "schema": "http://schema.org/"}, "@type": "Publication", "_id": "2020.01.20.913368", "_score": 1.0, "abstract": "Detailed genomic and structure-based analysis of a new coronavirus"}

        results = [i for i in load_annotations()]
        assert results[0]['correction'][0]['identifier'] == "2020.03.31.20048876"
        assert results[1]['topicCategory'] == "['Mechanism', 'Transmission', 'Treatment']"
