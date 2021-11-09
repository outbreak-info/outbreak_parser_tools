import biothings
import requests

def create_uploader(upload_config, parser_func):
    uploader_name = f"{upload_config['name'].capitalize()}Uploader"
    
    def get_mapping(klass):
        r = requests.get(upload_config['map'])
        if (r.status_code == 200):
            mapping = r.json()
            mapping_dict = {key: mapping[key] for key in MAP_VARS}
            return mapping_dict

    return type(uploader_name, (biothings.hub.dataload.uploader.BaseSourceUploader,), {
        'main_source':   upload_config['name'],
        'name':          upload_config['name'],
        '__metadata__':  upload_config['metadata'],
        'idconverter':   None,
        'storage_class': biothings.hub.dataload.storage.BasicStorage,
        'get_mapping':   classmethod(get_mapping)
        'load_data':     lambda x, y: parser_func(),
    })
