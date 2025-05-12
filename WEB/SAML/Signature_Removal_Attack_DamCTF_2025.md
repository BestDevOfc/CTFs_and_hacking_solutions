# DamCTF 2025 
## web/l33t-benign (SAML Attack)

<img width="319" alt="Screenshot 2025-05-11 at 9 43 23 PM" src="https://github.com/user-attachments/assets/a10335ea-390b-4cf2-bed2-7feefcdbf7d4" />

There are 3 ways to solve this:
1) ```Signature Removal```
2) ```Self-Signing```
3) ```Signing using leaked Private Key in Forum```

Stuff I tried:
1) ```Credential spraying```
2) ```CVE hunting```
3) ```Fuzzing```
4) ```XSW```
5) ```XXE```

- This challenge had numerous steps, I'll quickly just provide the context around it. Pretty much there's a PHPBB based forum where they provide a service for password stealers.
You download their chrome extension and install it in people's browsers. Then the keylogged credentials are sent over to the forum's subdomain ```mwaas.el1t3.fun```
What's interesting is the post talking about this feature says that accessing this service is simple as it uses the Forum's Auth. When you go to authenticate you're redirected
to a ```SimpleSAMLphp``` page where you need to login. It's important to note that this SimpleSAMLPHP login page is on the forum's main domain ```el1t3.fun```.

- This means 2 things, the ```Identity Provider``` (IdP) is the main forum ```el1t3.fun``` this is where the database of user passwords are stored. Since the forum offers
a Malware as a Service they included a subdomain ```mwaas.el1t3.fun``` which is the ```service provider``` (SP). If you look in the screenshot below you'll notice logically
after authenticating to the IDP we need some sort of "proof" to send back to the SP that we did in fact authenticate and we are who we say we are. This is done using the
```SAMLResponseToken```. In our case this is ```Base64Encoded``` + ```URLEncoded``` and is a POST request sent to ```mwaas.el1t3.fun``` after the credentials are sent to the IDP
at ```el1t3.fun```.

- Lastly, SAML can also handle ```authorization```, here's an example below of something the ```IDP``` will return. The difference between this and ```OAuth``` is that the authorization
is more ```SP-side``` whereas OAuth authorization is server-side. For example when you login with ```Google``` to some apps they ```request authorization to your google drive files```, for instance.

Analogy:
- ```SAML```: “Here’s who the user is and what they can do. ```You (SP) decide how to handle that.```”
- ```OAuth```: “Here’s a ```token``` saying the user let me access ```their calendar```. Let me in.”

```xml
<saml:AttributeStatement>
  <saml:Attribute Name="username">
    <saml:AttributeValue>alice</saml:AttributeValue>
  </saml:Attribute>
  <saml:Attribute Name="role">
    <saml:AttributeValue>admin</saml:AttributeValue>
    <saml:AttributeValue>editor</saml:AttributeValue>
  </saml:Attribute>
  <saml:Attribute Name="department">
    <saml:AttributeValue>finance</saml:AttributeValue>
  </saml:Attribute>
</saml:AttributeStatement>
```

- Now how does the ```SP``` know that the SAMLToken that we send isn't tampered with? This is done using the ```Signatures``` (kind of like ```JWTs```) that are embedded within the
```assertation```. These signatures are signed using the ```IDP's private key``` and are verified by the ```SP using the IDP's PUBLIC key``` (very similar to assymetric ```JWT sessions```).

- So logically, the attacks are very very similar to ```JWT attacks```, we can try attacks such as: ```signature removal```, ```signature forgery (confusion)```, ```parsing discrepancies```, etc.

- ⚠️ It's important to note there's also attacks against the ```IDP ITSELF```, such as ```misconfigured SAML implementations```, ```using different subdomains that don't use the same DB but the same signing keys, etc```.

- Moreover, I also attempted to enumerate the version of the ```SimpleSamlPHP``` and search for lowhanging CVEs surrounding it. These are all against the IDP itself, however, attacking
the ```SP``` tends to be easier.


Below I've shown the authentication flow and the screenshot mentioning the existence of the malware service:
- mentions the existence of the service and how it uses the forum's auth:
<img width="1250" alt="Screenshot 2025-05-11 at 9 57 55 PM" src="https://github.com/user-attachments/assets/5a907d85-274a-45ca-8c0e-38739561b2e0" />

- authentication credentials being sent to the ```IDP``` (```forum``` at ```el1t3.fun```).

<img width="1512" alt="Screenshot 2025-05-11 at 9 58 48 PM" src="https://github.com/user-attachments/assets/76292c3e-6313-43fe-8cd0-22648c75d15a" />
<img width="679" alt="Screenshot 2025-05-11 at 10 01 11 PM" src="https://github.com/user-attachments/assets/6eea1428-73f4-43c8-93c5-9f9d426e1cb0" />

- Now the ```SamlTokenResponse``` from the ```IDP``` is sent to the ```SP```, it is now the responsibility of the ```SP``` to verify it's integrity (this is where the desync happens)
<img width="702" alt="Screenshot 2025-05-11 at 9 59 18 PM" src="https://github.com/user-attachments/assets/bb803795-3087-40ce-8ce8-700afc5ca335" />


Now there are numerous types of attacks such as Signature Wrapping (XSW), re-signing assertations, etc. This video is super useful
https://www.youtube.com/watch?v=es9S2O7IS6Y&ab_channel=SamBowne

I solved this challenge in an unintended way by removing the signatures via the ```SAMLRaider``` tool (in the youtube video explained)

Once you're in it's a simple enumerating the endpoints and impersonating the right user to access the credentials, one of which will be the flag.
- I spent a lot of time using all of the credentials to spray the forum by using the ```ClusterBomb Intruder Attack``` in ```Burp Suite```.


## Self-Signing and swapping certificate
To understand this we need to take a closer look at the ```SAMLResponse XML``` itself. If we take a look at it we see some interesting fields shown below
<img width="530" alt="Screenshot 2025-05-11 at 10 54 42 PM" src="https://github.com/user-attachments/assets/813713bb-d032-40ac-9eb4-c47c7f115af4" />

- The ```SignatureValue``` is verified using the ```IDP's``` ```X509Certificate``` (```public key```). But what happens if we remove the IDP's public key certificate
  and use our own then generate our ```own signature```? Will the SP parse the public key and verify the signature and it'll just trust it?
  This is exactly how this attack works, it's explained here: ```https://redsiege.com/tools-techniques/2021/11/attacking-saml-implementations/```
    - this is pretty similar to ```JWKS spoofing attack for JWT(s) where we modify the ISS host and the server trusts it```.
    - This also makes me wonder if there are possible algorithm confusion attacks for SAML too.

- Another interesting field I noticed was the ```<saml:Audience>```
<img width="693" alt="Screenshot 2025-05-11 at 11 02 04 PM" src="https://github.com/user-attachments/assets/22ab1e42-fb7f-4c83-82fb-eecae6d80932" />
<img width="1320" alt="Screenshot 2025-05-11 at 11 02 56 PM" src="https://github.com/user-attachments/assets/bf086736-8482-4a67-a3ec-f9a1445e07b4" />

Notice how this is on the ```SP's side```... why? After some research it turns out sometimes the SP will ```encrypt``` their Auth requests to the IDP (usually it's also in SAML format),
I guess the CTF developers were getting ```skill-issued``` so they decided to send a simple POST request with a ```URLencoded``` body instead. 

<img width="490" alt="Screenshot 2025-05-11 at 11 06 14 PM" src="https://github.com/user-attachments/assets/e5180b1f-7b95-4c94-961b-5239949bd733" />


Lastly, this can be used by the ```IDP``` to understand how the authentication flow should be carried out, for example, it tells the IDP ```where to redirect``` to after ```successful authentication```
<img width="1220" alt="Screenshot 2025-05-11 at 11 08 34 PM" src="https://github.com/user-attachments/assets/f758e0c9-761c-4bcc-b421-97409d7de1e4" />
<img width="622" alt="Screenshot 2025-05-11 at 11 09 10 PM" src="https://github.com/user-attachments/assets/fdf961ac-2333-433b-ab6c-4c60b5388079" />
- As you can see the IDP listened and redirected to ```htts://mwaas.el1t3.fun/saml/acs/``` as a ```POST``` request with the token.


## Resigning Assertations via Private Key

- The ```intended solve``` was ```re-signing the assertations``` with the leaked ```private key``` in the forum.
  <img width="982" alt="Screenshot 2025-05-11 at 10 05 31 PM" src="https://github.com/user-attachments/assets/0b9f09cb-5052-4055-998a-fff0e3bf163d" />
- for some reason I can't figure out how to get my private key in without it ```erroring out```.



