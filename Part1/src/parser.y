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
 * This file implements some syntax analysis rules and works as a parser
 * The grammar tree is generated based on the rules and MIPS Code is generated
 * based on the grammar tree and the added structures and functions implemented
 * in File: added_structure_function.c
 */

%{
/* C declarations used in actions */
#include <cstdio>     
#include <cstdlib>
#include <cstring>
#include <string>
#include <vector>
#include <ctype.h>

#include "node.hpp"
using namespace std;
int yyerror (char *s);

int yylex();

extern "C" int yylineno;
extern int cst_only;
string getLabel(SymbolClass a);
Node* root_node = nullptr;
%}

// TODO: define yylval data types with %union
%union {
	struct Node * ptr;
	int d;
	char *s;
}
%start START
// TODO: define terminal symbols with %token. Remember to set the type.
%token <ptr> BEGIN_ END READ WRITE LPAREN RPAREN SEMICOLON COMMA ASSIGNOP PLUSOP MINUSOP SCANEOF INTLITERAL ID 
// Start Symbol
// TODO: define Non-Terminal Symbols with %type. Remember to set the type.
%type <ptr> START PROGRAM STATEMENT STATEMENT_LIST ID_LIST EXPRESSION EXPRESSION_LIST PRIMARY ADD_OP

%%
/**
 * Format:
 * Non-Terminal  :  [Non-Terminal, Terminal]+ (production rule 1)   { parser actions in C++ }
 *                  | [Non-Terminal, Terminal]+ (production rule 2) { parser actions in C++ }
 *                  ;
 */

// TODO: your production rule here
// The tree generation logic should be in the operation block of each production rule


START: PROGRAM SCANEOF { 
	if(cst_only){
		Node *node = new Node(SymbolClass::START, "");
		node->append_child($1);
		node->append_child($2);
		root_node = node;
	}
	return 0;
	
}

PROGRAM: BEGIN_ STATEMENT_LIST END {
	if(cst_only){
		Node *node = new Node(SymbolClass::PROGRAM, "");
		node->append_child($1);
		node->append_child($2);
		node->append_child($3);
		$$ = node;
	} else {
		root_node = new Node(SymbolClass::PROGRAM);
		root_node->append_child($2);
	}
	
}
STATEMENT_LIST: STATEMENT{
	Node *node = new Node(SymbolClass::STATEMENT_LIST, "");
	node->append_child($1);
	$$ = node;
	
} | STATEMENT_LIST STATEMENT{
	if(cst_only){
		Node *node = new Node(SymbolClass::STATEMENT_LIST, "");
		node->append_child($1);
		node->append_child($2);
		$$ = node;	
	} else {
		($1)->append_child($2);
		$$ = $1;
	}
}
STATEMENT: ID ASSIGNOP EXPRESSION SEMICOLON{
	if(cst_only){
		Node *node = new Node(SymbolClass::STATEMENT, "");

		node->dVal = ($3)->dVal;
		node->sVal = ($1)->sVal;

		node->append_child($1);
		node->append_child($2);
		node->append_child($3);
		node->append_child($4);	
		$$ = node;
	} else {
		$$ = new Node(SymbolClass::ASSIGNOP, ":=");
		($$)->append_child($1);
		($$)->append_child($3);
	}


} | READ LPAREN ID_LIST RPAREN SEMICOLON{
	if(cst_only){
		Node *node = new Node(SymbolClass::STATEMENT);
		node->append_child($1);
		node->append_child($2);
		node->append_child($3);
		node->append_child($4);
		node->append_child($5);

		$$ = node;	
	} else {
		Node *node = new Node(SymbolClass::READ, "read");
		for(auto it = ($3)->children.begin(); it != ($3)->children.end(); it++) {
			node->append_child(*it);
		}
		$$ = node;
	}
	//generate code

} | WRITE LPAREN EXPRESSION_LIST RPAREN SEMICOLON {
	if(cst_only){
		Node *node = new Node(SymbolClass::STATEMENT, "");
		node->append_child($1);
		node->append_child($2);
		node->append_child($3);
		node->append_child($4);
		node->append_child($5);

		$$ = node;	
	} else {
		Node *node = new Node(SymbolClass::WRITE, "write");
		for(auto it = ($3)->children.begin(); it != ($3)->children.end(); it++) {
			node->append_child(*it);
		}
		$$ = node;
	}
	//generate code
}
ID_LIST: ID{
	Node *node = new Node(SymbolClass::ID_LIST, "");
	node->append_child($1);
	$$ = node;	
	
} | ID COMMA ID_LIST {
	if(cst_only){
		Node *node = new Node(SymbolClass::ID_LIST, "");
		node->append_child($1);
		node->append_child($2);
		node->append_child($3);

		$$ = node;	
	} else {
		($3)->append_child_first($1);
		$$ = $3;
	}

}
EXPRESSION_LIST: EXPRESSION {
	Node *node = new Node(SymbolClass::EXPRESSION_LIST, "");
	node->append_child($1);
	$$ = node;

}| EXPRESSION_LIST COMMA EXPRESSION {
	if(cst_only){
		Node *node = new Node(SymbolClass::EXPRESSION_LIST, "");
		node->append_child($1);
		node->append_child($2);
		node->append_child($3);

		$$ = node;	
	} else {
		($1)->append_child($3);
		$$ = $1;
	}
}
EXPRESSION: PRIMARY {
	if(cst_only){
		Node *node = new Node(SymbolClass::EXPRESSION, "");

		node->dVal = ($1)->dVal;

		node->append_child($1);
		$$ = node;	
	} else {
		$$ = $1;
	}

}| EXPRESSION ADD_OP PRIMARY {
	if(cst_only){
		Node *node = new Node(SymbolClass::EXPRESSION, "");
		node->append_child($1);
		node->append_child($2);
		node->append_child($3);

		$$ = node;	
	} else {
		($2)->append_child($1);
		($2)->append_child($3);
		$$ = $2;
	}
	

}
PRIMARY: LPAREN EXPRESSION RPAREN  {
	if(cst_only){
		Node *node = new Node(SymbolClass::PRIMARY, "");
		node->sVal = ($2)->sVal;
		node->dVal = ($2)->dVal;

		node->append_child($1);
		node->append_child($2);
		node->append_child($3);
		$$ = node;	
	} else {
		$$ = $2;
	}
} | ID {
	if(cst_only){
		Node *node = new Node(SymbolClass::PRIMARY, ""); 
		node->append_child($1);
		$$ = node;	
	} else {
		$$ = $1;
	}
}| INTLITERAL {
	if(cst_only){
		Node *node = new Node(SymbolClass::PRIMARY, "");
		node->append_child($1);
		$$ = node;	
	} else {
		$$ = $1;
	}
} | MINUSOP INTLITERAL {
	if(cst_only){
		Node *node = new Node(SymbolClass::PRIMARY, "");
		node->append_child($2);
		$$ = node;	
	} else {
		$$ = new Node(SymbolClass::INTLITERAL, "-" + ($2)->lexeme);
	}
}

ADD_OP: MINUSOP {
	if(cst_only){
		Node *node = new Node(SymbolClass::MINUSOP, "");
		$$ = node;	
	} else {
		$$ = new Node(SymbolClass::MINUSOP, "-");
	}
}
| PLUSOP {
	if(cst_only){
		Node *node = new Node(SymbolClass::PLUSOP, "");
		$$ = node;
	} else {
		$$ = new Node(SymbolClass::PLUSOP, "+");	
	}
}


%%


int yyerror(char *s) {
	printf("%s on line %d\n", s, yylineno);
	return 0;
}

