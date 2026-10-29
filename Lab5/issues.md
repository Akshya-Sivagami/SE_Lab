# Lab 5 - Static Code Analysis Issues

| Issue | Type | Line(s) | Description | Fix Approach |
|---|---|---:|---|---|
| Use of MD5 hash (B324) | Security - High | 45 | MD5 is considered a weak hashing algorithm and was flagged by Bandit. | Replaced `hashlib.md5()` with the stronger `hashlib.sha256()` algorithm. |
| Shell command execution (B605) | Security - High | 56 | `os.system()` invokes a shell and can introduce command injection risks when input is incorporated into the command. | Removed `os.system()` and used a normal `print()` statement to display the export message. |
| Use of `eval()` (B307) | Security - Medium | 40 | `eval()` can execute arbitrary Python expressions and is unsafe for untrusted input. | Replaced `eval()` with a whitelist of explicitly supported treatment-cost formulas. |
| Insecure random generator (B311) | Security - Low | 49 | `random.randint()` is not suitable when a token should be generated securely. | Replaced it with `secrets.randbelow()` to generate the ward token. |
| Bare exception with `pass` (B110) | Security / Reliability - Low | 24 | A bare `except` catches every exception and silently ignores errors. | Changed it to catch `KeyError` specifically and return a status indicating failure. |
| Mutable default argument (W0102) | Bug / Code Quality | 13 | Using `intake_log=[]` creates one shared list across function calls. | Changed the default to `None` and initialized a new list inside the function. |
| Invalid function naming (C0103) | Style / Code Quality | 13 | `admitPatient` does not follow Python snake_case naming conventions. | Renamed the function to `admit_patient` and updated its call. |
| Unsafe file handling (R1732 / W1514) | Code Quality | 53 | The file was manually opened and closed, and no encoding was specified. | Used a `with open(..., encoding="utf-8")` context manager. |
| Comparison with `None` (C0121 / E711) | Style / Code Quality | 30 | The code used `== None` instead of Python's recommended identity comparison. | Replaced the check with `is None` and simplified the admission-status logic. |
| Formatting violations (E501 / W292) | Style | Multiple | Flake8 detected lines longer than 79 characters and a missing final newline. | Reformatted long statements and added the final newline. |