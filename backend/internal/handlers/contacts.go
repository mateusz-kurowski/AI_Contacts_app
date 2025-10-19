package handlers

import (
	"errors"
	"net/http"

	"contactsAI/contacts/internal/config"
	"contactsAI/contacts/internal/db"
	"contactsAI/contacts/internal/routeutils"

	"github.com/gin-gonic/gin"
	"github.com/jackc/pgx/v5"
)

func RegisterContactsRoutes(router *gin.RouterGroup, env *config.Env) {
	apiGroup := router.Group("/contacts")
	apiGroup.GET("/", func(c *gin.Context) { GetContacts(c, env) })
	apiGroup.GET("/:id", func(c *gin.Context) { GetContactByID(c, env) })
	apiGroup.POST("/", func(c *gin.Context) { CreateContact(c, env) })
	apiGroup.PUT("/:id", func(c *gin.Context) { UpdateContact(c, env) })
	apiGroup.DELETE("/:id", func(c *gin.Context) { DeleteContact(c, env) })
}

type CreateContactBody struct {
	Name  string `json:"name"  binding:"required"`
	Phone string `json:"phone" binding:"required,phonenumber"`
}

func CreateContact(c *gin.Context, env *config.Env) {
	var json CreateContactBody
	if err := c.ShouldBindJSON(&json); err != nil {
		c.JSON(http.StatusBadRequest, ErrorResponse(err.Error()))
		return
	}

	contact := db.CreateContactParams{
		Name:  json.Name,
		Phone: json.Phone,
	}
	createdContact, err := env.CreateContact(c, contact)
	if err != nil {
		c.JSON(http.StatusInternalServerError, ErrorResponse("Failed to create contact"))
		return
	}
	c.JSON(http.StatusCreated, SuccessResponse(createdContact))
}

func GetContacts(c *gin.Context, env *config.Env) {
	contacts, err := env.Queries.GetContacts(c)
	if err != nil {
		c.JSON(http.StatusInternalServerError, ErrorResponse(err.Error()))
		return
	}
	if contacts == nil {
		contacts = []db.Contact{}
	}
	c.JSON(http.StatusOK, SuccessResponse(contacts))
}

func GetContactByID(c *gin.Context, env *config.Env) {
	contactID, err := routeutils.GetInt32FromPath(c, "id")
	if err != nil {
		c.JSON(http.StatusBadRequest, ErrorResponse("Invalid contact ID"))
		return
	}

	contact, err := env.GetContactByID(c, contactID)
	if err != nil {
		if errors.Is(err, pgx.ErrNoRows) {
			c.JSON(http.StatusNotFound, ErrorResponse("Contact not found"))
			return
		}
		c.JSON(http.StatusInternalServerError, ErrorResponse(err.Error()))
		return
	}

	c.JSON(http.StatusOK, SuccessResponse(contact))
}

type UpdateContactBody struct {
	Name  string `json:"name"  binding:"required"`
	Phone string `json:"phone" binding:"required,phonenumber"`
}

func UpdateContact(c *gin.Context, env *config.Env) {
	contactID, parseErr := routeutils.GetInt32FromPath(c, "id")
	if parseErr != nil {
		c.JSON(http.StatusBadRequest, ErrorResponse("Invalid contact ID"))
		return
	}

	var json UpdateContactBody
	if bindErr := c.BindJSON(&json); bindErr != nil {
		c.JSON(http.StatusBadRequest, ErrorResponse(bindErr.Error()))
		return
	}
	contactParams := db.UpdateContactParams{
		ID:    contactID,
		Name:  json.Name,
		Phone: json.Phone,
	}

	contact, updateErr := env.UpdateContact(c, contactParams)
	if updateErr != nil {
		c.JSON(http.StatusInternalServerError, ErrorResponse("Updating contact failed."))
		return
	}
	c.JSON(http.StatusOK, SuccessResponse(contact))
}

func DeleteContact(c *gin.Context, env *config.Env) {
	id, err := routeutils.GetInt32FromPath(c, "id")
	if err != nil {
		c.JSON(http.StatusBadRequest, ErrorResponse("Invalid contact ID"))
		return
	}

	if err = env.DeleteContact(c, id); err != nil {
		if errors.Is(err, pgx.ErrNoRows) {
			c.JSON(http.StatusNotFound, ErrorResponse("Contact not found"))
			return
		}
		c.JSON(http.StatusInternalServerError, ErrorResponse(err.Error()))
		return
	}
	c.JSON(http.StatusNoContent, nil)
}
