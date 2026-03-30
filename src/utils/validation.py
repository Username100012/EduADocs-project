from utils.language_manager import i18n

def validate_inputs(subject, topic, llm_config):
    """Validate user inputs before document generation"""
    
    if not subject or not subject.strip():
        return False, i18n("validation.subject_required", "Subject is required")
    
    if not topic or not topic.strip():
        return False, i18n("validation.topic_required", "Topic description is required")
    
    if not llm_config:
        return False, i18n("validation.ai_config_required", "AI model configuration is required")
    
    # Validate LLM configuration based on provider
    if llm_config["provider"] == "openai":
        if not llm_config.get("api_key"):
            return False, i18n("validation.openai_api_key_required", "OpenAI API key is required")
    elif llm_config["provider"] == "ollama":
        if not llm_config.get("host") or not llm_config.get("model"):
            return False, i18n("validation.ollama_host_model_required", "Ollama host and model are required")
        if not llm_config.get("connected", False):
            return False, i18n("validation.ollama_not_connected", "Ollama is not connected. Please start Ollama and refresh the page")
    elif llm_config["provider"] == "huggingface":
        if not llm_config.get("model"):
            return False, i18n("validation.huggingface_model_required", "Hugging Face model is required")
    
    return True, i18n("validation.valid", "Valid")
