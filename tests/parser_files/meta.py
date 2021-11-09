metadata = {
    "src_meta": {
        "author": {
            "name": "Julia Mullen",
            "url":  "https://github.com/juliamullen"
            },
        "code": {
            "branch": "master",
            "repo": "https://github.com/outbreak-info/dataverses"
            },
        "url": "https://dataverse.org/",
        "license": "https://dataverse.org/best-practices/harvard-dataverse-general-terms-use",
    }
}


config = {
        'name': "dataverses"
        'map': "https://raw.githubusercontent.com/SuLab/outbreak.info-resources/master/outbreak_resources_es_mapping.json",
        "vars": ["@type", "author", "curatedBy", "dateModified", "datePublished", "description", "distribution", "doi", "keywords", "@id", "funding", "identifier", "creator", "license", "name", "date"]
        '__metadata__': metadata
}

