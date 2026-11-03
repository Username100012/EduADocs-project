# EduADocs - Document Generator

This project is a Streamlit application designed to assist teachers in generating various educational documents, including lesson plans, lecture notes, exercise lists, and lesson mind maps. The application allows users to select their preferred language model (LLM) from APIs, Ollama, or Hugging Face for document generation.

## Features

- **Multi-Language Support**: Choose between English and Portuguese (Português) 🌐
- **Lesson Plan Generation**: Build structured lesson plans with objectives, materials, and flow.
- **Lecture Notes**: Create classroom-ready notes aligned with the topic.
- **Exercise List Generation**: Create customized exercise lists based on specified subjects and requirements.
- **Lesson Mind Maps**: Generate hierarchical mind maps for lesson topics.
- **Assessment (Coming Soon)**: A dedicated module will be integrated later via an intelligent agent.
- **LLM Selection**: Choose from multiple LLMs (Google GenAI, OpenAI, Ollama, Hugging Face) to suit different document generation needs.

## Project Structure
```
EduADocs-doc-generator
├── src
│   ├── app.py
│   ├── components
│   │   ├── document_generator.py
│   │   ├── llm_selector.py
│   │   ├── language_selector.py
│   ├── generators
│   │   ├── assessment_generator.py
│   │   ├── exercise_generator.py
│   │   ├── lesson_notes_generator.py
│   │   ├── lesson_plan_generator.py
│   │   └── mind_map_generator.py
│   ├── application
│   │   └── generation_service.py
│   ├── models
│   ├── pedagogical
│   ├── prompting
│   ├── providers
│   ├── processing
│   ├── exporters
│   ├── experiment
│   └── utils
│       ├── language_manager.py
│       └── validation.py
├── locales
│   ├── en.json
│   └── pt.json
├── requirements.txt
├── .streamlit
│   └── config.toml
├── .gitignore
└── README.md
```

## 🌐 Language Support

The application supports multiple languages for a global audience:

- **English** (en) - Default language
- **Português** (pt) - Brazilian Portuguese

You can easily switch between languages using the language selector in the sidebar without refreshing the page.

### Adding New Languages

To add a new language:

1. Create a new JSON file in the `locales/` directory (e.g., `locales/es.json`)
2. Copy the structure from `locales/en.json` and translate all strings
3. Update `src/utils/language_manager.py` to include the new language in `SUPPORTED_LANGUAGES`


## Installation

1. Clone the repository:

   ```
   git clone https://github.com/Username100012/EduADocs-project.git
   cd EduADocs-project
   ```
2. Install the required dependencies:

   ```
   pip install -r requirements.txt
   ```
3. Copy `.env.example` to `.env` at the project root and fill in only the credentials for your chosen provider. Never commit `.env`.

## Usage

To run the application, execute the following command:

```
streamlit run src/app.py
```

Open your web browser and navigate to `http://localhost:8501` to access the application.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.

## Windows (PowerShell)

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
Copy-Item .env.example .env
# Edit .env with your own provider credentials.
.\.venv\Scripts\python.exe -m streamlit run src/app.py
```

If the environment already exists, reuse it. The application exports DOCX; the assessment module is reserved for future integration.

## Application regression tests

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests
```

This application update includes source code and focused offline tests. Research datasets, experimental runs and article drafts remain separate.

## Reprodutibilidade do estudo computacional

O pacote [research/](research/README.md) preserva a configuração e a versão experimental separadas da aplicação de produção. Inclui tarefas, prompts, scripts, respostas, falhas, julgamentos, rubricas e tabelas. Pilotos e simulações são identificados separadamente.

É possível recalcular os resultados salvos sem chaves ou novas chamadas pagas. Consulte o ambiente e o comando em [research/README.md](research/README.md). Uma nova coleta com LLMs é uma operação distinta e pode produzir respostas diferentes.
