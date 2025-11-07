```bash
sudo tcpdump -i any -nn -s 0 -w /tmp/all-traffic.pcap
```

# get all IPs
```bash
 tshark -r all-traffic.pcap -Y "ip or ipv6" -T fields -e ip.src -e ip.dst -e ipv6.src -e ipv6.dst \
| awk -F'\t' '{
  # choose ipv4 if present, otherwise ipv6 (field1=ip.src, field2=ip.dst, field3=ipv6.src, field4=ipv6.dst)
  src = ($1 != "" ? $1 : $3)
  dst = ($2 != "" ? $2 : $4)
  if (src != "" && dst != "") print src "," dst
}' > pairs.csv
```
