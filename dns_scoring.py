#!/usr/bin/env python3
import dns.reversename
import dns.resolver
import dns.exception


class DnsCheck:
    def __init__(self, host, team_number):
        self.host = host
        self.team_number = team_number
        self.resolver = dns.resolver.Resolver()
        self.resolver.nameservers = [self.host]
        self.result = Result()

    def check_rev(self, domain, ip):
        try:
            ans = self.resolver.resolve(dns.reversename.from_address(ip), 'PTR')
            for x in ans:
                lookup = str(x).rstrip('.')
                if lookup == domain:
                    return True
            return False
        except (dns.resolver.NXDOMAIN, dns.exception.Timeout, dns.resolver.NoNameservers, dns.exception.DNSException):
            return False

    def check_forward(self, domain, ip):
        try:
            ans = self.resolver.resolve(domain)
            return str(ans[0]) == ip
        except (dns.resolver.NXDOMAIN, dns.exception.Timeout, dns.resolver.NoNameservers, dns.exception.DNSException):
            return False

    def get_external_domains(self):
        return {
            f"ns1.team{self.team_number}.ncaecybergames.org": f"172.18.13.{self.team_number}",
            f"www.team{self.team_number}.ncaecybergames.org": f"172.18.13.{self.team_number}",
            f"shell.team{self.team_number}.ncaecybergames.org": f"172.18.14.{self.team_number}",
            f"files.team{self.team_number}.ncaecybergames.org": f"172.18.14.{self.team_number}"
        }

    def execute(self):
        domains = self.get_external_domains()
        failed_fwd_lookups = []
        failed_rev_lookups = []

        for domain, ip in domains.items():
            if not self.check_forward(domain, ip):
                failed_fwd_lookups.append(domain)
            if not self.check_rev(domain, ip):
                failed_rev_lookups.append(ip)

        if not failed_fwd_lookups and not failed_rev_lookups:
            self.result.success(feedback="All external DNS lookups resolved correctly")
        elif failed_fwd_lookups and failed_rev_lookups:
            if len(failed_fwd_lookups) == len(domains) and len(failed_rev_lookups) == len(domains):
                self.result.fail(feedback="Could not connect to DNS server or all lookups failed")
            else:
                self.result.warn(feedback="Some external DNS lookups failed", details={
                    "failed_fwd_lookups": failed_fwd_lookups,
                    "failed_rev_lookups": failed_rev_lookups
                })
        elif failed_fwd_lookups:
            self.result.warn(feedback="Some external forward DNS lookups failed", details={
                "failed_fwd_lookups": failed_fwd_lookups
            })
        elif failed_rev_lookups:
            self.result.warn(feedback="Some external reverse DNS lookups failed", details={
                "failed_rev_lookups": failed_rev_lookups
            })


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

if __name__ == "__main__":
    dns_server_ip = "172.18.1.12"
    team_number = 1

    check = DnsCheck(host=dns_server_ip, team_number=team_number)
    check.execute()
