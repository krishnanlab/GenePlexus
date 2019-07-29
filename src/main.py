import numpy as np
import argparse
import core
import os
import sys
import time
import fcntl

home_dir = '/'.join(os.path.dirname(os.path.realpath(__file__)).split('/')[:-1])
data_pth = home_dir + '/data/labels'
network_pth = home_dir + '/data/networks'
emd_pth = home_dir + '/data/embeddings'

all_networks = ['BioGRID', 'STRING-EXP', 'InBioMap', 'GIANT-TN', 'STRING']
all_gscs = ['GOBPtmp', 'GOBP', 'KEGGBP', 'DisGeNet', 'BeFree', 'GWAS', 'MGI']
all_valsplits = ['Holdout', '5FCV']
all_methods = ['SL-A', 'SL-I', 'SL-E', 'LP-I', 'LP-A'] # add the name of new models to this list

score_type_dict = {
	'auPRC':core.metrics.auPRC, 
	'P@TopK':core.metrics.PTopK, 
	'auROC':core.metrics.auROC
}

def parse():
	p = argparse.ArgumentParser()
	p.add_argument('-n', '--networks', nargs='+', default=['BioGRID'],
					help='Choose networks, default = BioGRID')
	p.add_argument('-c', '--gscs', nargs='+', default=['GOBPtmp'],
					help='Choose geneset collections, default = GOBPtmp')
	p.add_argument('-s', '--valsplits', nargs='+', default=['Holdout'],
					help='Choose validation split schemes (Can\'t perform 5FCV on GOBPtmp), default = Holdout')
	p.add_argument('-m', '--methods', nargs='+', default=['SL-A', 'SL-I', 'SL-E', 'LP-I', 'LP-A'],
					help='Choose methods to use, default = SL-A SL-I SL-E LP-I LP-A')
	p.add_argument('-o', '--output', type=str, default='None',
					help='Output file path (if \'None\', no output files will be generated), default = None')
	p.add_argument('-a', '--append', action='store_true',
					help='Only append to file, do not overwrite, default = False')
	p.add_argument('-v', '--verbose', action='store_true',
					help='Print time usage, default = False')
	args = p.parse_args()
	return args

def args_check(args):
	for network in args.networks:
		assert network in all_networks, "Network not exists: %s"%repr(network)
	for gsc in args.gscs:
		assert gsc in all_gscs, "Geneset collection not exists: %s"%repr(gsc)
	for valsplit in args.valsplits:
		assert valsplit in all_valsplits, "Validation split not exists: %s"%repr(valsplit)
	for method in args.methods:
		assert method in all_methods, "Method not exists: %s"%repr(method)
	print('Networks: ' + repr(args.networks))
	print('Geneset Collections: ' + repr(args.gscs))
	print('Validation splits: ' + repr(args.valsplits))
	print('Methods: ' + repr(args.methods))
	print('Append: ' + repr(args.append))
	print('Verbose: ' + repr(args.verbose))
	print('Output: ' + args.output)
	print('-'*80)

def timeit(fun, *args, **kwargs):
	start = time.time()
	result = fun(*args, **kwargs)
	end = time.time()
	sec = end - start
	print('Function call %s ran for %d:%d:%d'%(repr(fun), sec//3600, sec%3600//60, sec%3600%60))
	return result

def get_graphs(methods, network):
	graphs = set([i.split('-')[1] for i in methods])
	adjmat = infmat = emdmat = None
	pth_to_network = '/'.join([network_pth, network]) + '.edg'
	pth_to_emd = '/'.join([emd_pth, network]) + '.emd'
	if 'A' in graphs:
		print('Start loading network: %s...'%network)
		adjmat = timeit(core.graph.WUGraph.from_edgelist, pth_to_network)
	if 'I' in graphs:
		if 'A' in graphs:
			print('Random walking on %s...'%network)
			infmat = timeit(core.graph.Influence.from_wugraph, adjmat, beta=0.85)
		else:
			print('Loading and random walking on %s...'%network)
			infmat = timeit(core.graph.Influence.from_edgelist, pth_to_network, beta=0.85)
	if 'E' in graphs:
		print('Loading embedding for %s...'%network)
		emdmat = timeit(core.graph.Embedding.from_emd, pth_to_emd)
	return adjmat, infmat, emdmat

def get_mdl_dict(methods, adjmat, infmat, emdmat):
	mdl_dict = {}
	if 'SL-A' in methods: mdl_dict['SL-A'] = core.models.SL(adjmat)
	if 'SL-I' in methods: mdl_dict['SL-I'] = core.models.SL(infmat)
	if 'SL-E' in methods: mdl_dict['SL-E'] = core.models.SL(emdmat)
	if 'LP-A' in methods: mdl_dict['LP-A'] = core.models.LP(adjmat)
	if 'LP-I' in methods: mdl_dict['LP-I'] = core.models.LP(infmat)
	# Add user model here
	#if 'UserModel' in methods: md_dict['UserModel'] = core.models.UserModel(adjmat)
	return mdl_dict

def run(networks, gscs, valsplits, methods, output='None', append=False, verbose=True):
	if output != 'None':# initialize output file
		if not append:
			with open(output, 'w') as f:
				f.write('Geneset\tScore\tScore Type\tMethod\tValidation Split\tGeneset Collection\tNetwork\n')
		write_flag = True
	else:
		write_flag = False

	for network in networks:
		pth_to_network = '/'.join([network_pth, network]) + '.edg'
		pth_to_emd = '/'.join([emd_pth, network]) + '.emd'

		adjmat, infmat, emdmat = get_graphs(methods, network)
		mdl_dict = get_mdl_dict(methods, adjmat, infmat, emdmat)

		for gsc in gscs:
			pth_to_gsc = '/'.join([data_pth, gsc, network])
			print('Start evaluating %s on geneset collection: %s'%(network, gsc))

			if verbose:
				print('auPRC\tP@TopK\tauROC\tMethod\tValidation\tGeneset')

			for geneset_file_name in os.popen('ls ' + pth_to_gsc).read().split():
				geneset_name = geneset_file_name.split('.')[0]
				geneset = core.label.LabelSet('/'.join([pth_to_gsc, geneset_file_name]))

				for valsplit in valsplits:
					# skip GOBP temporal holdout set for 5FCV
					if (gsc == 'GOBPtmp') & (valsplit == '5FCV'):
						continue

					for mdl_name, mdl in mdl_dict.items():
						y_true, y_predict = mdl.test(geneset, mode=valsplit)

						score_dict = {}
						for score_type, score_fun in score_type_dict.items():
							score = score_fun(y_true, y_predict)
							score_dict[score_type] = score
							if write_flag:
								with open(output, 'a') as f:
									while True:
										try:
											fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
											break
										except IOError:
											continue
									f.write(geneset_name + '\t%.6f\t%s\t%s\t%s\t%s\t%s\n'%\
										(score, score_type, mdl_name, valsplit, gsc, network))
									fcntl.flock(f, fcntl.LOCK_UN)
						if verbose:
							print('%.2f\t%.2f\t%.2f\t%s\t%s\t\t%s'%(score_dict['auPRC'], \
								score_dict['P@TopK'], score_dict['auROC'], mdl_name, valsplit, geneset_name))

if __name__ == '__main__':
	args = parse()
	args_check(args)
	timeit(run, args.networks, args.gscs, args.valsplits, args.methods, \
		output=args.output, append=args.append, verbose=args.verbose)

