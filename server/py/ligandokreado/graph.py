"""
Main graph definition for LigandoKreado Python implementation.

This module contains the Python equivalent of the TypeScript LangGraph definition.
"""

from typing import Literal
from langgraph.graph import StateGraph, START, END
from langchain_core.messages import HumanMessage

from ligandokreado.types import (
    ResourceItem, ResourceMap, DryModeManager,
    NodeDownConfig, NodeDownUnit, NodeLowConfig, NodeUpConfig,
    NodeUpUnit, NodeHighConfig
)

from nodes.node_down import NodeDown
from nodes.node_low import NodeLow
from nodes.node_up import NodeUp
from nodes.node_high import NodeHigh
from types import GraphState

from .registries import intra_morphism_registry, inter_morphism_registry


def edge_should_retry(state: GraphState) -> Literal["nodeLow", "__end__"]:
    """
    Conditional edge function to determine if the process should retry.
    
    Args:
        state: Current graph state
        
    Returns:
        Next node name or END
    """
    if (state.resource_map.should_retry and 
        state.resource_map.should_retry.value):
        print('edge_should_retry: shouldRetry is true')
        return 'nodeLow'
    else:
        return END


def create_graph() -> StateGraph:
    """
    Create and configure the LigandoKreado graph.
    
    Returns:
        Compiled StateGraph ready for execution
    """
    # Create the state graph
    graph = StateGraph(GraphState)
    
    # Add nodeDown
    node_down_config = NodeDownConfig(
        units=[
            NodeDownUnit(
                key='anchor',
                intra_morphisms={
                    'transport': transport_registry.fetch_content_from_path,
                    'transform': intra_morphism_registry.do_nothing,
                }
            ),
            NodeDownUnit(
                key='target',
                intra_morphisms={
                    'transport': transport_registry.fetch_content_from_path,
                    'transform': intra_morphism_registry.chunk_pdb_content,
                }
            ),
            NodeDownUnit(
                key='box',
                intra_morphisms={
                    'transport': transport_registry.fetch_content_from_path,
                    'transform': intra_morphism_registry.chunk_pdb_content,
                }
            ),
        ]
    )
    node_down = NodeDown(node_down_config)
    graph.add_node('nodeDown', node_down)
    
    # Add nodeLow
    node_low_config = NodeLowConfig(
        inputs=['anchor', 'target'],
        outputs=['candidate'],
        inter_morphism=inter_morphism_registry.generate_candidate,
    )
    node_low = NodeLow(node_low_config)
    graph.add_node('nodeLow', node_low)

    # Add nodeUp
    node_up_config = NodeUpConfig(
        units=[
            NodeUpUnit(
                key='candidate',
                path='ligandokreado/1iep/timestamp/candidate.smi',
            )
        ]
    )
    node_up = NodeUp(node_up_config)
    graph.add_node('nodeUp', node_up)

    # Add nodeHigh
    node_high_config = NodeHighConfig(
        inputs=['candidate', 'target', 'box'],
        output_dir='candidate',  # ATTENTION: indicates same directory as candidate
        inter_morphism=lambda: 'https://docking-with-autodock-384484325421.europe-west2.run.app/autodock_basic',
    )
    node_high = NodeHigh(node_high_config)
    graph.add_node('nodeHigh', node_high)
    
    # Add nodeDown2
    node_down2_config = NodeDownConfig(
        units=[
            NodeDownUnit(
                key='docking',
                intra_morphisms={
                    'transport': transport_registry.fetch_content_from_path,
                    'transform': intra_morphism_registry.do_nothing,
                }
            ),
            NodeDownUnit(
                key='pose',
                intra_morphisms={
                    'transport': transport_registry.fetch_content_from_path,
                    'transform': intra_morphism_registry.do_nothing,
                }
            ),
        ]
    )
    node_down2 = NodeDown(node_down2_config)
    graph.add_node('nodeDown2', node_down2)

    # Add nodeLow2
    node_low2_config = NodeLowConfig(
        inputs=['docking', 'pose'],
        outputs=['shouldRetry'],
        inter_morphism=inter_morphism_registry.evaluate_docking_results,
    )
    node_low2 = NodeLow(node_low2_config)
    graph.add_node('nodeLow2', node_low2)
    
    # Add edges
    graph.add_edge(START, 'nodeDown')
    graph.add_edge('nodeDown', 'nodeLow')
    graph.add_edge('nodeLow', 'nodeUp')
    graph.add_edge('nodeUp', 'nodeHigh')
    graph.add_edge('nodeHigh', 'nodeDown2')
    graph.add_edge('nodeDown2', 'nodeLow2')
    graph.add_conditional_edges('nodeLow2', edge_should_retry)
    
    return graph.compile()


def create_initial_state(
    anchor_path: str = "ligandokreado/1iep/2025-01-01T00:00:00.000Z/candidate.smi",
    target_path: str = "ligandokreado/1iep/target.pdb",
    box_path: str = "ligandokreado/1iep/box.pdb"
) -> GraphState:
    """
    Create an initial state for the graph.
    
    Args:
        anchor_path: Path to the anchor molecule file
        target_path: Path to the target protein file
        box_path: Path to the binding box file
        
    Returns:
        Initial GraphState
    """
    resource_map = ResourceMap(
        anchor=ResourceItem(path=anchor_path, value=None),
        target=ResourceItem(path=target_path, value=None),
        box=ResourceItem(path=box_path, value=None),
    )
    
    dry_mode_manager = DryModeManager(
        dry_run_mode=False,
        delay=1000,
        dry_socket_mode=True
    )
    
    return GraphState(
        resource_map=resource_map,
        messages=[HumanMessage(content="Graph is invoked")],
        dry_mode_manager=dry_mode_manager
    )


# Create the compiled graph instance
compiled_graph = create_graph()
