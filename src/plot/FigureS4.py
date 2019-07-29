from commonvar import *

def genfig(result_df, rank_df_dict, figname):
	fig, axes = plt.subplots(len(network_lst), len(score_type_lst), figsize=(8, 10))
	group_lst = [
		(['GOBPtmp'], 'Temporal Holdout', 'Holdout'),
		(['GOBP', 'KEGGBP'], 'Study-bias Holdout', 'Holdout'),
		(['GOBP', 'KEGGBP'], '5-Fold Cross Validatoin', '5FCV'),
		(['DisGeNet', 'BeFree', 'GWAS', 'MGI'], 'Study-bias Holdout', 'Holdout'),
		(['DisGeNet', 'BeFree', 'GWAS', 'MGI'], '5-Fold Cross Validatoin', '5FCV')
	]

	for i, group in enumerate(group_lst):
		sub_gsc_lst, valsplit_name, valsplit = group
		for j, score_type in enumerate(score_type_lst):
			ax = axes[i,j]
			rank_df = rank_df_dict[valsplit][score_type]
			sub_df = rank_df[rank_df['Geneset Collection'].isin(sub_gsc_lst)]
			sns.boxplot(data=sub_df, x='Method', y='Average Rank', ax=ax, \
						notch=True, color='.9', showfliers=False)
			for gsc in sub_gsc_lst:
				sns.pointplot(data=sub_df[sub_df['Geneset Collection'] == gsc], \
							x='Method', y='Average Rank', hue='Network', ax=ax, \
							join=False, dodge=0.5, hue_order=network_lst, \
							markers=gsc_marker[gsc], palette=network_color)

			ax.get_legend().remove()
			ax.set_xlabel('')
			ax.set_ylabel('')
			if i == 0:
				ax.set_title(score_type, fontsize=12, fontweight='bold')
			if i != (len(group_lst) - 1):
				ax.get_xaxis().set_ticklabels([])
			if j == 0:
				ax.set_ylabel('Average Rank for\n' + valsplit_name, fontsize=9)

			ax.invert_yaxis()
			plt.setp(ax.collections, sizes=[30], edgecolors='k', linewidths=0.5, alpha=0.7)
			ax.yaxis.set_major_formatter(FormatStrFormatter('%.1f'))

			# panel annotation
			ax.annotate(panel_annot_lst[i * len(score_type_lst) + j], color='k', \
						textcoords='axes fraction', xycoords='axes fraction', \
						fontsize=12, ha='center', xy=(0, 0), xytext=(0.93, 0.88))

	# make legends
	legend_elements1 = []
	legend_labels1 = []
	for network in network_lst:
		legend_elements1.append(Line2D([0], [0], color=network_color[network], lw=4))
		legend_labels1.append(network)

	legend_elements2 = []
	legend_labels2 = []
	for gsc in gsc_lst:
		legend_elements2.append(Line2D([0], [0], marker=gsc_marker[gsc], color='w', \
			markerfacecolor='k', markersize=15 if gsc_marker[gsc] == '*' else 10))
		legend_labels2.append(gsc)

	# format the figure and place the legend
	fig.subplots_adjust(left=0.15, bottom=0.11, right=0.99, top=0.965, wspace=0.2, hspace=0.1)
	fig.legend(legend_elements1, legend_labels1, ncol=5, loc = 10, bbox_to_anchor=(0.5, 0.06), \
				frameon=False, title=r'$\bf{Networks}$', fontsize=10)
	fig.legend(legend_elements2, legend_labels2, ncol=7, loc = 10, bbox_to_anchor=(0.5, 0.02), \
				frameon=False, title=r'$\bf{Geneset}$ $\bf{Collections}$', fontsize=10)

	fig.text(0.03, 0.93, 'Function Prediction (GOBPtmp, GOBP, KEGGBP)', fontsize=12, \
			fontweight='bold', ha='center', rotation='vertical')
	fig.text(0.03, 0.4, 'Disease and Trait Prediction\n(DisGeNet, BeFree, GWAS, MGI)', \
			fontsize=12, fontweight='bold', ha='center', rotation='vertical')

	plt.savefig(fig_dir + figname)
	plt.close()

if __name__ == '__main__':
	result_df = helperfun.get_result_df(result_fp)
	rank_df_dict = helperfun.get_rank_df_dict(result_df)
	genfig(result_df, rank_df_dict, 'FigureS4.pdf')
