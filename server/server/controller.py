import json
import time
from aiohttp import web
from main_algorithm.data_model import DataModel
from .utility import load_model_pickle
from main_algorithm.vector_space_model import VectorSpaceModel
import pandas as pd
from typing import Dict, List, Set


def json_inject_execution_time(func):
    def inner_wrapper(*args, **kwargs):
        start_time = time.time()
        result: web.Response = func(*args, **kwargs)
        execution_time = time.time() - start_time
        payload: Dict = json.loads(result.text)
        payload['execution_time'] = execution_time
        result.text = json.dumps(payload)

        return result

    return inner_wrapper


@json_inject_execution_time
def index(request: web.Request):
    return web.json_response({"message": "Hello World This is Havid"})

@json_inject_execution_time
def search(request: web.Request):
    vsm, cluster = load_model_pickle()
    try:
        query: str = request.query.get('q', '').strip()
        current_page: int = int(request.query.get('page', 1))
        page_size_limit: int = int(request.query.get('limit', 10))
        query_clust: int = int(request.query.get('cluster',''))
        evaluator_result = vsm.indexing(query, cluster)
        result_docs = []
        if query_clust:
            for idy in range(len(vsm.get_result_documents()[0])):
                if vsm.get_result_documents()[2][idy]==query_clust:
                    result_docs.append(vsm.get_result_documents()[0][idy].asdict(output_keys=['slug','nomor_ayat', 'nomor_surat', 'tafsir','cosine', 'cluster'],
                                        cosine=vsm.get_result_documents()[1][idy],cluster=vsm.get_result_documents()[2][idy]))
        else:
            for idy in range(len(vsm.get_result_documents()[0])):
                result_docs.append(vsm.get_result_documents()[0][idy].asdict(output_keys=['slug','nomor_ayat', 'nomor_surat', 'tafsir','cosine', 'cluster'],
                                            cosine=vsm.get_result_documents()[1][idy],cluster=vsm.get_result_documents()[2][idy]))
        
        total_result: int = len(result_docs)
        offset: int = (current_page - 1) * page_size_limit
        result_docs = result_docs[offset:current_page * page_size_limit]

        return web.json_response({
            "message": "Success!",
            "meta": {
                "page": current_page,
                "size": len(result_docs),
                "limit": page_size_limit,
                "total": total_result
            },
            "data": result_docs
        })
    except:
        return web.json_response({"message": "Invalid Query!"}, status=422)
