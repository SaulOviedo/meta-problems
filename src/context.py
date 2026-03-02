"""
Generates the context for the simulation.
"""

def generate_context():
    """
    Generates a context dictionary with industry and location.
    
    For now, this returns a static context. In the future, this can be expanded
    to generate dynamic contexts.
    """
    return {
        "industry": "Industria Ganadera",
        "location": "Venezuela"
    }
