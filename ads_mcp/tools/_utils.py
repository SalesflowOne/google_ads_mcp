# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Common utilities for Google Ads API MCP tools."""

import os
import sys

from ads_mcp.utils import ROOT_DIR
from fastmcp.server.dependencies import get_access_token
from google.ads.googleads.client import GoogleAdsClient
from google.oauth2.credentials import Credentials
import yaml

_ADS_CLIENT: GoogleAdsClient | None = None


def get_credentials_path() -> str:
  """Returns the configured Google Ads credentials file path."""
  default_path = f"{ROOT_DIR}/google-ads.yaml"
  return os.environ.get("GOOGLE_ADS_CREDENTIALS", default_path)


def ensure_credentials_file() -> None:
  """Creates a minimal credentials file from env when only developer_token is set."""
  credentials_path = get_credentials_path()
  if os.path.isfile(credentials_path):
    return
  developer_token = os.getenv("GOOGLE_ADS_DEVELOPER_TOKEN")
  if not developer_token:
    return
  credentials_dir = os.path.dirname(credentials_path)
  if credentials_dir:
    os.makedirs(credentials_dir, exist_ok=True)
  with open(credentials_path, "w", encoding="utf-8") as f:
    yaml.dump(
        {"developer_token": developer_token, "use_proto_plus": True},
        f,
    )


def warn_if_credentials_missing() -> None:
  """Warns when credentials are missing without blocking server startup."""
  ensure_credentials_file()
  credentials_path = get_credentials_path()
  if os.path.isfile(credentials_path):
    return
  print(
      "Warning: Google Ads credentials not found at "
      f"{credentials_path}. Documentation tools are available; "
      "API tools require a valid google-ads.yaml. "
      "Copy google-ads.yaml.example to get started.",
      file=sys.stderr,
  )


def get_ads_client() -> GoogleAdsClient:
  """Gets a GoogleAdsClient instance.

  Looks for an access token from the environment or loads credentials from
  a YAML file.

  Returns:
      A GoogleAdsClient instance.

  Raises:
      FileNotFoundError: If the credentials YAML file is not found.
  """
  global _ADS_CLIENT

  access_token = get_access_token()
  if access_token:
    access_token = access_token.token

  credentials_path = get_credentials_path()
  if not os.path.isfile(credentials_path):
    raise FileNotFoundError(
        "Google Ads credentials YAML file is not found at "
        f"{credentials_path}. Set GOOGLE_ADS_CREDENTIALS or copy "
        "google-ads.yaml.example to google-ads.yaml."
    )

  if access_token:
    credentials = Credentials(access_token)
    with open(credentials_path, "r", encoding="utf-8") as f:
      ads_config = yaml.safe_load(f.read())
    return GoogleAdsClient(
        credentials,
        developer_token=ads_config.get("developer_token"),
        use_proto_plus=True,
    )

  if not _ADS_CLIENT:
    _ADS_CLIENT = GoogleAdsClient.load_from_storage(credentials_path)
    _ADS_CLIENT.use_proto_plus = (
        True  # Forced enable proto plus to avoid attribute issues.
    )

  return _ADS_CLIENT
