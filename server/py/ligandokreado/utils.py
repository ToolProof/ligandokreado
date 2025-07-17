"""
Utility functions for LigandoKreado.

This module contains utility functions converted from the TypeScript implementation.
"""

import re
from typing import List
from .types import ChunkInfo


def chunk_pdb_content(pdb_content: str, chunk_size: int = 1000) -> List[ChunkInfo]:
    """
    Chunk PDB content into manageable pieces.
    
    Args:
        pdb_content: The PDB file content as a string
        chunk_size: Maximum number of lines per chunk
        
    Returns:
        List of ChunkInfo objects containing chunked data
    """
    lines = pdb_content.split('\n')
    chunks: List[ChunkInfo] = []
    current_chunk: List[str] = []
    current_chain_id = ''
    start_residue = -1
    current_residue = -1

    for line in lines:
        if line.startswith('ATOM') or line.startswith('HETATM'):
            # Extract chain ID and residue number from PDB format
            chain_id = line[21:22].strip() if len(line) > 21 else ''
            residue_str = line[22:26].strip() if len(line) > 26 else '0'
            
            try:
                residue_number = int(residue_str)
            except ValueError:
                residue_number = 0

            # Start new chunk if conditions met
            if (len(current_chunk) >= chunk_size or 
                (current_chain_id and chain_id != current_chain_id)):
                
                if current_chunk:
                    chunks.append(ChunkInfo(
                        chain_id=current_chain_id,
                        start_residue=start_residue,
                        end_residue=current_residue,
                        content='\n'.join(current_chunk)
                    ))
                current_chunk = []
                start_residue = residue_number

            if start_residue == -1:
                start_residue = residue_number

            current_chain_id = chain_id
            current_residue = residue_number
            current_chunk.append(line)

    # Add the last chunk if not empty
    if current_chunk:
        chunks.append(ChunkInfo(
            chain_id=current_chain_id,
            start_residue=start_residue,
            end_residue=current_residue,
            content='\n'.join(current_chunk)
        ))

    return chunks


def do_nothing(s: str) -> str:
    """
    Identity function that returns the input unchanged.
    
    Args:
        s: Input string
        
    Returns:
        The same string unchanged
    """
    return s


async def fetch_content_from_path(path: str) -> str:
    """
    Fetch content from a file path.
    
    This is a placeholder implementation. In a real implementation,
    this would fetch from cloud storage, local filesystem, etc.
    
    Args:
        path: Path to the resource
        
    Returns:
        Content of the resource as string
    """
    # TODO: Implement actual fetching logic
    # This could involve:
    # - Reading from local filesystem
    # - Fetching from cloud storage (GCS, S3, etc.)
    # - Making HTTP requests
    
    print(f"Fetching content from path: {path}")
    return f"Mock content for {path}"


async def fetch_content_from_url(url: str) -> str:
    """
    Fetch content from a URL.
    
    Args:
        url: URL to fetch from
        
    Returns:
        Content from the URL as string
    """
    import httpx
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()
        return response.text
