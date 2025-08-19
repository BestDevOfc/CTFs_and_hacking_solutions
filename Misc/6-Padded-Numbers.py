# Generate numbers from 1 to 1,000,000 with zero-padding
def generate_padded_numbers(limit=1_000_000):
    padded_numbers = [str(i).zfill(6) for i in range(1, limit + 1)]
    return padded_numbers

# Example usage
if __name__ == "__main__":
  numbers = generate_padded_numbers()
  # Print first 10 for preview
  wordlist_file = open("Padded-Numbers.txt", 'w')
  for number in numbers:
     wordlist_file.write(f"{number}\n")
  wordlist_file.close()
