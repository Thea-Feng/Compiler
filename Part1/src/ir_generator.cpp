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

#include "ir_generator.hpp"
void IR_Generator::init(){
    this->prcnt = this->sccnt = this->regcnt = 0;
}
void IR_Generator::export_ast_to_llvm_ir(Node* node) {
    /* TODO: your program here */
    out << "; Declare printf\n" << "declare i32 @printf(i8*, ...)\n\n"
    << "; Declare scanf\n" << "declare i32 @scanf(i8*, ...)\n\n"
    << "define i32 @main() {\n";
    init();
    gen_llvm_ir(node);
    out << "\tret i32 0\n" << "}\n";

}
bool IR_Generator::isAllocVariable(std::string id){
    return aloc.find(id) != aloc.end();
}
void IR_Generator::alocVariable(std::string id){
    aloc[id] = "%" + id;
    out << "\t" << aloc[id] << " = alloca i32\n";
}
void IR_Generator::genRead(Node *node) {
    int number = node->children.size() * 3;
    out << "\t\%_scanf_format_" << (++sccnt) << " = alloca [" << number << " x i8]\n";
    
    out << "\tstore [" << number << " x i8] c\"%d";
    for(int i = 1; i < node->children.size(); i++) out << " %d";
    out << "\\00\", [" << number << " x i8]* \%_scanf_format_" << sccnt << "\n";

    out << "\t\%_scanf_str_" << sccnt << " = getelementptr [" << number << " x i8], ["
    << number << " x i8]* \%_scanf_format_" << sccnt << ", i32 0, i32 0\n";

    out << "\tcall i32 (i8*, ...) @scanf(i8* \%_scanf_str_" << sccnt;
    for(auto it = node->children.begin(); it != node->children.end(); it++)
        out << ", i32* " << aloc[(*it)->lexeme];
    out << ")\n";
}
void IR_Generator::genWrite(Node *node, std::vector<std::string> printReg) {
    int number = node->children.size() * 3 + 1;
    out << "\t\%_printf_format_" << (++prcnt) << " = alloca [" << number << " x i8]\n";
    
    out << "\tstore [" << number << " x i8] c\"%d";
    for(int i = 1; i < node->children.size(); i++) out << " %d";
    out << "\\0A\\00\", " << "[" << number << " x i8]* \%_printf_format_" << prcnt << "\n";

    out << "\t\%_printf_str_" << prcnt << " = getelementptr [" << number << " x i8], ["
    << number << " x i8]* \%_printf_format_" << prcnt << ", i32 0, i32 0\n";

    out << "\tcall i32 (i8*, ...) @printf(i8* \%_printf_str_" << prcnt;
    for(auto it = printReg.begin(); it != printReg.end(); it++)
        out << ", i32 " << (*it);
    out << ")\n";
}
void IR_Generator::storeReg(std::string addr, std::string rg){
    out << "\tstore i32 " << rg << ", i32* " << addr << "\n";
    return;
}
std::string IR_Generator::loadReg(std::string addr){
    std::string ret = "\%_tmp_" + std::to_string(++regcnt);
    out << "\t" << ret << " = load i32, i32* " << addr << "\n";
    return ret;
}
std::string IR_Generator::add(std::string lf, std::string rg){
    std::string ret = "\%_tmp_" + std::to_string(++regcnt);
    out << "\t" << ret << " = add i32 " << lf << ", " << rg << "\n";
    return ret;
}
std::string IR_Generator::sub(std::string lf, std::string rg){
    std::string ret = "\%_tmp_" + std::to_string(++regcnt);
    out << "\t" << ret << " = sub i32 " << lf << ", " << rg << "\n";
    return ret;
}
std::string IR_Generator::gen_llvm_ir(Node* node) {
    /* TODO: Your program here */
    if(node->lexeme == "<program>" || node->lexeme == "<statement list>") {
        for(auto it = node->children.begin(); it != node->children.end(); it++){
            gen_llvm_ir(*it);
        }
        return "";
    }
    if(node->lexeme == "read"){
        for(auto it = node->children.begin(); it != node->children.end(); it++)
                if(!isAllocVariable((*it)->lexeme)) alocVariable((*it)->lexeme);
            genRead(node);
        return "";
    }
    if(node->lexeme == "write"){
        std::vector<std::string> regList;
        for(auto it = node->children.begin(); it != node->children.end(); it++)
            if(isAllocVariable((*it)->lexeme)) 
                regList.push_back(loadReg(aloc[(*it)->lexeme]));
            else {
                std::string tmp = gen_llvm_ir(*it);
                regList.push_back(tmp);
            }
        genWrite(node, regList);
        return "";
    }
    if(node->lexeme == ":="){
        if(!isAllocVariable(node->children[0]->lexeme)) 
            alocVariable(node->children[0]->lexeme);
        std::string tmp = gen_llvm_ir(node->children[1]);
        storeReg(aloc[node->children[0]->lexeme], tmp);
        return "";
    }
    if(node->lexeme == "+"){
        std::string lf, rg;
        lf = gen_llvm_ir(node->children[0]);
        rg = gen_llvm_ir(node->children[1]);
        std::string ret = add(lf, rg);
        return ret;
    }
    if(node->lexeme == "-") {
        std::string lf, rg;
        lf = gen_llvm_ir(node->children[0]);
        rg = gen_llvm_ir(node->children[1]);
        std::string ret = sub(lf, rg);
        return ret;
    }
    if(isAllocVariable(node->lexeme))   
        return loadReg(aloc[node->lexeme]);
    else return node->lexeme;
}
