"""
Create a sample PDF script for testing the script reader
"""
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

def create_sample_script():
    """Create a sample film script PDF"""
    filename = "sample_script.pdf"
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter
    
    # Title
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, "THE COFFEE SHOP")
    c.drawString(50, height - 70, "A Short Film Script")
    
    # Script content
    c.setFont("Helvetica", 12)
    y = height - 120
    
    script_lines = [
        "",
        "FADE IN:",
        "",
        "INT. COFFEE SHOP - DAY",
        "",
        "A cozy coffee shop with warm lighting. JOHN (20s) sits at a",
        "corner table, nervously checking his phone.",
        "",
        "JOHN",
        "I hope she shows up.",
        "",
        "SARAH (20s) enters, looking around. She spots John and smiles.",
        "",
        "SARAH",
        "John! Sorry I'm late. Traffic was terrible.",
        "",
        "JOHN", 
        "No worries at all. I just got here myself.",
        "",
        "Sarah sits down across from John.",
        "",
        "SARAH",
        "This place is lovely. How did you find it?",
        "",
        "JOHN",
        "My sister recommended it. She says they have",
        "the best coffee in town.",
        "",
        "BARISTA (O.S.)",
        "What can I get you folks today?",
        "",
        "SARAH",
        "I'll have a cappuccino, please.",
        "",
        "JOHN",
        "Make that two cappuccinos.",
        "",
        "BARISTA (O.S.)",
        "Coming right up!",
        "",
        "John and Sarah smile at each other.",
        "",
        "SARAH",
        "So tell me about your new job.",
        "",
        "JOHN",
        "It's been amazing so far. The team is great",
        "and the projects are really challenging.",
        "",
        "SARAH",
        "That's wonderful! I'm so happy for you.",
        "",
        "FADE OUT.",
        "",
        "THE END"
    ]
    
    line_height = 15
    for line in script_lines:
        if y < 50:  # Start new page if needed
            c.showPage()
            c.setFont("Helvetica", 12)
            y = height - 50
        
        c.drawString(50, y, line)
        y -= line_height
    
    c.save()
    print(f"Sample script created: {filename}")

if __name__ == "__main__":
    create_sample_script()