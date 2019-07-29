from sklearn.model_selection import StratifiedKFold
import pandas as pd
import numpy as np
from core import util

class LabelSet:
	def __init__(self, fp):
		self.load(fp)

	@property
	def IDmap(self):
		return self._IDmap

	@property
	def label_ary(self):
		return self._label_ary

	@property
	def pos_IDlst(self):
		return [self.IDmap.lst[i] for i in np.where(self.label_ary == 1)[0]]

	@property
	def train_test_info_ary(self):
		return self._train_test_info_ary

	def load(self, fp):
		df = pd.read_csv(fp, sep='\t')
		IDmap = util.IDmap()
		for ID in df['Entrez Gene ID']:
			assert IDmap.addID(str(ID))
		label_ary = np.array(df['Label'], dtype=bool)
		train_test_info_ary = np.array(df['Train or Test']) == 'Tr'
		self._IDmap = IDmap
		self._label_ary = label_ary
		self._train_test_info_ary = train_test_info_ary

	def __get_id_label(self, idx_ary):
		id_ary = np.array([self.IDmap.lst[i] for i in idx_ary])
		label_ary = self.label_ary[idx_ary]
		return id_ary, label_ary

	def split(self, mode):
		def get_id_label(train_idx_ary, test_idx_ary):
			train_id_ary, train_label_ary = self.__get_id_label(train_idx_ary)
			test_id_ary, test_label_ary = self.__get_id_label(test_idx_ary)
			return train_id_ary, train_label_ary, test_id_ary, test_label_ary

		if mode == '5FCV':
			splitgen = StratifiedKFold(n_splits=5)
			for train_idx_ary, test_idx_ary in splitgen.split(self.label_ary, self.label_ary):
				yield get_id_label(train_idx_ary, test_idx_ary)
		elif mode == 'Holdout':
			train_idx_ary = np.where(self.train_test_info_ary == True)[0]
			test_idx_ary = np.where(self.train_test_info_ary == False)[0]
			if min(self.label_ary[train_idx_ary].sum(), self.label_ary[test_idx_ary].sum()) < 10:
				yield None, None, None, None
			else:
				yield get_id_label(train_idx_ary, test_idx_ary)
		else:
			raise ValueError('Unknown validation split mode %s'%repr(mode))
	

