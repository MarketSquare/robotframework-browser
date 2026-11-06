#!/usr/bin/env bash
#
# Install the Playwright browsers and, on Linux, the system packages they need.
#
# The runner images list the Azure Ubuntu mirror first in /etc/apt/apt-mirrors.txt
# and fall back to archive.ubuntu.com only when a download stalls. Some days the
# Azure mirror serves a runner at tens of kB/s without ever stalling, and the
# install eats the whole job timeout. So the system packages get DEPS_DEADLINE;
# past it, the Azure mirror is dropped from the list and they are installed again
# from the official Ubuntu archive.
#
# Usage: install-playwright.sh [install command]
# The install command defaults to `npx playwright install`; `rfbrowser install`
# works too. Run it after `npm ci`, so npx runs the Playwright from the lock file.
set -euo pipefail

DEPS_DEADLINE=5m
MIRRORS=/etc/apt/apt-mirrors.txt
TIMED_OUT=124
KILLED=137

if [ $# -eq 0 ]; then
  set -- npx playwright install
fi

"$@"

[ "$(uname -s)" = Linux ] || exit 0

status=0
timeout --kill-after=30s "$DEPS_DEADLINE" "$@" --with-deps || status=$?
if [ "$status" -ne "$TIMED_OUT" ] && [ "$status" -ne "$KILLED" ]; then
  exit "$status"
fi

echo "::warning::Installing the Playwright system packages did not finish in ${DEPS_DEADLINE}, retrying from archive.ubuntu.com."
# Playwright runs apt-get under sudo, out of reach of the timeout's signal.
for _ in $(seq 60); do
  sudo pkill -x apt-get || true
  pgrep -x 'apt-get|dpkg' > /dev/null || break
  sleep 1
done
sudo dpkg --configure -a

if grep -q 'azure\.archive\.ubuntu\.com' "$MIRRORS" 2> /dev/null; then
  sudo sed -i '/azure\.archive\.ubuntu\.com/d' "$MIRRORS"
else
  echo "::warning::${MIRRORS} lists no Azure mirror, retrying from the same sources."
fi
"$@" --with-deps
