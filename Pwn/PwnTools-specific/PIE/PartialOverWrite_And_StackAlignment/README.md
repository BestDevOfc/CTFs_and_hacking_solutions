# Use Ubuntu or Linux Mint otherwise, you will have a missing LibC function version

On kali Linux this is how I figured it out:

The initial warning I missed by instinctively clicking ENTER:
<img width="1066" alt="Screenshot 2024-11-14 at 7 04 44 PM" src="https://github.com/user-attachments/assets/11c110fc-747c-46ab-bf3e-f4055ac1eb1e">


Once we successfully Ret2Win to the win() func and do some stepping through:
<img width="1062" alt="Screenshot 2024-11-14 at 7 04 16 PM" src="https://github.com/user-attachments/assets/d03d37f5-2900-4551-a09d-3acf1eb164f1">
