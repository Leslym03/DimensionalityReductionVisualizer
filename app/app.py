from flask import Flask, render_template, jsonify
import pandas as pd
from sklearn.datasets import load_wine
from sklearn.datasets import load_breast_cancer
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
from scipy import stats
import numpy as np

app = Flask(__name__)

# Cargar el conjunto de datos de scikit-learn
data = load_wine()
wine_df = pd.DataFrame(data.data, columns=data.feature_names)
wine_df['target'] = data.target

data = load_breast_cancer()
breast_cancer_df = pd.DataFrame(data.data, columns=data.feature_names)
breast_cancer_df['target'] = data.target

# Global variable to hold the selected data
selected_data = None

# Función para preprocesar los datos
def preprocess_data(df):
    # Manejo de Valores Faltantes: llenar NA/NaN con la media de la columna
    df.fillna(df.mean(), inplace=True)

    # Detección y Manejo de Outliers: eliminar los outliers utilizando la puntuación Z
    z_scores = stats.zscore(df)
    abs_z_scores = np.abs(z_scores)
    filtered_entries = (abs_z_scores < 3).all(axis=1)
    df = df[filtered_entries]

    # Estandarización: transformar los datos a una media de 0 y una desviación estándar de 1
    #scaler = StandardScaler()
    #df_scaled = pd.DataFrame(scaler.fit_transform(df), columns=df.columns)

    return df


def reduction_then_clustering(reduction_method, selected_data):
    X = selected_data.drop(columns=['target'])
    y = selected_data['target']

    # Reduccion de la data
    reduced_data = reduction_method.fit_transform(X, y)
    selected_data = selected_data.drop(columns=['target'])

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
        title='Aplicacion de RD - Clustering',
        xaxis_title='Componente 1',
        yaxis_title='Componente 2',
        showlegend=True,
        legend=dict(x=1, y=1, xanchor='right', yanchor='top'),
        width=500, 
        height=400
    )

    # Convertir los datos del gráfico a formato JSON compatible
    plot_data = fig.to_json()
    return jsonify(plot_data)


def clustering_then_reduction(reduction_method, selected_data):
    # Separar los datos y las etiquetas
    X = selected_data.drop(columns=['target'])
    y = selected_data['target']

    # Realizar clustering utilizando K-means
    kmeans = KMeans(n_clusters=3, random_state=42)
    labels = kmeans.fit_predict(X)  # Aplicar clustering a los datos reducidos


    # Ajustar el método de reducción con los datos y las etiquetas
    reduced_data = reduction_method.fit_transform(X,y)

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
        title='Aplicacion de Clustering - RD',
        xaxis_title='Componente 1',
        yaxis_title='Componente 2',
        showlegend=True,
        legend=dict(x=1, y=1, xanchor='right', yanchor='top'),
        width=500, 
        height=400
    )

    # Convertir los datos del gráfico a formato JSON compatible
    plot_data = fig.to_json()
    return jsonify(plot_data)


@app.route('/')
def index():
   return render_template('index.html')

@app.route('/select_dataset/<string:dataset_name>')
def select_dataset(dataset_name):
    global selected_data
    if dataset_name == 'wine':
        selected_data = preprocess_data(wine_df)
    elif dataset_name == 'breast_cancer':
        selected_data = preprocess_data(breast_cancer_df)
    else:
        return jsonify(error='Dataset not found'), 404

    return jsonify(success=True, selected_data=selected_data.to_dict(orient='records'))


@app.route('/correlation_matrix')
def correlation_matrix_json():
    if selected_data is None:
        return jsonify(error='No dataset selected'), 404

    correlation_matrix = selected_data.corr()
    correlation_matrix_json = correlation_matrix.to_json(orient='split')
    return jsonify(correlation_matrix_json)


@app.route('/pca_plot')
def pca_plot():
    if selected_data is None:
        return jsonify(error='No dataset selected'), 404

    else:
        pca = PCA(n_components=2)
        scaled_data = selected_data.drop(columns=['target'])
        reduced_data = pca.fit_transform(scaled_data)

        # Crear un DataFrame con los datos reducidos
        reduced_df = pd.DataFrame(data=reduced_data, columns=['Component 1', 'Component 2'])
        reduced_df['target'] = selected_data['target']

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
            showlegend=True,
            legend=dict(x=1, y=1, xanchor='right', yanchor='top'),
            width=500, 
            height=400  
        )

        # Convertir los datos del gráfico a formato JSON compatible
        plot_data = json.loads(fig.to_json())
        return jsonify(plot_data)

@app.route('/tsne_plot')
def tsne_plot():
    if selected_data is None:
        return jsonify(error='No dataset selected'), 404

    tsne = TSNE(n_components=2, random_state=42)
    scaled_data = selected_data.drop(columns=['target'])
    reduced_data = tsne.fit_transform(scaled_data)

    # Crear un DataFrame con los datos reducidos
    reduced_df = pd.DataFrame(data=reduced_data, columns=['Component 1', 'Component 2'])
    reduced_df['target'] = selected_data['target']

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
        showlegend=True,
        legend=dict(x=1, y=1, xanchor='right', yanchor='top'),
        width=500, 
        height=400
    )

    # Convertir los datos del gráfico a formato JSON compatible
    plot_data = json.loads(fig.to_json())
    return jsonify(plot_data)

@app.route('/lda_plot')
def lda_plot():
    if selected_data is None:
        return jsonify(error='No dataset selected'), 404

    # Aplicar LDA para reducir la dimensionalidad a 2 componentes
    lda = LinearDiscriminantAnalysis(n_components=2)
    scaled_data = selected_data.drop(columns=['target'])
    reduced_data = lda.fit_transform(scaled_data, selected_data['target'])

    # Crear un DataFrame con los datos reducidos
    reduced_df = pd.DataFrame(data=reduced_data, columns=['Component 1', 'Component 2'])
    reduced_df['target'] = selected_data['target']

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
        showlegend=True,
        legend=dict(x=1, y=1, xanchor='right', yanchor='top'),
        width=500, 
        height=400
    )

    # Convertir los datos del gráfico a formato JSON compatible
    plot_data = json.loads(fig.to_json())
    return jsonify(plot_data)

@app.route('/isomap_plot')
def isomap_plot():
    if selected_data is None:
        return jsonify(error='No dataset selected'), 404

    isomap = Isomap(n_components=2)
    scaled_data = selected_data.drop(columns=['target'])
    reduced_data = isomap.fit_transform(scaled_data)

    # Crear un DataFrame con los datos reducidos
    reduced_df = pd.DataFrame(data=reduced_data, columns=['Component 1', 'Component 2'])
    reduced_df['target'] = selected_data['target']

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
        title='Resultado de aplicacion de Isomap',
        xaxis_title='Componente 1',
        yaxis_title='Componente 2',
        showlegend=True,
        legend=dict(x=1, y=1, xanchor='right', yanchor='top'),
        width=500, 
        height=400
    )

    # Convertir los datos del gráfico a formato JSON compatible
    plot_data = json.loads(fig.to_json())
    return jsonify(plot_data)



@app.route('/pca_and_clustering')
def pca_and_clustering():
    return reduction_then_clustering(PCA(n_components=2), selected_data)

@app.route('/clustering_and_pca')
def clustering_and_pca():
    return clustering_then_reduction(PCA(n_components=2), selected_data)

@app.route('/tsne_and_clustering')
def tsne_and_clustering():
    return reduction_then_clustering(TSNE(n_components=2), selected_data)

@app.route('/clustering_and_tsne')
def clustering_and_tsne():
    return clustering_then_reduction(TSNE(n_components=2), selected_data)

@app.route('/lda_and_clustering')
def lda_and_clustering():
    return reduction_then_clustering(LinearDiscriminantAnalysis(n_components=2), selected_data)

@app.route('/clustering_and_lda')
def clustering_and_lda():
    return clustering_then_reduction(LinearDiscriminantAnalysis(n_components=2), selected_data)

@app.route('/isomap_and_clustering')
def isomap_and_clustering():
    return reduction_then_clustering(Isomap(n_components=2), selected_data)

@app.route('/clustering_and_isomap')
def clustering_and_isomap():
    return clustering_then_reduction(Isomap(n_components=2), selected_data)


if __name__ == '__main__':
   app.run(debug=True)