from mcp.server.fastmcp import FastMCP
import os

# Create an MCP server
mcp = FastMCP("AI Sticky Notes")

NOTES_FILE = os.path.join(os.path.dirname(__file__), "notes.txt")

def ensure_file():
    if not os.path.exists(NOTES_FILE):
        with open(NOTES_FILE, "w") as f:
            f.write("")
        
@mcp.tool()
def add_note(message: str) -> str:
    """
    Append a new note to the sticky note file. 

    Args: 
        message (str): The note content to be added.

    Returns:
        str: Confirmation message indicating the note was saved.      
    """
    ensure_file()
    with open(NOTES_FILE, "a") as f:
        f.write(message + "\n")
    return "Note saved!"


@mcp.tool()
def read_notes() -> str:
    """
    Read all notes from the sticky note file.

    Returns:
        str: The content of all notes, or a message if no notes are found.
    """
    
    ensure_file()
    with open(NOTES_FILE, "r") as f:
        notes = f.read().strip()
    return notes if notes else "No notes found."


@mcp.resource("notes://latest")
def latest_note() -> str:
    """
    Retrieve the most recent note from the sticky note file.

    Returns:
        str: The content of the latest note, or a message if no notes are found.
    """
    ensure_file()
    with open(NOTES_FILE, "r") as f:
        lines = f.readlines()
    return lines[-1].strip() if lines else "No notes found."


@mcp.prompt()
def note_summary_prompt() -> str:
    """
    Generate a prompt to summarize the notes.

    Returns:
        str: A prompt asking for a summary of the notes.
    """
    ensure_file()

    with open(NOTES_FILE, "r") as f:
        notes = f.read().strip()
    
    if not notes:
        return "No notes to summarize."
    
    return f"Please summarize the following notes: {notes}"