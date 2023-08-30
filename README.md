Here is a README. There is lots to add, and currently this will serve as a progress tracker...

RSA.py:
- script with methods to generate RSA parameters based on defined input.
- public/private keys generated based on input integers
- methods to encrypt/decrypt plaintext/ciphertext
- THIS STILL NEEDS A TLS WRAPPER to allow for authentication
ECDHE.py:
- script with methods to generate ECDH parameters (ephemeral part meaning new session key per session)
- methods to generate session key using pair of public/private key pairs
- THIS STILL NEEDS A TLS WRAPPER to allow for session key generation and exchange

Zac's simple debugging notes....

1) AES.py has each routine for AES defined, but the expanded key schedule isn't working
2) the encrypt / decrypt routines aren't working either. TBC is this is due to broken key schedules
3) need to connect up each element of tls with proper protocol before finishing project