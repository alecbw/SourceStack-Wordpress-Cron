# SourceStack-Wordpress-Cron
Example ETL flow for pulling data from SourceStack.co and writing to a Wordpress site


Requires the following environment variables to be set:

- AWS_ACCOUNT_ID
- SOURCESTACK_KEY
- WP_URL
- WP_USER
- WP_PASS

When setting up, make sure to customize the following to your stack/need:
- AWS Area Zone (AZ)
- SourceStack API call filters
- Post `author`, `excerpt`, `meta` fields, `template`, `tags`, 

To deploy:
```
sls deploy --config serverless.yml
```

To test locally (emulating the cloud env):
```
sls invoke -f sourcestack-cron --config serverless.yml
```

To delete all related AWS resources:
```
sls remove --config serverless.yml
```
