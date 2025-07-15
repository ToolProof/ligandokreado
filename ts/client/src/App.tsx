import { Ligand } from './ligand/Ligand';
import { useEffect, useRef } from 'react'
import './App.css'

function App() {
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {

    const asyncWrapper = async () => {
      if (!containerRef.current) return;

      const ligand = new Ligand(containerRef.current);
      ligand.init();

      // Cleanup on unmount
      return () => {
      };
    }

    asyncWrapper();

  }, []);

  return (
    <div ref={containerRef} style={{ width: '100vw', height: '100vh', backgroundColor: 'orange' }}></div>
  );
}

export default App
