# Copyright (c) 2024 Liu Yuxuan
# Email: yuxuanliu1@link.cuhk.edu.cn
#
# This code is licensed under MIT license (see LICENSE file for details)
#
# This code is for teaching purpose of course: CUHKSZ's CSC4180: Compiler Construction
# as Assignment 4: Oat v.1 Compiler Frontend to LLVM IR using llvmlite
#
# Copyright (c)
# Oat v.1 Language was designed by Prof.Steve Zdancewic when he was teaching CIS 341 at U Penn.
# 

import sys                          # for CLI argument parsing
import llvmlite.binding as llvm     # for llvmlite IR generation
import llvmlite.ir as ir            # for llvmlite IR generation
import pydot                        # for .dot file parsing
from enum import Enum               # for enum in python

DEBUG = False

class SymbolTable:
    """
    Symbol table is a stack of maps, and each map represents a scope

    The key of map is the lexeme (string, not unique) of an identifier, and the value is its type (DataType)

    The size of self.scopes and self.scope_ids should always be the same
    """
    def __init__(self):
        """
        Initialize the symbol table with no scope inside
        """
        self.id_counter = 0      # Maintain an increment counter for each newly pushed scope
        self.scopes = []         # map<str, DataType> from lexeme to data type in one scope
        self.scope_ids = []      # stores the ID for each scope
        # self.scopes_llvm = []
        # self.scope_ids_llvm = []      # stores the ID for each scope for llwm
        self.index_name = {}

    def print(self):
        for table_idx in range(len(self.scopes) - 1, -1, -1):
            for x in self.scopes[table_idx]:
                print(table_idx, x, self.scopes[table_idx][x])
            
    def push_scope(self):
        """
        Push a new scope to symbol table

        Returns:
            - (int) the ID of the newly pushed scope
        """
        self.id_counter += 1
        # self.scopes_llvm.append({})
        self.scopes.append({})   # push a new table (mimics the behavior of stack)
        self.scope_ids.append(self.id_counter)
        return self.id_counter

    def pop_scope(self):
        """
        Pop a scope out of symbol table, usually called when the semantic analysis for one scope is finished
        """
        self.scopes.pop()    # pop out the last table (mimics the behavior of stack)
        self.scope_ids.pop()

    def unique_name(self, lexeme, scope_id):
        """
        Compute the unique name for an identifier in one certain scope

        Args:
            - lexeme(str)
            - scope_id(int)
        
        Returns:
            - str: the unique name of identifier used for IR codegen
        """
        return lexeme + "-" + str(scope_id)

    def insert(self, lexeme, type, index=-1):
        """
        Insert a new symbol to the top scope of symbol table

        Args:
            - lexeme(str): lexeme of the symbol
            - type(DataType): type of the symbol
        
        Returns:
            - (str): the unique ID of the symbol
        """
        # check the size of scopes and scope_id
        if len(self.scopes) != len(self.scope_ids):
            raise ValueError("Mismatch size of symbol_table and id_table")
        scope_idx = len(self.scopes) - 1
        self.scopes[scope_idx][lexeme] = type
        # self.scopes_llvm[scope_idx][lexeme] = self.scope_ids[scope_idx]
        if lexeme == 'main':
            unique_name = lexeme
        else:
            unique_name = self.unique_name(lexeme, self.scope_ids[scope_idx])
        self.index_name[index] = self.scope_ids[scope_idx]
        return unique_name
    
    def lookup_local(self, lexeme, index):
        """
        Lookup a symbol in the top scope of symbol table only
        called when we want to declare a new local variable

        Args:
            - lexeme(str): lexeme of the symbol

        Returns:
            - (str, DataType): 2D tuple of unique_id and data type if the symbol is found
            - None if the symbol is not found
        """
        if len(self.scopes) != len(self.scope_ids):
            raise ValueError("Mismatch size of symbol_table and id_table")
        table_idx = len(self.scopes) - 1
        if lexeme in self.scopes[table_idx]:
            unique_name = self.unique_name(lexeme, self.scope_ids[table_idx])
            type = self.scopes[table_idx][lexeme]
            self.index_name[index] = self.scope_ids[table_idx]
            return unique_name, type
        else:
            return None

    def lookup_global_llvm(self, lexeme, index):
        if index in self.index_name:
            return self.index_name[index]
        else:
            return 1
    
    def lookup_global(self, lexeme, index):
        """
        Lookup a symbol in all the scopes of symbol table (stack)
        called when we want to search a lexeme or declare a global variable

        Args:
            - lexeme(str): lexeme of the symbol

        Returns:
            - (str, DataType): 2D tuple of unique_id and data type if the symbol is found
            - None if the symbol is not found
        """
        if len(self.scopes) != len(self.scope_ids):
            raise ValueError("Mismatch size of symbol_table and id_table")
        for table_idx in range(len(self.scopes) - 1, -1, -1):
            if lexeme in self.scopes[table_idx]:
                unique_name = self.unique_name(lexeme, self.scope_ids[table_idx])
                type = self.scopes[table_idx][lexeme]
                self.index_name[index] = self.scope_ids[table_idx]
                return unique_name, type
        return None

# Global Symbol Table for Semantic Analysis
symbol_table = SymbolTable()

# Global Context of LLVM IR Code Generation
module = ir.Module()                    # Global LLVM IR Module
builder = ir.IRBuilder()                # Global LLVM IR Builder
ir_map = {}                             # Global Map from unique names to its LLVM IR item

class TreeNode:
    def __init__(self, index, lexeme):
        self.index = index              # [int] ID of the TreeNode, used for visualization 
        self.lexeme = lexeme            # [str] lexeme of the node (may have naming conflicts, and needs unique name in IR codegen)
        self.id = ""                    # [str] unique name of the node (used in IR codegen), filled in semantic analysis
        self.nodetype = NodeType.NONE   # [NodeType] type of node, used to determine which actions to do with the current node in semantic analysis or IR codegen
        self.datatype = DataType.NONE   # [DataType] data type of node, filled in semantic analysis and used in IR codegen
        self.children = []              # Array of childern TreeNodes

    def add_child(self, child_node):
        self.children.append(child_node)

def print_tree(node, level = 0):
    print("  " * level + '|' + node.lexeme.replace("\n","\\n") + ", " + node.nodetype.name)
    for child in node.children:
        print(child.lexeme, child.nodetype)
    print('-----------------------')
    for child in node.children:
        print_tree(child, level + 1)

def visualize_tree(root_node, output_path):
    """
    Visulize TreeNode in Graphviz

    Args:
        - root_node(TreeNode)
        - output_path(str): the output path for png file 
    """
    # construct pydot Node from TreeNode with label
    def pydot_node(tree_node):
        node = pydot.Node(tree_node.index)
        label = tree_node.nodetype.name
        if len(tree_node.id) > 0:
            label += "\n" + tree_node.id.replace("\\n","\/n")
        elif len(tree_node.lexeme) > 0:
            label += "\n" + tree_node.lexeme.replace("\\n","\/n")
        label += "\ntype: " + tree_node.datatype.name
        node.set("label", label)
        return node
    # Recursively visualize node
    def visualize(node, graph):
        # Add Root Node Only
        if node.index == 0:
            graph.add_node(pydot_node(node))
        # Add Children Nodes and Edges
        for child in node.children:
            graph.add_node(pydot_node(child))
            graph.add_edge(pydot.Edge(node.index, child.index))
            visualize(child, graph)
    # Output visualization png graph
    graph = pydot.Dot(graph_type="graph")
    visualize(root_node, graph)
    graph.write_png(output_path)

def construct_tree_from_dot(dot_filepath):
    """
    Read .dot file, which records the AST from parser

    Args:
        - dot_filepath(str): path of the .dot file

    Return:
        - TreeNode: the root node of the AST
    """
    # Extract the first graph from the list (assuming there is only one graph in the file)
    graph = pydot.graph_from_dot_file(dot_filepath)[0]
    # Initialize Python TreeNode structure
    nodes = []
    # code_type_map = { member.value: member for member in NodeType }
    # Add nodes
    for node in graph.get_nodes():
        if len(node.get_attributes()) == 0: continue
        index = int(node.get_name()[4:])
        # print(node.get_attributes(), node.get_attributes()['label'], node.get_attributes()['lexeme'])
        label = node.get_attributes()["label"][1:-1]    # exlcude enclosing quotes
        lexeme = node.get_attributes()['lexeme'][1:-1]  # exclude enclosing quotes
        tree_node = TreeNode(index, lexeme)
        tree_node.lexeme = lexeme
        tree_node.nodetype = { member.value: member for member in NodeType }[label] if any(label == member.value for member in NodeType) else NodeType.NONE
        # if DEBUG: print("Index: ", index, ", lexeme: ", lexeme, ", nodetype: ", tree_node.nodetype)

        nodes.append(tree_node)
    # Add Edges
    for edge in graph.get_edges():
        src_id = int(edge.get_source()[4:])
        dst_id = int(edge.get_destination()[4:])
        nodes[src_id].add_child(nodes[dst_id])
    # root node should always be the first node
    return nodes[0]

class NodeType(Enum):
    """
    Map lexeme of AST node to code type in IR generation

    The string value here is to convert the token class by bison to Python NodeType
    """
    PROGRAM = "<program>"
    GLOBAL_DECL = "<global_decl>"     # global variable declaration
    FUNC_DECL = "<function_decl>"       # function declaration
    VAR_DECLS = "<var_decls>"
    VAR_DECL = "<var_decl>"        # variable declaration
    ARGS = "<args>"
    ARG = "<arg>"
    REF = "<ref>"
    GLOBAL_EXPS = "<global_exps>"
    STMTS = "<stmts>"
    EXPS = "<exps>"
    FUNC_CALL = "<func call>"       # function call
    ARRAY_INDEX = "<array index>"    # array element retrieval by index
    IF_STMT = "IF"         # if-else statement (nested case included)
    ELSE_STMT = "ELSE"
    FOR_LOOP = "FOR"        # for loop statement (nested case included)
    WHILE_LOOP = "WHILE"      # while loop statement (nested case included)
    RETURN = "RETURN"          # return statement
    NEW = "NEW"         # new variable with/without initialization
    ASSIGN = "ASSIGN"         # assignment (lhs = rhs)
    EXP = "<exp>"     # expression (including a lot of binary operators)
    TVOID = "void"
    TINT = "int"
    TSTRING = "string"
    TBOOL = "bool"
    NULL = "NULL"
    TRUE = "TRUE"
    FALSE = "FALSE"
    STAR = "STAR"
    PLUS = "PLUS"
    MINUS = "MINUS"
    LSHIFT = "LSHIFT"
    RLSHIFT = "RLSHIFT"
    RASHIFT = "RASHIFT"
    LESS = "LESS"
    LESSEQ = "LESSEQ"
    GREAT = "GREAT"
    GREATEQ = "GREATEQ"
    EQ = "EQ"
    NEQ = "NEQ"
    LAND = "LAND"
    LOR = "LOR"
    BAND = "BAND"
    BOR = "BOR"
    NOT = "NOT"
    TILDE = "TILDE"
    INTLITERAL = "INTLITERAL"
    STRINGLITERAL = "STRINGLITERAL"
    ID = "ID"
    NONE = "unknown"         # unsupported

class DataType(Enum):
    INT = 1             # INT refers to Int32 type (32-bit Integer)
    BOOL = 2            # BOOL refers to Int1 type (1-bit Integer, 1 for True and 0 for False)
    STRING = 3          # STRING refers to an array of Int8 (8-bit integer for a single character)
    INT_ARRAY = 4       # Array of integers, no need to support unless for bonus
    BOOL_ARRAY = 5      # Array of booleans, no need to support unless for bonus
    STRING_ARRAY = 6    # Array of strings, no need to support unless for bonus
    VOID = 7            # Void, you can choose whether to support it or not
    NONE = 8            # Unknown type, used as initialized value for each TreeNode

def ir_type(data_type, array_size = 1):
    map = {
        DataType.INT: ir.IntType(32),       # integer is in 32-bit
        DataType.BOOL: ir.IntType(32),      # bool is also in 32-bit, 0 for false and 1 for True
        DataType.STRING: ir.ArrayType(ir.IntType(8), array_size),   # extra \0 (null terminator)
        DataType.INT_ARRAY: ir.ArrayType(ir.IntType(32), array_size),
        DataType.BOOL_ARRAY: ir.ArrayType(ir.IntType(32), array_size),
        DataType.STRING_ARRAY: ir.ArrayType(ir.ArrayType(ir.IntType(8), 32), array_size),   # string max size = 32 for string array 
    }
    type = map.get(data_type)
    if type:
        return type
    else:
        raise ValueError("Unsupported data type: ", data_type)

def declare_runtime_functions():
    """
    Declare built-in functions for Oat v.1 Language
    """
    # int32_t* array_of_string (char *str)
    func_type = ir.FunctionType(
        ir.PointerType(ir.IntType(32)),     # return type
        [ir.PointerType(ir.IntType(8))])    # args type
    # map function unique name in global scope to the function body
    # the global scope should have scope_id = 1 
    func = ir.Function(module, func_type, name="array_of_string")
    ir_map[symbol_table.unique_name(lexeme="array_of_string", scope_id=1)] = func
    # char* string_of_array (int32_t *arr)
    func_type = ir.FunctionType(
        ir.PointerType(ir.IntType(8)),      # return type
        [ir.PointerType(ir.IntType(32))])   # args type
    func = ir.Function(module, func_type, name="string_of_array")
    ir_map[symbol_table.unique_name("string_of_array", 1)] = func
    # int32_t length_of_string (char *str)
    func_type = ir.FunctionType(
        ir.IntType(32),                      # return type
        [ir.PointerType(ir.IntType(8))])    # args type
    func = ir.Function(module, func_type, name="length_of_string")
    ir_map[symbol_table.unique_name("length_of_string", 1)] = func
    # char* string_of_int(int32_t i)
    func_type = ir.FunctionType(
        ir.PointerType(ir.IntType(8)),      # return type
        [ir.IntType(32)])                   # args type
    func = ir.Function(module, func_type, name="string_of_int")
    ir_map[symbol_table.unique_name("string_of_int", 1)] = func
    # char* string_cat(char* l, char* r)
    func_type = ir.FunctionType(
        ir.PointerType(ir.IntType(8)),      # return tyoe
        [ir.PointerType(ir.IntType(8)), ir.PointerType(ir.IntType(8))]) # args type
    func = ir.Function(module, func_type, name="string_cat")
    ir_map[symbol_table.unique_name("string_cat", 1)] = func
    # void print_string (char* str)
    func_type = ir.FunctionType(
        ir.VoidType(),                      # return type
        [ir.PointerType(ir.IntType(8))])    # args type
    func = ir.Function(module, func_type, name="print_string")
    ir_map[symbol_table.unique_name("print_string", 1)] = func
    # void print_int (int32_t i)
    func_type = ir.FunctionType(
        ir.VoidType(),                      # return type
        [ir.IntType(32)])                   # args type
    func = ir.Function(module, func_type, name="print_int")
    ir_map[symbol_table.unique_name("print_int", 1)] = func
    # void print_bool (int32_t i)
    func_type = ir.FunctionType(
        ir.VoidType(),                      # return type
        [ir.IntType(32)])                   # args type
    func = ir.Function(module, func_type, name="print_bool")
    ir_map[symbol_table.unique_name("print_bool", 1)] = func

def codegen(node):
    """
    Recursively do LLVM IR generation

    Call corresponding handler function for each NodeType

    Different NodeTypes may be mapped to the same handelr function

    Args:
        node(TreeNode)
    """
    codegen_func_map = {
        NodeType.GLOBAL_DECL: codegen_handler_global_decl,
        # TODO: add more mappings from NodeType to its handler function of IR generation
        NodeType.FUNC_DECL: codegen_handler_function_declare,
        NodeType.VAR_DECL: codegen_handler_variable_declare,
        # NodeType.TVOID: codegen_handler_void,
        # NodeType.REF: codegen_handler_string,
        NodeType.ID: codegen_handler_id,
        NodeType.FUNC_CALL: codegen_handler_func_call,       
        NodeType.IF_STMT: codegen_handler_IF,         
        NodeType.FOR_LOOP: codegen_handler_for,        
        NodeType.WHILE_LOOP: codegen_handler_while,      
        NodeType.RETURN: codegen_handler_return,          
        NodeType.ASSIGN: codegen_handler_assign,         
        NodeType.EXPS: codegen_handler_exps,     
        # NodeType.NULL: codegen_handler_void,
        NodeType.STAR: codegen_handler_binop,
        NodeType.PLUS: codegen_handler_binop,
        NodeType.MINUS: codegen_handler_binop,
        NodeType.INTLITERAL: codegen_handler_int,
        NodeType.TRUE: codegen_handler_bool,
        NodeType.FALSE: codegen_handler_bool,
        NodeType.STRINGLITERAL: codegen_handler_string,
        NodeType.LSHIFT: codegen_handler_binop,
        NodeType.RLSHIFT: codegen_handler_binop,
        NodeType.RASHIFT: codegen_handler_binop,
        NodeType.LESS: codegen_handler_binop,
        NodeType.LESSEQ: codegen_handler_binop,
        NodeType.GREAT: codegen_handler_binop,
        NodeType.GREATEQ: codegen_handler_binop,
        NodeType.EQ: codegen_handler_binop,
        NodeType.NEQ: codegen_handler_binop,
        NodeType.LAND: codegen_handler_binop,
        NodeType.LOR: codegen_handler_binop,
        NodeType.BAND: codegen_handler_binop,
        NodeType.BOR: codegen_handler_binop,
        NodeType.TILDE: codegen_handler_uniop,
        NodeType.NOT: codegen_handler_uniop
    }
    codegen_func = codegen_func_map.get(node.nodetype)
    if codegen_func:
        return codegen_func(node)
    else:
        return codegen_handler_default(node)

# Some sample handler functions for IR codegen
# TODO: implement more handler functions for various node types
def codegen_handler_default(node):
    for child in node.children:
        codegen(child)

def codegen_handler_global_decl(node):
    """
    Global variable declaration
    """
    # var_name = node.children[0].lexeme
    # variable = ir.GlobalVariable(module, typ=ir_type(node.datatype), name=var_name)
    # # variable.initializer = ir.Constant(ir_type(node.datatype), )
    # # ir_map[symbol_table.unique_name(var_name, 1)] = variable
    # variable = codegen_handler_variable_declare(node)
    # variable.global_constant = True
    # variable.linkage = "private"
    
    
    var_name = node.children[0].lexeme
    idx = symbol_table.lookup_global_llvm(var_name, node.children[0].index)
    identifier = symbol_table.unique_name(var_name, idx)
    if node.children[0].datatype == DataType.STRING:
        s = (node.children[1].lexeme + '\0').replace('\\n', '\n')
        initializer = bytearray(s.encode("utf8"))
        size = len(initializer)
    else:
        size = 1
    variable = ir.GlobalVariable(module, typ=ir_type(node.children[0].datatype, size), name=identifier)
    if node.children[0].datatype == DataType.STRING:
        variable.initializer = ir.Constant(ir_type(node.children[0].datatype, len(initializer)), initializer)
    elif node.children[0].datatype == DataType.INT:
        variable.initializer = ir.Constant(ir_type(node.children[0].datatype), int(node.children[1].lexeme))
    elif node.childern[0].datatype == DataType.BOOL:
        if node.children[1].nodetype == NodeType.TRUE:
            fg = 1
        else:
            fg = 0
        variable.initializer = ir.Constant(ir_type(node.children[0].datatype), fg)
    else:
        print('Var declare to be done:', node.childern[0].datatype)
        
    variable.linkage = "private"
    variable.global_constant = True    
    ir_map[identifier] = variable
    return variable

def codegen_handler_variable_declare(node, is_global=0):
    '''
    Variable Local Declare
    '''
    var_name = node.children[0].lexeme
    idx = symbol_table.lookup_global_llvm(var_name, node.children[0].index)
    identifier = symbol_table.unique_name(var_name, idx)
    
    if node.children[0].datatype == DataType.STRING:
        s = (node.children[1].lexeme + '\0').replace('\\n', '\n')
        initializer = bytearray(s.encode("utf8"))
        size = len(initializer)
    else:
        size = 1
    variable = builder.alloca(ir_type(node.children[0].datatype, size), name=identifier)
    
    
    if node.children[0].datatype == DataType.STRING:
        # LLVM doesn't support initialized as local variables
        initializer = ir.Constant(ir_type(node.children[0].datatype, size), initializer)
        builder.store(initializer, variable)
        ir_map[identifier] = variable
    elif node.children[0].datatype == DataType.INT:
        initializer = ir.Constant(ir_type(node.children[0].datatype), int(node.children[1].lexeme))
        builder.store(initializer, variable)
        ir_map[identifier] = variable
        
    elif node.children[0].datatype == DataType.BOOL:
        if node.children[1].nodetype == NodeType.TRUE:
            fg = 1
        else:
            fg = 0
        initializer = ir.Constant(ir_type(node.children[0].datatype), fg)
        builder.store(initializer, variable)
        ir_map[identifier] = variable
    else:
        print('Var declare to be done:', node.childern[0].datatype)
        
   
    return variable
    
    

def codegen_handler_function_declare(node):
    """
    Function declaration
    """
    ret_type, func_name_str, args, stmts = node.children
    func_name = func_name_str.lexeme
    idx = symbol_table.lookup_global_llvm(func_name, func_name_str.index)
    if func_name != "main":
        func_name = symbol_table.unique_name(func_name, idx)
    func_return_type = ir_type(ret_type.datatype)
    func_args_types = [ir_type(arg[0].datatype) for arg in args.children]
    func_type = ir.FunctionType(func_return_type, func_args_types)
    
    function = ir.Function(module, func_type, name=func_name)
    
    entry_block = function.append_basic_block('entry')
    builder.position_at_end(entry_block)
    for i, arg in enumerate(function.args):
        arg.name = args.children[i][1].lexeme
    codegen(stmts)
    # builder.ret_void()
    ir_map[func_name] = function

def codegen_handler_return(node):
    """
    Handle return 
    """
    if node.children:
        ret_val = codegen(node.children[0])
        # ?convert to pointer (bonus)
        # print('return:', ret_val)
        builder.ret(ret_val)
    else:
        builder.ret_void()


def codegen_handler_id(node, is_lval=0):
    """
    Handle ID
    """
    identifier = symbol_table.unique_name(node.lexeme, symbol_table.lookup_global_llvm(node.lexeme, node.index))
    if identifier in ir_map:
        ir_entity = ir_map[identifier]
        print('find id', identifier, ir_entity)
        if isinstance(ir_entity, ir.Function) or is_lval:
            return ir_entity
        elif isinstance(ir_entity, ir.GlobalVariable):
            return ir_entity
        else:
            return builder.load(ir_entity, name=identifier)


def codegen_handler_IF(node):
    """
    Handle if statements 
    """
    condition = codegen(node.children[0])
    
    
    if_block = builder.append_basic_block(name="if_block")
    if len(node.children) > 2:
        else_block = builder.append_basic_block(name="else_block")
    else:
        else_block = None
    merge_block = builder.append_basic_block(name="merge_block")
    builder.cbranch(condition, if_block, else_block)
    
    
    builder.position_at_end(if_block)
    codegen(node.children[1])
    builder.branch(merge_block)
    
    if else_block:
        builder.position_at_end(else_block)
        codegen(node.children[2])
        builder.branch(merge_block)

    builder.position_at_end(merge_block)
    
    


def codegen_handler_assign(node):
    """
    Handle assignment 
    """
    target = codegen_handler_id(node.children[0], 1)  
    value = codegen(node.children[1])  
    print('assign: ', target.type, value.type)
    builder.store(value, target)


def codegen_handler_binop(node):
    """
    Handle binary operators 
    """
    left = codegen(node.children[0])
    right = codegen(node.children[1])
    if isinstance(left.type, ir.PointerType):
        left = builder.load(left, name='loadtmp')
    if isinstance(right.type, ir.PointerType):
        right = builder.load(right, name='loadtmp')
    print('binop', node, left, right)
    if node.nodetype == NodeType.PLUS:
        return builder.add(left, right, name='addtmp')
    elif node.nodetype == NodeType.MINUS:
        return builder.sub(left, right, name='subtmp')
    elif node.nodetype == NodeType.STAR:
        return builder.mul(left, right, name='multmp')
    elif node.nodetype == NodeType.LSHIFT:
        return builder.shl(left, right, name='shltmp')
    elif node.nodetype == NodeType.RLSHIFT:
        return builder.lshr(left, right, name='lshrtmp')
    elif node.nodetype == NodeType.RASHIFT:
        return builder.ashr(left, right, name='ashrtmp')
    elif node.nodetype == NodeType.LESS:
        return builder.icmp_signed('<', left, right, name='lesstmp')
    elif node.nodetype == NodeType.LESSEQ:
        return builder.icmp_signed('<=', left, right, name='lesseqtmp')
    elif node.nodetype == NodeType.GREAT:
        return builder.icmp_signed('>', left, right, name='greattmp')
    elif node.nodetype == NodeType.GREATEQ:
        return builder.icmp_signed('>=', left, right, name='greateqtmp')
    elif node.nodetype == NodeType.EQ:
        return builder.icmp_signed('==', left, right, name='eqtmp')
    elif node.nodetype == NodeType.NEQ:
        return builder.icmp_signed('!=', left, right, name='neqtmp')
    # elif node.nodetype == NodeType.LAND:
    #     codegen_logical_and(left, right)
    # elif node.nodetype == NodeType.LOR:
    #     codegen_logical_or(left, right)
    elif node.nodetype == NodeType.BAND:
        return builder.and_(left, right, name='bandtmp')
    elif node.nodetype == NodeType.BOR:
        return builder.or_(left, right, name='bortmp')
        

def codegen_handler_while(node):
    """
    Handle while loops
    """
    loop_cond_block = builder.append_basic_block('loop_cond')
    loop_body_block = builder.append_basic_block('loop_body')
    loop_end_block = builder.append_basic_block('loop_end')

    # Jump to condition check from current block
    builder.branch(loop_cond_block)

    # Build the condition check
    builder.position_at_end(loop_cond_block)
    cond_value = codegen(node.children[0])
    builder.cbranch(cond_value, loop_body_block, loop_end_block)

    # Build the loop body
    builder.position_at_end(loop_body_block)
    codegen(node.children[1])  
    builder.branch(loop_cond_block) 

    builder.position_at_end(loop_end_block)

def codegen_handler_for(node):
    """
    Handle for loops
    """
    codegen(node.children[0])
    loop_cond_block = builder.append_basic_block('loop_cond')
    loop_body_block = builder.append_basic_block('loop_body')
    loop_increment_block = builder.append_basic_block('loop_inc')
    loop_end_block = builder.append_basic_block('loop_end')

    builder.branch(loop_cond_block)

    builder.position_at_end(loop_cond_block)
    cond_value = codegen(node.children[1])
    builder.cbranch(cond_value, loop_body_block, loop_end_block)

    builder.position_at_end(loop_body_block)
    codegen(node.children[3])  
    builder.branch(loop_increment_block)

    builder.position_at_end(loop_increment_block)
    codegen(node.children[2])  
    builder.branch(loop_cond_block)

    builder.position_at_end(loop_end_block)

name_idx = 0
def get_new_name():
    global name_idx
    name = 'constant' + str(name_idx)
    while name in ir_map:
        name_idx += 1
        name = 'constant' + str(name_idx)
    return name

def codegen_handler_func_call(node):
    """
    Handle function calls and generate corresponding LLVM IR code.
    """
    func_name = node.children[0].lexeme
    func = module.get_global(func_name)
    call_args = []
    for arg in node.children[1].children:
        if arg.nodetype in [NodeType.STRINGLITERAL, NodeType.INTLITERAL, NodeType.TRUE, NodeType.FALSE]:
            call_args.append(codegen(arg))
        else:
            call_args.append(codegen_handler_id(arg, 1))
    expected_type = func.function_type.args
    actual_args = []
    for i, arg in enumerate(call_args):
        expected_type, arg_type = expected_type[i], arg.type
        print(expected_type, arg_type)
        if isinstance(expected_type, ir.PointerType) and isinstance(arg_type, ir.PointerType) and isinstance(arg_type.pointee, ir.ArrayType):
            if expected_type.pointee == ir.IntType(8):
                print("here", arg)
                zero = ir.Constant(ir.types.IntType(32), 0)
                variable_pointer = builder.gep(arg, [zero, zero], inbounds=True)
                actual_args.append(variable_pointer)
            else:
                print("To be finish")
        elif not isinstance(expected_type, ir.PointerType) and isinstance(arg_type, ir.PointerType):
            arg = builder.load(arg)
            actual_args.append(arg)
        elif isinstance(expected_type, ir.PointerType) and isinstance(arg_type, ir.ArrayType):
            if expected_type.pointee == ir.IntType(8):
                # print("goes this way")
                variable_pointer = ir.GlobalVariable(module, arg_type, name=get_new_name())
                variable_pointer.initializer = arg
                zero = ir.Constant(ir.types.IntType(32), 0)
                variable_first_pointer = builder.gep(variable_pointer, [zero, zero], inbounds=True)
                actual_args.append(variable_first_pointer)
        else:
            actual_args.append(arg)
        
    # print('function:',func)
    # print('actual arguments:',actual_args)
    # print('actual arguments', actual_args)
    return builder.call(func, actual_args, name='calltmp') 
 
def codegen_handler_uniop(node):
    """
    Handle logical operators like AND, OR and generate corresponding LLVM IR code.
    """
    var = codegen(node.children[1])
    # to be finish
    if node.nodetype == NodeType.TILDE:
        return builder.not_(var, name='nottmp')
    # elif node.nodetype == NodeType.NOT:
    #     return codegen_logical_not(var)    

def codegen_handler_exps(node):
    ret = []
    for child in node.children:
        exp = codegen(child)
        if exp:
            ret.append(exp)
    return ret
  
def semantic_analysis(node):
    """
    Perform semantic analysis on the root_node of AST

    Args:
        node(TreeNode)

    Returns:
        (DataType): datatype of the node
    """
    handler_map = {
        NodeType.PROGRAM: semantic_handler_program,
        NodeType.ID: semantic_handler_id,
        NodeType.TINT: semantic_handler_int,
        NodeType.TBOOL: semantic_handler_bool,
        NodeType.TSTRING: semantic_handler_string,
        NodeType.INTLITERAL: semantic_handler_int,
        NodeType.STRINGLITERAL: semantic_handler_string,
        NodeType.TRUE: semantic_handler_bool,
        NodeType.FALSE: semantic_handler_bool,
        NodeType.GLOBAL_DECL: semantic_handler_global_declare,
        NodeType.FUNC_DECL: semantic_handler_function_declare,
        NodeType.VAR_DECL: semantic_handler_variable_declare,
        NodeType.ARG: semantic_handler_arg,
        NodeType.TVOID: semantic_handler_void,
        NodeType.REF: semantic_handler_string,
        # NodeType.GLOBAL_EXPS: semantic_handler_global_exps,
        NodeType.STMTS: semantic_handler_stmts,
        NodeType.FUNC_CALL: semantic_handler_func_call,       
        NodeType.IF_STMT: semantic_handler_IF,         
        # NodeType.ELSE_STMT: semantic_handler_ELSE,
        NodeType.FOR_LOOP: semantic_handler_FOR,        
        NodeType.WHILE_LOOP: semantic_handler_WHILE,      
        NodeType.RETURN: semantic_handler_return,          
        NodeType.ASSIGN: semantic_handler_assign,         
        NodeType.EXP: semantic_handler_exp,     
        NodeType.NULL: semantic_handler_void,
        NodeType.STAR: semantic_handler_binop,
        NodeType.PLUS: semantic_handler_binop,
        NodeType.MINUS: semantic_handler_binop,
        NodeType.LSHIFT: semantic_handler_binop,
        NodeType.RLSHIFT: semantic_handler_binop,
        NodeType.RASHIFT: semantic_handler_binop,
        NodeType.LESS: semantic_handler_binop,
        NodeType.LESSEQ: semantic_handler_binop,
        NodeType.GREAT: semantic_handler_binop,
        NodeType.GREATEQ: semantic_handler_binop,
        NodeType.EQ: semantic_handler_binop,
        NodeType.NEQ: semantic_handler_binop,
        NodeType.LAND: semantic_handler_binop,
        NodeType.LOR: semantic_handler_binop,
        NodeType.BAND: semantic_handler_binop,
        NodeType.BOR: semantic_handler_binop,
        # TODO: add more mapping from NodeType to its corresponding handler functions here
    }
    handler = handler_map.get(node.nodetype)
    # print(node.lexeme, str(handler))
    if handler:
        handler(node)
    else:
        default_handler(node)
    return node.datatype

def codegen_handler_int(node):
    return ir.Constant(ir_type(node.datatype), int(node.lexeme))

def codegen_handler_string(node):
    s = (node.lexeme + '\0').replace('\\n', '\n')
    val = bytearray(s.encode("utf8"))
    return ir.Constant(ir_type(node.datatype, len(val)), val)

def codegen_handler_bool(node):
    if node.nodetype == NodeType.TRUE:
        fg = 1
    else:
        fg = 0
    return ir.Constant(ir_type(node.datatype), fg)

def semantic_handler_program(node):
    symbol_table.push_scope()
    # insert built-in function names in global scope symbol table
    symbol_table.insert("array_of_string", DataType.INT_ARRAY)
    symbol_table.insert("string_of_array", DataType.STRING)
    symbol_table.insert("length_of_string", DataType.INT)
    symbol_table.insert("string_of_int", DataType.STRING)
    symbol_table.insert("string_cat", DataType.STRING)
    symbol_table.insert("print_string", DataType.VOID)
    symbol_table.insert("print_int", DataType.VOID)
    symbol_table.insert("print_bool", DataType.BOOL)
    # recursively do semantic analysis in left-to-right order for all children nodes
    for child in node.children:
        semantic_analysis(child)
    symbol_table.pop_scope()

# Some Sample handler functions
# TODO: define more hanlder functions for various node types
def semantic_handler_id(node):
    # symbol_table.print()
    if symbol_table.lookup_global(node.lexeme, node.index) is None:
        raise ValueError("Variable not defined: ", node.lexeme)
    else:
        node.id, node.datatype = symbol_table.lookup_global(node.lexeme, node.index)

def semantic_handler_global_declare(node):
    var, val = node.children
    semantic_analysis(val)
    # var.datatype = val.datatype
    
    if symbol_table.lookup_global(var.lexeme, var.index) is not None:
        raise ValueError("Variable already defined: ", var.lexeme)
    symbol_table.insert(var.lexeme, val.datatype, var.index)
    semantic_analysis(var)
    node.children = [var, val]
    node.datatype = node.children[0].datatype
    
def semantic_handler_IF(node):
    exp, stmt, else_stmt = node.children
    semantic_analysis(exp)
    semantic_analysis(stmt)
    semantic_analysis(else_stmt)
   
def semantic_handler_WHILE(node):   
    exp, stmts = node.children
    semantic_analysis(exp)
    default_handler(stmts)
    node.children = [exp, stmts]
    
def semantic_handler_FOR(node):
    symbol_table.push_scope()
    default_handler(node.children[0]) # declare variables
    semantic_analysis(node.children[1]) # condition
    semantic_analysis(node.children[2]) # increment
    semantic_analysis(node.children[3]) # stmts
    symbol_table.pop_scope()
    
def semantic_handler_function_declare(node):
    _type, _id, args, stmts = node.children
    scope_id = symbol_table.push_scope()
    
    semantic_analysis(_type)
    semantic_analysis(args)
    semantic_analysis(stmts)
    func_name = _id.lexeme
    
    # for ch in args.children:
    #     func_name += str(ch.datatype)
    func_type = _type.datatype
    # print("Declare function", func_name)
    # arguments are valid?
    if symbol_table.lookup_global(func_name, _id.index) is not None:
        raise ValueError("Function already defined: ", func_name)
    if func_type != stmts.datatype:
        raise ValueError("Function return type does not match: ", func_name, func_type, stmts.datatype)
    symbol_table.insert(func_name, func_type, _id.index)
    symbol_table.pop_scope()
    
def semantic_handler_func_call(node):
    default_handler(node)
    func_name_node, args = node.children
    func_name = func_name_node.lexeme
    # for child in node.children:
    #     func_name += str(child.datatype)
    # print("Call function", func_name)
    if symbol_table.lookup_global(func_name, func_name_node.index) is None:
        raise ValueError("Function not defined")
    func = symbol_table.lookup_global(func_name, func_name_node.index)
    
def semantic_handler_arg(node):
    _type, _id = node.children
    if symbol_table.lookup_local(_id.lexeme, _id.index) is not None:
        raise ValueError("Variable already defined: ", _id.lexeme)
    
    semantic_analysis(_type)
    symbol_table.insert(_id.lexeme, _type.datatype, _id.index)
    semantic_analysis(_id)
    node.children = [_id, _type]
    
def semantic_handler_assign(node):
    default_handler(node)
    left, right = node.children
    if left.datatype != right.datatype:
        raise ValueError("Binary operator type mismatch: ", node.lexeme, left.lexeme, right.lexeme)
        
def semantic_handler_variable_declare(node):
    var, val = node.children
    semantic_analysis(val)
    # var.datatype = val.datatype
    
    if symbol_table.lookup_local(var.lexeme, var.index) is not None:
        raise ValueError("Variable already defined: ", var.lexeme)
    symbol_table.insert(var.lexeme, val.datatype, var.index)
    semantic_analysis(var)
    node.children = [var, val]
    node.datatype = val.datatype

def semantic_handler_stmts(node):
    symbol_table.push_scope()
    for child in node.children:
        semantic_analysis(child)
        if child.nodetype == NodeType.RETURN:
            node.datatype = child.datatype
    symbol_table.pop_scope()
    

def semantic_handler_exp(node):    
    return None

def semantic_handler_return(node):
    if node.children:
        semantic_analysis(node.children[0])
        node.datatype = node.children[0].datatype
    else:
        node.datatype = DataType.VOID

def semantic_handler_int(node):
    node.datatype = DataType.INT

def semantic_handler_bool(node):
    node.datatype = DataType.BOOL

def semantic_handler_string(node):
    node.datatype = DataType.STRING

def semantic_handler_void(node):
    node.datatype = DataType.VOID
  
def semantic_handler_binop(node):
    left, right = node.children
    semantic_analysis(left)
    semantic_analysis(right)
    if left.datatype != right.datatype:
        raise ValueError("Binary operator type mismatch: ", node.lexeme, left.lexeme, left.datatype, right.lexeme, right.datatype)
    node.datatype = left.datatype

def default_handler(node):
    for child in node.children:
        semantic_analysis(child)


if len(sys.argv) == 3:
    # visualize AST before semantic analysis
    dot_path = sys.argv[1]
    ast_png_before_semantic_analysis = sys.argv[2]
    root_node = construct_tree_from_dot(dot_path)
    if DEBUG: print_tree(root_node)
    visualize_tree(root_node, ast_png_before_semantic_analysis)
elif len(sys.argv) == 4:
#     # visualize AST after semantic analysis
# if __name__ == "__main__":
    # dot_path, ast_png_before_semantic_analysis, ast_png_after_semantics_analysis, llvm_ir = 'testcases/ast/test3.dot', 'testcases/ast/test3-before.png', 'testcases/output/test3-after.png', './llvm_ir/test3-self.ll'
    dot_path = sys.argv[1]
    ast_png_after_semantics_analysis = sys.argv[2]
    llvm_ir = sys.argv[3]
    root_node = construct_tree_from_dot(dot_path)
    semantic_analysis(root_node)
    visualize_tree(root_node, ast_png_after_semantics_analysis)
    ## Uncomment the following when you are trying the do IR generation
    # # init llvm
    llvm.initialize()
    llvm.initialize_native_target()
    llvm.initialize_native_asmprinter()
    declare_runtime_functions()
    
    codegen(root_node)
    # # print LLVM IR
    with open(llvm_ir, 'w') as f:
        f.write(str(module))
    print(module)
else:
    raise SyntaxError("Usage: python3 a4.py <.dot> <.png before>\nUsage: python3 ./a4.py <.dot> <.png after> <.ll>")
