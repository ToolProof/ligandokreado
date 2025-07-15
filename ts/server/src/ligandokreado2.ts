import { intraMorphismRegistry, interMorphismRegistry } from './registries.js';
import { GraphStateAnnotationRoot, GraphState } from 'updohilo/dist/types';
import { NodeDown } from 'updohilo/dist/nodes/nodeDown';
import { NodeLow } from 'updohilo/dist/nodes/nodeLow';
import { NodeHigh } from 'updohilo/dist/nodes/nodeHigh';
import { transportRegistry } from 'updohilo/dist/registries/registries';
import { StateGraph, START, END } from '@langchain/langgraph';


const edgeShouldRetry = (state: GraphState) => {
    // console.log('state :', state);
    if (state.resourceMap.shouldRetry && state.resourceMap.shouldRetry.value) {
        console.log('edgeShouldRetry: shouldRetry is true');
        return 'nodeLow';
    } else {
        return END;
    }
};


const stateGraph = new StateGraph(GraphStateAnnotationRoot)
    .addNode(
        'nodeHigh',
        new NodeHigh({
            units: [
                {
                    key: 'candidate',
                    path: 'ligandokreado/1iep/timestamp/candidate.smi',
                }
            ]
        }),
    )
    .addNode(
        'nodeHigh',
        new NodeHigh({
            inputs: ['candidate', 'target', 'box'],
            outputDir: 'candidate', // ATTENTION: indicates same directory as candidate
            interMorphism: () => 'https://service-autodock-384484325421.europe-west2.run.app/autodock_basic',
        })
    )
    .addNode(
        'nodeDown2',
        new NodeDown({
            units: [
                {
                    key: 'docking',
                    intraMorphisms: {
                        transport: transportRegistry.fetchContentFromUrl,
                        transform: intraMorphismRegistry.doNothing,
                    }
                },
                {
                    key: 'pose',
                    intraMorphisms: {
                        transport: transportRegistry.fetchContentFromUrl,
                        transform: intraMorphismRegistry.doNothing,
                    }
                },
            ]
        })
    )
    .addNode(
        'nodeLow2',
        new NodeLow({
            inputs: ['docking', 'pose'],
            outputs: ['shouldRetry'] as const,
            interMorphism: interMorphismRegistry.evaluateDockingResults,
        })
    )
    .addEdge(START, 'nodeDown')
    .addEdge('nodeDown', 'nodeLow')
    .addEdge('nodeLow', 'nodeUp')
    .addEdge('nodeUp', 'nodeHigh')
    .addEdge('nodeHigh', 'nodeDown2')
    .addEdge('nodeDown2', 'nodeLow2')
    .addConditionalEdges('nodeLow2', edgeShouldRetry);

export const graph = stateGraph.compile();



