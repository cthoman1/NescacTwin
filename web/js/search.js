let athletes = [];
let selectedAthleteName = ''; 
let selectedAthleteID = ''; 


async function fetchAthleteNames() {
  try {
    const response = await fetch('http://127.0.0.1:3000/athletes'); // Fetch from server endpoint
    if (!response.ok) {
      throw new Error('Network response was not ok.');
    }
    const data = await response.json();
    athletes = data;
    filterAthletes();
  } catch (error) {
    console.error('Error fetching athlete data:', error);
  }
}

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
    .filter(athlete => athlete.name.toLowerCase().includes(searchInput))
    .forEach(athlete => {
      const div = document.createElement('div');
      div.className = 'search-result';

      // Create a span for the school logo
      const schoolLogo = document.createElement('img');
      schoolLogo.className = 'school-logo';
      schoolLogo.src = getSchoolLogoSrc(athlete.school); 
      div.appendChild(schoolLogo);

      // Create a span for the athlete's name
      const nameSpan = document.createElement('span');
      nameSpan.textContent = athlete.name;
      nameSpan.className = 'athlete-name';
      div.appendChild(nameSpan);

      const yearsActiveSpan = document.createElement('span');
      yearsActiveSpan.textContent = athlete.years_active; 
      yearsActiveSpan.className = 'years-active';
      div.appendChild(yearsActiveSpan);

      div.onclick = () => selectAthlete(athlete.name, athlete.athlete_id);

      searchResults.appendChild(div);
    });
}


function selectAthlete(name, athlete_id) {
  selectedAthleteName = name;
  selectedAthleteID = athlete_id;
  console.log(selectedAthleteID);
  searchBar.value = selectedAthleteName; 
  document.getElementById('searchResults').style.display = 'none'; 
  fetchRelevantEvents(selectedAthleteID);
}

async function fetchRelevantEvents(athlete_id) {
  try {
      const response = await fetch(`http://127.0.0.1:3000/relevant_events?athlete_id=${encodeURIComponent(athlete_id)}`);
      if (!response.ok) {
          throw new Error('Network response was not ok.');
      }
      const events = await response.json();
      populateDropdown(events);
  } catch (error) {
      console.error('Error fetching relevant events:', error);
  }
}

function populateDropdown(events) {
  const dropdownMenu = document.getElementById('eventDropdown');
  
  while (dropdownMenu.options.length > 1) {
    dropdownMenu.remove(1);
  }

  events.forEach(event => {
    const option = document.createElement('option');
    option.value = event; 
    option.textContent = event;
    dropdownMenu.appendChild(option);
  });
}


function getSchoolLogoSrc(schoolName) {
  switch (schoolName) {
    case 'Bates':
      return 'images/bates.png';
    case 'Bowdoin':
      return 'images/bowdoin.png';
    case 'Colby':
      return 'images/colby.png';
  }
}

document.getElementById('searchBar').addEventListener('input', () => {
  document.getElementById('eventDropdown').innerHTML = '<option value="">Select an event</option>';
});

