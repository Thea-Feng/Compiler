/* A Bison parser, made by GNU Bison 3.0.4.  */

/* Bison interface for Yacc-like parsers in C

   Copyright (C) 1984, 1989-1990, 2000-2015 Free Software Foundation, Inc.

   This program is free software: you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation, either version 3 of the License, or
   (at your option) any later version.

   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with this program.  If not, see <http://www.gnu.org/licenses/>.  */

/* As a special exception, you may create a larger work that contains
   part or all of the Bison parser skeleton and distribute that work
   under terms of your choice, so long as that work isn't itself a
   parser generator using the skeleton or a modified version thereof
   as a parser skeleton.  Alternatively, if you modify or redistribute
   the parser skeleton itself, you may (at your option) remove this
   special exception, which will cause the skeleton and the resulting
   Bison output files to be licensed under the GNU General Public
   License without this special exception.

   This special exception was added by the Free Software Foundation in
   version 2.2 of Bison.  */

#ifndef YY_YY_PARSER_HPP_INCLUDED
# define YY_YY_PARSER_HPP_INCLUDED
/* Debug traces.  */
#ifndef YYDEBUG
# define YYDEBUG 0
#endif
#if YYDEBUG
extern int yydebug;
#endif

/* Token type.  */
#ifndef YYTOKENTYPE
# define YYTOKENTYPE
  enum yytokentype
  {
    NUL = 258,
    TRUE_ = 259,
    FALSE_ = 260,
    TVOID = 261,
    TINT = 262,
    TSTRING = 263,
    TBOOL = 264,
    IF = 265,
    ELSE = 266,
    WHILE = 267,
    FOR = 268,
    RETURN = 269,
    NEW = 270,
    VAR = 271,
    GLOBAL = 272,
    SCANEOF = 273,
    SEMICOLON = 274,
    COMMA = 275,
    ASSIGN = 276,
    INTLITERAL = 277,
    STRINGLITERAL = 278,
    ID = 279,
    LPAREN = 280,
    RPAREN = 281,
    LBRACKET = 282,
    RBRACKET = 283,
    LBRACE = 284,
    RBRACE = 285,
    BOR = 286,
    BAND = 287,
    LOR = 288,
    LAND = 289,
    EQ = 290,
    NEQ = 291,
    LESS = 292,
    LESSEQ = 293,
    GREAT = 294,
    GREATEQ = 295,
    LSHIFT = 296,
    RLSHIFT = 297,
    RASHIFT = 298,
    PLUS = 299,
    MINUS = 300,
    STAR = 301,
    UMINUS = 302,
    NOT = 303,
    TILDE = 304
  };
#endif

/* Value type.  */
#if ! defined YYSTYPE && ! defined YYSTYPE_IS_DECLARED

union YYSTYPE
{
#line 34 "parser.y" /* yacc.c:1909  */

    struct Node *node;
    std::string *string;
    int integer;

#line 110 "parser.hpp" /* yacc.c:1909  */
};

typedef union YYSTYPE YYSTYPE;
# define YYSTYPE_IS_TRIVIAL 1
# define YYSTYPE_IS_DECLARED 1
#endif


extern YYSTYPE yylval;

int yyparse (void);

#endif /* !YY_YY_PARSER_HPP_INCLUDED  */
