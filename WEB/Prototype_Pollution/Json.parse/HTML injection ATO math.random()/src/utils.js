const { getUserById } = require('./database');
const createDOMPurify = require('dompurify');
const { JSDOM } = require('jsdom');

const window = new JSDOM('').window;
const DOMPurify = createDOMPurify(window);
const cookieParams = {sameSite: 'strict', httpOnly: true, signed: true};

function addCSRFToken(req, res, next) {
    const csrfToken = getRandomHash(64);
    res.cookie('__csrf', csrfToken, cookieParams);
    res.locals.csrfToken = csrfToken;
    next();
}

function validateCSRFToken(req, res, next) {
    const csrfToken = req.signedCookies['__csrf'] || '';
    if (!csrfToken || csrfToken !== req.body._csrf) {
        return res.sendStatus(403);
    }
    res.clearCookie('__csrf');
    next();
}

function extractUserIfValidToken(token, callback) {
    if (token && token.id) {
        getUserById(token.id, (err, user) => {
            if (!err && user) {
                return callback(null, user);
            }
            callback(err)
        });
    }
    callback("empty token");
}

function getRandomHash(x) {
    let hash = '';
    for (let i = 0; i < x; i++) {
        hash += Math.floor(Math.random() * 0xffff).toString(16).padStart(4, '0');
    }
    return hash;
}

module.exports = {
    addCSRFToken,
    validateCSRFToken,
    getRandomHash,
    DOMPurify,
    extractUserIfValidToken,
    cookieParams
};