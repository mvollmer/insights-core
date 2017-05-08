"""
mlx4_port - Files contents
==========================
This module provides processing for the output of the
``find /sys/bus/pci/devices/*/mlx4_port[0-9] -print -exec cat {} \;`` command.

The specs handled by this CommandSpec::

    "mlx4_port"                 : CommandSpec("/usr/bin/find /sys/bus/pci/devices/*/mlx4_port[0-9] -print -exec cat {} \;"),

Sample output of this command looks like::

    /sys/bus/pci/devices/0000:0c:00.0/mlx4_port1
    ib
    /sys/bus/pci/devices/0000:0c:00.0/mlx4_port2
    eth

The ``port_val`` method is to return a dictionary contains mlx4_port name and
its content as the parsing result::

{'mlx4_port2': 'eth', 'mlx4_port1': 'ib'}

Examples:
    >>> mlx4_port_content = '''
    ... /sys/bus/pci/devices/0000:0c:00.0/mlx4_port1
    ... ib
    ... /sys/bus/pci/devices/0000:0c:00.0/mlx4_port2
    ... eth
    ... '''.strip()
    >>> from falafel.tests import context_wrap
    >>> from falafel.mappers.mlx4_port import Mlx4Port
    >>> shared = {Mlx4Port: Mlx4Port(context_wrap(mlx4_port_content))}
    >>> mlx4_port_results = Mlx4Port(context_wrap(mlx4_port_content))
    >>> mlx4_port_results.port_val
    {'mlx4_port2': 'eth', 'mlx4_port1': 'ib'}
"""

from .. import Mapper, mapper


@mapper('mlx4_port')
class Mlx4Port(Mapper):
    """
    Parse the output of the command:

    ``find /sys/bus/pci/devices/*/mlx4_port[0-9] -print -exec cat {} \;``.
    """
    @property
    def port_val(self):
        """
        dict: Returns the dictionary of `mlx4 port` name and its content
        """
        return self._mapping

    def parse_content(self, content):
        self._mapping = {}
        for line in content:
            mlx4_port_val = ''
            if line.startswith('/sys/'):
                port_name = line.split('/')[6]
            else:
                mlx4_port_val = line.strip()
            self._mapping[port_name] = mlx4_port_val
        return
