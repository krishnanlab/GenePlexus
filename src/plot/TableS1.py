from commonvar import *

def export_table():
	num_node_lst = []
	num_edge_lst = []
	edg_dens_lst = []
	exist_network_lst = []
	for network in network_lst:
		print('Generating data for %s...'%network)
		try:
			g = core.graph.WUGraph.from_edgelist(network_dir + network + '.edg')
			exist_network_lst.append(network)
			num_node_lst.append(g.size)
			num_edge_lst.append((g.mat > 0).sum() / 2)
			edg_dens_lst.append(core.graph.get_edg_dens(g, g.IDmap.lst))
		except FileNotFoundError:
			print("Warning: network %s not found, data not generated."%repr(network))

	df = pd.DataFrame()
	df['Network'] = exist_network_lst
	df['Number of Genes'] = num_node_lst
	df['Number of Edges'] = num_edge_lst
	df['Edge Density'] = edg_dens_lst

	df.to_csv(fig_dir + 'TableS1.tsv', index=False, sep='\t')

if __name__ == '__main__':
	export_table()
