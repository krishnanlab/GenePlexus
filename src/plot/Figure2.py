from commonvar import *

def genfig(result_df, rank_df, figname, score_type, valsplit):
	fig, axes = plt.subplots(3, 1, figsize=(4,8))

	group_lst = [
		(['GOBPtmp'], 'Temporal Holdout'),
		(['GOBP', 'KEGGBP'], 'Study-bias Holdout'),
		(['DisGeNet', 'BeFree', 'GWAS', 'MGI'], 'Study-bias Holdout')
	]

	# average rank boxplots
	for i, group in enumerate(group_lst):
		ax = axes[i]
		sub_gsc_lst, valsplit_name = group
		sub_df = rank_df[rank_df['Geneset Collection'].isin(sub_gsc_lst)]
		sns.boxplot(data=sub_df, x='Method', y='Average Rank', ax=ax, \
					notch=True, color='.9', showfliers=False)
		for gsc in sub_gsc_lst:
			sns.pointplot(data=sub_df[sub_df['Geneset Collection'] == gsc], x='Method', \
						y='Average Rank', hue='Network', ax=ax, \
						join=False, dodge=0.5, hue_order=network_lst, \
						markers=gsc_marker[gsc], palette=network_color)
			
		ax.invert_yaxis()
		ax.get_legend().remove()
		ax.set_xlabel('')
		ax.set_ylabel('Average Rank', fontsize=10)
		plt.setp(ax.collections, sizes=[30], \
				edgecolors='k', linewidths=0.5, alpha=0.7)
		if i != (len(group_lst) - 1):
			ax.get_xaxis().set_ticklabels([])
		title_str = valsplit_name + '\n(' + ', '.join(sub_gsc_lst) + ')'
		ax.set_title(title_str, fontsize=10)

		# pannel annotation
		ax.annotate(panel_annot_lst[i], xy=(0, 0), \
					xytext=(0.95, 0.85), textcoords='axes fraction', \
					xycoords='axes fraction', fontsize=12, ha='center', color='k')

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

	# format figure and place legends
	fig.subplots_adjust(left=0.3, bottom=0.27, right=0.99, top=0.95, wspace=0.12, hspace=0.4)
	fig.legend(legend_elements1, legend_labels1, ncol=3, loc = 10, bbox_to_anchor=(0.5, 0.18), \
			frameon=False, title=r'$\bf{Networks}$', fontsize=10)
	fig.legend(legend_elements2, legend_labels2, ncol=3, loc = 10, bbox_to_anchor=(0.5, 0.065), \
			frameon=False, title=r'$\bf{Geneset}$ $\bf{Collections}$', fontsize=10)
	
	# add panel descriptions
	fig.text(0.09, 0.83, 'Function Prediction', fontsize=10, fontweight='bold', \
			ha='center', rotation='vertical')
	fig.text(0.08, 0.41, 'Disease and Trait\nPrediction', fontsize=10, \
			fontweight='bold', ha='center', rotation='vertical')

	plt.savefig(fig_dir + figname)
	plt.close()

if __name__ == '__main__':
	result_df = helperfun.get_result_df(result_fp)
	rank_df = helperfun.get_rank_df(result_df, 'Holdout', 'auPRC')
	genfig(result_df, rank_df, 'Figure2.pdf', 'auPRC', 'Holdout')
