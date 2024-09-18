import json

from groq import Groq

from json_file_funcs import load_data_from_data_json


def create_msg_mail():
    api_data = load_data_from_data_json()

    html_content = """
    <html>
    <body>
    <h1>Job Listings</h1>
    <table border="1" cellpadding="5" cellspacing="0">
        <tr>
            <th>Job Title</th>
            <th>Company</th>
            <th>Location</th>
            <th>Job Link</th>
            <th>Job Type</th>
            <th>Description</th>
            <th>Estimated Salary</th>
            <th>Date Posted</th>
        </tr>
    """

    for job in api_data['jobs']:
        html_content += create_job_msg_mail(job)

    html_content += """
    </table>
    </body>
    </html>
    """

    return html_content

def create_job_msg_mail(job):
    web, description, salary = job['web'], job['description'], job['salary']

    job_html = f"""
    <tr>
        <td>{job['title']}</td>
        <td>{job['company']}</td>
        <td>{job['location']}</td>
        <td><a href="{web['url']}">{web['jobProvider']}</a></td>
        <td>{job['employmentType']}</td>
        <td>{description}</td>
        <td>{salary}</td>
        <td>{job['datePosted']}</td>
    </tr>
    """

    return job_html


# Set up the Groq client
API_KEY = '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'
client = Groq(api_key=API_KEY)


# Function to interact with the Groq chatbot API
def generate_groq_response(prompt):
    try:
        # print("Generating message")
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


# Create msg for telegram
def create_msg_telegram():
    api_data = load_data_from_data_json()

    msg = ''

    for job in api_data['jobs']:
        msg += create_job_msg_telegram(job)

    return msg

# Create msg for each job with description and salary hypothesis
def create_job_msg_telegram(job):
    web, description, salary = job['web'], job['description'], job['salary']

    job_msg = (f"Job Name: {job['title']}\n"
               f"Company Name: {job['company']}\n"
               f"Location: {job['location']}\n"
               f"Job Link: [{web['jobProvider']}]({web['url']})\n"
               f"Job Type: {job['employmentType']}\n"
               f"{description}\n"
               f"Estimated Salary: {salary}\n"
               f"Date Posted: {job['datePosted']}\n"
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
    for website in job['jobProviders']:
        if website['jobProvider'] == 'LinkedIn':
            return website  # Return the whole object
    return job['jobProviders'][0]  # Return the first provider if LinkedIn is not found

# Create general job msg for both mail and telegram (web, description, and salary)
def create_job_msg(job):
    web = prioritised_websites(job)

    # Call Groq API to generate a job description
    description = generate_job_description(job)

    # Hypothesize the salary range using Groq API
    salary = generate_salary_hypothesis(job)

    return [web, description, salary]


# Main function
def main():
    # Call the create_msg function to generate job messages
    # job_messages = create_msg_mail()
    # Print the generated job messages
    # print(job_messages)
    re = 1

if __name__ == "__main__":
    main()
