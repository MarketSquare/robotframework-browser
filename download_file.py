import argparse
import shutil
import tempfile
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Union, Optional
from xml.etree import ElementTree as ET
from zipfile import ZipFile

from dateutil import parser as du_parser
import requests

SAVED_ARTIFACTS = [
    "ubuntu-latest 14.x Clean install results",
    "ubuntu-latest 12.x Clean install results",
    "windows-latest 14.x Clean install results",
    "windows-latest 12.x Clean install results",
    "Test results",
]

OUT_FOLDER = Path(".") / "flip_rate"
DOWNLOAD_FOLDER = OUT_FOLDER / "download"
XUNIT_FOLDER = OUT_FOLDER / "xunit"


@dataclass
class XUnitFiles:
    robot: Optional[str]
    pytest: Optional[str]


@dataclass
class Artifact:
    name: Path
    id: Union[str, int]
    created_date: datetime


def get_artifacts(url: str) -> dict:
    params = {"per_page": 90}
    response = requests.get(f"{url}/actions/artifacts", params=params)
    response.raise_for_status()
    data = response.json()
    artifacts = data["artifacts"]
    print(f"Found {len(artifacts)}")
    return artifacts


def get_artifact(
    artifact: dict, saved_artifacts: list, download_folder: Path, headers: dict
) -> Union[Artifact, None]:
    url: str = artifact["archive_download_url"]
    name: str = artifact["name"]
    artifact_id = artifact["id"]
    date = du_parser.parse(artifact["created_at"])
    file_name = name.replace(" ", "_")
    file_name = str(download_folder / f"{file_name}-{artifact_id}.zip")
    if name not in saved_artifacts:
        return
    print(f"Download archive to {file_name}")
    try:
        _get_artifact(url, file_name, headers)
    except requests.exceptions.RequestException as error:
        print(f"Got error: {error}, retry.")
        _get_artifact(url, file_name, headers)
    return Artifact(Path(file_name), artifact_id, date)


def _get_artifact(url: str, file_name: str, headers: dict):
    with requests.get(url, headers=headers, stream=True) as response:
        response.raise_for_status()
        with open(file_name, "wb") as file:
            for chunk in response.iter_content(None):
                file.write(chunk)


def get_xunit(zip_artifact: Artifact, xunit_folder: Path) -> list:
    xunit_files = []
    with ZipFile(zip_artifact.name) as zip_file:
        for name in zip_file.namelist():
            xunit = XUnitFiles(None, None)
            if name.endswith(".xml") and "xunit" in name:
                xunit_files.append(
                    _xunit(zip_file, zip_artifact, xunit, name, xunit_folder)
                )
            if name.endswith("zip"):
                xunit_files.extend(
                    _extract_zip_from_zip(zip_file, name, zip_artifact, xunit_folder)
                )
    return list(filter(lambda item: item != [], xunit_files))


def _xunit(
    zip_file: ZipFile,
    zip_artifact: Artifact,
    xunit: XUnitFiles,
    name: str,
    xunit_folder: Path,
) -> XUnitFiles:
    unique_name = name.replace(".xml", "")
    unique_name = str(xunit_folder / f"{unique_name}-{zip_artifact.id}.xml")
    with tempfile.TemporaryDirectory() as tmp_folder:
        zip_file.extract(name, tmp_folder)
        extracted_file = Path(tmp_folder) / name
        shutil.move(extracted_file, unique_name)
        if name.startswith("robot"):
            tree = ET.parse(unique_name)
            root = tree.getroot()
            root.attrib["timestamp"] = zip_artifact.created_date.strftime(
                "%Y-%m-%dT%H:%M:%S.000000"
            )
            new_root = ET.Element("testsuites")
            new_root.insert(0, root)
            ET.ElementTree(new_root).write(unique_name)
            xunit.robot = unique_name
        if name.startswith("pytest"):
            xunit.pytest = unique_name
    print(f"Xunit: {unique_name}")
    return xunit


def _extract_zip_from_zip(
    zip_file: ZipFile, name: str, artifact: Artifact, xunit_folder: Path
):
    with tempfile.TemporaryDirectory() as tmp_folder:
        zip_file.extract(name, tmp_folder)
        extracted_file = Path(tmp_folder) / name
        name_id = f"{artifact.id}-{name.replace('.zip', '')}"
        return get_xunit(
            Artifact(extracted_file, name_id, artifact.created_date), xunit_folder
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Download artifacts from GitHub actions"
    )
    parser.add_argument("--project", help="project name in GitHub", required=True)
    parser.add_argument("--repo", help="Repository name in GitHub", required=True)
    parser.add_argument(
        "--token", help="GitHub token for reading artifacts", required=True
    )
    args = parser.parse_args()
    headers = {"Authorization": f"token {args.token}"}
    url = f"https://api.github.com/repos/{args.project}/{args.repo}"

    DOWNLOAD_FOLDER.mkdir(exist_ok=True, parents=True)
    XUNIT_FOLDER.mkdir(exist_ok=True, parents=True)
    artifact_files = []
    for artifact in get_artifacts(url):
        artifact_files.append(
            get_artifact(artifact, SAVED_ARTIFACTS, DOWNLOAD_FOLDER, headers)
        )
    artifact_files = list(filter(lambda item: item is not None, artifact_files))
    xunit_files = []
    for artifact in artifact_files:
        xunit_from_zip = get_xunit(artifact, XUNIT_FOLDER)
        xunit_files.extend(xunit_from_zip)
    xunit_files = list(filter(lambda item: item != [], xunit_files))
