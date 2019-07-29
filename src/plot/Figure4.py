from commonvar import *

def genfig(result_df, figname, score_type, valsplit):
	group_dict = gsc_group_dict.copy()
	if valsplit == '5FCV':
		group_dictp['Function Prediction'].pop(0)

	fig = plt.figure(figsize=(6.4,8.8))
	gs1 = gridspec.GridSpec(len(network_lst) + 2, len(gsc_group_dict), \
		hspace=0, wspace=0.1, width_ratios=[len(group) for group in group_dict.values()])
	gs2 = gridspec.GridSpec(len(network_lst) - 1, len(gsc_group_dict))
	for network_idx, network in enumerate(network_lst):
		for gsc_group_idx, gsc_group in enumerate(group_dict):
			ax = plt.subplot(gs1[network_idx, gsc_group_idx])
			if (network_idx + gsc_group_idx) == 0:
				ax.annotate('A)', fontweight='bold', \
					xy=(-0.2, 1.05), xycoords='axes fraction', fontsize=11)
			indicator = helperfun.subset_indicator(result_df, network=network, \
				valsplit=valsplit, score_type=score_type)
			helperfun.sorted_boxplot(x='Geneset Collection', y='Score', \
				data=result_df[indicator], order=group_dict[gsc_group], \
				ax=ax, hue='Method', hue_order=method_lst, notch=True, \
				showfliers=False, palette=boxplot_color, linewidth=0.9)
			ax.get_legend().remove()
			ax.set_xlabel('')
			ax.yaxis.set_major_locator(MaxNLocator(nbins=3, integer=True))

			if score_type == 'auROC':
				baseline = 0.5
				wspace = 0.18
			else:
				baseline = 0
				wspace = 0.14
			ax.axhline(y=baseline, linestyle='--', alpha=0.8)

			if network_idx == 0:
				ax.set_title(gsc_group)
			if gsc_group_idx == 0:
				ax.set_ylabel(network + '\n' + score_type)
			else:
				ax.set_ylabel('')

	# part b
	median_score_df = pd.DataFrame()
	median_score_name = ' '.join(['Median', score_type])
	# gsc - network - method
	for gsc in gsc_lst:
		for network in network_lst:
			for method in method_lst:
				try:
					indicator = helperfun.subset_indicator(result_df, network=network, \
						method=method, gsc=gsc, valsplit=valsplit, score_type=score_type)
					median_score = np.nanmedian(result_df[indicator]['Score'].values)
					tmp_df = pd.DataFrame()
					tmp_df['Network'] = [network]
					tmp_df['Geneset Collection'] = [gsc]
					tmp_df['Method'] = [method]
					tmp_df[median_score_name] = [median_score]
					median_score_df = median_score_df.append(tmp_df)
				except KeyError:
					pass
	ax = plt.subplot(gs2[-1,:])
	order = gsc_lst if valsplit != '5FCV' else gsc_lst[1:]
	sns.boxplot(data=median_score_df, x='Geneset Collection', y=median_score_name, order=order, \
				color='grey', showfliers=False, boxprops={'alpha':0.3}, ax=ax, notch=True)
	sns.swarmplot(data=median_score_df, x='Geneset Collection', y=median_score_name, order=order, ax=ax, \
				hue='Method', hue_order=method_lst, palette=boxplot_color, dodge=True)
	ax.get_legend().remove()
	ax.set_xlabel('')
	ax.annotate('B)', fontweight='bold', xy=(-0.08, 1.05), xycoords='axes fraction', fontsize=11)

	fig.tight_layout(rect=[0.015, 0.025, 1, 0.98])
	plt.legend(bbox_to_anchor=(0.82,-0.13),frameon=False,ncol=4)
	plt.savefig(fig_dir + figname)
	plt.close()

if __name__ == '__main__':
	result_df = helperfun.get_result_df(result_fp)
	genfig(result_df, 'Figure4.pdf', 'auPRC', 'Holdout')






