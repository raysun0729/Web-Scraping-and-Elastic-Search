from elasticsearch import Elasticsearch
import configparser
import json


def query(q):
    es = Elasticsearch()

    index_name = 'law_search_latest'
    type_ = 'test_type'

    search_params = {
        'query': {
            'query_string': {
                'query': q,
                'default_field': 'summary'

            }
        }
    }
    result = es.search(index=index_name, doc_type=type_, body=search_params)
    if len(result['hits']['hits']) > 10:
        result = result['hits']['hits'][0:10]
    else:
        result = result['hits']['hits'][0:-1]

    for i in range(len(result)):
        # _score
        print('Score: ' + str(result[i]['_score']))
        print('標題: ' + str(result[i]['_source']['title']))
        print('日期: ' + str(result[i]['_source']['date']))
        #print('案由: ' + str(result[i]['_source']['article']))
        print('摘要: ' + str(result[i]['_source']['summary']))
        ###    print('內文: ' + str(result[i]['_source']['artical']))
        print('***************************************************')


if __name__ == '__main__':

    while True:
        q = input('請輸入搜尋...\n')
        if q == 'exit':
            break
        query(q)