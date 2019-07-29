from commonvar import *

def get_prop_df(prop_df_dict, network):
	prop_df = pd.DataFrame()
	for gsc in prop_df_dict:
		tmp_df = prop_df_dict[gsc][network]
		tmp_df['Geneset Collection'] = gsc
		prop_df = prop_df.append(tmp_df)
	return prop_df

def genfig(prop_df_dict, figname):
	fig, axes = plt.subplots(len(network_lst), len(prop_lst), figsize=(7.2,8.7))
	fig.tight_layout(rect=[0, 0.03, 1, 0.98])
	plt.subplots_adjust(hspace=0.12, wspace=0.20)

	for i, network in enumerate(network_lst):
		prop_df = get_prop_df(prop_df_dict, network)
		for j, prop in enumerate(prop_lst):
			ax = axes[i,j]
			sns.boxplot(data=prop_df, x='Geneset Collection', y=prop, order=gsc_lst, \
					notch=True, showfliers=False, palette=gsc_distinct_color, ax=ax)

			ax.set_yscale('log')
			ax.tick_params(labelsize=7.5)
			ax.set_xlabel('')
			ax.set_ylabel('')
			ax.get_xaxis().set_ticklabels([])
			if i == 0:
				ax.set_title(prop, fontsize=12, fontweight='bold')
			if j == 0:
				ax.set_ylabel(network, fontsize=11)

	# make legends
	legend_elements = []
	legend_labels = []
	for gsc in gsc_lst:
		legend_elements.append(Line2D([0], [0], color=gsc_distinct_color[gsc], marker='o', lw=0))
		legend_labels.append(gsc)

	# format the figure and place the legend
	fig.legend(legend_elements, legend_labels, ncol=4, loc = 10, \
				bbox_to_anchor=(0.5, 0.03), frameon=False)

	plt.savefig(fig_dir + figname)
	plt.close()

if __name__ == '__main__':
	prop_df_dict = helperfun.get_prop_df_dict(prop_dir)
	genfig(prop_df_dict, 'FigureS3.pdf')