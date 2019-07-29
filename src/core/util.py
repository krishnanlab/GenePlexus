import numpy as np
import os

class IDmap:
	def __init__(self):
		self._data = {}
		self._lst = []

	def __contains__(self, key):
		return key in self._data

	def __getitem__(self, key):
		if isinstance(key, (list,np.ndarray)):
			idx_ary = np.array([self.data[i] for i in key])
			return np.array(idx_ary)
		else:
			return self._data[key]

	@property
	def size(self):
		return len(self._data)

	@property
	def data(self):
		return self._data
	
	@property
	def lst(self):
		return self._lst
	
	def addID(self, ID):
		"""
		Args:
			ID (str):	ID to be added

		Return:
			bool: True if ID not exist, False if ID exists.
		"""
		if ID not in self:
			self._data[ID] = self.size
			self._lst.append(ID)
			return True
		return False

	def idx2ID(self, idx):
		return self._lst[idx]



