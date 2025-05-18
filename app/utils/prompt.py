import json

class PromptGenerator:
    """Class for generating prompts for medical specialty matching"""
    
    def __init__(self, specialties_file_path=None):
        """
        Initialize the PromptGenerator with the path to the specialties.json file.
        
        Args:
            specialties_file_path (str, optional): Path to the specialties.json file.
                If None, defaults to '../services/specialties.json'
        """
        self.specialties = self._get_specialty_list(specialties_file_path)
    
<<<<<<< HEAD
    def create_specialty_matching_prompt(self, patient_description):
=======
<<<<<<< HEAD
    def create_specialty_matching_prompt(self, patient_description):
=======
    def create_specialty_matching_prompt(self, symptom_description):
>>>>>>> 5b1c811 (Implement map_symptoms_to_specialties)
>>>>>>> ad550cb (Implement map_symptoms_to_specialties)
        """
        Create a prompt for the LLM to match a patient description to a specialty
        
        Args:
<<<<<<< HEAD
            patient_description (str): Description of the patient's symptoms
            
=======
<<<<<<< HEAD
            patient_description (str): Description of the patient's symptoms
            
=======
            symptom_description (str): Description of the patient's symptoms

>>>>>>> 5b1c811 (Implement map_symptoms_to_specialties)
>>>>>>> ad550cb (Implement map_symptoms_to_specialties)
        Returns:
            str: A formatted prompt for the LLM
        """
        # Construct the prompt with context and schema requirements
        return f"""
        You are a medical professional tasked with determining the most appropriate medical specialty for a patient based on their description of symptoms or conditions.

        Below are the available medical specialties with their descriptions:

        {self._format_specialties(self.specialties)}

<<<<<<< HEAD
        PATIENT DESCRIPTION:
        {patient_description}
=======
<<<<<<< HEAD
        PATIENT DESCRIPTION:
        {patient_description}
=======
        SYMPTOM DESCRIPTION:
        {symptom_description}
>>>>>>> 5b1c811 (Implement map_symptoms_to_specialties)
>>>>>>> ad550cb (Implement map_symptoms_to_specialties)

        TASK: Based on the patient's description, determine the most appropriate medical specialty from the list above. 
        Consider the symptoms, conditions, and affected body systems described by the patient.

        Your response "MUST" strictly adhere to the following JSON format:

<<<<<<< HEAD
=======
<<<<<<< HEAD
>>>>>>> ad550cb (Implement map_symptoms_to_specialties)
        Example (not to include ```json ```): {{
        "RECOMMENDED_SPECIALTY": ["specialty1", "specialty2", "specialty3"],
        "REASONING": "Explain why these specialties are recommended based on the patient's symptoms and conditions.",
        "CONFIDENCE": "One of 'High', 'Medium', or 'Low'"
        }}

        - RECOMMENDED_SPECIALTY: array of strings (up to 3 specialties from the provided list, in order of relevance)
        - REASONING: string (detailed but concise explanation of your recommendation, Pretend you are a medical advisor and provide a easy to understand explanation for this patient why these specialties are recommended in first person (maximum 30 words))
        - CONFIDENCE: string (must be one of: "High", "Medium", or "Low")
<<<<<<< HEAD
=======
=======
        Example: [
        {{
            "RECOMMENDED_SPECIALTY": "specialty1",
            "REASONING": "Explain why these specialties are recommended based on the patient's symptoms and conditions.",
            "CONFIDENCE": "One of 'High', 'Medium', or 'Low'"
        }},
        {{
            "RECOMMENDED_SPECIALTY": "specialty2",
            "REASONING": "Explain why these specialties are recommended based on the patient's symptoms and conditions.",
            "CONFIDENCE": "One of 'High', 'Medium', or 'Low'"
        }}
        ]

        - RECOMMENDED_SPECIALTY: string (up to 3 specialties from the provided list, in order of relevance)
        - REASONING: string (detailed but concise explanation of your recommendation for each specialty, Pretend you are a medical advisor and provide a easy to understand explanation for this patient why these specialties are recommended in first person (maximum 30 words))
        - CONFIDENCE: string (must be one of: "High", "Medium", or "Low")

        The output must be an array of JSON objects, each containing the keys "RECOMMENDED_SPECIALTY", "REASONING", and "CONFIDENCE".
        The length of the array should be up to 3.
>>>>>>> 5b1c811 (Implement map_symptoms_to_specialties)
>>>>>>> ad550cb (Implement map_symptoms_to_specialties)
        """

    def _format_specialties(self, specialties):
        """
        Format the specialties list for the prompt
        
        Args:
            specialties (list): List of specialty dictionaries
            
        Returns:
            str: Formatted specialties text
        """
        formatted = ""
        for specialty in specialties:
            formatted += f"- {specialty['specialtyName']}: {specialty['description']}\n"
        return formatted

    def _get_specialty_list(self, specialties_file_path):
        """
        Load and return the list of specialties
        
        Returns:
            list: List of specialty dictionaries
        """
        # Load specialties from the JSON file
        with open(specialties_file_path, 'r') as f:
            specialties = json.load(f)
        # Extract relevant information for our prompt
        specialties = [{
            "specialtyName": specialty["specialtyName"],
            "description": specialty["description"]
        } for specialty in specialties]
        return specialties