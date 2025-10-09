"""
API Usage Examples for RealTime Token Scanner
Demonstrates how to interact with the FastAPI backend
"""

import requests
import json
from datetime import datetime

# Base URL
API_URL = "http://localhost:8000"


def print_json(data):
    """Pretty print JSON data"""
    print(json.dumps(data, indent=2))


def check_health():
    """Check API health status"""
    print("\n🏥 Checking API Health...")
    response = requests.get(f"{API_URL}/health")
    print_json(response.json())
    return response.status_code == 200


def get_new_tokens(page=1, network=None, confirmed_only=True):
    """Get list of new tokens"""
    print(f"\n📋 Getting new tokens (page {page}, network: {network or 'all'})...")
    
    params = {
        "page": page,
        "page_size": 10,
        "confirmed_only": confirmed_only
    }
    
    if network:
        params["network"] = network
    
    response = requests.get(f"{API_URL}/tokens/new", params=params)
    tokens = response.json()
    
    print(f"Found {len(tokens)} tokens:")
    for token in tokens[:5]:  # Show first 5
        print(f"  • {token['name']} ({token['symbol']}) - {token['network']} - {token['address'][:10]}...")
    
    return tokens


def get_stats():
    """Get statistics summary"""
    print("\n📊 Getting Statistics...")
    response = requests.get(f"{API_URL}/stats/summary")
    stats = response.json()
    
    print(f"  Total Tokens: {stats['total_tokens']}")
    print(f"  Last 24h: {stats['tokens_last_24h']}")
    print(f"  Last Hour: {stats['tokens_last_hour']}")
    print(f"  By Network: {stats['by_network']}")
    
    return stats


def get_token_by_id(token_id):
    """Get specific token by ID"""
    print(f"\n🔍 Getting token #{token_id}...")
    response = requests.get(f"{API_URL}/tokens/{token_id}")
    
    if response.status_code == 200:
        token = response.json()
        print(f"  Name: {token['name']}")
        print(f"  Symbol: {token['symbol']}")
        print(f"  Address: {token['address']}")
        print(f"  Network: {token['network']}")
        print(f"  Block: {token['block_number']}")
        print(f"  Risk Score: {token['risk_score']}/10")
        return token
    else:
        print(f"  ❌ Token not found (status: {response.status_code})")
        return None


def get_token_by_address(address, network):
    """Get token by contract address"""
    print(f"\n🔎 Getting token at {address} on {network}...")
    response = requests.get(
        f"{API_URL}/tokens/address/{address}",
        params={"network": network}
    )
    
    if response.status_code == 200:
        token = response.json()
        print_json(token)
        return token
    else:
        print(f"  ❌ Token not found")
        return None


def get_recent_alerts(limit=5):
    """Get recent high-risk tokens"""
    print(f"\n⚠️  Getting recent alerts (limit: {limit})...")
    response = requests.get(
        f"{API_URL}/alerts/recent",
        params={"limit": limit}
    )
    
    alerts = response.json()
    print(f"Found {len(alerts)} alerts:")
    
    for alert in alerts:
        print(f"  ⚠️  {alert['name']} ({alert['symbol']}) - Risk: {alert['risk_score']}/10")
    
    return alerts


def filter_eth_tokens():
    """Get only Ethereum tokens"""
    print("\n⟠ Getting Ethereum tokens only...")
    response = requests.get(
        f"{API_URL}/tokens/new",
        params={"network": "ETH", "page_size": 5}
    )
    
    tokens = response.json()
    for token in tokens:
        print(f"  • {token['name']} - Block: {token['block_number']}")
    
    return tokens


def filter_bsc_tokens():
    """Get only BSC tokens"""
    print("\n🔶 Getting BSC tokens only...")
    response = requests.get(
        f"{API_URL}/tokens/new",
        params={"network": "BSC", "page_size": 5}
    )
    
    tokens = response.json()
    for token in tokens:
        print(f"  • {token['name']} - Block: {token['block_number']}")
    
    return tokens


def pagination_example():
    """Demonstrate pagination"""
    print("\n📄 Pagination Example...")
    
    for page in range(1, 4):
        print(f"\n  Page {page}:")
        response = requests.get(
            f"{API_URL}/tokens/new",
            params={"page": page, "page_size": 3}
        )
        
        tokens = response.json()
        for token in tokens:
            print(f"    - {token['name']} ({token['symbol']})")


def main():
    """Run all examples"""
    print("=" * 60)
    print("🔍 RealTime Token Scanner - API Examples")
    print("=" * 60)
    
    # Check if API is running
    if not check_health():
        print("\n❌ API is not running. Please start it with:")
        print("   docker-compose up")
        return
    
    # Run examples
    try:
        stats = get_stats()
        get_new_tokens(page=1)
        get_new_tokens(page=1, network="ETH")
        filter_eth_tokens()
        filter_bsc_tokens()
        get_recent_alerts(limit=3)
        
        # Get specific token if any exist
        tokens = get_new_tokens(page=1)
        if tokens and len(tokens) > 0:
            get_token_by_id(tokens[0]['id'])
            get_token_by_address(tokens[0]['address'], tokens[0]['network'])
        
        # Pagination
        pagination_example()
        
        print("\n" + "=" * 60)
        print("✅ All examples completed successfully!")
        print("=" * 60)
        
    except requests.exceptions.ConnectionError:
        print("\n❌ Cannot connect to API. Make sure it's running on http://localhost:8000")
    except Exception as e:
        print(f"\n❌ Error: {e}")


if __name__ == "__main__":
    main()


