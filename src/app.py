import streamlit as st
import sys
from pathlib import Path

# Add src directory to path for imports
src_path = Path(__file__).parent
sys.path.append(str(src_path))

from components import llm_selector, document_generator, language_selector
from application.record_download import execution_record_json
from utils.validation import validate_inputs
from utils.language_manager import get_language_manager, i18n, i18n_list

def main():
    st.set_page_config(
        page_title=i18n("page.title"),
        page_icon=i18n("page.icon"),
        layout="wide"
    )
    
    st.title(i18n("page.header"))
    st.markdown(i18n("page.description"))
    
    # Sidebar for LLM selection and Language selection
    with st.sidebar:
        st.header(i18n("sidebar.ai_model_selection_header"))
        selected_llm = llm_selector.display_llm_selector()
        
        # Display language selector at the bottom of sidebar
        language_selector.display_language_selector()
        
        
    
    # Main content area
    col1, col2 = st.columns([2, 1])

    
    with col1:
        st.header(i18n("document_settings.header"))
        subject = st.text_input(
            i18n("document_settings.subject_label"),
            placeholder=i18n("document_settings.subject_placeholder")
        )
        grade_level = st.selectbox(
            i18n("document_settings.grade_level_label"),
            i18n_list("document_settings.grade_level_options"),
            key="grade_level"
        )
        
        st.header(i18n("content_description.header"))
        doc_type = st.selectbox(
            i18n("content_description.document_type_label"),
            i18n_list("content_description.document_type_options"),
            key="doc_type"
        )
        topic = st.text_area(
            i18n("content_description.topic_label"),
            height=200,
            placeholder=i18n("content_description.topic_placeholder")
        )
        
        # Additional parameters based on document type
        doc_type_options = i18n_list("content_description.document_type_options")
        lesson_plan_type = doc_type_options[0] if len(doc_type_options) > 0 else "Lesson Plan"
        lecture_notes_type = doc_type_options[1] if len(doc_type_options) > 1 else "Lecture Notes"
        exercise_list_type = doc_type_options[2] if len(doc_type_options) > 2 else "Exercise List"
        mind_map_type = doc_type_options[3] if len(doc_type_options) > 3 else "Lesson Mind Map"
        assessment_type = doc_type_options[4] if len(doc_type_options) > 4 else "Assessment"

        # Map localized label to canonical key
        doc_type_map = {
            lesson_plan_type: "lesson_plan",
            lecture_notes_type: "lecture_notes",
            exercise_list_type: "exercise",
            mind_map_type: "mind_map",
            assessment_type: "assessment",
        }
        doc_type_key = doc_type_map.get(doc_type, "lesson_plan")
        
        if doc_type_key == "lesson_plan":  # Lesson Plan
            duration_minutes = st.number_input(
                i18n("lesson_plan.duration_label"),
                min_value=10,
                value=50,
                step=5,
                help=i18n("lesson_plan.duration_help")
            )
            learning_objectives = st.text_area(
                i18n("lesson_plan.learning_objectives_label"),
                placeholder=i18n("lesson_plan.learning_objectives_placeholder"),
                height=120
            )
            materials = st.text_area(
                i18n("lesson_plan.materials_label"),
                placeholder=i18n("lesson_plan.materials_placeholder"),
                height=100
            )
            methodology = st.selectbox(
                i18n("lesson_plan.methodology_label"),
                i18n_list("lesson_plan.methodology_options")
            )
            assessment_strategy = st.text_area(
                i18n("lesson_plan.assessment_strategy_label"),
                placeholder=i18n("lesson_plan.assessment_strategy_placeholder"),
                height=100
            )
            lesson_flow = st.text_area(
                i18n("lesson_plan.lesson_flow_label"),
                placeholder=i18n("lesson_plan.lesson_flow_placeholder"),
                height=100
            )
            include_differentiation = st.checkbox(
                i18n("lesson_plan.include_differentiation_label"),
                value=True
            )

        elif doc_type_key == "lecture_notes":  # Lecture Notes
            detail_level = st.selectbox(
                i18n("lecture_notes.detail_level_label"),
                i18n_list("lecture_notes.detail_level_options")
            )
            format_style = st.selectbox(
                i18n("lecture_notes.format_style_label"),
                i18n_list("lecture_notes.format_style_options")
            )
            include_examples = st.checkbox(
                i18n("lecture_notes.include_examples_label"),
                value=True
            )
            include_references = st.checkbox(
                i18n("lecture_notes.include_references_label"),
                value=False
            )

        elif doc_type_key == "exercise":  # Exercise List
            num_questions = st.number_input(
                i18n("exercise_list.num_questions_label"), 
                min_value=1, value=10, step=1
            )
            difficulty_options = i18n_list("exercise_list.difficulty_options")
            difficulty = st.select_slider(
                i18n("exercise_list.difficulty_label"),
                options=difficulty_options,
                value=difficulty_options[1] if len(difficulty_options) > 1 else "Medium"  # Default to Medium
            )
            question_types = st.multiselect(
                i18n("exercise_list.question_types_label"),
                i18n_list("exercise_list.question_types_options"),
                default=i18n_list("exercise_list.question_types_default")
            )
            include_answer_key = st.checkbox(
                i18n("exercise_list.include_answer_key_label"),
                value=True
            )

        elif doc_type_key == "mind_map":  # Lesson Mind Map
            main_branches = st.number_input(
                i18n("mind_map.main_branches_label"),
                min_value=3,
                value=6,
                step=1
            )
            depth_levels = st.number_input(
                i18n("mind_map.depth_label"),
                min_value=2,
                max_value=6,
                value=3,
                step=1
            )
            include_examples = st.checkbox(
                i18n("mind_map.include_examples_label"),
                value=True
            )
            highlight_hierarchy = st.checkbox(
                i18n("mind_map.highlight_hierarchy_label"),
                value=True
            )

        elif doc_type_key == "assessment":  # Assessment
            st.caption(i18n("assessment.coming_soon"))
    
    with col2:
        st.header(i18n("generation.options_header"))
        
        button_disabled = doc_type_key == "assessment"
        if button_disabled:
            st.info(i18n("assessment.coming_soon"))

        if st.button(
            i18n("generation.generate_button"),
            type="primary",
            use_container_width=True,
            disabled=button_disabled
        ):

            # Validate inputs
            is_valid, validation_message = validate_inputs(subject, topic, selected_llm)
            
            if is_valid:
                with st.spinner(i18n("generation.spinner_message")):
                    try:
                        # Prepare generation parameters
                        params = {
                            "doc_type": doc_type,
                            "doc_type_key": doc_type_key,
                            "subject": subject,
                            "grade_level": grade_level,
                            "topic": topic,
                            "language": get_language_manager().get_current_language(),
                            "llm_config": selected_llm
                        }
                        
                        # Add specific parameters based on document type
                        if doc_type_key == "lesson_plan":
                            params.update({
                                "duration_minutes": duration_minutes,
                                "learning_objectives": learning_objectives,
                                "materials": materials,
                                "methodology": methodology,
                                "assessment_strategy": assessment_strategy,
                                "lesson_flow": lesson_flow,
                                "include_differentiation": include_differentiation
                            })
                        elif doc_type_key == "lecture_notes":
                            params.update({
                                "detail_level": detail_level,
                                "format_style": format_style,
                                "include_examples": include_examples,
                                "include_references": include_references
                            })
                        elif doc_type_key == "exercise":
                            params.update({
                                "num_questions": num_questions,
                                "difficulty": difficulty,
                                "question_types": question_types,
                                "include_answer_key": include_answer_key
                            })
                        elif doc_type_key == "mind_map":
                            params.update({
                                "main_branches": main_branches,
                                "depth_levels": depth_levels,
                                "include_examples": include_examples,
                                "highlight_hierarchy": highlight_hierarchy
                            })
                        
                        # Generate document
                        result = document_generator.generate_document(params)
                        
                        record = result.get("execution_record")
                        st.session_state["last_generation"] = {
                            "success": result["success"],
                            "error": result.get("error"),
                            "content": result.get("content"),
                            "docx_file": result.get("docx_file"),
                            "word_filename": f"{subject}_{doc_type.replace(' ', '_')}.docx",
                            "execution_id": result.get("execution_id", "generation"),
                            "record_json": execution_record_json(
                                record, secrets=(selected_llm.get("api_key", ""),)
                            ) if record else None,
                            "warnings": record.processing_warnings if record else [],
                        }
                    except Exception as e:
                        st.error(i18n("generation.exception_template").format(error=str(e)))
            else:
                st.warning(validation_message)
        
        last = st.session_state.get("last_generation")
        if last:
            if last["success"]:
                st.success(i18n("generation.success_message"))
                if "probability_coin_die_example_corrected_v1" in last["warnings"]:
                    st.info(i18n("generation.probability_correction"))
                st.header(i18n("generation.document_preview_header"))
                with st.expander(i18n("generation.view_generated_content"), expanded=True):
                    st.markdown(last["content"])
                st.header(i18n("generation.download_options_header"))
                if last["docx_file"]:
                    st.download_button(
                        label=i18n("generation.download_word_label"),
                        data=last["docx_file"],
                        file_name=last["word_filename"],
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                        key="download_last_word",
                    )
            else:
                st.error(i18n("generation.error_generating_template").format(error=last['error']))
            if last["record_json"]:
                st.download_button(
                    label=i18n("generation.download_record_label"),
                    data=last["record_json"],
                    file_name=f"execution_{last['execution_id']}.json",
                    mime="application/json",
                    key="download_last_record",
                )

        # Help section
        with st.expander(i18n("help.title")):
            getting_started = i18n_list("help.getting_started_steps")
            ollama_steps = i18n_list("help.ollama_for_users")
            tips = i18n_list("help.tips_for_better_results")
            
            st.markdown(f"""
            **Getting Started:**
            1. {getting_started[0] if len(getting_started) > 0 else ""}
            2. {getting_started[1] if len(getting_started) > 1 else ""}
            3. {getting_started[2] if len(getting_started) > 2 else ""}
            4. {getting_started[3] if len(getting_started) > 3 else ""}
            
            **For Ollama users:**
            - {ollama_steps[0] if len(ollama_steps) > 0 else ""}
            - {ollama_steps[1] if len(ollama_steps) > 1 else ""}
            - {ollama_steps[2] if len(ollama_steps) > 2 else ""}
            
            **Tips for better results:**
            - {tips[0] if len(tips) > 0 else ""}
            - {tips[1] if len(tips) > 1 else ""}
            - {tips[2] if len(tips) > 2 else ""}
            - {tips[3] if len(tips) > 3 else ""}
            """)

if __name__ == "__main__":
    main()
