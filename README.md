# SweatingDataRNCryptor
SweatingDataRNCryptor is a Python tool designed to decrypt databases and data using the advanced RNCryptor algorithm. With SweatingDataRNCryptor, you can securely unlock encrypted databases and sensitive data using a specified key. This tool provides a user-friendly interface to select the encrypted files, apply the decryption process using the RNCryptor algorithm, and extract the decrypted contents. Whether you're dealing with encrypted databases or encrypted data, SweatingDataRNCryptor ensures seamless decryption with robust security measures. Unlock the secrets hidden within your encrypted data effortlessly with SweatingDataRNCryptor.
![imagem](https://github.com/labcif/SweatingDataRNCryptor/assets/112128696/be56a8c4-84f2-4666-b95c-f028ccaabf47)


## Features
- Decrypt databases and data securely
- Utilize the RNCryptor algorithm with a specified key
- User-friendly interface for ease of use
- Simplifies the decryption process for encrypted data

## Installation
1. Clone the repository: `git clone https://github.com/labcif/SweatingDataRNCryptor.git`
2. Install dependencies: `pip install -r requirements.txt`
3. Run the application (GUI): `python ./SweatingData_GUI.py`

## Usage GUI
1. Launch the application.
2. Provide the necessary parameters, including the database or file path and the decryption key.
3. Click the "Decrypt" button to unlock the encrypted data securely.
4. Access the decrypted data and utilize it as needed.

## Usage CLI
```
python ./SweatingData_CLI.py [-h] [--output OUTPUT] [--key KEY] input
positional arguments:
  input            Encrypted text or path to the database file

options:
  -h, --help       show this help message and exit
  --output OUTPUT  Path to save the decrypted database (optional)
  --key KEY        Decryption key
```

## Contributors
- Ricardo Bento Santos (https://github.com/RicardoBeny) - Creator and main developer
- Guilherme dos Reis Guilherme (https://github.com/guilhermegui08) - Creator and main developer

## License
This project is licensed under the [GPL-3.0](LICENSE).
