from flask import Flask, render_template, request, redirect
import pandas as pd
import os
app = Flask(__name__)

# Load dataset (Ensure dataset.csv contains 'Name', 'Phone', 'Resume_Skills', 'LinkedIn_Skills', 'Internship', 'Internship_Duration')
df = pd.read_csv('dataset.csv')

# Function to extract relevant skills from user input
def extract_skills(user_input):
    skills = ["TensorFlow", "Python", "Machine Learning", "Deep Learning", "NLP", "Cloud", "Data Science","React","Web Development","Java","HTML","JavaScript","Django","Flask","Node.js","Express.js","MongoDB","PostgreSQL","MySQL","AWS","Azure","GCP","Docker","Kubernetes","CI/CD","Git","Jenkins","Ansible","Terraform","Linux","Windows","MacOS","Android","iOS","Flutter","React Native","Swift","Kotlin","Objective-C","UI/UX","Adobe XD","Figma","Sketch","Photoshop","Illustrator","InDesign","After Effects","Premiere Pro","Final Cut Pro","Blender","Unity","Unreal Engine","Maya","3ds Max","AutoCAD","SolidWorks","Fusion 360","Revit","SketchUp","Rhino","Grasshopper","Arduino","Raspberry Pi","IoT","Blockchain","Cryptocurrency","Bitcoin","Ethereum","Smart Contracts","DeFi","NFT","Cybersecurity","Ethical Hacking","Penetration Testing","Incident Response","Security Operations","Security Architecture","Security Engineering","Security Analysis","Security Auditing","Security Compliance","Security Governance","Security Risk Management","Security Consulting","Security Awareness","Security Training","Security Policies","Security Procedures","Security Standards","Security Frameworks","Security Protocols","Security Certifications","Security Tools","Security Software","Security Hardware","Security Services","Security Solutions","Security Products","Security Systems","Security Networks","Security Applications","Security Platforms","Security Cloud","Security Data","Security AI","Security ML","Security IoT","Security Blockchain","Security Cryptocurrency","Security Bitcoin","Security Ethereum","Security Smart Contracts","Security DeFi","Security NFT","Security Cybersecurity","Security Ethical Hacking","Security Penetration Testing","Security Incident Response","Security Security Operations","Security Security Architecture","Security Security Engineering","Security Security Analysis","Security Security Auditing","Security Security Compliance","Security Security Governance","Security Security Risk Management","Security Security Consulting","Security Security Awareness","Security Security Training","Security Security Policies","Security Security Procedures","Security Security Standards","Security Security Frameworks","Security Security Protocols","Security Security Certifications","Security Security Tools","Security Security Software","Security Security Hardware","Security Security Services","Security Security Solutions","Security Security Products","Security Security Systems","Security Security Networks","Security Security Applications","Security Security Platforms","Security Security Cloud","Security Security Data","Security Security AI","Security Security ML","Security Security IoT","Security Security Blockchain","Security Security Cryptocurrency","Security Security Bitcoin","Security"]
    extracted = [skill for skill in skills if skill.lower() in user_input.lower()]
    return extracted

# Function to find top 10 persons who can help
def find_helpers(extracted_skills):
    if not extracted_skills:
        return []

    # Ensure required columns exist
    if 'Resume_Skills' not in df.columns or 'LinkedIn_Skills' not in df.columns:
        return []

    # Convert to lowercase for case-insensitive matching
    df['Match_Score'] = df.apply(
        lambda x: sum(skill.lower() in (str(x['Resume_Skills']).lower() + " " + str(x['LinkedIn_Skills']).lower()) 
                      for skill in extracted_skills), axis=1
    )

    # Sort by match score and internship duration (descending)
    top_helpers = df[df['Match_Score'] > 0].sort_values(by=['Match_Score', 'Internship_Duration'], ascending=[False, False])

    # Get top 10 helpers
    return top_helpers[['Name', 'Phone', 'Internship', 'Internship_Duration']].head(10).to_dict(orient='records')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result', methods=['POST'])
def result():
    if request.method == 'POST':
        description = request.form.get('description', '')

        # Extract skills
        extracted_skills = extract_skills(description)

        # Find top helpers
        helpers = find_helpers(extracted_skills)

        return render_template('result.html', skills=extracted_skills, helpers=helpers)
    
    return redirect('/')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
