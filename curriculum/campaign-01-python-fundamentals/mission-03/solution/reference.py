def dedupe_customers(customers: list[dict]) -> tuple[list[dict], set[str]]:
    seen: dict[str, dict] = {}
    domains: set[str] = set()
    for c in customers:
        if "email" not in c:
            raise ValueError("customer missing 'email' field")
        key = c["email"].lower()
        if key not in seen:
            seen[key] = c
        domains.add(key.split("@")[1])
    return list(seen.values()), domains
