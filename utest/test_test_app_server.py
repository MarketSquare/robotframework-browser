from atest.library.test_app_server import http_command, start_test_app


def crash_once():
    starts = []

    def cmd_builder(port: str, token: str) -> list:
        starts.append(port)
        if len(starts) == 1:
            return ["node", "-e", "process.exit(3)"]
        return http_command(port, token)

    return cmd_builder


def test_a_crashed_start_is_retried_and_reported(tmp_path):
    server = start_test_app(tmp_path, cmd_builder=crash_once())
    try:
        assert server.process.poll() is None
        assert len(server.failed_attempts) == 1
        assert "crashed, exit code 3" in server.failed_attempts[0]
    finally:
        server.stop()
