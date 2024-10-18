#!bin/bash

make all

mkdir -p ./output

for test_idx in {0..5}; do
    test="test$test_idx"
    test_program="./testcases/test$test_idx.oat"
    echo "$test"
    # tokens
    ./scanner $test_program > ./testcases/${test}_scanner.txt
    ./lexer < $test_program > ./testcases/${test}_lexer.txt
    if diff -q ./testcases/${test}_scanner.txt ./testcases/${test}_lexer.txt; then
        echo "|--Pass"
    else
        echo "|--Failed"
        diff ./testcases/${test}_scanner.txt ./testcases/${test}_lexer.txt
    fi
done