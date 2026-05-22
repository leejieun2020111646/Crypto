from __future__ import annotations

from pathlib import Path

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


SECUAREA_KEY = b"JVBBOHDPOPJMYZTK"
EXPECTED_HEADER = b"USBSAFE_SECUAREA_IMAGE_HEADER1"
HEADER_TEST_LEN = 0x80
FAT_OFFSET = 0x1000


def seed_ecb_decrypt(ciphertext: bytes, key: bytes) -> bytes:
    """Reproduce sub_413A80-style decryption.
    - 16-byte full blocks: SEED decrypt
    - trailing bytes, if any: XOR with remaining length
    """
    if len(key) != 16:
        raise ValueError(f"SEED key must be 16 bytes, got {len(key)}")

    full_len = (len(ciphertext) // 16) * 16
    full_blocks = ciphertext[:full_len]
    remainder = bytearray(ciphertext[full_len:])

    cipher = Cipher(algorithms.SEED(key), modes.ECB())
    decryptor = cipher.decryptor()
    plaintext = decryptor.update(full_blocks) + decryptor.finalize()

    rem = len(remainder)
    for i in range(len(remainder)):
        remainder[i] ^= rem
        rem -= 1

    return plaintext + bytes(remainder)


def main() -> int:
    # 이 .py 파일이 있는 폴더 기준으로 SecuArea.img를 자동 탐색
    script_dir = Path(__file__).resolve().parent
    src = script_dir / "SecuArea.img"

    if not src.exists():
        print("ERROR: Cannot find SecuArea.img in the same folder.")
        print(f"Checked location: {src}")
        return 1

    data = src.read_bytes()
    if len(data) < HEADER_TEST_LEN:
        print("ERROR: SecuArea.img file size is too small.")
        return 1

    print(f"- Input: {src}")
    print(f"- Size : {len(data):,} bytes")
    print(f"- Key  : {SECUAREA_KEY.decode('ascii')}")

    # 1) 앞 128바이트 복호화로 키 검증
    first_plain = seed_ecb_decrypt(data[:HEADER_TEST_LEN], SECUAREA_KEY)

    print("\n1. Decrypted first 128 bytes")
    print(first_plain)
    print()

    if first_plain.startswith(EXPECTED_HEADER):
        print("Header check SUCCESS")
        print(f"Found prefix: {EXPECTED_HEADER.decode('ascii')}")
    else:
        print("Header check FAILED")
        print("Current key/target file/decryption method may not be correct.")
        return 2

    # 2) 전체 이미지 복호화
    decrypted = seed_ecb_decrypt(data, SECUAREA_KEY)
    out_img = script_dir / "SecuArea_decrypted.img"
    out_img.write_bytes(decrypted)

    print("\n2. Full decrypted image written:")
    print(f"    {out_img}")

    # 3) 0x1000 이후 FAT 후보 이미지 추출
    if len(decrypted) > FAT_OFFSET:
        fat = decrypted[FAT_OFFSET:]
        out_fat = script_dir / "SecuArea_FAT_from_0x1000.img"
        out_fat.write_bytes(fat)

        print("\n3. FAT candidate image written:")
        print(f"    {out_fat}")

        print("\n4. First 64 bytes of FAT candidate")
        print(fat[:64].hex(" ").upper())

        if len(fat) >= 512 and fat[510:512] == b"\x55\xAA":
            print("Boot sector signature 55 AA found at offset 0x1FE of extracted image.")
        else:
            print("55 AA boot signature was not found at offset 0x1FE.")
            print("Just open it with FTK Imager to verify.")
    else:
        print("Decrypted file is smaller than 0x1000, so no FAT candidate was extracted.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
