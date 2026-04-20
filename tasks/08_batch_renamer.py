"""
Task 08: Batch File Renamer
Renames files based on content analysis and metadata extraction.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import argparse
import os
import re
import hashlib
from datetime import datetime
from typing import List, Dict, Any, Optional, Callable
from smolagents import ToolCallingAgent, InferenceClientModel


def extract_file_metadata(file_path: str) -> Dict[str, Any]:
    """
    Extract metadata from a file.
    
    Args:
        file_path: Path to file
    
    Returns:
        Dictionary with metadata
    """
    path = Path(file_path)
    stats = path.stat()
    
    # Basic metadata
    metadata = {
        "original_name": path.name,
        "stem": path.stem,
        "extension": path.suffix.lower(),
        "size_bytes": stats.st_size,
        "size_human": f"{stats.st_size / 1024:.1f}KB" if stats.st_size < 1024**2 else f"{stats.st_size / 1024**2:.1f}MB",
        "created": datetime.fromtimestamp(stats.st_ctime).strftime("%Y-%m-%d"),
        "modified": datetime.fromtimestamp(stats.st_mtime).strftime("%Y-%m-%d"),
        "hash_short": hashlib.md5(path.name.encode()).hexdigest()[:8]
    }
    
    # Content-based metadata for text files
    if metadata["extension"] in ['.txt', '.md', '.py', '.js', '.json', '.csv', '.log']:
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read(5000)  # Read first 5000 chars
                metadata["content_preview"] = content[:200]
                metadata["line_count"] = content.count('\n') + 1
                
                # Extract title/first line
                first_line = content.split('\n')[0].strip()
                if first_line and len(first_line) < 100:
                    metadata["title"] = first_line
        except:
            pass
    
    # Image metadata
    if metadata["extension"] in ['.jpg', '.jpeg', '.png', '.gif', '.bmp']:
        try:
            from PIL import Image
            with Image.open(file_path) as img:
                metadata["dimensions"] = f"{img.size[0]}x{img.size[1]}"
                metadata["image_format"] = img.format
        except:
            pass
    
    return metadata


def generate_filename(metadata: Dict[str, Any], pattern: str, 
                     ai_enhance: bool = False) -> str:
    """
    Generate new filename based on pattern and metadata.
    
    Args:
        metadata: File metadata
        pattern: Naming pattern with placeholders
        ai_enhance: Whether to use AI for content analysis
    
    Returns:
        New filename (without extension)
    """
    # AI enhancement for content analysis
    if ai_enhance and "content_preview" in metadata:
        model = get_model()
        agent = ToolCallingAgent(tools=[], model=model, max_steps=2)
        
        prompt = f"""Analyze this file content and suggest a concise descriptive name (2-4 words, no spaces, use underscores):

File type: {metadata.get('extension', 'unknown')}
First line: {metadata.get('title', metadata.get('content_preview', '')[:100])}

Return ONLY the suggested name, nothing else."""
        
        try:
            ai_name = agent.run(prompt).strip()
            # Clean the AI name
            ai_name = re.sub(r'[^\w\s-]', '', ai_name)
            ai_name = re.sub(r'[-\s]+', '_', ai_name)
            metadata["ai_suggested_name"] = ai_name[:50]
        except:
            pass
    
    # Pattern replacements
    replacements = {
        "{name}": metadata.get("stem", "file"),
        "{date}": metadata.get("modified", datetime.now().strftime("%Y-%m-%d")),
        "{created}": metadata.get("created", datetime.now().strftime("%Y-%m-%d")),
        "{ext}": metadata.get("extension", "").lstrip('.'),
        "{size}": metadata.get("size_human", "0KB").replace(" ", ""),
        "{hash}": metadata.get("hash_short", ""),
        "{ai_name}": metadata.get("ai_suggested_name", metadata.get("stem", "file")),
    }
    
    # Add dimensions for images
    if "dimensions" in metadata:
        replacements["{dims}"] = metadata["dimensions"]
    
    new_name = pattern
    for placeholder, value in replacements.items():
        new_name = new_name.replace(placeholder, str(value))
    
    # Clean up filename
    new_name = re.sub(r'_{2,}', '_', new_name)  # Remove multiple underscores
    new_name = new_name.strip('_')
    
    # Ensure valid filename
    new_name = re.sub(r'[<>:"/\\|?*]', '', new_name)
    
    return new_name


def batch_rename_files(folder_path: str, pattern: str = "{date}_{name}", 
                       file_filter: str = "*", dry_run: bool = True,
                       ai_enhance: bool = False) -> str:
    """
    Batch rename files in a folder based on content and metadata.
    
    Args:
        folder_path: Path to folder containing files
        pattern: Naming pattern with placeholders: {name}, {date}, {created}, {ext}, {size}, {hash}, {ai_name}, {dims}
        file_filter: Glob pattern to filter files
        dry_run: If True, only show what would be renamed without doing it
        ai_enhance: Use AI to analyze content for better names
    
    Returns:
        Report of renaming operations
    """
    try:
        folder = Path(folder_path)
        if not folder.exists():
            return f"Error: Folder '{folder_path}' does not exist"
        
        files = list(folder.glob(file_filter))
        files = [f for f in files if f.is_file()]
        
        if not files:
            return f"No files found in '{folder_path}' matching pattern '{file_filter}'"
        
        operations = []
        
        for file_path in files:
            try:
                metadata = extract_file_metadata(str(file_path))
                new_stem = generate_filename(metadata, pattern, ai_enhance)
                new_name = f"{new_stem}{metadata['extension']}"
                
                operations.append({
                    "original": file_path.name,
                    "new": new_name,
                    "path": str(file_path),
                    "metadata": metadata
                })
            except Exception as e:
                operations.append({
                    "original": file_path.name,
                    "error": str(e)
                })
        
        # Check for duplicates
        new_names = [op["new"] for op in operations if "new" in op]
        duplicates = [name for name in new_names if new_names.count(name) > 1]
        
        # Execute renames (or simulate)
        results = []
        for op in operations:
            if "error" in op:
                results.append(f"❌ {op['original']}: Error - {op['error']}")
                continue
            
            original_path = Path(op["path"])
            new_path = original_path.parent / op["new"]
            
            if op["new"] in duplicates:
                # Add counter for duplicates
                base = Path(op["new"]).stem
                ext = Path(op["new"]).suffix
                counter = 1
                while new_path.exists() or any(r.endswith(op["new"]) for r in results if "→" in r):
                    op["new"] = f"{base}_{counter}{ext}"
                    new_path = original_path.parent / op["new"]
                    counter += 1
            
            if not dry_run and not original_path.samefile(new_path):
                try:
                    original_path.rename(new_path)
                    status = "✅"
                except Exception as e:
                    status = f"❌ ({e})"
            else:
                status = "📝 (dry run)" if dry_run else "⏭️ (same name)"
            
            results.append(f"{status} {op['original']} → {op['new']}")
        
        # Build report
        mode = "DRY RUN" if dry_run else "EXECUTED"
        report = f"""# Batch Rename Report ({mode})

**Folder:** {folder_path}
**Pattern:** {pattern}
**Files Processed:** {len(operations)}
**AI Enhancement:** {'Enabled' if ai_enhance else 'Disabled'}

## Operations
"""
        for result in results:
            report += f"- {result}\n"
        
        if dry_run:
            report += "\n⚠️ This was a dry run. No files were actually renamed."
            report += "\nTo execute renames, add --execute flag."
        
        return report
        
    except Exception as e:
        return f"Error during batch rename: {str(e)}"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Batch rename files by content/metadata")
    parser.add_argument("folder", help="Path to folder containing files")
    parser.add_argument("--pattern", default="{date}_{name}", 
                       help="Naming pattern (placeholders: {name}, {date}, {created}, {ext}, {size}, {hash}, {ai_name}, {dims})")
    parser.add_argument("--filter", default="*", help="File filter pattern (e.g., '*.txt', '*.jpg')")
    parser.add_argument("--execute", action="store_true", help="Actually perform renames (default is dry run)")
    parser.add_argument("--ai", action="store_true", help="Use AI to analyze content for better names")
    args = parser.parse_args()
    
    report = batch_rename_files(args.folder, args.pattern, args.filter, 
                                not args.execute, args.ai)
    print(report)
