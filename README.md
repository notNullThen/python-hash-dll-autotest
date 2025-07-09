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

#### 4. Run tests

```bash
pytest -v -n auto
```

### Lower level tests (without wrapper usage)

- Error handling tests

### Higher level tests (with wrapper usage)

- Test 1 file in directory hashing
- Test multiple files in directory hashing

# Found bugs

- BUG: HashStop() and HashTerminate() freeze if operation is not finished
