from core import util
import numpy as np

class AdjLst:
	"""
	Attributes:
		data (list of dict): undirected adjacency list
		IDmap (IDmap):
	"""
	def __init__(self):
		self.data = []
		self.IDmap = util.IDmap()

	def addEdge(self, ID1, ID2, weight):
		for ID in ID1, ID2:
			if self.IDmap.addID(ID):
				self.data.append({})
		idx1 = self.IDmap[ID1]
		idx2 = self.IDmap[ID2]
		self.data[idx1][idx2] = self.data[idx2][idx1] = weight

	def to_npymat(self):
		dim = self.IDmap.size
		mat = np.zeros((dim, dim))
		for idx1 in range(dim):
			for idx2, weight in self.data[idx1].items():
				mat[idx1, idx2] = weight
		return mat

class WUGraph:
	"""Weighted Undirected Graph object.

	"""
	def __init__(self, IDmap=None, mat=None):
		self._IDmap = None
		self._mat = None
		if IDmap is not None and mat is not None:
			self.load_graph(IDmap, mat)

	@property
	def IDmap(self):
		return self._IDmap

	@property
	def mat(self):
		return self._mat

	@property
	def size(self):
		return self.IDmap.size
	
	def load_graph(self, IDmap, mat):
		assert isinstance(IDmap, util.IDmap)
		assert IDmap.size == mat.shape[0] == mat.shape[1]
		self._IDmap = IDmap
		self._mat = mat

	@classmethod
	def from_edgelist(cls, fp):
		"""Construct graph object from edge list file

		Args:
			fp (str):	Path to edge list file
		"""
		adjlst = AdjLst()
		with open(fp, 'r') as f:
			for line in f:
				data = line.split('\t')
				weight = float(data[2] if len(data) == 3 else 1)
				ID1, ID2 = data[:2]
				adjlst.addEdge(ID1.strip(), ID2.strip(), weight)
		mat = adjlst.to_npymat()
		IDmap = adjlst.IDmap
		return cls(IDmap=IDmap, mat=mat)

	@classmethod
	def from_npymat(cls, fp):
		"""Construct graph object from numpy matrix file

		Args:
			fp (str):	Path to numpy matrix file
		"""
		mat = np.load(fp)
		dim = mat.shape[0]
		IDmap = util.IDmap()
		for ID in mat[:,0]:
			assert IDmap.addID(str(int(ID)))
		mat = mat[:,1:]
		IDmap = IDmap
		return cls(IDmap=IDmap, mat=mat)

class Influence(WUGraph):
	def __init__(self, IDmap=None, mat=None, beta=0.85):
		super().__init__(IDmap=IDmap, mat=mat)
		if IDmap is not None and mat is not None:
			self.__transform(beta=beta)

	def __transform(self, beta):
		col_norm = self.mat / self.mat.sum(axis=0)
		self._mat = beta * np.linalg.inv(np.identity(self.size) - (1 - beta) * col_norm)

	@classmethod
	def from_wugraph(cls, wugraph, beta):
		return cls(wugraph.IDmap, wugraph.mat, beta)

class Embedding(WUGraph):
	def __init__(self, IDmap=None, mat=None):
		super().__init__(IDmap=IDmap, mat=mat)

	def load_graph(self, IDmap, mat):
		assert isinstance(IDmap, util.IDmap)
		assert IDmap.size == mat.shape[0]
		self._IDmap = IDmap
		self._mat = mat

	@classmethod
	def from_edgelist(cls, fp):
		raise TypeError("Can't load embeddings from edgelist files, use from_emd or from_npymat")

	@classmethod
	def from_emd(cls, fp):
		IDmap = util.IDmap()
		fvec_lst = []
		with open(fp, 'r') as f:
			f.readline() # skip header line
			for line in f:
				terms = line.split()
				ID = terms[0].strip()
				assert IDmap.addID(ID)
				fvec_lst.append(np.array(terms[1:], dtype=float))
		mat = np.asarray(fvec_lst)
		return cls(IDmap=IDmap, mat=mat)

def get_edg_dens(g, pos_IDlst):
	pos_idx_ary = g.IDmap[pos_IDlst]
	edg_sum = g.mat[pos_idx_ary][:,pos_idx_ary].sum()
	max_sum = len(pos_IDlst) * (len(pos_IDlst) - 1)
	edg_dens = edg_sum / max_sum
	return edg_dens

def get_seg(g, pos_IDlst):
	pos_idx_ary = g.IDmap[pos_IDlst]
	inner_conn = g.mat[pos_idx_ary][:,pos_idx_ary].sum()
	all_conn = g.mat[pos_idx_ary].sum() + g.mat[:,pos_idx_ary].sum() - inner_conn
	seg = inner_conn / all_conn
	return seg
