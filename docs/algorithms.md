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

### Scopo
Questo algoritmo cerca di correggere gli errori più frequenti di digitalizzazione delle geometrie.

Vengono eseguiti in particolare eseguite le seguenti operazioni:

- Aggancia punti al reticolo (con reticolo di 1mm)
- Creazione e rimozione di un buffer negativo molto piccolo (1e-06 m) per rimuovere "sbavature" delle geometrie
- Rimozione delle aree con superficie inferiore a 1m<sup>2</sup>
- Rimozione dei buchi con superficie maggiore a 1m<sup>2</sup>

### Parametri input
- Layer con le geometrie

### Ouptut
Viene generato un layer con le geometrie corrette mantenendo gli attributi delle geometrie iniziali.

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
