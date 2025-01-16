# Define the Docker subnet to scan
NETWORK="172.18.0"
 
# Loop through all potential IPs in the range
for ip in {1..254}; do
  # Check if the IP is reachable on port 80 (or any common port)
  (echo > /dev/tcp/${NETWORK}.$ip/80) >/dev/null 2>&1 && \
  echo "Host ${NETWORK}.$ip is up" &
done
 
# Wait for all background processes to complete
wait
 
echo "Scan completed for ${NETWORK}.x range."
