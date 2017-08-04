# == Copyright: 2017, CCX Technologies

from asyncio import wait_for
from .. import sdbus


async def get(service, address, path, interface, name, timeout_ms=30000):
    """Gets a D-Bus Property from another process.

    This is a co-routine, so must be await-ed from within a asyncio mainloop.

    Args:
        service (adbus.server.Service): service to connect to
        address (str): address (name) of the D-Bus Service to call
        path (str): path of method to call, ie. /com/awesome/Settings1
        interface (str): interface label to call, ie. com.awesome.settings
        name (str): name of the name to get, ie. TestProperty
        timeout_ms (int): maximum time to wait for a response in milli-seconds

    Returns:
        Value of the name.
    """

    call = sdbus.Call(
        service.sdbus,
        address.encode(),
        path.encode(), b"org.freedesktop.DBus.Properties", b"Get",
        (interface, name), b"v"
    )

    call.send(timeout_ms)
    await wait_for(call.wait_for_response(), timeout_ms / 1000)
    response = call.get_response()

    if isinstance(response, Exception):
        raise response
    else:
        return response


async def get_all(service, address, path, interface, timeout_ms=30000):
    """Gets a All D-Bus Properties from another process.

    This is a co-routine, so must be await-ed from within a asyncio mainloop.

    Args:
        service (adbus.server.Service): service to connect to
        address (str): address (name) of the D-Bus Service to call
        path (str): path of method to call, ie. /com/awesome/Settings1
        interface (str): interface label to call, ie. com.awesome.settings
        timeout_ms (int): maximum time to wait for a response in milli-seconds

    Returns:
        A dictionary, keys are the name names and values are the name
        values.
    """

    call = sdbus.Call(
        service.sdbus,
        address.encode(),
        path.encode(), b"org.freedesktop.DBus.Properties", b"GetAll",
        (interface, ), b"a{sv}"
    )

    call.send(timeout_ms)
    await wait_for(call.wait_for_response(), timeout_ms / 1000)
    response = call.get_response()

    if isinstance(response, Exception):
        raise response
    else:
        return response


class _variant_wrapper:
    def __init__(self, value):
        self.dbus_value = value
        self.dbus_signature = "v"


async def set_(
    service, address, path, interface, name, value, timeout_ms=30000
):
    """Sets a D-Bus Property in another process.

    This is a co-routine, so must be await-ed from within a asyncio mainloop.

    Args:
        service (adbus.server.Service): service to connect to
        address (str): address (name) of the D-Bus Service to call
        path (str): path of method to call, ie. /com/awesome/Settings1
        interface (str): interface label to call, ie. com.awesome.settings
        name (str): name of the name to get, ie. TestProperty
        value (object): value to set the name to, must be compatible
            with the defined D-Bus Property type
        timeout_ms (int): maximum time to wait for a response in milli-seconds
    """

    call = sdbus.Call(
        service.sdbus,
        address.encode(),
        path.encode(), b"org.freedesktop.DBus.Properties", b"Set",
        (interface, name, _variant_wrapper(value))
    )

    call.send(timeout_ms)
    await wait_for(call.wait_for_response(), timeout_ms / 1000)
    response = call.get_response()

    if isinstance(response, Exception):
        raise response
