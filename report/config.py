config = {
    "weights": "percorso/ai/pesi.h5",
    "classes": {
        "Tesserino": {
            "lang": "ita",
            "min_conf": 50,
            "primaryKey": "Matricola",
            "regions": [
                {
                    "name": "Matricola",
                    "type": "regex",
                    "rule": "^\\d{6}$",
                    "needed": True
                },
                {
                    "name": "Nome",
                    "type": "box",
                    "rule": [0, 0.6, 0.2, 1],
                    "needed": False
                }
            ]
        }
    }
}
