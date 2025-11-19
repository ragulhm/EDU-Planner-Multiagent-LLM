"""Simple caching utilities to reduce LLM load."""
import functools
from typing import Any, Callable
import json
import time
from pathlib import Path

def get_cache_path() -> Path:
    """Return the cache directory path, creating if needed."""
    cache_dir = Path(__file__).resolve().parents[2] / 'cache'
    cache_dir.mkdir(parents=True, exist_ok=True)
    return cache_dir

def cache_llm(ttl_seconds: int = 3600) -> Callable:
    """Cache LLM responses to reduce API calls and load.
    
    Args:
        ttl_seconds: Cache lifetime in seconds (default: 1 hour)
    """
    def decorator(func: Callable) -> Callable:
        cache = {}  # in-memory cache
        cache_file = get_cache_path() / f"{func.__name__}_cache.json"
        
        # Load existing cache from disk
        if cache_file.exists():
            try:
                saved = json.loads(cache_file.read_text(encoding='utf-8'))
                # Filter out expired entries
                now = time.time()
                cache.update({
                    k: v for k, v in saved.items()
                    if v.get('timestamp', 0) + ttl_seconds > now
                })
            except Exception:
                pass
        
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            # Create cache key from args/kwargs
            key = json.dumps({'args': args, 'kwargs': kwargs}, sort_keys=True)
            
            now = time.time()
            if key in cache:
                entry = cache[key]
                if entry['timestamp'] + ttl_seconds > now:
                    return entry['result']
                
            # Cache miss or expired: call function
            result = func(*args, **kwargs)
            cache[key] = {'result': result, 'timestamp': now}
            
            # Save to disk (keep only fresh entries)
            fresh = {
                k: v for k, v in cache.items()
                if v['timestamp'] + ttl_seconds > now
            }
            try:
                cache_file.write_text(
                    json.dumps(fresh, indent=2),
                    encoding='utf-8'
                )
            except Exception:
                pass  # disk cache is optional
            
            return result
        return wrapper
    return decorator