# 🧪 python-hash-dll-autotest

Automated test suite for validating the behavior and stability of a C/C++ dynamic library (`hash.dll` / `libhash.so`) responsible for calculating MD5 hashes of files in a directory. Written in Python using `pytest`.

---

## 🚀 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/notNullThen/python-hash-dll-autotest.git
cd python-hash-dll-autotest
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

## 🐞 Known and Confirmed Bugs

### Return Code Issues

| Function            | Issue                                                                         | Covered |
| :------------------ | :---------------------------------------------------------------------------- | :------ |
| HashStop            | Does not return a valid error when the library is uninitialized or terminated | ✅      |
| HashFree            | Returns no valid error code                                                   | ✅      |
| HashInit            | Does not return an error if the library is already initialized                | ✅      |
| HashReadNextLogLine | Returns '1: Unknown error' instead of '4: Reading an empty log'               | ✅      |

### Functional Issues

| Component                        | Issue                                                                          | Covered |
| :------------------------------- | :----------------------------------------------------------------------------- | :------ |
| HashDirectory                    | Incorrect MD5 hash calculation                                                 | ✅      |
| Parallel Hashing                 | Log lines are mixed when hashing two folders in parallel                       | ✅      |
| HashStop / HashTerminate         | Freeze if the operation is not yet complete                                    | ✅      |
| Memory mix up                    | Memory can be mixed up when running several separate processes                 | ✅      |
| Terminate() doesn't clean memory | Log lines can be read even after running HashTerminate() and HashInit() again. | ✅      |
| Long non-ASCII paths             | Cannot process long non-ASCII paths                                            | ✅      |

## 🧩 Test Coverage Overview

### 🔻 Low-Level Error Handling Tests (`test_error_handling.py`)

| Test Case                                    | Purpose                                                                     | Notes                                 |
| -------------------------------------------- | --------------------------------------------------------------------------- | ------------------------------------- |
| `test_invalid_argument_passed_to_a_function` | Verifies proper error codes when passing `None` or invalid pointers         | Covers error codes 5 and 6            |
| `test_library_is_not_initialized`            | Ensures all functions return error code 7 if the library is not initialized | Terminates before executing functions |
| `test_library_is_already_initialized`        | Ensures re-initialization of the library returns error code 8               | Skipped due to bug                    |
| `test_reading_an_empty_log`                  | Ensures reading an empty log returns error code 4                           | Skipped due to bug                    |

---

### 🔺 Functional Integration Tests (`test_functions.py`)

| Test Case                  | Purpose                                                      | Notes                                |
| -------------------------- | ------------------------------------------------------------ | ------------------------------------ |
| `test_HashDirectory`       | Tests directory hashing operation and validates operation ID | Skipped due to freezing bug          |
| `test_HashReadNextLogLine` | Validates successful log reading after hashing               | Uses helper utils                    |
| `test_HashStatus`          | Verifies that the operation status reflects real-time state  | Monitors during and after operation  |
| `test_HashStop`            | Validates stopping a running hash operation                  | Skipped due to freeze bug            |
| `test_HashFree`            | Tests memory release behavior after reading a log            | Skipped due to memory cleanup issues |

---

### 🧩 Scenario-Based Tests (`test_scenarios.py`)

| Test Case                                    | Purpose                                                  | Notes                                        |
| -------------------------------------------- | -------------------------------------------------------- | -------------------------------------------- |
| `test_init_then_terminate`                   | Validates basic init and terminate lifecycle             |                                              |
| `test_hash_dir_then_stop`                    | Runs hashing and immediately stops operation             | Skipped due to freeze bug                    |
| `test_hash_dir_then_terminate`               | Runs hashing and calls terminate during operation        |                                              |
| `test_hash_dir_with_invalid_path`            | Validates error handling for non-existent path           | Skipped - filesystem error to be defined     |
| `test_hash_one_file_dir`                     | Tests hashing a directory with one file                  | Skipped - incorrect MD5 bug                  |
| `test_hash_multiple_files_and_one_file_dirs` | Chains multi-file and one-file hashing                   | Skipped - incorrect MD5 + memory issues      |
| `test_hash_empty_dir`                        | Validates behavior for empty directories                 | Skipped - should only run separately         |
| `test_two_parallel_hashes`                   | Validates parallel hashing behavior and result isolation | Skipped - mixed log/memory corruption issues |
| `test_multiple_files_dir_hash`               | Hashes a multi-file directory and verifies order/results | Skipped - incorrect MD5 bug                  |
| `test_non_ascii_file_dir_hash`               | Hashes a file with non-ASCII characters name and content | Skipped - incorrect MD5 bug                  |
