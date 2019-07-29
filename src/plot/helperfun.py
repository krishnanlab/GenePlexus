from seaborn.categorical import _BoxPlotter
from seaborn.utils import remove_na
from commonvar import *

def subset_indicator(df, **kwargs):
	for i, j in kwargs.items():
		key = kw_dict[i]
		try:
			indicator = indicator & (df[key] == j)
		except NameError:
			indicator = df[key] == j
	return indicator

def get_grouped_df(df):
	grouped_df = {}
	for gsc in gsc_lst:
		grouped_df[gsc] = {}
		for valsplit in valsplit_dict:
			grouped_df[gsc][valsplit] = subset_indicator(df, gsc=gsc, valsplit=valsplit)
	return grouped_df

def get_score(df, gs_lst, network, gsc, valsplit, method, score_type):
	indicator = subset_indicator(df, network=network, gsc=gsc, valsplit=valsplit, \
								method=method, score_type=score_type)
	sub_df = df[indicator]
	score_dict = {i:j for i,j in zip(sub_df['Geneset'].values, sub_df['Score'].values)}
	#score_ary = np.array([score_dict[i] for i in gs_lst])
	score_ary = np.zeros(len(gs_lst))
	for i, j in enumerate(gs_lst):
		try:
			score_ary[i] = score_dict[j]
		except KeyError:
			print('\t\t\t'+j)
	return score_ary

def get_score_prop_ary(prop_df_dict, prop, sub_df, network, gsc):
	score_ary = sub_df['Score'].values
	gs_lst = list(sub_df['Geneset'].values)
	prop_df = prop_df_dict[gsc][network]
	prop_dict = {i:j for i,j in zip(prop_df['Geneset'].values, prop_df[prop])}
	prop_ary = np.array([prop_dict[i] for  i in gs_lst])
	return score_ary, prop_ary
						
def bold_text(ax, textsize=10.5):
	for text in ax.texts:
		text.set_size(textsize)
		original_text = text.get_text()
		if original_text:
			text.set_color('k')
			if text.get_text()[-1] == '*':
				text.set_text(original_text[:-1])
				text.set_weight('bold')

def set_neginf_PTopK_to_min(df):
	score_type = 'P@TopK'
	finite_indicator = np.isfinite(df['Score'])
	for gsc in gsc_lst:
		gsc_indicator = df['Geneset Collection']==gsc
		for network in network_lst:
			gsc_net_indicator = gsc_indicator & (df['Network']==network)
			for valsplit in valsplit_dict:
				if (gsc == 'GOBPtmp') & (valsplit == '5FCV'):
					continue
				gsc_net_val_st_indicator = gsc_net_indicator & \
					(df['Validation Split']==valsplit) & (df['Score Type']==score_type)
				min_val = df[gsc_net_val_st_indicator & finite_indicator]['Score'].values.min()
				df.loc[gsc_net_val_st_indicator & ~finite_indicator, 'Score'] = min_val

def get_result_df(result_fp):
	result_df = pd.read_csv(result_fp, sep='\t')
	set_neginf_PTopK_to_min(result_df)
	return result_df

def get_rank_df(result_df, valsplit, score_type, method_lst=method_lst):
	rank_df = pd.DataFrame()
	n_methods = len(method_lst)
	for network in network_lst:
		#print(network)
		for gsc in gsc_lst:
			#print('\t'+gsc)
			if (gsc == 'GOBPtmp') & (valsplit == '5FCV'):
				continue
			indicator = subset_indicator(result_df, network=network, gsc=gsc, \
										valsplit=valsplit, score_type=score_type)
			gs_lst = list(result_df[indicator]['Geneset'].unique())
			n_gs = len(gs_lst)
			for method_idx, method in enumerate(method_lst):
				#print('\t\t'+method)
				score = get_score(result_df, gs_lst, network, gsc, valsplit, method, score_type)
				score_mat = score if method_idx == 0 else np.vstack([score_mat, score])
			notnan = ~np.isnan(score_mat[0])

			rank_mat = np.zeros((n_methods,n_gs))
			rank_mat[:] = np.nan
			for i in range(n_gs):
				if notnan[i]:
					rank_ary = score_mat[:,i].argsort()[::-1]
					rank_num = 1
					for j in range(n_methods):
						rank_mat[rank_ary[j],i] = rank_num
						if j < 3:
							if score_mat[rank_ary[j], i] > score_mat[rank_ary[j+1], i]:
								rank_num = j + 2

			sub_df = pd.DataFrame()
			sub_df['Method'] = method_lst
			sub_df['Network'] = network
			sub_df['Geneset Collection'] = gsc
			sub_df['Average Rank'] = [np.nanmean(rank_mat[i,:]) for i in range(n_methods)]
			rank_df = rank_df.append(sub_df, ignore_index=True)
	return rank_df

def get_rank_df_dict(result_df):
	rank_df_dict = {}
	for valsplit in valsplit_dict:
		rank_df_dict[valsplit] = {}
		for score_type in score_type_lst:
			rank_df_dict[valsplit][score_type] = get_rank_df(result_df, valsplit, score_type)
	return rank_df_dict

def get_prop_df_dict(prop_dir):
	prop_df_dict = {}
	for gsc in gsc_lst:
		prop_df_dict[gsc] = {}
		for network in network_lst:
			try:
				prop_df_dict[gsc][network] = pd.read_csv(prop_dir + gsc + '/' + network + '.tsv', sep='\t')
			except FileNotFoundError:
				print("Warning: geneset collection %s missing geneset properties for %s"%(repr(gsc),repr(network)))
				continue
	return prop_df_dict

def performance_test(df, valsplit, score_type, method_class_dict, alpha, gsc_lst=gsc_lst):
	method_class_lst = list(method_class_dict)
	# initialize annotation and average test score dataframes
	annot_df = pd.DataFrame([[''] * len(gsc_lst)] * len(network_lst))
	test_score_combined_df = pd.DataFrame(np.zeros((len(network_lst), len(gsc_lst))))
	test_score_combined_df.columns = annot_df.columns = [i for i in gsc_lst]
	test_score_combined_df.index = annot_df.index = [i for i in network_lst]

	for network in network_lst:
		for gsc in gsc_lst:
			gs_lst = list(df[subset_indicator(df, network=network, gsc=gsc)]['Geneset'].unique())
			score_dict = {}
			shape = []
			for method_class, methods in method_class_dict.items():
				score_dict[method_class] = {}
				shape.append(len(methods))
				for method in methods:
					method_name = '-'.join([method_class, method])
					sub_df = df[subset_indicator(df, network=network, gsc=gsc, 
							score_type=score_type, valsplit=valsplit, method=method_name)]
					score_dict[method_class][method] = get_score(df, \
							gs_lst, network, gsc, valsplit, method_name, score_type)

			# pair test between methods from different class
			class1 = method_class_lst[0]
			class2 = method_class_lst[1]
			test_mat_df = pd.DataFrame(np.zeros(shape))
			test_mat_df.index = ['-'.join([class1, method]) for method in method_class_dict[class1]]
			test_mat_df.columns = ['-'.join([class2, method]) for method in method_class_dict[class2]]
			test_score_combined = 0
			for method1 in method_class_dict[class1]:
				name1 = '-'.join([class1, method1])
				for method2 in method_class_dict[class2]:
					name2 = '-'.join([class2, method2])
					s1 = score_dict[class1][method1]
					s2 = score_dict[class2][method2]
					notnan = ~np.isnan(s1) & ~np.isnan(s2)
					s1 = s1[notnan]; s2 = s2[notnan]
					test_mat_df.loc[name1, name2] = wilcoxon(s1, s2)[1]
					test_score = (s1 > s2).sum() - (s2 > s1).sum()
					if test_score < 0:
						test_mat_df.loc[name1, name2] *= -1
					test_score_combined += test_score
			test_score_combined = test_score_combined / test_mat_df.size / s1.size / 2 + 0.5
			test_score_combined_df.loc[network, gsc] = test_score_combined
			test_mat = test_mat_df.values
			test_mat_df.iloc[:,:] = np.sign(test_mat) * \
				np.reshape(fdrcorrection(np.absolute(test_mat.flatten()), alpha=alpha)[0], test_mat_df.shape)

			# find winner
			winner = ''
			for method1 in test_mat_df.index:
				if test_mat_df.loc[method1,:].sum() == len(method_class_dict[class2]):
					if not winner:
						winner = method1
					else:
						winner += (',' + method1.split('-')[1])
						if len(winner.split(',')) == len(method_class_dict[class1]):
							winner = class1 + '*'
			for method2 in test_mat_df.columns:
				if test_mat_df.loc[:,method2].sum() == -len(method_class_dict[class1]):
					if not winner:
						winner = method2
					else:
						winner += (',' + method2.split('-')[1])
						if len(winner.split(',')) == len(method_class_dict[class2]):
							winner = class2 + '*'
			annot_df.loc[network, gsc] = winner

	return annot_df, test_score_combined_df

class SortedBoxPlotter(_BoxPlotter):
	def __init__(self, *args, **kwargs):
		super(SortedBoxPlotter, self).__init__(*args, **kwargs)

	def draw_boxplot(self, ax, kws):
		'''
		Below code has been copied partly from seaborn.categorical.py
		and is reproduced only for educational purposes.
		'''
		if self.plot_hues is None:
			# Sorting by hue doesn't apply here. Just
			return super(SortedBoxPlotter, self).draw_boxplot(ax, kws)

		vert = self.orient == "v"
		props = {}
		for obj in ["box", "whisker", "cap", "median", "flier"]:
			props[obj] = kws.pop(obj + "props", {})

		for i, group_data in enumerate(self.plot_data):

			# ==> Sort offsets by median
			offsets = self.hue_offsets
			medians = [ np.nanmedian(group_data[self.plot_hues[i] == h])
						for h in self.hue_names ]
			offsets_sorted = offsets[np.argsort(medians)[::-1].argsort()]

			# Draw nested groups of boxes
			for j, hue_level in enumerate(self.hue_names):

				# Add a legend for this hue level
				if not i:
					self.add_legend_data(ax, self.colors[j], hue_level)

				# Handle case where there is data at this level
				if group_data.size == 0:
					continue

				hue_mask = self.plot_hues[i] == hue_level
				box_data = remove_na(group_data[hue_mask])

				# Handle case where there is no non-null data
				if box_data.size == 0:
					continue

				# ==> Fix ordering
				center = i + offsets_sorted[j]

				artist_dict = ax.boxplot(box_data,
										 vert=vert,
										 patch_artist=True,
										 positions=[center],
										 widths=self.nested_width,
										 **kws)
				self.restyle_boxplot(artist_dict, self.colors[j], props)

def sorted_boxplot(x=None, y=None, hue=None, data=None, order=None, hue_order=None,
				   orient=None, color=None, palette=None, saturation=.75,
				   width=.8, dodge=True, fliersize=5, linewidth=None,
				   whis=1.5, notch=False, ax=None, **kwargs):

	'''
	Same as sns.boxplot(), except that nested groups of boxes are plotted by
	increasing median.
	'''

	plotter = SortedBoxPlotter(x, y, hue, data, order, hue_order,
							   orient, color, palette, saturation,
							   width, dodge, fliersize, linewidth)
	if ax is None:
		ax = plt.gca()
	kwargs.update(dict(whis=whis, notch=notch))
	plotter.plot(ax, kwargs)
	return ax
