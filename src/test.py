import numpy as np
import os
from core import *

network = 'BioGRID'
gsc = 'GOBPtmp'
pth = '../data/labels'
valsplit = 'Holdout'

print('Network:\t%s'%network)
print('Geneset Collection:\t%s'%gsc)
print('Validation:\t%s'%valsplit)

def get_scores(y_true, y_predict):
	return metrics.auPRC(y_true, y_predict), \
			metrics.PTopK(y_true, y_predict), \
			metrics.auROC(y_true, y_predict)

g = graph.WUGraph.from_edgelist('../data/networks/' + network + '.edg')
#g = graph.Embedding.from_emd('../data/embeddings/' + network + '.emd')
mdl = models.SL(g)

print('auPRC\tP@TopK\tauROC\t# Pos\tGeneset')
pth_to_gsc = '/'.join([pth, gsc, network])
for i in os.popen('ls ' + pth_to_gsc).read().split():
	lbset = label.LabelSet('/'.join([pth_to_gsc, i]))
	y_true, y_predict = mdl.test(lbset, mode=valsplit)
	scores = get_scores(y_true, y_predict)
	print('%.2f\t%.2f\t%.2f\t%d\t%s'%(*scores, lbset.label_ary.sum(), i))
