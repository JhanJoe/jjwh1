document.addEventListener('DOMContentLoaded', function() {
  const header = document.createElement('header');
  const navbar = document.createElement('div');
  navbar.className = 'navbar';
  const titleSpan = document.createElement('span');
  titleSpan.className = 'title';
  titleSpan.textContent = 'My Website';
  navbar.appendChild(titleSpan);
  const desktopMenu = document.createElement('ul');
  desktopMenu.className = 'desktop-menu';
  ['Item 1', 'Item 2', 'Item 3', 'Item 4'].forEach(text => {
      const li = document.createElement('li');
      li.textContent = text;
      desktopMenu.appendChild(li);
  });
  navbar.appendChild(desktopMenu);
  const burgerDiv = document.createElement('div');
  burgerDiv.id = 'burger';
  const burgerImg = document.createElement('img');
  burgerImg.src = 'burger_menu.svg';
  burgerImg.width = 30;
  burgerImg.height = 30;
  burgerImg.className = 'mobile-menu';
  burgerImg.onclick = togglemenu;
  burgerDiv.appendChild(burgerImg);
  navbar.appendChild(burgerDiv);
  const popupMenu = document.createElement('div');
  popupMenu.className = 'popup-menu';
  const popupContent = document.createElement('div');
  popupContent.className = 'popup-content';
  const closeBtn = document.createElement('span');
  closeBtn.className = 'close-btn';
  closeBtn.textContent = '×';
  popupContent.appendChild(closeBtn);
  const popupList = document.createElement('ul');
  ['Item 1', 'Item 2', 'Item 3', 'Item 4'].forEach(text => {
      const li = document.createElement('li');
      li.textContent = text;
      popupList.appendChild(li);
  });
  popupContent.appendChild(popupList);
  popupMenu.appendChild(popupContent);
  navbar.appendChild(popupMenu);
  header.appendChild(navbar);
  document.body.appendChild(header);
  const welcomeDiv = document.createElement('div');
  welcomeDiv.className = 'welcome';
  welcomeDiv.textContent = 'Welcome to MyHome';
  document.body.appendChild(welcomeDiv);
  const contentDiv = document.createElement('div');
  contentDiv.className = 'content';
  document.body.appendChild(contentDiv);
  const content2Div = document.createElement('div');
  content2Div.className = 'content2';
  document.body.appendChild(content2Div);

  closeBtn.addEventListener('click', function() {
      popupMenu.style.display = 'none';
  });

  function togglemenu() {
      var popupMenu = document.querySelector('.popup-menu');
      popupMenu.style.display = popupMenu.style.display === 'block' ? 'none' : 'block';
  }

  function getData() {
      fetch("https://padax.github.io/taipei-day-trip-resources/taipei-attractions-assignment-1")
      .then(response => {
          if (!response.ok) throw new Error("Network response was not ok " + response.statusText);
          return response.json();
      })
      .then(data => {
          const attractions = data.data.results;
          populateContent(attractions);
      })
      .catch(error => {
          console.error("Error fetching data: ", error);
          const results = document.getElementById("results");
          if (results) results.innerHTML = "<p>Error loading data! " + error.message + "</p>";
      });
  }

  function populateContent(attractions) {
      const contentDiv = document.querySelector('.content');
      const content2Div = document.querySelector('.content2');

      attractions.slice(0, 3).forEach((attraction, index) => {
          const imageUrl = attraction.filelist.split("https://")[1]?.split(" ")[0];
          contentDiv.innerHTML += `
          <div class="smallbox">
              <img src="https://${imageUrl}" class="smallboxpic">
              <div class="smallboxword">${attraction.stitle}</div>
          </div>`;
      });

      attractions.slice(3, 13).forEach((attraction, index) => {
          const imageUrl = attraction.filelist.split("https://")[1]?.split(" ")[0];
          const boxClass = index % 5 === 0 ? 'largebox' : 'mediumbox';
          content2Div.innerHTML += `
          <div class="${boxClass}">
              <img src="https://${imageUrl}" class="boxpic">
              <div class="overlay">
                  <div class="text">${attraction.stitle}</div>
              </div>
              <img src="heart.svg" class="heart">
          </div>`;
      });
  }

  getData();
});
