#!/usr/bin/env python3
# Copyright (C) 2020 tribe29 GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

import pytest

from cmk.gui.plugins.dashboard import utils


@pytest.mark.parametrize(
    "entry, result",
    [
        pytest.param(
            {"svc_status_display": {"some": "content"}, "some": "other stuff"},
            {"status_display": {"some": "content"}, "some": "other stuff"},
            id="2.0.0->2.1.0i1",
        ),
    ],
)
def test_migrate_dashlet_status_display(entry, result) -> None:  # type:ignore[no-untyped-def]
    assert utils.ABCFigureDashlet._migrate_vs(entry) == result


@pytest.mark.parametrize(
    "context, single_infos, title, additional_macros, result",
    [
        pytest.param(
            {},
            [],
            "Some title $HOST_ALIAS$",
            {},
            {"$DEFAULT_TITLE$": "dashlet"},
            id="no single_infos",
        ),
        pytest.param(
            {"host": {"host": "heute"}},
            ["host"],
            "Best graph",
            {},
            {
                "$DEFAULT_TITLE$": "dashlet",
                "$HOST_NAME$": "heute",
            },
            id="host single_infos",
        ),
        pytest.param(
            {"service": {"service": "CPU utilization"}},
            ["service"],
            "Best graph",
            {},
            {
                "$DEFAULT_TITLE$": "dashlet",
                "$SERVICE_DESCRIPTION$": "CPU utilization",
            },
            id="service single_infos",
        ),
        pytest.param(
            {
                "host": {"host": "vm-123"},
                "service": {"service": "CPU utilization"},
            },
            ["host", "service"],
            "Best graph",
            {},
            {
                "$DEFAULT_TITLE$": "dashlet",
                "$HOST_NAME$": "vm-123",
                "$SERVICE_DESCRIPTION$": "CPU utilization",
            },
            id="host and service single_infos",
        ),
        pytest.param(
            {
                "host": {"host": "vm-123"},
                "service": {"service": "CPU utilization"},
            },
            ["host", "service"],
            "Best graph $HOST_ALIAS$",
            {
                "$SITE$": "site",
            },
            {
                "$DEFAULT_TITLE$": "dashlet",
                "$HOST_NAME$": "vm-123",
                "$HOST_ALIAS$": "alias",
                "$SERVICE_DESCRIPTION$": "CPU utilization",
                "$SITE$": "site",
            },
            id="site and host alias",
        ),
        pytest.param(
            {
                "host": {"host": "vm-123"},
                "service": {"service": "CPU utilization"},
            },
            ["host", "service"],
            "Best graph $HOST_ALIAS$",
            {
                "$ADD_MACRO_1$": "1",
                "$ADD_MACRO_2$": "2",
            },
            {
                "$DEFAULT_TITLE$": "dashlet",
                "$HOST_NAME$": "vm-123",
                "$HOST_ALIAS$": "alias",
                "$SERVICE_DESCRIPTION$": "CPU utilization",
                "$ADD_MACRO_1$": "1",
                "$ADD_MACRO_2$": "2",
            },
            id="additional macros",
        ),
    ],
)
def test_macro_mapping_from_context(
    monkeypatch,
    context,
    single_infos,
    title,
    result,
    additional_macros,
):
    monkeypatch.setattr(
        utils,
        "get_alias_of_host",
        lambda _site, _host_name: "alias",
    )
    assert (
        utils.macro_mapping_from_context(
            context,
            single_infos,
            title,
            "dashlet",
            **additional_macros,
        )
        == result
    )


@pytest.mark.parametrize(
    "single_infos, result",
    [
        pytest.param(
            [],
            [],
            id="no single infos",
        ),
        pytest.param(
            ["service", "host"],
            ["$HOST_NAME$", "$HOST_ALIAS$", "$SERVICE_DESCRIPTION$"],
            id="service and host",
        ),
        pytest.param(
            ["site"],
            [],
            id="unknown single info",
        ),
    ],
)
def test_get_title_macros_from_single_infos(  # type:ignore[no-untyped-def]
    single_infos, result
) -> None:
    assert list(utils._get_title_macros_from_single_infos(single_infos)) == result


@pytest.mark.parametrize(
    "single_infos, additional_macros, result",
    [
        pytest.param(
            [],
            [],
            "You can use the following macros to fill in the corresponding information:"
            "<ul><li><tt>$DEFAULT_TITLE$ (default title of the element)</tt></li></ul>"
            "These macros can be combined with arbitrary text elements, e.g. "
            '"some text <tt>$MACRO1$</tt> -- <tt>$MACRO2$</tt>".',
            id="default title only",
        ),
        pytest.param(
            ["host"],
            [],
            "You can use the following macros to fill in the corresponding information:"
            "<ul><li><tt>$DEFAULT_TITLE$ (default title of the element)</tt></li>"
            "<li><tt>$HOST_NAME$</tt></li>"
            "<li><tt>$HOST_ALIAS$</tt></li></ul>"
            "These macros can be combined with arbitrary text elements, e.g. "
            '"some text <tt>$MACRO1$</tt> -- <tt>$MACRO2$</tt>".',
            id="host single infos",
        ),
        pytest.param(
            [],
            ["$MACRO$"],
            "You can use the following macros to fill in the corresponding information:"
            "<ul><li><tt>$DEFAULT_TITLE$ (default title of the element)</tt></li>"
            "<li><tt>$MACRO$</tt></li></ul>"
            "These macros can be combined with arbitrary text elements, e.g. "
            '"some text <tt>$MACRO1$</tt> -- <tt>$MACRO2$</tt>".',
            id="additional macro",
        ),
        pytest.param(
            ["service", "host"],
            ["$MACRO1$", "$MACRO2$ (some explanation)"],
            "You can use the following macros to fill in the corresponding information:"
            "<ul><li><tt>$DEFAULT_TITLE$ (default title of the element)</tt></li>"
            "<li><tt>$HOST_NAME$</tt></li>"
            "<li><tt>$HOST_ALIAS$</tt></li>"
            "<li><tt>$SERVICE_DESCRIPTION$</tt></li>"
            "<li><tt>$MACRO1$</tt></li>"
            "<li><tt>$MACRO2$ (some explanation)</tt></li></ul>"
            "These macros can be combined with arbitrary text elements, e.g. "
            '"some text <tt>$MACRO1$</tt> -- <tt>$MACRO2$</tt>".',
            id="host, service in single infos and additional macros",
        ),
    ],
)
def test_title_help_text_for_macros(  # type:ignore[no-untyped-def]
    monkeypatch, single_infos, additional_macros, result
) -> None:
    monkeypatch.setattr(
        utils.ABCFigureDashlet,
        "single_infos",
        lambda: single_infos,
    )
    monkeypatch.setattr(
        utils.ABCFigureDashlet,
        "get_additional_title_macros",
        lambda: additional_macros,
    )
    # TODO: Fix this! mypy is correct...
    assert utils._title_help_text_for_macros(utils.ABCFigureDashlet) == result  # type: ignore[misc,type-abstract]
