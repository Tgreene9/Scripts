#!/usr/bin/env python3
import argparse
import requests


class Result:
    def fail(self, feedback, details=None, staff_details=None):
        print(f"FAIL: {feedback}")
        if details:
            print(f"Details: {details}")
        if staff_details:
            print(f"Staff Details: {staff_details}")

    def success(self, feedback, details=None, staff_details=None):
        print(f"SUCCESS: {feedback}")
        if details:
            print(f"Details: {details}")
        if staff_details:
            print(f"Staff Details: {staff_details}")


class BasicHTTPCheck:
    def __init__(self, host, timeout=5, path='/'):
        self.host = host
        self.timeout = timeout
        self.path = path
        self.result = Result()

    def execute(self) -> None:
        """Execute the Check."""
        response = None
        url = f"http://{self.host}{self.path}"
        details: dict = {
            'timeout': self.timeout
        }
        staff_details = {
            'url': url
        }
        try:
            response = requests.get(url, timeout=self.timeout)
            staff_details['status_code'] = str(response.status_code)
        except requests.exceptions.ConnectionError as e:
            self.result.fail(
                feedback="Failed to connect to server, is port 80 open?",
                details=details,
                staff_details={
                    'raw': str(e)
                }
            )
        except Exception as e:
            details['raw'] = str(e)
            self.result.fail(feedback="HTTP not found", details=details)
        else:
            if response.status_code == 200:
                self.result.success(feedback="HTTP Accessible", details=details, staff_details=staff_details)
            else:
                self.result.fail(feedback="HTTP Accessible but unexpected status code", details=details, staff_details=staff_details)
        finally:
            if response:
                response.close()


if __name__ == '__main__':
    scoring_ip = '172.18.0.10'
    external_router_ip = '172.18.0.1'
    timeout = 5
    path = '/'

    check = BasicHTTPCheck(host=external_router_ip, timeout=timeout, path=path)
    check.execute()
