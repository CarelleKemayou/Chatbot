import os
import gradio as gr
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, CSVLoader
from langchain_community.document_loaders import UnstructuredExcelLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.llms import Ollama
from langchain_classic.chains import RetrievalQA
import shutil

# ============================================================
# CONFIGURATION — modifie ce chemin vers ton dossier base_donnees
# ============================================================
BASE_DOSSIER = r"C:\Users\Carelle.Kemayou\Desktop\base_donnees"
CHROMA_DIR = "./chroma_db"

# ============================================================
# CHARGEMENT DES DOCUMENTS
# ============================================================
def charger_documents(dossier):
    documents = []
    extensions_supportees = {
        ".pdf": PyPDFLoader,
        ".docx": Docx2txtLoader,
        ".csv": CSVLoader,
    }

    for racine, sous_dossiers, fichiers in os.walk(dossier):
        for fichier in fichiers:
            chemin = os.path.join(racine, fichier)
            ext = os.path.splitext(fichier)[1].lower()

            if ext in extensions_supportees:
                try:
                    loader = extensions_supportees[ext](chemin)
                    docs = loader.load()
                    # Ajouter le département et type comme métadonnée
                    parties = chemin.replace(dossier, "").split(os.sep)
                    departement = parties[1] if len(parties) > 1 else "General"
                    for doc in docs:
                        doc.metadata["departement"] = departement
                        doc.metadata["fichier"] = fichier
                    documents.extend(docs)
                    print(f"✅ Chargé : {chemin}")
                except Exception as e:
                    print(f"❌ Erreur sur {chemin} : {e}")
            elif ext in [".xlsx", ".xls"]:
                try:
                    loader = UnstructuredExcelLoader(chemin)
                    docs = loader.load()
                    parties = chemin.replace(dossier, "").split(os.sep)
                    departement = parties[1] if len(parties) > 1 else "General"
                    for doc in docs:
                        doc.metadata["departement"] = departement
                        doc.metadata["fichier"] = fichier
                    documents.extend(docs)
                    print(f"✅ Chargé : {chemin}")
                except Exception as e:
                    print(f"❌ Erreur sur {chemin} : {e}")

    return documents

# ============================================================
# INDEXATION DANS CHROMADB
# ============================================================
def indexer_documents():
    print("📂 Chargement des documents...")
    documents = charger_documents(BASE_DOSSIER)

    if not documents:
        return "❌ Aucun document trouvé dans le dossier. Vérifie le chemin."

    print(f"📄 {len(documents)} documents chargés. Découpage en morceaux...")
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    morceaux = splitter.split_documents(documents)

    print("🔢 Création des embeddings avec Ollama...")
    embeddings = OllamaEmbeddings(model="mistral")#le model utilisé pour les embeddings

    if os.path.exists(CHROMA_DIR):
        shutil.rmtree(CHROMA_DIR)

    vectorstore = Chroma.from_documents(
        documents=morceaux,
        embedding=embeddings,
        persist_directory=CHROMA_DIR
    )
    vectorstore.persist()
    print("✅ Indexation terminée !")
    return f"✅ {len(morceaux)} morceaux indexés depuis {len(documents)} documents !"

# ============================================================
# QUESTION / RÉPONSE
# ============================================================
def poser_question(question, departement_filtre):
    if not os.path.exists(CHROMA_DIR):
        return "❌ Base de données non indexée. Clique d'abord sur 'Indexer les documents'."

    embeddings = OllamaEmbeddings(model="mistral")
    vectorstore = Chroma(
        persist_directory=CHROMA_DIR,
        embedding_function=embeddings
    )

    # Filtre par département si sélectionné
    if departement_filtre and departement_filtre != "Tous":
        retriever = vectorstore.as_retriever(
            search_kwargs={
                "filter": {"departement": departement_filtre},
                "k": 5
            }
        )
    else:
        retriever = vectorstore.as_retriever(search_kwargs={"k": 5})

    llm = Ollama(model="mistral")
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True
    )

    resultat = qa_chain({"query": question})
    reponse = resultat["result"]
    sources = resultat["source_documents"]

    # Afficher les sources
    sources_text = "\n\n---\n📎 **Sources utilisées :**\n"
    for src in sources:
        dept = src.metadata.get("departement", "?")
        fichier = src.metadata.get("fichier", "?")
        sources_text += f"- [{dept}] {fichier}\n"

    return reponse + sources_text

# ============================================================
# LISTE DES DÉPARTEMENTS DISPONIBLES
# ============================================================
def get_departements():
    departements = ["Tous"]
    if os.path.exists(BASE_DOSSIER):
        for d in os.listdir(BASE_DOSSIER):
            if os.path.isdir(os.path.join(BASE_DOSSIER, d)):
                departements.append(d)
    return departements

# ============================================================
# INTERFACE GRADIO
# ============================================================
with gr.Blocks(
    title="📚 Assistant IA — Base documentaire",
    theme=gr.themes.Soft(primary_hue="blue")
) as app:

    gr.Markdown("""
    # 📚 Assistant IA — Base documentaire interne
    > Pose des questions sur tes documents internes. Tout tourne **100% en local** sur ton PC. 🔒
    """)

    with gr.Tab("💬 Poser une question"):
        with gr.Row():
            departement = gr.Dropdown(
                choices=get_departements(),
                value="Tous",
                label="📁 Filtrer par département",
                interactive=True
            )

        question = gr.Textbox(
            label="Ta question",
            placeholder="Ex: Quels sont les marchés publics en cours ? Quel est le budget RH 2025 ?",
            lines=3
        )

        btn_question = gr.Button("🔍 Poser la question", variant="primary")
        reponse = gr.Markdown(label="Réponse de Mistral")

        btn_question.click(
            fn=poser_question,
            inputs=[question, departement],
            outputs=reponse
        )

    with gr.Tab("⚙️ Indexer les documents"):
        gr.Markdown("""
        ### Comment ça marche ?
        1. Place tes documents dans `base_donnees/` (organisés par département)
        2. Clique sur **Indexer** pour que Mistral apprenne leur contenu
        3. Va dans l'onglet **Poser une question** et interroge ta base !

        > ⚠️ Re-indexe à chaque fois que tu ajoutes de nouveaux documents.
        """)

        btn_indexer = gr.Button("📥 Indexer les documents", variant="primary", size="lg")
        statut = gr.Textbox(label="Statut", interactive=False)

        btn_indexer.click(
            fn=indexer_documents,
            inputs=[],
            outputs=statut
        )

    with gr.Tab("ℹ️ Infos"):
        gr.Markdown(f"""
        ### Configuration actuelle
        - 📁 **Dossier surveillé** : `{BASE_DOSSIER}`
        - 🤖 **Modèle** : Mistral 7B (via Ollama)
        - 🔒 **Connexion internet** : Non — tout est local
        - 💾 **Base vectorielle** : ChromaDB (stockée dans `./chroma_db`)

        ### Formats supportés
        - 📄 PDF
        - 📝 Word (.docx)
        - 📊 Excel (.xlsx, .xls)
        - 📋 CSV
        """)

app.launch(share=False, server_name="0.0.0.0", server_port=7860)