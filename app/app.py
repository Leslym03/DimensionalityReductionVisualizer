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

app = Flask(__name__)

# Cargar el conjunto de datos wine de scikit-learn
data = load_wine()
wine_df = pd.DataFrame(data.data, columns=data.feature_names)
wine_df['target'] = data.target

@app.route('/')
def index():
   return render_template('index.html')

'''
@app.route('/')
def index():
   img_path = create_correlation_matrix()
   return render_template('index.html', img_path=img_path)

def create_correlation_matrix():
    # Calcular la matriz de correlación
    correlation_matrix = wine_df.corr()

    # Crear una figura de Seaborn con la matriz de correlación
    sns.set(font_scale=1.2)
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(correlation_matrix, annot=False,square=True, cmap='Blues', linewidths=0.5, ax=ax)
    
    # Guardar la figura como una imagen en el servidor
    img_path = 'static/correlation_matrix.png'
    plt.savefig(img_path, bbox_inches='tight')
    plt.close()

    return img_path
'''

@app.route('/correlation_matrix')
def correlation_matrix_json():
    # Calcular la matriz de correlación
    correlation_matrix = wine_df.corr()

    # Convertir la matriz de correlación a formato JSON compatible
    correlation_matrix_json = correlation_matrix.to_json(orient='split')

    return jsonify(correlation_matrix_json)




## TECNICAS RD




@app.route('/pca_plot')
def pca_plot():
    # Aplicar PCA para reducir la dimensionalidad a 2 componentes principales
    pca = PCA(n_components=2)
    wine_sintarget = wine_df.drop(columns=['target'])
    reduced_data = pca.fit_transform(wine_sintarget)

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
    wine_sintarget = wine_df.drop(columns=['target'])
    reduced_data = pca.fit_transform(wine_sintarget)

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
    wine_sintarget = wine_df.drop(columns=['target'])
    labels = kmeans.fit_predict(wine_sintarget)

    # Aplicar PCA para reducir la dimensionalidad a 2 componentes
    pca = PCA(n_components=2)
    reduced_data = pca.fit_transform(wine_sintarget)

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





@app.route('/tsne_plot')
def tsne_plot():
    # Aplicar t-SNE para reducir la dimensionalidad a 2 componentes
    tsne = TSNE(n_components=2, random_state=42)
    wine_sintarget = wine_df.drop(columns=['target'])
    reduced_data = tsne.fit_transform(wine_sintarget)

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
        #title='t-SNE - Wine Data',
        xaxis_title='Componente 1',
        yaxis_title='Componente 2',
        showlegend=True
    )

    # Convertir los datos del gráfico a formato JSON compatible
    plot_data = json.loads(fig.to_json())
    return jsonify(plot_data)

@app.route('/lda_plot')
def lda_plot():
    # Aplicar LDA para reducir la dimensionalidad a 2 componentes
    lda = LinearDiscriminantAnalysis(n_components=2)
    wine_sintarget = wine_df.drop(columns=['target'])
    reduced_data = lda.fit_transform(wine_sintarget, wine_df['target'])

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
        xaxis_title='Componente 1',
        yaxis_title='Componente 2',
        showlegend=True
    )

    # Convertir los datos del gráfico a formato JSON compatible
    plot_data = json.loads(fig.to_json())
    return jsonify(plot_data)

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
        xaxis_title='Componente 1',
        yaxis_title='Componente 2',
        showlegend=True
    )

    # Convertir los datos del gráfico a formato JSON compatible
    plot_data = json.loads(fig.to_json())
    return jsonify(plot_data)

if __name__ == '__main__':
   app.run(debug=True)