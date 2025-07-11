# 🧪 python-hash-dll-autotest

Automated test suite for validating the behavior and stability of a C/C++ dynamic library (`hash.dll` / `libhash.so`) responsible for calculating MD5 hashes of files in a directory. Written in Python using `pytest`.

---

## 🚀 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/notNullThen/python-hash-dll-autotest.git
```

### 2. Create and Activate a Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## ✅ Running the Tests

### Run All Tests in Parallel

```bash
pytest -v -n auto tests/
```

### Run All Tests Sequentially

```bash
pytest -v tests/
```

### Run a Specific Test File

```bash
pytest -v tests/test_functions.py
```

### Run with Console Debug Output

```bash
pytest -v -s tests/test_functions.py
```

---

## 🧩 Test Coverage Overview

### 🔻 Low-Level Tests (Direct Library Calls)

- Error code validation for each function
- Handling of null/invalid arguments
- Proper library init/terminate behavior

### 🔺 High-Level Tests (Via Python Wrapper)

- Hashing a directory with a single file
- Hashing a directory with multiple files
- Reading logs from completed operations
- Parallel hashing scenarios

---

## 🐞 Known and Confirmed Bugs

### Return Code Issues

| Function            | Issue                                                                         | Covered |
| :------------------ | :---------------------------------------------------------------------------- | :------ |
| HashStop            | Does not return a valid error when the library is uninitialized or terminated | ✅      |
| HashFree            | Returns no valid error code                                                   | ✅      |
| HashInit            | Does not return an error if the library is already initialized                | ✅      |
| HashReadNextLogLine | Returns '1: Unknown error' instead of '4: Reading an empty log'               | ✅      |

### Functional Issues

| Component                | Issue                                                          | Covered |
| :----------------------- | :------------------------------------------------------------- | :------ |
| HashDirectory            | Incorrect MD5 hash calculation                                 | ✅      |
| Parallel Hashing         | Log lines are mixed when hashing two folders in parallel       | ✅      |
| HashStop / HashTerminate | Freeze if the operation is not yet complete                    | ✅      |
| Memory management        | Memory can be mixed up when running several separate processes | ✅      |
