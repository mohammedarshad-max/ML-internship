# -*- coding: utf-8 -*-
"""McDonald code replication.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1253AUsbpU5bPEYzs00MaCNiJ2tXH-Igv
"""

pip install msa

import pandas as pd

# Load dataset from a CSV file
mcdonalds = pd.read_csv('/content/mcdonalds.csv')

# Display the first few rows of the dataset to verify it's loaded correctly
print(mcdonalds.columns)

print(mcdonalds.shape)

print(mcdonalds.head(3))

import pandas as pd

MD_x = mcdonalds.iloc[:, 0:11]
MD_x = (MD_x == "Yes").astype(int)
column_means = MD_x.mean().round(2)

print(column_means)

from sklearn.decomposition import PCA

pca = PCA()
MD_pca = pca.fit(MD_x)

print(MD_pca.explained_variance_ratio_)


PCs = MD_pca.components_
PCs_rounded = PCs.round(1)

print(PCs_rounded)

import matplotlib.pyplot as plt

cluster_assignments = pca.transform(MD_x)

plt.scatter(cluster_assignments[:, 0], cluster_assignments[:, 1], color='grey')
plt.xlabel('PC1')
plt.ylabel('PC2')
plt.title('PCA Plot')
plt.show()


PCs = pca.components_

# Plot the projected axes
plt.plot([0, PCs[0, 0]], [0, PCs[0, 1]], color='red', linewidth=2, label='PC1')
plt.plot([0, PCs[1, 0]], [0, PCs[1, 1]], color='blue', linewidth=2, label='PC2')
plt.xlabel('Variable 1')
plt.ylabel('Variable 2')
plt.title('Projected Axes')
plt.legend()
plt.show()

from sklearn.cluster import KMeans

import numpy as np
np.random.seed(1234)
cluster_results = {}
k_values = range(2, 9)

for k in k_values:

    kmeans = KMeans(n_clusters=k, n_init=10, random_state=1234)
    kmeans.fit(MD_x)
    cluster_results[k] = kmeans.labels_
MD_km28 = cluster_results

!pip install rich
from rich import print

print(MD_km28)
print(kmeans.inertia_)

import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

for k, kmeans in MD_km28.items():
    inertia_values.append(kmeans)

plt.plot(list(MD_km28.keys()), marker='o')

plt.xlabel('Number of Segments (k)')
plt.ylabel('Within-Cluster Sum of Squares')
plt.title('Elbow Method')
plt.xticks(list(MD_km28.keys()))
plt.show()



from sklearn.utils import resample
import numpy as np
np.random.seed(1234)
boot_cluster_results = {}

k_values = range(2, 9)

n_boot = 100

for k in k_values:
    boot_labels = []

    for _ in range(n_boot):
        boot_samples = resample(MD_x, replace=True, random_state=np.random.randint(1, 1000))
        kmeans_boot = KMeans(n_clusters=k, n_init=10, random_state=1234)
        kmeans_boot.fit(boot_samples)
        boot_labels.append(kmeans_boot.labels_)

    boot_cluster_results[k] = boot_labels

!pip install pomegranate

from sklearn.metrics import silhouette_score

avg_silhouette = []
std_silhouette = []

for k, boot_labels in boot_cluster_results.items():
    silhouettes = [silhouette_score(MD_x, labels) for labels in boot_labels]

    avg_silhouette.append(np.mean(silhouettes))
    std_silhouette.append(np.std(silhouettes))

plt.errorbar(list(boot_cluster_results.keys()), avg_silhouette, yerr=std_silhouette, fmt='o')
plt.xlabel('Number of Segments (k)')
plt.ylabel('Average Silhouette Score')
plt.title('Bootstrapped Clustering Results')
plt.show()

import matplotlib.pyplot as plt

# Extract cluster membership probabilities for 4 segments
cluster_probs = MD_km28[4]

# Plot histogram of cluster membership probabilities
plt.hist(cluster_probs, bins=20, range=(0, 1))
plt.xlim(0, 1)
plt.xlabel('Cluster Membership Probability')
plt.ylabel('Frequency')
plt.title('Histogram of Cluster Membership Probabilities')
plt.show()

MD_k4 = MD_km28[4]

from sklearn.cluster import SpectralClustering

spectral_clustering = SpectralClustering(n_clusters=4, affinity='nearest_neighbors', random_state=1234)

MD_r4 = spectral_clustering.fit_predict(MD_x)

import matplotlib.pyplot as plt

segment_stability = [sum(MD_r4 == i) / len(MD_r4) for i in range(4)]

plt.bar(range(1, 5), segment_stability)
plt.ylim(0, 1)
plt.xlabel('Segment Number')
plt.ylabel('Segment Stability')
plt.title('Segment Stability from Spectral Clustering')
plt.show()

"""** Using Mixtures of Distributions**"""

from sklearn.mixture import GaussianMixture

# Set random seed
np.random.seed(1234)

# Initialize empty list to store fitted models for each k
fitted_models = []

# Define the range of k values
k_values = range(2, 9)

# Define the number of repetitions
n_rep = 10

# Iterate over each k value
for k in k_values:
    # Fit GMM for each repetition
    for _ in range(n_rep):
        # Initialize GMM with k components
        gmm = GaussianMixture(n_components=k, covariance_type='full', random_state=1234)

        # Fit GMM to the data
        gmm.fit(MD_x)

        # Store fitted GMM
        fitted_models.append(gmm)

# You can access the fitted models for different k values from fitted_models

# Initialize empty list to store average BIC values for each k
avg_bic_values = []

# Iterate over each k value
for k in k_values:
    # Extract BIC values for all models with the same k
    bic_values_k = [bic for i, bic in enumerate(bic_values) if (i % n_rep == 0) and (i // n_rep == k - 2)]

    # Calculate average BIC for current k
    avg_bic = np.mean(bic_values_k)

    # Store average BIC
    avg_bic_values.append(avg_bic)

# Plot the average BIC values
plt.plot(range(2, 9), avg_bic_values, marker='o')
plt.xlabel('Number of Components (k)')
plt.ylabel('Average BIC')
plt.title('Average BIC for Model Selection')
plt.show()

"""**Using Mixtures of Regression Models**"""

from collections import Counter

like_counts = Counter(mcdonalds['Like'])

reversed_counts = dict(reversed(like_counts.items()))

print(reversed_counts)

import pandas as pd

# Convert the "Like" column to numeric values
mcdonalds['Like'] = pd.to_numeric(mcdonalds['Like'], errors='coerce')

# Subtract the numeric values from 6 to create the new column "Like_n"
mcdonalds['Like_n'] = 6 - mcdonalds['Like']

# Display the table of counts for the new column
table_counts = mcdonalds['Like_n'].value_counts()
print(table_counts)

"""**A.6 Step 6: Profiling Segments**"""

from scipy.cluster.hierarchy import linkage, dendrogram
import numpy as np

distance_matrix = np.transpose(MD_x)

MD_vclust = linkage(distance_matrix, method='complete')

dendrogram(MD_vclust)
plt.xlabel('Segments')
plt.ylabel('Distance')
plt.title('Hierarchical Clustering Dendrogram')
plt.show()

import matplotlib.pyplot as plt


hierarchical_order = MD_vclust[:, 0].astype(int)

cluster_assignments = [MD_k4[i] for i in hierarchical_order]

plt.bar(range(len(cluster_assignments)), cluster_assignments, color=plt.cm.viridis(np.linspace(0, 1, len(cluster_assignments))))
plt.xlabel('Observation')
plt.ylabel('Cluster')
plt.title('Cluster Assignments with Hierarchical Clustering Shading')
plt.show()

import matplotlib.pyplot as plt

# Assuming MD_k4 contains the cluster assignments from k-means clustering
# Assuming MD_pca contains the PCA object
# Assuming MD_x contains the data

# Transform the data using the PCA object
MD_pca_components = MD_pca.components_
MD_pca_scores = MD_pca.transform(MD_x)

# Plot clustered data points projected onto the first two principal components
plt.scatter(MD_pca_scores[:, 0], MD_pca_scores[:, 1], c=MD_k4, cmap='viridis')

# Plot principal axes
plt.quiver(0, 0, MD_pca_components[0, 0], MD_pca_components[0, 1], scale=5, color='red')
plt.quiver(0, 0, MD_pca_components[1, 0], MD_pca_components[1, 1], scale=5, color='blue')

# Set labels and title
plt.xlabel('Principal Component 1')
plt.ylabel('Principal Component 2')
plt.title('Clustered Data Points with Principal Axes')

# Show plot
plt.show()

"""**Step 7: Describing Segments**"""

import pandas as pd


k4 = MD_k4

df = pd.DataFrame({'Cluster': k4, 'Like': mcdonalds['Like']})

table_counts = pd.crosstab(df['Cluster'], df['Like'])

table_counts.plot(kind='bar', stacked=True)
plt.xlabel('Cluster')
plt.ylabel('Count')
plt.title('Mosaic Plot of Cluster vs Like')
plt.show()

import pandas as pd
from statsmodels.graphics.mosaicplot import mosaic


k4 = MD_k4

df = pd.DataFrame({'Cluster': k4, 'Gender': mcdonalds['Gender']})

table_counts = pd.crosstab(df['Cluster'], df['Gender'])

mosaic(df, ['Cluster', 'Gender'], title='Mosaic Plot of Cluster vs Gender', axes_label=True)
plt.show()