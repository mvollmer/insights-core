from falafel.mappers import iptables
from falafel.tests import context_wrap


IPTABLES_RUEL = """
# Generated by iptables-save v1.4.7 on Thu Aug 11 14:50:53 2016
*filter
:INPUT ACCEPT [0:0]
:FORWARD ACCEPT [0:0]
:OUTPUT ACCEPT [183:39596]
-A INPUT -m state --state RELATED,ESTABLISHED -j ACCEPT
-A INPUT -p icmp -j ACCEPT
-A INPUT -i lo -j ACCEPT
-A INPUT -p tcp -m state --state NEW -m tcp --dport 22 -j ACCEPT
-A INPUT -j REJECT --reject-with icmp-host-prohibited
-A INPUT -j REJECT --reject-with tcp-reset
-A FORWARD -j REJECT --reject-with icmp-host-prohibited
COMMIT
# Completed on Thu Aug 11 14:50:53 2016
""".strip()

ICMP_PROHIBITED = """
-A INPUT -j REJECT --reject-with icmp-host-prohibited
-A FORWARD -j REJECT --reject-with icmp-host-prohibited
""".strip()


def test_iptables():
    iptables_info = iptables.iptables_rule(context_wrap(IPTABLES_RUEL))
    assert iptables_info.get("icmp-host-prohibited") == \
        ICMP_PROHIBITED.splitlines()
    assert len(iptables_info.get("tcp-reset")) == 1
    assert "tcp-reset" in iptables_info
