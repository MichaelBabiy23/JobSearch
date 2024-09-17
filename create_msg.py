# Create msg for mail
import json

def create_msg_html():
    with open('data.json', 'r') as f:
        api_data = json.load(f)

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
        </tr>
    """

    for job in api_data['jobs']:
        html_content += create_job_html(job)

    html_content += """
    </table>
    </body>
    </html>
    """

    return html_content

def create_job_html(job):
    web = prioritised_websites(job)

    job_html = f"""
    <tr>
        <td>{job['title']}</td>
        <td>{job['company']}</td>
        <td>{job['location']}</td>
        <td>{web}</td>
        <td>{job['employmentType']}</td>
    </tr>
    """

    return job_html

def prioritised_websites(job):
    for website in job['jobProviders']:
        if website['jobProvider'] == 'LinkedIn':
            return f'<a href="{website["url"]}">LinkedIn</a>'

    # If LinkedIn is not found, use the first available job provider
    return f'<a href="{job["jobProviders"][0]["url"]}">{job["jobProviders"][0]["jobProvider"]}</a>'
