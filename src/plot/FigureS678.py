from commonvar import *

def genfig(result_df, figname, score_type):
	fig, axes = plt.subplots(len(network_lst), len(valsplit_dict), \
					figsize=(8.6,9.8), gridspec_kw={'width_ratios':[7,6]})

	for i, network in enumerate(network_lst):
		for j, valsplit in enumerate(valsplit_dict):
			ax = axes[i,j]
			gsc_order = gsc_lst[:] if valsplit == 'Holdout' else gsc_lst[1:]
			indicator = helperfun.subset_indicator(result_df, network=network, \
								valsplit=valsplit, score_type=score_type)
			helperfun.sorted_boxplot(x='Geneset Collection', y='Score', \
				data=result_df[indicator], order=gsc_order, \
				ax=ax, hue='Method', hue_order=method_lst, notch=True, \
				showfliers=False, palette=boxplot_color, linewidth=0.9)
			ax.get_legend().remove()
			ax.set_xlabel('')
			ax.tick_params(labelsize=8.5)
			ax.yaxis.set_major_locator(MaxNLocator(nbins=3, integer=True))
			ax.axhline(y=0.5 if score_type == 'auROC' else 0, linestyle='--', alpha=0.8)

			if i == 0:
				ax.set_title(valsplit_dict[valsplit])
			if j == 0:
				ax.set_ylabel(network + '\n' + score_type)
			else:
				ax.set_ylabel('')

	plt.legend(bbox_to_anchor=(0.4,-0.13), frameon=False, ncol=4)
	fig.tight_layout(rect=[0, 0, 1, 1])
	fig.subplots_adjust(wspace=0.12 if score_type == 'auROC' else 0.08, hspace=0.16)
	plt.savefig(fig_dir + figname)
	plt.close()

if __name__ == '__main__':
	result_df = helperfun.get_result_df(result_fp)
	for i, score_type in enumerate(score_type_lst):
		genfig(result_df, 'FigureS' + str(i+6) + '.pdf', score_type)
