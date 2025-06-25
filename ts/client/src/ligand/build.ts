import { build } from 'esbuild';

async function bundleScene() {
  await build({
    entryPoints: ['./Ligand.entry.ts'],
    bundle: true,
    platform: 'browser',
    format: 'iife',
    globalName: 'ExportedSceneBundle',
    outfile: '../../public/scenes/ligand.js',
  });

  console.log('✅ ligand.js built successfully.');
}

bundleScene().catch(err => {
  console.error('❌ Build failed:', err);
  process.exit(1);
});
