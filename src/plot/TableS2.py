from commonvar import *
import os

##########################for release#########################
network_lst = ['BioGRID','STRING-EXP','GIANT-TN','STRING']
gsc_lst = ['GOBPtmp','GOBP','DisGeNet','BeFree','GWAS','MGI']
print("WARNING: results generated will be different from that's shown in paper, due to exclusino of InBioMap and KEGGBP")
#############################################################

def get_gsc_info_dict():
	gsc_info_dict = {}
	for network in network_lst:
		gsc_info_dict[network] = {}
		for gsc in gsc_lst:
			gsc_info_dict[network][gsc] = {}
			for gs_fn in os.popen('ls ' + gsc_dir + gsc + '/' + network).read().split():
				gs_fp = gsc_dir + gsc + '/' + network + '/' + gs_fn
				gs = core.label.LabelSet(gs_fp)
				gsc_info_dict[network][gsc][gs_fn] = set(gs.pos_IDlst)
	return gsc_info_dict

def get_combined_gsc_info_dict(gsc_info_dict):
	combined_gsc_info_dict = {}
	for gsc in gsc_lst:
		combined_gsc_info_dict[gsc] = {}
		for network in network_lst:
			for gs, IDlst in gsc_info_dict[network][gsc].items():
				if gs not in combined_gsc_info_dict[gsc]:
					combined_gsc_info_dict[gsc][gs] = set(IDlst)
				else:
					combined_gsc_info_dict[gsc][gs].update(IDlst)
	return combined_gsc_info_dict

def get_table(gsc_info):
	num_gene_lst = []
	num_gs_lst = []
	gs_size_range_lst = []
	med_gs_size_lst = []
	for gsc in gsc_lst:
		network_gs_lst = [i for i in gsc_info[gsc].values()]
		gs_size_lst = [len(i) for i in network_gs_lst]

		num_gene_lst.append(len(set.union(*network_gs_lst)))
		num_gs_lst.append(len(network_gs_lst))
		gs_size_range_lst.append((np.min(gs_size_lst), np.max(gs_size_lst)))
		med_gs_size_lst.append(np.median(gs_size_lst))

	table = pd.DataFrame()
	table['Geneset Collection'] = gsc_lst
	table['Number of Genes'] = num_gene_lst
	table['Number of Genesets'] = num_gs_lst
	table['Range of Geneset sizes'] = gs_size_range_lst
	table['Median Geneset size'] = med_gs_size_lst
	return table

def get_table_combined(combined_gsc_info_dict, gsc_info_dict):
	num_gene_lst = []
	num_gs_lst = []
	gs_size_range_lst = []
	med_gs_size_lst = []
	for gsc in gsc_lst:
		gs_lst = [i for i in combined_gsc_info_dict[gsc].values()]
		num_gene_lst.append(len(set.union(*gs_lst)))
		num_gs_lst.append(len(gs_lst))

		gs_size_lst = []
		for network in network_lst:
			network_gs_lst = [i for i in gsc_info_dict[network][gsc].values()]
			gs_size_lst.extend([len(i) for i in network_gs_lst])

		gs_size_range_lst.append((np.min(gs_size_lst), np.max(gs_size_lst)))
		med_gs_size_lst.append(np.median(gs_size_lst))

	table = pd.DataFrame()
	table['Geneset Collection'] = gsc_lst
	table['Number of Genes'] = num_gene_lst
	table['Number of Genesets'] = num_gs_lst
	table['Range of Geneset sizes'] = gs_size_range_lst
	table['Median Geneset size'] = med_gs_size_lst
	return table

def export_table():
	gsc_info_dict = get_gsc_info_dict()
	combined_gsc_info_dict = get_combined_gsc_info_dict(gsc_info_dict)
	table_dict = {}
	for network in network_lst:
		table_dict[network] = get_table(gsc_info_dict[network])
		table_dict[network].to_csv(fig_dir + 'TableS2-' + network + '.tsv', index=False, sep='\t')
	table_combined = get_table_combined(combined_gsc_info_dict, gsc_info_dict)
	table_combined.to_csv(fig_dir + 'TableS2.tsv', index=False, sep='\t')

if __name__ == '__main__':
	export_table()
