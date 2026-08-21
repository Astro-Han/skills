"""Filename pattern matching for feed discovery."""


def match_glob(pattern, name):
    """Return True when name matches a shell-style pattern with * and ?."""
    return _match(pattern, 0, name, 0)


def _match(pattern, pi, name, ni):
    while pi < len(pattern):
        char = pattern[pi]
        if char == "*":
            if pi + 1 == len(pattern):
                return True
            for skip in range(ni, len(name) + 1):
                if _match(pattern, pi + 1, name, skip):
                    return True
            return False
        if ni >= len(name):
            return False
        if char != "?" and char != name[ni]:
            return False
        pi += 1
        ni += 1
    return ni == len(name)
