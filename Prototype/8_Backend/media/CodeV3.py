def populate_sample_data():
    # Check if the data already exists
    if dbsession.query(Tag).count() == 0:
        
        
        EPQ_tag = Tag(name="EPQ")
        dbsession.add(EPQ_tag)
        
        planning_tag = Tag(name="Planning A01", parents=[EPQ_tag])
        dbsession.add(planning_tag)
        
        research_tag = Tag(name="Research A02", parents=[EPQ_tag])
        dbsession.add(research_tag)
        ui_tag = Tag(name="UI", parents=[research_tag])
        technical_tag = Tag(name="Technical", parents=[research_tag])
        ai_tag = Tag(name="AI", parents=[research_tag])
        visualisation_tag = Tag(name="Visualisation", parents=[research_tag])
        dbsession.add(ui_tag)
        dbsession.add(technical_tag)
        dbsession.add(ai_tag)
        dbsession.add(visualisation_tag)
        
        evaluation_tag = Tag(name="Evaluation A04", parents=[EPQ_tag])
        dbsession.add(evaluation_tag)
        
        skilldevelopment_tag = Tag(name="Skill Development A03", parents=[EPQ_tag, evaluation_tag])
        dbsession.add(skilldevelopment_tag)
        
        
        
        project_tag = Tag(name="Project Choice", parents=[EPQ_tag])
        dbsession.add(project_tag)
        
        homework_tag = Tag(name="Homework", parents=[EPQ_tag])
        dbsession.add(homework_tag)
        
        diary_tag = Tag(name="Diary", parents=[EPQ_tag, homework_tag])
        dbsession.add(diary_tag)
        
        airefereencing_tag = Tag(name="AI Referencing", parents=[EPQ_tag])
        dbsession.add(airefereencing_tag)
        
        completed_tag = Tag(name="Completed", parents=[EPQ_tag, skilldevelopment_tag, evaluation_tag, project_tag])
        dbsession.add(completed_tag)
        
        research1_note = Note(name="Note 1", tags=[diary_tag, homework_tag, technical_tag])
        research2_note = Note(name="Note 2", tags=[diary_tag, homework_tag, ai_tag])
        airefrence1_note = Note(name="Note 3", tags=[airefereencing_tag])
        airefrence2_note = Note(name="Note 4", tags=[airefereencing_tag, completed_tag])
        dbsession.add(research1_note)
        dbsession.add(research2_note)
        dbsession.add(airefrence1_note)
        dbsession.add(airefrence2_note)
        # Commit the changes to the database
        dbsession.commit()
# Populate sample data if not already present
populate_sample_data()
