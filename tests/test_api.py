#!/usr/bin/env python3
"""Quick test script to validate the API changes."""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_chat_angel():
    """Test the /chat/angel endpoint."""
    print("Testing /chat/angel endpoint...")
    print("-" * 60)

    test_message = "I forgot to do my homework!"

    response = requests.post(
        f"{BASE_URL}/chat/angel",
        json={"message": test_message},
        headers={"Content-Type": "application/json"}
    )

    print(f"Status Code: {response.status_code}")
    print(f"Response Headers: {dict(response.headers)}")
    print(f"Response Body: {response.text}")

    if response.status_code == 200:
        try:
            data = response.json()
            print(f"\nParsed JSON: {json.dumps(data, indent=2)}")

            if data.get("response"):
                print(f"\n✅ SUCCESS: Got Angel response")
                print(f"Response length: {len(data['response'])} characters")
                print(f"\nAngel says:\n{data['response'][:200]}...")
                return True
            else:
                print(f"\n❌ FAILED: Empty response from Angel")
                return False
        except json.JSONDecodeError as e:
            print(f"\n❌ FAILED: Could not parse JSON: {e}")
            return False
    else:
        print(f"\n❌ FAILED: HTTP {response.status_code}")
        try:
            error_data = response.json()
            print(f"Error details: {json.dumps(error_data, indent=2)}")
        except:
            pass
        return False

def test_root():
    """Test the root endpoint."""
    print("\nTesting / root endpoint...")
    print("-" * 60)

    response = requests.get(f"{BASE_URL}/")
    print(f"Status Code: {response.status_code}")

    if response.status_code == 200:
        data = response.json()
        print(f"✅ Root endpoint working: {json.dumps(data, indent=2)}")
        return True
    else:
        print(f"❌ Root endpoint failed: {response.status_code}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("TreatOrHell API Validation Tests")
    print("=" * 60)

    results = []

    # Test root endpoint
    results.append(("Root Endpoint", test_root()))

    # Test chat endpoint
    results.append(("Chat Angel Endpoint", test_chat_angel()))

    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    for test_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status}: {test_name}")

    all_passed = all(result for _, result in results)
    print(f"\nOverall: {'✅ ALL TESTS PASSED' if all_passed else '❌ SOME TESTS FAILED'}")
