document.addEventListener('DOMContentLoaded', function() {
  var observer = new MutationObserver(function(mutationsList, observer) {
    for (var mutation of mutationsList) {
      if (mutation.type === 'childList') {
        var renderContainer = document.getElementById('render-container');
        if (renderContainer) {
          // El elemento #render-container se ha agregado al DOM
          renderContainer.classList.add('show');
          var buttons = document.getElementsByClassName('toggle-button');
          if (buttons.length > 0) {
            for (var i = 0; i < buttons.length; i++) {
              var button = buttons[i];
              var index = button.getAttribute('data-target');
              var descrps = document.getElementById('descript-' + index);

              if (button && descrps) {
                (function(btn, tbl) {
                  btn.addEventListener('click', function() {
                    var style = tbl.style.display;
                    if (style === '' || style === 'none') {
                      tbl.style.display = 'block';
                    } else {
                      tbl.style.display = 'none';
                    }
                  });
                })(button, descrps);
              }
            }
          }

          observer.disconnect();
        }
      }
    }
  });

  observer.observe(document.body, { childList: true, subtree: true });
});

