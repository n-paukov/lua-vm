grammar lua;

root: block EOF;

block: statement* return_statement?;

statement
    : ';'                                   #colon_statement
    | left_tuple=variables_tuple op='=' right_tuple=expressions_tuple #assignment_statement
    | function_call                         #call_statement
    | 'break'                               #break_statement
    | 'do' block 'end'                      #do_loop_statement
    | 'while' expression 'do' block 'end'   #while_loop_statement
    | 'repeat' block 'until' expression     #repeat_loop_statement
    | 'if' expression 'then' block ('elseif' expression 'then' block)* ('else' block)? 'end' #if_block_statement
    | 'for' IDENTIFIER '=' expression ',' expression (',' expression)? 'do' block 'end'      #for_loop_statement
    | 'for' entry=identifiers_tuple 'in' collection=expressions_tuple 'do' block 'end'                        #foreach_loop_statement
    | 'function' function_name function_body                                                 #function_decl_statement
    | 'local' 'function' local_function_name function_body                                   #local_function_statement
    | 'local' left=identifiers_tuple (op='=' right=expressions_tuple)?                                     #local_variables_statement
    ;

return_statement: 'return' expressions_tuple? ';'?;
function_name: IDENTIFIER ('.' IDENTIFIER)* (':' IDENTIFIER)?;
local_function_name: IDENTIFIER;

variables_tuple: variable (',' variable)*;

identifiers_tuple: IDENTIFIER (',' IDENTIFIER)*;

expressions_tuple: expression ((',') expression)*;

expression
    : 'nil'                                                            #nil_literal_expression
    | 'false'                                                          #false_literal_expression
    | 'true'                                                           #true_literal_expression
    | number                                                           #number_literal_expression
    | string                                                           #string_literal_expression
    | '...'                                                            #ellipsis_expression
    | function_expr                                                    #function_expression
    | handle=value_handle args=args_expression*                                          #value_handle_expression
    | table_declaration                                                      #table_declaration_expression
    | <assoc=right> left=expression op='^' right=expression                  #xor_expression
    | op=('not' | '#' | '-' | '~') right=expression                          #unary_expression
    | left=expression op=( '*' | '/' | '%' | '//') right=expression          #binary_term_expression
    | left=expression op=( '+' | '-' ) right=expression                      #binary_expr_expression
    | <assoc=right> left=expression op='..' right=expression                 #concat_expression
    | left=expression op=('<' | '>' | '<=' | '>=' | '~=' | '==') right=expression #equal_expression
    | left=expression op='and' right=expression                                   #and_expression
    | left=expression op='or' right=expression                                                  #or_expression
    | right=expression op=('&' | '|' | '~' | '<<' | '>>') right=expression                       #bit_expression
    ;

function_call: (varpointer=variable | varexpr='(' expression ')') args=args_expression+;

value_handle: variable | '(' expression ')';

variable: (IDENTIFIER | '(' expression ')' variable_expr_suffix) variable_expr_suffix*;
variable_expr_suffix: args_expression* ('[' expression ']' | '.' IDENTIFIER);

args_expression: (':' IDENTIFIER)? function_args;

function_args: '(' expressions_tuple? ')' | table_declaration | string;
function_expr: 'function' function_body;
function_body: '(' parameters_list? ')' block 'end';
parameters_list: identifiers_tuple (',' '...')? | '...';

table_declaration: '{' table_fields_list? '}';
table_fields_list: table_field ((',' | ';') table_field)* (',' | ';')?;
table_field: '[' expression ']' '=' expression | IDENTIFIER '=' expression | expression;

number: INT | FLOAT;
string: DOUBLE_QUOTE_STRING | SINGLE_QUOTE_STRING;

// TOKENS

IDENTIFIER: [a-zA-Z_][a-zA-Z_0-9]*;

DOUBLE_QUOTE_STRING: '"' ( ESCAPED_SYMBOLS | ~('\\'|'"') )* '"';
SINGLE_QUOTE_STRING: '\'' ( ESCAPED_SYMBOLS | ~('\''|'\\') )* '\'';

INT: Digit+;

FLOAT
    : Digit+ '.' Digit* EXPONENT?
    | '.' Digit+ EXPONENT?
    | Digit+ EXPONENT
    ;

fragment
EXPONENT: [eE] [+-]? Digit+;

fragment
ESCAPED_SYMBOLS: '\\' [abfnrtvz"'\\] | '\\' '\r'? '\n';

fragment
Digit: [0-9];

fragment
NESTED_STR: '=' NESTED_STR '='| '[' .*? ']';

COMMENT: '--[' NESTED_STR ']' -> channel(HIDDEN);
LINE_COMMENT: '--' ~('['|'\r'|'\n') ~('\r'|'\n')* ('\r\n'|'\r'|'\n'|EOF) -> channel(HIDDEN);

WS: [ \t\u000C\r\n]+ -> skip;
