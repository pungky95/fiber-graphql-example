package main

import (
	"fmt"
	"log"

	"github.com/gofiber/fiber/v2"
	"github.com/graphql-go/graphql"
)

type Input struct {
	Query         string                 `query:"query"`
	OperationName string                 `query:"operationName"`
	Variables     map[string]interface{} `query:"variables"`
}

func main() {
	// Create GraphQL fields
	fields := graphql.Fields{
		"hello": &graphql.Field{
			Type: graphql.String,
			Resolve: func(p graphql.ResolveParams) (interface{}, error) {
				return "tokyo", nil
			},
		},
	}

	// Create RootQuery object config
	rootQuery := graphql.ObjectConfig{Name: "RootQuery", Fields: fields}

	// Create schema config with RootQuery
	schemaConfig := graphql.SchemaConfig{Query: graphql.NewObject(rootQuery)}

	// Create schema
	schema, err := graphql.NewSchema(schemaConfig)
	if err != nil {
		log.Fatalf("failed to create new schema, error: %v", err)
	}

	// Create Fiber app
	app := fiber.New()

	// Handler function for GraphQL requests
	graphqlHandler := func(ctx *fiber.Ctx) error {
		var input Input
		if err := ctx.BodyParser(&input); err != nil {
			errMsg := fmt.Sprintf("Cannot parse request body: %v", err)
			return ctx.Status(fiber.StatusInternalServerError).SendString(errMsg)
		}
		result := graphql.Do(graphql.Params{
			Schema:         schema,
			RequestString:  input.Query,
			OperationName:  input.OperationName,
			VariableValues: input.Variables,
		})
		ctx.Set("Content-Type", "application/graphql-response+json")
		return ctx.JSON(result)
	}

	// Handle GET requests
	app.Get("/", graphqlHandler)

	// Handle POST requests
	app.Post("/", graphqlHandler)

	log.Fatal(app.Listen(":8080"))
}
