# %%
import sys
sys.path.append("D:\\OneDrive - HKUST\\LongCOVIDCode\\scripts")

from mongo.get_database import get_database
from igraph import * 
import pickle
import re
from info.keywords import labels as keyword_labels
from concurrent.futures import ThreadPoolExecutor

# %%
db = get_database()
network_collection = db.get_collection('networks')

# %%
select_network_picle_selector = {
    "_id": {
        "$regex":"_28x22$"
    },
    "matrix": {
        "$type": "binData"
    }
}

mongo_find_network_adjacency_matrices = network_collection.find(
    filter=select_network_picle_selector,
    sort=[("date", 1)]
)
network_adjacency_matrices = [(result.get('date'), result.get('matrix')) for result in mongo_find_network_adjacency_matrices]

# %%
def export_edge_list_per_adjacency(result):
    (resultDate, graphPickle) = result
    formatted_date = resultDate.strftime("%Y-%m-%d")
    matrix = pickle.loads(graphPickle)
    graph = Graph.Adjacency(matrix.values)

    with open(f"./data/intermediate/edgelist/{formatted_date}.csv", 'w') as f:
        f.writelines(
            ["source,target,timestamp\n"] + [
                f"{in_node},{out_node},{formatted_date}\n" 
                for (in_node, out_node) in [e.tuple for e in graph.es]
            ]
        )

(_, matrix) = network_adjacency_matrices[0] 
matrix = pickle.loads(matrix)
labels = list(matrix.columns)

with open("./data/intermediate/vertices.csv", 'w') as f:
    vertices = [ (index, keyword_labels[label].replace("\n", "")) for index, label in enumerate(labels) ]
    f.writelines(['id,label\n'] + [ f"{index},{label}\n" for (index, label) in vertices ])

with ThreadPoolExecutor(max_workers=5, thread_name_prefix="NetworkLocalCluster") as executor:
    executor.map(export_edge_list_per_adjacency, network_adjacency_matrices)

# %%
