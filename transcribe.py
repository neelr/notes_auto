from pathlib import Path
import sys
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

client = OpenAI()

# Ensure an API key is set for OpenAI


def read_file(file_path):
    """Reads the content of a file and returns it."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        sys.exit(1)


def send_to_chatgpt(content):
    """Sends content to ChatGPT and returns the LaTeX conversion."""
    try:
        # Start the conversation with note-taking
        note_taking_response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert professor that takes his lecture transcript and gives professor-like lecture notes. Nobel prize genius brilliant. Expressive long and detailed notes."},
                {"role": "user", "content": f"""{
                    content}

                    This is a lecture transcript.
                    generate a basic outline of what the lecture was about. make it bulleted and include everything in the transcript, its okay to be verbose/long."""}
            ]
        )

        # Extract the note-taking response text
        notes_content = note_taking_response.choices[0].message.content.strip()
        print("Generated outline...")

        non_latex = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {
                    "role": "user",
                    "content": f"""
                    {notes_content}
                    {content}

                    write out a good students full lecture notes 2nd person (about 3-4 pages) while not leaving out details (feel free to include steps, ie. fill in steps/explain algorithms like A* or Existentialism or Gaussian methods if mentioned + details from your own knowledge) and include minute tips that might help people studying. Feel free to include paragraphs and annotate (bold/italics) accordingly. Label it accordingly + main topic. Feel free to loosely follow the structure above and add things as you go. \n\n.\n\n"""}
            ]
        )

        non_latex_content = non_latex.choices[0].message.content.strip()

        print("Generated lecture notes...")

        # Continue the conversation with LaTeX conversion, without including the original lecture transcript
        latex_conversion_response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {
                    "role": "user",
                    "content": f"""now convert it to a full latex document with a table of contents. only output the latex, no code block or extra text and it should compile standalone (use hyperref though).\n\n{
                        non_latex_content}"""}
            ]
        )

        print("Converted to LaTeX...")

        # Extract the LaTeX conversion response text
        latex = latex_conversion_response.choices[0].message.content.strip()

        return latex
    except Exception as e:
        print(f"Error communicating with OpenAI: {e}")
        sys.exit(1)


def save_to_file(content, file_path):
    """Saves content to a file."""
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)
    except Exception as e:
        print(f"Error writing to {file_path}: {e}")
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py arg1.txt")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = Path(input_file).stem + ".tex"

    file_content = read_file(input_file)
    latex_content = send_to_chatgpt(file_content)
    save_to_file(latex_content, output_file)

    print(f"Output saved to {output_file}")
