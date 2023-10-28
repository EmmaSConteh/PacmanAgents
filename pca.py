# PCA Algorithm

import numpy as np

X = np.array([[4, 2, 3], [6, 1, 3], [4, 2, 5], [7, 8, 3]])

# 1. compute mean row vector and matrix
# 2. subtract mean from X

X_meaned = X - np.mean(X , axis = 0)

# 3. compute covariance matrix

cov_mat = np.cov(X_meaned , rowvar = False)

# Compute k largest eigenvalues and corresponding eigenvectors

eigen_values , eigen_vectors = np.linalg.eigh(cov_mat)

# Sort the eigenvalues in descending order

sorted_index = np.argsort(eigen_values)[::-1]
sorted_eigenvalue = eigen_values[sorted_index]
sorted_eigenvectors = eigen_vectors[:,sorted_index]

# Select the first n eigenvectors, n is desired dimension

n_components = 2
eigenvector_subset = sorted_eigenvectors[:,0:n_components]

# Transform the data

X_reduced = np.dot(eigenvector_subset.transpose() , X_meaned.transpose()).transpose()

print(X_reduced)