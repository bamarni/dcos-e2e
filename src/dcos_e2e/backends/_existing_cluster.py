"""
Helpers for interacting with existing clusters.
"""

from pathlib import Path
from typing import Any, Dict, Set

from dcos_e2e.backends._base_classes import ClusterBackend, ClusterManager
from dcos_e2e.node import Node


class ExistingCluster(ClusterBackend):
    """
    A record of an existing DC/OS cluster backend.
    """

    def __init__(
        self,
        masters: Set[Node],
        agents: Set[Node],
        public_agents: Set[Node],
        default_ssh_user: str,
    ) -> None:
        """
        Create a record of an existing cluster backend for use by a cluster
        manager.
        """
        self.masters = masters
        self.agents = agents
        self.public_agents = public_agents
        self._default_ssh_user = default_ssh_user

    @property
    def cluster_cls(self):
        """
        Return the `ClusterManager` class to use to create and manage a
        cluster.
        """
        return ExistingClusterManager

    @property
    def default_ssh_user(self) -> str:
        """
        Return the default SSH user for this backend.
        """
        return self._default_ssh_user


class ExistingClusterManager(ClusterManager):
    """
    A record of a DC/OS cluster.
    """

    def __init__(  # pylint: disable=super-init-not-called
        self,
        masters: int,
        agents: int,
        public_agents: int,
        files_to_copy_to_installer: Dict[Path, Path],
        cluster_backend: ExistingCluster,
    ) -> None:
        """
        Create a manager for an existing DC/OS cluster.

        Args:
            masters: The number of master nodes to create.
                This must match the number of masters in `cluster_backend`.
            agents: The number of agent nodes to create.
                This must match the number of agents in `cluster_backend`.
            public_agents: The number of public agent nodes to create.
                This must match the number of public agents in
                `cluster_backend`.
            files_to_copy_to_installer: An ignored mapping of host paths to
                paths on the installer node.
            cluster_backend: Details of the specific existing cluster backend
                to use.
        """
        self._masters = cluster_backend.masters
        self._agents = cluster_backend.agents
        self._public_agents = cluster_backend.public_agents

    def install_dcos_from_url(
        self,
        build_artifact: str,
        extra_config: Dict[str, Any],
        log_output_live: bool,
    ) -> None:
        """
        Raises:
            NotImplementedError: It is assumed that clusters created with the
                ExistingCluster backend already have an installed instance of
                DC/OS running on them.
        """
        raise NotImplementedError

    def install_dcos_from_path(
        self,
        build_artifact: Path,
        extra_config: Dict[str, Any],
        log_output_live: bool,
    ) -> None:
        """
        Raises:
            NotImplementedError: It is assumed that clusters created with the
                ExistingCluster backend already have an installed instance of
                DC/OS running on them.
        """
        raise NotImplementedError

    @property
    def masters(self) -> Set[Node]:
        """
        Return all DC/OS master ``Node``s.
        """
        return self._masters

    @property
    def agents(self) -> Set[Node]:
        """
        Return all DC/OS agent ``Node``s.
        """
        return self._agents

    @property
    def public_agents(self) -> Set[Node]:
        """
        Return all DC/OS public agent ``Node``s.
        """
        return self._public_agents

    def destroy(self) -> None:
        """
        Destroying an existing cluster is the responsibility of the caller.

        Raises: NotImplementedError when called.
        """
        raise NotImplementedError
