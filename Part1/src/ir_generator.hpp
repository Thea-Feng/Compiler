/**
 * --------------------------------------
 * CUHK-SZ CSC4180: Compiler Construction
 * Assignment 1: Micro Language Compiler
 * --------------------------------------
 * Author: Mr.Liu Yuxuan
 * Position: Teaching Assisant
 * Date: January 25th, 2024
 * Email: yuxuanliu1@link.cuhk.edu.cn
 * 
 * This file defines the LLVM IR Generator class, which generate LLVM IR (.ll) file given the AST from parser.
 */

#ifndef CSC4180_IR_GENERATOR_HPP
#define CSC4180_IR_GENERATOR_HPP

#include "node.hpp"

/**
 * TODO: LLVM IR Generator of Micro Language
 * It takes the AST generated from parser and generate LLVM IR instructions.
 */
class IR_Generator {
public:
    IR_Generator(std::ofstream &output)
        : out(output) {}

    /**
     * TODO: Export AST to LLVM IR file
     * 
     * It calls gen_llvm_ir recursively to generate LLVM IR instruction for each node in the AST
     * 
     * @param node
     * @return
     */
    void export_ast_to_llvm_ir(Node* node);
    /**
     * TODO: Recursively generate LLVM IR of the given AST tree node
     * 
     * Should have different logic for different symbol classes
     * 
     * @note: this should be a recursive function
     */
    std::string gen_llvm_ir(Node* node);
    void init();
    bool isAllocVariable(std::string id);
    void alocVariable(std::string id);
    void genRead(Node *node);
    void genWrite(Node *node, std::vector<std::string>);
    void storeReg(std::string addr, std::string rg);
    std::string loadReg(std::string addr);
    std::string add(std::string lf, std::string rg);
    std::string sub(std::string lf, std::string rg);



    /* Add any function you want here */

private:
    std::ofstream &out;
    int prcnt, sccnt, regcnt;
    std::map <std::string, std::string> aloc;

 };

#endif  // CSC4180_IR_GENERATOR_HPP
