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

### Hash functions return code

- ✅ HashStop does not return valid error code when Hash is not initialized or terminated
- ✅ HashFree does not return valid error code
- ✅ HashInit does not return error code when the library is already initialized
- ✅ HashReadNextLogLine returns "1: Unknown error" error instead of "4: Reading an empty log"

### Functional bugs

- ✅ MD5 Hash is calculated incorrectly
- ⚙️ Returns only last file hash from multiple files folder
- ⚙️ Mixes resutls into one line if hash 2 folders paralelly
- ✅ HashStop() and HashTerminate() freeze if operation is not finished
- ✅ Memory is being managed incorrectly
  - To reproduce - unskip `test_hash_two_different_dirs` test and run it by bash command `pytest -v tests -k test_hash_two_different_dirs`
  - In error report you will see that expected directory was `oneFileDir`, but actual directory is `multipleFilesDir`
  - If you comment the first directory hash line - `utils.get_directory_hash(DIRS_PATH.multipleFilesDir)`, you will see that error report now has the oneFileDir in both actual and expected results, which is correct behavior. It means that first dir hash was used in second dir hash line
