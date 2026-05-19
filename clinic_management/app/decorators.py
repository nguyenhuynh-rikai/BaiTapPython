"""
MediFlow — core/decorators.py
==============================
4 decorators dùng xuyên suốt toàn bộ project:

  @audit_action(action)    — ghi AuditLog trước/sau khi method chạy
  @log_execution           — đo thời gian + log kết quả / exception
  @require_role(*roles)    — kiểm tra quyền trước khi thực thi
  @cache_result(ttl, key)  — cache kết quả vào Redis / memory fallback
"""

import functools
import hashlib
import json
import logging
import time
from typing import Callable, Optional

from django.core.cache import cache
from django.utils import timezone

logger = logging.getLogger("mediflow.core")


def audit_action(action: str, model_name: str = ""):
  
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            import inspect
            from django.db.models import Model

            # Lấy user từ kwargs hoặc positional args
            user = kwargs.get("user")
            if user is None:
                sig = inspect.signature(func)
                params = list(sig.parameters.keys())
                for i, name in enumerate(params):
                    if name == "user" and i < len(args):
                        user = args[i]
                        break

            # Tìm instance Django model đầu tiên trong args (bỏ qua self)
            instance = None
            object_id = None
            before_state = {}
            for arg in args[1:]:
                if isinstance(arg, Model):
                    instance = arg
                    object_id = arg.pk
                    # Snapshot trạng thái trước
                    before_state = {
                        f: str(v) for f, v in
                        instance.__dict__.items()
                        if not f.startswith("_")
                    }
                    break

            # Chạy function thực sự
            result = func(*args, **kwargs)

            # Snapshot trạng thái sau
            after_state = {}
            if instance is not None:
                try:
                    instance.refresh_from_db()
                    after_state = {
                        f: str(v) for f, v in
                        instance.__dict__.items()
                        if not f.startswith("_")
                    }
                except Exception:
                    pass

            diff = {
                "before": {k: before_state[k] for k in before_state if before_state.get(k) != after_state.get(k)},
                "after":  {k: after_state[k]  for k in after_state  if before_state.get(k) != after_state.get(k)},
            }

            # Ghi AuditLog — import lazy để tránh circular import
            try:
                from .models import AuditLog
                AuditLog.objects.create(
                    user=user if hasattr(user, "pk") else None,
                    action=action,
                    model_name=model_name or (instance.__class__.__name__ if instance else ""),
                    object_id=object_id,
                    diff=diff,
                )
            except Exception as e:
                # Không để lỗi audit làm hỏng luồng chính
                logger.warning("audit_action failed to write log: %s", e)

            return result

        return wrapper
    return decorator


def log_execution(func: Optional[Callable] = None, *, level: str = "DEBUG"):
  
    def decorator(fn: Callable) -> Callable:
        log_fn = getattr(logger, level.lower(), logger.debug)

        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            start = time.perf_counter()
            qualname = fn.__qualname__

            log_fn("→ START  %s", qualname)
            try:
                result = fn(*args, **kwargs)
                elapsed = (time.perf_counter() - start) * 1000
                log_fn("← OK     %s  (%.1f ms)", qualname, elapsed)
                return result
            except Exception as exc:
                elapsed = (time.perf_counter() - start) * 1000
                logger.exception(
                    "✗ ERROR  %s  (%.1f ms) — %s: %s",
                    qualname, elapsed, type(exc).__name__, exc,
                )
                raise

        return wrapper

    # Hỗ trợ dùng không có tham số: @log_execution
    if func is not None:
        return decorator(func)
    return decorator


class PermissionDeniedError(PermissionError):
    """Raise khi user không có quyền thực hiện thao tác."""
    pass


def require_role(*allowed_roles: str):


    def decorator(func: Callable) -> Callable:
        import inspect

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Lấy user
            user = kwargs.get("user")
            if user is None:
                sig = inspect.signature(func)
                params = list(sig.parameters.keys())
                for i, name in enumerate(params):
                    if name == "user" and i < len(args):
                        user = args[i]
                        break

            if user is None:
                raise ValueError(
                    f"@require_role: không tìm thấy tham số 'user' trong {func.__qualname__}"
                )

            user_role = getattr(user, "role", None)
            if user_role not in allowed_roles:
                raise PermissionDeniedError(
                    f"Hành động '{func.__qualname__}' yêu cầu role {allowed_roles}, "
                    f"nhưng user '{user}' có role '{user_role}'."
                )

            return func(*args, **kwargs)

        # Lưu metadata để test / introspect dễ hơn
        wrapper._allowed_roles = allowed_roles
        return wrapper

    return decorator

_MEMORY_CACHE: dict = {}   # fallback nếu Redis không sẵn sàng


def cache_result(ttl: int = 300, key_prefix: str = ""):

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            no_cache         = kwargs.pop("no_cache", False)
            invalidate        = kwargs.pop("invalidate_cache", False)

            # Tạo cache key
            raw = json.dumps(
                {"args": [str(a) for a in args], "kwargs": {k: str(v) for k, v in kwargs.items()}},
                sort_keys=True,
            )
            key_hash = hashlib.md5(raw.encode()).hexdigest()[:12]
            cache_key = f"mediflow:{key_prefix or func.__qualname__}:{key_hash}"

            # Invalidate
            if invalidate:
                cache.delete(cache_key)
                _MEMORY_CACHE.pop(cache_key, None)
                logger.debug("cache_result: invalidated %s", cache_key)

            if no_cache or invalidate:
                return func(*args, **kwargs)

            # Thử lấy từ Redis
            try:
                cached = cache.get(cache_key)
                if cached is not None:
                    logger.debug("cache_result: HIT  %s", cache_key)
                    return cached
            except Exception:
                # Redis down → thử memory cache
                if cache_key in _MEMORY_CACHE:
                    entry = _MEMORY_CACHE[cache_key]
                    if time.time() < entry["expires"]:
                        logger.debug("cache_result: MEMORY HIT  %s", cache_key)
                        return entry["value"]

            # Cache miss → chạy function
            result = func(*args, **kwargs)

            # Lưu vào Redis
            try:
                cache.set(cache_key, result, ttl)
                logger.debug("cache_result: SET  %s  (ttl=%ds)", cache_key, ttl)
            except Exception:
                # Redis down → lưu vào memory
                _MEMORY_CACHE[cache_key] = {
                    "value": result,
                    "expires": time.time() + ttl,
                }
                logger.warning("cache_result: Redis unavailable, using memory for %s", cache_key)

            return result

        return wrapper
    return decorator