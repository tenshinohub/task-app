# Makefile for building the task C library into lib/

CC = gcc
CFLAGS = -Wall -fPIC

SRC = src/c/task.c
LIB_DIR = lib

# Linux/Mac shared library
LIB_NAME = $(LIB_DIR)/libtask.so

all: $(LIB_NAME)

$(LIB_NAME): $(SRC) | $(LIB_DIR)
	$(CC) $(CFLAGS) -shared -o $(LIB_NAME) $(SRC)

$(LIB_DIR):
	mkdir -p $(LIB_DIR)

clean:
	rm -f $(LIB_NAME)
