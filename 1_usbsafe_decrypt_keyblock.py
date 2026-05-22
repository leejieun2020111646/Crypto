from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

stored_hex = """
5D 71 12 B0 F0 BB 69 36 CC 7B 62 5E 3D EC 95 8C
38 21 72 4E D1 40 56 FF E7 E2 B4 A9 36 F6 74 A5
96 08 0A C9 47 A7 FB BA EE 16 09 8E E1 3B 37 61
F0 F6 EA 42 BB 90 53 20 67 6C 83 45 26 94 03 07
"""

stored = bytes.fromhex(stored_hex)

seed_ciphertext = bytes(b ^ 0xCC for b in stored)

master_key = b"NSRSoft_USBSAFE\x00"

cipher = Cipher(algorithms.SEED(master_key), modes.ECB())
decryptor = cipher.decryptor()
plain = decryptor.update(seed_ciphertext) + decryptor.finalize()

print("1. Decrypted 64-byte key record:")
print(plain)
print()


print("2. Marker bytes at offset:")
print(plain[50:60])
print()

secuarea_key = plain[:16]
print("3. SecuArea.img SEED key (first 16 bytes):")
print(secuarea_key)