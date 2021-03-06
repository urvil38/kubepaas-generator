# PLEASE DO NOT EDIT 
# AUTOGENERATED WITH KUBEPAAS-GENERATOR

FROM {{ config.docker_image }}
WORKDIR /src
COPY go.mod ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -ldflags="-w -s" -o /src/app
CMD ["/src/app"]