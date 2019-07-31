from commonvar import *

def get_annot(pvals, alpha=0.1):
	annot = pd.DataFrame(pvals)
	for i in annot:
		for j, k in enumerate(annot[i]):
			if k < alpha:
				annot.iloc[j,i] = r'$\bf{X}$'
			else:
				annot.iloc[j,i] = ''
	return annot

def pairtests(df, method1, method2, score_type, valsplit):
	fraction = np.zeros((5, 7))
	pvals = np.zeros((5, 7))
	for network_idx, network in enumerate(network_lst):
		for gsc_idx, gsc in enumerate(gsc_lst):
			indicator = helperfun.subset_indicator(df, network=network, gsc=gsc, \
										score_type=score_type, valsplit=valsplit)
			gs_lst = list(df[indicator]['Geneset'].unique())
			s1 = helperfun.get_score(df, gs_lst, network, gsc, valsplit, method1, score_type)
			s2 = helperfun.get_score(df, gs_lst, network, gsc, valsplit, method2, score_type)
			notnan = ~np.isnan(s1) & ~np.isnan(s2)
			s1 = s1[notnan]; s2 = s2[notnan]

			fraction[network_idx, gsc_idx] = (s1 > s2).sum() / (s1 != s2).sum()
			pvals[network_idx, gsc_idx] = wilcoxon(s1, s2)[1]
	annot = get_annot(pvals)
	fraction = pd.DataFrame(fraction)
	fraction.index = [network for network in network_lst]
	fraction.columns = [gsc for gsc in gsc_lst]
	return fraction, pvals, annot

def fix_annot_color(ax):
	for text in ax.texts:
		if text.get_text():
			text.set_color('k')

def genfig(result_df, figname, score_type, valsplit):
	fig, axes = plt.subplots(2, 1, figsize=(6.5,7), sharey=True)
	method1 = 'SL-E'
	for i, method2 in enumerate(['LP-I', 'SL-A']):
		f, p, annot = pairtests(result_df, method1, method2, score_type, valsplit)
		sns.heatmap(data=f, annot=annot, cmap='PuOr', center=0.5, vmin=0,vmax=1, ax=axes[i], fmt='', \
			cbar_kws={'orientation': 'horizontal', 'label':'Percentage of times SL-E outperforms the other method'}, \
			cbar_ax=fig.add_axes([.18, 0.07, .7, .022]))
		axes[i].set_title('Wilcoxon test %s vs %s'%('SL-E', method2))
		fix_annot_color(axes[i])
		axes[i].annotate(panel_annot_lst[i]+')', fontweight='bold',\
				xy=(-0.17, 1.05), xycoords='axes fraction', fontsize=11)
	fig.tight_layout(rect=[0, 0.095, 1, 1])
	plt.savefig(fig_dir + figname)
	plt.close()

if __name__ == '__main__':
	result_df = helperfun.get_result_df(result_fp)
	genfig(result_df, 'Figure6.pdf', 'auPRC', 'Holdout')
