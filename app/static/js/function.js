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
    
    document.getElementById('pca_clustering_plot').style.display = 'none';
    document.getElementById('clustering_pca_plot').style.display = 'none';
    
    // Recorrer los checkboxes y mostrar las gráficas seleccionadas
    if (checkboxResultado.checked) {
        // Cargar y mostrar la gráfica PCA
        document.getElementById('pca_container').style.display = 'block';
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
            var updatedData = data.data.map(trace => ({ ...trace, mode: 'markers', marker: { color: 'black' } }));
            //Plotly.newPlot('pca_plot', data.data, data.layout);
            Plotly.newPlot('pca_plot', updatedData, data.layout);
            // Añadir un evento de selección para el gráfico PCA
            document.getElementById('pca_plot').on('plotly_selected', (eventData) => {
                var selectedPoints = eventData.points;
                var selectedIndices = selectedPoints.map(point => point.pointIndex);
                updateTSNEPlot(selectedIndices);
                updateLDAPlot(selectedIndices);
                updateISOMAPPlot(selectedIndices);
            });
        });
}

// Función para cargar el gráfico PCA y Clustering
function loadPCAAndClusteringPlot() {
    fetch('/pca_and_clustering')
        .then(response => response.json())
        .then(data => {
            Plotly.newPlot('pca_clustering_plot', JSON.parse(data));
        });
}

// Función para cargar el gráfico Clustering y PCA
function loadClusteringAndPCAPlot() {
    fetch('/clustering_and_pca')
        .then(response => response.json())
        .then(data => {
            Plotly.newPlot('clustering_pca_plot', JSON.parse(data));
        });
}

// Función para cargar el gráfico t-SNE
function loadTSNEPlot() {
    fetch('/tsne_plot')
        .then(response => response.json())
        .then(data => {
            // Eliminar los colores de los puntos y establecer marcadores negros
            var updatedData = data.data.map(trace => ({ ...trace, mode: 'markers', marker: { color: 'black' } }));
            Plotly.newPlot('tsne_plot', updatedData, data.layout);
            //Plotly.newPlot('tsne_plot', data.data, data.layout);
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

// Función para cargar el gráfico LDA
function loadLDAPlot() {
    fetch('/lda_plot')
        .then(response => response.json())
        .then(data => {
            // Eliminar los colores de los puntos y establecer marcadores negros
            var updatedData = data.data.map(trace => ({ ...trace, mode: 'markers', marker: { color: 'black' } }));
            Plotly.newPlot('lda_plot', updatedData, data.layout);
            //Plotly.newPlot('tsne_plot', data.data, data.layout);
            document.getElementById('lda_plot').on('plotly_selected', (eventData) => {
                var selectedPoints = eventData.points;
                var selectedIndices = selectedPoints.map(point => point.pointIndex);
                updatePCAPlot(selectedIndices);
                updateTSNEPlot(selectedIndices);
                updateISOMAPPlot(selectedIndices);
            });
        });
}
// Función para cargar el gráfico de Isomap
function loadIsomapPlot() {
    fetch('/isomap_plot')
        .then(response => response.json())
        .then(data => {
            // Eliminar los colores de los puntos y establecer marcadores negros
            var updatedData = data.data.map(trace => ({ ...trace, mode: 'markers', marker: { color: 'black' } }));
            Plotly.newPlot('isomap_plot', updatedData, data.layout);
            document.getElementById('isomap_plot').on('plotly_selected', (eventData) => {
                var selectedPoints = eventData.points;
                var selectedIndices = selectedPoints.map(point => point.pointIndex);
                updatePCAPlot(selectedIndices);
                updateTSNEPlot(selectedIndices);
                updateLDAPlot(selectedIndices);
            });
        });
}


// Actualizar el gráfico PCA con los puntos seleccionados en el gráfico t-SNE
function updatePCAPlot(selectedIndices) {
    Plotly.restyle('pca_plot', {selectedpoints: selectedIndices});
}

// Actualizar el gráfico t-SNE con los puntos seleccionados en el gráfico PCA
function updateTSNEPlot(selectedIndices) {
    Plotly.restyle('tsne_plot', {selectedpoints: selectedIndices});
}

// Actualizar el gráfico LDA con los puntos seleccionados en los otros gráficos
function updateLDAPlot(selectedIndices) {
    Plotly.restyle('lda_plot', { selectedpoints: selectedIndices });
}

// Actualizar el gráfico Isomap con los puntos seleccionados en los otros gráficos
function updateISOMAPPlot(selectedIndices) {
    Plotly.restyle('isomap_plot', { selectedpoints: selectedIndices });
}


//Tippy ventanas emergentes
document.querySelectorAll('[data-tippy-content]').forEach(x => {
    x.setAttribute('data-tippy-content', i18n.__(x.getAttribute('data-tippy-content')));
    tippy(x, { theme: 'manaflux' });
   });


// Cargar ambos gráficos al cargar la página
window.onload = function() {
    loadPCAPlot();
    loadPCAAndClusteringPlot();
    loadClusteringAndPCAPlot();
    loadTSNEPlot();
    loadLDAPlot();
    loadIsomapPlot();
    loadCorrelationMatrix();
    mostrarTecnicasRD(); // Llamar a la función para cargar las técnicas RD
    mostrarPCA();
};



document.addEventListener("DOMContentLoaded", function() {
    document.getElementById('checkAllButton').addEventListener('click', function(e) {
        e.preventDefault();
        checkAll();
    });
    document.getElementById('desmarcar').addEventListener('click', function(e) {
        e.preventDefault();
        uncheckAll();
    });
});

function checkAll() {
    document.querySelectorAll('#atributos input[type=checkbox]').forEach(function(checkElement) {
        checkElement.checked = true;
    });
}

function uncheckAll() {
    document.querySelectorAll('#atributos input[type=checkbox]').forEach(function(checkElement) {
        checkElement.checked = false;
    });
}