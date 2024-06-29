
const express = require('express');
const app = express();
const bodyParser = require('body-parser');
const Netconf = require('node-netconf').Netconf;

app.use(bodyParser.json());

app.post('/api/configure', (req, res) => {
  const ssid = req.body.ssid;
  const password = req.body.password;

  const configCommands = [
    `wireless ssid ${ssid}`,
    `authentication open`,
    `authentication key-management wpa`,
    `wpa-psk ascii ${password}`
  ];

  const connection = new Netconf({
    host: '10.1.44.105',
    port: 22,
    username: 'admin',
    password: 'MFUschl123'
  });

  connection.on('rpc-reply', (xml) => {
    console.log('Configuration successful:', xml);
    // Handle success response as needed
    connection.end();
    res.json({ message: 'WLAN SSID configured successfully' });
  });

  connection.on('error', (error) => {
    console.error('Configuration failed:', error);
    // Handle error as needed
    connection.end();
    res.status(500).json({ error: 'Failed to configure WLAN SSID' });
  });

  connection.connect(() => {
    connection.rpc(configCommands.join('\n'));
  });
});

app.listen(3000, () => {
  console.log('Server running on port 3000');
});
