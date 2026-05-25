# USBSafe Decryption Scripts

이 폴더는 USBSafe 관련 이미지 파일을 복호화하기 위한 Python 스크립트와 원본 이미지 파일로 구성되어 있습니다.

## 파일 구성

- `1_usbsafe_decrypt_keyblock.py`
  - 내부에 저장된 key block 데이터를 복호화하여 `SecuArea.img` 복호화에 사용할 SEED key를 확인합니다.
- `2_usbsafe_decrypt_secuarea.py`
  - `SecuArea.img`를 복호화합니다.
  - 실행 후 `SecuArea_decrypted.img`, `SecuArea_FAT_from_0x1000.img` 파일이 생성됩니다.
- `SecuArea.img`
  - 복호화 대상 원본 이미지 파일입니다.

## 실행 환경

- Python 3.10 이상 권장
- macOS, Windows, Linux 모두 실행 가능
- 필요한 외부 Python 패키지:
  - `cryptography`

## 처음 실행하는 방법

압축을 푼 뒤 터미널 또는 명령 프롬프트에서 해당 폴더로 이동합니다.

```bash
cd Crypto-main
```

가상환경을 생성합니다.

```bash
python3 -m venv .venv
```

가상환경을 활성화합니다.

macOS / Linux:

```bash
source .venv/bin/activate
```

Windows:

```bash
.venv\Scripts\activate
```

필요한 패키지를 설치합니다.

```bash
python -m pip install cryptography
```

## 실행 순서

먼저 key block 복호화 스크립트를 실행합니다.

```bash
python 1_usbsafe_decrypt_keyblock.py
```

정상 실행되면 `SecuArea.img SEED key`가 출력됩니다.

그 다음 `SecuArea.img` 복호화 스크립트를 실행합니다.

```bash
python 2_usbsafe_decrypt_secuarea.py
```

정상 실행되면 같은 폴더에 다음 결과 파일이 생성됩니다.

- `SecuArea_decrypted.img`
- `SecuArea_FAT_from_0x1000.img`

## 주의 사항

- `SecuArea.img`는 반드시 `2_usbsafe_decrypt_secuarea.py`와 같은 폴더에 있어야 합니다.
- `ModuleNotFoundError: No module named 'cryptography'` 오류가 발생하면 현재 실행 중인 Python 환경에 `cryptography`가 설치되지 않은 것입니다.
- 이 경우 아래 명령어를 다시 실행한 뒤 스크립트를 실행합니다.

```bash
python -m pip install cryptography
```

VS Code를 사용하는 경우, Python 인터프리터를 이 폴더의 가상환경으로 선택해야 합니다.

예시:

```text
Crypto-main/.venv/bin/python
```

