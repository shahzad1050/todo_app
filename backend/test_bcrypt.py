#!/usr/bin/env python3
"""Test script to check bcrypt functionality"""

import bcrypt

# Test basic bcrypt functionality
try:
    # Test with a short password
    password = "short"
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    print(f"Successfully hashed short password: {len(password.encode('utf-8'))} bytes")

    # Test with a 72-byte password (the bcrypt limit)
    password_72 = "a" * 72
    hashed_72 = bcrypt.hashpw(password_72.encode('utf-8'), bcrypt.gensalt())
    print(f"Successfully hashed 72-byte password: {len(password_72.encode('utf-8'))} bytes")

    # Test with a 73-byte password (should fail)
    try:
        password_73 = "a" * 73
        hashed_73 = bcrypt.hashpw(password_73.encode('utf-8'), bcrypt.gensalt())
        print(f"ERROR: 73-byte password was accepted: {len(password_73.encode('utf-8'))} bytes")
    except ValueError as e:
        print(f"Correctly rejected 73-byte password: {e}")

    print("Bcrypt functionality test completed successfully!")

except Exception as e:
    print(f"Error during bcrypt test: {e}")
    import traceback
    traceback.print_exc()