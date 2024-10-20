const crypto = require('crypto');
const fs = require('fs');
const path = require('path');


const PRIVATE_KEY = fs.readFileSync(path.join(__dirname, './keys/private'));
const PUBLIC_KEY = fs.readFileSync(path.join(__dirname, './keys/public'));

function sign(data){
    return { data, signature : crypto.sign('RSA-SHA256', data, PRIVATE_KEY).toString('base64') };
}

function verify(signedUser){
    const {data, signature } = signedUser;
    return crypto.verify('RSA-SHA256', data, PUBLIC_KEY, Buffer.from(signature, 'base64'))
}
module.exports = {
    sign,
    verify
};

console.log(sign( 'charles' ));



