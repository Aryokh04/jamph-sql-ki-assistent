# For å kjøre ollama nais versjonen. som heter reops-ollama, kan du bruke følgende kommandoer:

docker build -f Dockerfile.build-from-source -t reops-ollama:secure .
docker run -d -p 11434:11434 --name ollama-container reops-ollama:secure
API endpoint: http://localhost:11434

# For å stoppe og fjerne containeren, kan du bruke følgende kommandoer:
docker stop ollama-container
docker rm ollama-container
# For å fjerne bildet, kan du bruke følgende kommando:
docker rmi reops-ollama:secure
