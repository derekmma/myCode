CC = g++
CFLAGS = -g
HEADERS = board.h queen.h
SOURCES = board.cpp queen.cpp 8queen.cpp
OBJS = board.o queen.o 8queen.o

TARGET = 8queen

$(TARGET):$(OBJS)
	$(CC) $(CFLAGS) $(OBJS) -o $(TARGET)

$(OBJS):$(SOURCES) $(HEADERS)
	$(CC) $(CFLAGS) -c $(SOURCES)

tidy:
	\rm -rf $(OBJS) *~

clean:tidy
	\rm -rf $(TARGET)
