import { GraphStateAnnotationRoot, GraphState } from '../types.js';
import { NodeMutus } from '../nodes/nodeMutus.js'; // ATTENTION: consider default exports
import { NodeNomen } from '../nodes/nodeNomen.js';
import { NodeKokis } from '../nodes/nodeKokis.js';
import { NodeDedit } from '../nodes/nodeDedit.js';
import { fetchRegistry, intraMorphismRegistry, interMorphismRegistry } from '../registries/registries.js';
import { StateGraph, START, END } from '@langchain/langgraph';


const edgeShouldRetry = (state: GraphState) => {
    // console.log('state :', state);
    if (state.resourceMap.shouldRetry && state.resourceMap.shouldRetry.value) {
        console.log('edgeShouldRetry: shouldRetry is true');
        return 'nodeNomen';
    } else {
        return END;
    }
};


const stateGraph = new StateGraph(GraphStateAnnotationRoot)
    .addNode(
        'nodeMutus',
        new NodeMutus({
            inputs: [
                {
                    key: 'anchor',
                    intraMorphisms: {
                        fetch: fetchRegistry.fetchContentFromUrl,
                        transform: intraMorphismRegistry.doNothing,
                    }
                },
                {
                    key: 'target',
                    intraMorphisms: {
                        fetch: fetchRegistry.fetchContentFromUrl,
                        transform: intraMorphismRegistry.chunkPDBContent,
                    }
                },
                {
                    key: 'box',
                    intraMorphisms: {
                        fetch: fetchRegistry.fetchContentFromUrl,
                        transform: intraMorphismRegistry.chunkPDBContent,
                    }
                },
            ]
        })
    )
    .addNode(
        'nodeNomen',
        new NodeNomen({
            inputs: ['anchor', 'target'],
            outputs: [
                {
                    key: 'candidate',
                    intraMorphisms: ['doNothing'],
                },
            ] as const,
            interMorphism: interMorphismRegistry.generateCandidate,
        })
    )
    .addNode(
        'nodeDedit',
        new NodeDedit({
            inputs: [
                {
                    key: 'candidate',
                    path: 'ligandokreado/1iep/timestamp/candidate.smi',
                }
            ]
        }),
    )
    .addNode(
        'nodeKokis',
        new NodeKokis({
            inputs: ['candidate', 'target', 'box'],
            outputDir: 'candidate', // ATTENTION: indicates same directory as candidate
            interMorphism: () => 'https://service-autodock-384484325421.europe-west2.run.app/autodock_basic',
        })
    )
    .addNode(
        'nodeMutus2',
        new NodeMutus({
            inputs: [
                {
                    key: 'docking',
                    intraMorphisms: {
                        fetch: fetchRegistry.fetchContentFromUrl,
                        transform: intraMorphismRegistry.doNothing,
                    }
                },
                {
                    key: 'pose',
                    intraMorphisms: {
                        fetch: fetchRegistry.fetchContentFromUrl,
                        transform: intraMorphismRegistry.doNothing,
                    }
                },
            ]
        })
    )
    .addNode(
        'nodeNomen2',
        new NodeNomen({
            inputs: ['docking', 'pose'],
            outputs: [
                {
                    key: 'shouldRetry',
                    intraMorphisms: ['doNothing'],
                }] as const,
            interMorphism: interMorphismRegistry.evaluateDockingResults,
        })
    )
    .addEdge(START, 'nodeMutus')
    .addEdge('nodeMutus', 'nodeNomen')
    .addEdge('nodeNomen', 'nodeDedit')
    .addEdge('nodeDedit', 'nodeKokis')
    .addEdge('nodeKokis', 'nodeMutus2')
    .addEdge('nodeMutus2', 'nodeNomen2')
    .addConditionalEdges('nodeNomen2', edgeShouldRetry);

export const graph = stateGraph.compile();



