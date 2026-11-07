import socket

SILENT_SERVERS: list[socket.socket] = []


def start_silent_server() -> str:
    """Start a server that accepts TCP connections and never answers them.

    Returns the address as ``127.0.0.1:<port>``. A client that connects to it
    waits until its own timeout, whatever network the test runs in. An address
    that is only meant to be unreachable does not do that: some networks refuse
    the connection at once.
    """
    server = socket.create_server(("127.0.0.1", 0))
    SILENT_SERVERS.append(server)
    host, port = server.getsockname()
    return f"{host}:{port}"


def stop_silent_servers() -> None:
    """Close every server that `Start Silent Server` started."""
    while SILENT_SERVERS:
        SILENT_SERVERS.pop().close()
