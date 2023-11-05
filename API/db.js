// const mysql = require('mysql');
// const url = require('url');
// const dotenv = require('dotenv');
// const path = require('path');
//
// dotenv.config({ path: path.join(__dirname, '../.env') });
//
// // Parse the DATABASE_URL
// const databaseUrl = url.parse(process.env.DATABASE_URL);
// const dbConfig = {
//     host: databaseUrl.hostname,
//     user: databaseUrl.auth.split(':')[0],
//     password: databaseUrl.auth.split(':')[1],
//     database: databaseUrl.pathname.substr(1),
// };
//
// const db = mysql.createConnection(dbConfig);
//
// db.connect((err) => {
//     if (err) {
//     console.error('Error connecting to MySQL:', err);
//     } else {
//     console.log('Connected to MySQL');
//     }
// });
//
//
// ////////////////////////////////////////////////////////////////
// const insertQuery = `
//         INSERT INTO message (mobile_number, content, status, added_at)
//         VALUES (?, ?, ?, ?)
//     `;
//
//
//
// ////////////////////////////////////////////////////////////////
//
// function getCurrDateTimeFormatForMySQL() {
//     const currentUtcTime = new Date().toISOString().slice(0, 19).replace('T', ' '); // Get the current UTC time in the 'YYYY-MM-DD HH:MM:SS' format
//     return currentUtcTime;
// }
//
// // Function to insert a message into the database
// function insertMessage(number, content, key) {
//     const status = 'unsent';
//     const added_at = getCurrDateTimeFormatForMySQL();
//
//     return new Promise((resolve, reject) => {
//         db.query(insertQuery, [number, content, status, added_at], (err, result) => {
//             if (err) {
//             console.error('Error inserting message:', err);
//             reject(err);
//             } else {
//                 const message = {
//                     'ID' : result.insertId,
//                     'attachments' : undefined,
//                     'deliveredDate' : undefined,
//                     'deviceID' : 1,
//                     'errorCode' : undefined,
//                     'expiryDate' : undefined,
//                     'groupID' : undefined,
//                     'message': `${content}`,
//                     'number' : `${number}`,
//                     'prioritize' : 1,
//                     'resultCode' : undefined,
//                     'retries' : undefined,
//                     'schedule' : undefined,
//                     'sentDate' : undefined,
//                     'simSlot' : undefined,
//                     'status' : 'pending',
//                     'type' : 'sms',
//                     'userID' : 1
//                 };
//                 resolve(message);
//             }
//         }
//         );
//     });
// }
//
//
// module.exports = {
//     insertMessage,
// };







const mysql = require('mysql2/promise'); // Use mysql2
const url = require('url');
const dotenv = require('dotenv');
const path = require('path');

dotenv.config({ path: path.join(__dirname, '../.env') });

// Parse the DATABASE_URL
const databaseUrl = url.parse(process.env.DATABASE_URL);
const dbConfig = {
    host: databaseUrl.hostname,
    user: databaseUrl.auth.split(':')[0],
    password: databaseUrl.auth.split(':')[1],
    database: databaseUrl.pathname.substr(1),
};

let db;

(async () => {
    try {
        db = await mysql.createConnection(dbConfig);
        console.log('Connected to MySQL');
    } catch (err) {
        console.error('Error connecting to MySQL:', err);
    }
})();

const insertQuery = `
    INSERT INTO message (mobile_number, content, status, added_at)
    VALUES (?, ?, ?, ?)
`;

function getCurrDateTimeFormatForMySQL() {
    const currentUtcTime = new Date().toISOString().slice(0, 19).replace('T', ' '); // Get the current UTC time in the 'YYYY-MM-DD HH:MM:SS' format
    return currentUtcTime;
}

// Function to insert a message into the database
async function insertMessage(number, content, key) {
    const status = 'unsent';
    const added_at = getCurrDateTimeFormatForMySQL();

    try {
        const [rows, fields] = await db.execute(insertQuery, [number, content, status, added_at]);

        const message = {
            'ID': rows.insertId,
            'attachments': undefined,
            'deliveredDate': undefined,
            'deviceID': 1,
            'errorCode': undefined,
            'expiryDate': undefined,
            'groupID': undefined,
            'message': `${content}`,
            'number': `${number}`,
            'prioritize': 1,
            'resultCode': undefined,
            'retries': undefined,
            'schedule': undefined,
            'sentDate': undefined,
            'simSlot': undefined,
            'status': 'pending',
            'type': 'sms',
            'userID': 1
        };
        return message;
    } catch (err) {
        console.error('Error inserting message:', err);
        throw err;
    }
}

module.exports = {
    insertMessage,
};
