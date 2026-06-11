CENTRALE_NAME_MAP = {
    "BLAYAIS": "BLAYAIS (LE)",
    "BUGEY": "BUGEY (LE)",
    "CHINON": "CHINON B",
    "CHOOZ": "CHOOZ B",
    "DAMPIERRE": "DAMPIERRE-EN-BURLY",
    "NOGENT": "NOGENT-SUR-SEINE",
    "ST ALBAN": "ST-ALBAN-ST-MAURICE",
    "ST LAURENT": "ST-LAURENT-DES-EAUX B",
    "TRICASTIN": "TRICASTIN (LE)",
}


def normalize_centrale(nom_tranche):
    centrale = nom_tranche.rsplit(" ", 1)[0]
    return CENTRALE_NAME_MAP.get(centrale, centrale)
