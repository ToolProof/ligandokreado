import { runRemoteGraph as runLigandokreado } from './clientLigandokreado.js';

if (process.env.NODE_ENV === 'ligandokreado') {
    runLigandokreado();
}