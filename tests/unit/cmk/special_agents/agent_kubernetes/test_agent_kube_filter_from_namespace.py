#!/usr/bin/env python3
# Copyright (C) 2021 tribe29 GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

from tests.unit.cmk.special_agents.agent_kube.factory import (
    api_to_agent_deployment,
    APIDeploymentFactory,
    APIPodFactory,
    MetaDataFactory,
)

from cmk.special_agents.agent_kube import kube_objects_from_namespaces, pods_from_namespaces
from cmk.special_agents.utils_kubernetes.schemata import api


def test_filter_pods_from_namespaces() -> None:
    # Arrange
    pods = [
        APIPodFactory.build(
            metadata=MetaDataFactory.build(name="one", namespace=api.NamespaceName("default")),
        ),
        APIPodFactory.build(
            metadata=MetaDataFactory.build(name="two", namespace=api.NamespaceName("standard"))
        ),
    ]

    # Act
    filtered_pods = pods_from_namespaces(pods, {api.NamespaceName("default")})

    # Assert
    assert len(filtered_pods) == 1
    assert filtered_pods[0].metadata.name == "one"


def test_filter_deployments_from_monitored_namespaces() -> None:
    # Arrange
    deployments = [
        api_to_agent_deployment(
            APIDeploymentFactory.build(
                metadata=MetaDataFactory.build(namespace=api.NamespaceName("default"))
            ),
        ),
        api_to_agent_deployment(
            APIDeploymentFactory.build(
                metadata=MetaDataFactory.build(namespace=api.NamespaceName("standard"))
            ),
        ),
    ]

    # Act
    filtered_deployments = kube_objects_from_namespaces(deployments, {api.NamespaceName("default")})

    # Assert
    assert [deployment.metadata.namespace for deployment in filtered_deployments] == ["default"]
