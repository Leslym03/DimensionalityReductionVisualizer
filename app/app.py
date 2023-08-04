from flask import Flask, render_template, jsonify
import pandas as pd
from sklearn.datasets import load_wine
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.manifold import Isomap
import plotly.graph_objects as go
import json
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import DBSCAN

app = Flask(__name__)

# Cargar el conjunto de datos wine de scikit-learn
data = load_wine()
wine_df = pd.DataFrame(data.data, columns=data.feature_names)
wine_df['target'] = data.target

# Estandarizar los datos
scaler = StandardScaler()
wine_sintarget = wine_df.drop(columns=['target'])
wine_sintarget_scaled = pd.DataFrame(scaler.fit_transform(wine_sintarget), columns=wine_sintarget.columns)


@app.route('/')
def index():
   return render_template('index.html')

# Calcular la matriz de correlación de atributos
@app.route('/correlation_matrix')
def correlation_matrix_json():
    correlation_matrix = wine_df.corr()
    # Convertir la matriz de correlación a formato JSON compatible
    correlation_matrix_json = correlation_matrix.to_json(orient='split')
    return jsonify(correlation_matrix_json)


########################################## PCA

@app.route('/pca_plot')
def pca_plot():
    # Aplicar PCA para reducir la dimensionalidad a 2 componentes principales
    pca = PCA(n_components=2)
    wine_sintarget_scaled = wine_df.drop(columns=['target'])
    reduced_data = pca.fit_transform(wine_sintarget_scaled)

    # Crear un DataFrame con los datos reducidos
    reduced_df = pd.DataFrame(data=reduced_data, columns=['Component 1', 'Component 2'])
    reduced_df['target'] = wine_df['target']

    # Crear un gráfico de dispersión interactivo con Plotly
    fig = go.Figure()
    for target_label in reduced_df['target'].unique():
        fig.add_trace(go.Scatter(
            x=reduced_df.loc[reduced_df['target'] == target_label, 'Component 1'],
            y=reduced_df.loc[reduced_df['target'] == target_label, 'Component 2'],
            mode='markers',
            name=f'Clase {target_label}'
        ))
    fig.update_layout(
        title='Resultado de aplicacion de PCA',
        xaxis_title='Componente 1',
        yaxis_title='Componente 2',
        showlegend=True
    )

    # Convertir los datos del gráfico a formato JSON compatible
    plot_data = json.loads(fig.to_json())
    return jsonify(plot_data)


@app.route('/pca_and_clustering')
def pca_and_clustering():
    # Aplicar PCA para reducir la dimensionalidad a 2 componentes
    pca = PCA(n_components=2)
    wine_sintarget_scaled = wine_df.drop(columns=['target'])
    reduced_data = pca.fit_transform(wine_sintarget_scaled)

    # Realizar clustering utilizando K-means
    kmeans = KMeans(n_clusters=3, random_state=42, n_init='auto')
    labels = kmeans.fit_predict(reduced_data)

    # Crear un DataFrame con los datos reducidos y las etiquetas de clustering
    reduced_df = pd.DataFrame(data=reduced_data, columns=['Component 1', 'Component 2'])
    reduced_df['Cluster'] = labels

    # Crear un gráfico de dispersión interactivo con Plotly
    fig = go.Figure()
    for cluster_label in reduced_df['Cluster'].unique():
        fig.add_trace(go.Scatter(
            x=reduced_df.loc[reduced_df['Cluster'] == cluster_label, 'Component 1'],
            y=reduced_df.loc[reduced_df['Cluster'] == cluster_label, 'Component 2'],
            mode='markers',
            name=f'Cluster {cluster_label}'
        ))
    fig.update_layout(
        title='Aplicacion de PCA - Clustering',
        xaxis_title='Componente 1',
        yaxis_title='Componente 2',
        showlegend=True
    )

    # Convertir los datos del gráfico a formato JSON compatible
    plot_data = fig.to_json()
    return jsonify(plot_data)


@app.route('/clustering_and_pca')
def clustering_and_pca():
    # Realizar clustering utilizando K-means
    kmeans = KMeans(n_clusters=3, random_state=42, n_init='auto')
    wine_sintarget_scaled = wine_df.drop(columns=['target'])
    labels = kmeans.fit_predict(wine_sintarget_scaled)

    # Aplicar PCA para reducir la dimensionalidad a 2 componentes
    pca = PCA(n_components=2)
    reduced_data = pca.fit_transform(wine_sintarget_scaled)

    # Crear un DataFrame con los datos reducidos y las etiquetas de clustering
    reduced_df = pd.DataFrame(data=reduced_data, columns=['Component 1', 'Component 2'])
    reduced_df['Cluster'] = labels

    # Crear un gráfico de dispersión interactivo con Plotly
    fig = go.Figure()
    for cluster_label in reduced_df['Cluster'].unique():
        fig.add_trace(go.Scatter(
            x=reduced_df.loc[reduced_df['Cluster'] == cluster_label, 'Component 1'],
            y=reduced_df.loc[reduced_df['Cluster'] == cluster_label, 'Component 2'],
            mode='markers',
            name=f'Cluster {cluster_label}'
        ))
    fig.update_layout(
        title='Aplicacion de Clustering - PCA',
        xaxis_title='Componente 1',
        yaxis_title='Componente 2',
        showlegend=True
    )

    # Convertir los datos del gráfico a formato JSON compatible
    plot_data = fig.to_json()
    return jsonify(plot_data)


########################################## TSNE

@app.route('/tsne_plot')
def tsne_plot():
    # Aplicar t-SNE para reducir la dimensionalidad a 2 componentes
    tsne = TSNE(n_components=2, random_state=42)
    wine_sintarget_scaled = wine_df.drop(columns=['target'])
    reduced_data = tsne.fit_transform(wine_sintarget_scaled)

    # Crear un DataFrame con los datos reducidos
    reduced_df = pd.DataFrame(data=reduced_data, columns=['Component 1', 'Component 2'])
    reduced_df['target'] = wine_df['target']

    # Crear un gráfico de dispersión interactivo con Plotly
    fig = go.Figure()
    for target_label in reduced_df['target'].unique():
        fig.add_trace(go.Scatter(
            x=reduced_df.loc[reduced_df['target'] == target_label, 'Component 1'],
            y=reduced_df.loc[reduced_df['target'] == target_label, 'Component 2'],
            mode='markers',
            name=f'Clase {target_label}'
        ))
    fig.update_layout(
        title='Resultado de aplicacion de t-SNE',
        xaxis_title='Componente 1',
        yaxis_title='Componente 2',
        showlegend=True
    )

    # Convertir los datos del gráfico a formato JSON compatible
    plot_data = json.loads(fig.to_json())
    return jsonify(plot_data)

@app.route('/clustering_and_tsne')
def clustering_and_tsne():
    # Realizar clustering utilizando K-means
    kmeans = KMeans(n_clusters=3, random_state=42, n_init='auto')
    wine_sintarget_scaled = wine_df.drop(columns=['target'])
    wine_sintarget_scaled['Cluster'] = kmeans.fit_predict(wine_sintarget_scaled)

    # Aplicar t-SNE para reducir la dimensionalidad a 2 componentes
    tsne = TSNE(n_components=2, random_state=42)
    reduced_data = tsne.fit_transform(wine_sintarget_scaled)

    # Crear un DataFrame con los datos reducidos y las etiquetas de clustering
    reduced_df = pd.DataFrame(data=reduced_data, columns=['Component 1', 'Component 2'])
    reduced_df['Cluster'] = wine_sintarget_scaled['Cluster']

    # Crear un gráfico de dispersión interactivo con Plotly
    fig = go.Figure()
    for cluster_label in reduced_df['Cluster'].unique():
        fig.add_trace(go.Scatter(
            x=reduced_df.loc[reduced_df['Cluster'] == cluster_label, 'Component 1'],
            y=reduced_df.loc[reduced_df['Cluster'] == cluster_label, 'Component 2'],
            mode='markers',
            name=f'Cluster {cluster_label}'
        ))
    fig.update_layout(
        title='Aplicacion de Clustering - t-SNE',
        xaxis_title='Componente 1',
        yaxis_title='Componente 2',
        showlegend=True
    )

    # Convertir los datos del gráfico a formato JSON compatible
    plot_data = fig.to_json()
    return jsonify(plot_data)

@app.route('/tsne_and_clustering')
def tsne_and_clustering():
    # Aplicar t-SNE para reducir la dimensionalidad a 2 componentes
    tsne = TSNE(n_components=2, random_state=42)
    wine_sintarget_scaled = wine_df.drop(columns=['target'])
    reduced_data = tsne.fit_transform(wine_sintarget_scaled)

    # Realizar clustering utilizando K-means
    kmeans = KMeans(n_clusters=3, random_state=42, n_init='auto')
    labels = kmeans.fit_predict(reduced_data)

    # Crear un DataFrame con los datos reducidos y las etiquetas de clustering
    reduced_df = pd.DataFrame(data=reduced_data, columns=['Component 1', 'Component 2'])
    reduced_df['Cluster'] = labels

    # Crear un gráfico de dispersión interactivo con Plotly
    fig = go.Figure()
    for cluster_label in reduced_df['Cluster'].unique():
        fig.add_trace(go.Scatter(
            x=reduced_df.loc[reduced_df['Cluster'] == cluster_label, 'Component 1'],
            y=reduced_df.loc[reduced_df['Cluster'] == cluster_label, 'Component 2'],
            mode='markers',
            name=f'Cluster {cluster_label}'
        ))
    fig.update_layout(
        title='Aplicacion de t-SNE - Clustering',
        xaxis_title='Componente 1',
        yaxis_title='Componente 2',
        showlegend=True
    )

    # Convertir los datos del gráfico a formato JSON compatible
    plot_data = fig.to_json()
    return jsonify(plot_data)


########################################## LDA

@app.route('/lda_plot')
def lda_plot():
    # Aplicar LDA para reducir la dimensionalidad a 2 componentes
    lda = LinearDiscriminantAnalysis(n_components=2)
    wine_sintarget_scaled = wine_df.drop(columns=['target'])
    reduced_data = lda.fit_transform(wine_sintarget_scaled, wine_df['target'])

    # Crear un DataFrame con los datos reducidos
    reduced_df = pd.DataFrame(data=reduced_data, columns=['Component 1', 'Component 2'])
    reduced_df['target'] = wine_df['target']

    # Crear un gráfico de dispersión interactivo con Plotly
    fig = go.Figure()
    for target_label in reduced_df['target'].unique():
        fig.add_trace(go.Scatter(
            x=reduced_df.loc[reduced_df['target'] == target_label, 'Component 1'],
            y=reduced_df.loc[reduced_df['target'] == target_label, 'Component 2'],
            mode='markers',
            name=f'Clase {target_label}'
        ))
    fig.update_layout(
        title='Resultado de aplicacion de LDA',
        xaxis_title='Componente 1',
        yaxis_title='Componente 2',
        showlegend=True
    )

    # Convertir los datos del gráfico a formato JSON compatible
    plot_data = json.loads(fig.to_json())
    return jsonify(plot_data)

@app.route('/lda_and_clustering')
def lda_and_clustering():
    # Aplicar LDA para reducir la dimensionalidad a 2 componentes
    lda = LinearDiscriminantAnalysis(n_components=2)
    wine_sintarget_scaled = wine_df.drop(columns=['target'])
    reduced_data = lda.fit_transform(wine_sintarget_scaled, wine_df['target'])

    # Realizar clustering utilizando K-means
    kmeans = KMeans(n_clusters=3, random_state=42, n_init='auto')
    labels = kmeans.fit_predict(reduced_data)

    # Crear un DataFrame con los datos reducidos y las etiquetas de clustering
    reduced_df = pd.DataFrame(data=reduced_data, columns=['Component 1', 'Component 2'])
    reduced_df['Cluster'] = labels

    # Crear un gráfico de dispersión interactivo con Plotly
    fig = go.Figure()
    for cluster_label in reduced_df['Cluster'].unique():
        fig.add_trace(go.Scatter(
            x=reduced_df.loc[reduced_df['Cluster'] == cluster_label, 'Component 1'],
            y=reduced_df.loc[reduced_df['Cluster'] == cluster_label, 'Component 2'],
            mode='markers',
            name=f'Cluster {cluster_label}'
        ))
    fig.update_layout(
        title='Aplicacion de LDA - Clustering',
        xaxis_title='Componente 1',
        yaxis_title='Componente 2',
        showlegend=True
    )

    # Convertir los datos del gráfico a formato JSON compatible
    plot_data = fig.to_json()
    return jsonify(plot_data)


@app.route('/clustering_and_lda')
def clustering_and_lda():
    # Realizar clustering utilizando K-means
    kmeans = KMeans(n_clusters=3, random_state=42, n_init='auto')
    wine_sintarget_scaled = wine_df.drop(columns=['target'])
    wine_sintarget_scaled['Cluster'] = kmeans.fit_predict(wine_sintarget_scaled)

    # Aplicar LDA para reducir la dimensionalidad a 2 componentes
    lda = LinearDiscriminantAnalysis(n_components=2)
    reduced_data = lda.fit_transform(wine_sintarget_scaled, wine_df['target'])

    # Crear un DataFrame con los datos reducidos y las etiquetas de clustering
    reduced_df = pd.DataFrame(data=reduced_data, columns=['Component 1', 'Component 2'])
    reduced_df['Cluster'] = wine_sintarget_scaled['Cluster']

    # Crear un gráfico de dispersión interactivo con Plotly
    fig = go.Figure()
    for cluster_label in reduced_df['Cluster'].unique():
        fig.add_trace(go.Scatter(
            x=reduced_df.loc[reduced_df['Cluster'] == cluster_label, 'Component 1'],
            y=reduced_df.loc[reduced_df['Cluster'] == cluster_label, 'Component 2'],
            mode='markers',
            name=f'Cluster {cluster_label}'
        ))

    fig.update_layout(
        title='Aplicacion de Clustering - LDA',
        xaxis_title='Componente 1',
        yaxis_title='Componente 2',
        showlegend=True
    )

    # Convertir los datos del gráfico a formato JSON compatible
    plot_data = fig.to_json()
    return jsonify(plot_data)


########################################## ISOMAP

@app.route('/isomap_plot')
def isomap_plot():
    # Aplicar Isomap para reducir la dimensionalidad a 2 componentes
    isomap = Isomap(n_components=2, n_neighbors=10)
    wine_sintarget = wine_df.drop(columns=['target'])
    reduced_data = isomap.fit_transform(wine_sintarget)

    # Crear un DataFrame con los datos reducidos
    reduced_df = pd.DataFrame(data=reduced_data, columns=['Component 1', 'Component 2'])
    reduced_df['target'] = wine_df['target']

    # Crear un gráfico de dispersión interactivo con Plotly
    fig = go.Figure()
    for target_label in reduced_df['target'].unique():
        fig.add_trace(go.Scatter(
            x=reduced_df.loc[reduced_df['target'] == target_label, 'Component 1'],
            y=reduced_df.loc[reduced_df['target'] == target_label, 'Component 2'],
            mode='markers',
            name=f'Clase {target_label}'
        ))

    fig.update_layout(
        title='Resultado de aplicacion de ISOMAP',
        xaxis_title='Componente 1',
        yaxis_title='Componente 2',
        showlegend=True
    )

    # Convertir los datos del gráfico a formato JSON compatible
    plot_data = json.loads(fig.to_json())
    return jsonify(plot_data)

if __name__ == '__main__':
   app.run(debug=True)