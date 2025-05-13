from pathlib import Path

def get_output_path(input_path: str, target_format: str) -> str:
    p = Path(input_path)
    return str(p.with_suffix(f'.{target_format}'))
