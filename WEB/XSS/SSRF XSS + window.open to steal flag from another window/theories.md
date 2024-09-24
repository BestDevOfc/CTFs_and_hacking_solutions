// like flask the session is set to a username not a UUID (maybe we can login as any user and retrieve note with flag?)
req.session.set('user', username);

abusing different protocols like data:// or something to get RCE and somehow access the flag note.
    - max URL lenght limit is 1,000
- also interesting how the body of the note has a 1,000 character limit.


* I think it's possible to bruteforce the username, but how to get the password (maybe it's the same for both the seed 
    randomizer?)
if (user === null) {
    return res.status(400).send('User not found');
}

if (!(await argon2.verify(user.password, password))) {
    return res.status(400).send('Wrong password!');
}



/*
    --no-sandbox
        other tabs and windows can be accessed from one tab
    --disable-setuid-sandbox
        chrome vulnerability could be exploited to access the host
        system, from there possible RCE.

*/

using XSS access /notes, parse flag, login to our acc, make a new note with the flag's contents
    - we'd need to also parse the CSRF tokens somehow (not sure if they're dynamically generated using JS)
        - doesn't matter, we're rendering it in a browser via puppeteer



disproven:
SQL injection via ID?
let { id } = req.body;
    - uses ORM

maybe using XSS password and username is leaked in one of the .EJS template files?
    - no, but the flag would be leaked if we accessed it using XSS