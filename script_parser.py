"""
Film Script PDF Parser
Extracts characters and their dialogue from PDF film scripts
"""
import re
import PyPDF2
from typing import Dict, List, Tuple
from io import BytesIO


class ScriptParser:
    def __init__(self):
        # Common patterns for script formatting
        self.character_patterns = [
            r'^([A-Z][A-Z\s\.\-\']+)$',  # All caps character names
            r'^([A-Z][A-Z\s\.\-\']+):',  # Character names with colon
            r'^\s*([A-Z][A-Z\s\.\-\']+)\s*$',  # Whitespace around character names
        ]
        
        # Patterns to ignore (stage directions, scene descriptions, etc.)
        self.ignore_patterns = [
            r'^\s*(INT\.|EXT\.)',  # Scene headers
            r'^\s*(FADE IN|FADE OUT|CUT TO)',  # Transitions
            r'^\s*\([^)]*\)$',  # Stage directions in parentheses
            r'^\s*[0-9]+\.$',  # Page numbers
            r'^\s*(CONTINUED|CONT\'D)',  # Continuations
        ]
    
    def extract_text_from_pdf(self, pdf_file) -> str:
        """Extract text from PDF file"""
        try:
            if isinstance(pdf_file, str):
                with open(pdf_file, 'rb') as file:
                    reader = PyPDF2.PdfReader(file)
                    text = ""
                    for page in reader.pages:
                        text += page.extract_text() + "\n"
            else:
                # Handle file upload object
                reader = PyPDF2.PdfReader(BytesIO(pdf_file.read()))
                text = ""
                for page in reader.pages:
                    text += page.extract_text() + "\n"
            return text
        except Exception as e:
            raise Exception(f"Error reading PDF: {str(e)}")
    
    def should_ignore_line(self, line: str) -> bool:
        """Check if line should be ignored based on patterns"""
        line = line.strip()
        if not line:
            return True
        
        for pattern in self.ignore_patterns:
            if re.match(pattern, line, re.IGNORECASE):
                return True
        return False
    
    def is_character_name(self, line: str) -> str:
        """Check if line is a character name and return cleaned name"""
        line = line.strip()
        
        # Skip empty lines or obvious non-character lines
        if not line or len(line) < 2 or len(line) > 50:
            return None
        
        for pattern in self.character_patterns:
            match = re.match(pattern, line)
            if match:
                character = match.group(1).strip()
                # Clean up character name
                character = re.sub(r'\s+', ' ', character)  # Multiple spaces to single
                character = character.replace(':', '').strip()
                
                # Filter out common false positives
                if self.is_valid_character_name(character):
                    return character
        return None
    
    def is_valid_character_name(self, name: str) -> bool:
        """Validate that this is likely a real character name"""
        # Too short or too long
        if len(name) < 2 or len(name) > 30:
            return False
        
        # Common false positives to filter out
        false_positives = [
            'THE END', 'TITLE CARD', 'MONTAGE', 'SERIES OF SHOTS',
            'LATER', 'MEANWHILE', 'SAME TIME', 'MOMENTS LATER',
            'FLASHBACK', 'DREAM SEQUENCE', 'VOICE OVER', 'V.O.',
            'O.S.', 'OFF SCREEN', 'NARRATION'
        ]
        
        if name.upper() in false_positives:
            return False
        
        # Must contain at least one letter
        if not re.search(r'[A-Za-z]', name):
            return False
        
        return True
    
    def parse_script(self, pdf_file) -> Dict[str, List[str]]:
        """
        Parse script and return dictionary of characters and their dialogue
        Returns: {character_name: [list_of_dialogue_lines]}
        """
        text = self.extract_text_from_pdf(pdf_file)
        lines = text.split('\n')
        
        script_data = {}
        current_character = None
        current_dialogue = []
        
        for line in lines:
            line = line.strip()
            
            # Skip empty lines and ignored patterns
            if self.should_ignore_line(line):
                continue
            
            # Check if this is a character name
            character = self.is_character_name(line)
            if character:
                # Save previous character's dialogue if exists
                if current_character and current_dialogue:
                    if current_character not in script_data:
                        script_data[current_character] = []
                    script_data[current_character].extend(current_dialogue)
                
                # Start new character
                current_character = character
                current_dialogue = []
            
            else:
                # This is dialogue or stage direction
                if current_character and line:
                    # Clean up dialogue line
                    cleaned_line = self.clean_dialogue_line(line)
                    if cleaned_line:
                        current_dialogue.append(cleaned_line)
        
        # Don't forget the last character
        if current_character and current_dialogue:
            if current_character not in script_data:
                script_data[current_character] = []
            script_data[current_character].extend(current_dialogue)
        
        # Filter out characters with very few lines (likely false positives)
        filtered_data = {char: lines for char, lines in script_data.items() 
                        if len(lines) >= 1 and char}
        
        return filtered_data
    
    def clean_dialogue_line(self, line: str) -> str:
        """Clean up dialogue line"""
        line = line.strip()
        
        # Remove stage directions in parentheses within dialogue
        line = re.sub(r'\([^)]*\)', '', line)
        
        # Remove extra whitespace
        line = re.sub(r'\s+', ' ', line).strip()
        
        # Skip very short lines that are likely formatting artifacts
        if len(line) < 3:
            return None
        
        return line
    
    def get_script_summary(self, script_data: Dict[str, List[str]]) -> Dict:
        """Get summary statistics of the parsed script"""
        total_lines = sum(len(lines) for lines in script_data.values())
        character_count = len(script_data)
        
        character_stats = {}
        for char, lines in script_data.items():
            character_stats[char] = {
                'line_count': len(lines),
                'total_words': sum(len(line.split()) for line in lines),
                'sample_line': lines[0] if lines else ""
            }
        
        return {
            'character_count': character_count,
            'total_dialogue_lines': total_lines,
            'characters': character_stats
        }


# Example usage and testing
if __name__ == "__main__":
    parser = ScriptParser()
    
    # Test with sample script text
    sample_script = """
    FADE IN:
    
    INT. COFFEE SHOP - DAY
    
    JOHN enters the coffee shop, looking around nervously.
    
    JOHN
    I'll have a large coffee, please.
    
    BARISTA
    Coming right up! Anything else?
    
    JOHN
    Actually, make that two. I'm expecting someone.
    
    MARY walks in and spots John.
    
    MARY
    John! Sorry I'm late.
    
    JOHN
    No problem. I got you a coffee.
    
    MARY
    You're the best. How was your meeting?
    """
    
    # For testing, we'd need to create a mock PDF
    print("ScriptParser module created successfully!")