def recognize(image):
    return [{
       "type": "Carta d'Identità",
        "snapshot": image,
        "attributes": {
            "name": "",
            "id": ""
        }
    }]