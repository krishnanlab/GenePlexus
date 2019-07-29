import core
import os
import pandas as pd

home_dir = '/'.join(os.path.dirname(os.path.realpath(__file__)).split('/')[:-1])
network_dir = home_dir +'/data/networks/'
gsc_dir = home_dir + '/data/labels/'
prop_dir = home_dir + '/properties_new/'
if not os.path.isdir(prop_dir):
	os.mkdir(prop_dir)

def export_prop_table(g, network, gsc):
	gs_lst = []
	num_genes_lst = []
	edg_dens_lst = []
	seg_lst = []
	for gs_fn in os.popen('ls ' + gsc_dir + gsc + '/' + network).read().split():
		gs_fp = gsc_dir + gsc + '/' + network + '/' + gs_fn
		gs = core.label.LabelSet(gs_fp)
		pos_IDlst = gs.pos_IDlst

		gs_lst.append(gs_fn.split('.tsv')[0])
		num_genes_lst.append(len(pos_IDlst))
		edg_dens_lst.append(core.graph.get_edg_dens(g, pos_IDlst))
		seg_lst.append(core.graph.get_seg(g, pos_IDlst))

	df = pd.DataFrame()
	df['Geneset'] = gs_lst
	df['Number of Genes'] = num_genes_lst
	df['Edge Density'] = edg_dens_lst
	df['Segregation'] = seg_lst

	out_dir = prop_dir + gsc + '/'
	if not os.path.isdir(out_dir):
		os.mkdir(out_dir)
	out_fp = out_dir + network + '.tsv'
	df.to_csv(out_fp, index=False, sep='\t')

for network_fn in os.popen('ls ' + network_dir).read().split():
	network_fp = network_dir + network_fn
	print('-'*80)
	print('Loading ' + network_fp)
	g = core.graph.WUGraph.from_edgelist(network_fp)
	network = network_fn.split('.edg')[0]
	for gsc in os.popen('ls ' + gsc_dir).read().split():
		print('Calculating geneset properties of ' + gsc)
		if not os.path.isdir(prop_dir + gsc):
			os.mkdir(prop_dir + gsc)
		export_prop_table(g, network, gsc)


