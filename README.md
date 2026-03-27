# EduADocs-1.0

This project is a Streamlit application designed to assist teachers in generating various educational documents, including lesson plans, lecture notes, exercise lists, and lesson mind maps. The application allows users to select their preferred language model (LLM) from APIs, Ollama, or Hugging Face for document generation.

---

## Features

- **Multi-Language Support**: Choose between English and Portuguese (Português).
- **Lesson Plan Generation**: Build structured lesson plans with objectives, materials, and flow.
- **Lecture Notes**: Create classroom-ready notes aligned with the topic.
- **Exercise List Generation**: Create customized exercise lists based on specified subjects and requirements.
- **Lesson Mind Maps**: Generate hierarchical mind maps for lesson topics.
- **Assessment (Coming Soon)**: A dedicated module will be integrated later via an intelligent agent.
- **LLM Selection**: Choose from multiple LLMs (Google GenAI, OpenAI, Ollama, Hugging Face) to suit different document generation needs.

---

## Project Structure

```
EduADocs-1.0
├── src
│   ├── app.py
│   ├── components
│   │   ├── document_generator.py
│   │   ├── llm_selector.py
│   │   ├── language_selector.py
│   ├── generators
│   │   ├── exercise_generator.py
│   │   ├── lesson_notes_generator.py
│   │   ├── lesson_plan_generator.py
│   │   ├── mind_map_generator.py
│   │   ├── slides_generator.py
│   │   └── summary_generator.py
│   ├── llm_handlers
│   │   ├── api_handler.py
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
└── LICENSE
└── EduADocs_SUS.xlsx
```

---

## Language Support

The application supports multiple languages for a global audience:

- **English** (en) - Default language
- **Português** (pt) - Brazilian Portuguese

You can easily switch between languages using the language selector in the sidebar without refreshing the page.

### Adding New Languages

To add a new language:

1. Create a new JSON file in the `locales/` directory (e.g., `locales/es.json`)
2. Copy the structure from `locales/en.json` and translate all strings
3. Update `src/utils/language_manager.py` to include the new language in `SUPPORTED_LANGUAGES`

---

## Installation

1. Clone the repository:

   ```
   git clone https://github.com/Username100012/EduADocs-1.0.git
   cd EduADocs-1.0
   ```
2. Install the required dependencies:

   ```
   pip install -r requirements.txt
   ```
3. Set up your environment variables for API keys and other configurations as needed in `config/settings.py`.

---

## Usage

To run the application, execute the following command:

```
streamlit run src/app.py
```

Open your web browser and navigate to `http://localhost:8501` to access the application.

---

## System Usability Scale (SUS) Evaluation

SUS scores (contained in `EduADocs_SUS.xlsx`) were calculated following the standard procedure (odd items: X−1; even items: 5−X; total × 2.5).

---

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.

---

## License

This project is licensed under the MIT License. See the LICENSE file for more details.
