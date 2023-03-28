# Plugin


## Installazione

Per installare il plugin in QGIS è necessario aggiungere un nuovo
repository dei plugin in QGIS:

È possibile aggiungere il repository andando nel menu *Plugins -> Gestisci ed Installa Plugin...*

![Aggiungere repository](./assets/repository_plugin.png)

```
https://download.opengis.ch/repos/ticino/plugins.xml
```

A questo punto è possibile installare il plugin chiamato `pzp`.

!!! Note
    Richiede QGIS 3.16 o superiore


## Funzionalità

Le funzionalità del plugin sono accessibili tramite la toolbar del plugin.

![Toolbar](./assets/toolbar.png)

In particolare tramite la toolbar è possibile:
- aggiungere un nuovo processo con i relativi layer al progetto QGIS attuale
- aggiungere dei layer con dati di base o mappe di base
- eseguire il calcolo delle zone di pericolo
- eseguire il calcolo delle zone di nessun impatto
- modificare il valore delle zone di pericolo che hanno possibilità multiple
- consultare questo manuale

### Aggiunta dei layer per la registrazione di un processo al progetto QGIS

Tramite il pulsante "Aggiuni proceso" è possible aggiungere al
progetto QGIS attuale un nuovo gruppo contenente i layer per
digitalizzare le intensità.

Viene chiesto il percorso di una directory in cui salvare i dati (in
formato GeoPackage) e il tipo di processo da aggiungere. Il processo
che viene aggiunto consiste in un gruppo di layer.

![Aggiungi processo](./assets/aggiungi_processo.gif)

### Aggiunta di layer con dati o mappe di base

Tramite i pulsanti "Aggiungi mappa base" e "Aggiungi dati base" è
possibile aggiungere al progetto QGIS attuale i layer contenenti le
mappe di base o i layer di base.

![Aggiungi dati_base](./assets/aggiungi_dati_base.gif)

### Digitalizzazione delle geometrie

#### Area di studio

#### Intensità

#### Probabilità di propagazione

#### Probabilità di rottura

### Calcolo delle zone di pericolo

![Calcolo zone di pericolo](./assets/calcolo_zone_pericolo.gif)

### Calcolo delle zone di nessun impatto

![Calcolo zone di nessun impatto](./assets/calcolo_nessun_impatto.gif)

### Modifica delle zone con possibilità multiple

![Modifica zone con possibilità multiple](./assets/modifica_possibilita_multiple.gif)

### Ottenere informazioni
