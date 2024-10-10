const express = require('express');
const app = express();

app.post('/start', (req, res) => {
  // Start script ka code yahaan likhein
  console.log('Script started');
  res.send('Script started');
});

app.post('/stop', (req, res) => {
  // Stop script ka code yahaan likhein
  console.log('Script stopped');
  res.send('Script stopped');
});

app.listen(3000, () => {
  console.log('Server running on port 3000');
});
