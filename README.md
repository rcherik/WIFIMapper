# Pcap parser

## Installation

```
sudo apt-get update && sudo apt-get upgrade && sudo apt-get install python python-pip python-scapy && sudo pip install flask
```

## How to run
```
python application.py <pcap_files>
```

Puis se connecter sur 127.0.0.1:5000

## Fichiers pcap

**Vous avez trois fichier dans Pcap_traces:**
	- single_wap.pcap qui montre un seul handshake réussi avec plusieurs retransmissions pour le step4 puis une désauthentification, enlevant le bssid
	- double_wpa_and_fail.pcap qui montre deux handshakes réussis ainsi qu'un raté
	- unknown_ap.pcap qui montre les access points trop loins pour recevoir les beacons mais quand même repérés dans les paquets (aucun handshake)

## Features

- Les panel Access Point et Station peuvent collapse en cliquant dessus
- Vous pouvez trier tous les champs des tables
- Vous pouvez télécharger les handshake de tout le fichier sous le panel des Stations
- Le champ handshake dans les stations permet de savoir si un handshake a été réussi et vous pouvez, en cliquant, télécharger tous les handshakes pour cette station
- En cliquant sur le + à côté d'une station vous aurez le détail des frames échangées avec des access points ainsi que tous les steps du handshake wpa qu'ils aient aboutis ou non, les fails (voir Rapport) et les réussites que vous pouvez télécharger uniquement pour cette station avec cet access point
- Si les champs wpa sont vide alors aucune tentative de connexion, déconnexion ou steps de wpa handshake n'a été faite, sinon des 0 sont affichés
- En cliquant sur Open dans la modale que vous venez d'ouvrir vous serez redirigé sur une autre page contenant des informations sur les paquets échangés entre la station et l'access point
- Si des stations sont présentes et n'ont aucun paquets envoyés ou reçu alors ils ont été ajoutés grâce à leurs probe requests
