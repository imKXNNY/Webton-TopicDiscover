import streamlit as st
import requests
import pandas as pd
import os

# Backend URLs
GEN_KEYWORDS_URL = "http://127.0.0.1:5000/generate-keywords"
ANALYZE_TRENDS_URL = "http://127.0.0.1:5000/analyze-trends"

# Streamlit Config
st.set_page_config(
    page_title="Webton TopicDiscover",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon=":rocket:",
)

# Initiale Templates und Keywords basierend auf der Projektstrategie
TEMPLATE_OPTIONS = [
    "fix error code",
    "solve problem",
    "correct issue",
    "resolve error",
    "debug issue",
    "troubleshoot problem",
]

INITIAL_KEYWORDS = [
    "Roblox Error Code 268",
    "Valorant Error Code 43",
    "Minecraft Server Connection Issues",
    "React useEffect Warning",
    "Python asyncio warnings",
    "TypeScript compilation errors",
    "Windows 11 Update Issues",
    "MacOS Monterey Speed Up",
    "macOS Catalina Wi-Fi Problems",
    "Office 365 Installation Errors",
]

# Initialize session state for page navigation
if "page" not in st.session_state:
    st.session_state.page = "Generate Topics"

# Initialize session state for keywords and templates
if "additional_templates" not in st.session_state:
    st.session_state.additional_templates = []

if "additional_keywords" not in st.session_state:
    st.session_state.additional_keywords = []


# Helper Function: Load Markdown File
def load_markdown(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()
    else:
        return f"Datei nicht gefunden: {file_path}"


# Sidebar Navigation mit Full-width Buttons und Icons
st.sidebar.title("Navigation")


# Funktion zur Navigation
def navigate(page_name):
    st.session_state.page = page_name


# Buttons mit voller Breite und Icons
if st.sidebar.button("🔍 Generate Topics", use_container_width=True):
    navigate("Generate Topics")
if st.sidebar.button("📈 Analyze", use_container_width=True):
    navigate("Analyze")
if st.sidebar.button("📄 Documentation", use_container_width=True):
    navigate("Documentation")

# Aktuelle Seite aus dem Session State abrufen
page = st.session_state.page

# Generate Topics View
if page == "Generate Topics":
    st.title("Generate Topics")
    st.subheader("Discover potential 'How-To' topics.")

    # Layout für Templates und Keywords
    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown("### Select Templates")
        selected_templates = st.multiselect(
            "Choose one or more templates:",
            options=TEMPLATE_OPTIONS + st.session_state.additional_templates,
            default=["fix error code", "solve problem"],
            help="Wähle die Templates aus, die du für die Generierung der How-To-Themen verwenden möchtest.",
        )
        new_template = st.text_input("Add a new template:", "")
        if st.button("Add Template"):
            if (
                new_template
                and new_template.strip()
                not in TEMPLATE_OPTIONS + st.session_state.additional_templates
            ):
                st.session_state.additional_templates.append(new_template.strip())
                st.success(f"Template '{new_template.strip()}' hinzugefügt.")
                st.experimental_rerun()
            elif (
                new_template.strip()
                in TEMPLATE_OPTIONS + st.session_state.additional_templates
            ):
                st.warning("Dieses Template existiert bereits.")
            else:
                st.warning("Bitte gib ein gültiges Template ein.")

    with col2:
        st.markdown("### Select Keywords")
        selected_keywords = st.multiselect(
            "Choose one or more keywords:",
            options=INITIAL_KEYWORDS + st.session_state.additional_keywords,
            default=["Roblox Error Code 268", "Valorant Error Code 43"],
            help="Wähle die Keywords aus, für die du How-To-Themen generieren möchtest.",
        )
        new_keyword = st.text_input("Add a new keyword:", "")
        if st.button("Add Keyword"):
            if (
                new_keyword
                and new_keyword.strip()
                not in INITIAL_KEYWORDS + st.session_state.additional_keywords
            ):
                st.session_state.additional_keywords.append(new_keyword.strip())
                st.success(f"Keyword '{new_keyword.strip()}' hinzugefügt.")
                st.experimental_rerun()
            elif (
                new_keyword.strip()
                in INITIAL_KEYWORDS + st.session_state.additional_keywords
            ):
                st.warning("Dieses Keyword existiert bereits.")
            else:
                st.warning("Bitte gib ein gültiges Keyword ein.")

    # Button zum Generieren der How-To-Themen
    if st.button("Generate How-To Topics"):
        with st.spinner("Fetching topics..."):
            try:
                # Kombiniere Templates mit Keywords
                combined_keywords = [
                    f"{template} {keyword}"
                    for template in selected_templates
                    for keyword in selected_keywords
                ]
                # Sende die kombinierten Keywords an das Backend als kommaseparierte Zeichenkette
                response = requests.get(
                    GEN_KEYWORDS_URL, params={"base": ", ".join(combined_keywords)}
                )
                if response.status_code == 200:
                    data = response.json()
                    st.success("Topics generated successfully!")
                    howto_keywords = data.get("howto_keywords", [])
                    st.session_state["howto_keywords"] = howto_keywords
                    st.table(pd.DataFrame(howto_keywords, columns=["How-To Topics"]))
                else:
                    st.error(f"Error: {response.status_code}")
            except Exception as e:
                st.error(f"An error occurred: {e}")

    # Optional: Anzeige der kombinierten Keywords
    if "howto_keywords" in st.session_state:
        st.markdown("## Generated How-To Topics")
        st.write(", ".join(st.session_state["howto_keywords"]))

# Analyze View
elif page == "Analyze":
    st.title("Analyze Trends")
    st.subheader("Visualize interest and identify top-performing keywords.")

    if "howto_keywords" in st.session_state:
        if st.button("Analyze Trends"):
            with st.spinner("Analyzing trends..."):
                try:
                    response = requests.post(
                        ANALYZE_TRENDS_URL,
                        json={"keywords": st.session_state["howto_keywords"]},
                    )
                    if response.status_code == 200:
                        trends_data = response.json().get("trends", [])
                        if trends_data:
                            trends_df = pd.DataFrame(trends_data)
                            st.success("Trends analyzed successfully!")

                            # Datumsspalte in datetime umwandeln
                            trends_df["date"] = pd.to_datetime(trends_df["date"])

                            # Diagramm-Daten vorbereiten
                            trends_chart_data = trends_df.set_index("date")

                            # Responsive Layout: Diagramm und Tabelle nebeneinander
                            col1, col2 = st.columns(2)

                            with col1:
                                st.write("### Interesse im Zeitverlauf")
                                st.line_chart(
                                    trends_chart_data.drop(
                                        columns=["isPartial"], errors="ignore"
                                    )
                                )

                            with col2:
                                st.write("### Top Keywords nach Interesse")
                                # Nur numerische Spalten auswählen
                                trends_numeric = trends_df.drop(
                                    columns=["isPartial"], errors="ignore"
                                ).select_dtypes(include=["float64", "int64"])
                                # Mittelwerte berechnen und sortieren
                                top_keywords = (
                                    trends_numeric.mean()
                                    .sort_values(ascending=False)
                                    .head(10)
                                )
                                st.table(top_keywords)
                        else:
                            st.warning("Keine Trenddaten verfügbar.")
                    else:
                        st.error(f"Error: {response.status_code}")
                except Exception as e:
                    st.error(f"Ein Fehler ist aufgetreten: {e}")
    else:
        st.warning("Generiere zuerst Keywords im Tab 'Generate Topics'!")

# Documentation View
elif page == "Documentation":
    st.title("Dokumentation")

    docs_folder = "docs"  # Ordner mit Markdown-Dateien
    if not os.path.exists(docs_folder):
        os.makedirs(docs_folder)

    # Datei-Auswahl für Dokumentation
    markdown_files = [f for f in os.listdir(docs_folder) if f.endswith(".md")]

    if markdown_files:
        # Standard-Dokumentationsdatei auswählen (z.B. Einleitung)
        default_doc = "einleitung.md"
        if default_doc in markdown_files:
            selected_file = st.selectbox(
                "Wähle eine Dokumentationsdatei",
                markdown_files,
                index=markdown_files.index(default_doc),
            )
        else:
            selected_file = st.selectbox(
                "Wähle eine Dokumentationsdatei", markdown_files
            )

        if selected_file:
            st.markdown("""---""")
            doc_content = load_markdown(os.path.join(docs_folder, selected_file))
            st.markdown(doc_content)
    else:
        st.warning("Keine Markdown-Dateien im Dokumentationsordner gefunden.")
