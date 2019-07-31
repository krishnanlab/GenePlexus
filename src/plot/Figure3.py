from commonvar import *

def genfig(result_df, figname, score_type, valsplit):
	if valsplit == '5FCV':
		fig,axes = plt.subplots(1, 2, figsize=(5.8,3), gridspec_kw={'width_ratios':[2, 4]}, sharex='col', sharey=True)
	else:
		fig,axes = plt.subplots(1, 2, figsize=(6.8,3), gridspec_kw={'width_ratios':[3, 4]}, sharex='col', sharey=True)

	annot_df,test_score_combined_df = helperfun.performance_test(result_df, \
										valsplit, score_type, method_class_dict, alpha)

	grouped_gsc_lst = [i for i in gsc_group_dict.values()]
	for group_idx in range(2):
		group = grouped_gsc_lst[group_idx]
		if (valsplit == '5FCV') & (group_idx == 0):
			offset = 1
		else:
			offset = 0
		sns.heatmap(test_score_combined_df[grouped_gsc_lst[group_idx][offset:]], \
			annot=annot_df[grouped_gsc_lst[group_idx][offset:]], \
			fmt='',ax=axes[group_idx], \
			center=0.5,cmap='coolwarm',vmin=0,vmax=1, \
			cbar_ax=None if 0 else fig.add_axes([.87, .15, .02, .7]) )
		helperfun.bold_text(axes[group_idx])
	axes[0].set_title('Function Prediction')
	axes[1].set_title('Disease and Trait Prediction')

	#add colorbar label
	fig.text(0.96, 0.83, 'Percentage of times SL outperforms LP', fontsize=8, ha='center', rotation='vertical')

	fig.tight_layout(rect=[0, 0, 0.87, 1])
	fig.subplots_adjust(hspace=0.08, wspace=0.08)
	plt.savefig(fig_dir + figname)
	plt.close()

if __name__ == '__main__':
	result_df = helperfun.get_result_df(result_fp)
	genfig(result_df, 'Figure3.pdf', 'auPRC', 'Holdout')






