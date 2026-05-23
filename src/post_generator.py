from llm_integration import get_llm
from few_shot_prompting import FewShotPrompting

few_shot = FewShotPrompting()


def get_length_str(length):
    if length == "Short":
        return "1 to 5 lines"
    if length == "Medium":
        return "6 to 10 lines"
    if length == "Long":
        return "11 to 15 lines"


def generate_post(length, language, tag):
    llm = get_llm()
    if llm is None:
        raise ValueError("Groq API Key is not configured. Please set the GROQ_CLOUD_API_KEY environment variable or Streamlit Secrets.")
    prompt = get_prompt(length, language, tag)
    response = llm.invoke(prompt)
    return response.content


def get_prompt(length, language, tag):
    length_str = get_length_str(length)

    prompt = f"""
    Generate a LinkedIn post using the below information. No preamble.

    1) Topic: {tag}
    2) Length: {length_str}
    3) Language: {language}
    
    Guideline for Language and Script:
    - If Language is English, write the post in English language using the English script.
    - If Language is Hinglish, write the post in Hinglish (a mix of Hindi and English) using the English (Latin) script.
    - If Language is Bengali, write the post in the Bengali language using the Bengali script (বাংলা).
    """
    examples = few_shot.get_filtered_posts(length, language, tag)

    if len(examples) > 0:
        prompt += "4) Use the writing style as per the following examples."

    for i, post in enumerate(examples):
        post_text = post["text"]
        prompt += f"\n\n Example {i+1}: \n\n {post_text}"

        if i == 1:  
            break

    return prompt


if __name__ == "__main__":
    print(generate_post("Medium", "English", "Innovation"))
