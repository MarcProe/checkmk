# Copyright (C) 2019 tribe29 GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

# TODO(sp) We should really use autotools here...
ifneq ($(shell which g++-12 2>/dev/null),)
        CXX := g++-12 -std=c++17
else ifneq ($(shell which clang++-14 2>/dev/null),)
        CXX := clang++-14 -std=c++17
else ifneq ($(shell which clang++-13 2>/dev/null),)
        CXX := clang++-13 -std=c++17
else ifneq ($(shell which g++-11 2>/dev/null),)
        CXX := g++-11 -std=c++17
else ifneq ($(shell which clang++-12 2>/dev/null),)
        CXX := clang++-12 -std=c++17
else ifneq ($(shell which g++-10 2>/dev/null),)
        CXX := g++-10 -std=c++17
else ifneq ($(shell which clang++-11 2>/dev/null),)
        CXX := clang++-11 -std=c++17
else ifneq ($(shell which clang++-10 2>/dev/null),)
        CXX := clang++-10 -std=c++17
else ifneq ($(shell which g++-9 2>/dev/null),)
        CXX := g++-9 -std=c++17
else ifneq ($(shell which clang++-9 2>/dev/null),)
        CXX := clang++-9 -std=c++17
else ifneq ($(shell which clang++-8 2>/dev/null),)
        CXX := clang++-8 -std=c++17
else ifneq ($(shell which g++-8 2>/dev/null),)
        CXX := g++-8 -std=c++17
else ifneq ($(shell which clang++-7 2>/dev/null),)
        CXX := clang++-7 -std=c++17
else ifneq ($(shell which g++-7 2>/dev/null),)
        CXX := g++-7 -std=c++17
else ifneq ($(shell which clang++-6.0 2>/dev/null),)
        CXX := clang++-6.0 -std=c++17
else ifneq ($(shell which clang++-5.0 2>/dev/null),)
        CXX := clang++-5.0 -std=c++17
else ifneq ($(shell which g++ 2>/dev/null),)
        CXX := g++ -std=c++17
else
        CXX := clang++ -std=c++17
endif

CXXFLAGS    := -gdwarf-4 -O3 -Wall -Wextra
LDFLAGS     := -static-libstdc++

.PHONY: all clean

all: $(EXECUTABLES)

clean:
	$(RM) $(EXECUTABLES)
