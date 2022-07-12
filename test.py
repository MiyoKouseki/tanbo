from elasticsearch import Elasticsearch
 
# Elasticsearch接続
es = Elasticsearch("https://tanbo.kb.us-central1.gcp.cloud.es.io:9243")

print(dir(es.get))
es.get()

# # データ登録
# es.index(index="test",
#          doc_type='_doc',
#          id=1,
#          body={"key": "100", "value": "elasticsearchのテスト"})
 
# # データ取得
# res = es.get(index="test",
#              doc_type='_doc',
#              id=1)['_source']
 
# print(res)
 
# 接続を閉じる
es.close()
