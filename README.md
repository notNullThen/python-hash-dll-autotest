# python-hash-dll-autotest

## Setup

#### 1. Clone the repository and navigate it

```bash
git clone https://github.com/your-username/hash-lib-tests.git
cd hash-lib-tests
```

#### 2. Create and use virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

#### 3. Install defined Python packages

```bash
pip install -r requirements.txt
```

#### 4. Run tests:

#### Paralelly:

```bash
pytest -v -n auto tests/
```

#### Not-paralelly

```bash
pytest -v tests/
```

#### Specific file

```bash
pytest -v tests/test_functions.py
```

#### Specific file with console messages (Debug)

```bash
pytest -v tests/test_functions.py -s
```

### Lower level tests (without wrapper usage)

- Error handling tests

### Higher level tests (with wrapper usage)

- Test 1 file in directory hashing
- Test multiple files in directory hashing

# Found bugs

- ✅ HashStop() and HashTerminate() freeze if operation is not finished
- ✅ MD5 Hash is calculated incorrectly
- ⚙️ Returns only last file hash from multiple files folder
- ⚙️ Mixes resutls into one line if hash 2 folders paralelly
- ⚙️ HashFree does not return valid error code
- ❓️ Memory is being managed incorrectly
  - To reproduce - unskip the `test_hash_one_file_dir()` test and run in bash `pytest -v tests/`
  - Then you can see in report that the actual result contains `multipleFilesFolder` and `file3.txt` though in Python script we use `file1.txt` from `oneFilesFolder`
  - The test will pass if you run only the `test_hash_one_file_dir` test with bash command `pytest -v tests/ -k test_hash_one_file_dir`
  - That means that memory is handled wrongly.
