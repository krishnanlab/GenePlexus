from sys import path
path.append("../src")

from core import graph, label, metrics, models

geneset_fp = "../data/labels/GOBPtmp/BioGRID/GLYCOPROTEIN_METABOLIC_PROCESS.tsv"
network_fp = "../data/networks/BioGRID.edg"
score_func = metrics.auPRC

# load the BioGRID adjacency matrix
adjmat = graph.WUGraph.from_edgelist(network_fp)
print(f"Loaded graph from {network_fp}, number of nodes = "
      f"{adjmat.mat.shape[0]:,d}, number of edges = "
      f"{int((adjmat.mat > 0).sum() / 2):,d}")

# load the gene set as labels
geneset = label.LabelSet(geneset_fp)
print(f"Loaded gene set from {geneset_fp}, number of positives = "
      f"{len(geneset.pos_IDlst)}")

# train and evaluat LPA
mdl_LPA = models.LP(adjmat)
y_true, y_pred = mdl_LPA.test(geneset, mode='Holdout')
score = score_func(y_true, y_pred)
print(f"Trained prediction model using LPA, evaluation score = {score:.2f}")

# train and evaluate SLA
mdl_SLA = models.SL(adjmat)
y_true, y_pred = mdl_SLA.test(geneset, mode='Holdout')
score = score_func(y_true, y_pred)
print(f"Trained prediction model using SLA, evaluation score = {score:.2f}")
