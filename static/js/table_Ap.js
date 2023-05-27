function handleFileUpload() {
    var fileInput = document.querySelector('input[name="csv_file"]');
    var file = fileInput.files[0];

    var reader = new FileReader();

    reader.onload = function(e) {
        var fileContent = e.target.result;

        // Aquí puedes procesar el contenido del archivo, como convertirlo a DataFrame y generar la tabla HTML
        processData(fileContent);
    };

    reader.readAsText(file);
}

function processData(fileContent) {
    // Aquí puedes utilizar la cadena `fileContent` para procesar los datos, como convertirlos a un objeto JSON y generar la tabla HTML

    // Ejemplo de procesamiento: convertir CSV a DataFrame utilizando la biblioteca Papa Parse
    var parsedData = Papa.parse(fileContent, {
        header: true,
        dynamicTyping: true,
        skipEmptyLines: true
    });

    var data = parsedData.data;

    // Crear la tabla HTML
    var tableHtml = '<table>';
    tableHtml += '<tr>';
    Object.keys(data[0]).forEach(function(key) {
        tableHtml += '<th>' + key + '</th>';
    });
    tableHtml += '</tr>';

    data.forEach(function(row) {
        tableHtml += '<tr>';
        Object.values(row).forEach(function(value) {
            tableHtml += '<td>' + value + '</td>';
        });
        tableHtml += '</tr>';
    });

    tableHtml += '</table>';

    // Agregar la tabla al contenedor
    var tableContainer = document.getElementById('output-data-upload');
    tableContainer.innerHTML = tableHtml;
}
