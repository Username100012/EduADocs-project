from generators.exercise_generator import generate_exercises
from generators.lesson_notes_generator import generate_lecture_notes
from generators.lesson_plan_generator import generate_lesson_plan
from generators.mind_map_generator import generate_mind_map
from generators.slides_generator import generate_slide_presentation
from generators.summary_generator import generate_summary

def generate_document(params):
    """Main document generation coordinator"""
    
    try:
        doc_type_key = params.get("doc_type_key")
        doc_type = params.get("doc_type")

        # Backwards-compatible detection using canonical keys
        if doc_type_key:
            doc_type_key = doc_type_key.lower()
        else:
            # Fallback: map common labels in EN/PT to canonical keys
            normalized = (doc_type or "").lower()
            if "plano" in normalized and "aula" in normalized:
                doc_type_key = "lesson_plan"
            elif "notas" in normalized and "aula" in normalized:
                doc_type_key = "lecture_notes"
            elif "exercise" in normalized or "exercício" in normalized:
                doc_type_key = "exercise"
            elif "mind map" in normalized or "mapa mental" in normalized:
                doc_type_key = "mind_map"
            elif "slide_presentation" in normalized or "apresenta" in normalized:
                doc_type_key = "slide_presentation"
            elif "summary" in normalized or "resumo" in normalized:
                doc_type_key = "summary"
            else:
                doc_type_key = "unknown"
        
        if doc_type_key == "lesson_plan":
            return generate_lesson_plan(params)
        elif doc_type_key == "lecture_notes":
            return generate_lecture_notes(params)
        elif doc_type_key == "exercise":
            return generate_exercises(params)
        elif doc_type_key == "mind_map":
            return generate_mind_map(params)
        elif doc_type_key == "slide_presentation":
            return generate_slide_presentation(params)
        elif doc_type_key == "summary":
            return generate_summary(params)
        else:
            return {"success": False, "error": "Unknown document type"}
            
    except Exception as e:
        return {"success": False, "error": str(e)}
