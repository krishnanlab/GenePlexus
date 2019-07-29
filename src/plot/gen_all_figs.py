from commonvar import *
import Figure2, Figure3, Figure4, Figure5, Figure6
import FigureS1a2a, FigureS1b2b, FigureS3, FigureS4, FigureS5, FigureS678, FigureS9

if __name__ == '__main__':
	main_score_type = 'auPRC'
	maint_valsplit = 'Holdout'

	print('Loading and preprocessing result dataframe...')
	result_df = helperfun.get_result_df(result_fp)
	rank_df_dict = helperfun.get_rank_df_dict(result_df)
	prop_df_dict = helperfun.get_prop_df_dict(prop_dir)
	mdlsel_result_df = helperfun.get_result_df(mdlsel_result_fp)
	print('Done preprocessing, start gennerating figures...')

	Figure2.genfig(result_df, rank_df_dict[maint_valsplit][main_score_type], \
		'Figure2.pdf', main_score_type, maint_valsplit)
	print('Figure2 generated.')

	Figure3.genfig(result_df, 'Figure3.pdf', main_score_type, maint_valsplit)
	print('Figure3 generated.')

	Figure4.genfig(result_df, 'Figure4.pdf', main_score_type, maint_valsplit)
	print('Figure4 generated.')

	Figure5.genfig(result_df, prop_df_dict, 'Figure5.pdf', main_score_type, \
		maint_valsplit, ['SL-A', 'LP-I'], 'STRING')
	print('Figure5 generated.')

	Figure6.genfig(result_df, 'Figure6.pdf', main_score_type, maint_valsplit)
	print('Figure6 generated.')

	FigureS1a2a.genfig(mdlsel_result_df, 'FigureS1a.pdf', 'auPRC', 'Holdout', \
		method_group_dict['Label Propagation'])
	print('FigureS1a generated.')

	FigureS1b2b.genfig(mdlsel_result_df, 'FigureS1b.pdf', 'auPRC', 'Holdout', \
		method_group_dict['Label Propagation'])
	print('FigureS1b generated.')

	FigureS1a2a.genfig(mdlsel_result_df, 'FigureS2a.pdf', 'auPRC', 'Holdout', \
		method_group_dict['Supervised Learning'])
	print('FigureS2a generated.')

	FigureS1b2b.genfig(mdlsel_result_df, 'FigureS2b.pdf', 'auPRC', 'Holdout', \
		method_group_dict['Supervised Learning'])
	print('FigureS2b generated.')

	FigureS3.genfig(prop_df_dict, 'FigureS3.pdf')
	print('FigureS3 generated.')

	FigureS4.genfig(result_df, rank_df_dict, 'FigureS4.pdf')
	print('FigureS4 gnereated.')

	FigureS5.genfig(result_df, 'FigureS5.pdf')
	print('FigureS5 generated.')

	FigureS678.genfig(result_df, 'FigureS6.pdf', main_score_type)
	print('FigureS6 generated.')

	FigureS678.genfig(result_df, 'FigureS7.pdf', 'P@TopK')
	print('FigureS7 generated.')

	FigureS678.genfig(result_df, 'FigureS8.pdf', 'auROC')
	print('FigureS8 generated.')

	FigureS9.genfig(result_df, prop_df_dict, 'FigureS9.pdf', main_score_type, \
		maint_valsplit, ['SL-A', 'LP-I'])
	print('FigureS9 generated.')

	print('All figures generated successfully.')
