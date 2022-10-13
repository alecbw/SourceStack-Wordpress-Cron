import os
import json
from datetime import datetime
import base64

# Non-standard-lib
import requests


def fetch_jobs():
    response = requests.post(
        "https://sourcestack-api.com/jobs",
        headers={
            "X-API-KEY": os.environ["SOURCESTACK_KEY"],
            "Content-Type": 'application/json' # this must be included for POSTs
        },
        data=json.dumps({
            "export": "caller",
            "limit": 100,
            "fields": ["post_url", "company_url", "job_name", "company_name", "job_location", "hours", "department", "seniority", "remote", "tags_matched", "tag_categories", "last_indexed", "post_html"],
            "filters": [{"field": "job_name", "operator": "CONTAINS_ANY", "value": ["SEO", "Content Market", "Digital Market"]}]
        })
    )
    return response.json()


def create_wp_auth():
    credentials = os.environ['WP_USER'] + ':' + os.environ['WP_PASS']
    token = base64.b64encode(credentials.encode())
    header = {'Authorization': 'Basic ' + token.decode('utf-8')}
    return header

# based on https://developer.wordpress.org/rest-api/reference/posts/#create-a-post
def create_wp_post(job, auth_header):

    request_body = {
        "date": datetime.now().strftime('%Y-%m-%d'), # alternately, could use last_indexed for date / date_gmt - # The date the object was published, in the site's timezone.
        "date_gmt": datetime.utcnow().strftime('%Y-%m-%d'), # The date the object was published, as GMT.
        "slug": job['job_name'].replace("  ", "-").replace(" ", "-").replace("%20", "-").replace("/", "").replace("#", "-").replace("(", "-").replace(")", "-").replace(",", "").replace("!", "").replace(".", "").replace(";", "").replace("$", "").replace("+", "").replace("&", "-").replace("'", "-").replace(":", "").replace("%", ""), # An alphanumeric identifier for the object unique to its type.
        "status": "publish", # A named status for the object.
        "password": os.environ["WP_PASS"], # A password to protect access to the content and excerpt.
        "title": job['job_name'], # The title for the object.
        "content": job['post_html'], # The content for the object.
        "author": "TODO", # The ID for the author of the object.
        "excerpt": "TODO", # The excerpt for the object.
        "featured_media": job['logo_url'], # The ID of the featured media for the object.
        "comment_status": "False", # Whether or not comments are open on the object.
        "ping_status": "False", # Whether or not the object can be pinged.
        "format": "standard", # The format for the object.
        "meta": "TODO", # Meta fields.
        "sticky": "False", # Whether or not the object should be treated as sticky.
        "template": "TODO", # The theme file to use to display the object.
        "categories": job['categories'], # The terms assigned to the object in the category taxonomy.
        "tags": ["TODO"], # The terms assigned to the object in the post_tag taxonomy.
    }
    url_endpoint = os.environ['WP_URL'].rstrip("/") + '/wp-json/wp/v2/posts'
    requests.post(url_endpoint, headers=auth_header, data=json.dumps(request_body))


def lambda_handler(event, context):
    jobs = fetch_jobs()
    auth_header = create_wp_auth()
    for job in jobs['data']:
        create_wp_post(job, auth_header)