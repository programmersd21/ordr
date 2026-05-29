# Security Policy

## Supported Versions

| Version | Supported |
| ------- | --------- |
| 0.2.x   | Yes       |

## Reporting a Vulnerability

If you discover a security vulnerability in ordr, please report it by emailing the maintainers directly rather than opening a public issue.

Please include:
- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if any)

We will respond within 48 hours and work with you to address the issue promptly.

## Security Considerations

ordr is a sorting library that processes user data. While we strive for memory safety through Rust, please be aware:

- The library does not validate or sanitize input data beyond type checking
- Large inputs may consume significant memory
- Parallel sorting may spawn multiple threads

For production use, ensure appropriate resource limits and input validation at the application level.
