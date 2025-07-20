@app.route('/search', methods=['POST'])
def search():
    query = request.json.get('query', '')
    def get_all_descendants(tag):
        """Recursively get all descendant tags of a given tag."""
        descendants = []
        for child in tag.children:
            descendants.append(child)
            descendants.extend(get_all_descendants(child))
        return descendants
    elements = []
    # Search for tags matching the query
    matched_tags = dbsession.query(Tag).filter(Tag.name.ilike(f"%{query}%")).all()
    # Process each matched tag
    for tag in matched_tags:
        # Add the tag itself
        element = {
            'id': tag.id,
            'name': tag.name,
            'children': [child.id for child in tag.children],
            'type': "tag",  # Add type property
            'data': []
        }
        elements.append(element)
        # Add all descendants of the tag
        for descendant in get_all_descendants(tag):
            descendant_element = {
                'id': descendant.id,
                'name': descendant.name,
                'children': [child.id for child in descendant.children],
                'type': "tag",
                'data': []
            }
            # Avoid duplicates
            if descendant_element not in elements:
                elements.append(descendant_element)
    # Optionally include notes that match the query or are associated with found tags
    for note in dbsession.query(Note).filter(Note.name.ilike(f"%{query}%")).all():
        element = {
            'id': note.id,
            'name': note.name,
            'tags': [tag.id for tag in note.tags],
            'type': "note",  # Add type property
            'data': []
        }
        elements.append(element)
    return jsonify(elements=elements)