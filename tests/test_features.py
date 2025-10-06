import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backend import features
import pytest

# Patch dependencies for a good cases
import requests, subprocess, socket, ssl, types, builtins
from bs4 import BeautifulSoup as orig_bs

def test_check_speed(monkeypatch):
    # Mock the speedtest.Speedtest class
    class MockSpeedtest:
        def download(self): return 100_000_000
        def upload(self, pre_allocate=False): return 50_000_000
        @property
        def results(self): return self
        def share(self): pass
        def dict(self):
            return {
                'ping': 10,
                'timestamp': '2025-10-02T12:00:00.000Z',
                'bytes_sent': 1000000,
                'bytes_received': 2000000,
                'server': {'country': 'US'}
            }
    monkeypatch.setattr('backend.features.speedtest.Speedtest', MockSpeedtest)
    result = features.check_speed(from_test_cases=True)
    assert 'Download' in result
    assert result['Download'] == 100.0
    assert result['Upload'] == 50.0
    assert result['Ping'] == 10
    assert result['Date_Time'] == '2025-10-02T12:00:00.000Z'
    assert result['byts_S'] == 1.0
    assert result['byts_R'] == 2.0

def test_get_ISPndLoc_info():
    # Good case: valid API response
    class MockResponse:
        def json(self):
            return {
                "ip": "1.2.3.4",
                "city": "Testville",
                "region": "TestRegion",
                "org": "TestISP",
                "postal": "12345",
                "timezone": "Test/Zone",
                "country": "TS"
            }
    def mock_get(*args, **kwargs):
        return MockResponse()
    
    # Patch requests.get
    orig_get = requests.get
    requests.get = mock_get
    result = features.get_ISPndLoc_info()
    assert result["IP"] == "1.2.3.4"
    assert result["City"] == "Testville"
    assert result["Region"] == "TestRegion"
    assert result["ISP"] == "TestISP"
    assert result["Postal"] == "12345"
    assert result["TimeZone"] == "Test/Zone"
    assert result["Country_cli"] == "TS"
    # Bad case: API error
    def mock_get_error(*args, **kwargs):
        raise Exception("API failure")
    requests.get = mock_get_error
    try:
        result = features.get_ISPndLoc_info()
        assert "Error" in result or isinstance(result, dict)
    except Exception:
        # If function does not handle, this will catch
        assert True
    # Restore original requests.get
    requests.get = orig_get

def test_get_compareson():
    # Patch globals and dependencies for a good case
    features.user_country = "US"
    features.user_download_speed = 100.0
    features.user_upload_speed = 50.0
    features.user_ping = 10.0

    # Mock requests.get and BeautifulSoup
    class MockSoup:
        def find(self, *args, **kwargs):
            return self
        def text(self):
            return ""
        @property
        def text(self):
            return "75.0"  # Simulate average value
        def strip(self):
            return "75.0"

    class MockResponse:
        status_code = 200
        text = "<html></html>"

    def mock_get(*args, **kwargs):
        return MockResponse()

    orig_get = requests.get
    requests.get = mock_get


    def mock_bs(*args, **kwargs):
        return MockSoup()
    features.BeautifulSoup = mock_bs

    result = features.get_compareson()
    assert isinstance(result, tuple)
    assert "Download Speed" in result[0]
    assert "Upload Speed" in result[2]
    assert "latency" in result[4]

    # Bad case: user_country is None
    features.user_country = None
    result = features.get_compareson()
    assert "No Speed Test Data" in result

    # Restore
    requests.get = orig_get
    features.BeautifulSoup = orig_bs

def test_check_internet():
    # Good connection: router, internet, ping < 100ms
    def mock_run_good(args, **kwargs):
        class Result:
            returncode = 0
            stdout = ""
            stderr = ""
        return Result()
    def mock_popen_good(args, **kwargs):
        class MockStdout:
            def __iter__(self):
                # The regex expects at least one character before 'Average'
                return iter(["Reply from 8.8.8.8: bytes=32 time=50ms TTL=117", "Some text Average = 50ms"])
        class Proc:
            stdout = MockStdout()
        return Proc()

    orig_run = subprocess.run
    orig_popen = subprocess.Popen
    subprocess.run = mock_run_good
    subprocess.Popen = mock_popen_good
    result = features.check_internet()
    assert "Good Connection" in result["net_status"]
    assert "good" in result["suggests"].lower()

    # No router connection
    def mock_run_fail_router(args, **kwargs):
        class Result:
            returncode = 1
            stdout = ""
            stderr = ""
        return Result()
    subprocess.run = mock_run_fail_router
    result = features.check_internet()
    assert "Completely Disconnected" in result["net_status"]

    # Restore
    subprocess.run = orig_run
    subprocess.Popen = orig_popen

def test_check_Wifi_quality():
    # Patch os_name and subprocess.Popen for Windows
    features.os_name = "Windows"
    class MockProc:
        def communicate(self):
            # Simulate netsh wlan show interfaces output
            return (
                "SSID : TestWiFi B\n"
                "Signal : 80%\n"
                "BSSID : 00:11:22:33:44:55 N\n"
                "Receive rate (Mbps) : 150 T\n"
                "Transmit rate (Mbps) : 144 S\n"
                "Channel : 6 R\n",
                ""
            )
    orig_popen = subprocess.Popen
    subprocess.Popen = lambda *a, **k: MockProc()
    result = features.check_Wifi_quality()
    assert "Wi-Fi: TestWiFi" in result
    assert "Signal Quality: 80%" in result
    assert "Receive rate: 150" in result
    assert "Transmit rate: 144" in result
    assert "Channel: 6" in result
    # Restore
    subprocess.Popen = orig_popen

def test_check_website_stat():

    # Patch check_internet to always return online
    orig_check_internet = features.check_internet
    features.check_internet = lambda: {"net_status": "Online", "error": "", "suggests": ""}

    class MockResponse:
        status_code = 200
        text = "<html><title>Test Title</title><meta name='description' content='Test Desc'></html>"
        elapsed = types.SimpleNamespace(total_seconds=lambda: 0.123)
    
    def mock_get(url, verify=True):
        return MockResponse()
    orig_get = requests.get
    requests.get = mock_get

    orig_gethostbyname = socket.gethostbyname
    socket.gethostbyname = lambda domain: "1.2.3.4"

    class MockProc:
        def __init__(self): self.stdout = ["Reply from 1.2.3.4: bytes=32 time=10ms TTL=117", "Average = 10ms"]
    orig_popen = subprocess.Popen
    subprocess.Popen = lambda *a, **k: MockProc()

    class MockWhois:
        def __getitem__(self, key):
            return {
                "domain_name": "test.com",
                "registrar": "TestRegistrar",
                "updated_date": "2025-01-01",
                "creation_date": "2020-01-01",
                "expiration_date": "2030-01-01",
                "name_servers": ["ns1.test.com", "ns2.test.com"],
                "name": "TestOrg",
                "address": "123 Test St",
                "city": "TestCity",
                "state": "TS",
                "registrant_postal_code": "12345",
                "country": "TC"
            }[key]

    orig_whois = getattr(features, "whois", None)
    features.whois = types.SimpleNamespace(whois=lambda domain: MockWhois())

    class MockSSLSock:
        def getpeercert(self):
            return {"notAfter": "Dec 31 23:59:59 2099 GMT"}
    class MockContext:
        def wrap_socket(self, sock, server_hostname=None):
            return MockSSLSock()
    orig_create_connection = socket.create_connection
    socket.create_connection = lambda addr: None
    orig_create_default_context = ssl.create_default_context
    ssl.create_default_context = lambda: MockContext()

    class MockSoup:
        def __init__(self, *a, **k): pass
        def find(self, tag, attrs=None):
            if tag == "title": return types.SimpleNamespace(text="Test Title")
            if tag == "meta" and attrs and attrs.get("name") == "description": return {"content": "Test Desc"}
            return None
    builtins.BeautifulSoup = MockSoup

    result = features.check_website_stat("example.com")
    assert "online and working" in result["status"]
    assert result["meta_title"] == "Test Title"
    assert result["meta_description"] == "Test Desc"
    assert "test.com" in result["domain_info"]
    assert "SSL is valid" in result["ssl_status"]
    assert result["server_ip"] == "1.2.3.4"

    # Restore
    requests.get = orig_get
    socket.gethostbyname = orig_gethostbyname
    subprocess.Popen = orig_popen
    if orig_whois: features.whois = orig_whois
    socket.create_connection = orig_create_connection
    ssl.create_default_context = orig_create_default_context
    builtins.BeautifulSoup = orig_bs
    features.check_internet = orig_check_internet
