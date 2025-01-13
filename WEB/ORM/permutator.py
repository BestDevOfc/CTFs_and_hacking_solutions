import itertools

def generate_wordlist(base_string):
    # Split the base string into characters
    characters = list(base_string)
    
    # Create a list to hold variations for each character
    variations = []
    
    for char in characters:
        # If the character is a letter, add both uppercase and lowercase to the variations
        if char.isalpha():
            variations.append([char.lower(), char.upper()])
        else:
            # Non-alphabetic characters are kept as-is
            variations.append([char])
    
    # Use itertools.product to generate all possible combinations
    wordlist = [''.join(combination) for combination in itertools.product(*variations)]
    
    return wordlist

# Define the base string
base_string = "8axcgmish5zn59rsxjm"

# Generate the wordlist
wordlist = generate_wordlist(base_string)

# Save the wordlist to a file or print
output_file = "wordlist.txt"
with open(output_file, "w") as file:
    for word in wordlist:
        file.write(word + "\n")

print(f"Wordlist generated with {len(wordlist)} permutations and saved to {output_file}.")
