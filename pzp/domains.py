from collections import OrderedDict

PROCESS_TYPES = OrderedDict(
    {
        1110: "Alluvionamento corso d'acqua minore",
        1120: "Alluvionamento corso d'acqua principale",
        1200: "Flusso detrito",
        1400: "Ruscellamento superficiale",
        2001: "Scivolamento spontaneo",
        2002: "Colata detritica di versante",
        # 3000: "Caduta sassi o blocchi",
        # 4100: "Valanga radente",
        # 4200: "Valanga polverosa",
    }
)

PROPAGATION_PROBABILITIES = OrderedDict(
    {
        1001: "Bassa",
        1002: "Media",
        1003: "Alta",
    }
)

EVENT_PROBABILITIES = OrderedDict(
    {
        1000: "Molto bassa",
        1001: "Bassa",
        1002: "Media",
        1003: "Alta",
    }
)

INTENSITIES = OrderedDict(
    {
        1000: "Nessun impatto",
        1001: "Impatto presente",
        1002: "Debole",
        1003: "Medio",
        1004: "Forte",
    }
)

DANGER_TYPES = OrderedDict(
    {
        1000: "Non in pericolo",
        1001: "Pericolo residuo",  # Light yellow
        1002: "Basso",  # Yellow
        1003: "Medio",  # Blue
        1004: "Elevato",  # Red
    }
)

DANGER_LEVELS = OrderedDict(
    {
        1000: 0,
        1001: 9,
        1002: 8,
        1003: 7,
        1004: 6,
        1005: 5,
        1006: 4,
        1007: 3,
        1008: 2,
        1009: 1,
        1010: -10,
    }
)
