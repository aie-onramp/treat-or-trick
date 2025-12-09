"""Validation script for Upstash Redis connection.

Usage:
    uv run python scripts/upstash_validation.py

Requires environment variables:
    - KV_REST_API_URL (or UPSTASH_REDIS_REST_URL)
    - KV_REST_API_TOKEN (or UPSTASH_REDIS_REST_TOKEN)
"""

from upstash_redis import Redis
from dotenv import load_dotenv


def main() -> None:
    """Test Upstash Redis connection."""
    load_dotenv()

    try:
        redis = Redis.from_env()

        # Test write (synchronous - no await needed)
        redis.set("test_key", "test_value")
        print("✓ Successfully wrote to Redis")

        # Test read
        value = redis.get("test_key")
        print(f"✓ Successfully read from Redis: {value}")

        # Clean up
        redis.delete("test_key")
        print("✓ Successfully deleted test key")

        print("\n✅ Upstash Redis connection validated successfully!")

    except Exception as e:
        print(f"\n❌ Error connecting to Upstash Redis: {e}")
        print("\nMake sure you have the following environment variables set:")
        print("  - KV_REST_API_URL (or UPSTASH_REDIS_REST_URL)")
        print("  - KV_REST_API_TOKEN (or UPSTASH_REDIS_REST_TOKEN)")
        raise


if __name__ == "__main__":
    main()
