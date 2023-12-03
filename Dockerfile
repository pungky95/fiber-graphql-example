# Use nxgo/cli as the base image to do the build
FROM golang:alpine AS builder

RUN apk update && apk add --no-cache git

# Create app directory
WORKDIR $GOPATH/src/app

# Copy source files
COPY . .

# Using go get.
RUN go get -d -v

# Build apps
RUN GOOS=linux GOARCH=amd64 go build -ldflags="-w -s" -o /go/bin/fiber-graphql-example main.go

FROM alpine:latest AS final

RUN apk update && apk upgrade --no-cache

WORKDIR /go/bin

# Copy over artifacts from builder image
COPY --from=builder /go/bin/fiber-graphql-example /go/bin/fiber-graphql-example

# Expose default port
EXPOSE 8080

# Start server
CMD ["./fiber-graphql-example"]
