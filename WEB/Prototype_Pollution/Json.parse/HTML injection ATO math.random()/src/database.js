const sqlite3 = require('sqlite3').verbose();
const path = require('path');

const dbPath = path.resolve(__dirname, 'users.db');

const db = new sqlite3.Database(dbPath, (err) => {
    if (err) {
        console.error('Failed to connect to the database:', err.message);
    } else {
        console.log('Connected to the SQLite database.');
    }
});

db.run(`CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT,
    isAdmin INTEGER DEFAULT 0,
    bestWPM INTEGER DEFAULT 0,
    latestTestResults TEXT DEFAULT '{}'
)`);

db.run(`CREATE TABLE IF NOT EXISTS wpms (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    wpm INTEGER,
    userId INTEGER,
    FOREIGN KEY (userId) REFERENCES users(id)
)`);

const addUser = (username, hashedPassword, callback) => {
    db.run(`INSERT INTO users (username, password) VALUES (?, ?)`, [username, hashedPassword], function(err) {
        if (err) {
            return callback(err);
        }
        callback(null, { id: this.lastID });
    });
};

const addAdmin = (username, hashedPassword, callback) => {
    db.run(`INSERT INTO users (username, password, isAdmin) VALUES (?, ?, 1)`, [username, hashedPassword], function(err) {
        if (err) {
            return callback(err);
        }
        callback(null, { id: this.lastID });
    });
}

const getUserByUsername = (username, callback) => {
    db.get(`SELECT * FROM users WHERE username = ?`, [username], (err, user) => {
        if (err) {
            return callback(err);
        }
        callback(null, user);
    });
};

const getUserById = (id, callback) => {
    db.get(`SELECT * FROM users WHERE id = ?`, [id], (err, user) => {
        if (err) {
            return callback(err);
        }
        callback(null, user);
    });
};

const updatePassword = (id, hashedPassword, callback) => {
    db.run(`UPDATE users SET password = ? WHERE id = ?`, [hashedPassword, id], function(err) {
        if (err) {
            return callback(err);
        }
        callback(null);
    });
};

const updateBestWPM = (id, bestWPM, callback) => {
    db.run(`UPDATE users SET bestWPM = ? WHERE id = ?`, [bestWPM, id], function(err) {
        if (err) {
            return callback(err);
        }
        callback(null);
    });
}

const updateLatestTestResults = (id, latestTestResults, callback) => {
    db.run(`UPDATE users SET latestTestResults = ? WHERE id = ?`, [latestTestResults, id], function(err) {
        if (err) {
            return callback(err);
        }
        callback(null);
    });
}

const addWPM = (wpm, userId, callback) => {
    db.run(`INSERT INTO wpms (wpm, userId) VALUES (?, ?)`, [wpm, userId], function(err) {
        if (err) {
            return callback(err);
        }
        callback(null, { id: this.lastID });
    });
}

const getWPMs = (userId, callback) => {
    db.all(`SELECT * FROM wpms WHERE userId = ?`, [userId], (err, wpms) => {
        if (err) {
            return callback(err);
        }
        callback(null, wpms);
    });
}

const listUsers = (callback) => {
    db.all(`SELECT * FROM users WHERE isAdmin = 0 ORDER BY bestWPM DESC LIMIT 100`, (err, users) => {
        if (err) {
            return callback(err);
        }
        callback(null, users);
    });
};

const listUsersLike = (username, callback) => {
    db.all(`SELECT * FROM users WHERE username LIKE ? AND isAdmin = 0 ORDER BY bestWPM DESC LIMIT 100`, [`%${username}%`], (err, users) => {
        if (err) {
            return callback(err);
        }
        callback(null, users);
    });
};

module.exports = {
    addUser,
    addAdmin,
    getUserByUsername,
    getUserById,
    updatePassword,
    updateBestWPM,
    updateLatestTestResults,
    addWPM,
    getWPMs,
    listUsers,
    listUsersLike
};