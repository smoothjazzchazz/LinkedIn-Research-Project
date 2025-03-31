import re
import json

def extract_experiences(text):
    experiences = []
    
    # Split experiences based on organization name followed by role
    experience_sections = re.split(r'(?=\n[A-Za-z].*?\slogo\n)', text)
    
    for section in experience_sections:
        if not section.strip():
            continue
       
        lines = section.strip().split("\n") 
        # Extract organization
        organization_match = re.search(r'^([A-Za-z\s]+) logo', section)
        organization = organization_match.group(1).strip() if organization_match else "Unknown"
        
        # Extract role
        role = lines[1].strip() if len(lines) > 1 else "Unknown"

        # Extract employment type
        employment_type = "Full-time" if "Full-time" in section else "Seasonal" if "Seasonal" in section else "Part-time" if "Part-time" in section else "Unknown"
        
        # Extract dates
        dates_match = re.search(r'(\w+ \d{4}) - (Present|\w+ \d{4})', section)
        start_date, end_date = dates_match.groups() if dates_match else ("Unknown", "Unknown")
        
        # Extract duration
        duration_match = re.search(r'· (\d+) mos', section)
        duration = f"{duration_match.group(1)} months" if duration_match else "Unknown"
        
        # Extract location
        location_match = re.search(r'([A-Za-z]+(?: [A-Za-z]+)*), ([A-Za-z]+), ([A-Za-z]+)', section)
        location = {
            "city": location_match.group(1) if location_match else "Unknown",
            "state": location_match.group(2) if location_match else "Unknown",
            "country": location_match.group(3) if location_match else "Unknown",
            "work_type": "On-site" if "On-site" in section else "Unknown"
        }
        
        # Extract description (everything between location and skills)
        description_match = re.search(r'\n(?:On-site|Hybrid|Unknown).*?\n(.*?)\nSkills:', section, re.DOTALL)
        description = description_match.group(1).strip() if description_match else "Unknown"
        
        # Extract skills
        skills_match = re.search(r'Skills: (.*)', section)
        skills = [skill.strip() for skill in skills_match.group(1).split('·')] if skills_match else []
        
        experiences.append({
            "organization": organization,
            "role": role,
            "employment_type": employment_type,
            "dates": {
                "start": start_date,
                "end": end_date,
                "duration": duration
            },
            "location": location,
            "description": description,
            "skills": skills
        })
    
    return experiences

def process_text_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        raw_text = file.read()
    
    output_data = extract_experiences(raw_text)
    
    with open("output.json", "w", encoding="utf-8") as json_file:
        json.dump(output_data, json_file, indent=4)
    
    print(json.dumps(output_data, indent=4))

if __name__ == "__main__":
    process_text_file("raw_profiles.txt")

