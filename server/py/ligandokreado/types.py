"""
Type definitions for LigandoKreado Python implementation.

This module contains Pydantic models that correspond to the TypeScript interfaces
used in the original implementation.
"""

from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel, Field
from langchain_core.messages import BaseMessage


class ChunkInfo(BaseModel):
    """Information about a PDB content chunk."""
    chain_id: str = Field(description="Chain identifier")
    start_residue: int = Field(description="Starting residue number")
    end_residue: int = Field(description="Ending residue number")
    content: str = Field(description="PDB content for this chunk")


class ResourceItem(BaseModel):
    """A resource item with path and optional value."""
    path: str = Field(description="Path to the resource")
    value: Optional[Any] = Field(default=None, description="Cached value of the resource")


class ResourceMap(BaseModel):
    """Map of resources used in the graph."""
    anchor: Optional[ResourceItem] = Field(default=None, description="Anchor molecule resource")
    target: Optional[ResourceItem] = Field(default=None, description="Target protein resource")
    box: Optional[ResourceItem] = Field(default=None, description="Binding box resource")
    candidate: Optional[ResourceItem] = Field(default=None, description="Generated candidate resource")
    docking: Optional[ResourceItem] = Field(default=None, description="Docking results resource")
    pose: Optional[ResourceItem] = Field(default=None, description="Pose results resource")
    should_retry: Optional[ResourceItem] = Field(default=None, description="Retry flag resource")


class DryModeManager(BaseModel):
    """Configuration for dry run mode."""
    dry_run_mode: bool = Field(default=False, description="Whether to run in dry mode")
    delay: int = Field(default=1000, description="Delay in milliseconds")
    dry_socket_mode: bool = Field(default=True, description="Whether to use dry socket mode")


class GraphState(BaseModel):
    """State of the LigandoKreado graph."""
    resource_map: ResourceMap = Field(description="Map of all resources")
    messages: List[BaseMessage] = Field(default_factory=list, description="Messages in the conversation")
    dry_mode_manager: Optional[DryModeManager] = Field(default=None, description="Dry mode configuration")


class NodeConfig(BaseModel):
    """Base configuration for nodes."""
    pass


class NodeDownUnit(BaseModel):
    """Configuration for a NodeDown unit."""
    key: str = Field(description="Resource key")
    intra_morphisms: Dict[str, Any] = Field(description="Intra-morphism functions")


class NodeDownConfig(NodeConfig):
    """Configuration for NodeDown."""
    units: List[NodeDownUnit] = Field(description="List of units to process")


class NodeLowConfig(NodeConfig):
    """Configuration for NodeLow."""
    inputs: List[str] = Field(description="Input resource keys")
    outputs: List[str] = Field(description="Output resource keys")
    inter_morphism: Any = Field(description="Inter-morphism function")


class NodeUpUnit(BaseModel):
    """Configuration for a NodeUp unit."""
    key: str = Field(description="Resource key")
    path: str = Field(description="Upload path")


class NodeUpConfig(NodeConfig):
    """Configuration for NodeUp."""
    units: List[NodeUpUnit] = Field(description="List of units to upload")


class NodeHighConfig(NodeConfig):
    """Configuration for NodeHigh."""
    inputs: Optional[List[str]] = Field(default=None, description="Input resource keys")
    units: Optional[List[NodeUpUnit]] = Field(default=None, description="Units for upload mode")
    output_dir: Optional[str] = Field(default=None, description="Output directory")
    inter_morphism: Optional[Any] = Field(default=None, description="Inter-morphism function")


# Transport function type aliases
TransportFunction = Any
TransformFunction = Any
InterMorphismFunction = Any
