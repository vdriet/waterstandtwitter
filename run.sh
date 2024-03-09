docker stop waterstandtwitter
docker rm -f waterstandtwitter
docker run \
	--detach \
	--name waterstandtwitter \
	--env-file env.list \
	waterstandtwitter
