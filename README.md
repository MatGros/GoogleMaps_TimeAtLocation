# 📍 Google Maps - Time At Location Analyzer

[![Python](https://img.shields.io/badge/Python-3.x-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Google Maps](https://img.shields.io/badge/Google%20Maps-Takeout-green.svg)](https://takeout.google.com/)

> **Analyseur de localisation Google Maps** : Calcule le temps passé à des emplacements spécifiques à partir de vos données Google Maps Timeline (Google Takeout).

---

## 📖 Description

Ce projet Python permet d'analyser les données de localisation Google Maps (exportées via Google Takeout) pour calculer le temps total passé à des emplacements spécifiques. Le script parcourt vos données de timeline, identifie les visites à des adresses cibles ou dans un rayon géographique défini, et génère un rapport CSV détaillé.

### ✨ Fonctionnalités

- 📊 **Analyse temporelle** : Calcule le temps passé par jour et par mois à vos localisations cibles
- 🎯 **Ciblage flexible** : Filtrage par adresse texte ou coordonnées géographiques (latitude/longitude)
- 📍 **Rayon géographique** : Recherche dans un rayon configurable (en mètres) autour d'un point
- 🗓️ **Support multi-mois** : Traite automatiquement les données JSON mensuelles d'une année complète
- 🔄 **Cibles multiples** : Supporte jusqu'à deux emplacements cibles simultanément
- 📁 **Export CSV** : Génère un fichier CSV lisible avec toutes les statistiques
- 🌍 **Calcul précis** : Utilise la formule Haversine pour les distances géographiques

---

## 🔧 Prérequis

- **Python 3.x**
- Modules Python standard (aucune dépendance externe requise) :
  - `json`
  - `datetime`
  - `os`
  - `csv`
  - `math`

---

## 📥 Installation

1. Clonez ce dépôt :
```bash
git clone https://github.com/MatGros/GoogleMaps_TimeAtLocation.git
cd GoogleMaps_TimeAtLocation
```

2. Exportez vos données Google Maps :
   - Rendez-vous sur [Google Takeout](https://takeout.google.com/)
   - Sélectionnez **"Historique des positions"** (Location History)
   - Choisissez le format **JSON**
   - Téléchargez et extrayez l'archive

3. Organisez vos données :
```
GoogleMaps_TimeAtLocation/
├── GoogleMaps_TimeAtlocation_v0.9.py
└── GoogleMaps_TimeAtlocation_JsonData/
    └── 2014/  (ou votre année)
        ├── 2014_JANUARY.json
        ├── 2014_FEBRUARY.json
        ├── 2014_MARCH.json
        └── ...
```

---

## ⚙️ Configuration

Avant d'exécuter le script, configurez les paramètres dans la section **"Main"** du fichier Python :

### 🎯 Définir l'emplacement cible

```python
# Numéro de la cible dans la liste (0-5)
TargetNumber = 1

# Activer une deuxième cible (0 = désactivé, 1 = activé)
EnableSecondTarget = 1
SecondTargetNumber = 4

# Liste des adresses cibles
TargetAdressList = [
    'nofilter',                          # 0 - Aucun filtre
    'Parade, 30200 Orsan',               # 1
    'Méditerranée, 30132 Caissargues',   # 2
    'Genêts, 30132 Caissargues',         # 3
    'Galilée, 13310 Saint-Martin-de-Crau', # 4
    '?'                                   # 5 - À définir
]

# Coordonnées GPS correspondantes (latitude)
Target_latList = [
    0,                    # nofilter
    44.13860983334649,    # Orsan
    43.78764719820701,    # Caissargues - Méditerranée
    43.787566701084096,   # Caissargues - Genêts
    43.64180566129205,    # Saint-Martin-de-Crau
    0
]

# Coordonnées GPS correspondantes (longitude)
Target_lngList = [
    0,
    4.657463254390843,
    4.386207165386871,
    4.391149034481557,
    4.795406268735807,
    0
]

# Rayon de recherche en mètres
radius = 200  # 200 mètres par défaut
```

### 📅 Définir l'année à analyser

```python
Year = 2014  # Modifiez selon vos données
```

---

## 🚀 Utilisation

Exécutez le script Python :

```bash
python GoogleMaps_TimeAtlocation_v0.9.py
```

Le script va :
1. 🔍 Parcourir tous les fichiers JSON mensuels de l'année spécifiée
2. 📊 Filtrer les visites correspondant à vos critères
3. ⏱️ Calculer les temps de présence par jour et par mois
4. 💾 Générer le fichier `GoogleMaps_TimeAtlocation.csv`

### 📤 Format de sortie CSV

Le fichier généré contient les colonnes suivantes :

| Colonne | Description |
|---------|-------------|
| `Address` | Adresse complète de la localisation |
| `End_time` | Date et heure de fin de visite (format ISO 8601) |
| `Year` | Année |
| `Month` | Numéro du mois (1-12) |
| `Day` | Jour du mois |
| `TotalHoursPerDay` | Temps total passé ce jour-là (format HH:MM:SS) |
| `TotalHoursPerMonth` | Temps total cumulé pour le mois (format HH:MM:SS) |

**Exemple de sortie :**
```csv
Address;End_time;Year;Month;Day;TotalHoursPerDay;TotalHoursPerMonth
Route de la Parade. 30200 Orsan. France;2014-02-20T14:35:02.591Z;2014;2;20;05:37:56;15:45:32
Route de la Parade. 30200 Orsan. France;2014-02-21T17:14:14.980Z;2014;2;21;09:31:29;25:16:61
```

---

## 📊 Exemple d'utilisation

### Cas d'usage : Calculer le temps passé au bureau

1. Trouvez les coordonnées GPS de votre bureau (via Google Maps)
2. Ajoutez l'adresse et les coordonnées dans les listes de configuration
3. Définissez un rayon approprié (ex: 200m pour inclure les bâtiments voisins)
4. Exécutez le script pour obtenir vos statistiques de présence

### Cas d'usage : Analyser plusieurs localisations

Activez `EnableSecondTarget = 1` pour suivre deux emplacements simultanément (par exemple : bureau principal et site secondaire).

---

## 🔬 Fonctionnement technique

### Algorithme de calcul de distance

Le script utilise la **formule Haversine** pour calculer la distance orthodromique (great-circle distance) entre deux points géographiques :

```python
def Dist2Geopoints(target_lat, target_lng, lat, lng):
    # Conversion degrés → radians
    # Calcul de distance avec formule Haversine
    # Retourne la distance en mètres
```

### Structure des données Google Takeout

Les fichiers JSON contiennent un objet `timelineObjects` avec :
- `placeVisit` : Visites de lieux
  - `location` : Coordonnées et adresse
  - `duration` : Timestamps de début et fin
- `activitySegment` : Déplacements (non traités par ce script)

---

## 📝 Notes importantes

- ⚠️ **Vie privée** : Vos données de localisation sont sensibles. Ne partagez jamais vos fichiers JSON publiquement.
- 📏 **Précision** : La précision dépend de la qualité des données Google Maps (GPS, Wi-Fi, tours cellulaires).
- 🗓️ **Format de dates** : Le script attend des fichiers nommés `YYYY_MONTHNAME.json` (ex: `2014_JANUARY.json`).
- 🔧 **Personnalisation** : Le code est documenté en français pour faciliter les modifications.

---

## 🤝 Contribution

Ce projet est un projet personnel archivé. Le code n'est plus activement maintenu mais reste disponible pour référence et réutilisation.

---

## 📄 Licence

Ce projet est sous licence **MIT** - voir le fichier [LICENSE](LICENSE) pour plus de détails.

---

## 👤 Auteur

**MatGros**

- GitHub: [@MatGros](https://github.com/MatGros)

---

## 🙏 Remerciements

- Google Takeout pour l'export des données de localisation
- La communauté Python pour les outils et bibliothèques standards

---

## 📚 Ressources

- [Google Takeout](https://takeout.google.com/) - Exportez vos données Google
- [Documentation formule Haversine](https://en.wikipedia.org/wiki/Haversine_formula)
- [Format JSON Timeline Google](https://locationhistoryformat.com/)

---

<div align="center">
  
**⭐ Si ce projet vous a été utile, n'hésitez pas à lui donner une étoile ! ⭐**

</div>
