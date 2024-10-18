/**
 * --------------------------------------
 * CUHK-SZ CSC4180: Compiler Construction
 * Assignment 2: Oat v.1 Scanner
 * --------------------------------------
 * Author: Mr.Liu Yuxuan
 * Position: Teaching Assisant
 * Date: February 27th, 2024
 * Email: yuxuanliu1@link.cuhk.edu.cn
 * 
 * File: lexer.l
 * -----------------------------
 * This file implements some lexical analysis rules to scan the input file 
 * and return the tokens which will be used later for parser
 */
%option yylineno 
%{
/* C/C++ Stuff (headers, declarations, variables, etc.) */
#include <cstdio>
#include <string>
#include <vector>

int yyerror (char *s);

int yylex();
%}



%%

for {
  printf("FOR for\n");
}
while {
  printf("WHILE while\n");
}
if {
  printf("IF if\n");
}
else {
  printf("ELSE else\n");
}
var {
  printf("VAR var\n");
}
new {
  printf("NEW new\n");
}
global {
  printf("GLOBAL global\n"); 
}
return {
  printf("RETURN return\n");
}
int {
  printf("TINT int\n");
}
bool {
  printf("TBOOL bool\n");
}
string {
  printf("TSTRING string\n");
}
\( {
  printf("LPAREN (\n");
}
\) {
  printf("RPAREN )\n");
}
\[ {
  printf("LBRACKET [\n");
}
\] {
  printf("RBRACKET ]\n");
}
\{ {
  printf("LBRACE {\n");
}
\} {
  printf("RBRACE }\n");
}
; {
  printf("SEMICOLON ;\n");
}
, {
  printf("COMMA ,\n");
}
\* {
  printf("STAR *\n");
}
\+ {
  printf("PLUS +\n");
}
- {
  printf("MINUS -\n");
}
\<< {
  printf("LSHIFT <<\n");
}
>>> {
  printf("RASHIFT >>>\n");
}
>> {
  printf("RLSHIFT >>\n");
}

>= {
  printf("GREATEQ >=\n");
}
\<= {
  printf("LESSEQ <=\n");
}

\< {
  printf("LESS <\n");
}
> {
  printf("GREAT >\n");
}
== {
  printf("EQ ==\n");
}
!= {
  printf("NEQ !=\n");
}
& {
  printf("LAND &\n");
}
\| {
  printf("LOR |\n");
}
\[&\] {
  printf("BAND [&]\n");
}
\[\|\] {
  printf("BOR [|]\n");
}
= {
  printf("ASSIGN =\n");
}
[0-9]+ {
  printf("INTLITERAL %s\n", yytext);
}
null {
  printf("NUL null\n");
}
void {
  printf("TVOID void\n");
}
true {
  printf("TRUE true\n");
}
false {
  printf("FALSE false\n");
}
! {
  printf("NOT !\n");
}
~ {
  printf("TILDE ~\n");
}

[a-zA-Z][a-zA-Z0-9_]* {
  printf("ID %s\n", yytext);
}
[0-9]+ {
  printf("INTLITERAL %s\n", yytext);
}
\/\*([^*]|\*+[^*/])*\*+\/ {
  printf("COMMENT %s\n", yytext);
}
\"(.)*\" {
  printf("STRINGLITERAL %s\n", yytext);
}
[ \t\n]+ {/* ignore spaces */}
%%

int main(int argc, char **argv)
{
  yylex();
  yywrap();
}

int yywrap (void) {return 1;}

int yyerror(char *s, ...){
  fprintf(stderr, "%d: error:", yylineno);
  return 1;
}
