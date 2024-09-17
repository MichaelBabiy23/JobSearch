import json
from groq import Groq

# Set up the Groq client
API_KEY = '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'
client = Groq(api_key=API_KEY)

# Function to interact with the Groq chatbot API
def generate_groq_response(prompt):
    try:
        print("Generating message")
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are an assistant that helps generate job descriptions and salary "
                                              "estimates in Israel, NIS per MONTH, if you don't have information "
                                              "about that, do per YEAR. Short answer please, 1 sentance. Write only "
                                              "the answer, no prolog, no quotation marks. dont mention the location. when I ask you about "
                                              "the salary write only the salary itself without mentioning the role."},
                {"role": "user", "content": prompt}
            ],
            model="llama3-8b-8192",  # Ensure this model is available in Groq's API
            temperature=0.7
        )
        return chat_completion.choices[0].message.content.strip()
    except Exception as e:
        print(f"An error occurred: {e}")
        return "No response"

# Create msg for mail
def create_msg():
    with open('data.json', 'r') as f:
        api_data = json.load(f)

    msg = ''

    for job in api_data['jobs']:
        msg += create_job_msg(job)

    return msg

# Create msg for each job with description and salary hypothesis
def create_job_msg(job):
    web = prioritised_websites(job)

    # Call Groq API to generate a job description
    description = generate_job_description(job)

    # Hypothesize the salary range using Groq API
    salary = generate_salary_hypothesis(job)

    job_msg = (f"Job name : {job['title']}\n"
               f"Company name : {job['company']}\n"
               f"Location : {job['location']}\n"
               f"Job link : {web}\n"
               f"Job type : {job['employmentType']}\n"
               f"Description : {description}\n"
               f"Estimated Salary : {salary}\n"
               "---------------------------------------------------------------------------------------------\n"
               )

    return job_msg

# Generate a job description using Groq API
def generate_job_description(job):
    prompt = f"Create a short, professional description for the following job: {job['title']} at {job['company']} in {job['location']}."
    return generate_groq_response(prompt)

# Generate a salary hypothesis using Groq API
def generate_salary_hypothesis(job):
    prompt = f"Estimate the salary range for the following job: {job['title']} at {job['company']} in {job['location']}. The job type is {job['employmentType']}."
    return generate_groq_response(prompt)

# Prioritize LinkedIn for job link
def prioritised_websites(job):
    web = ''

    for website in job['jobProviders']:
        if website['jobProvider'] == 'LinkedIn':
            web = 'LinkedIn'
            break

    if web:
        return web
    else:
        return job['jobProviders'][0]['jobProvider']

# Main function
def main():
    # Call the create_msg function to generate job messages
    job_messages = create_msg()

    # Print the generated job messages
    print(job_messages)

if __name__ == "__main__":
    main()
