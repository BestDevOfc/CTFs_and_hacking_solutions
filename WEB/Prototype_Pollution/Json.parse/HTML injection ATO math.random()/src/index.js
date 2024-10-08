const express = require('express');
const cookieParser = require('cookie-parser');
const crypto = require('crypto');
const puppeteer = require('puppeteer');
const url = require('url');
const path = require('path');
const bcrypt = require('bcryptjs');
const { addCSRFToken, validateCSRFToken, cookieParams } = require('./utils');
const { addUser, getUserByUsername, getUserById, updatePassword, updateBestWPM, updateLatestTestResults, listUsers, listUsersLike, addWPM, getWPMs, addAdmin } = require('./database');

const app = express();

app.use(express.urlencoded({ extended: false }));
app.use(cookieParser(crypto.randomBytes(64).toString('hex'), cookieParams))
app.use(express.static(path.join(__dirname, 'public')));
app.use(function (req, res, next) {
    res.setHeader('Content-Security-Policy', "default-src 'self'; object-src 'none'; base-uri 'none';");
    res.setHeader('X-Frame-Options', 'DENY');
    res.setHeader('X-Content-Type-Options', 'nosniff');
    next();
});
app.set('view engine', 'ejs');

app.get('/', function(req, res) {
    const { error, info, success, message } = req.query;
    
    if (!req.signedCookies['token']) {
        res.clearCookie('token');
        return res.render('index');
    }

    getUserById(req.signedCookies['token'].id, (err, user) => {
        if (err || !user) {
            res.clearCookie('token');
            return res.render('index', { status: { error: true, message: "Invalid token" } });
        } else {
            return res.render('index', { username: user.username, status: { error: error, info: info, success: success, message: message } });
        }
    });
});

app.get('/register', addCSRFToken, function(req, res) {
    const { error, info, success, message } = req.query;

    res.render('register', { status: { error: error, info: info, success: success, message: message } });
});

app.post('/register', validateCSRFToken, function(req, res) {
    const { username, password } = req.body;
    if (!username || !password) {
        return res.redirect(url.format({
            pathname: 'register',
            query: { error: true, message: "Invalid username or password" }
        }));
    }

    if (!/^[a-zA-Z0-9!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]*$/.test(username)) {
        return res.redirect(url.format({
            pathname: 'register',
            query: { error: true, message: "Invalid username" }
        }));
    }

    if (!/^[a-zA-Z0-9!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]*$/.test(password)) {
        return res.redirect(url.format({
            pathname: 'register',
            query: { error: true, message: "Invalid password" }
        }));
    }

    if (username.length < 3 || password.length < 3) {
        return res.redirect(url.format({
            pathname: 'register',
            query: { error: true, message: "Username and password must be atleast 3 characters long" }
        }));
    }

    let hashedPassword = bcrypt.hashSync(password, 10);

    addUser(username, hashedPassword, (err, user) => {
        if (err) {
            return res.redirect(url.format({
                pathname: 'register',
                query: {
                    error: true, message: "Error adding user"
                }
            }));
        } else {
            return res.redirect('/');
        }
    });
});

app.get('/login', addCSRFToken, function(req, res) {
    const { error, info, success, message } = req.query;

    res.render('login', { status: { error: error, info: info, success: success, message: message } });
});

app.post('/login', validateCSRFToken, function(req, res) {
    const { username, password } = req.body;
    
    if (!username || !password) {
        return res.redirect(url.format({
            pathname: 'register',
            query: { error: true, message: "Invalid username or password" }
        }));
    }

    if (!/^[a-zA-Z0-9!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]*$/.test(username)) {
        return res.redirect(url.format({
            pathname: 'register',
            query: { error: true, message: "Invalid username" }
        }));
    }

    if (!/^[a-zA-Z0-9!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]*$/.test(password)) {
        return res.redirect(url.format({
            pathname: 'register',
            query: { error: true, message: "Invalid password" }
        }));
    }

    if (username.length < 3 || password.length < 3) {
        return res.redirect(url.format({
            pathname: 'register',
            query: { error: true, message: "Username and password must be atleast 3 characters long" }
        }));
    }

    getUserByUsername(username, (err, user) => {
        if (err) {
            return res.redirect(url.format({
                pathname: 'login',
                query: { error: true, message: "Error fetching user" }
            }));
        }

        if (!user || !bcrypt.compareSync(password, user.password)) {
            return res.redirect(url.format({
                    pathname: 'login',
                    query: { error: true, message: "Invalid username or password" }
                }));
        }

        res.cookie('token', { id: user.id }, cookieParams);
        res.redirect(url.format({
            pathname: '/',
            query: { success: true, message: "Logged in successfully" }
        }));
    });
});

app.get('/changepassword', addCSRFToken, function(req, res) {
    const { error, info, success, message } = req.query;

    if (!req.signedCookies['token']) {
        return res.redirect('/');
    }

    getUserById(req.signedCookies['token'].id, (err, user) => {
        if (err || !user) {
            res.clearCookie('token');
            return res.redirect('/');
        }

        res.render('changepassword', { username: user.username, status: { error: error, info: info, success: success, message: message } });
    });
});

app.post('/changepassword', validateCSRFToken, function(req, res) {
    if (!req.signedCookies['token']) {
        return res.redirect('/');
    }

    const { newPassword } = req.body;
    if (!newPassword) {
        return res.redirect(url.format({
            pathname: 'changepassword',
            query: { error: true, message: "Invalid password" }
        }));
    }

    var newHashedPassword = bcrypt.hashSync(newPassword, 10);

    getUserById(req.signedCookies['token'].id, (err, user) => {
        if (err || !user) {
            res.clearCookie('token');
            return res.redirect('/');
        }

        updatePassword(user.id, newHashedPassword, (err) => {
            if (err) {
                return res.redirect(url.format({
                    pathname: 'changepassword',
                    query: { error: true, message: "Error updating password" }
                }));
            }

            res.redirect(url.format({
                pathname: 'changepassword',
                query: { success: true, message: "Password updated successfully" }
            }));
        });
    });
});

app.get('/leaderboard', function(req, res) {
    listUsers((err, users) => {
        if (err) {
            return res.render('leaderboard', { status: { error: true, message: "Error fetching users" } });
        }

        if (!req.signedCookies['token']) {
            res.render('leaderboard', { users: users});
        } else {
            getUserById(req.signedCookies['token'].id, (err, user) => {
                if (err || !user) {
                    res.clearCookie('token');
                    return res.render('leaderboard', { users: users });
                }

                res.render('leaderboard', { users: users, username: user.username });
            });
        }
    });
});

app.get('/type', function(req, res) {
    if (!req.signedCookies['token']) {
        res.clearCookie('token');
        return res.render('type');
    }

    getUserById(req.signedCookies['token'].id, (err, user) => {
        if (err || !user) {
            res.clearCookie('token');
            return res.render('type', { status: { error: true, message: "Invalid token" } });
        }

        res.render('type', { username: user.username });
    });
});

app.get('/results', addCSRFToken, function(req, res) {
    if (!req.signedCookies['token']) {
        res.clearCookie('token');
        return res.render('results');
    }

    getUserById(req.signedCookies['token'].id, (err, user) => {
        if (err || !user) {
            res.clearCookie('token');
            return res.render('results', { status: { error: true, message: "Invalid token" } });
        }

        res.render('results', { username: user.username });
    });
});

app.post('/results', function(req, res) {
    if (!req.signedCookies['token']) {
        return res.sendStatus(403);
    }

    const { wpm } = req.body;
    if (!wpm) {
        return res.sendStatus(400);
    }

    var wpmInt = 0;

    try {
        wpmInt = Math.floor(parseFloat(wpm));
    } catch (e) {
        return res.sendStatus(400);
    }

    if (isNaN(wpmInt) || wpmInt <= 0 || !Number.isInteger(wpmInt)) {
        return res.sendStatus(400);
    }

    addWPM(wpmInt, req.signedCookies['token'].id, (err, _) => {
        if (err) {
            return res.sendStatus(500);
        }

        getUserById(req.signedCookies['token'].id, (err, user) => {
            if (err || !user) {
                res.clearCookie('token');
                return res.sendStatus(403);
            }

            if (wpmInt > user.bestWPM) {
                updateBestWPM(user.id, wpmInt, (err) => {
                    if (err) {
                        return res.sendStatus(500);
                    }
                });
            }
        });

        return res.sendStatus(200);
    });
});

app.post('/results/latest', function(req, res) {
    if (!req.signedCookies['token']) {
        return res.sendStatus(403);
    }
    const { data } = req.body;

    if (!data) {
        return res.sendStatus(400);
    }

    let dataObj = JSON.parse(atob(data));
    if (!dataObj) {
        return res.sendStatus(400);
    }

    updateLatestTestResults(req.signedCookies['token'].id, data, (err) => {
        if (err) {
            return res.sendStatus(500);
        }

        return res.sendStatus(200);
    });
});

app.get('/logout', function(req, res) {
    res.clearCookie('token');
    res.redirect('/');
});

app.get('/profile', function(req, res) {
    if (!req.signedCookies['token']) {
        return res.redirect('/');
    }

    if (req.signedCookies['token']) {
        getUserById(req.signedCookies['token'].id, (err, user) => {
            if (err || !user) {
                res.clearCookie('token');
                return res.redirect('/');
            }
            
            if (user.isAdmin === 1) {
                return res.render('profile', { username: user.username, flag: process.env.FLAG || "FFCTF{f4k3_fl4g}" });
            }

            res.render('profile', { username: user.username });
        });
    }
});

app.get('/profile/wpms', function(req, res) {
    if (!req.signedCookies['token']) {
        return res.statusCode(403);
    }

    getWPMs(req.signedCookies['token'].id, (err, wpms) => {
        if (err) {
            return res.sendStatus(500);
        }

        let wpmsArr = [];
        for (let i = 0; i < wpms.length; i++) {
            wpmsArr.push(wpms[i].wpm);
        }

        return res.json(wpmsArr);
    });
});

app.post('/results/report', function(req, res) {
    if (!req.signedCookies['token']) {
        return res.sendStatus(403);
    }

    const { data } = req.body;
    if (!data) {
        return res.sendStatus(400);
    }

    getUserById(req.signedCookies['token'].id, (err, user) => {
        if (err || !user) {
            res.clearCookie('token');
            return res.sendStatus(403);
        }

        if (user.isAdmin) {
            return res.sendStatus(403);
        }

        let randomUsername = crypto.randomBytes(16).toString('hex');
        let randomPassword = crypto.randomBytes(16).toString('hex');

        let hashedPassword = bcrypt.hashSync(randomPassword, 10);

        function delay(time) {
            return new Promise(function(resolve) { 
                setTimeout(resolve, time)
            });
        }

        addAdmin(randomUsername, hashedPassword, (err, _) => {
            if (err) {
                return res.sendStatus(500);
            }

            (async () => {
                const browser = await puppeteer.launch({
                    args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage', '--disable-gpu', '--headless'],
                });
                const page = await browser.newPage();
                await page.goto('http://localhost:3000/login');
                await page.type('input[name=username]', randomUsername);
                await page.type('input[name=password]', randomPassword);
                await page.click('button[type=submit]');
                await delay(1000);
                await page.goto('http://localhost:3000/results?data=' + data);
                await delay(2000);
                await page.click('button[type=submit].save-results-button');
                await delay(1000);
                await browser.close();
            })();

            return res.json({ username: randomUsername });
        });
    });
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`Server listening on port ${PORT}`);
});