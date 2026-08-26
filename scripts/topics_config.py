"""
Rotating list of (board, class, subject, chapter) topics.
Each daily run picks the next topic in sequence (stored in
output/topic_index.txt) so the channel cycles through the full
syllabus over time instead of repeating.
"""

TOPICS = [
    ("CBSE", "12", "Physics", "Electrostatics"),
    ("CBSE", "12", "Physics", "Current Electricity"),
    ("CBSE", "12", "Physics", "Magnetic Effects of Current"),
    ("CBSE", "12", "Physics", "Electromagnetic Induction"),
    ("CBSE", "12", "Physics", "Optics - Ray Optics"),
    ("CBSE", "12", "Physics", "Dual Nature of Matter"),
    ("CBSE", "12", "Physics", "Atoms and Nuclei"),
    ("CBSE", "12", "Chemistry", "Solutions"),
    ("CBSE", "12", "Chemistry", "Electrochemistry"),
    ("CBSE", "12", "Chemistry", "Chemical Kinetics"),
    ("CBSE", "12", "Chemistry", "d and f Block Elements"),
    ("CBSE", "12", "Chemistry", "Coordination Compounds"),
    ("CBSE", "12", "Chemistry", "Aldehydes Ketones and Carboxylic Acids"),
    ("CBSE", "12", "Maths", "Relations and Functions"),
    ("CBSE", "12", "Maths", "Matrices and Determinants"),
    ("CBSE", "12", "Maths", "Continuity and Differentiability"),
    ("CBSE", "12", "Maths", "Application of Derivatives"),
    ("CBSE", "12", "Maths", "Integrals"),
    ("CBSE", "12", "Maths", "Differential Equations"),
    ("CBSE", "12", "Maths", "Vectors and 3D Geometry"),
    ("CBSE", "12", "Maths", "Probability"),
    ("CBSE", "10", "Science", "Chemical Reactions and Equations"),
    ("CBSE", "10", "Science", "Acids Bases and Salts"),
    ("CBSE", "10", "Science", "Metals and Non-metals"),
    ("CBSE", "10", "Science", "Light - Reflection and Refraction"),
    ("CBSE", "10", "Science", "Electricity"),
    ("CBSE", "10", "Science", "Magnetic Effects of Electric Current"),
    ("CBSE", "10", "Maths", "Real Numbers"),
    ("CBSE", "10", "Maths", "Polynomials"),
    ("CBSE", "10", "Maths", "Pair of Linear Equations"),
    ("CBSE", "10", "Maths", "Quadratic Equations"),
    ("CBSE", "10", "Maths", "Arithmetic Progressions"),
    ("CBSE", "10", "Maths", "Triangles"),
    ("CBSE", "10", "Maths", "Trigonometry"),
    ("CBSE", "10", "Maths", "Circles"),
    ("CBSE", "10", "Maths", "Surface Areas and Volumes"),
    ("CBSE", "10", "Maths", "Statistics and Probability"),
]


def get_todays_topic():
    """Reads/increments a rotating index so each run advances to the next topic."""
    import os
    index_path = os.path.join(os.path.dirname(__file__), "..", "output", "topic_index.txt")
    idx = 0
    if os.path.exists(index_path):
        with open(index_path) as f:
            idx = int(f.read().strip() or 0)
    topic = TOPICS[idx % len(TOPICS)]
    with open(index_path, "w") as f:
        f.write(str((idx + 1) % len(TOPICS)))
    return topic
