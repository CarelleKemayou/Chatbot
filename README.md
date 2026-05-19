#  Assistant IA — Base Documentaire Interne
### Powered by Mistral + Ollama + LangChain + ChromaDB

> Un assistant intelligent qui répond à vos questions à partir de vos documents internes.
> **100% local · 100% gratuit · 100% privé **

---

## Description du projet

Cet outil permet d'interroger en langage naturel une base de documents internes (PDF, Word, Excel, CSV), sans envoyer aucune donnée sur internet. Tout fonctionne localement grâce à Ollama et au modèle Mistral.

---

##  Architecture

```
Question utilisateur
    ↓
Gradio (interface navigateur)
    ↓
LangChain (orchestrateur)
    ↓
ChromaDB (recherche vectorielle dans les documents)
    ↓
Ollama → Mistral 7B (génération de la réponse)
    ↓
Réponse + sources affichées
```

| Composant | Rôle |
|-----------|------|
| **Gradio** | Interface graphique dans le navigateur |
| **LangChain** | Connecte tous les composants ensemble |
| **ChromaDB** | Mémorise et indexe les documents (base vectorielle) |
| **Ollama** | Fait tourner le modèle IA en local |
| **Mistral 7B** | Modèle open source — génère les réponses |

---

## ⚙️ Prérequis

### Système
- OS : Windows 10/11, macOS 12+, ou Linux (Ubuntu 20.04+)
- RAM : 8 Go minimum (16 Go conseillé pour Mistral 7B)
- Stockage : 10 Go libres minimum (modèle Mistral ~4 Go + dépendances)
- Python 3.9 ou version supérieure
- Connexion internet uniquement pour l'installation initiale

### Logiciels à installer
- Python 3.9+ : https://www.python.org/downloads/
- Ollama : https://ollama.com/download

---

## Installation

### 1. Installer Ollama

Télécharger et installer depuis : **https://ollama.com/download**

Puis télécharger le modèle Mistral (une seule fois, ~4 Go) :
```bash
ollama pull mistral
```

### 2. Copier le projet

Copier le dossier du projet à l'emplacement de votre choix. La structure attendue est :

```
mon-projet/
├── app.py
├── README.md
├── base_donnees/          ← Vos documents ici
│   ├── RH/
│   ├── Finance/
│   ├── Juridique/
│   └── ...
├── chroma_db/             ← Généré automatiquement (ne pas partager)
└── .venv/                 ← Environnement Python (ne pas partager)
```

### 3. Configurer le chemin des documents

Ouvrir `app.py` et modifier la ligne suivante :

```python
# Windows
BASE_DOSSIER = r"C:\chemin\vers\votre\base_donnees"

# Mac / Linux
BASE_DOSSIER = "/chemin/vers/votre/base_donnees"
```

>  C'est le **seul paramètre obligatoire** à adapter selon votre machine.

### 4. Créer l'environnement Python

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Mac / Linux
source .venv/bin/activate
```

### 5. Installer les dépendances

```bash
pip install langchain langchain-community langchain-classic langchain-text-splitters gradio chromadb pypdf docx2txt unstructured openpyxl
```

---

## ▶️ Lancement

À chaque utilisation, suivre ces étapes dans l'ordre :

```bash
# Étape 1 — Activer l'environnement Python
.venv\Scripts\activate        # Windows
source .venv/bin/activate     # Mac / Linux

# Étape 2 — Lancer l'application
python app.py

# Étape 3 — Ouvrir le navigateur
# → http://localhost:7860
```

>  Ollama se lance automatiquement au démarrage de Windows. Si une erreur "port déjà utilisé" apparaît lors de `ollama serve`, c'est normal — il tourne déjà en arrière-plan.

---

##  Utilisation

### Indexer les documents
1. Placer les documents dans `base_donnees/`, organisés par sous-dossier
2. Aller dans l'onglet **⚙️ Indexer les documents**
3. Cliquer sur **Indexer les documents**
4. Attendre la confirmation (peut prendre plusieurs minutes selon le volume)

>  Re-indexer à chaque ajout de nouveaux documents.

### Poser une question
1. Sélectionner un département dans le menu déroulant (ou laisser "Tous")
2. Saisir la question en langage naturel
3. Cliquer sur **🔍 Poser la question**
4. La réponse s'affiche avec les sources utilisées

---

##  Formats supportés

| Format | Extension(s) |
|--------|-------------|
| PDF | `.pdf` |
| Word | `.docx` |
| Excel | `.xlsx`, `.xls` |
| CSV | `.csv` |

---

##  Paramètres configurables dans `app.py`

| Paramètre | Valeur par défaut | Description |
|-----------|------------------|-------------|
| `BASE_DOSSIER` | *(à définir)* | Chemin absolu vers le dossier des documents — **OBLIGATOIRE** |
| `CHROMA_DIR` | `./chroma_db` | Dossier de stockage de la base vectorielle |
| `model` (embeddings) | `mistral` | Modèle Ollama pour les embeddings |
| `model` (LLM) | `mistral` | Modèle Ollama pour générer les réponses |
| `chunk_size` | `500` | Taille des morceaux de texte pour l'indexation |
| `chunk_overlap` | `50` | Chevauchement entre les morceaux |
| `k` (résultats) | `5` | Nombre de passages récupérés par requête |
| `server_port` | `7860` | Port de l'interface Gradio |

---

## Commandes Ollama utiles

```bash
ollama serve          # Démarrer le serveur manuellement
ollama pull mistral   # Télécharger Mistral 7B
ollama pull llama3    # Télécharger Llama 3 (alternative)
ollama list           # Lister les modèles installés
ollama run mistral    # Tester Mistral en ligne de commande
ollama ps             # Voir les modèles en cours d'exécution
ollama rm mistral     # Supprimer le modèle
```

---

##  Dépannage

| Problème | Solution |
|----------|----------|
| `ModuleNotFoundError` | Activer le `.venv` puis relancer `pip install ...` |
| `ERR_ADDRESS_INVALID` dans le navigateur | Utiliser `http://localhost:7860` et non `http://0.0.0.0:7860` |
| `ollama serve` — port déjà utilisé | Normal : Ollama tourne déjà en arrière-plan |
| Aucun document trouvé | Vérifier le chemin `BASE_DOSSIER` dans `app.py` |
| Réponse lente au premier appel | Normal : Mistral charge en mémoire — patienter |
| `ImportError` sur `RetrievalQA` | Remplacer `langchain.chains` par `langchain_classic.chains` |
| Erreur sur fichier Excel | Vérifier que `unstructured` et `openpyxl` sont bien installés |

---

##  Cadre juridique

| Obligation | Statut | Remarque |
|-----------|--------|----------|
| **RGPD** | Conforme | Aucune donnée ne quitte la machine locale |
| **Cloud Act américain** |  Non concerné | Modèle 100% local, sans dépendance étrangère |
| **ANSSI** |  Solution souveraine | Diagnostic MonAideCyber disponible |
| **Fiche registre CNIL** |  À créer | À déposer auprès de votre DPO |
| **AI Act européen** |  Risque faible | Assistant documentaire interne |

---

##  Déploiement serveur (optionnel)

Pour rendre l'application accessible à plusieurs utilisateurs sur un réseau interne :

| Nb utilisateurs | Modèle conseillé | Matériel indicatif | Budget estimé |
|----------------|-----------------|-------------------|---------------|
| 1 – 5 | Mistral 7B | Mac Mini M4 24 Go RAM | ~950 € |
| 5 – 15 | Mistral 13B | Serveur + RTX 4090 | ~2 500 € |
| 15 – 30 | Llama 3 70B | Serveur + 2x RTX 3090 | ~5 000 € |

Stack recommandée en production :
```
Ollama + Open WebUI + ChromaDB + Docker Compose + Reverse proxy HTTPS
```

---

*Documentation technique — Usage interne uniquement*
