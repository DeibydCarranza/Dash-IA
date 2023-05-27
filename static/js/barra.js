document.addEventListener("DOMContentLoaded", function() {
    const body = document.querySelector('body'),
          sidebar = body.querySelector('nav'),
          toggle = body.querySelector(".toggle"),
          searchBtn = body.querySelector(".search-box"),
          modeSwitch = body.querySelector(".toggle-switch"),
          modeText = document.querySelector(".mode-text"),
          header = body.querySelector("header");
  
    toggle.addEventListener("click", () => {
      sidebar.classList.toggle("close");
    });
  
    searchBtn.addEventListener("click", () => {
      sidebar.classList.remove("close");
    });
  
    modeSwitch.addEventListener("click", () => {
      body.classList.toggle("dark");
      if (body.classList.contains("dark")) {
        modeText.innerText = "Light mode";
        if (header) { 
          header.classList.add("dark");
        }
      } else {
        modeText.innerText = "Dark mode";
        if (header) {
          header.classList.remove("dark");
        }
      }
      const paragraphs = document.querySelectorAll('p');
      const h1s = document.querySelectorAll('h1');
      const h2s = document.querySelectorAll('h2');
      const h3s = document.querySelectorAll('h3');
      paragraphs.forEach(p => p.classList.toggle('dark'));
      h1s.forEach(h1 => h1.classList.toggle('dark'));
      h2s.forEach(h2 => h2.classList.toggle('dark'));
      h3s.forEach(h3 => h3.classList.toggle('dark'));
      const contentContainer = document.querySelector('.content-container');
      contentContainer.classList.toggle('dark');
    });
  });