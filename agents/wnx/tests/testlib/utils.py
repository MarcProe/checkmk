#!/usr/bin/env python3
# Copyright (C) 2019 tribe29 GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

# pylint: disable=redefined-outer-name

import os
from pathlib import Path
from typing import Final

_CHECKMK_GIT_ENV_VAR: Final = "CHECKMK_GIT_DIR"


def get_path_from_env(env: str) -> Path:
    env_value = os.getenv(env)
    assert env_value is not None
    return Path(env_value)


def get_git_root_path() -> Path:
    return get_path_from_env(_CHECKMK_GIT_ENV_VAR)
