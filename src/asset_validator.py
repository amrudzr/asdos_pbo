import os
import re
from typing import Tuple, List

def get_files_with_extensions(directory: str, extensions: Tuple[str, ...]) -> List[str]:
    """Helper to list files in a directory with specific extensions."""
    if not os.path.exists(directory):
        return []
    valid_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(extensions):
                valid_files.append(file)
    return valid_files

def validate_assets(source_dir: str) -> Tuple[int, int, List[str]]:
    """
    Validates assets in a Greenfoot project directory.
    Returns: (image_count, sound_count, missing_assets)
    """
    image_exts = ('.png', '.jpg', '.jpeg', '.gif', '.bmp')
    sound_exts = ('.wav', '.mp3', '.au', '.aiff', '.mid', '.midi')
    
    images_dir = os.path.join(source_dir, 'images')
    sounds_dir = os.path.join(source_dir, 'sounds')
    
    # Collect all available assets
    available_images = get_files_with_extensions(images_dir, image_exts)
    available_sounds = get_files_with_extensions(sounds_dir, sound_exts)
    
    # Include assets in the root folder as well, just in case they put them there
    available_root = []
    if os.path.exists(source_dir):
        for file in os.listdir(source_dir):
            if os.path.isfile(os.path.join(source_dir, file)) and file.lower().endswith(image_exts + sound_exts):
                available_root.append(file)
    
    all_available_assets = set(available_images + available_sounds + available_root)
    
    image_count = len(available_images)
    sound_count = len(available_sounds)
    
    # Analyze .java files for asset references
    missing_assets = []
    referenced_assets = set()
    
    # Regex to match string literals that look like media filenames
    # Example: "hero.png", "bg.mp3"
    asset_regex = re.compile(r'"([^"]+\.(?:png|jpg|jpeg|gif|bmp|wav|mp3|au|aiff|mid|midi))"', re.IGNORECASE)
    
    for root, _, files in os.walk(source_dir):
        for file in files:
            if file.endswith('.java'):
                path = os.path.join(root, file)
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        matches = asset_regex.findall(content)
                        for match in matches:
                            # In Greenfoot, it's usually just the filename without path, 
                            # but sometimes they might write "images/hero.png"
                            basename = os.path.basename(match)
                            referenced_assets.add(basename)
                except Exception:
                    pass
                    
    # Check for missing assets
    for asset in referenced_assets:
        if asset not in all_available_assets:
            missing_assets.append(asset)
            
    return image_count, sound_count, list(set(missing_assets))
