from commonvar import *

def genfig(result_df, prop_df_dict, figname, score_type, valsplit, method_lst):
	n_row = len(network_lst)
	n_col = len(prop_lst) * len(method_lst)
	fig, axes = plt.subplots(n_row, n_col, figsize=(2*n_col, 2*n_row), sharey='row')

	for i, network in enumerate(network_lst):
		for prop_idx, prop in enumerate(prop_lst):
			for method_idx, method in enumerate(method_lst):
				j = prop_idx * len(method_lst) + method_idx
				ax = axes[i,j]
				ax.tick_params(labelsize=8.5)
				ax.set_xlabel(prop if i == (len(network_lst) - 1) else '')
				ax.set_ylabel(network + '\n' + score_type if j == 0 else '')
				if i == 0:
					ax.set_title(method)
				if prop != 'Number of Genes':
					ax.set_xscale('log')

				for color, sub_gsc_lst in gsc_color_dict.items():
					combined_prop_ary = np.array([])
					combined_score_ary = np.array([])
					for gsc in sub_gsc_lst:
						indicator = helperfun.subset_indicator(result_df, network=network, gsc=gsc, \
											method=method, score_type=score_type, valsplit=valsplit)
						sub_df = result_df[indicator]
						score_ary, prop_ary = helperfun.get_score_prop_ary(prop_df_dict, prop, sub_df, network, gsc)
						combined_prop_ary = np.append(combined_prop_ary, prop_ary)
						combined_score_ary = np.append(combined_score_ary, score_ary)
					sns.regplot(combined_prop_ary, combined_score_ary, color=color, x_bins=10, \
								fit_reg=False, ax=ax, scatter_kws={'s':18})

	# make legends
	legend_elements = []
	legend_labels = []
	for color, sub_gsc_lst in gsc_color_dict.items():
		group_name = r'$\bf{}$ $\bf{}$'.format(*gsc_group_color_dict[color].split())
		legend_elements.append(Line2D([0], [0], color=color, marker='o', lw=0))
		legend_labels.append(group_name + '\n(' + ', '.join(sub_gsc_lst) + ')')
	fig.legend(legend_elements, legend_labels, ncol=3, loc = 10, \
				bbox_to_anchor=(0.5, 0.03), frameon=False)

	plt.tight_layout(rect=[0, 0.04, 1, 1])
	plt.subplots_adjust(hspace=0.15, wspace=0.08)
	plt.savefig(fig_dir + figname)
	plt.close()

if __name__ == '__main__':
	result_df = helperfun.get_result_df(result_fp)
	prop_df_dict = helperfun.get_prop_df_dict(prop_dir)
	genfig(result_df, prop_df_dict, 'FigureS9.pdf', 'auPRC', 'Holdout', ['SL-A', 'LP-I'])