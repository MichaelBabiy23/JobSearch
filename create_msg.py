# Create msg for mail
import json


def create_msg():

    with open('data.json', 'r') as f:
        api_data = json.load(f)

    msg = ''

    for job in api_data['jobs']:
        msg += create_job_msg(job)

    return msg


# Create msg for each job
def create_job_msg(job):

    web = prioritised_websites(job)

    job_msg = ('Job name : ' + job['title'] + '\n'
                + 'Company name : ' + job['company'] + '\n'
                + 'Location : ' + job['location'] + '\n'
                + 'Job link : ' + web + '\n'
                + 'Job type : ' + job['employmentType'] + '\n'
                + '---------------------------------------------------------------------------------------------' + '\n'
                )

    return job_msg


# Priorities LinkedIn
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


#job name:
#comp name:
#location:
#job link:
#job type: