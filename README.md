# REST APIs Recording Project

### ENV VARIABLE NEEDED
> DATABASE_URL (Postgres)
> API_KEY (MAILGUN API KEY)
> MAILGUN_DOMAIN
> REDIS_URL

### HOW TO RUN:
On 1st Terminal

> docker build -t {{image_name}} .
> docker run -p 5000:80 {{image_name}}

On 2nd Terminal
> docker run -w /app {{image_name}} sh -c "rq worker -u {{redis_url}} emails"