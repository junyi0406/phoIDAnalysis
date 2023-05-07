
# $@: target
# $?: all prerequisites newer than the target
# $^: all prerequisites
# $<: first dependency

cc = g++ # compiler name
CPPFLAGS = -Wall -g -c
# -Wall: turn on all the warning
# -g: turn on the debug info
flag = $(shell root-config --cflags --glibs --libs)
INC = include
LDLIBS = -lhpdfs
SRC:=src
OBJ:=obj
PHOALGOSRC:= PhoVarAlgo/src

SOURCES := $(wildcard $(SRC)/*.cpp $(PHOALGOSRC)/*.cpp)
OBJECTS := $(patsubst $(SRC)/%.cpp, $(OBJ)/%.o, $(SOURCES))


bin/main.out : $(OBJECTS)
	$(cc) $^ -o $@ $(flag)

$(OBJ)/%.o: $(SRC)/%.cpp 
	$(cc) -I$(SRC) -c $< $(CPPFLAGS) $(flag) -o $@ 
$(OBJ)/%.o: $(PHOALGOSRC)/%.cpp 
	$(cc) -I$(PHOALGOSRC) -c $< $(CPPFLAGS) $(flag) -o $@ 


# $(addprefix obj/, %.o) : $(addprefix src/, %.cpp)
# 	$(cc)   $^ -o $@



.PHONY: clean

clean :
	rm obj/*.o



