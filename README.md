<a id="readme-top"></a>

<!-- PROJECT SHIELDS -->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![License][license-shield]][license-url]
<!-- [![LinkedIn][linkedin-shield]][linkedin-url] -->
[![Webton][webton-shield]][webton-url]

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/imKXNNY/Webton-TopicDiscover">
    <img src="docs/assets/images/logo.png" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">Webton TopicDiscover</h3>

  <p align="center">
    Ein leistungsstarkes Tool zur Identifikation unerschlossener YouTube-Nischen und zur Generierung von "How-To"-Content.
    <br />
    <a href="docs"><strong>Dokumentation durchsuchen »</strong></a>
    <br />
    <br />
    <a href="https://github.com/imKXNNY/Webton-TopicDiscover">Demo ansehen</a>
    ·
    <a href="https://github.com/imKXNNY/Webton-TopicDiscover/issues/new?labels=bug&template=bug-report---.md">Fehler melden</a>
    ·
    <a href="https://github.com/imKXNNY/Webton-TopicDiscover/issues/new?labels=enhancement&template=feature-request---.md">Feature anfragen</a>
  </p>
</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Inhaltsverzeichnis</summary>
  <ol>
    <li>
      <a href="#über-das-projekt">Über das Projekt</a>
      <ul>
        <li><a href="#technologien">Technologien</a></li>
      </ul>
    </li>
    <li>
      <a href="#erste-schritte">Erste Schritte</a>
      <ul>
        <li><a href="#voraussetzungen">Voraussetzungen</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#nutzung">Nutzung</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#beitragen">Beitragen</a></li>
    <li><a href="#lizenz">Lizenz</a></li>
    <li><a href="#kontakt">Kontakt</a></li>
    <li><a href="#danksagungen">Danksagungen</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->
## Über das Projekt

![Product Screenshot](docs/assets/images/project-banner.webp)

**Webton TopicDiscover** ist ein Tool, das speziell entwickelt wurde, um YouTube-Nischen zu analysieren und "How-To"-Themen basierend auf Keywords und Trends zu generieren. Es nutzt Google Trends sowie Autocomplete-APIs, um Inhalte zu identifizieren, die bei Zuschauern auf Interesse stoßen.

<p align="right">(<a href="#readme-top">Zurück zum Anfang</a>)</p>

### Technologien

* [![Python][Python.org]][Python-url]
* [![Streamlit][Streamlit.io]][Streamlit-url]
* [![Google Trends API][GoogleTrends.org]][GoogleTrends-url]

<p align="right">(<a href="#readme-top">Zurück zum Anfang</a>)</p>

<!-- GETTING STARTED -->
## Erste Schritte

Folgen Sie diesen Schritten, um das Projekt lokal einzurichten und zu starten.

### Voraussetzungen

- Python 3.10 oder höher
- Poetry (Abhängigkeitsmanager)

### Installation

1. **Repository klonen**:
   ```bash
   git clone https://github.com/imKXNNY/Webton-TopicDiscover.git
   cd Webton-TopicDiscover
   ```

2. **Poetry installieren**:
   Falls noch nicht installiert:
   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   ```

3. **Abhängigkeiten installieren**:
   ```bash
   poetry install
   ```

4. **Backend starten**:
   ```bash
   poetry run python backend/app.py
   ```

5. **Frontend starten**:
   In einem separaten Terminal:
   ```bash
   poetry run streamlit run frontend/streamlit_prototype.py
   ```

6. **Browser öffnen**:
   Besuchen Sie `http://localhost:8501`, um die Anwendung zu verwenden.

<p align="right">(<a href="#readme-top">Zurück zum Anfang</a>)</p>

<!-- USAGE -->
## Nutzung

1. **"How-To"-Themen generieren**:
   - Wählen Sie ein Template und Keywords oder fügen Sie eigene Keywords hinzu.
   - Klicken Sie auf **"Generate How-To Topics"**.

2. **Trendanalysen durchführen**:
   - Navigieren Sie zum **"Analyze"**-Tab und analysieren Sie das Interesse an den Keywords über Zeit.

3. **Dokumentation nutzen**:
   - Im **"Documentation"**-Tab finden Sie Projektstrategien und Anleitungen.

<p align="right">(<a href="#readme-top">Zurück zum Anfang</a>)</p>

<!-- ROADMAP -->
## Roadmap

- [ ] Erweiterte API-Support für mehrere Plattformen
- [ ] Unterstützung für zusätzliche Sprachen
- [ ] Live-Demo-Link hinzufügen

<p align="right">(<a href="#readme-top">Zurück zum Anfang</a>)</p>

<!-- CONTRIBUTING -->
## Beitragen

Beiträge sind willkommen! Sie können Fehler melden, Vorschläge machen oder Pull Requests einreichen.

1. Repository forken
2. Einen Branch erstellen (`feature/AmazingFeature`)
3. Änderungen committen (`git commit -m 'Add AmazingFeature'`)
4. Änderungen pushen (`git push origin feature/AmazingFeature`)
5. Pull Request erstellen

<p align="right">(<a href="#readme-top">Zurück zum Anfang</a>)</p>

<!-- LICENSE -->
## Lizenz

Veröffentlicht unter der MIT License. Siehe `LICENSE` für Details.

<p align="right">(<a href="#readme-top">Zurück zum Anfang</a>)</p>

<!-- CONTACT -->
## Kontakt

**Kenny R. Güçlü**  
**Webton e.U.**  
📧 [kontakt@webton.at](mailto:kontakt@webton.at)  
🌐 [Webton e.U](https://webton.at)  
🐙 [GitHub: imKXNNY](https://github.com/imKXNNY)

<p align="right">(<a href="#readme-top">Zurück zum Anfang</a>)</p>

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[webton-shield]: https://img.shields.io/badge/Webton-cyan?style=for-the-badge&logo=webton&logoColor=white
[webton-url]: https://webton.at
[contributors-shield]: https://img.shields.io/github/contributors/imKXNNY/Webton-TopicDiscover.svg?style=for-the-badge
[contributors-url]: https://github.com/imKXNNY/Webton-TopicDiscover/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/imKXNNY/Webton-TopicDiscover.svg?style=for-the-badge
[forks-url]: https://github.com/imKXNNY/Webton-TopicDiscover/network/members
[stars-shield]: https://img.shields.io/github/stars/imKXNNY/Webton-TopicDiscover.svg?style=for-the-badge
[stars-url]: https://github.com/imKXNNY/Webton-TopicDiscover/stargazers
[issues-shield]: https://img.shields.io/github/issues/imKXNNY/Webton-TopicDiscover.svg?style=for-the-badge
[issues-url]: https://github.com/imKXNNY/Webton-TopicDiscover/issues
[license-shield]: https://img.shields.io/github/license/imKXNNY/Webton-TopicDiscover.svg?style=for-the-badge
[license-url]: https://github.com/imKXNNY/Webton-TopicDiscover/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/kenny-guclu
[product-screenshot]: docs/assets/images/project-banner.webp
[Python.org]: https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white
[Python-url]: https://www.python.org/
[Streamlit.io]: https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white
[Streamlit-url]: https://streamlit.io/
[GoogleTrends.org]: https://img.shields.io/badge/Google%20Trends-4285F4?style=for-the-badge&logo=google&logoColor=white
[GoogleTrends-url]: https://trends.google.com/