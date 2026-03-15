from engine.config import get_llm


def generate_final_image(final_prompt: str):
    llm = get_llm()
    image = llm.generate_image(final_prompt)
    return image