# 📚 Assistant IA — Base Documentaire Interne
### Mairie de Villeneuve-les-Prés · Powered by Mistral + Ollama

> Un assistant intelligent qui répond à vos questions à partir de vos documents internes.
> **100% local · 100% gratuit · 100% privé 🔒**

---

## 🧠 C'est quoi ce projet ?

La collectivité peinait à gérer l'importante masse documentaire produite quotidiennement par ses services. Les agents perdaient un temps précieux à rechercher des informations dispersées dans de multiples supports (emails, dossiers partagés, classeurs). 

Ce projet apporte une solution : un outil simple permettant d'**interroger en langage naturel** l'ensemble de la base documentaire, sans envoyer aucune donnée sur internet.

---

## 🏗️ Comment ça marche ?

```
Ta question
    ↓
Gradio (interface navigateur)
    ↓
LangChain (chef d'orchestre)
    ↓
ChromaDB (recherche dans les documents)
    ↓
Ollama → Mistral 7B (génère la réponse)
    ↓
Réponse + sources affichées
```

| Composant | Rôle | Coût |
|-----------|------|------|
| **Gradio** | Interface graphique dans le navigateur | Gratuit |
| **LangChain** | Connecte tous les composants ensemble | Gratuit |
| **ChromaDB** | Mémorise et indexe les documents | Gratuit |
| **Ollama** | Fait tourner le modèle IA en local | Gratuit |
| **Mistral 7B** | Le cerveau — modèle open source français | Gratuit |

---

## 💡 Pourquoi Mistral et pas ChatGPT ou Gemini ?

| Critère | Mistral (notre choix) | ChatGPT | Gemini |
|---------|----------------------|---------|--------|
| 🇫🇷 Entreprise française | ✅ Oui | ❌ Américain | ❌ Américain |
| 💰 Gratuit en local | ✅ Totalement | ❌ Payant à la requête | ❌ Payant à la requête |
| 📄 Licence libre (Apache 2.0) | ✅ Oui | ❌ Propriétaire | ❌ Propriétaire |
| 🔒 Cloud Act américain | ✅ Non concerné | ⚠️ Soumis | ⚠️ Soumis |
| 🇫🇷 Qualité en français | ✅ Excellent | ✅ Bon | ✅ Bon |
| 🏛️ Adopté par l'État français | ✅ Oui (10 000 agents) | ❌ Non | ❌ Non |

> **En résumé** : Mistral est le seul modèle qui combine souveraineté française, licence totalement libre, excellente maîtrise du français, et déploiement 100% local sans dépendance juridique étrangère.

---

## 🔧 C'est quoi Ollama ?

Ollama est un logiciel gratuit et open source qui permet de faire tourner des modèles IA directement sur ton ordinateur ou serveur, **sans connexion internet**.

```
Sans Ollama → tes données partent sur les serveurs d'OpenAI aux USA
Avec Ollama → tout reste sur ta machine, rien ne sort
```

**Ollama = App Store de modèles IA gratuits**

```bash
ollama pull mistral      # Mistral 7B 🇫🇷 — notre choix
ollama pull llama3       # Llama 3 (Meta)
ollama pull gemma3       # Gemma (Google)
ollama pull deepseek-r1  # DeepSeek (raisonnement)
```

La seule fois où tu as besoin d'internet :
- ✅ Installer Ollama (une fois)
- ✅ Télécharger le modèle (une fois)

Après ça → **internet coupé, tout fonctionne quand même.**

---

## ⚙️ Installation

### 1. Installer Ollama
Télécharge et installe depuis : **https://ollama.com/download**

### 2. Télécharger le modèle Mistral
```bash
ollama pull mistral
```

### 3. Créer l'environnement Python
```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # Mac/Linux
```

### 4. Installer les dépendances
```bash
pip install langchain langchain-community langchain-classic langchain-text-splitters gradio chromadb pypdf docx2txt unstructured openpyxl
```

---

## 🚀 Lancement

À chaque utilisation, suivre ces étapes dans l'ordre :

```bash
# Étape 1 — Activer l'environnement Python
.venv\Scripts\activate

# Étape 2 — Lancer l'application
python app.py

# Étape 3 — Ouvrir le navigateur
# → http://localhost:7860
```

> ⚠️ Ollama se lance automatiquement avec Windows. Si tu vois une erreur "port déjà utilisé" en lançant `ollama serve`, c'est normal — il tourne déjà en arrière-plan.

---

## 📁 Structure des dossiers

```
📁 Nouveau dossier/
├── 📄 app.py                    ← Application principale
├── 📄 README.md                 ← Ce fichier
├── 📁 .venv/                    ← Environnement Python (ne pas toucher)
├── 📁 chroma_db/                ← Base vectorielle (générée automatiquement)
└── 📁 base_donnees/             ← 👈 Tes documents ici
    ├── 📁 RH/
    ├── 📁 Finance/
    ├── 📁 Juridique/
    ├── 📁 Comptabilite/
    ├── 📁 IT/
    ├── 📁 Direction/
    ├── 📁 Marketing/
    └── 📁 Achats/
```

---

## 📄 Formats de documents supportés

| Format | Extension |
|--------|-----------|
| PDF | `.pdf` |
| Word | `.docx` |
| Excel | `.xlsx` `.xls` |
| CSV | `.csv` |

---

## 🖥️ Commandes Ollama utiles

```bash
ollama serve          # Démarrer le serveur manuellement
ollama pull mistral   # Télécharger Mistral 7B
ollama list           # Lister les modèles installés
ollama run mistral    # Tester Mistral en ligne de commande
ollama ps             # Voir les modèles en cours d'exécution
ollama rm mistral     # Supprimer le modèle
```

---

## ❓ Dépannage

| Problème | Solution |
|----------|----------|
| `ModuleNotFoundError` | Re-active le `.venv` puis `pip install ...` |
| `ERR_ADDRESS_INVALID` | Utilise `http://localhost:7860` et non `http://0.0.0.0:7860` |
| `ollama serve` — port déjà utilisé | Normal, Ollama tourne déjà en arrière-plan |
| Aucun document trouvé | Vérifie le chemin `BASE_DOSSIER` dans `app.py` |
| Réponse lente | Normal au premier appel — Mistral charge en mémoire |
| `from langchain.chains import RetrievalQA` | Remplace par `from langchain_classic.chains import RetrievalQA` |

---

## ⚖️ Cadre juridique

| Obligation | Statut |
|-----------|--------|
| **RGPD** | ✅ Conforme — aucune donnée ne sort de la mairie |
| **Cloud Act** | ✅ Non concerné — modèle 100% local |
| **ANSSI** | ✅ Solution souveraine recommandée — diagnostic MonAideCyber disponible |
| **Fiche registre CNIL** | ⚠️ À créer auprès de votre DPO |
| **AI Act européen** | ✅ Risque faible — assistant documentaire interne |

---

## 🔮 Pour aller plus loin (déploiement serveur)

Pour déployer sur un serveur interne accessible à tous les agents :

| Nb agents | Modèle conseillé | Matériel | Budget |
|-----------|-----------------|----------|--------|
| 1–5 | Mistral 7B | Mac Mini M4 24Go | ~950 € |
| 5–15 | Mistral 13B | Serveur + RTX 4090 | ~2 500 € |
| 15–30 | Llama 3 70B | Serveur + 2x RTX 3090 | ~5 000 € |

Stack recommandée en production :
```
Ollama + Open WebUI + ChromaDB + Docker Compose + Reverse proxy HTTPS
```

---

*Documentation interne — Mairie de Villeneuve-les-Prés · Usage interne uniquement*
