from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.ensemble import RandomForestClassifier
import numpy as np
from core import graph

class MdlBase:
	def __init__(self, G):
		self.G = G

	@property
	def G(self):
		return self._G
	
	@G.setter
	def G(self, g):
		assert isinstance(g, graph.WUGraph)
		self._G = g

	def get_idx_ary(self, ID_ary):
		return self.G.IDmap[ID_ary]

	def get_x(self, ID_ary):
		idx_ary = self.get_idx_ary(ID_ary)
		return self.G.mat[idx_ary]

	def test(self, labelset, mode='Holdout'):
		y_true = np.array([])
		y_predict = np.array([])
		for train_id_ary, train_label_ary, test_id_ary, test_label_ary in labelset.split(mode):
			if train_id_ary is None:
				return None, None
			self.train(train_id_ary, train_label_ary)
			decision_ary = self.decision(test_id_ary, test_label_ary)
			y_true = np.append(y_true, test_label_ary)
			y_predict = np.append(y_predict, decision_ary)
		return y_true, y_predict

class LogReg(MdlBase, LogisticRegression):
	def __init__(self, G, penalty, solver='lbfgs', **kwargs):
		super().__init__(G)
		super(MdlBase, self).__init__(penalty=penalty, solver=solver, **kwargs)

	def train(self, ID_ary, y):
		x = self.get_x(ID_ary)
		self.fit(x, y)

	def decision(self, ID_ary, y):
		x = self.get_x(ID_ary)
		decision_ary = self.decision_function(x)
		return decision_ary

class SVM(MdlBase, LinearSVC):
	def __init__(self, G, **kwargs):
		super().__init__(G)
		super(MdlBase, self).__init__(**kwargs)

	def train(self, ID_ary, y):
		x = self.get_x(ID_ary)
		self.fit(x, y)

	def decision(self, ID_ary, y):
		x = self.get_x(ID_ary)
		decision_ary = self.decision_function(x)
		return decision_ary

class RF(MdlBase, RandomForestClassifier):
	def __init__(self, G, **kwargs):
		super().__init__(G)
		super(MdlBase, self).__init__(**kwargs)

	def train(self, ID_ary, y):
		x = self.get_x(ID_ary)
		self.fit(x, y)

	def decision(self, ID_ary, y):
		x = self.get_x(ID_ary)
		decision_ary = self.predict_proba(x)[:,1] # take positive class
		return decision_ary

class SL(LogReg):
	def __init__(self, G):
		super().__init__(G, 'l2')

class LP(MdlBase):
	def __init__(self, G):
		super(LP, self).__init__(G)

	def train(self, ID_ary, y):
		pos_idx_ary = self.get_idx_ary(ID_ary)[y]
		hotvecs_ary = np.zeros(self.G.size)
		hotvecs_ary[pos_idx_ary] = True
		self.coef_ = np.matmul(self.G.mat, hotvecs_ary)

	def decision(self, ID_ary, y):
		idx_ary = self.get_idx_ary(ID_ary)
		decision_ary = self.coef_[idx_ary]
		return decision_ary

"""
import UserModel #if necessary
class ModelTemplate(MdlBase, UserModel):
	def __init__(self, G):
		super().__init__(G)
		super(UserModel, self).__init__(*args, **kwargs)

	def train(self, ID_ary, y):
		# x is  feature arrays of all input IDs in ID_ary, size m x d, m number of training sample, d dimension
		x = self.get_x(ID_ary)
		# y is a boolean array indicating positive samples
		self.some_fit_fucntion_from_UserModel(x, y)

	def decision(self, ID_ary, y):
		x = self.get_x(ID_ary)
		decision_ary = self.some_decision_function_from_UserModel(x)
		return decision_ary
"""
