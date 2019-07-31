from commonvar import *

def genfig(result_df, figname):
	fig, axes = plt.subplots(3,3,figsize=(8,8))
	fig.tight_layout(rect=[0.09, 0.15, 1, 0.98])
	fig.subplots_adjust(hspace=0.22, wspace=0.08)

	valsplit_dict = {
		'GO Temporal Holdout': 'Holdout',
		'Study-bias Holdout': 'Holdout',
		'5-Fold Cross Validatoin': '5FCV'
	}

	for i, valsplit in enumerate(valsplit_dict):
		for j, score_type in enumerate(score_type_lst):
			if valsplit == 'GO Temporal Holdout':
				annot_df,test_score_combined_df = helperfun.performance_test(result_df, \
					valsplit_dict[valsplit], score_type, method_class_dict, alpha, gsc_lst=[gsc_lst[0]])
			else:
				annot_df,test_score_combined_df = helperfun.performance_test(result_df, \
					valsplit_dict[valsplit], score_type, method_class_dict, alpha, gsc_lst=gsc_lst[1:])

			sns.heatmap(test_score_combined_df, annot=annot_df, fmt='',ax=axes[i,j], \
				center=0.5, cmap='coolwarm', vmin=0, vmax=1, \
				cbar_kws={"orientation": "horizontal"}, \
				cbar_ax=fig.add_axes([.18, 0.074, .7, .02]))
			helperfun.bold_text(axes[i,j], textsize=7)

			axes[i,j].set_xlabel('')
			axes[i,j].set_ylabel(valsplit if j == 0 else '', fontsize=9, fontweight='bold')
			if j != 0:
				axes[i,j].get_yaxis().set_ticklabels([])
			if i == 1:
				axes[i,j].get_xaxis().set_ticklabels([])
			if i == 0:
				axes[i,j].set_title(score_type, fontsize=12, fontweight='bold')

	#add colorbar label
	fig.text(0.5, 0.02, 'Percentage of times SL outperforms LP', fontsize=10, ha='center')

	plt.savefig(fig_dir + figname)
	plt.close()

if __name__ == '__main__':
	result_df = helperfun.get_result_df(result_fp)
	genfig(result_df, 'FigureS5.pdf')