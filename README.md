# Quickseal

Quickseal is a simple web application to quickly share files publicly or
privately. It's divided into two services: the frontend, `public`, and the API,
`api`. Both services are written in Python using Flask.

## Deployment

To deploy Quickseal, all you have to do is `git clone` the repository, and run
the Docker Compose configuration provided:

```sh
docker compose up -d
```

This will spin up the Quickseal services and an instance of NGINX mapped to the
hosts `:80` (HTTP) port.

Keep in mind that the provided NGINX configuration proxies all traffic on the
`/api/v1/` route to the API service, and everything else to the frontend
service.
