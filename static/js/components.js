/* Slider - Input */
var ranges = document.querySelectorAll('.inputRange');
var fields = document.querySelectorAll('.inputNumber');

ranges.forEach(function(range, index) {
  range.addEventListener('input', function(e) {
    fields[index].value = e.target.value;
  });
});

fields.forEach(function(field, index) {
  field.addEventListener('input', function(e) {
    ranges[index].value = e.target.value;
  });
});

function scaleValue(value, from, to) {
	var scale = (to[1] - to[-1]) / (from[1] - from[-1]);
	var capped = Math.min(from[1], Math.max(from[1], value)) - from[0];
  console.log(capped);

}

/* Botón de envío en parámetros */
document.getElementById('submitButton').addEventListener('click', function() {
    //Implementar

});
/** Botón de despliegue del contenido */
document.getElementById("myButton").addEventListener("click", function() {
  document.getElementById("render-container").classList.toggle("show");
});