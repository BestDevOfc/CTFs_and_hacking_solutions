#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
decrypt_flag.py

This script factors the RSA modulus N, recovers the private key, and decrypts the ciphertext CT to reveal the flag.
It leverages the special structure of the primes used in N (p, q = 2p + 1, r = 2q + 1, s = 2r + 1).

Usage:
    python decrypt_flag.py

Ensure that 'output.txt' is in the same directory as this script and contains the N and CT values.
"""

import sys
from Crypto.Util.number import inverse, long_to_bytes

def read_output(file_path):
    """
    Reads N and CT from the specified output file.

    Args:
        file_path (str): Path to the output file.

    Returns:
        tuple: A tuple containing N and CT as integers.
    """
    N = None
    CT = None
    try:
        with open(file_path, 'r') as f:
            for line in f:
                if line.startswith('N = '):
                    N = int(line.strip().split('= ')[1])
                elif line.startswith('CT = '):
                    CT = int(line.strip().split('= ')[1])
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading '{file_path}': {e}")
        sys.exit(1)
    
    if N is None or CT is None:
        print("Error: N or CT not found in the output file.")
        sys.exit(1)
    
    return N, CT

def integer_nth_root(n, k):
    """
    Compute the integer component of the real k-th root of n using binary search.

    Args:
        n (int): The number to find the root of.
        k (int): The degree of the root.

    Returns:
        int: The integer k-th root of n.
    """
    if n < 0:
        raise ValueError("n must be non-negative")
    if n == 0:
        return 0

    # Initial bounds for binary search
    low = 1
    high = 1 << ((n.bit_length() + k - 1) // k)

    while low <= high:
        mid = (low + high) // 2
        mid_k = mid ** k

        if mid_k == n:
            return mid
        elif mid_k < n:
            low = mid + 1
        else:
            high = mid - 1

    return high  # Return the floor of the root

def compute_p_approx(N):
    """
    Approximates the value of p using integer arithmetic.

    Args:
        N (int): The RSA modulus.

    Returns:
        int: Approximated value of p.
    """
    N_over_64 = N // 64
    p_approx = integer_nth_root(N_over_64, 4)
    return p_approx

def find_p(N, p_approx, delta=1000000):
    """
    Searches for the correct prime p within a specified range around p_approx.

    Args:
        N (int): The RSA modulus.
        p_approx (int): Approximated value of p.
        delta (int, optional): Range to search around p_approx. Defaults to 1,000,000.

    Returns:
        tuple: A tuple containing p, q, r, s if found, else (None, None, None, None).
    """
    print(f"Starting search for p around the approximated value: {p_approx}")
    for i in range(-delta, delta + 1):
        p_candidate = p_approx + i
        if p_candidate <= 0:
            continue  # Skip non-positive candidates
        q = 2 * p_candidate + 1
        r = 2 * q + 1
        s = 2 * r + 1
        # Compute p*q*r*s
        computed_N = p_candidate * q * r * s
        if computed_N == N:
            print(f"Success! Found p: {p_candidate}")
            print(f"q: {q}")
            print(f"r: {r}")
            print(f"s: {s}")
            return p_candidate, q, r, s
        # Optional: Print progress at intervals
        if i % 100000 == 0:
            print(f"Checked p_candidate: {p_candidate}")
    print("Failed to find p within the specified range.")
    return None, None, None, None

def compute_phi(N, p, q, r, s):
    """
    Computes Euler's Totient function φ(N).

    Args:
        N (int): The RSA modulus.
        p, q, r, s (int): The prime factors of N.

    Returns:
        int: The value of φ(N).
    """
    phi_N = (p - 1) * (q - 1) * (r - 1) * (s -1)
    return phi_N

def decrypt_flag(CT, d, N):
    """
    Decrypts the ciphertext using the private exponent.

    Args:
        CT (int): The ciphertext.
        d (int): The private exponent.
        N (int): The RSA modulus.

    Returns:
        str: The decrypted flag.
    """
    flag_int = pow(CT, d, N)
    flag_bytes = long_to_bytes(flag_int)
    try:
        flag = flag_bytes.decode()
    except UnicodeDecodeError:
        # If decoding fails, return raw bytes
        flag = flag_bytes
    return flag

def main():
    # Path to the output file
    output_file = 'output.txt'
    
    # Step 1: Read N and CT from the output file
    N, CT = read_output(output_file)
    print(f"Successfully read N and CT from '{output_file}'.")
    
    # Step 2: Compute the approximated value of p
    p_approx = compute_p_approx(N)
    print(f"Approximated p: {p_approx}")
    
    # Step 3: Search for the correct p within the range [p_approx - delta, p_approx + delta]
    p, q, r, s = find_p(N, p_approx, delta=1000000)
    if p is None:
        print("Unable to factor N with the current search parameters.")
        sys.exit(1)
    
    # Step 4: Compute φ(N)
    phi_N = compute_phi(N, p, q, r, s)
    print(f"Computed φ(N).")
    
    # Step 5: Compute the private exponent d
    e = 0x10001  # Public exponent
    try:
        d = inverse(e, phi_N)
    except ValueError:
        print("Error: Inverse of e mod φ(N) does not exist.")
        sys.exit(1)
    print(f"Computed private exponent d.")
    
    # Step 6: Decrypt the ciphertext to obtain the flag
    flag = decrypt_flag(CT, d, N)
    print(f"Decrypted Flag: {flag}")

if __name__ == '__main__':
    main()
