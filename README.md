# SourceStack-Wordpress-Cron
Example ETL flow for pulling data from SourceStack.co and writing to a Wordpress site


Requires the following environment variables to be set:

- AWS_ACCOUNT_ID
- SOURCESTACK_KEY
- WP_URL
- WP_PASS

When setting up, make sure to customize the following to your stack:
- AWS Area Zone (AZ)
- SourceStack API call filters
- Post `author`, `excerpt`, `meta` fields, `template`, `tags`, 
