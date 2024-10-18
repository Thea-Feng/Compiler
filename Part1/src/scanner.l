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
 * This file implements some lexical analysis rules to scan the input file 
 * and return the tokens which will be used for parser 
 */
%option yylineno noyywrap
%{
/* C/C++ Stuff (headers, declarations, variables, etc.) */
#include <cstdio>
#include <string>
#include <vector>
#include "parser.hpp"
#include "node.hpp"

int yyerror (char *s);

int yylex();

/**
 * scan_only indicates whehter the flex scanner should print out the token information for debug.
 * The token information is in the following form:
 *   <token-class, lexeme>
 */
extern int scan_only;
%}

/* TODO: define some regular expressions here */

%%
begin {
    Node *node = new Node(SymbolClass::BEGIN_, "");
    yylval.ptr = node;
    if(scan_only) printf("BEGIN _begin\n");return BEGIN_;
    }
end {
    Node *node = new Node(SymbolClass::END, "");
    yylval.ptr = node;
    if(scan_only)  printf("END end\n");return END;}
read {
    Node *node = new Node(SymbolClass::READ, "");
    yylval.ptr = node;
    if(scan_only)  printf("READ read\n");return READ;}
write {
    Node *node = new Node(SymbolClass::WRITE, "");
    yylval.ptr = node;
    if(scan_only)  printf("WRITE write\n");return WRITE;}
\( {
    Node *node = new Node(SymbolClass::LPAREN, "");
    yylval.ptr = node;
    if(scan_only)  printf("LPAREN (\n");return LPAREN;}
\) {
    Node *node = new Node(SymbolClass::RPAREN, "");
    yylval.ptr = node;
    if(scan_only)  printf("RPAREN )\n");return RPAREN;}
; {
    Node *node = new Node(SymbolClass::SEMICOLON, "");
    yylval.ptr = node;
    if(scan_only)  printf("SEMICOLON ;\n");return SEMICOLON;}
, {
    Node *node = new Node(SymbolClass::COMMA, "");
    yylval.ptr = node;
    if(scan_only)  printf("COMMMA ,\n");return COMMA;}
:= {
    Node *node = new Node(SymbolClass::ASSIGNOP, "");
    yylval.ptr = node;
    if(scan_only)  printf("ASSIGNOP :=\n");return ASSIGNOP;}
\+ {
    Node *node = new Node(SymbolClass::PLUSOP, "");
    yylval.ptr = node;
    if(scan_only)  printf("PLUSOP +\n");return PLUSOP;}
- {
    Node *node = new Node(SymbolClass::MINUSOP, "");
    yylval.ptr = node;
    if(scan_only)  printf("MINUSOP -\n");return MINUSOP;}
[a-zA-Z][a-zA-Z0-9]{0,31} {
    Node *node = new Node(SymbolClass::ID, yytext);
    yylval.ptr = node;
    if(scan_only) printf("ID %s\n", yytext); return ID;
    }
[0-9]+ {
    Node *node = new Node(SymbolClass::INTLITERAL, yytext);
    yylval.ptr = node;
    if(scan_only) printf("INTLITERAL %s\n", yytext); 
    return INTLITERAL;
    }
<<EOF>> {
    if(scan_only)  {printf("SCANEOF\n");return 0;}
    Node *node = new Node(SymbolClass::SCANEOF, "");
    yylval.ptr = node;
    return SCANEOF;
    }
--.*\n {}
[ \t\n]+ {/* ignore spaces */}

%%

void yyerror(char *s, ...){
    /*va_list ap;
    va_satrt(ap, s);

    fprintf(stderr, "%d: error: ", yylineno);
    vprintf(stderr, s, ap);
    fprintf(stderr, "\n");*/
}

/*
int main(){
    nodeNume = 0;
    dFile = fopen("ATS.dot","w");
    if(!dFile){
        printf("No file\n");
        return 1;
    }
    int a = yyparse();
    fclose(dFile);
    return a;
}*/
/* int yywrap (void) {return 1;} */
