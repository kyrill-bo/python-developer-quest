"""Mission: Resilient Batch Importer."""


def import_batch(records: list[dict]) -> tuple[list[dict], list[dict]]:
    # TODO: validate each record independently; collect valid records and
    # {"record":..., "reason":...} entries for invalid ones. Never abort
    # the whole batch on one bad record.
    raise NotImplementedError
