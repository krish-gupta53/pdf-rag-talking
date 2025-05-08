from state_schema import State

def detect_query(state: State) -> tuple[str, State]:
    """
    Determines whether the PDF has been uploaded.
    Routes to 'upload_pdf' if not uploaded yet,
    otherwise continues to 'deupload_pdf' or the next step.

    Returns:
        (str, State): Next node name, updated state
    """
    if not state["is_pdf_uploaded"]:
        return "upload_pdf", state
    else:
        return "deupload_pdf", state
