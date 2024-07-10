// search.js

let athletes = [];

async function fetchAthleteNames() {
    try {
      const response = await fetch('http://127.0.0.1:8000/names');
      if (!response.ok) {
        throw new Error('Network response was not ok.');
      }
      const data = await response.json();
      athletes = data; 
      filterAthletes(); 
    } catch (error) {
      console.error('Error fetching athlete names:', error);
    }
  }
fetchAthleteNames(); 


function filterAthletes() {
    const searchInput = document.getElementById('searchBar').value.trim(); 
    const searchResults = document.getElementById('searchResults');
    searchResults.innerHTML = '';
  
    if (searchInput.length === 0) {
      searchResults.style.display = 'none';
      return;
    }
  
    searchResults.style.display = 'block';
  
    athletes
      .filter(athlete => athlete.name.toLowerCase().includes(searchInput.toLowerCase()))
      .forEach(athlete => {
        const div = document.createElement('div');
        div.className = 'search-result';
        div.textContent = athlete.name; 
        div.onclick = () => selectAthlete(athlete);
        searchResults.appendChild(div);
      });
  }

function selectAthlete(name) {
  console.log(`Selected athlete: ${name}`);
}
