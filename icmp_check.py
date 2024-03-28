#!/usr/bin/env python3
import ping3

ping3.EXCEPTIONS = True


class ICMPCheck:
    def __init__(self, host, timeout):
        self.host = host
        self.timeout = timeout
        self.result = Result()

    def execute(self):
        """Execute the Check."""
        details = {
            'target': self.host
        }
        try:
            print('Starting ping to', self.host)
            ping3.ping(self.host, timeout=self.timeout)
        except ping3.errors.Timeout as e:
            details['raw'] = str(e)
            self.result.fail(
                feedback=f'Request Timed Out after {self.timeout} seconds',
                staff_details=details
            )
        except ping3.errors.HostUnknown as e:
            details['raw'] = str(e)
            self.result.error(
                feedback=f'Could not resolve host: {self.host}',
                staff_details=details
            )
        except ping3.errors.DestinationHostUnreachable as e:
            details['raw'] = str(e)
            self.result.fail(
                feedback='ping says "Destination Host Unreachable"',
                staff_details=details
            )
        except ping3.errors.DestinationUnreachable as e:
            details['raw'] = str(e)
            self.result.error(
                feedback='ping says "Destination Unreachable"',
                staff_details=details
            )
        except ping3.errors.PingError as e:
            details['raw'] = str(e)
            self.result.error(
                feedback="An unknown ping error occurred",
                staff_details=details
            )
        else:
            self.result.success(feedback=f'Ping successful to host {self.host}')


class Result:
    def __init__(self):
        self.status = "unknown"
        self.feedback = ""

    def fail(self, feedback, details=None):
        self.status = "fail"
        self.feedback = feedback
        print(f"FAIL: {feedback}")
        if details:
            print(f"Details: {details}")

    def warn(self, feedback, details=None):
        self.status = "warn"
        self.feedback = feedback
        print(f"WARN: {feedback}")
        if details:
            print(f"Details: {details}")

    def success(self, feedback):
        self.status = "success"
        self.feedback = feedback
        print(f"SUCCESS: {feedback}")


if __name__ == '__main__':
    scoring_user_ip = '172.18.0.10'
    external_router_ip = '172.18.0.1'
    timeout = 5  # Timeout in seconds

    check = ICMPCheck(external_router_ip, timeout)
    check.execute(
