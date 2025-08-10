def classify_prompt_type(state):
    has_file = bool(state.file_path)
    has_prompt = bool(state.prompt)

    if has_file and not has_prompt:
        return {"next": "only_file"}
    elif has_file and has_prompt:
        return {"next": "prompt_and_file"}
    elif not has_file and has_prompt:
        return {"next": "only_prompt"}
    else:
        raise ValueError("No file or prompt provided.")

# def classify_prompt_type(state):
#     has_file = bool(state.file_url)
#     has_prompt = bool(state.prompt)

#     if has_file and not has_prompt:
#         return "only_file"
#     elif has_file and has_prompt:
#         return "prompt_and_file"
#     elif not has_file and has_prompt:
#         return "only_prompt"
#     else:
#         return "none" 