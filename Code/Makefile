# Makefile for the Nagel-Schreckenberg Traffic Model code
# Starting point of a "Peachy Assignment"

CXX = g++
CXXFLAGS = -O2 -march=native -std=c++17 -g -Wall
LDFLAGS = -g
OBJS = traffic.o parameters.o npywriter.o

all: traffic

traffic.o: traffic.cpp parameters.h npywriter.h
	$(CXX) -c $(CXXFLAGS) -o $@ $<

parameters.o: parameters.cpp parameters.h
	$(CXX) -c $(CXXFLAGS) -o $@ $<

npywriter.o: npywriter.cpp npywriter.h
	$(CXX) -c $(CXXFLAGS) -o $@ $<

traffic: ${OBJS}
	$(CXX) $(LDFLAGS) -o $@ $^ $(LDLIBS)

clean:
	$(RM) $(OBJS)

distclean: clean
	$(RM) traffic traffic-????.npy traffic.png test-????.npy largetest-????.npy test.png largetest.png

test: traffic test.ini
	time ./traffic test.ini && python npyplot.py test.ini

largetest: traffic largetest.ini
	time ./traffic largetest.ini && python npyplot.py largetest.ini

.PHONY: all clean distclean run 
