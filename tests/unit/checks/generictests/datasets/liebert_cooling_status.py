#!/usr/bin/env python3
# Copyright (C) 2019 tribe29 GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

# fmt: off
# type: ignore



checkname = 'liebert_cooling_status'


info = [
    [u'Fancy cooling device', u'awesome'],
]


discovery = {
    '': [
        (u'Fancy cooling device', {}),
    ],
}


checks = {
    '': [
        (u'Fancy cooling device', {}, [(0, "awesome", [])]),
    ],
}
