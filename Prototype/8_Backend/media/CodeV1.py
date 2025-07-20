from flask import Flask, render_template, jsonify
app = Flask(__name__)
# Sample note data with tags and links
# Expanded note data with multiple layers and connections
notes = [
    # Top-Level Category
    {"id": "1", "title": "School", "content": "General category for school subjects.", "tags": ["category"], "depth": 0},
    
    # Subjects
    {"id": "2", "title": "Chemistry", "content": "Chemistry subject overview.", "tags": ["subject", "science"], "depth": 1},
    {"id": "3", "title": "Biology", "content": "Biology subject overview.", "tags": ["subject", "science"], "depth": 1},
    {"id": "4", "title": "Physics", "content": "Physics subject overview.", "tags": ["subject", "science"], "depth": 1},
    
    # Chemistry categories
    {"id": "5", "title": "Chemistry Classwork", "content": "In-class notes and activities for Chemistry.", "tags": ["chemistry", "classwork"], "depth": 2},
    {"id": "6", "title": "Chemistry Homework", "content": "Homework assignments for Chemistry.", "tags": ["chemistry", "homework"], "depth": 2},
    {"id": "7", "title": "Chemistry Notes", "content": "Personal notes on Chemistry topics.", "tags": ["chemistry", "notes"], "depth": 2},
    # Biology categories
    {"id": "8", "title": "Biology Classwork", "content": "In-class notes and activities for Biology.", "tags": ["biology", "classwork"], "depth": 2},
    {"id": "9", "title": "Biology Homework", "content": "Homework assignments for Biology.", "tags": ["biology", "homework"], "depth": 2},
    {"id": "10", "title": "Biology Notes", "content": "Personal notes on Biology topics.", "tags": ["biology", "notes"], "depth": 2},
    
    # Physics categories
    {"id": "11", "title": "Physics Classwork", "content": "In-class notes and activities for Physics.", "tags": ["physics", "classwork"], "depth": 2},
    {"id": "12", "title": "Physics Homework", "content": "Homework assignments for Physics.", "tags": ["physics", "homework"], "depth": 2},
    {"id": "13", "title": "Physics Notes", "content": "Personal notes on Physics topics.", "tags": ["physics", "notes"], "depth": 2},
    # Individual Notes (Depth 3)
    {"id": "14", "title": "Introduction to Atoms", "content": "Basic concepts of atomic structure.", "tags": ["chemistry", "classwork"], "depth": 3},
    {"id": "15", "title": "Periodic Table", "content": "Understanding the periodic table of elements.", "tags": ["chemistry", "classwork"], "depth": 3},
    {"id": "16", "title": "Chemical Reactions", "content": "Notes on types of chemical reactions.", "tags": ["chemistry", "classwork"], "depth": 3},
    {"id": "17", "title": "Cell Structure Homework", "content": "Homework assignment on cell structure.", "tags": ["biology", "homework"], "depth": 3},
    {"id": "18", "title": "Genetics Worksheet", "content": "Worksheet on genetics and inheritance.", "tags": ["biology", "homework"], "depth": 3},
    {"id": "19", "title": "Ecology Case Study", "content": "Homework on ecology case studies.", "tags": ["biology", "homework"], "depth": 3},
    {"id": "20", "title": "Newton's Laws", "content": "Overview of Newton's laws of motion.", "tags": ["physics", "notes"], "depth": 3},
    {"id": "21", "title": "Electromagnetism", "content": "Notes on electromagnetism concepts.", "tags": ["physics", "notes"], "depth": 3},
    {"id": "22", "title": "Quantum Mechanics Intro", "content": "Introduction to quantum mechanics.", "tags": ["physics", "notes"], "depth": 3},
]

relationships = [

    {"source": "1", "target": "2"}, {"source": "1", "target": "3"}, {"source": "1", "target": "4"},
    

    {"source": "2", "target": "5"}, {"source": "2", "target": "6"}, {"source": "2", "target": "7"},
    {"source": "3", "target": "8"}, {"source": "3", "target": "9"}, {"source": "3", "target": "10"},
    {"source": "4", "target": "11"}, {"source": "4", "target": "12"}, {"source": "4", "target": "13"},

    {"source": "5", "target": "14"}, {"source": "5", "target": "15"}, {"source": "5", "target": "16"},

    {"source": "9", "target": "17"}, {"source": "9", "target": "18"}, {"source": "9", "target": "19"},

    {"source": "13", "target": "20"}, {"source": "13", "target": "21"}, {"source": "13", "target": "22"},
]
@app.route('/')
def index():
    return render_template('index_backup.html')
@app.route('/data')
def data():
    elements = []
    # Add notes as nodes with depth information
    for note in notes:
        node = {
            'data': {
                'id': note['id'],
                'label': note['title'],
                'tags': ", ".join(note['tags']),
                'depth': note['depth']  # Include depth in data
            },
            'classes': 'note'
        }
        elements.append(node)
    # Add relationships as edges
    for relation in relationships:
        edge = {
            'data': {
                'source': relation['source'],
                'target': relation['target']
            },
            'classes': 'link'
        }
        elements.append(edge)
    return jsonify(elements=elements)
if __name__ == '__main__':
    app.run(debug=True)