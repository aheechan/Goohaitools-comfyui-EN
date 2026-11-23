"""English option-value localization for the Goohai node pack.

ComfyUI renders combo widget entries exactly as they are returned by
``INPUT_TYPES``.  Translating those values would normally change what gets
stored in a workflow and what the node receives, so this module keeps the
original Chinese values as the canonical, executable values:

* ``INPUT_TYPES`` is wrapped and its dropdown options are returned in English.
* The selected English value is mapped back to the original Chinese value
  before ``FUNCTION`` runs, so every node keeps working unchanged.
* ``VALIDATE_INPUTS`` is made lenient so workflows saved with the original
  Chinese values (upstream or older exports) still load and run.

The translation table lives in ``locales/en/option_values.json``.
"""

from __future__ import annotations

import inspect
import json
import logging
from pathlib import Path

LOGGER = logging.getLogger(__name__)

_TABLE_PATH = Path(__file__).parent / "locales" / "en" / "option_values.json"

# Boolean widget captions are display-only; no value mapping is needed.
_LABEL_MAP = {
    "开": "On",
    "关": "Off",
    "包含子文件夹": "Include Subfolders",
    "阻断": "Block",
    "通过": "Pass",
}

# Placeholder text is display-only as well.
_PLACEHOLDER_MAP = {
    "请输入字符串": "Enter a string",
    "分隔符，默认为空格": "Delimiter, defaults to a space",
    "例如: a+b*c, round(c/a)": "e.g. a+b*c, round(c/a)",
    "例如: (a+c-d*f)//2": "e.g. (a+c-d*f)//2",
}

try:
    VALUE_MAP: dict[str, str] = json.loads(_TABLE_PATH.read_text(encoding="utf-8"))
except Exception:  # pragma: no cover - missing/broken file should not break the pack
    LOGGER.warning("[GoohaiTools] could not load %s, option values stay untranslated", _TABLE_PATH)
    VALUE_MAP = {}


def _translate_list(values, maps, name):
    """Translate a dropdown option list and record the English -> Chinese map."""
    out = []
    reverse = {}
    changed = False
    for value in values:
        if isinstance(value, str) and value in VALUE_MAP:
            english = VALUE_MAP[value]
            if english in reverse and reverse[english] != value:
                # Two originals would collapse into one label: keep them apart.
                english = "%s (%s)" % (english, value)
            reverse[english] = value
            out.append(english)
            changed = True
        else:
            out.append(value)
    if changed:
        existing = maps.setdefault(name, {})
        existing.update(reverse)
    return out, changed


def _translate_entry(entry, maps, name):
    """Return a copy of a single INPUT_TYPES entry with English option labels."""
    if not isinstance(entry, (tuple, list)) or not entry:
        return entry

    head = entry[0]
    options = entry[1] if len(entry) > 1 and isinstance(entry[1], dict) else None
    changed = False

    if isinstance(head, list):
        head, changed = _translate_list(head, maps, name)
    elif isinstance(head, tuple) and all(isinstance(item, str) for item in head):
        new_list, changed = _translate_list(list(head), maps, name)
        head = tuple(new_list)
    elif head == "COMBO" and options and isinstance(options.get("options"), list):
        new_list, changed = _translate_list(options["options"], maps, name)
        options = dict(options)
        options["options"] = new_list

    if options is not None:
        options = dict(options)
        default = options.get("default")
        if isinstance(default, str) and default in VALUE_MAP:
            options["default"] = VALUE_MAP[default]
            changed = True
        for key in ("label_on", "label_off"):
            value = options.get(key)
            if isinstance(value, str) and value in _LABEL_MAP:
                options[key] = _LABEL_MAP[value]
                changed = True
        placeholder = options.get("placeholder")
        if isinstance(placeholder, str) and placeholder in _PLACEHOLDER_MAP:
            options["placeholder"] = _PLACEHOLDER_MAP[placeholder]
            changed = True

    if not changed:
        return entry

    rest = list(entry[1:])
    if rest and isinstance(rest[0], dict):
        rest[0] = options
    return tuple([head] + rest)


def _remap(kwargs, maps):
    """Map English option values back to the original Chinese values."""
    if not maps:
        return kwargs
    result = dict(kwargs)
    for name, value in kwargs.items():
        reverse = maps.get(name)
        if reverse and isinstance(value, str) and value in reverse:
            result[name] = reverse[value]
    return result


_SIGNATURES = {}


def _invoke(original, args, kwargs, maps):
    """Call a node function after translating option values (positional or keyword)."""
    try:
        signature = _SIGNATURES.get(original)
        if signature is None:
            signature = inspect.signature(original)
            _SIGNATURES[original] = signature
        bound = signature.bind_partial(*args, **kwargs)
    except (TypeError, ValueError):
        return original(*args, **_remap(kwargs, maps))

    for name, value in list(bound.arguments.items()):
        reverse = maps.get(name)
        if reverse and isinstance(value, str) and value in reverse:
            bound.arguments[name] = reverse[value]
            continue
        parameter = signature.parameters.get(name)
        if parameter is not None and parameter.kind == parameter.VAR_KEYWORD and isinstance(value, dict):
            remapped = dict(value)
            for key, item in value.items():
                item_reverse = maps.get(key)
                if item_reverse and isinstance(item, str) and item in item_reverse:
                    remapped[key] = item_reverse[item]
            bound.arguments[name] = remapped
    return original(*bound.args, **bound.kwargs)


def _check_option_values(cls, kwargs):
    """Reject values that are neither the English label nor the original value."""
    maps = getattr(cls, "_gh_option_maps", {})
    for name, value in kwargs.items():
        reverse = maps.get(name)
        if not reverse or not isinstance(value, str):
            continue
        allowed = set(reverse) | set(reverse.values())
        if value not in allowed:
            return "%s: %r not in %s" % (name, value, sorted(allowed))
    return None


def _install_lenient_validator(cls):
    """Let combo validation accept both English and legacy Chinese values."""
    if getattr(cls, "_gh_lenient_validator", False):
        return
    existing = cls.__dict__.get("VALIDATE_INPUTS")

    if existing is None:
        def VALIDATE_INPUTS(cls_, **kwargs):
            problem = _check_option_values(cls_, kwargs)
            return problem if problem else True

        cls.VALIDATE_INPUTS = classmethod(VALIDATE_INPUTS)
        cls._gh_lenient_validator = True
        return

    if isinstance(existing, (classmethod, staticmethod)):
        original = existing.__func__
    else:
        original = existing
    try:
        signature = inspect.signature(original)
    except (TypeError, ValueError):
        return
    accepted = [
        p.name for p in signature.parameters.values()
        if p.name != "cls" and p.kind in (p.POSITIONAL_OR_KEYWORD, p.KEYWORD_ONLY)
    ]
    has_var_kw = any(p.kind == p.VAR_KEYWORD for p in signature.parameters.values())

    def VALIDATE_INPUTS(cls_, **kwargs):
        problem = _check_option_values(cls_, kwargs)
        if problem:
            return problem
        remapped = _remap(kwargs, getattr(cls_, "_gh_option_maps", {}))
        if has_var_kw:
            return original(cls_, **remapped)
        subset = {name: remapped[name] for name in accepted if name in remapped}
        return original(cls_, **subset)

    cls.VALIDATE_INPUTS = classmethod(VALIDATE_INPUTS)
    cls._gh_lenient_validator = True


def _install_function_wrapper(cls, maps):
    function_name = getattr(cls, "FUNCTION", None)
    if not function_name:
        return
    descriptor = cls.__dict__.get(function_name)
    if descriptor is None or getattr(cls, "_gh_function_wrapped", False):
        return

    if isinstance(descriptor, staticmethod):
        original = descriptor.__func__

        def wrapper(*args, **kwargs):
            return _invoke(original, args, kwargs, maps)

        setattr(cls, function_name, staticmethod(wrapper))
    elif isinstance(descriptor, classmethod):
        original = descriptor.__func__

        def wrapper(cls_, *args, **kwargs):
            return _invoke(original, (cls_,) + args, kwargs, maps)

        setattr(cls, function_name, classmethod(wrapper))
    else:
        original = descriptor
        if inspect.iscoroutinefunction(original):
            async def wrapper(self, *args, **kwargs):
                return await _invoke(original, (self,) + args, kwargs, maps)
        else:
            def wrapper(self, *args, **kwargs):
                return _invoke(original, (self,) + args, kwargs, maps)

        setattr(cls, function_name, wrapper)
    cls._gh_function_wrapped = True


def _wrap_class(cls):
    if getattr(cls, "_gh_options_wrapped", False):
        return
    descriptor = cls.__dict__.get("INPUT_TYPES")
    if descriptor is None:
        return
    original = descriptor.__func__ if isinstance(descriptor, classmethod) else descriptor
    maps = {}
    cls._gh_option_maps = maps

    @classmethod
    def INPUT_TYPES(cls_, *args, **kwargs):
        spec = original(cls_, *args, **kwargs)
        result = {}
        for group, items in spec.items():
            if group not in ("required", "optional") or not isinstance(items, dict):
                result[group] = items
                continue
            translated = {}
            for name, entry in items.items():
                translated[name] = _translate_entry(entry, maps, name)
            result[group] = translated
        if maps and not getattr(cls_, "_gh_options_active", False):
            cls_._gh_options_active = True
            _install_function_wrapper(cls_, maps)
            _install_lenient_validator(cls_)
        return result

    cls.INPUT_TYPES = INPUT_TYPES
    cls._gh_options_wrapped = True


def apply_english_options(class_mappings):
    """Wrap every registered node class so dropdown values display in English."""
    if not VALUE_MAP:
        return
    count = 0
    for cls in set(class_mappings.values()):
        try:
            _wrap_class(cls)
            count += 1
        except Exception as exc:  # pragma: no cover - keep loading no matter what
            LOGGER.warning("[GoohaiTools] option localization skipped for %s: %s", cls, exc)
    LOGGER.info("[GoohaiTools] English option values enabled for %s node classes", count)
