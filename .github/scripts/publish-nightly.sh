#!/usr/bin/env bash
#
# Put the wheels built from main on the `nightly` release.
#
# The release is created once and from then on only has its assets replaced.
# That is the whole point of this script: GitHub notifies everybody watching the
# repository when a release is *published*, and a build of main is not news, so
# nothing here ever publishes a second time. The tag is moved to the commit the
# wheels were built from, which is quiet.
#
# Wants GH_TOKEN, GITHUB_REPOSITORY and GITHUB_SHA from the workflow, VERSION
# from `inv dev-version`, and the wheels in WHEEL_DIR.
set -euo pipefail

TAG="nightly"
WHEEL_DIR="${WHEEL_DIR:-nightly-wheels}"
: "${VERSION:?the dev version the wheels were built with}"

shopt -s nullglob
wheels=("${WHEEL_DIR}"/*.whl)
shopt -u nullglob
if [ ${#wheels[@]} -eq 0 ]; then
  echo "No wheels in ${WHEEL_DIR}, nothing to publish." >&2
  exit 1
fi

# Wheels whose version does not match mean the stamping step did not run
# everywhere, and shipping a mixed set would hand testers a BrowserBatteries
# that refuses to install next to its own Browser wheel.
for wheel in "${wheels[@]}"; do
  case "$(basename "${wheel}")" in
    *-"${VERSION}"-*) ;;
    *)
      echo "$(basename "${wheel}") is not version ${VERSION}." >&2
      exit 1
      ;;
  esac
done

notes="$(mktemp)"
{
  echo "Wheels built from the latest green \`main\`, for trying out changes"
  echo "before they are released. Not a release: the version is a \`.dev\`"
  echo "build of the next milestone and it is replaced on every push to main."
  echo
  echo "Version \`${VERSION}\`, built from commit \`${GITHUB_SHA}\`."
  echo
  echo '## Install'
  echo
  echo "Install both wheels together. \`robotframework-browser-batteries\` pins"
  echo "the exact \`robotframework-browser\` it was built with, so a mixed pair"
  echo "will not resolve. Pick the batteries wheel for your platform."
  echo
  echo '```'
  echo "base=https://github.com/${GITHUB_REPOSITORY}/releases/download/${TAG}"
  echo "pip install --pre \\"
  echo "  \${base}/robotframework_browser-${VERSION}-py3-none-any.whl \\"
  echo "  \${base}/<the batteries wheel for your platform>"
  echo "rfbrowser init"
  echo '```'
  echo
  echo '## Wheels in this build'
  echo
  for wheel in "${wheels[@]}"; do
    echo "- \`$(basename "${wheel}")\`"
  done
  echo
  echo "Please report anything broken in these builds as an issue, mentioning"
  echo "the version above."
} > "${notes}"

if gh release view "${TAG}" > /dev/null 2>&1; then
  echo "Replacing the assets on the existing ${TAG} release."
  git tag --force "${TAG}" "${GITHUB_SHA}"
  git push --force origin "refs/tags/${TAG}"
  for asset in $(gh release view "${TAG}" --json assets --jq '.assets[].name'); do
    gh release delete-asset "${TAG}" "${asset}" --yes
  done
  gh release edit "${TAG}" --notes-file "${notes}" --prerelease
else
  echo "No ${TAG} release yet, creating it. This one does notify watchers."
  gh release create "${TAG}" \
    --target "${GITHUB_SHA}" \
    --title "Nightly builds from main" \
    --notes-file "${notes}" \
    --prerelease
fi

gh release upload "${TAG}" "${wheels[@]}" --clobber
echo "Published ${#wheels[@]} wheels as ${VERSION}."
