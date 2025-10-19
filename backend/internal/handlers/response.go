package handlers

import "contactsAI/contacts/internal/strutils"

type Response[T any] struct {
	Message *string `json:"message,omitempty"`
	Data    T       `json:"data,omitempty"`
}

func NewResponse[T any](message *string, data T) Response[T] {
	return Response[T]{
		Message: message,
		Data:    data,
	}
}

func SuccessResponse[T any](data T) Response[T] {
	return NewResponse(nil, data)
}

func ErrorResponse(message string) Response[struct{}] {
	return NewResponse(strutils.PointStr(message), struct{}{})
}
