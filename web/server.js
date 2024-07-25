// server.js

const express = require('express');
const cors = require('cors');
const path = require('path');
const axios = require('axios');

const app = express();
const port = 3000;

app.use(cors());
app.listen(port, () => {
    console.log(`Server is listening on port ${port}`);
});

app.use(express.static(path.join(__dirname)));

app.get('/athletes', async (req, res) => {
    try {
        const response = await axios.get('http://127.0.0.1:8000/athletes');
        res.json(response.data);
    } catch (error) {
        res.status(500).send('Error fetching data');
    }
});

app.get('/events', async (req, res) => {
    try {
        const response = await axios.get('http://127.0.0.1:8000/events');
        res.json(response.data);
    } catch (error) {
        res.status(500).send('Error fetching event data');
    }
});

app.get('/relevant_events', async (req, res) => {
    const athlete_id = req.query.athlete_id; 
    try {
        const response = await axios.get(`http://127.0.0.1:8000/relevant_events?id=${encodeURIComponent(athlete_id)}`);
        res.json(response.data);
    } catch (error) {
        res.status(500).send('Error fetching relevant events');
    }
});

app.get('/compare_trajectory', async (req, res) => {
    const athlete_id = req.query.id1; 
    const id2 = req.query.id2; 
    const first_year = req.query.first_year; 
    const last_year = req.query.last_year; 
    const min_events = req.query.min_events; 
    const recency_bias = req.query.recency_bias; 
    
    try {
        const response = await axios.get(`http://127.0.0.1:8000/compare_trajectory?id1=${encodeURIComponent(athlete_id)}&id2=${encodeURIComponent(id2)}&first_year=${encodeURIComponent(first_year)}&last_year=${encodeURIComponent(last_year)}&min_events=${encodeURIComponent(min_events)}&recency_bias=${encodeURIComponent(recency_bias)}`);
        res.json(response.data);
    } catch (error) {
        console.error('Error fetching compare trajectory:', error);
        res.status(500).send('Error fetching relevant events');
    }
});

app.get('/athlete_trajectory', async (req, res) => {
    const athlete_id = req.query.id1; 
    const id2 = req.query.id2; 
    
    try {
        const response = await axios.get(`http://127.0.0.1:8000/athlete_trajectory?id1=${encodeURIComponent(athlete_id)}&id2=${encodeURIComponent(id2)}`);
        res.json(response.data);
    } catch (error) {
        console.error('Error fetching compare trajectory:', error);
        res.status(500).send('Error fetching athlete trajectory');
    }
});

app.use((req, res) => {
    res.status(404).sendFile(path.join(__dirname, '404.html'));
});

app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'index.html'));
});

