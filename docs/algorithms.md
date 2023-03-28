# Algoritmi

Gli algoritmi utilizzati dal plugin sono anche disponibili in QGIS
come "Algoritmi di Processing" utilizzabili singolarmente.

![Algoritmi](./assets/algoritmi.png)

## Applica matrice

![Applica matrice](./assets/algoritmo_applica_matrice.png)

### Scopo
Questo algoritmo aggiunge un campo con il valore della matrice a ogni geometria del layer con le intensità

### Parametri input
- Layer con le geometrie (intensità)
  - Campo contenente il periodo di ritorno
  - Campo contenente l'intensità
- Matrice da utilizzare (predefinita o manuale)

### Output
Viene generato un layer uguale al layer in ingresso con l'aggiunta di
un campo contenente il valore della matrice per ogni geometria.

## Correggi geometrie

![Correggi geometrie](./assets/algoritmo_correggi_geometrie.png)

## Fondi layer intensità

![Fondi layer intensità](./assets/algoritmo_fondi_intensita.png)

## Propagazione

![Propagazione](./assets/algoritmo_propagazione.png)


## Semplifica intensità

![Semplifica intensità](./assets/algoritmo_semplifica_intensita.png)

## Zone di pericolo

![Zone di pericolo](./assets/algoritmo_zone_pericolo.png)

## Zone nessun impatto

![Zone nessun impatto](./assets/algoritmo_zone_nessun_impatto.png)
