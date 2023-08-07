// selecionar data 
function initSelectDatasetButton() {
    const selectDatasetButton = document.getElementById('select-dataset-button');
    const datasetSelect = document.getElementById('dataset-select');
  
    if (selectDatasetButton && datasetSelect) {
      selectDatasetButton.addEventListener('click', function() {
        var selectedDataset = datasetSelect.value;
        fetch('/select_dataset/' + selectedDataset)
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert('Se cargo la data correctamente.');
                    updateDataInFrontend(data.selected_data);
                } else {
                    alert('Error al seleccionar el conjunto de datos.');
                }
            })
      });
    }
  }
  
  // Llama a la función para inicializar el botón y la selección de dataset cuando se cargue la página
  document.addEventListener('DOMContentLoaded', initSelectDatasetButton);
  
  // Función para cargar la matriz de correlación
  function loadCorrelationMatrix() {
      fetch('/correlation_matrix')
          .then(response => response.json())
          .then(data => {
              // Convertir el JSON en un objeto JavaScript
              var correlationMatrixData = JSON.parse(data);
  
              // Crear un gráfico de heatmap con Plotly
              Plotly.newPlot('correlation_matrix', [{
                  type: 'heatmap',
                  z: correlationMatrixData.data,
                  x: correlationMatrixData.columns,
                  y: correlationMatrixData.index,
                  colorscale: 'Viridis'
              }]);
          });
  }
  
  //Funcion para aplicar las tecnicas de 
  function mostrarGraficas() {
      const contenedor = document.getElementById("contenedorGraficos");
  
      // Obtener los checkboxes seleccionados
      const checkboxPCA = document.getElementById('checkbox1');
      const checkboxTSNE = document.getElementById('checkbox2');
      const checkboxLDA = document.getElementById('checkbox3');
      const checkboxISOMAP = document.getElementById('checkbox4');
      
      // Limpiar el contenido anterior de graficasDiv
      document.getElementById('pca_container').style.display = 'none';
      document.getElementById('tsne_container').style.display = 'none';
      document.getElementById('lda_container').style.display = 'none';
      document.getElementById('isomap_container').style.display = 'none';
      
      // Recorrer los checkboxes y mostrar las gráficas seleccionadas
      if (checkboxPCA.checked) {
          // Cargar y mostrar la gráfica PCA
          document.getElementById('pca_container').style.display = 'block';
          loadPCAPlot();
      }
      
      if (checkboxTSNE.checked) {
          // Cargar y mostrar la gráfica t-SNE
          document.getElementById('tsne_container').style.display = 'block';
          loadTSNEPlot();
      }
      if (checkboxLDA.checked) {
          // Cargar y mostrar la gráfica LDA
          document.getElementById('lda_container').style.display = 'block';
          loadLDAPlot();
      }
      if (checkboxISOMAP.checked) {
          // Cargar y mostrar la gráfica ISOMAP
          document.getElementById('isomap_container').style.display = 'block';
          loadIsomapPlot();
      }
  }
  
  
  //Funcion para mostrar resutaldo, clustering RD
  function mostrarPCA() {
      // Obtener los checkboxes seleccionados
      const checkboxResultado = document.getElementById('PCA-btncheck1');
      const checkboxDRClustering = document.getElementById('PCA-btncheck2');
      const checkboxClusteringDR = document.getElementById('PCA-btncheck3');
  
      document.getElementById('pca_plot').style.display = 'none';
      document.getElementById('pca_clustering_plot').style.display = 'none';
      document.getElementById('clustering_pca_plot').style.display = 'none';
      
      // Recorrer los checkboxes y mostrar las gráficas seleccionadas
      if (checkboxResultado.checked) {
          // Cargar y mostrar la gráfica PCA
          document.getElementById('pca_plot').style.display = 'block';
          loadPCAPlot();
      }
      
      if (checkboxDRClustering.checked) {
          document.getElementById('pca_clustering_plot').style.display = 'block';
          loadPCAAndClusteringPlot();
      }
      if (checkboxClusteringDR.checked) {
          document.getElementById('clustering_pca_plot').style.display = 'block';
          loadClusteringAndPCAPlot();
      }
  }
  
  
  // Función para cargar el gráfico PCA
  function loadPCAPlot() {
      fetch('/pca_plot')
          .then(response => response.json())
          .then(data => {
              // Eliminar los colores de los puntos y establecer marcadores negros
              //var updatedData = data.data.map(trace => ({ ...trace, mode: 'markers', marker: { color: 'black' } }));
              Plotly.newPlot('pca_plot', data.data, data.layout);
              //Plotly.newPlot('pca_plot', updatedData, data.layout);
              // Añadir un evento de selección para el gráfico PCA
              document.getElementById('pca_plot').on('plotly_selected', (eventData) => {
                  var selectedPoints = eventData.points;
                  var selectedIndices = selectedPoints.map(point => point.pointIndex);
                  updateTSNEPlot(selectedIndices);
                  updateLDAPlot(selectedIndices);
                  updateISOMAPPlot(selectedIndices);
  
                  updateClusteringAndPCAPlot(selectedIndices);
                  updatePCAAndClusteringPlot(selectedIndices);
              });
          });
  }
  
  // Función para cargar el gráfico PCA y Clustering
  function loadPCAAndClusteringPlot() {
      fetch('/pca_and_clustering')
          .then(response => response.json())
          .then(data => {
              Plotly.newPlot('pca_clustering_plot', JSON.parse(data));
              // Añadir un evento de selección para el gráfico PCA
              document.getElementById('pca_clustering_plot').on('plotly_selected', (eventData) => {
                  var selectedPoints = eventData.points;
                  var selectedIndices = selectedPoints.map(point => point.pointIndex);
                  updatePCAPlot(selectedIndices);
                  updateClusteringAndPCAPlot(selectedIndices);
              });
          });
  }
  
  // Función para cargar el gráfico Clustering y PCA
  function loadClusteringAndPCAPlot() {
      fetch('/clustering_and_pca')
          .then(response => response.json())
          .then(data => {
              Plotly.newPlot('clustering_pca_plot', JSON.parse(data));
              // Añadir un evento de selección para el gráfico PCA
              document.getElementById('clustering_pca_plot').on('plotly_selected', (eventData) => {
                  var selectedPoints = eventData.points;
                  var selectedIndices = selectedPoints.map(point => point.pointIndex);
                  updatePCAPlot(selectedIndices);
                  updatePCAAndClusteringPlot(selectedIndices);
              });
          });
  }
  
  //Funcion para mostrar resutaldo, clustering t-SNE
  function mostrarTSNE() {
      // Obtener los checkboxes seleccionados
      const checkboxResultado = document.getElementById('TSNE-btncheck1');
      const checkboxDRClustering = document.getElementById('TSNE-btncheck2');
      const checkboxClusteringDR = document.getElementById('TSNE-btncheck3');
  
      document.getElementById('tsne_plot').style.display = 'none';
      document.getElementById('tsne_clustering_plot').style.display = 'none';
      document.getElementById('clustering_tsne_plot').style.display = 'none';
  
      // Recorrer los checkboxes y mostrar las gráficas seleccionadas
      if (checkboxResultado.checked) {
          // Cargar y mostrar la gráfica t-SNE
          document.getElementById('tsne_plot').style.display = 'block';
          loadTSNEPlot();
      }
  
      if (checkboxDRClustering.checked) {
          document.getElementById('tsne_clustering_plot').style.display = 'block';
          loadTSNEClusteringPlot();
      }
      if (checkboxClusteringDR.checked) {
          document.getElementById('clustering_tsne_plot').style.display = 'block';
          loadClusteringAndTSNEPlot();
      }
  }
  
  // Función para cargar el gráfico t-SNE
  function loadTSNEPlot() {
      fetch('/tsne_plot')
          .then(response => response.json())
          .then(data => {
              // Eliminar los colores de los puntos y establecer marcadores negros
              //var updatedData = data.data.map(trace => ({ ...trace, mode: 'markers', marker: { color: 'black' } }));
              //Plotly.newPlot('tsne_plot', updatedData, data.layout);
              Plotly.newPlot('tsne_plot', data.data, data.layout);
              // Añadir un evento de selección para el gráfico t-SNE
              document.getElementById('tsne_plot').on('plotly_selected', (eventData) => {
                  var selectedPoints = eventData.points;
                  var selectedIndices = selectedPoints.map(point => point.pointIndex);
                  updatePCAPlot(selectedIndices);
                  updateLDAPlot(selectedIndices);
                  updateISOMAPPlot(selectedIndices);
              });
          });
  }
  
  // Función para cargar el gráfico t-SNE y DBSCAN
  function loadTSNEClusteringPlot() {
      fetch('/tsne_and_clustering')
          .then(response => response.json())
          .then(data => {
              Plotly.newPlot('tsne_clustering_plot', JSON.parse(data));
              document.getElementById('tsne_clustering_plot').on('plotly_selected', (eventData) => {
                  var selectedPoints = eventData.points;
                  var selectedIndices = selectedPoints.map(point => point.pointIndex);
                  updateDBSCANPlot(selectedIndices);
              });
          });
  }
  
  // Función para cargar el gráfico DBSCAN y t-SNE
  function loadClusteringAndTSNEPlot() {
      fetch('/clustering_and_tsne')
          .then(response => response.json())
          .then(data => {
              Plotly.newPlot('clustering_tsne_plot', JSON.parse(data));
              document.getElementById('clustering_tsne_plot').on('plotly_selected', (eventData) => {
                  var selectedPoints = eventData.points;
                  var selectedIndices = selectedPoints.map(point => point.pointIndex);
                  updateTSNEPlot(selectedIndices);
              });
          });
  }
  
  // Función para mostrar resutaldo, clustering LDA
  function mostrarLDA() {
      const checkboxResultado = document.getElementById('LDA-btncheck1');
      const checkboxDRClustering = document.getElementById('LDA-btncheck2');
      const checkboxClusteringDR = document.getElementById('LDA-btncheck3');
  
      document.getElementById('lda_plot').style.display = 'none';
      document.getElementById('lda_clustering_plot').style.display = 'none';
      document.getElementById('clustering_lda_plot').style.display = 'none';
  
      if (checkboxResultado.checked) {
          document.getElementById('lda_plot').style.display = 'block';
          loadLDAPlot();
      }
  
      if (checkboxDRClustering.checked) {
          document.getElementById('lda_clustering_plot').style.display = 'block';
          loadLDAClusteringPlot();
      }
      if (checkboxClusteringDR.checked) {
          document.getElementById('clustering_lda_plot').style.display = 'block';
          loadClusteringAndLDAPlot();
      }
  }
  
  // Función para cargar el gráfico LDA
  function loadLDAPlot() {
      fetch('/lda_plot')
          .then(response => response.json())
          .then(data => {
              // Eliminar los colores de los puntos y establecer marcadores negros
              //var updatedData = data.data.map(trace => ({ ...trace, mode: 'markers', marker: { color: 'black' } }));
              //Plotly.newPlot('lda_plot', updatedData, data.layout);
              Plotly.newPlot('lda_plot', data.data, data.layout);
              document.getElementById('lda_plot').on('plotly_selected', (eventData) => {
                  var selectedPoints = eventData.points;
                  var selectedIndices = selectedPoints.map(point => point.pointIndex);
                  updatePCAPlot(selectedIndices);
                  updateTSNEPlot(selectedIndices);
                  updateISOMAPPlot(selectedIndices);
              });
          });
  }
  
  // Función para cargar el gráfico LDA y Clustering
  function loadLDAClusteringPlot() {
      fetch('/lda_and_clustering')
          .then(response => response.json())
          .then(data => {
              Plotly.newPlot('lda_clustering_plot', JSON.parse(data));
              document.getElementById('lda_clustering_plot').on('plotly_selected', (eventData) => {
                  var selectedPoints = eventData.points;
                  var selectedIndices = selectedPoints.map(point => point.pointIndex);
                  updateLDAPlot(selectedIndices);
                  updateClusteringAndLDAPlot(selectedIndices);
              });
          });
  }
  
  // Función para cargar el gráfico Clustering y LDA
  function loadClusteringAndLDAPlot() {
      fetch('/clustering_and_lda')
          .then(response => response.json())
          .then(data => {
              Plotly.newPlot('clustering_lda_plot', JSON.parse(data));
              document.getElementById('clustering_lda_plot').on('plotly_selected', (eventData) => {
                  var selectedPoints = eventData.points;
                  var selectedIndices = selectedPoints.map(point => point.pointIndex);
                  updateLDAPlot(selectedIndices);
                  updateLDAClusteringPlot(selectedIndices);
              });
          });
  }
  
  function mostrarISOMAP() {
      const checkboxResultado = document.getElementById('ISOMAP-btncheck1');
      const checkboxDRClustering = document.getElementById('ISOMAP-btncheck2');
      const checkboxClusteringDR = document.getElementById('ISOMAP-btncheck3');
  
      document.getElementById('isomap_plot').style.display = 'none';
      document.getElementById('isomap_clustering_plot').style.display = 'none';
      document.getElementById('clustering_isomap_plot').style.display = 'none';
  
      if (checkboxResultado.checked) {
          document.getElementById('isomap_plot').style.display = 'block';
          loadIsomapPlot();
      }
  
      if (checkboxDRClustering.checked) {
          document.getElementById('isomap_clustering_plot').style.display = 'block';
          loadIsomapClusteringPlot();
      }
      if (checkboxClusteringDR.checked) {
          document.getElementById('clustering_isomap_plot').style.display = 'block';
          loadClusteringAndIsomapPlot();
      }
  }
  
  // Función para cargar el gráfico de Isomap
  function loadIsomapPlot() {
      fetch('/isomap_plot')
          .then(response => response.json())
          .then(data => {
              // Eliminar los colores de los puntos y establecer marcadores negros
              //var updatedData = data.data.map(trace => ({ ...trace, mode: 'markers', marker: { color: 'black' } }));
              Plotly.newPlot('isomap_plot', data.data, data.layout);
              document.getElementById('isomap_plot').on('plotly_selected', (eventData) => {
                  var selectedPoints = eventData.points;
                  var selectedIndices = selectedPoints.map(point => point.pointIndex);
                  updatePCAPlot(selectedIndices);
                  updateTSNEPlot(selectedIndices);
                  updateLDAPlot(selectedIndices);
              });
          });
  }
  
  // Función para cargar el gráfico Isomap y Clustering
  function loadIsomapClusteringPlot() {
      fetch('/isomap_and_clustering')
          .then(response => response.json())
          .then(data => {
              Plotly.newPlot('isomap_clustering_plot', JSON.parse(data));
              document.getElementById('isomap_clustering_plot').on('plotly_selected', (eventData) => {
                  var selectedPoints = eventData.points;
                  var selectedIndices = selectedPoints.map(point => point.pointIndex);
                  updateIsomapPlot(selectedIndices);
                  updateClusteringAndIsomapPlot(selectedIndices);
              });
          });
  }
  
  // Función para cargar el gráfico Clustering y Isomap
  function loadClusteringAndIsomapPlot() {
      fetch('/clustering_and_isomap')
          .then(response => response.json())
          .then(data => {
              Plotly.newPlot('clustering_isomap_plot', JSON.parse(data));
              document.getElementById('clustering_isomap_plot').on('plotly_selected', (eventData) => {
                  var selectedPoints = eventData.points;
                  var selectedIndices = selectedPoints.map(point => point.pointIndex);
                  updateIsomapPlot(selectedIndices);
                  updateIsomapClusteringPlot(selectedIndices);
              });
          });
  }
  
  
  // Actualizar el gráfico PCA con los puntos seleccionados en el gráfico t-SNE
  function updatePCAPlot(selectedIndices) {
      Plotly.restyle('pca_plot', {selectedpoints: selectedIndices});
  }
  
  function updatePCAAndClusteringPlot(selectedIndices) {
      Plotly.restyle('pca_clustering_plot', {selectedpoints: selectedIndices});
  }
  
  function updateClusteringAndPCAPlot(selectedIndices) {
      Plotly.restyle('clustering_pca_plot', {selectedpoints: selectedIndices});
  }
  
  
  // Actualizar el gráfico t-SNE con los puntos seleccionados en el gráfico PCA
  function updateTSNEPlot(selectedIndices) {
      Plotly.restyle('tsne_plot', {selectedpoints: selectedIndices});
  }
  
  function updateTSNEClusteringPlot(selectedIndices) {
      Plotly.restyle('tsne_clustering_plot', {selectedpoints: selectedIndices});
  }
  
  function updateClusteringAndTSNEPlot(selectedIndices) {
      Plotly.restyle('clustering_tsne_plot', {selectedpoints: selectedIndices});
  }
  
  // Actualizar el gráfico LDA con los puntos seleccionados en los otros gráficos
  function updateLDAPlot(selectedIndices) {
      Plotly.restyle('lda_plot', { selectedpoints: selectedIndices });
  }
  
  function updateLDAClusteringPlot(selectedIndices) {
      Plotly.restyle('lda_clustering_plot', {selectedpoints: selectedIndices});
  }
  
  function updateClusteringAndLDAPlot(selectedIndices) {
      Plotly.restyle('clustering_lda_plot', {selectedpoints: selectedIndices});
  }
  
  // Actualizar el gráfico Isomap con los puntos seleccionados en los otros gráficos
  function updateISOMAPPlot(selectedIndices) {
      Plotly.restyle('isomap_plot', { selectedpoints: selectedIndices });
  }
  
  
  
  
  // Cargar ambos gráficos al cargar la página
  window.onload = function() {
      loadPCAPlot();
      loadPCAAndClusteringPlot();
      loadClusteringAndPCAPlot();
      loadTSNEPlot();
      loadClusteringAndTSNEPlot();
      loadTSNEClusteringPlot();
      loadLDAPlot();
      loadLDAClusteringPlot()
      loadClusteringAndLDAPlot()
      loadIsomapPlot();
      loadClusteringAndIsomapPlot();
      loadIsomapClusteringPlot();
      loadCorrelationMatrix();
      mostrarPCA();
      mostrarLDA();
      mostrarTSNE();
      mostrarISOMAP();
      initSelectDatasetButton();
  };
  
  
  