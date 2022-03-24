from elasticsearch import Elasticsearch, helpers
import json

qa_mapping = {
    "properties": {
        "title": {
            "type": "text"
        },
        "date": {
            "type": "text"
        },
        "article": {
            "type": "text"
        },
        "summary": {
            "type": "text"
        }
    }
}

renames_key = {
    'title': 'title',
    'date': 'date',
    'article': 'article',
    'summary': 'summary'
}

# Load Amazon QA dataset
def read_data():
    with open('judgementcrawler.json', 'r', encoding='utf-8') as f:
        for row in f:
            d = eval(row.strip())
            d = json.dumps(d)
            row = json.loads(d)

            for k, v in renames_key.items():
                for old_name in list(row):
                    if k == old_name:
                        row[v] = row.pop(old_name)
            yield row


def load2_elasticsearch():
    index_name = 'amazon_qa2'
    type = 'one_to_one'
    es = Elasticsearch()

    # Create Index
    if not es.indices.exists(index=index_name):
        es.indices.create(index=index_name)
    print('Index created!')

    # Put mapping into index
    if not es.indices.exists_type(index=index_name, doc_type=type):
        es.indices.put_mapping(
            index=index_name, doc_type=type, body=qa_mapping, include_type_name=True)
    print('Mappings created!')

    # Import data to elasticsearch
    success, _ = helpers.bulk(
        client=es, actions=read_data(), index=index_name, doc_type=type, ignore=400)
    print('success: ', success)

load2_elasticsearch()