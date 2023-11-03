const express = require('express');
const bodyParser = require('body-parser');
const db = require('./db'); // Import the database controller module
const { logEvents } = require('./logEvent');

const app = express();
const port = process.env.PORT || 3000;

app.use(bodyParser.json());

app.post('/api/send', async (req, res) => {
    logEvents(req.body);
    const number = req.body.number;
    const message = req.body.message;
    const key = req.body.key;
    const devices = req.body.devices;
    const type = req.body.type;
    const prioritize = req.body.prioritize;

    if (!number || !message || !key || !devices || !type || !prioritize) {
        res.status(400).json({ error: 'Invalid request' });
        return;
    }

    if (key !== process.env.API_KEY) {
        res.status(401).json({ error: 'Unauthorized' });
        return;
    }

    try {
        const messageId = await db.insertMessage(number, message, key);
        res.status(201).json({
            'data':{
                'messages': [resolve(result)],
                },
                'error': undef,
                'success': true
            }
        );
    } catch (err) {
        res.status(500).json({
            'data':{
                'messages': [],
                },
            'error': resolve(err),
            'success': false
            });
        }
    });

app.listen(port, () => {
    console.log(`Server is running on port ${port}`);
});
