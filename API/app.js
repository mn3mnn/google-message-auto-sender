const express = require('express');
const bodyParser = require('body-parser');
const db = require('./db'); // Import the database controller module
const logEvents = require('./logEvent');
const path = require('path');
const dotenv = require('dotenv');

dotenv.config({ path: path.join(__dirname, '../.env') });

const app = express();
const port = process.env.PORT || 3000;

app.use(bodyParser.json());


app.post(process.env.SEND_MSG_API, async (req, res) => {
    logEvents(req.body.message + '\t' + req.body.number + '\t' + req.body.key);
    const number = req.body.number;
    const message = req.body.message;
    const key = req.body.key;
    const devices = req.body.devices;
    const type = req.body.type;
    const prioritize = req.body.prioritize;

    console.log(req.body);

    if (!number || !message || !key || !devices || !type || !prioritize) {
        res.status(400).json({ error: 'Invalid request' });
        return;
    }

    if (key !== process.env.API_KEY) {
        res.status(401).json({ error: 'Unauthorized' });
        return;
    }

    try {
        const insertedMessage = await db.insertMessage(number, message, key);
        res.status(201).json({
            'data':{
                'messages': [insertedMessage],
                },
                'error': undefined,
                'success': true
            }
        );
    } catch (err) {
        res.status(500).json({
            'data':{
                'messages': [],
                },
            'error': err,
            'success': false
            });
        }
    });

app.listen(port, () => {
    console.log(`Server is running on port ${port}`);
});
